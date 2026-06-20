"""问询函相关性标签（v2）：脚本剪枝 + LLM 语义二分类。

该标签器区分三个概念：
- ``inquiry_received``：该公司-年度在年报窗口期内是否收到交易所问询函 / 关注函 / 监管工作函；
- ``reply_received``：是否存在回复函 / 延期公告 / 专项说明等回应类公告；
- ``capitalization_related``：收到的监管函件是否实质针对研发支出资本化、开发支出确认、
  无形资产确认或研发费用资本化政策。

``capitalization_related`` 是问询闭环可行性测试的 ``Y`` 标签；``inquiry_received`` / ``reply_received``
仅用于描述性统计。脚本通过 Tier-1 高置信度关键词直接判定 ``capitalization_related``；
若仅命中 Tier-2 泛词，则将标题 + PDF 首页 / 关键词片段送入 LLM 做语义二分类。
"""

from __future__ import annotations

import csv
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import pdfplumber
from tqdm import tqdm


logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 触发 "capitalization_related" 的高置信度短关键词/短语
TIER_1_KEYWORDS = (
    "资本化",
    "开发支出",
    "研发费用资本化",
    "研发支出资本化",
    "研发投入资本化",
    "研发资本化",
    "资本化条件",
    "资本化政策",
    "资本化时点",
    "资本化标准",
    "开发支出余额",
    "开发支出减值",
    "开发支出转无形资产",
    "研发无形资产",
)

# 仅命中这些泛词时，需要 LLM 语义确认
TIER_2_KEYWORDS = (
    "研发",
    "研发费用",
    "研发投入",
    "无形资产",
)

# 费用化必须和研发/资本化语境同时出现才进入 Tier-1
EXPENSE_CONTEXT_KEYWORDS = ("研发", "研发费用", "研发支出", "研发投入", "资本化")

# 监管函件 vs 回应类公告
REPLY_ROLES = {
    "substantive_reply",
    "delay_notice",
    "supporting_statement",
}
INQUIRY_ROLES = {
    "inquiry_notice",
    "attention_letter",
    "regulatory_work_letter",
    "process_other",
}

MAX_PDF_PAGES = 3
MAX_TEXT_CHARS = 8000
MAX_SNIPPETS = 5


def _clean_text(value: Any) -> str:
    text = re.sub(r"<.*?>", "", str(value or ""))
    return re.sub(r"\s+", "", text)


def _report_year(record: dict[str, str]) -> int:
    doc_id = record.get("doc_id", "")
    match = re.search(r"(20\d{2})年报", doc_id)
    if match:
        return int(match.group(1))
    publish_date = record.get("publish_date", "")[:10]
    try:
        return datetime.strptime(publish_date, "%Y-%m-%d").year - 1
    except ValueError:
        return 0


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _resolve_local_path(project_root: Path, local_path: str) -> Path:
    path = Path(local_path)
    if path.is_absolute():
        return path
    return project_root / path


def extract_pdf_text(pdf_path: Path, max_pages: int = MAX_PDF_PAGES) -> str:
    """Extract text from the first pages of a candidate inquiry PDF."""
    if not pdf_path.exists():
        return ""
    chunks: list[str] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:max_pages]:
                chunks.append(page.extract_text() or "")
    except Exception:
        return ""
    return "\n".join(chunks)[:MAX_TEXT_CHARS]


def _keyword_snippets(text: str, keywords: tuple[str, ...]) -> list[str]:
    snippets: list[str] = []
    compact = re.sub(r"\s+", "", text)
    for keyword in keywords:
        index = compact.find(keyword)
        if index < 0:
            continue
        start = max(0, index - 45)
        end = min(len(compact), index + 95)
        snippet = compact[start:end]
        if snippet and snippet not in snippets:
            snippets.append(snippet)
    return snippets[:MAX_SNIPPETS]


def _keyword_hits(text: str, keywords: tuple[str, ...]) -> list[str]:
    """Return keywords that appear in cleaned text."""
    compact = _clean_text(text)
    return [kw for kw in keywords if kw in compact]


def _classify_keywords(text: str) -> tuple[list[str], list[str]]:
    """Classify keywords in text into (tier_1_hits, tier_2_hits).

    Tier-1 hits directly indicate capitalization-related accounting treatment.
    Tier-2 hits are broad R&D / intangible asset mentions that require LLM review.
    """
    compact = _clean_text(text)
    tier1: list[str] = []

    # Core capitalization and policy terms
    for kw in TIER_1_KEYWORDS:
        if kw in compact and kw not in tier1:
            tier1.append(kw)

    # 费用化 only counts if it appears alongside R&D/capitalization context
    if "费用化" in compact:
        if any(ctx in compact for ctx in EXPENSE_CONTEXT_KEYWORDS):
            if "费用化" not in tier1:
                tier1.append("费用化")

    # Tier-2 = broad keywords that did NOT already trigger Tier-1
    tier2 = [kw for kw in TIER_2_KEYWORDS if kw in compact and kw not in tier1]

    return tier1, tier2


def _is_inquiry_family(role: str | None) -> bool:
    return role in INQUIRY_ROLES


def _is_reply_family(role: str | None) -> bool:
    return role in REPLY_ROLES


LLM_PROMPT_TEMPLATE = """你是一位熟悉中国上市公司信息披露和会计准则的财务分析专家。

请判断以下交易所函件（问询函、关注函或监管工作函）是否**实质针对研发支出资本化、
开发支出确认、无形资产确认或研发费用资本化政策**等会计处理问题。

判断标准：
- 如果函件明确要求公司说明“研发支出资本化条件”“开发支出余额变化”“资本化金额”
  “无形资产确认”“研发费用资本化率”等，判为相关。
- 如果函件只是泛泛提到“研发投入”“研发费用”“研发项目”但没有追问会计处理，
  判为不相关。
- 如果函件与研发无关（例如关联交易、股价异常波动、资金占用），判为不相关。

候选公告标题：
{title}

从 PDF 中提取的文本片段：
{snippets}

请只返回 JSON，不要添加解释：
{{
  "is_about_rd_capitalization": true 或 false,
  "confidence": 0.0 到 1.0 之间的置信度,
  "evidence_snippet": "支持你判断的最关键原文片段，不超过 80 字",
  "aspect": "资本化条件 / 开发支出 / 无形资产 / 费用化口径 / 其他"
}}
"""


def _build_llm_prompt(title: str, snippets: list[str], tier2_hits: list[str]) -> str:
    snippet_text = "\n".join(f"- {s}" for s in snippets) or "（无文本片段）"
    return LLM_PROMPT_TEMPLATE.format(
        title=title,
        snippets=snippet_text,
        tier2_keywords=", ".join(tier2_hits),
    )


class LLMInquiryClassifier:
    """Thin wrapper around LLMClient for inquiry semantic classification."""

    def __init__(self, client: Any | None = None) -> None:
        self.client = client

    @staticmethod
    def _default_client() -> Any:
        from src.extract.llm_client import LLMClient

        return LLMClient()

    def classify(
        self,
        title: str,
        snippets: list[str],
        tier2_hits: list[str],
    ) -> dict[str, Any]:
        """Return LLM classification result; on failure return conservative 'not related'."""
        if not self.client:
            self.client = self._default_client()

        prompt = _build_llm_prompt(title, snippets, tier2_hits)
        system_prompt = (
            "你必须以有效的 JSON 格式输出，只包含要求的四个字段，不要添加任何其他文本。"
        )
        try:
            result = self.client.call_json(prompt, system_prompt=system_prompt)
        except Exception as exc:
            logger.warning("LLM 问询语义分类失败: %s", exc)
            return {
                "is_about_rd_capitalization": False,
                "confidence": 0.0,
                "evidence_snippet": "LLM classification failed",
                "aspect": "其他",
            }

        # Normalize and validate
        is_related = bool(result.get("is_about_rd_capitalization"))
        confidence = float(result.get("confidence") or 0.0)
        evidence = str(result.get("evidence_snippet") or "")
        aspect = str(result.get("aspect") or "其他")
        return {
            "is_about_rd_capitalization": is_related,
            "confidence": round(max(0.0, min(1.0, confidence)), 4),
            "evidence_snippet": evidence[:120],
            "aspect": aspect,
        }


class InquiryLabeler:
    """Generate one inquiry label record per annual company-year."""

    def __init__(
        self,
        metadata_path: str | Path = "data/metadata/metadata.csv",
        candidates_path: str | Path = "data/inquiry/inquiry_candidates.csv",
        output_path: str | Path = "data/inquiry/inquiry_records.jsonl",
        project_root: str | Path = PROJECT_ROOT,
        pdf_text_extractor: Callable[[Path], str] = extract_pdf_text,
        llm_classifier: LLMInquiryClassifier | None = None,
        use_llm: bool = True,
    ) -> None:
        self.project_root = Path(project_root)
        self.metadata_path = self._resolve(metadata_path)
        self.candidates_path = self._resolve(candidates_path)
        self.output_path = self._resolve(output_path)
        self.pdf_text_extractor = pdf_text_extractor
        self.llm_classifier = llm_classifier
        self.use_llm = use_llm

    @staticmethod
    def _resolve(path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def _candidate_text(self, candidate: dict[str, str]) -> str:
        text = (
            str(candidate.get("announcement_title", ""))
            + "\n"
            + str(candidate.get("pdf_title", ""))
        )
        local_path = candidate.get("local_pdf_path", "")
        if local_path:
            pdf_path = _resolve_local_path(self.project_root, local_path)
            text += "\n" + self.pdf_text_extractor(pdf_path)
        return text

    def _classify_candidate(
        self, candidate: dict[str, str]
    ) -> tuple[list[str], list[str]]:
        text = self._candidate_text(candidate)
        return _classify_keywords(text)

    def _llm_confirm(
        self,
        candidate: dict[str, str],
        tier2_hits: list[str],
    ) -> dict[str, Any]:
        if not self.use_llm or not tier2_hits:
            return {
                "is_about_rd_capitalization": False,
                "confidence": 0.0,
                "evidence_snippet": "",
                "aspect": "其他",
            }
        if self.llm_classifier is None:
            self.llm_classifier = LLMInquiryClassifier()
        text = self._candidate_text(candidate)
        snippets = _keyword_snippets(text, tier2_hits)
        return self.llm_classifier.classify(
            title=str(candidate.get("announcement_title", "")),
            snippets=snippets,
            tier2_hits=tier2_hits,
        )

    def _label_one(
        self,
        annual_record: dict[str, str],
        candidates: list[dict[str, str]],
    ) -> dict[str, Any]:
        inquiry_candidates = [
            c for c in candidates if _is_inquiry_family(c.get("document_role"))
        ]
        reply_candidates = [
            c for c in candidates if _is_reply_family(c.get("document_role"))
        ]

        # Pre-classify all inquiry-family candidates
        candidate_classifications: list[
            tuple[dict[str, str], list[str], list[str]]
        ] = []
        for candidate in inquiry_candidates:
            tier1, tier2 = self._classify_candidate(candidate)
            candidate_classifications.append((candidate, tier1, tier2))

        # Tier-1 auto-flag
        tier1_related: list[dict[str, str]] = []
        tier1_keywords: set[str] = set()
        for candidate, tier1, _tier2 in candidate_classifications:
            if tier1:
                tier1_related.append(candidate)
                tier1_keywords.update(tier1)

        # Tier-2 LLM review (only on inquiry-family candidates)
        llm_related: list[dict[str, str]] = []
        llm_keywords: set[str] = set()
        llm_confidence: float | None = None
        llm_evidence: str = ""
        llm_aspect: str = ""
        llm_failed = False
        for candidate, _tier1, tier2 in candidate_classifications:
            if candidate in tier1_related or not tier2:
                continue
            llm_result = self._llm_confirm(candidate, tier2)
            if llm_result.get("is_about_rd_capitalization"):
                llm_related.append(candidate)
                llm_keywords.update(tier2)
                if llm_confidence is None:
                    llm_confidence = llm_result.get("confidence")
                    llm_evidence = llm_result.get("evidence_snippet", "")
                    llm_aspect = llm_result.get("aspect", "")
            if llm_result.get("confidence", 1.0) == 0.0 and self.use_llm:
                llm_failed = True

        related_candidates = tier1_related + llm_related
        related_keywords = sorted(tier1_keywords | llm_keywords)

        # Primary candidate for display: first related inquiry, else first inquiry
        primary = (
            related_candidates[0]
            if related_candidates
            else (inquiry_candidates[0] if inquiry_candidates else {})
        )

        # Evidence snippets
        text_by_doc_id: dict[str, str] = {
            c.get("doc_id", ""): self._candidate_text(c) for c in inquiry_candidates
        }
        inquiry_questions: list[str] = []
        for candidate in related_candidates:
            inquiry_questions.extend(
                _keyword_snippets(
                    text_by_doc_id.get(candidate.get("doc_id", ""), ""),
                    TIER_1_KEYWORDS + TIER_2_KEYWORDS,
                )
            )
        inquiry_questions = inquiry_questions[:8]

        notes: list[str] = []
        if not candidates:
            notes.append("TODO: no inquiry candidate discovered")
        else:
            if not inquiry_candidates:
                notes.append("MVP: only reply/supporting candidates found")
            if inquiry_candidates and not related_candidates:
                notes.append(
                    "TODO: inquiry candidates found but no R&D capitalization content"
                )
            if tier1_related:
                notes.append(
                    f"Tier-1 keyword hit: {', '.join(sorted(tier1_keywords))}"
                )
            if llm_related:
                notes.append(
                    f"LLM confirmed (confidence={llm_confidence}): {', '.join(sorted(llm_keywords))}"
                )
            if llm_failed:
                notes.append("LLM classification failed for some candidates; treated as not related")

        capitalization_related = bool(related_candidates)

        return {
            "stock_code": annual_record.get("stock_code", ""),
            "year": _report_year(annual_record),
            "annual_doc_id": annual_record.get("doc_id", ""),
            "inquiry_doc_id": primary.get("doc_id") or None,
            "inquiry_title": primary.get("announcement_title") or None,
            "inquiry_date": primary.get("publish_date") or None,
            "inquiry_keywords": related_keywords,
            "inquiry_questions": inquiry_questions,
            "reply_doc_id": self._first_role(reply_candidates, "substantive_reply", "doc_id"),
            "reply_date": self._first_role(reply_candidates, "substantive_reply", "publish_date"),
            "reply_summary": None,
            "reply_satisfactory": None,
            "anomaly_predicted_inquiry": False,
            # 保留旧字段名作为 Y 标签，确保下游 analyze/report 兼容
            "inquiry_actually_received": capitalization_related,
            # 新增更明确的字段
            "inquiry_received": bool(inquiry_candidates),
            "reply_received": bool(reply_candidates),
            "capitalization_related": capitalization_related,
            "capitalization_confidence": (
                1.0 if tier1_related else (llm_confidence or 0.0)
            ),
            "capitalization_evidence": llm_evidence or None,
            "capitalization_aspect": llm_aspect or None,
            "prediction_result": None,
            "candidate_count": len(candidates),
            "inquiry_candidate_count": len(inquiry_candidates),
            "reply_candidate_count": len(reply_candidates),
            "related_candidate_count": len(related_candidates),
            "notes": notes,
        }

    @staticmethod
    def _first_role(
        candidates: list[dict[str, str]],
        role: str,
        field: str,
    ) -> str | None:
        for candidate in candidates:
            if candidate.get("document_role") == role and candidate.get(field):
                return candidate[field]
        return None

    def run(self) -> dict[str, int]:
        annual_records = _read_csv(self.metadata_path)
        candidates = _read_csv(self.candidates_path)
        candidates_by_annual: dict[str, list[dict[str, str]]] = {}
        for candidate in candidates:
            candidates_by_annual.setdefault(
                candidate.get("annual_doc_id", ""), []
            ).append(candidate)

        output_rows: list[dict[str, Any]] = []
        with_candidates = 0
        related = 0
        for annual_record in tqdm(annual_records, desc="问询打标", unit="份", ncols=80):
            annual_doc_id = annual_record.get("doc_id", "")
            candidate_rows = candidates_by_annual.get(annual_doc_id, [])
            if candidate_rows:
                with_candidates += 1
            row = self._label_one(annual_record, candidate_rows)
            if row["capitalization_related"]:
                related += 1
            output_rows.append(row)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", encoding="utf-8") as f:
            for row in output_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        return {
            "total": len(output_rows),
            "with_candidates": with_candidates,
            "related": related,
        }


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #


def main() -> int:
    """独立运行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    labeler = InquiryLabeler()
    stats = labeler.run()
    print(f"\n✅ 问询标签完成: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
