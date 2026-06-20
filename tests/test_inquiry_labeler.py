"""Tests for the improved inquiry labeler (script pruning + optional LLM)."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pytest

from src.analysis.inquiry_labeler import (
    InquiryLabeler,
    _classify_keywords,
    _is_inquiry_family,
    _is_reply_family,
)


def test_classify_keywords_tier1_direct() -> None:
    """资本化 / 开发支出应直接触发 Tier-1。"""
    tier1, tier2 = _classify_keywords("请问公司开发支出余额大幅上升的原因")
    assert "开发支出" in tier1
    assert not tier2


def test_classify_keywords_expense_only_no_rd_context() -> None:
    """单独的费用化不应触发 Tier-1。"""
    tier1, tier2 = _classify_keywords("请说明本期费用化金额")
    assert "费用化" not in tier1


def test_classify_keywords_expensed_with_rd_context() -> None:
    """研发费用化 + 研发语境应触发 Tier-1。"""
    tier1, tier2 = _classify_keywords("请说明本期研发费用化研发投入金额")
    assert "费用化" in tier1


def test_classify_keywords_tier2_broad() -> None:
    """单独的 研发 只触发 Tier-2。"""
    tier1, tier2 = _classify_keywords("请说明公司研发投入情况")
    assert not tier1
    assert "研发" in tier2


def test_role_classification() -> None:
    assert _is_inquiry_family("inquiry_notice")
    assert _is_inquiry_family("attention_letter")
    assert _is_inquiry_family("regulatory_work_letter")
    assert _is_inquiry_family("process_other")
    assert not _is_inquiry_family("substantive_reply")
    assert _is_reply_family("substantive_reply")
    assert _is_reply_family("delay_notice")
    assert _is_reply_family("supporting_statement")


@pytest.fixture
def labeler(tmp_path: Path) -> InquiryLabeler:
    """Build a labeler that uses temp paths and never calls a real LLM."""
    metadata_path = tmp_path / "metadata.csv"
    candidates_path = tmp_path / "candidates.csv"
    output_path = tmp_path / "inquiry_records.jsonl"

    return InquiryLabeler(
        metadata_path=metadata_path,
        candidates_path=candidates_path,
        output_path=output_path,
        project_root=tmp_path,
        pdf_text_extractor=lambda _path: "",
        use_llm=False,
    )


def _write_metadata(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "doc_id",
                "stock_code",
                "stock_name",
                "market",
                "announcement_title",
                "announcement_type",
                "publish_date",
                "url",
                "pdf_url",
                "local_pdf_path",
                "download_status",
                "source",
                "crawl_time",
                "error_message",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_candidates(path: Path, rows: list[dict[str, str]]) -> None:
    columns = [
        "annual_doc_id",
        "report_year",
        "query_window_start",
        "query_window_end",
        "doc_id",
        "stock_code",
        "stock_name",
        "market",
        "announcement_id",
        "announcement_title",
        "announcement_type",
        "document_role",
        "publish_date",
        "url",
        "pdf_url",
        "local_pdf_path",
        "download_status",
        "source",
        "crawl_time",
        "error_message",
        "notes",
        "pdf_title",
        "pdf_title_status",
        "title_match_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            full = {col: "" for col in columns}
            full.update(row)
            writer.writerow(full)


def test_label_one_tier1_inquiry_is_related(labeler: InquiryLabeler) -> None:
    """问询函标题命中 Tier-1 关键词应判为相关。"""
    annual = {
        "doc_id": "600276_恒瑞医药_2023年报",
        "stock_code": "600276",
        "stock_name": "恒瑞医药",
        "market": "sh",
        "announcement_title": "恒瑞医药2023年年度报告",
        "announcement_type": "年度报告",
        "publish_date": "2024-04-20",
        "url": "",
        "pdf_url": "",
        "local_pdf_path": "",
        "download_status": "success",
        "source": "cninfo_official_api",
        "crawl_time": "",
        "error_message": "",
        "notes": "",
    }
    candidates = [
        {
            "annual_doc_id": "600276_恒瑞医药_2023年报",
            "doc_id": "600276_恒瑞医药_2023_2024-05-20_inquiry_notice_1",
            "stock_code": "600276",
            "stock_name": "恒瑞医药",
            "announcement_title": "关于对恒瑞医药2023年年报研发支出资本化的问询函",
            "document_role": "inquiry_notice",
            "publish_date": "2024-05-20",
        }
    ]
    result = labeler._label_one(annual, candidates)
    assert result["inquiry_received"] is True
    assert result["capitalization_related"] is True
    assert result["inquiry_actually_received"] is True
    assert result["reply_received"] is False


def test_label_one_reply_only_is_not_inquiry(labeler: InquiryLabeler) -> None:
    """只有回复函时不应判为收到问询。"""
    annual = {
        "doc_id": "600276_恒瑞医药_2023年报",
        "stock_code": "600276",
        "stock_name": "恒瑞医药",
        "market": "sh",
        "announcement_title": "恒瑞医药2023年年度报告",
        "announcement_type": "年度报告",
        "publish_date": "2024-04-20",
        "url": "",
        "pdf_url": "",
        "local_pdf_path": "",
        "download_status": "success",
        "source": "cninfo_official_api",
        "crawl_time": "",
        "error_message": "",
        "notes": "",
    }
    candidates = [
        {
            "annual_doc_id": "600276_恒瑞医药_2023年报",
            "doc_id": "600276_恒瑞医药_2023_2024-05-20_substantive_reply_1",
            "stock_code": "600276",
            "stock_name": "恒瑞医药",
            "announcement_title": "恒瑞医药关于2023年年报问询函的回复公告",
            "document_role": "substantive_reply",
            "publish_date": "2024-05-25",
        }
    ]
    result = labeler._label_one(annual, candidates)
    assert result["inquiry_received"] is False
    assert result["reply_received"] is True
    assert result["capitalization_related"] is False


def test_label_one_broad_keyword_without_llm_not_related(
    labeler: InquiryLabeler,
) -> None:
    """仅命中泛词且不使用 LLM 时，应判为不相关。"""
    annual = {
        "doc_id": "601360_三六零_2023年报",
        "stock_code": "601360",
        "stock_name": "三六零",
        "market": "sh",
        "announcement_title": "三六零2023年年度报告",
        "announcement_type": "年度报告",
        "publish_date": "2024-04-20",
        "url": "",
        "pdf_url": "",
        "local_pdf_path": "",
        "download_status": "success",
        "source": "cninfo_official_api",
        "crawl_time": "",
        "error_message": "",
        "notes": "",
    }
    candidates = [
        {
            "annual_doc_id": "601360_三六零_2023年报",
            "doc_id": "601360_三六零_2023_2024-05-20_regulatory_work_letter_1",
            "stock_code": "601360",
            "stock_name": "三六零",
            "announcement_title": "关于对三六零2023年年度报告信息披露的监管工作函",
            "document_role": "regulatory_work_letter",
            "publish_date": "2024-05-20",
        }
    ]
    result = labeler._label_one(annual, candidates)
    # 监管工作函标题里没有 Tier-1 关键词，且 use_llm=False，所以不相关
    assert result["inquiry_received"] is True
    assert result["capitalization_related"] is False


def test_run_writes_one_record_per_annual(labeler: InquiryLabeler) -> None:
    """应每个年报记录输出一行，无候选也要保留以计算 TN/FN。"""
    _write_metadata(
        labeler.metadata_path,
        [
            {
                "doc_id": "600276_恒瑞医药_2023年报",
                "stock_code": "600276",
                "stock_name": "恒瑞医药",
                "market": "sh",
                "announcement_title": "恒瑞医药2023年年度报告",
                "announcement_type": "年度报告",
                "publish_date": "2024-04-20",
                "url": "",
                "pdf_url": "",
                "local_pdf_path": "",
                "download_status": "success",
                "source": "cninfo_official_api",
                "crawl_time": "",
                "error_message": "",
                "notes": "",
            },
            {
                "doc_id": "300760_迈瑞医疗_2023年报",
                "stock_code": "300760",
                "stock_name": "迈瑞医疗",
                "market": "sz",
                "announcement_title": "迈瑞医疗2023年年度报告",
                "announcement_type": "年度报告",
                "publish_date": "2024-04-18",
                "url": "",
                "pdf_url": "",
                "local_pdf_path": "",
                "download_status": "success",
                "source": "cninfo_official_api",
                "crawl_time": "",
                "error_message": "",
                "notes": "",
            },
        ],
    )
    _write_candidates(
        labeler.candidates_path,
        [
            {
                "annual_doc_id": "600276_恒瑞医药_2023年报",
                "doc_id": "600276_恒瑞医药_2023_2024-05-20_inquiry_notice_1",
                "stock_code": "600276",
                "stock_name": "恒瑞医药",
                "announcement_title": "关于对恒瑞医药2023年年报研发支出资本化的问询函",
                "document_role": "inquiry_notice",
                "publish_date": "2024-05-20",
            }
        ],
    )

    stats = labeler.run()
    assert stats["total"] == 2
    assert stats["with_candidates"] == 1

    rows = list(labeler.output_path.open("r", encoding="utf-8"))
    assert len(rows) == 2
    first = json.loads(rows[0])
    second = json.loads(rows[1])
    assert first["annual_doc_id"] == "600276_恒瑞医药_2023年报"
    assert first["inquiry_received"] is True
    assert second["annual_doc_id"] == "300760_迈瑞医疗_2023年报"
    assert second["inquiry_received"] is False
    assert "capitalization_related" in first
    assert "reply_received" in first
