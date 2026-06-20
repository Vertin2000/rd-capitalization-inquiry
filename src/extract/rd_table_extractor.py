"""Deterministic extraction of R&D capitalization tables from MinerU Markdown.

MinerU renders tables as HTML ``<table>`` blocks inside the Markdown. This module
parses those tables, identifies the two critical table types for this project:

1. **研发投入情况表** (R&D investment summary)
2. **开发支出明细表** (development expenditure detail)
3. **无形资产附注** (intangible assets note, for cross-check only)

and extracts the rows needed for capitalization-rate calculation and validation.

Output is written to ``data/extracted/tables/tables.jsonl`` and can be
used as a fallback / cross-check for the LLM extractor.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

TABLE_TYPE_RULES: list[tuple[str, list[str]]] = [
    (
        "rd_investment",
        ["研发投入", "研发费用", "研发支出", "费用化", "资本化"],
    ),
    (
        "development_expenditure",
        ["开发支出", "年初余额", "年末余额", "期初余额", "期末余额", "本年增加", "本期增加"],
    ),
    (
        "intangible_assets",
        ["无形资产", "内部研发", "自行开发"],
    ),
]

# Order matters: longer / more specific labels should be checked first.
RD_INVESTMENT_ROW_PATTERNS: dict[str, list[str]] = {
    "capitalization_rate": [
        "资本化研发投入占研发投入的比例",
        "研发投入资本化的比重",
        "研发投入资本化率",
        "资本化研发投入占比",
        "资本化率",
    ],
    "expensed_amount": [
        "本期费用化研发投入",
        "费用化研发投入",
        "费用化的金额",
        "费用化研发支出",
        "费用化金额",
        "研发费用化金额",
    ],
    "capitalized_amount": [
        "本期资本化研发投入",
        "资本化研发投入",
        "研发投入资本化的金额",
        "资本化的金额",
        "资本化研发支出",
        "资本化金额",
    ],
    "total_amount": [
        "研发投入合计",
        "研发投入金额",
        "研发支出合计",
        "研发费用合计",
        "研发投入总计",
        "研发支出总计",
        "研发费用总计",
        "合计",
    ],
}

DEV_EXPENDITURE_ROW_PATTERNS: dict[str, list[str]] = {
    "opening_balance": ["期初余额", "年初余额"],
    "internal_development": ["内部开发支出", "内部研发支出", "内部研究开发支出"],
    "current_additions": ["本期增加金额", "本年增加", "本期增加"],
    "recognized_intangible": ["确认为无形资产"],
    "transferred_to_expense": ["转入当期损益"],
    "current_reductions": ["本期减少金额", "本年减少", "本期减少"],
    "closing_balance": ["期末余额", "年末余额"],
}

INTANGIBLE_ASSETS_ROW_PATTERNS: dict[str, list[str]] = {
    "internal_development": ["内部研发", "自行开发"],
    "development_expenditure_category": ["开发支出"],
}

UNIT_PATTERN = re.compile(r"单位[：:]\s*([^\n<]+)", re.UNICODE)
LABEL_UNIT_PATTERN = re.compile(r"[（(]([^）)]*(?:百万元|万元|元))[^）)]*[）)]", re.UNICODE)


def _normalize_number(value: Any) -> float | None:
    """Convert a Chinese numeric cell to a float (in original unit)."""
    if value is None:
        return None
    text = str(value).strip()
    if text in {"", "—", "-", "/", "不适用", "None", "null"}:
        return None
    # Remove thousand separators and percent sign
    text = text.replace(",", "").replace("，", "").replace("%", "").strip()
    # Handle parentheses as negative: (1,234) -> -1234
    negative = False
    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1]
    try:
        number = float(text)
    except (TypeError, ValueError):
        return None
    if negative:
        number = -number
    return number


def _extract_unit_from_text(text: str) -> str | None:
    """Look for '百万元' / '万元' / '元' in a short text snippet."""
    text = str(text or "")
    if "百万元" in text or "百万" in text:
        return "百万元"
    if "万元" in text:
        return "万元"
    if "元" in text:
        return "元"
    return None


def _detect_unit(md_text: str, table_start: int, table_end: int) -> str:
    """Look for '单位：...' near the table (before or after)."""
    # Before table
    window_start = max(0, table_start - 1500)
    window = md_text[window_start:table_start]
    match = UNIT_PATTERN.search(window)
    if match:
        unit = _extract_unit_from_text(match.group(1))
        if unit:
            return unit
    # After table (some publishers put the unit note below the table)
    window_end = min(len(md_text), table_end + 1500)
    window = md_text[table_end:window_end]
    match = UNIT_PATTERN.search(window)
    if match:
        unit = _extract_unit_from_text(match.group(1))
        if unit:
            return unit
    return "元"  # conservative default


def _to_wan_yuan(value: float | None, unit: str) -> float | None:
    """Normalize a numeric value to 万元."""
    if value is None:
        return None
    if unit == "百万元":
        return round(value * 100, 6)
    if unit == "万元":
        return round(value, 6)
    if unit == "元":
        return round(value / 10000, 6)
    return value


def _cell_text(cell: Any) -> str:
    return str(cell).strip().replace("\n", " ")


def _match_row_label(row_label: str, patterns: list[str]) -> bool:
    compact = re.sub(r"\s+", "", row_label)
    if not compact:
        return False
    for pattern in patterns:
        if pattern in compact or compact in pattern:
            return True
    return False


def _extract_year_from_header(header: str) -> int | None:
    match = re.search(r"(20\d{2})\s*[年]?", header)
    if match:
        return int(match.group(1))
    return None


def _year_from_doc_id(doc_id: str) -> int | None:
    match = re.search(r"(20\d{2})年报", doc_id)
    if match:
        return int(match.group(1))
    return None


def _parse_table(html: str) -> list[list[str]]:
    """Parse an HTML table into a rectangular grid of cell texts.

    Expands ``rowspan`` and ``colspan`` by duplicating merged cells so that
    downstream logic sees a regular 2-D grid.
    """
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []

    grid: list[list[str]] = []
    # pending[col] = list of (remaining_rows, cell_text) to insert at col
    pending: list[list[tuple[int, str]]] = []

    for tr in table.find_all("tr"):
        row: list[str] = []
        col = 0
        # Drain pending cells for this row
        while pending and col < len(pending) and pending[col]:
            remaining, text = pending[col].pop(0)
            row.append(text)
            if remaining > 1:
                # Re-queue for subsequent rows
                if col >= len(pending):
                    pending.extend([[] for _ in range(col - len(pending) + 1)])
                pending[col].append((remaining - 1, text))
            col += 1

        for cell in tr.find_all(["td", "th"]):
            text = _cell_text(cell.get_text())
            rowspan = int(cell.get("rowspan", 1) or 1)
            colspan = int(cell.get("colspan", 1) or 1)

            # Make room in pending list
            while col >= len(pending):
                pending.append([])

            # Place the cell (and duplicates for colspan)
            for _ in range(colspan):
                row.append(text)
                if rowspan > 1:
                    pending[col].append((rowspan - 1, text))
                col += 1
                while col >= len(pending):
                    pending.append([])

        if row:
            grid.append(row)

    return grid


class RDTableExtractor:
    """Extract R&D capitalization tables from MinerU Markdown files."""

    def __init__(
        self,
        parsed_dir: str | Path = "data/parsed",
        output_dir: str | Path = "data/extracted/tables",
    ) -> None:
        self.project_root = PROJECT_ROOT
        self.parsed_dir = self._resolve(parsed_dir)
        self.output_dir = self._resolve(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _resolve(path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    @staticmethod
    def _find_tables(md_text: str) -> list[tuple[int, int, str]]:
        """Return list of (start_index, end_index, html_table_string)."""
        tables: list[tuple[int, int, str]] = []
        start = 0
        while True:
            table_start = md_text.find("<table", start)
            if table_start == -1:
                break
            table_end = md_text.find("/table>", table_start)
            if table_end == -1:
                break
            table_end += len("/table>")
            tables.append((table_start, table_end, md_text[table_start:table_end]))
            start = table_end
        return tables

    def _classify_table(self, rows: list[list[str]]) -> str | None:
        """Classify table type based on cell contents."""
        flat = " ".join(" ".join(row) for row in rows)
        for table_type, keywords in TABLE_TYPE_RULES:
            if any(kw in flat for kw in keywords[:3]):
                if table_type == "rd_investment" and any(
                    kw in flat for kw in ["费用化", "资本化", "合计"]
                ):
                    return table_type
                if table_type == "development_expenditure" and any(
                    kw in flat
                    for kw in ["期初余额", "期末余额", "年初余额", "年末余额"]
                ):
                    return table_type
                if table_type == "intangible_assets" and any(
                    kw in flat for kw in ["无形资产", "内部研发", "自行开发"]
                ):
                    return table_type
        return None

    def _extract_rd_investment_rows(
        self,
        rows: list[list[str]],
        table_unit: str,
        doc_id: str,
        evidence_text: str,
        doc_year: int | None = None,
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        if not rows:
            return records

        # Determine year columns (skip first label column)
        headers = rows[0]
        year_columns: list[tuple[int, int | None]] = []
        for col_idx, header in enumerate(headers[1:], start=1):
            year = _extract_year_from_header(header)
            year_columns.append((col_idx, year))

        for row in rows[1:]:
            if not row:
                continue
            label = _cell_text(row[0])
            if not label:
                continue

            field_name: str | None = None
            for fname, patterns in RD_INVESTMENT_ROW_PATTERNS.items():
                if _match_row_label(label, patterns):
                    field_name = fname
                    break
            if not field_name:
                continue

            # Try to extract unit from the row label itself (e.g. "...（百万元人民币）")
            label_unit_match = LABEL_UNIT_PATTERN.search(label)
            row_unit = (
                _extract_unit_from_text(label_unit_match.group(1))
                if label_unit_match
                else None
            )
            effective_unit = row_unit or table_unit

            is_rate_field = field_name == "capitalization_rate"

            for col_idx, year in year_columns:
                if col_idx >= len(row):
                    continue
                # 只取与年报年度匹配的列；若 doc_year 未知则全部保留
                if doc_year is not None and year != doc_year:
                    continue
                raw_value = row[col_idx]
                number = _normalize_number(raw_value)
                if number is None:
                    continue
                if is_rate_field:
                    value = number
                    unit = "%"
                else:
                    value = _to_wan_yuan(number, effective_unit)
                    unit = "万元"
                records.append(
                    {
                        "doc_id": doc_id,
                        "table_type": "rd_investment",
                        "row_label": field_name,
                        "display_label": label,
                        "year": year,
                        "value": value,
                        "unit": unit,
                        "raw_value": _cell_text(raw_value),
                        "original_unit": effective_unit,
                        "evidence_text": evidence_text,
                    }
                )
        return records

    def _extract_development_expenditure_rows(
        self,
        rows: list[list[str]],
        unit: str,
        doc_id: str,
        evidence_text: str,
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        if not rows:
            return records

        header_row_idx: int | None = None
        for idx, row in enumerate(rows):
            if not row:
                continue
            first = _cell_text(row[0])
            if first in {"", "项目", "项目类型", "类别", "项目/类别"}:
                header_row_idx = idx
                break
        if header_row_idx is None:
            return records

        header = rows[header_row_idx]
        col_to_field: dict[int, str] = {}
        for col_idx, cell in enumerate(header[1:], start=1):
            label = _cell_text(cell)
            for fname, patterns in DEV_EXPENDITURE_ROW_PATTERNS.items():
                if _match_row_label(label, patterns):
                    col_to_field[col_idx] = fname
                    break

        total_row: list[str] | None = None
        for row in rows:
            if row and _cell_text(row[0]) in {"合计", "总计"}:
                total_row = row
                break
        if not total_row:
            return records

        for col_idx, field_name in col_to_field.items():
            if col_idx >= len(total_row):
                continue
            raw_value = total_row[col_idx]
            number = _normalize_number(raw_value)
            if number is None:
                continue
            value = _to_wan_yuan(number, unit)
            records.append(
                {
                    "doc_id": doc_id,
                    "table_type": "development_expenditure",
                    "row_label": field_name,
                    "display_label": header[col_idx],
                    "year": None,
                    "value": value,
                    "unit": "万元",
                    "raw_value": _cell_text(raw_value),
                    "original_unit": unit,
                    "evidence_text": evidence_text,
                }
            )
        return records

    def _extract_intangible_assets_rows(
        self,
        rows: list[list[str]],
        unit: str,
        doc_id: str,
        evidence_text: str,
    ) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for row in rows:
            if not row:
                continue
            label = _cell_text(row[0])
            if not label:
                continue
            field_name: str | None = None
            for fname, patterns in INTANGIBLE_ASSETS_ROW_PATTERNS.items():
                if _match_row_label(label, patterns):
                    field_name = fname
                    break
            if not field_name:
                continue
            for col_idx in range(len(row) - 1, 0, -1):
                raw_value = row[col_idx]
                number = _normalize_number(raw_value)
                if number is not None:
                    value = _to_wan_yuan(number, unit)
                    records.append(
                        {
                            "doc_id": doc_id,
                            "table_type": "intangible_assets",
                            "row_label": field_name,
                            "display_label": label,
                            "year": None,
                            "value": value,
                            "unit": "万元",
                            "raw_value": _cell_text(raw_value),
                            "original_unit": unit,
                            "evidence_text": evidence_text,
                        }
                    )
                    break
        return records

    def _extract_from_table(
        self,
        md_text: str,
        table_start: int,
        table_end: int,
        html: str,
        doc_id: str,
        doc_year: int | None = None,
    ) -> list[dict[str, Any]]:
        rows = _parse_table(html)
        if not rows:
            return []
        table_type = self._classify_table(rows)
        if not table_type:
            return []
        unit = _detect_unit(md_text, table_start, table_end)
        evidence_text = f"{table_type} table at offset {table_start} (unit: {unit})"
        if table_type == "rd_investment":
            return self._extract_rd_investment_rows(
                rows, unit, doc_id, evidence_text, doc_year=doc_year
            )
        if table_type == "development_expenditure":
            return self._extract_development_expenditure_rows(
                rows, unit, doc_id, evidence_text
            )
        if table_type == "intangible_assets":
            return self._extract_intangible_assets_rows(
                rows, unit, doc_id, evidence_text
            )
        return []

    def extract_one(self, md_path: Path) -> list[dict[str, Any]]:
        doc_id = md_path.stem
        doc_year = _year_from_doc_id(doc_id)
        md_text = md_path.read_text(encoding="utf-8")
        tables = self._find_tables(md_text)
        records: list[dict[str, Any]] = []
        for table_start, table_end, html in tables:
            try:
                records.extend(
                    self._extract_from_table(
                        md_text,
                        table_start,
                        table_end,
                        html,
                        doc_id,
                        doc_year=doc_year,
                    )
                )
            except Exception as exc:
                logger.warning("[%s] 表格提取异常: %s", doc_id, exc)
        return records

    def run(
        self,
        limit: int | None = None,
        output_path: str | Path | None = None,
    ) -> dict[str, int]:
        md_files = sorted(self.parsed_dir.glob("*.md"))
        if not md_files:
            logger.warning("未找到 Markdown 文件: %s", self.parsed_dir)
            return {"total": 0, "tables": 0, "records": 0}

        if limit:
            md_files = md_files[:limit]

        out_path = self.output_dir / "tables.jsonl"
        if output_path:
            out_path = self._resolve(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("", encoding="utf-8")

        total_tables = 0
        total_records = 0
        for md_path in md_files:
            records = self.extract_one(md_path)
            if records:
                total_tables += len(
                    {r.get("evidence_text") for r in records}
                )
                total_records += len(records)
                with out_path.open("a", encoding="utf-8") as f:
                    for record in records:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")

        logger.info(
            "表格提取完成: docs=%d, tables=%d, records=%d",
            len(md_files),
            total_tables,
            total_records,
        )
        return {
            "total": len(md_files),
            "tables": total_tables,
            "records": total_records,
        }


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #


def main() -> int:
    """独立运行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Extract R&D tables from MinerU Markdown")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of Markdown files to process",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Override the output JSONL path",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    extractor = RDTableExtractor()
    stats = extractor.run(limit=args.limit, output_path=args.output)
    print(f"\n{'✅' if stats['records'] > 0 else '⚠️'} 表格提取完成: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
