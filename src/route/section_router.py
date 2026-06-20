"""章节定位器

从 MinerU 解析后的 Markdown 中定位研发相关章节，输出章节切片。

Usage:
    from src.route.section_router import SectionRouter
    router = SectionRouter()
    stats = router.run()

讲义依据: Week 13 — 章节定位
"""

from __future__ import annotations

import csv
import logging
import re
from pathlib import Path
from typing import Any

import yaml
from tqdm import tqdm

from src.model.schemas import SectionSlice

logger = logging.getLogger(__name__)

# 章节切片上下文行数
CONTEXT_LINES_BEFORE = 2
CONTEXT_LINES_AFTER = 50
DEFAULT_MAX_SLICES_PER_RULE = 2
BASE_MATCH_SCORE = 10.0

# section_check_report 质量阈值（与 _score_candidate 的打分量纲匹配）
LOW_MATCH_SCORE = 30.0
MIN_SLICE_CHARS = 200
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


class SectionRouter:
    """章节定位器

    读取 MinerU 解析后的 Markdown，根据关键词规则定位研发相关章节，
    输出 SectionSlice 结构的 JSONL 文件。

    Resume 策略: data/sections/{doc_id}_sections.jsonl 文件存在则跳过。
    """

    def __init__(
        self,
        parsed_dir: str = "data/parsed",
        output_dir: str = "data/sections",
        rules_path: str = "configs/section_rules.yaml",
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.parsed_dir = self.project_root / parsed_dir
        self.output_dir = self.project_root / output_dir
        self.rules_path = self.project_root / rules_path

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rules = self._load_rules()

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _load_rules(self) -> list[dict]:
        """加载章节定位规则"""
        with open(self.rules_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        rules = config.get("rules", [])
        # 按 priority 排序，数字小的优先
        return sorted(rules, key=lambda r: r.get("priority", 99))

    def _extract_slice(
        self,
        lines: list[str],
        match_line: int,
        doc_id: str,
        rule_name: str,
        keyword: str,
        *,
        context_before: int = CONTEXT_LINES_BEFORE,
        context_after: int = CONTEXT_LINES_AFTER,
        match_score: float | None = None,
        match_reason: str = "",
    ) -> SectionSlice:
        """从匹配行提取上下文切片"""
        start = max(0, match_line - context_before)
        end = min(len(lines), match_line + context_after)
        text = "".join(lines[start:end])

        return SectionSlice(
            doc_id=doc_id,
            section_name=rule_name,
            matched_keyword=keyword,
            text=text.strip(),
            line_start=start,
            line_end=end,
            match_score=match_score,
            match_reason=match_reason,
        )

    def _score_candidate(
        self,
        text: str,
        line: str,
        rule: dict[str, Any],
        keyword: str,
    ) -> tuple[float, str]:
        """Score a candidate slice by high-signal and noise keywords."""
        positive_keywords = rule.get("positive_keywords", [])
        negative_keywords = rule.get("negative_keywords", [])
        score = BASE_MATCH_SCORE + max(0, 20 - len(keyword))
        reasons = [f"keyword:{keyword}"]

        positives = [kw for kw in positive_keywords if kw in text]
        if positives:
            score += 15 * len(positives)
            reasons.append("positive:" + ",".join(positives[:5]))

        negatives = [kw for kw in negative_keywords if kw in text]
        if negatives:
            score -= 20 * len(negatives)
            reasons.append("negative:" + ",".join(negatives[:5]))

        if "<table" in text:
            score += 12
            reasons.append("table")
        if line.lstrip().startswith("#"):
            score += 8
            reasons.append("heading")
        if "附注" in text:
            score += 8
            reasons.append("note")
        if "资产负债表" in text and rule.get("name") == "开发支出":
            score -= 15
            reasons.append("balance_sheet_penalty")

        return score, ";".join(reasons)

    def _candidate_overlaps_existing(
        self,
        candidate: SectionSlice,
        selected: list[SectionSlice],
    ) -> bool:
        """Avoid returning multiple slices from the same local paragraph/table."""
        for existing in selected:
            overlap_start = max(candidate.line_start, existing.line_start)
            overlap_end = min(candidate.line_end, existing.line_end)
            if overlap_start < overlap_end:
                overlap = overlap_end - overlap_start
                shorter = min(
                    candidate.line_end - candidate.line_start,
                    existing.line_end - existing.line_start,
                )
                if shorter > 0 and overlap / shorter > 0.6:
                    return True
        return False

    def _find_sections(self, md_path: Path, doc_id: str) -> list[SectionSlice]:
        """在 Markdown 中查找所有匹配的章节"""
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        slices: list[SectionSlice] = []

        for rule in self.rules:
            rule_name = rule["name"]
            keywords = rule["keywords"]
            context_before = int(rule.get("context_before", CONTEXT_LINES_BEFORE))
            context_after = int(rule.get("context_after", CONTEXT_LINES_AFTER))
            max_slices = int(
                rule.get("max_slices", DEFAULT_MAX_SLICES_PER_RULE)
            )
            candidates: list[SectionSlice] = []
            for keyword in keywords:
                for i, line in enumerate(lines):
                    if keyword in line:
                        start = max(0, i - context_before)
                        end = min(len(lines), i + context_after)
                        text = "".join(lines[start:end])
                        score, reason = self._score_candidate(
                            text=text,
                            line=line,
                            rule=rule,
                            keyword=keyword,
                        )
                        slice_obj = self._extract_slice(
                            lines,
                            i,
                            doc_id,
                            rule_name,
                            keyword,
                            context_before=context_before,
                            context_after=context_after,
                            match_score=score,
                            match_reason=reason,
                        )
                        candidates.append(slice_obj)

            candidates.sort(
                key=lambda s: (
                    s.match_score or 0,
                    -(s.line_end - s.line_start),
                    -s.line_start,
                ),
                reverse=True,
            )
            selected: list[SectionSlice] = []
            for candidate in candidates:
                if self._candidate_overlaps_existing(candidate, selected):
                    continue
                selected.append(candidate)
                if len(selected) >= max_slices:
                    break
            slices.extend(sorted(selected, key=lambda s: s.line_start))

        return slices

    # ------------------------------------------------------------------ #
    # section_check_report（Week 13 讲义要求：定位后要检查是否找对）
    # ------------------------------------------------------------------ #

    @staticmethod
    def _extract_section_title(text: str) -> str:
        """从切片文本提取首个 Markdown 标题作为章节标题。"""
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            m = HEADING_RE.match(line)
            if m:
                return m.group(1).strip()
        return ""

    @staticmethod
    def _derive_quality_issue(slice_obj: SectionSlice) -> str:
        """根据现成 match_score / match_reason / 文本长度推导质量标记。

        讲义字段 quality_issue：空表示无问题；否则给出具体问题。
        page_start/page_end 在 parsed Markdown 中无页码来源，统一标 page_unavailable。
        """
        issues: list[str] = []
        score = slice_obj.match_score or 0.0
        reason = slice_obj.match_reason or ""
        text_len = len(slice_obj.text or "")

        if score < LOW_MATCH_SCORE:
            issues.append(f"low_score({score:.0f})")
        if "negative:" in reason:
            issues.append("negative_keyword_hit")
        if text_len < MIN_SLICE_CHARS:
            issues.append(f"too_short({text_len}chars)")
        if "positive:" not in reason:
            issues.append("no_positive_keyword")
        issues.append("page_unavailable")
        return ";".join(issues)

    def _iter_section_files(self) -> list[Path]:
        """已产出的章节切片文件（含空文件标记）。"""
        return sorted(self.output_dir.glob("*_sections.jsonl"))

    def _write_section_check_report(
        self,
        report_csv: Path,
        report_md: Path,
    ) -> dict[str, int]:
        """汇总每文档每规则是否定位成功，写出 csv + md。

        字段对齐 Week 13 讲义：
        doc_id, title, target_section, found, section_title,
        page_start, page_end, quality_issue, notes
        """
        rows: list[dict[str, Any]] = []
        # title 从 metadata.csv 回填（若有），否则留空
        title_map = self._load_metadata_titles()

        for section_file in self._iter_section_files():
            doc_id = section_file.name[: -len("_sections.jsonl")]
            title = title_map.get(doc_id, "")
            slices = self._read_slices(section_file)
            if not slices:
                rows.append({
                    "doc_id": doc_id,
                    "title": title,
                    "target_section": "",
                    "found": "no",
                    "section_title": "",
                    "page_start": "",
                    "page_end": "",
                    "quality_issue": "no_slice_found",
                    "notes": "route 未匹配到任何章节",
                })
                continue
            # 每个规则取其首个切片为代表行
            seen_rules: set[str] = set()
            for s in slices:
                if s.section_name in seen_rules:
                    continue
                seen_rules.add(s.section_name)
                rows.append({
                    "doc_id": doc_id,
                    "title": title,
                    "target_section": s.section_name,
                    "found": "yes",
                    "section_title": self._extract_section_title(s.text),
                    "page_start": "",
                    "page_end": "",
                    "quality_issue": self._derive_quality_issue(s),
                    "notes": s.match_reason,
                })

        report_csv.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "doc_id", "title", "target_section", "found",
            "section_title", "page_start", "page_end",
            "quality_issue", "notes",
        ]
        with open(report_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        self._write_section_check_md(report_md, rows)
        return {
            "rows": len(rows),
            "found": sum(1 for r in rows if r["found"] == "yes"),
            "not_found": sum(1 for r in rows if r["found"] == "no"),
        }

    def _write_section_check_md(
        self, report_md: Path, rows: list[dict[str, Any]]
    ) -> None:
        total = len(rows)
        found = sum(1 for r in rows if r["found"] == "yes")
        not_found = total - found
        # 质量问题分布
        issue_counter: dict[str, int] = {}
        for r in rows:
            if r["quality_issue"]:
                for tag in r["quality_issue"].split(";"):
                    issue_counter[tag] = issue_counter.get(tag, 0) + 1

        lines = [
            "# Section Check Report",
            "",
            "route 阶段章节定位质量检查（Week 13 讲义要求：定位后要检查是否找对）。",
            "",
            f"- 检查行数: {total}",
            f"- 定位成功行: {found}",
            f"- 未定位行: {not_found}",
            "",
            "## 质量问题分布",
            "",
            "| 问题标记 | 出现次数 |",
            "| -------- | --------: |",
        ]
        if issue_counter:
            for tag, cnt in sorted(issue_counter.items(), key=lambda x: -x[1]):
                lines.append(f"| {tag} | {cnt} |")
        else:
            lines.append("| (无) | 0 |")
        lines.extend([
            "",
            "## 字段说明",
            "",
            "- `found`: 该 doc 是否定位到任一目标章节",
            "- `section_title`: 切片文本首个 Markdown 标题（规则名见 `target_section`）",
            "- `page_start/page_end`: parsed Markdown 无页码来源，留空，"
            "`quality_issue` 标 `page_unavailable`",
            "- `quality_issue`: 由 match_score / match_reason / 文本长度推导",
            "",
        ])
        report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def _read_slices(section_file: Path) -> list[SectionSlice]:
        slices: list[SectionSlice] = []
        with open(section_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    slices.append(SectionSlice.model_validate_json(line))
                except Exception:
                    continue
        return slices

    def _load_metadata_titles(self) -> dict[str, str]:
        """从 metadata.csv 读 doc_id -> stock_name，用于回填 title。"""
        meta_path = self.project_root / "data" / "metadata" / "metadata.csv"
        title_map: dict[str, str] = {}
        if not meta_path.exists():
            return title_map
        try:
            with open(meta_path, "r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    doc_id = row.get("doc_id", "")
                    name = row.get("stock_name", "") or row.get("announcement_title", "")
                    if doc_id:
                        title_map[doc_id] = name
        except Exception:
            pass
        return title_map

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def route(self, md_path: Path, doc_id: str, force: bool = False) -> Path | None:
        """定位单个 Markdown 文件的章节

        Returns:
            输出文件路径，或 None（处理失败）
        """
        output_path = self.output_dir / f"{doc_id}_sections.jsonl"

        # Resume: 已存在的跳过
        if output_path.exists() and not force:
            logger.info("[%s] 章节切片已存在，跳过", doc_id)
            return output_path

        try:
            slices = self._find_sections(md_path, doc_id)
        except Exception as e:
            logger.error("[%s] 章节定位异常: %s", doc_id, e)
            return None

        if not slices:
            logger.warning("[%s] 未找到任何匹配章节", doc_id)
            # 写入空文件标记为已处理，避免反复扫描
            output_path.write_text("", encoding="utf-8")
            return output_path

        with open(output_path, "w", encoding="utf-8") as f:
            for s in slices:
                f.write(s.model_dump_json() + "\n")

        section_names = [s.section_name for s in slices]
        logger.info(
            "[%s] 章节定位完成: %d 个切片 (%s)",
            doc_id, len(slices), ", ".join(section_names),
        )
        return output_path

    def run(
        self,
        limit: int | None = None,
        force: bool = False,
    ) -> dict[str, int]:
        """运行章节定位

        Args:
            limit: 限制处理的 Markdown 数量（用于测试）

        Returns:
            统计信息: {"total": 总数, "success": 有切片数, "empty": 空切片数}
        """
        md_files = sorted(self.parsed_dir.glob("*.md"))
        if not md_files:
            logger.warning("未找到 Markdown 文件: %s", self.parsed_dir)
            return {"total": 0, "success": 0, "empty": 0}

        if limit:
            md_files = md_files[:limit]

        total = len(md_files)
        success = 0
        empty = 0

        logger.info("开始章节定位 %d 份 Markdown...", total)

        for md_path in tqdm(md_files, desc="章节定位", unit="份", ncols=80):
            doc_id = md_path.stem
            result = self.route(md_path, doc_id, force=force)
            if result:
                if result.stat().st_size > 0:
                    success += 1
                else:
                    empty += 1

        logger.info(
            "章节定位完成: total=%d, success=%d, empty=%d",
            total, success, empty,
        )

        # Week 13 讲义要求：定位后产出 section_check_report
        check_stats = self._write_section_check_report(
            report_csv=self.project_root / "outputs" / "reports" / "section_check_report.csv",
            report_md=self.project_root / "outputs" / "reports" / "section_check_report.md",
        )
        logger.info("section_check_report: %s", check_stats)
        return {"total": total, "success": success, "empty": empty}


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    router = SectionRouter()
    stats = router.run()
    print(f"\n✅ 章节定位完成: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
