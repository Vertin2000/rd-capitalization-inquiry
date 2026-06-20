"""Tests for ranked annual-report section routing."""

from __future__ import annotations

import json
from pathlib import Path

from src.route.section_router import SectionRouter


def make_router(tmp_path: Path) -> SectionRouter:
    rules_path = tmp_path / "section_rules.yaml"
    rules_path.write_text(
        """
rules:
  - name: "研发费用"
    keywords: ["研发投入", "研发费用"]
    positive_keywords: ["研发投入金额", "费用化的金额", "资本化的金额", "资本化研发投入占研发投入的比例"]
    negative_keywords: ["董事长", "公司简介", "联系方式"]
    priority: 1
    max_slices: 2
    context_before: 1
    context_after: 8

  - name: "开发支出"
    keywords: ["开发支出"]
    positive_keywords: ["本期增加", "期初余额", "期末余额", "内部开发支出"]
    negative_keywords: ["资产负债表"]
    priority: 2
    max_slices: 1
    context_before: 1
    context_after: 8
""",
        encoding="utf-8",
    )
    return SectionRouter(
        parsed_dir=str(tmp_path / "parsed"),
        output_dir=str(tmp_path / "sections"),
        rules_path=str(rules_path),
    )


def test_router_prefers_rd_investment_table_over_generic_discussion(
    tmp_path: Path,
) -> None:
    """High-signal R&D investment tables should outrank vague keyword mentions."""
    router = make_router(tmp_path)
    md_path = tmp_path / "parsed" / "sample.md"
    md_path.parent.mkdir(parents=True)
    md_path.write_text(
        "\n".join(
            [
                "董事长致辞：公司持续进行高强度研发投入。",
                "公司简介和联系方式。",
                "## 管理层讨论与分析",
                "## 研发投入情况",
                "<table><tr><td>项目</td><td>2023年</td></tr>",
                "<tr><td>研发投入金额</td><td>26,783.3</td></tr>",
                "<tr><td>费用化的金额</td><td>25,289.2</td></tr>",
                "<tr><td>资本化的金额</td><td>1,494.1</td></tr>",
                "<tr><td>资本化研发投入占研发投入的比例</td><td>5.58%</td></tr></table>",
            ],
        ),
        encoding="utf-8",
    )

    slices = router._find_sections(md_path, "sample")

    rd_slice = next(s for s in slices if s.section_name == "研发费用")
    assert "研发投入金额" in rd_slice.text
    assert "资本化的金额" in rd_slice.text
    assert "董事长致辞" not in rd_slice.text
    assert rd_slice.match_score > 0
    assert "positive:" in rd_slice.match_reason


def test_router_prefers_development_cost_note_over_balance_sheet_line(
    tmp_path: Path,
) -> None:
    """Development cost note tables should outrank isolated balance-sheet rows."""
    router = make_router(tmp_path)
    md_path = tmp_path / "parsed" / "sample.md"
    md_path.parent.mkdir(parents=True)
    md_path.write_text(
        "\n".join(
            [
                "## 资产负债表",
                "<table><tr><td>开发支出</td><td>7,697,446</td></tr></table>",
                "## 财务报表附注",
                "## 16. 开发支出",
                "<table><tr><td>项目</td><td>期初余额</td><td>本期增加</td><td>期末余额</td></tr>",
                "<tr><td>内部开发支出</td><td>100</td><td>50</td><td>150</td></tr></table>",
            ],
        ),
        encoding="utf-8",
    )

    slices = router._find_sections(md_path, "sample")

    dev_slice = next(s for s in slices if s.section_name == "开发支出")
    assert "本期增加" in dev_slice.text
    assert "期末余额" in dev_slice.text
    assert dev_slice.matched_keyword == "开发支出"


def test_route_force_overwrites_existing_section_file(tmp_path: Path) -> None:
    """force=True should regenerate an existing section JSONL file."""
    router = make_router(tmp_path)
    md_path = tmp_path / "parsed" / "sample.md"
    md_path.parent.mkdir(parents=True)
    md_path.write_text("研发投入金额\n资本化的金额\n", encoding="utf-8")
    output_path = tmp_path / "sections" / "sample_sections.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("stale\n", encoding="utf-8")

    result = router.route(md_path, "sample", force=True)

    assert result == output_path
    first_line = output_path.read_text(encoding="utf-8").splitlines()[0]
    assert json.loads(first_line)["doc_id"] == "sample"
    assert "stale" not in first_line


def test_route_writes_empty_file_when_no_section_matches(tmp_path: Path) -> None:
    """No-match documents still get an empty marker file for resume semantics."""
    router = make_router(tmp_path)
    md_path = tmp_path / "parsed" / "sample.md"
    md_path.parent.mkdir(parents=True)
    md_path.write_text("没有目标关键词\n", encoding="utf-8")

    result = router.route(md_path, "sample", force=True)

    assert result is not None
    assert result.read_text(encoding="utf-8") == ""


def test_section_check_report_marks_found_and_not_found(tmp_path: Path) -> None:
    """section_check_report 应区分定位成功与未定位的文档。"""
    router = make_router(tmp_path)
    parsed_dir = tmp_path / "parsed"
    parsed_dir.mkdir(parents=True)

    # doc A：能匹配研发费用
    (parsed_dir / "docA.md").write_text(
        "## 研发投入情况\n<table><tr><td>研发投入金额</td><td>100</td></tr>"
        "<tr><td>费用化的金额</td><td>80</td></tr>"
        "<tr><td>资本化的金额</td><td>20</td></tr></table>\n",
        encoding="utf-8",
    )
    # doc B：无匹配
    (parsed_dir / "docB.md").write_text("无关内容\n", encoding="utf-8")

    router.run(force=True)

    report_csv = tmp_path / "reports" / "section_check_report.csv"
    report_md = tmp_path / "reports" / "section_check_report.md"
    stats = router._write_section_check_report(report_csv, report_md)

    assert stats["found"] >= 1
    assert stats["not_found"] >= 1

    import csv as csv_mod
    with open(report_csv, "r", encoding="utf-8", newline="") as f:
        rows = list(csv_mod.DictReader(f))
    doc_ids = {r["doc_id"] for r in rows}
    assert "docA" in doc_ids and "docB" in doc_ids
    found_a = [r for r in rows if r["doc_id"] == "docA" and r["found"] == "yes"]
    not_found_b = [r for r in rows if r["doc_id"] == "docB" and r["found"] == "no"]
    assert found_a, "docA 应至少有一行 found=yes"
    assert not_found_b, "docB 应有 found=no 行"
    # found=yes 行应带 page_unavailable（parsed md 无页码）
    for r in found_a:
        assert "page_unavailable" in r["quality_issue"]
    # found=no 行标记 no_slice_found
    for r in not_found_b:
        assert r["quality_issue"] == "no_slice_found"

    md_text = report_md.read_text(encoding="utf-8")
    assert "质量问题分布" in md_text
    assert "page_unavailable" in md_text
