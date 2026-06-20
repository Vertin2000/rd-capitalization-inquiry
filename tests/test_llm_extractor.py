"""Tests for LLM extraction orchestration."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
import threading
import time

import src.extract.llm_client as llm_client_module
from src.extract.llm_client import LLMClient
from src.extract.llm_extractor import LLMExtractor
from src.model.schemas import SectionSlice


def write_sections(path: Path, doc_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    section = SectionSlice(
        doc_id=doc_id,
        section_name="研发费用",
        matched_keyword="研发投入金额",
        text="研发投入金额 100 万元；资本化的金额 20 万元；费用化的金额 80 万元。",
        line_start=1,
        line_end=2,
    )
    path.write_text(section.model_dump_json() + "\n", encoding="utf-8")


def write_metadata(path: Path, doc_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "doc_id": doc_id,
            "stock_code": "000001",
            "stock_name": "真实公司",
            "market": "sz",
            "announcement_title": "真实公司：2023年年度报告",
            "announcement_type": "年度报告",
            "publish_date": "2024-04-20",
            "url": "",
            "pdf_url": "",
            "local_pdf_path": "data/pdf/000001_真实公司_2023年报.pdf",
            "download_status": "success",
            "source": "cninfo_official_api",
            "crawl_time": "",
            "error_message": "",
            "notes": "",
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_extractor_uses_metadata_over_llm_identity_fields(tmp_path: Path) -> None:
    """metadata.csv should be authoritative for company identity and PDF path."""
    doc_id = "000001_真实公司_2023年报"
    sections_dir = tmp_path / "sections"
    metadata_path = tmp_path / "metadata.csv"
    write_sections(sections_dir / f"{doc_id}_sections.jsonl", doc_id)
    write_metadata(metadata_path, doc_id)

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
        metadata_path=str(metadata_path),
    )
    extractor.client.call_json = lambda _prompt: {
        "company_name": "幻觉公司",
        "company_code": "999999",
        "year": 2099,
        "rd_expense_total": {"value": 100.0, "evidence_text": "研发投入金额 100 万元"},
        "rd_capitalized_amount": {"value": 20.0, "evidence_text": "资本化的金额 20 万元"},
        "rd_expensed_amount": {"value": 80.0, "evidence_text": "费用化的金额 80 万元"},
        "capitalization_rate": {"value": 20.0, "evidence_text": "资本化率 20%"},
    }

    record = extractor.extract(doc_id)

    assert record is not None
    assert record["company_name"] == "真实公司"
    assert record["company_code"] == "000001"
    assert record["year"] == 2023
    assert record["source_pdf_path"] == "data/pdf/000001_真实公司_2023年报.pdf"
    assert record["capitalization_rate"]["value"] == 20.0


def test_extractor_skips_docs_without_sections(tmp_path: Path) -> None:
    """Docs without section JSONL should not produce malformed records."""
    extractor = LLMExtractor(
        sections_dir=str(tmp_path / "sections"),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )

    assert extractor.extract("missing_doc") is None
    assert not (tmp_path / "extracted" / "records.jsonl").exists()


def test_llm_client_loads_project_env_file(tmp_path: Path, monkeypatch) -> None:
    """LLMClient should load .env so shell-level env injection is not required."""
    env_path = tmp_path / ".env"
    env_path.write_text(
        "LLM_API_KEY=env-file-key\nLLM_BASE_URL=https://example.test/v1\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.setattr(llm_client_module, "PROJECT_ROOT", tmp_path)

    client = LLMClient()

    assert client.api_key == "env-file-key"
    assert client.base_url == "https://example.test/v1"


def test_llm_client_sends_configured_user_agent(monkeypatch) -> None:
    """Some providers gate coding endpoints by client User-Agent."""
    captured = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self):
            return {"choices": [{"message": {"content": "ok"}}]}

    def fake_post(api_url, json, headers, timeout):  # noqa: ANN001
        captured["api_url"] = api_url
        captured["headers"] = headers
        return FakeResponse()

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_BACKEND", "http")
    monkeypatch.setenv("LLM_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("LLM_USER_AGENT", "CodexPipeline/0.1")
    monkeypatch.setattr(llm_client_module.httpx, "post", fake_post)

    client = LLMClient()

    assert client.call("ping") == "ok"
    assert captured["headers"]["User-Agent"] == "CodexPipeline/0.1"


def test_llm_client_can_call_kimi_code_cli_backend(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Kimi Code CLI backend should use the local authenticated kimi binary."""
    captured = {}

    class FakeProcess:
        pid = 123
        returncode = 0

        def communicate(self, timeout=None):  # noqa: ANN001
            return "• ok\n\nTo resume this session: kimi -r session_123\n", ""

    def fake_popen(args, **kwargs):  # noqa: ANN001
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(llm_client_module, "PROJECT_ROOT", tmp_path)
    monkeypatch.setenv("LLM_BACKEND", "kimi_code_cli")
    monkeypatch.setenv("KIMI_CODE_CLI_COMMAND", "kimi")
    monkeypatch.setattr(llm_client_module.subprocess, "Popen", fake_popen)

    client = LLMClient()

    assert client.call("用户提示", system_prompt="系统提示") == "ok"
    assert captured["args"][:2] == ["kimi", "-p"]
    assert "系统提示" in captured["args"][2]
    assert "用户提示" in captured["args"][2]
    assert captured["kwargs"]["stdout"] is llm_client_module.subprocess.PIPE
    assert captured["kwargs"]["stderr"] is llm_client_module.subprocess.PIPE


def test_llm_client_call_json_extracts_first_json_from_cli_output(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Kimi CLI text output may include bullets and resume hints around JSON."""

    class FakeProcess:
        pid = 123
        returncode = 0

        def communicate(self, timeout=None):  # noqa: ANN001
            return (
                '• {"rd_expense_total":{"value":100},"company_code":"000001"}\n\n'
                "• The user asked for JSON only.\n\n"
                "To resume this session: kimi -r session_123\n"
            ), ""

    monkeypatch.setattr(llm_client_module, "PROJECT_ROOT", tmp_path)
    monkeypatch.setenv("LLM_BACKEND", "kimi_code_cli")
    monkeypatch.setattr(
        llm_client_module.subprocess,
        "Popen",
        lambda *args, **kwargs: FakeProcess(),
    )

    client = LLMClient()

    result = client.call_json("prompt")
    assert result["company_code"] == "000001"
    assert result["rd_expense_total"]["value"] == 100


def test_save_record_writes_utf8_jsonl(tmp_path: Path) -> None:
    """Saved extraction records should stay UTF-8 JSONL with Chinese text intact."""
    output_path = tmp_path / "records.jsonl"
    extractor = LLMExtractor(output_path=str(output_path))

    extractor._save_record({"doc_id": "doc", "company_name": "真实公司"})

    raw = output_path.read_text(encoding="utf-8")
    assert json.loads(raw)["company_name"] == "真实公司"


def test_build_prompt_caps_large_section_text(tmp_path: Path) -> None:
    """Huge Markdown tables should be capped before sending to the LLM."""
    extractor = LLMExtractor(output_path=str(tmp_path / "records.jsonl"))
    sections = [
        SectionSlice(
            doc_id="doc",
            section_name="研发费用",
            matched_keyword="研发投入",
            text="研发投入金额 " + ("很长的表格内容" * 5000),
            line_start=1,
            line_end=2,
            match_score=100,
        ),
        SectionSlice(
            doc_id="doc",
            section_name="开发支出",
            matched_keyword="开发支出",
            text="开发支出期初余额 " + ("很长的附注内容" * 5000),
            line_start=3,
            line_end=4,
            match_score=90,
        ),
    ]

    prompt = extractor._build_prompt(sections)

    assert "研发投入金额" in prompt
    assert "开发支出期初余额" in prompt
    assert len(prompt) < 22000


def test_kimi_code_cli_retries_rate_limit_once(tmp_path: Path, monkeypatch) -> None:
    """Transient Kimi Code CLI rate limits should be retried."""
    calls = []

    class FailedProcess:
        pid = 101
        returncode = 1

        def communicate(self, timeout=None):  # noqa: ANN001
            return "", "provider.rate_limit: 429"

    class SuccessfulProcess:
        pid = 102
        returncode = 0

        def communicate(self, timeout=None):  # noqa: ANN001
            return "• ok\n", ""

    def fake_popen(*args, **kwargs):  # noqa: ANN001
        calls.append((args, kwargs))
        return FailedProcess() if len(calls) == 1 else SuccessfulProcess()

    monkeypatch.setattr(llm_client_module, "PROJECT_ROOT", tmp_path)
    monkeypatch.setenv("LLM_BACKEND", "kimi_code_cli")
    monkeypatch.setenv("KIMI_CODE_CLI_RETRIES", "1")
    monkeypatch.setenv("KIMI_CODE_CLI_RETRY_DELAY", "0")
    monkeypatch.setattr(llm_client_module.subprocess, "Popen", fake_popen)

    client = LLMClient()

    assert client.call("ping") == "ok"
    assert len(calls) == 2


def test_prompt_includes_capitalization_rate_and_policy_guard(
    tmp_path: Path,
) -> None:
    """Prompt should encode project-specific capitalization-rate rules."""
    extractor = LLMExtractor(output_path=str(tmp_path / "records.jsonl"))
    section = SectionSlice(
        doc_id="doc",
        section_name="研发费用",
        matched_keyword="研发投入",
        text="资本化研发投入占研发投入的比例 9.61%",
        line_start=1,
        line_end=2,
    )

    prompt = extractor._build_prompt([section])

    assert "capitalization_rate" in prompt
    assert "禁止把开发支出期末余额直接当作本期资本化金额" in prompt


def test_extractor_run_supports_parallel_workers(tmp_path: Path) -> None:
    """Parallel extraction should save records from completed workers safely."""
    sections_dir = tmp_path / "sections"
    for doc_id in ["doc_a", "doc_b", "doc_c"]:
        write_sections(sections_dir / f"{doc_id}_sections.jsonl", doc_id)

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )

    def fake_extract(doc_id: str, extracted=None):  # noqa: ANN001
        return {"doc_id": doc_id, "company_name": f"公司{doc_id}"}

    extractor.extract = fake_extract  # type: ignore[method-assign]

    stats = extractor.run(workers=3)

    assert stats == {"total": 3, "success": 3, "failed": 0}
    lines = (tmp_path / "extracted" / "records.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    saved_doc_ids = {json.loads(line)["doc_id"] for line in lines}
    assert saved_doc_ids == {"doc_a", "doc_b", "doc_c"}


def test_extractor_run_logs_parallel_progress(
    tmp_path: Path,
    caplog,
) -> None:
    """Parallel extraction should log visible progress as futures finish."""
    sections_dir = tmp_path / "sections"
    for doc_id in ["doc_a", "doc_b"]:
        write_sections(sections_dir / f"{doc_id}_sections.jsonl", doc_id)

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )
    extractor.extract = lambda doc_id, extracted=None, raise_on_error=False: {  # type: ignore[method-assign] # noqa: E501
        "doc_id": doc_id
    }

    with caplog.at_level(logging.INFO):
        stats = extractor.run(workers=2)

    assert stats == {"total": 2, "success": 2, "failed": 0}
    assert "进度: done=1/2" in caplog.text
    assert "进度: done=2/2" in caplog.text


def test_extractor_run_fail_fast_terminates_active_client_processes(
    tmp_path: Path,
) -> None:
    """Fail-fast should stop on the first worker error and clean active clients."""
    sections_dir = tmp_path / "sections"
    for doc_id in ["doc_a", "doc_b", "doc_c"]:
        write_sections(sections_dir / f"{doc_id}_sections.jsonl", doc_id)

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )
    release_workers = threading.Event()
    terminated = []

    class FakeClient:
        backend = "http"

        def terminate_active_processes(self) -> None:
            terminated.append(True)
            release_workers.set()

    def fake_extract(doc_id: str, extracted=None, raise_on_error=False):  # noqa: ANN001
        if doc_id == "doc_a":
            raise RuntimeError("boom")
        release_workers.wait(timeout=1)
        return {"doc_id": doc_id}

    extractor.client = FakeClient()  # type: ignore[assignment]
    extractor.extract = fake_extract  # type: ignore[method-assign]

    started = time.monotonic()
    stats = extractor.run(workers=3, fail_fast=True)

    assert time.monotonic() - started < 0.5
    assert terminated == [True]
    assert stats["total"] == 3
    assert stats["failed"] > 0


def test_extractor_run_fail_fast_preflights_empty_sections(
    tmp_path: Path,
) -> None:
    """Fail-fast should stop before launching workers when a section file is empty."""
    sections_dir = tmp_path / "sections"
    write_sections(sections_dir / "doc_a_sections.jsonl", "doc_a")
    (sections_dir / "doc_b_sections.jsonl").write_text("", encoding="utf-8")
    calls = []

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )

    def fake_extract(doc_id: str, extracted=None, raise_on_error=False):  # noqa: ANN001
        calls.append(doc_id)
        return {"doc_id": doc_id}

    extractor.extract = fake_extract  # type: ignore[method-assign]

    stats = extractor.run(workers=149, fail_fast=True)

    assert calls == []
    assert stats == {"total": 2, "success": 0, "failed": 2}


def test_extractor_run_fail_fast_can_skip_empty_sections(
    tmp_path: Path,
) -> None:
    """Known empty sections can be skipped while fail-fast protects other docs."""
    sections_dir = tmp_path / "sections"
    write_sections(sections_dir / "doc_a_sections.jsonl", "doc_a")
    (sections_dir / "doc_b_sections.jsonl").write_text("", encoding="utf-8")
    calls = []

    extractor = LLMExtractor(
        sections_dir=str(sections_dir),
        output_path=str(tmp_path / "extracted" / "records.jsonl"),
    )

    def fake_extract(doc_id: str, extracted=None, raise_on_error=False):  # noqa: ANN001
        calls.append(doc_id)
        return {"doc_id": doc_id}

    extractor.extract = fake_extract  # type: ignore[method-assign]

    stats = extractor.run(workers=149, fail_fast=True, skip_empty_sections=True)

    assert calls == ["doc_a"]
    assert stats == {"total": 2, "success": 1, "failed": 1}
