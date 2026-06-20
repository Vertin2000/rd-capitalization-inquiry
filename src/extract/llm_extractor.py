"""LLM 字段抽取器

从章节切片中抽取研发资本化相关字段，输出 FieldEvidence 嵌套结构。

Usage:
    from src.extract.llm_extractor import LLMExtractor
    extractor = LLMExtractor()
    stats = extractor.run()

讲义依据: Week 13 — LLM 字段抽取
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
import re
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from src.extract.llm_client import LLMClient
from src.model.schemas import FieldEvidence, SectionSlice

logger = logging.getLogger(__name__)

MAX_SECTION_CHARS = 4000
MAX_COMBINED_SECTION_CHARS = 16000

DEFAULT_PROMPT_TEMPLATE = """你是一位资深财务分析师，擅长从上市公司年报中提取研发支出相关数据。

请从以下年报文本中提取以下字段，以 JSON 格式返回。

需要提取的字段（每个字段必须包含 value、evidence_text、page_no、confidence）：
- rd_expense_total: 研发支出总额（万元）
- rd_capitalized_amount: 资本化金额（万元）
- rd_expensed_amount: 费用化金额（万元）
- dev_cost_opening: 开发支出期初余额（万元）
- dev_cost_closing: 开发支出期末余额（万元）
- impairment: 减值准备（万元）
- capitalization_rate: 资本化率（%）
- capitalization_condition: 资本化条件描述（原文）

输出格式要求：
{{
  "company_name": "公司名称",
  "company_code": "股票代码（6位数字）",
  "year": 2023,
  "rd_expense_total": {{"value": 49896.36, "evidence_text": "研发投入合计 49,896.36 万元", "page_no": 156, "confidence": 0.95}},
  "rd_capitalized_amount": {{"value": 0, "evidence_text": "资本化金额 0 万元", "page_no": 156, "confidence": 0.90}},
  ...
}}

规则：
1. 金额单位为万元，如果原文为元请转换
2. capitalization_rate 优先使用年报直接披露值；若没有披露，可返回 null，由校验阶段计算
3. 禁止把开发支出期末余额直接当作本期资本化金额
4. 原文明确为 0 时才能填 0；无法判断或未披露时 value 返回 null，evidence_text 说明原因
5. confidence 为 0-1 的浮点数，表示你对该字段提取结果的确信程度
6. page_no 为整数，如无法确定则填 null
7. 确保资本化金额 + 费用化金额 ≈ 总额

文本内容：
{section_text}

请直接返回 JSON，不要添加任何解释。
"""


class LLMExtractor:
    """LLM 字段抽取器

    读取章节切片，调用 LLM API 抽取结构化字段，
    输出 FieldEvidence 嵌套结构的 JSONL 文件。

    Resume 策略: 读取 records.jsonl，已抽取的 doc_id 跳过。
    """

    def __init__(
        self,
        sections_dir: str = "data/sections",
        output_path: str = "data/extracted/records.jsonl",
        metadata_path: str = "data/metadata/metadata.csv",
        prompt_template: str | None = None,
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.sections_dir = self.project_root / sections_dir
        self.output_path = self.project_root / output_path
        self.metadata_path = self.project_root / metadata_path
        self.prompt_template = prompt_template or DEFAULT_PROMPT_TEMPLATE

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.client = LLMClient()
        self.metadata_by_doc_id = self._load_metadata()

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _load_extracted_set(self) -> set[str]:
        """加载已抽取的 doc_id 集合"""
        if not self.output_path.exists():
            return set()
        extracted: set[str] = set()
        with open(self.output_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    extracted.add(record.get("doc_id", ""))
                except json.JSONDecodeError:
                    continue
        return extracted

    def _load_metadata(self) -> dict[str, dict[str, Any]]:
        """Load annual-report metadata keyed by doc_id."""
        if not self.metadata_path.exists():
            return {}
        df = pd.read_csv(
            self.metadata_path,
            encoding="utf-8",
            dtype=str,
        ).fillna("")
        if "doc_id" not in df.columns:
            return {}
        return {
            str(row["doc_id"]): row.to_dict()
            for _, row in df.iterrows()
            if str(row.get("doc_id", ""))
        }

    def _load_sections(self, doc_id: str) -> list[SectionSlice]:
        """加载某个 doc 的所有 section slices"""
        path = self.sections_dir / f"{doc_id}_sections.jsonl"
        if not path.exists():
            return []
        slices: list[SectionSlice] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    slices.append(SectionSlice.model_validate_json(line))
                except Exception:
                    continue
        return slices

    def _build_prompt(self, sections: list[SectionSlice]) -> str:
        """构建 Prompt"""
        selected_texts: list[str] = []
        total_chars = 0
        for section in sorted(
            sections,
            key=lambda s: (s.match_score or 0),
            reverse=True,
        ):
            text = section.text.strip()
            if len(text) > MAX_SECTION_CHARS:
                text = text[:MAX_SECTION_CHARS] + "\n[section truncated]"
            if total_chars + len(text) > MAX_COMBINED_SECTION_CHARS:
                remaining = MAX_COMBINED_SECTION_CHARS - total_chars
                if remaining <= 0:
                    break
                text = text[:remaining] + "\n[prompt truncated]"
            selected_texts.append(text)
            total_chars += len(text)
        combined_text = "\n\n---\n\n".join(selected_texts)
        return self.prompt_template.format(section_text=combined_text)

    @staticmethod
    def _year_from_doc_id(doc_id: str) -> int:
        """Extract report year from human-readable doc_id."""
        match = re.search(r"(20\d{2})年报", doc_id)
        if match:
            return int(match.group(1))
        return 0

    def _metadata_for_doc(self, doc_id: str) -> dict[str, Any]:
        """Return authoritative metadata for a document when available."""
        return self.metadata_by_doc_id.get(doc_id, {})

    def _wrap_field_evidence(
        self, raw: dict[str, Any], doc_id: str
    ) -> dict[str, Any]:
        """将 LLM 原始输出包装为 FieldEvidence 嵌套结构"""
        metadata = self._metadata_for_doc(doc_id)
        year = self._year_from_doc_id(doc_id)
        if not year:
            try:
                year = int(raw.get("year", 0) or 0)
            except (TypeError, ValueError):
                year = 0

        record: dict[str, Any] = {
            "doc_id": doc_id,
            "company_name": metadata.get("stock_name") or raw.get("company_name", ""),
            "company_code": metadata.get("stock_code") or raw.get("company_code", ""),
            "year": year,
            "source_pdf_path": metadata.get("local_pdf_path", ""),
            "evidence_text": "",
            "page_no": 0,
        }

        # 核心财务字段 — 统一包装为 FieldEvidence
        field_names = [
            "rd_expense_total",
            "rd_capitalized_amount",
            "rd_expensed_amount",
            "dev_cost_opening",
            "dev_cost_closing",
            "impairment",
            "capitalization_rate",
        ]

        for field_name in field_names:
            field_data = raw.get(field_name)
            if isinstance(field_data, dict):
                # LLM 已输出 FieldEvidence 结构
                record[field_name] = FieldEvidence(**field_data).model_dump()
            elif field_data is not None:
                # 兼容扁平数值输出
                record[field_name] = FieldEvidence(
                    value=field_data,
                    evidence_text=raw.get("evidence_text", ""),
                    page_no=raw.get("page_no"),
                ).model_dump()
            else:
                record[field_name] = FieldEvidence(
                    value=None,
                    evidence_text=raw.get("null_reason", "未找到该字段"),
                ).model_dump()

        # 文本字段：capitalization_condition
        cap_condition = raw.get("capitalization_condition")
        if isinstance(cap_condition, dict):
            record["capitalization_condition"] = cap_condition.get("value")
        else:
            record["capitalization_condition"] = cap_condition

        # 从第一个有 evidence_text 的字段中提取记录级 evidence
        for field_name in field_names:
            fe_data = record.get(field_name)
            if isinstance(fe_data, dict) and fe_data.get("evidence_text"):
                record["evidence_text"] = fe_data["evidence_text"]
                if fe_data.get("page_no") is not None:
                    record["page_no"] = fe_data["page_no"]
                break

        return record

    def _save_record(self, record: dict[str, Any]) -> None:
        """保存抽取记录到 JSONL"""
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def extract(
        self,
        doc_id: str,
        extracted: set[str] | None = None,
        raise_on_error: bool = False,
    ) -> dict[str, Any] | None:
        """抽取单个 doc 的字段

        Returns:
            抽取结果字典，或 None（失败/跳过）
        """
        # Resume 检查
        if extracted is None:
            extracted = self._load_extracted_set()
        if doc_id in extracted:
            logger.info("[%s] 已抽取，跳过", doc_id)
            return None

        sections = self._load_sections(doc_id)
        if not sections:
            logger.warning("[%s] 无章节切片，跳过", doc_id)
            return None

        prompt = self._build_prompt(sections)

        try:
            result = self.client.call_json(prompt)
            record = self._wrap_field_evidence(result, doc_id)
            logger.info("[%s] 抽取成功", doc_id)
            return record
        except Exception as e:
            logger.error("[%s] 抽取失败: %s", doc_id, e)
            if raise_on_error:
                raise
            return None

    def _log_progress(
        self,
        done: int,
        total: int,
        success: int,
        failed: int,
    ) -> None:
        """Log visible progress for long-running extraction batches."""
        logger.info(
            "进度: done=%d/%d success=%d failed=%d pending=%d",
            done,
            total,
            success,
            failed,
            max(total - done, 0),
        )

    def _terminate_active_llm_calls(self) -> None:
        """Ask the client to stop active backend processes if it supports it."""
        terminate = getattr(self.client, "terminate_active_processes", None)
        if callable(terminate):
            terminate()

    def _finalize_stats(
        self,
        doc_ids: list[str],
        *,
        fail_fast_triggered: bool = False,
    ) -> dict[str, int]:
        """Compute final stats from the JSONL output file."""
        final_extracted = self._load_extracted_set()
        success = sum(1 for doc_id in doc_ids if doc_id in final_extracted)
        failed = len(doc_ids) - success
        if fail_fast_triggered:
            logger.error(
                "抽取提前停止: total=%d, success=%d, failed=%d",
                len(doc_ids),
                success,
                failed,
            )
        else:
            logger.info(
                "抽取完成: total=%d, success=%d, failed=%d",
                len(doc_ids),
                success,
                failed,
            )
        return {"total": len(doc_ids), "success": success, "failed": failed}

    def run(
        self,
        limit: int | None = None,
        workers: int = 1,
        fail_fast: bool = False,
        skip_empty_sections: bool = False,
    ) -> dict[str, int]:
        """运行抽取

        Args:
            limit: 限制处理的文档数量（用于测试）
            workers: 并发抽取 worker 数。1 为串行，>1 使用线程池。
            fail_fast: 任一文档失败时立即终止活跃 LLM 调用并返回。
            skip_empty_sections: 跳过空 section 文档，留待后续补抓补 route。

        Returns:
            统计信息: {"total": 总数, "success": 成功数, "failed": 失败数}
        """
        section_files = sorted(self.sections_dir.glob("*_sections.jsonl"))
        if not section_files:
            logger.warning("未找到章节切片文件: %s", self.sections_dir)
            return {"total": 0, "success": 0, "failed": 0}

        # 提取 doc_id 列表
        doc_ids = [f.stem.replace("_sections", "") for f in section_files]

        if limit:
            doc_ids = doc_ids[:limit]

        total = len(doc_ids)
        extracted = self._load_extracted_set()
        success = sum(1 for doc_id in doc_ids if doc_id in extracted)
        failed = 0
        pending_doc_ids = [doc_id for doc_id in doc_ids if doc_id not in extracted]

        workers = max(1, workers)
        if self.client.backend in {"kimi_code_cli", "kimi_cli", "kimi-code-cli", "kimi"}:
            import os

            max_kimi_workers = max(
                1, int(os.environ.get("KIMI_MAX_WORKERS", "4"))
            )
            if workers > max_kimi_workers:
                logger.warning(
                    "Kimi Code CLI 会为每次 -p 调用创建 agent session；"
                    "workers=%d 已降为 %d，避免本机内存/会话目录被打满",
                    workers,
                    max_kimi_workers,
                )
                workers = max_kimi_workers
        if fail_fast:
            empty_doc_ids = []
            for doc_id in pending_doc_ids:
                if not self._load_sections(doc_id):
                    empty_doc_ids.append(doc_id)
            if empty_doc_ids and skip_empty_sections:
                for doc_id in empty_doc_ids:
                    logger.warning("[%s] 空章节切片，已跳过并留待补抓", doc_id)
                pending_doc_ids = [
                    doc_id
                    for doc_id in pending_doc_ids
                    if doc_id not in set(empty_doc_ids)
                ]
                failed += len(empty_doc_ids)
            elif empty_doc_ids:
                doc_id = empty_doc_ids[0]
                logger.error("[%s] fail-fast 触发: 无章节切片", doc_id)
                self._terminate_active_llm_calls()
                return self._finalize_stats(
                    doc_ids,
                    fail_fast_triggered=True,
                )

        logger.info(
            "开始抽取 %d 份文档: pending=%d, skipped=%d, workers=%d, fail_fast=%s",
            total,
            len(pending_doc_ids),
            success,
            workers,
            fail_fast,
        )

        if workers == 1 or len(pending_doc_ids) <= 1:
            pbar = tqdm(pending_doc_ids, desc="LLM 抽取", unit="份", ncols=80)
            for doc_id in pbar:
                try:
                    record = self.extract(
                        doc_id,
                        extracted=extracted,
                        raise_on_error=fail_fast,
                    )
                except Exception as e:
                    logger.error("[%s] fail-fast 触发: %s", doc_id, e)
                    self._terminate_active_llm_calls()
                    pbar.close()
                    return self._finalize_stats(
                        doc_ids,
                        fail_fast_triggered=True,
                    )
                if record:
                    self._save_record(record)
                    extracted.add(doc_id)
                    success += 1
                else:
                    failed += 1
                    if fail_fast:
                        logger.error("[%s] fail-fast 触发: 未生成抽取记录", doc_id)
                        self._terminate_active_llm_calls()
                        pbar.close()
                        return self._finalize_stats(
                            doc_ids,
                            fail_fast_triggered=True,
                        )
                self._log_progress(success + failed, total, success, failed)
                pbar.set_postfix(ok=success, fail=failed)
            pbar.close()
        else:
            executor = ThreadPoolExecutor(
                max_workers=min(workers, len(pending_doc_ids))
            )
            shutdown_without_wait = False
            try:
                future_to_doc_id = {}
                for doc_id in pending_doc_ids:
                    if fail_fast:
                        future = executor.submit(
                            self.extract,
                            doc_id,
                            extracted=extracted,
                            raise_on_error=True,
                        )
                    else:
                        future = executor.submit(
                            self.extract,
                            doc_id,
                            extracted=extracted,
                        )
                    future_to_doc_id[future] = doc_id

                pbar = tqdm(total=len(future_to_doc_id), desc="LLM 抽取", unit="份", ncols=80)
                for future in as_completed(future_to_doc_id):
                    doc_id = future_to_doc_id[future]
                    try:
                        record = future.result()
                    except Exception as e:
                        logger.error("[%s] 抽取任务异常: %s", doc_id, e)
                        if fail_fast:
                            logger.error("[%s] fail-fast 触发，取消剩余任务", doc_id)
                            for pending_future in future_to_doc_id:
                                pending_future.cancel()
                            self._terminate_active_llm_calls()
                            shutdown_without_wait = True
                            pbar.close()
                            executor.shutdown(wait=False, cancel_futures=True)
                            return self._finalize_stats(
                                doc_ids,
                                fail_fast_triggered=True,
                            )
                        record = None
                    if record:
                        self._save_record(record)
                        extracted.add(doc_id)
                        success += 1
                    else:
                        failed += 1
                        if fail_fast:
                            logger.error("[%s] fail-fast 触发: 未生成抽取记录", doc_id)
                            for pending_future in future_to_doc_id:
                                pending_future.cancel()
                            self._terminate_active_llm_calls()
                            shutdown_without_wait = True
                            pbar.close()
                            executor.shutdown(wait=False, cancel_futures=True)
                            return self._finalize_stats(
                                doc_ids,
                                fail_fast_triggered=True,
                            )
                    self._log_progress(success + failed, total, success, failed)
                    pbar.update(1)
                    pbar.set_postfix(ok=success, fail=failed)
                pbar.close()
            finally:
                if not shutdown_without_wait:
                    executor.shutdown(wait=True, cancel_futures=True)

        # 并发运行期间其它进程可能写入 records.jsonl；最终用文件状态校正一次。
        return self._finalize_stats(doc_ids)


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    extractor = LLMExtractor()
    stats = extractor.run()
    print(f"\n{'✅' if stats['failed'] == 0 else '⚠️'} 抽取完成: {stats}")
    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
