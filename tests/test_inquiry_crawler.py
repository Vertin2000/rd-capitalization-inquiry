"""Tests for CNINFO inquiry/reply discovery crawler."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

import src.crawl.inquiry_crawler as inquiry_module
from src.crawl.inquiry_crawler import (
    INQUIRY_METADATA_COLUMNS,
    InquiryCrawler,
    add_days,
    classify_inquiry_title,
    clean_title,
)
from src.crawl.inquiry_quality import (
    audit_inquiry_pdf_titles,
    build_inquiry_doc_id,
    classify_document_role,
    extract_title_from_pdf_text,
    title_match_status,
    write_orphan_pdf_report,
)

import pytest


@pytest.fixture
def crawler(tmp_path: Path, monkeypatch) -> InquiryCrawler:
    """构造一个使用临时目录且不限速的问询 crawler。"""
    monkeypatch.setattr(
        inquiry_module,
        "load_config",
        lambda _path: {
            "download": {"delay_seconds": 0, "max_retries": 1},
            "inquiry_keywords": ["研发", "资本化", "开发支出", "无形资产", "费用化"],
        },
    )

    c = InquiryCrawler(limit=1)
    c.annual_metadata_path = tmp_path / "metadata.csv"
    c.candidates_path = tmp_path / "inquiry_candidates.csv"
    c.log_path = tmp_path / "inquiry_log.jsonl"
    c.cache_path = tmp_path / "inquiry_discovery_cache.json"
    c.download_pdf_dir = tmp_path / "pdf"
    return c


def test_add_days_generates_180_day_window_end() -> None:
    """年报发布日期后 180 天应作为问询主窗口结束日。"""
    assert add_days("2024-04-20", 180) == date(2024, 10, 17)


def test_clean_title_removes_cninfo_highlight_tags() -> None:
    """巨潮标题高亮标签不应进入候选 metadata。"""
    assert clean_title("<em>恒瑞医药</em>：关于年报问询函的回复公告") == "恒瑞医药：关于年报问询函的回复公告"
    assert clean_title("<em>通策医疗</em>") == "通策医疗"


def test_classify_inquiry_title() -> None:
    """标题分类应区分问询函、回复函、关注函和监管工作函。"""
    assert classify_inquiry_title("关于恒瑞医药2023年年报的问询函") == "inquiry"
    assert classify_inquiry_title("恒瑞医药关于年报问询函的回复公告") == "reply"
    assert classify_inquiry_title("关于对恒瑞医药的关注函") == "attention"
    assert classify_inquiry_title("关于对恒瑞医药发出监管工作函的公告") == "regulatory_work_letter"
    assert classify_inquiry_title("恒瑞医药关于研发项目进展的公告") == "other"
    assert classify_inquiry_title("会计师关于审核问询函的回复") == "other"
    assert classify_inquiry_title("关于发行注册环节反馈意见落实函回复的公告") == "other"
    assert classify_inquiry_title("发行人及保荐机构关于第二轮审核问询函的回复") == "other"
    assert classify_inquiry_title("通策医疗股份有限公司关于回复上海证券交易所问询函的公告") == "reply"


def test_classify_document_role() -> None:
    """document_role 应把正式回复、延期公告、专项说明和问询公告拆开。"""
    assert classify_document_role("通策医疗股份有限公司关于收到上海证券交易所问询函的公告") == "inquiry_notice"
    assert classify_document_role("通策医疗股份有限公司关于回复上海证券交易所问询函的公告") == "substantive_reply"
    assert classify_document_role("通策医疗股份有限公司关于延期回复上海证券交易所问询函的公告") == "delay_notice"
    assert classify_document_role("关于对通策医疗股份有限公司非经营性资金往来等相关事项问询函回复的专项说明") == "supporting_statement"
    assert classify_document_role("独立董事关于对深圳证券交易所创业板年报问询函相关事项核查的独立意见") == "supporting_statement"
    assert classify_document_role("关于对恒瑞医药的关注函") == "attention_letter"
    assert classify_document_role("关于对恒瑞医药发出监管工作函的公告") == "regulatory_work_letter"


def test_build_inquiry_doc_id_is_readable_and_stable() -> None:
    """问询 PDF 文件名应包含代码、公司、报告年度、日期、角色和 announcementId。"""
    assert build_inquiry_doc_id(
        stock_code="600763",
        stock_name="<em>通策医疗</em>",
        report_year="2021",
        publish_date="2022-09-06",
        document_role="substantive_reply",
        announcement_id="1214567890",
    ) == "600763_通策医疗_2021_2022-09-06_substantive_reply_1214567890"


def test_parse_candidate_maps_cninfo_fields(tmp_path: Path, crawler: InquiryCrawler) -> None:
    """CNINFO 前端返回字段应映射为下载器可复用的 metadata 行。"""
    item = {
        "secCode": "600276",
        "secName": "<em>恒瑞医药</em>",
        "announcementId": "1219999999",
        "announcementTitle": "<em>恒瑞医药</em>：关于2023年年报问询函的回复公告",
        "adjunctUrl": "finalpage/2024-05-20/1219999999.PDF",
        "announcementTime": 1716134400000,
    }

    record = crawler._parse_candidate(
        item,
        annual_record={
            "doc_id": "600276_恒瑞医药_2023年报",
            "stock_code": "600276",
            "stock_name": "恒瑞医药",
            "market": "sh",
            "publish_date": "2024-04-20",
        },
        report_year="2023",
    )

    assert record is not None
    assert record["annual_doc_id"] == "600276_恒瑞医药_2023年报"
    assert record["report_year"] == "2023"
    assert record["stock_code"] == "600276"
    assert record["stock_name"] == "恒瑞医药"
    assert record["announcement_id"] == "1219999999"
    assert record["announcement_title"] == "恒瑞医药：关于2023年年报问询函的回复公告"
    assert record["announcement_type"] == "reply"
    assert record["document_role"] == "substantive_reply"
    assert record["publish_date"] == "2024-05-20"
    assert record["pdf_url"] == "http://static.cninfo.com.cn/finalpage/2024-05-20/1219999999.PDF"
    assert record["doc_id"] == "600276_恒瑞医药_2023_2024-05-20_substantive_reply_1219999999"
    assert record["local_pdf_path"] == (
        "data/inquiry/pdf/600276_恒瑞医药_2023_2024-05-20_substantive_reply_1219999999.pdf"
    )
    assert record["download_status"] == "pending"
    assert record["pdf_title"] == ""
    assert record["pdf_title_status"] == ""
    assert record["title_match_status"] == ""
    assert list(record.keys()) == INQUIRY_METADATA_COLUMNS


def test_run_applies_limit_dedupes_and_writes_candidates(
    tmp_path: Path,
    crawler: InquiryCrawler,
    monkeypatch,
) -> None:
    """run 应按 limit 处理年报、去重候选，并写出 inquiry_candidates.csv。"""
    write_annual_metadata(
        crawler.annual_metadata_path,
        [
            {
                "doc_id": "600276_恒瑞医药_2023年报",
                "stock_code": "600276",
                "stock_name": "恒瑞医药",
                "market": "sh",
                "announcement_title": "恒瑞医药：2023年年度报告",
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
                "announcement_title": "迈瑞医疗：2023年年度报告",
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

    calls: list[tuple[str, str, str]] = []

    def fake_search(annual_record: dict[str, str], report_year: str) -> list[dict[str, str]]:
        calls.append((annual_record["stock_code"], annual_record["stock_name"], report_year))
        return [
            make_candidate("600276", "恒瑞医药", "1219999999", "关于恒瑞医药2023年年报的问询函"),
            make_candidate("600276", "恒瑞医药", "1219999999", "关于恒瑞医药2023年年报的问询函"),
        ]

    monkeypatch.setattr(crawler, "_search_for_annual_record", fake_search)
    monkeypatch.setattr(inquiry_module.time, "sleep", lambda _seconds: None)

    output_path = crawler.run(discover_only=True)

    rows = list(csv.DictReader(output_path.open("r", encoding="utf-8", newline="")))
    assert calls == [("600276", "恒瑞医药", "2023")]
    assert len(rows) == 1
    assert rows[0]["announcement_id"] == "1219999999"
    assert rows[0]["query_window_start"] == "2024-04-20"
    assert rows[0]["query_window_end"] == "2024-10-17"
    assert crawler.cache_path.read_text(encoding="utf-8")


def test_fetch_page_uses_public_frontend_query(crawler: InquiryCrawler, monkeypatch) -> None:
    """问询发现应走巨潮前端公开查询接口，而不是官方 API。"""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.raise_for_status = MagicMock()
    fake_response.json.return_value = {"announcements": [], "totalpages": 0}
    post = MagicMock(return_value=fake_response)
    monkeypatch.setattr(crawler.session, "post", post)

    result = crawler._fetch_page(
        page_num=2,
        code="600276",
        name="恒瑞医药",
        date_range="2024-04-20~2024-10-17",
    )

    assert result == {"announcements": [], "totalpages": 0}
    call = post.call_args
    assert call.args[0] == inquiry_module.CNINFO_SEARCH_URL
    assert call.kwargs["data"]["pageNum"] == "2"
    assert call.kwargs["data"]["searchkey"] == "恒瑞医药"
    assert call.kwargs["data"]["stock"] == ""
    assert call.kwargs["data"]["category"] == ""
    assert call.kwargs["data"]["seDate"] == "2024-04-20~2024-10-17"


def test_fetch_page_does_not_send_bare_stock_code(crawler: InquiryCrawler, monkeypatch) -> None:
    """CNINFO frontend expects blank stock or code,orgId; bare code returns empty results."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.raise_for_status = MagicMock()
    fake_response.json.return_value = {"announcements": [], "totalpages": 0}
    post = MagicMock(return_value=fake_response)
    monkeypatch.setattr(crawler.session, "post", post)

    crawler._fetch_page(
        page_num=1,
        code="300760",
        name="迈瑞医疗",
        date_range="2024-04-20~2024-10-17",
    )

    assert post.call_args.kwargs["data"]["stock"] != "300760"


def test_run_resumes_from_discovery_cache_without_duplicate_candidates(
    crawler: InquiryCrawler,
    monkeypatch,
) -> None:
    """已完成的 annual_doc_id 应跳过，已有候选不应重复写入。"""
    crawler.limit = None
    write_annual_metadata(
        crawler.annual_metadata_path,
        [
            annual_metadata_row("600276", "恒瑞医药", "2024-04-20"),
            annual_metadata_row("300760", "迈瑞医疗", "2024-04-18"),
        ],
    )
    crawler.cache_path.write_text('["600276_恒瑞医药_2023年报"]', encoding="utf-8")
    write_candidates(
        crawler.candidates_path,
        [
            make_candidate_record(
                annual_doc_id="600276_恒瑞医药_2023年报",
                code="600276",
                name="恒瑞医药",
                announcement_id="1219999999",
                title="关于恒瑞医药2023年年报的问询函",
            )
        ],
    )

    calls: list[str] = []

    def fake_search(annual_record: dict[str, str], report_year: str) -> list[dict[str, str]]:
        calls.append(annual_record["doc_id"])
        return [
            make_candidate("300760", "迈瑞医疗", "1220000000", "关于迈瑞医疗2023年年报的问询函")
        ]

    monkeypatch.setattr(crawler, "_search_for_annual_record", fake_search)
    monkeypatch.setattr(inquiry_module.time, "sleep", lambda _seconds: None)

    crawler.run()

    rows = list(csv.DictReader(crawler.candidates_path.open("r", encoding="utf-8", newline="")))
    assert calls == ["300760_迈瑞医疗_2023年报"]
    assert [row["announcement_id"] for row in rows] == ["1219999999", "1220000000"]
    assert set(crawler.cache_path.read_text(encoding="utf-8").split('"')) >= {
        "600276_恒瑞医药_2023年报",
        "300760_迈瑞医疗_2023年报",
    }


def test_run_force_rebuilds_candidates_and_cache(
    crawler: InquiryCrawler,
    monkeypatch,
) -> None:
    """force=True 应忽略旧 cache，并重建候选 CSV。"""
    write_annual_metadata(
        crawler.annual_metadata_path,
        [annual_metadata_row("600276", "恒瑞医药", "2024-04-20")],
    )
    crawler.cache_path.write_text('["600276_恒瑞医药_2023年报"]', encoding="utf-8")
    write_candidates(
        crawler.candidates_path,
        [
            make_candidate_record(
                annual_doc_id="old",
                code="000000",
                name="旧数据",
                announcement_id="old-id",
                title="旧问询函",
            )
        ],
    )

    monkeypatch.setattr(
        crawler,
        "_search_for_annual_record",
        lambda _record, _year: [
            make_candidate("600276", "恒瑞医药", "1219999999", "关于恒瑞医药2023年年报的问询函")
        ],
    )
    monkeypatch.setattr(inquiry_module.time, "sleep", lambda _seconds: None)

    crawler.run(force=True)

    rows = list(csv.DictReader(crawler.candidates_path.open("r", encoding="utf-8", newline="")))
    assert [row["announcement_id"] for row in rows] == ["1219999999"]
    assert "old-id" not in crawler.candidates_path.read_text(encoding="utf-8")
    assert "600276_恒瑞医药_2023年报" in crawler.cache_path.read_text(encoding="utf-8")


def test_run_migrates_existing_candidate_schema(
    crawler: InquiryCrawler,
    monkeypatch,
) -> None:
    """旧 inquiry_candidates.csv 缺少新列时，应先补齐 schema 再续写。"""
    crawler.limit = None
    write_annual_metadata(
        crawler.annual_metadata_path,
        [annual_metadata_row("600276", "恒瑞医药", "2024-04-20")],
    )
    crawler.candidates_path.write_text(
        "annual_doc_id,doc_id,stock_code,pdf_url,local_pdf_path,download_status\n"
        "old,old_doc,600276,http://static.cninfo.com.cn/old.pdf,data/inquiry/pdf/old.pdf,success\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        crawler,
        "_search_for_annual_record",
        lambda _record, _year: [
            make_candidate("600276", "恒瑞医药", "1219999999", "关于恒瑞医药2023年年报的问询函")
        ],
    )
    monkeypatch.setattr(inquiry_module.time, "sleep", lambda _seconds: None)

    crawler.run()

    with crawler.candidates_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert reader.fieldnames == INQUIRY_METADATA_COLUMNS
    assert len(rows) == 2
    assert rows[0]["document_role"] == ""
    assert rows[1]["document_role"] == "inquiry_notice"


def test_extract_title_from_pdf_text_uses_first_heading_block() -> None:
    """PDF 首页文字层应能抽出公告大标题。"""
    text = """
证券简称：通策医疗    证券代码：600763    编号：临 2022-045

               通策医疗股份有限公司
        关于对上海证券交易所问询函回复的公告

本公司董事会及全体董事保证本公告内容不存在任何虚假记载。
"""
    assert extract_title_from_pdf_text(text) == "通策医疗股份有限公司 关于对上海证券交易所问询函回复的公告"
    assert extract_title_from_pdf_text("\n \n") == ""


def test_audit_inquiry_pdf_titles_writes_title_status(
    tmp_path: Path,
) -> None:
    """下载后标题校验应回写 pdf_title、pdf_title_status 和 title_match_status。"""
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    local_pdf = tmp_path / "data" / "inquiry" / "pdf" / "600763_2024-05-20_testhash.pdf"
    local_pdf.parent.mkdir(parents=True)
    local_pdf.write_bytes(b"%PDF-1.7\n")
    write_candidates(
        candidates_path,
        [
            make_candidate_record(
                annual_doc_id="600763_通策医疗_2021年报",
                code="600763",
                name="通策医疗",
                announcement_id="1219999999",
                title="通策医疗股份有限公司关于回复上海证券交易所问询函的公告",
            )
        ],
    )

    stats = audit_inquiry_pdf_titles(
        candidates_path=candidates_path,
        project_root=tmp_path,
        extractor=lambda _path: ("通策医疗股份有限公司 关于回复上海证券交易所问询函的公告", "ok"),
    )

    rows = list(csv.DictReader(candidates_path.open("r", encoding="utf-8", newline="")))
    assert stats == {"ok": 1, "empty": 0, "needs_ocr": 0, "missing": 0, "error": 0}
    assert rows[0]["pdf_title"] == "通策医疗股份有限公司 关于回复上海证券交易所问询函的公告"
    assert rows[0]["pdf_title_status"] == "ok"
    assert rows[0]["title_match_status"] == "match"


def test_title_match_status_accepts_stock_name_abbreviation() -> None:
    """公司简称和 PDF 法定全称不完全连续时，不应误报 mismatch。"""
    row = {
        "announcement_title": "独立董事关于2022年年度报告信息披露监管工作函的独立意见",
        "stock_name": "韦尔股份",
        "document_role": "regulatory_work_letter",
    }
    pdf_title = "上海韦尔半导体股份有限公司独立董事 关于2022年年度报告信息披露监管工作函回复的独立意见"

    assert title_match_status(row, pdf_title, "ok") == "match"


def test_audit_inquiry_pdf_titles_respects_limit(tmp_path: Path) -> None:
    """小样本下载后，标题审计不应污染 limit 之外的候选行。"""
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    pdf_dir = tmp_path / "data" / "inquiry" / "pdf"
    pdf_dir.mkdir(parents=True)
    first_pdf = pdf_dir / "first.pdf"
    first_pdf.write_bytes(b"%PDF-1.7\n")
    write_candidates(
        candidates_path,
        [
            {
                **make_candidate_record(
                    annual_doc_id="600763_通策医疗_2021年报",
                    code="600763",
                    name="通策医疗",
                    announcement_id="1219999999",
                    title="通策医疗股份有限公司关于回复上海证券交易所问询函的公告",
                ),
                "local_pdf_path": "data/inquiry/pdf/first.pdf",
            },
            {
                **make_candidate_record(
                    annual_doc_id="600763_通策医疗_2021年报",
                    code="600763",
                    name="通策医疗",
                    announcement_id="1220000000",
                    title="通策医疗股份有限公司关于收到上海证券交易所问询函的公告",
                ),
                "local_pdf_path": "data/inquiry/pdf/not_downloaded_yet.pdf",
            },
        ],
    )

    stats = audit_inquiry_pdf_titles(
        candidates_path=candidates_path,
        project_root=tmp_path,
        limit=1,
        extractor=lambda _path: ("通策医疗股份有限公司 关于回复上海证券交易所问询函的公告", "ok"),
    )

    rows = list(csv.DictReader(candidates_path.open("r", encoding="utf-8", newline="")))
    assert stats == {"ok": 1, "empty": 0, "needs_ocr": 0, "missing": 0, "error": 0}
    assert rows[0]["pdf_title_status"] == "ok"
    assert rows[1]["pdf_title"] == ""
    assert rows[1]["pdf_title_status"] == ""
    assert rows[1]["title_match_status"] == ""


def test_write_orphan_pdf_report_does_not_delete_files(tmp_path: Path) -> None:
    """orphan report 只报告未被候选表引用的 PDF，不删除任何文件。"""
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    pdf_dir = tmp_path / "data" / "inquiry" / "pdf"
    pdf_dir.mkdir(parents=True)
    referenced = pdf_dir / "referenced.pdf"
    orphan = pdf_dir / "orphan.pdf"
    referenced.write_bytes(b"%PDF-1.7\n")
    orphan.write_bytes(b"%PDF-1.7\n")
    write_candidates(
        candidates_path,
        [
            {
                **make_candidate_record(
                    annual_doc_id="600763_通策医疗_2021年报",
                    code="600763",
                    name="通策医疗",
                    announcement_id="1219999999",
                    title="通策医疗股份有限公司关于收到上海证券交易所问询函的公告",
                ),
                "local_pdf_path": "data/inquiry/pdf/referenced.pdf",
            }
        ],
    )
    report_path = tmp_path / "outputs" / "reports" / "inquiry_orphan_pdf_report.md"

    stats = write_orphan_pdf_report(candidates_path, pdf_dir, report_path, project_root=tmp_path)

    report = report_path.read_text(encoding="utf-8")
    assert stats == {"referenced": 1, "pdf_files": 2, "orphans": 1}
    assert "orphan.pdf" in report
    assert "referenced.pdf" not in report
    assert referenced.exists()
    assert orphan.exists()


def make_candidate(
    code: str,
    name: str,
    announcement_id: str,
    title: str,
) -> dict[str, str | int]:
    return {
        "secCode": code,
        "secName": name,
        "announcementId": announcement_id,
        "announcementTitle": title,
        "adjunctUrl": f"finalpage/2024-05-20/{announcement_id}.PDF",
        "announcementTime": 1716134400000,
    }


def annual_metadata_row(code: str, name: str, publish_date: str) -> dict[str, str]:
    return {
        "doc_id": f"{code}_{name}_2023年报",
        "stock_code": code,
        "stock_name": name,
        "market": "sh" if code.startswith("6") else "sz",
        "announcement_title": f"{name}：2023年年度报告",
        "announcement_type": "年度报告",
        "publish_date": publish_date,
        "url": "",
        "pdf_url": "",
        "local_pdf_path": "",
        "download_status": "success",
        "source": "cninfo_official_api",
        "crawl_time": "",
        "error_message": "",
        "notes": "",
    }


def make_candidate_record(
    annual_doc_id: str,
    code: str,
    name: str,
    announcement_id: str,
    title: str,
) -> dict[str, str]:
    return {
        "annual_doc_id": annual_doc_id,
        "report_year": "2023",
        "query_window_start": "2024-04-20",
        "query_window_end": "2024-10-17",
        "doc_id": f"{code}_2024-05-20_testhash",
        "stock_code": code,
        "stock_name": name,
        "market": "sh" if code.startswith("6") else "sz",
        "announcement_id": announcement_id,
        "announcement_title": title,
        "announcement_type": "inquiry",
        "publish_date": "2024-05-20",
        "url": f"http://www.cninfo.com.cn/new/disclosure/detail?stockCode={code}&announcementId={announcement_id}",
        "pdf_url": f"http://static.cninfo.com.cn/finalpage/2024-05-20/{announcement_id}.PDF",
        "local_pdf_path": f"data/inquiry/pdf/{code}_2024-05-20_testhash.pdf",
        "download_status": "pending",
        "source": "cninfo_frontend_inquiry",
        "crawl_time": "",
        "error_message": "",
        "notes": "",
    }


def write_annual_metadata(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_candidates(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=INQUIRY_METADATA_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
