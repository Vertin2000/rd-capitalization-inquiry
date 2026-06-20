"""数据校验器

对 LLM 抽取结果进行 Pydantic Schema 校验和会计恒等式交叉验证。

Usage:
    from src.validate.validator import DataValidator
    validator = DataValidator()
    stats = validator.run()

讲义依据: Week 13 — Schema 校验
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from src.model.schemas import RDCapitalizationRecord

logger = logging.getLogger(__name__)

# 恒等式差异阈值（5%）
IDENTITY_TOLERANCE = 0.05

# 表格提取值对 LLM 缺失字段的 fallback 映射
# key = rd_table_extractor 输出的 row_label, value = RDCapitalizationRecord 字段名
TABLE_FALLBACK_MAP: dict[str, str] = {
    "expensed_amount": "rd_expensed_amount",
    "capitalized_amount": "rd_capitalized_amount",
    "total_amount": "rd_expense_total",
    "capitalization_rate": "capitalization_rate",
    "opening_balance": "dev_cost_opening",
    "closing_balance": "dev_cost_closing",
}


class DataValidator:
    """数据校验器

    输入: data/extracted/records.jsonl (FieldEvidence 嵌套结构)
    输出:
      - data/validated/records.jsonl (通过校验的记录)
      - data/validated/validation_errors.jsonl (失败记录及原因)
    """

    def __init__(
        self,
        input_path: str = "data/extracted/records.jsonl",
        output_path: str = "data/validated/records.jsonl",
        error_path: str = "data/validated/validation_errors.jsonl",
        table_fallback_path: str | None = None,
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.input_path = self.project_root / input_path
        self.output_path = self.project_root / output_path
        self.error_path = self.project_root / error_path

        # table_fallback_path=None means "follow model_config.yaml".
        # Explicitly pass a path to force enable/disable.
        if table_fallback_path is None:
            self.table_fallback_path = self._default_table_fallback_path()
        elif table_fallback_path == "":
            self.table_fallback_path = None
        else:
            self.table_fallback_path = self.project_root / table_fallback_path

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._table_fallback = self._load_table_fallback()
        self._table_fallback_notes: dict[str, list[str]] = {}

    def _default_table_fallback_path(self) -> Path | None:
        """Enable table fallback only when model_config.yaml explicitly sets it."""
        config_path = self.project_root / "configs" / "model_config.yaml"
        if not config_path.exists():
            return None
        with config_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        if config.get("table_extraction", {}).get("fallback_to_tables"):
            return self.project_root / "data" / "extracted" / "tables" / "tables.jsonl"
        return None

    def _load_table_fallback(self) -> dict[str, dict[str, float]]:
        """Load deterministic table values to backfill missing LLM-extracted fields.

        When multiple rows map to the same schema field, prefer the row whose
        ``year`` matches the annual report year extracted from ``doc_id``.
        """
        if not self.table_fallback_path or not self.table_fallback_path.exists():
            return {}

        import re

        candidates: dict[str, dict[str, list[tuple[int | None, float]]]] = {}
        with self.table_fallback_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                doc_id = row.get("doc_id")
                row_label = row.get("row_label")
                value = row.get("value")
                schema_field = TABLE_FALLBACK_MAP.get(row_label)
                if not doc_id or not schema_field or value is None:
                    continue
                candidates.setdefault(doc_id, {}).setdefault(schema_field, []).append(
                    (row.get("year"), value)
                )

        fallback: dict[str, dict[str, float]] = {}
        for doc_id, fields in candidates.items():
            doc_year_match = re.search(r"(20\d{2})年报", doc_id)
            doc_year = int(doc_year_match.group(1)) if doc_year_match else None
            fallback[doc_id] = {}
            for field, values in fields.items():
                # Prefer year-matching value
                chosen = next(
                    (v for y, v in values if y == doc_year),
                    None,
                )
                if chosen is None:
                    chosen = next((v for y, v in values if v is not None), None)
                if chosen is not None:
                    fallback[doc_id][field] = chosen
        return fallback

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _flatten_record(self, record: dict[str, Any]) -> dict[str, Any]:
        """将 FieldEvidence 嵌套结构展平为 RDCapitalizationRecord 格式

        如果字段值是 dict（FieldEvidence），提取 value；否则保持原值。
        同时从第一个有 evidence_text 的字段中提取记录级回退值。
        """
        flat: dict[str, Any] = {}
        record_evidence = ""
        record_page_no = 0

        for key, value in record.items():
            if isinstance(value, dict) and "value" in value:
                # FieldEvidence 嵌套结构
                flat[key] = value["value"]
                # 收集记录级证据（从第一个非空 evidence 中提取）
                if not record_evidence and value.get("evidence_text"):
                    record_evidence = value["evidence_text"]
                if record_page_no == 0 and value.get("page_no"):
                    record_page_no = value["page_no"]
            else:
                flat[key] = value

        # 设置记录级回退字段
        flat.setdefault("evidence_text", record_evidence)
        flat.setdefault("page_no", record_page_no)

        return flat

    def _identity_check(
        self, record: RDCapitalizationRecord
    ) -> tuple[bool, str]:
        """会计恒等式交叉验证

        校验: capitalized + expensed ≈ total
        差异 > 5% 标记为警告。
        """
        cap = record.rd_capitalized_amount
        exp = record.rd_expensed_amount
        total = record.rd_expense_total

        if cap is None or exp is None:
            return True, "资本化/费用化金额缺失，跳过恒等式校验"

        calculated_total = cap + exp

        if total is not None and total > 0:
            diff_ratio = abs(calculated_total - total) / total
            if diff_ratio > IDENTITY_TOLERANCE:
                return (
                    False,
                    f"恒等式偏差: {diff_ratio * 100:.1f}% "
                    f"(资本化+费用化={calculated_total:.2f}, "
                    f"总额={total:.2f})",
                )

        return True, "恒等式校验通过"

    def _rate_consistency_check(
        self, record: RDCapitalizationRecord
    ) -> tuple[bool, str]:
        """资本化率一致性校验

        校验: record.capitalization_rate 与 calculated_capitalization_rate
        差异 > 5% 标记为警告。
        """
        if record.capitalization_rate is None:
            return True, "资本化率未提供，跳过一致性校验"

        calculated = record.calculated_capitalization_rate
        if calculated is None:
            return True, "无法计算资本化率，跳过一致性校验"

        diff = abs(record.capitalization_rate - calculated)
        if diff > 5.0:
            return (
                False,
                f"资本化率不一致: 记录值={record.capitalization_rate:.2f}%, "
                f"计算值={calculated:.2f}%, 差异={diff:.2f}%",
            )

        return True, "资本化率一致性校验通过"

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def validate_record(
        self, record: dict[str, Any]
    ) -> tuple[RDCapitalizationRecord | None, str]:
        """校验单条记录

        Returns:
            (校验通过的记录, 错误信息) — 通过时错误信息为空
        """
        # 1. 展平 FieldEvidence
        flat = self._flatten_record(record)

        # 2. Pydantic Schema 校验
        try:
            validated = RDCapitalizationRecord.model_validate(flat)
        except Exception as e:
            return None, f"Pydantic 校验失败: {e}"

        # 2.5 Table fallback for missing LLM-extracted numeric fields
        fallback_values = self._table_fallback.get(record.get("doc_id", ""), {})
        if fallback_values:
            filled_fields: list[str] = []
            for schema_field, table_value in fallback_values.items():
                if getattr(validated, schema_field) is None and table_value is not None:
                    setattr(validated, schema_field, table_value)
                    filled_fields.append(schema_field)
            if filled_fields:
                if not validated.evidence_text:
                    validated.evidence_text = (
                        "table fallback: " + ", ".join(filled_fields)
                    )
                # data_quality_notes is not part of RDCapitalizationRecord, but we
                # can carry it in the dict if downstream expects it. The scored stage
                # reads from JSONL and uses data_quality_notes; add it to flat.
                # However, validated is a Pydantic model without data_quality_notes.
                # We will inject the note when serializing in _save_record.
                self._table_fallback_notes[record.get("doc_id", "")] = [
                    f"table_fallback: {f}" for f in filled_fields
                ]

        # 3. 会计恒等式校验
        passed, msg = self._identity_check(validated)
        if not passed:
            return None, msg

        # 4. 资本化率一致性校验
        passed, msg = self._rate_consistency_check(validated)
        if not passed:
            return None, msg

        return validated, ""

    def run(self) -> dict[str, int]:
        """运行校验

        Returns:
            统计信息: {"total": 总数, "passed": 通过数, "failed": 失败数}
        """
        if not self.input_path.exists():
            logger.warning("未找到抽取结果: %s", self.input_path)
            return {"total": 0, "passed": 0, "failed": 0}

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("", encoding="utf-8")
        self.error_path.write_text("", encoding="utf-8")

        total = 0
        passed = 0
        failed = 0

        with open(self.input_path, "r", encoding="utf-8") as f_in:
            for line in f_in:
                line = line.strip()
                if not line:
                    continue

                total += 1

                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    failed += 1
                    self._save_error({"error": "JSON 解析失败", "raw": line})
                    continue

                validated, error = self.validate_record(record)
                if validated:
                    self._save_record(validated)
                    passed += 1
                else:
                    self._save_error({
                        "doc_id": record.get("doc_id", ""),
                        "error": error,
                        "raw": record,
                    })
                    failed += 1

        logger.info(
            "校验完成: total=%d, passed=%d, failed=%d",
            total, passed, failed,
        )
        return {"total": total, "passed": passed, "failed": failed}

    def _save_record(self, record: RDCapitalizationRecord) -> None:
        """保存通过校验的记录"""
        data = record.model_dump()
        notes = self._table_fallback_notes.get(record.doc_id)
        if notes:
            data["data_quality_notes"] = notes
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def _save_error(self, error: dict[str, Any]) -> None:
        """保存校验错误"""
        with open(self.error_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(error, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    validator = DataValidator()
    stats = validator.run()
    print(f"\n{'✅' if stats['failed'] == 0 else '⚠️'} 校验完成: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
