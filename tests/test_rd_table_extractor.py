"""Tests for deterministic R&D table extraction from Markdown HTML tables."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.extract.rd_table_extractor import (
    RDTableExtractor,
    _detect_unit,
    _normalize_number,
)


def test_normalize_number_handles_chinese_formats() -> None:
    assert _normalize_number("1,234.56") == 1234.56
    assert _normalize_number("1，234.56") == 1234.56
    assert _normalize_number("(123.45)") == -123.45
    assert _normalize_number("—") is None
    assert _normalize_number("不适用") is None
    assert _normalize_number("") is None
    assert _normalize_number("12.5%") == 12.5


def test_detect_unit_finds_yuan_wan_yuan_baiwan() -> None:
    text = "单位：人民币万元\n<table>...</table>"
    table_start = text.find("<table")
    table_end = text.find("/table>") + len("/table>")
    assert _detect_unit(text, table_start, table_end) == "万元"

    text = "单位：元\n<table>...</table>"
    table_start = text.find("<table")
    table_end = text.find("/table>") + len("/table>")
    assert _detect_unit(text, table_start, table_end) == "元"

    text = "单位：百万元人民币\n<table>...</table>"
    table_start = text.find("<table")
    table_end = text.find("/table>") + len("/table>")
    assert _detect_unit(text, table_start, table_end) == "百万元"

    text = "<table>...</table>"
    table_start = text.find("<table")
    table_end = text.find("/table>") + len("/table>")
    assert _detect_unit(text, table_start, table_end) == "元"


def test_find_tables_extracts_html_blocks() -> None:
    md = "some text <table><tr><td>A</td></tr></table> more"
    tables = RDTableExtractor._find_tables(md)
    assert len(tables) == 1
    assert tables[0][2].startswith("<table")
    assert tables[0][2].endswith("/table>")


def test_extract_one_rd_investment_table(tmp_path: Path) -> None:
    md_path = tmp_path / "600276_恒瑞医药_2023年报.md"
    md_path.write_text(
        '单位：人民币万元\n'
        '<table>'
        '<tr><td>项目</td><td>2023年</td><td>2022年</td></tr>'
        '<tr><td>本期费用化研发投入</td><td>5,000.00</td><td>4,500.00</td></tr>'
        '<tr><td>本期资本化研发投入</td><td>500.00</td><td>300.00</td></tr>'
        '<tr><td>研发投入合计</td><td>5,500.00</td><td>4,800.00</td></tr>'
        '</table>',
        encoding="utf-8",
    )
    extractor = RDTableExtractor(
        parsed_dir=tmp_path,
        output_dir=tmp_path / "tables",
    )
    records = extractor.extract_one(md_path)

    by_label = {r["row_label"]: r for r in records}
    assert "expensed_amount" in by_label
    assert "capitalized_amount" in by_label
    assert "total_amount" in by_label
    assert by_label["expensed_amount"]["value"] == 5000.0
    assert by_label["capitalized_amount"]["value"] == 500.0
    assert by_label["total_amount"]["value"] == 5500.0
    assert by_label["expensed_amount"]["unit"] == "万元"


def test_extract_one_development_expenditure_table(tmp_path: Path) -> None:
    md_path = tmp_path / "000063_中兴通讯_2023年报.md"
    md_path.write_text(
        '单位：百万元人民币\n'
        '<table>'
        '<tr><td></td><td>年初余额</td><td>本年增加</td><td>本年减少</td><td>年末余额</td></tr>'
        '<tr><td>手机产品</td><td>100</td><td>200</td><td>50</td><td>250</td></tr>'
        '<tr><td>合计</td><td>1,000</td><td>2,000</td><td>500</td><td>2,500</td></tr>'
        '</table>',
        encoding="utf-8",
    )
    extractor = RDTableExtractor(
        parsed_dir=tmp_path,
        output_dir=tmp_path / "tables",
    )
    records = extractor.extract_one(md_path)

    by_label = {r["row_label"]: r for r in records}
    assert "opening_balance" in by_label
    assert "closing_balance" in by_label
    assert by_label["opening_balance"]["value"] == 100000.0  # 百万元 -> 万元
    assert by_label["closing_balance"]["value"] == 250000.0


def test_run_writes_jsonl(tmp_path: Path) -> None:
    md_path = tmp_path / "600276_恒瑞医药_2023年报.md"
    md_path.write_text(
        '单位：万元\n'
        '<table>'
        '<tr><td>项目</td><td>2023年</td></tr>'
        '<tr><td>研发投入合计</td><td>1,000.00</td></tr>'
        '</table>',
        encoding="utf-8",
    )
    extractor = RDTableExtractor(
        parsed_dir=tmp_path,
        output_dir=tmp_path / "tables",
    )
    stats = extractor.run(output_path=tmp_path / "tables" / "tables.jsonl")
    assert stats["total"] == 1
    assert stats["records"] >= 1

    out_path = tmp_path / "tables" / "tables.jsonl"
    assert out_path.exists()
    lines = list(out_path.open("r", encoding="utf-8"))
    assert len(lines) >= 1
    first = __import__("json").loads(lines[0])
    assert first["doc_id"] == "600276_恒瑞医药_2023年报"
    assert first["table_type"] == "rd_investment"
