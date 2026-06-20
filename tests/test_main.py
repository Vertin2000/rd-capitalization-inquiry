"""CLI stage dispatch tests."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import src.main as main


def test_run_parse_returns_nonzero_when_any_pdf_fails(monkeypatch) -> None:
    class FakeMinerUParser:
        def run(self, limit=None):  # noqa: ANN001
            assert limit == 1
            return {"total": 1, "success": 0, "failed": 1}

    fake_module = types.SimpleNamespace(MinerUParser=FakeMinerUParser)
    monkeypatch.setitem(sys.modules, "src.parse.mineru_parser", fake_module)

    assert main.run_parse(limit=1) == 1


def test_run_parse_returns_zero_when_all_pdfs_succeed(monkeypatch) -> None:
    class FakeMinerUParser:
        def run(self, limit=None):  # noqa: ANN001
            assert limit == 1
            return {"total": 1, "success": 1, "failed": 0}

    fake_module = types.SimpleNamespace(MinerUParser=FakeMinerUParser)
    monkeypatch.setitem(sys.modules, "src.parse.mineru_parser", fake_module)

    assert main.run_parse(limit=1) == 0


def test_run_parse_api_backend_invokes_api_parser(monkeypatch) -> None:
    calls = []

    class FakeMinerUApiParser:
        def run(self, limit=None):  # noqa: ANN001
            calls.append(("api", limit))
            return {"total": 1, "success": 1, "failed": 0}

    fake_module = types.SimpleNamespace(MinerUApiParser=FakeMinerUApiParser)
    monkeypatch.setitem(sys.modules, "src.parse.mineru_api_parser", fake_module)

    assert main.run_parse(limit=1, parse_backend="api") == 0
    assert calls == [("api", 1)]


def test_run_parse_api_batch_backend_invokes_batch_parser(monkeypatch) -> None:
    calls = []

    class FakeMinerUApiBatchParser:
        def run(self, limit=None):  # noqa: ANN001
            calls.append(("api-batch", limit))
            return {"total": 2, "success": 2, "failed": 0}

    fake_module = types.SimpleNamespace(MinerUApiBatchParser=FakeMinerUApiBatchParser)
    monkeypatch.setitem(sys.modules, "src.parse.mineru_api_parser", fake_module)

    assert main.run_parse(limit=2, parse_backend="api-batch") == 0
    assert calls == [("api-batch", 2)]


def test_run_stage_passes_parse_backend(monkeypatch) -> None:
    calls = []

    def fake_run_parse(limit=None, parse_backend="local"):  # noqa: ANN001
        calls.append((limit, parse_backend))
        return 0

    monkeypatch.setattr(main, "run_parse", fake_run_parse)

    assert main.run_stage("parse", limit=1, parse_backend="api") == 0
    assert calls == [(1, "api")]


def test_run_inquiry_invokes_crawler_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    calls = []
    candidate_path = tmp_path / "inquiry_candidates.csv"
    candidate_path.write_text(
        "doc_id,stock_code,pdf_url,local_pdf_path,download_status\n"
        "inq001,600276,http://static.cninfo.com.cn/a.pdf,data/inquiry/pdf/inq001.pdf,pending\n",
        encoding="utf-8",
    )

    class FakeInquiryCrawler:
        def __init__(self, limit=None):  # noqa: ANN001
            assert limit == 3

        def run(self, discover_only=True, force=False):  # noqa: ANN001
            assert discover_only is True
            assert force is False
            calls.append("crawl")
            return candidate_path

    class FailingPDFDownloader:
        def __init__(
            self,
            *args,
            **kwargs,
        ):  # noqa: ANN001
            raise AssertionError("inquiry discovery should not download PDFs")

    fake_inquiry_module = types.SimpleNamespace(InquiryCrawler=FakeInquiryCrawler)
    fake_download_module = types.SimpleNamespace(PDFDownloader=FailingPDFDownloader)
    monkeypatch.setitem(sys.modules, "src.crawl.inquiry_crawler", fake_inquiry_module)
    monkeypatch.setitem(sys.modules, "src.download.downloader", fake_download_module)

    assert main.run_inquiry(limit=3) == 0
    assert calls == ["crawl"]


def test_inquiry_stage_is_implemented() -> None:
    assert "inquiry" in main.IMPLEMENTED
    assert "inquiry-download" in main.IMPLEMENTED


def test_run_inquiry_skips_download_when_no_candidates(
    tmp_path: Path,
    monkeypatch,
) -> None:
    candidate_path = tmp_path / "inquiry_candidates.csv"
    candidate_path.write_text(
        "doc_id,stock_code,pdf_url,local_pdf_path,download_status\n",
        encoding="utf-8",
    )

    class FakeInquiryCrawler:
        def __init__(self, limit=None):  # noqa: ANN001
            assert limit is None

        def run(self, discover_only=True, force=False):  # noqa: ANN001
            assert discover_only is True
            assert force is False
            return candidate_path

    class FailingPDFDownloader:
        def __init__(self, *args, **kwargs):  # noqa: ANN001
            raise AssertionError("downloader should not run for empty candidates")

    fake_inquiry_module = types.SimpleNamespace(InquiryCrawler=FakeInquiryCrawler)
    fake_download_module = types.SimpleNamespace(PDFDownloader=FailingPDFDownloader)
    monkeypatch.setitem(sys.modules, "src.crawl.inquiry_crawler", fake_inquiry_module)
    monkeypatch.setitem(sys.modules, "src.download.downloader", fake_download_module)

    assert main.run_inquiry() == 0


def test_run_inquiry_download_invokes_downloader(tmp_path: Path, monkeypatch) -> None:
    calls = []
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    candidates_path.parent.mkdir(parents=True)
    candidates_path.write_text(
        "doc_id,stock_code,pdf_url,local_pdf_path,download_status\n"
        "inq001,600276,http://static.cninfo.com.cn/a.pdf,data/inquiry/pdf/inq001.pdf,pending\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(main, "PROJECT_ROOT", tmp_path)

    class FakePDFDownloader:
        def __init__(
            self,
            metadata_path,
            pdf_dir,
            log_path,
            limit=None,
            delay_seconds=3.0,
            max_retries=3,
        ):  # noqa: ANN001
            assert metadata_path == "data/inquiry/inquiry_candidates.csv"
            assert pdf_dir == "data/inquiry/pdf"
            assert log_path == "outputs/logs/inquiry_download_log.jsonl"
            assert limit == 3

        def run(self):  # noqa: ANN001
            calls.append("download")
            return {"success": 1, "failed": 0, "skipped": 0, "collision": 0}

    def fake_audit_inquiry_pdf_titles(candidates_path, project_root, limit=None):  # noqa: ANN001
        assert candidates_path == tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
        assert project_root == tmp_path
        assert limit == 3
        calls.append("title-audit")
        return {"ok": 1, "empty": 0, "needs_ocr": 0, "missing": 0, "error": 0}

    def fake_write_orphan_pdf_report(candidates_path, pdf_dir, report_path, *, project_root):  # noqa: ANN001
        assert candidates_path == tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
        assert pdf_dir == tmp_path / "data" / "inquiry" / "pdf"
        assert report_path == tmp_path / "outputs" / "reports" / "inquiry_orphan_pdf_report.md"
        assert project_root == tmp_path
        calls.append("orphan-report")
        return {"referenced": 1, "pdf_files": 1, "orphans": 0}

    fake_download_module = types.SimpleNamespace(PDFDownloader=FakePDFDownloader)
    fake_quality_module = types.SimpleNamespace(
        audit_inquiry_pdf_titles=fake_audit_inquiry_pdf_titles,
        write_orphan_pdf_report=fake_write_orphan_pdf_report,
    )
    monkeypatch.setitem(sys.modules, "src.download.downloader", fake_download_module)
    monkeypatch.setitem(sys.modules, "src.crawl.inquiry_quality", fake_quality_module)

    assert main.run_inquiry_download(limit=3) == 0
    assert calls == ["download", "title-audit", "orphan-report"]


def test_run_stage_passes_force_to_inquiry_download(monkeypatch) -> None:
    calls = []

    def fake_run_inquiry_download(limit=None, force=False):  # noqa: ANN001
        calls.append((limit, force))
        return 0

    monkeypatch.setattr(main, "run_inquiry_download", fake_run_inquiry_download)

    assert main.run_stage("inquiry-download", limit=10, force=True) == 0
    assert calls == [(10, True)]


def test_run_stage_passes_force_to_route(monkeypatch) -> None:
    calls = []

    def fake_run_route(limit=None, force=False):  # noqa: ANN001
        calls.append((limit, force))
        return 0

    monkeypatch.setattr(main, "run_route", fake_run_route)

    assert main.run_stage("route", limit=20, force=True) == 0
    assert calls == [(20, True)]


def test_run_extract_returns_nonzero_when_any_doc_fails(monkeypatch) -> None:
    class FakeLLMExtractor:
        def run(  # noqa: ANN001
            self,
            limit=None,
            workers=1,
            fail_fast=False,
            skip_empty_sections=False,
        ):
            assert limit == 5
            assert workers == 1
            assert fail_fast is False
            assert skip_empty_sections is False
            return {"total": 5, "success": 0, "failed": 5}

    fake_module = types.SimpleNamespace(LLMExtractor=FakeLLMExtractor)
    monkeypatch.setitem(sys.modules, "src.extract.llm_extractor", fake_module)

    assert main.run_extract(limit=5) == 1


def test_run_extract_passes_workers_to_extractor(monkeypatch) -> None:
    class FakeLLMExtractor:
        def run(  # noqa: ANN001
            self,
            limit=None,
            workers=1,
            fail_fast=False,
            skip_empty_sections=False,
        ):
            assert limit is None
            assert workers == 149
            assert fail_fast is False
            assert skip_empty_sections is False
            return {"total": 149, "success": 149, "failed": 0}

    fake_module = types.SimpleNamespace(LLMExtractor=FakeLLMExtractor)
    monkeypatch.setitem(sys.modules, "src.extract.llm_extractor", fake_module)

    assert main.run_extract(workers=149) == 0


def test_run_stage_passes_workers_to_extract(monkeypatch) -> None:
    calls = []

    def fake_run_extract(  # noqa: ANN001
        limit=None,
        workers=1,
        fail_fast=False,
        skip_empty_sections=False,
    ):
        calls.append((limit, workers, fail_fast, skip_empty_sections))
        return 0

    monkeypatch.setattr(main, "run_extract", fake_run_extract)

    assert main.run_stage("extract", limit=10, workers=149) == 0
    assert calls == [(10, 149, False, False)]


def test_run_extract_passes_fail_fast_to_extractor(monkeypatch) -> None:
    class FakeLLMExtractor:
        def run(  # noqa: ANN001
            self,
            limit=None,
            workers=1,
            fail_fast=False,
            skip_empty_sections=False,
        ):
            assert limit == 5
            assert workers == 149
            assert fail_fast is True
            assert skip_empty_sections is False
            return {"total": 5, "success": 0, "failed": 5}

    fake_module = types.SimpleNamespace(LLMExtractor=FakeLLMExtractor)
    monkeypatch.setitem(sys.modules, "src.extract.llm_extractor", fake_module)

    assert main.run_extract(limit=5, workers=149, fail_fast=True) == 1


def test_run_stage_passes_fail_fast_to_extract(monkeypatch) -> None:
    calls = []

    def fake_run_extract(  # noqa: ANN001
        limit=None,
        workers=1,
        fail_fast=False,
        skip_empty_sections=False,
    ):
        calls.append((limit, workers, fail_fast, skip_empty_sections))
        return 0

    monkeypatch.setattr(main, "run_extract", fake_run_extract)

    assert main.run_stage("extract", limit=10, workers=149, fail_fast=True) == 0
    assert calls == [(10, 149, True, False)]


def test_run_stage_passes_skip_empty_sections_to_extract(monkeypatch) -> None:
    calls = []

    def fake_run_extract(  # noqa: ANN001
        limit=None,
        workers=1,
        fail_fast=False,
        skip_empty_sections=False,
    ):
        calls.append((limit, workers, fail_fast, skip_empty_sections))
        return 0

    monkeypatch.setattr(main, "run_extract", fake_run_extract)

    assert (
        main.run_stage(
            "extract",
            limit=10,
            workers=149,
            fail_fast=True,
            skip_empty_sections=True,
        )
        == 0
    )
    assert calls == [(10, 149, True, True)]


def test_run_inquiry_download_returns_error_when_candidates_missing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(main, "PROJECT_ROOT", tmp_path)

    class FailingPDFDownloader:
        def __init__(self, *args, **kwargs):  # noqa: ANN001
            raise AssertionError("downloader should not run without candidates")

    fake_download_module = types.SimpleNamespace(PDFDownloader=FailingPDFDownloader)
    monkeypatch.setitem(sys.modules, "src.download.downloader", fake_download_module)

    assert main.run_inquiry_download() == 1


def test_run_stage_writes_run_log_on_success(tmp_path: Path, monkeypatch) -> None:
    """run_stage 成功时应向 run_log.jsonl 追加一行 status=success。"""
    monkeypatch.setattr(main, "PROJECT_ROOT", tmp_path)

    def fake_run_route(limit=None, force=False):  # noqa: ANN001
        return 0

    monkeypatch.setattr(main, "run_route", fake_run_route)
    assert main.run_stage("route") == 0

    log_path = tmp_path / "outputs" / "logs" / "run_log.jsonl"
    assert log_path.exists()
    import json

    lines = [json.loads(l) for l in log_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lines, "run_log 应至少一行"
    last = lines[-1]
    assert last["step"] == "route"
    assert last["status"] == "success"
    assert last["doc_id"] == "*"
    assert "time" in last and "elapsed" in last


def test_run_stage_logs_error_and_returns_nonzero_on_exception(
    tmp_path: Path, monkeypatch
) -> None:
    """阶段抛异常时 run_log 记 status=error 且返回 1，不静默。"""
    monkeypatch.setattr(main, "PROJECT_ROOT", tmp_path)

    def boom(limit=None, force=False):  # noqa: ANN001
        raise RuntimeError("boom")

    monkeypatch.setattr(main, "run_route", boom)
    assert main.run_stage("route") == 1

    import json

    log_path = tmp_path / "outputs" / "logs" / "run_log.jsonl"
    lines = [json.loads(l) for l in log_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    last = lines[-1]
    assert last["status"] == "error"
    assert "boom" in last["error"]


def test_run_stage_logs_failed_when_rc_nonzero(tmp_path: Path, monkeypatch) -> None:
    """阶段返回非零 rc 时记 status=failed。"""
    monkeypatch.setattr(main, "PROJECT_ROOT", tmp_path)

    def fake_run_route(limit=None, force=False):  # noqa: ANN001
        return 1

    monkeypatch.setattr(main, "run_route", fake_run_route)
    assert main.run_stage("route") == 1

    import json

    log_path = tmp_path / "outputs" / "logs" / "run_log.jsonl"
    lines = [json.loads(l) for l in log_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lines[-1]["status"] == "failed"
