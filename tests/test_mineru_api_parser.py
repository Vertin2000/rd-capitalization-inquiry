"""MinerU API parser tests."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
import requests

from src.parse.mineru_api_parser import (
    MinerUApiBatchParser,
    MinerUApiError,
    MinerUApiParser,
    split_page_ranges,
)


class FakeResponse:
    def __init__(
        self,
        *,
        status_code: int = 200,
        payload: dict | None = None,
        content: bytes = b"",
    ) -> None:
        self.status_code = status_code
        self._payload = payload or {}
        self.content = content
        self.text = json.dumps(self._payload, ensure_ascii=False)

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, zip_bytes: bytes = b"") -> None:
        self.zip_bytes = zip_bytes
        self.posts: list[tuple[str, dict, dict]] = []
        self.gets: list[tuple[str, dict | None]] = []
        self.task_counter = 0

    def post(self, url, headers=None, json=None, timeout=None):  # noqa: ANN001
        self.task_counter += 1
        task_id = f"task-{self.task_counter}"
        self.posts.append((url, headers or {}, json or {}))
        return FakeResponse(payload={"code": 0, "msg": "ok", "data": {"task_id": task_id}})

    def get(self, url, headers=None, timeout=None):  # noqa: ANN001
        self.gets.append((url, headers))
        if "/extract/task/" in url:
            task_id = url.rsplit("/", 1)[-1]
            return FakeResponse(
                payload={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "task_id": task_id,
                        "state": "done",
                        "full_zip_url": f"https://example.test/{task_id}.zip",
                        "err_msg": "",
                    },
                },
            )
        return FakeResponse(content=self.zip_bytes)


class FakeBatchSession:
    def __init__(self, zip_bytes: bytes = b"") -> None:
        self.zip_bytes = zip_bytes
        self.posts: list[tuple[str, dict, dict]] = []
        self.gets: list[tuple[str, dict | None]] = []
        self.batch_counter = 0
        self.posted_files: list[dict] = []

    def post(self, url, headers=None, json=None, timeout=None):  # noqa: ANN001
        self.batch_counter += 1
        self.posts.append((url, headers or {}, json or {}))
        self.posted_files = list((json or {}).get("files", []))
        return FakeResponse(
            payload={"code": 0, "msg": "ok", "data": {"batch_id": f"batch-{self.batch_counter}"}},
        )

    def get(self, url, headers=None, timeout=None):  # noqa: ANN001
        self.gets.append((url, headers))
        if "/extract-results/batch/" in url:
            return FakeResponse(
                payload={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "batch_id": url.rsplit("/", 1)[-1],
                        "extract_result": [
                            {
                                "data_id": file["data_id"],
                                "state": "done",
                                "full_zip_url": f"https://example.test/{file['data_id']}.zip",
                                "err_msg": "",
                            }
                            for file in self.posted_files
                        ],
                    },
                },
            )
        return FakeResponse(content=self.zip_bytes)


class SelectiveDownloadBatchSession(FakeBatchSession):
    def __init__(self, zip_bytes: bytes = b"", fail_url_fragment: str = "") -> None:
        super().__init__(zip_bytes=zip_bytes)
        self.fail_url_fragment = fail_url_fragment

    def get(self, url, headers=None, timeout=None):  # noqa: ANN001
        if self.fail_url_fragment and self.fail_url_fragment in url:
            raise requests.exceptions.SSLError("transient cdn failure")
        return super().get(url, headers=headers, timeout=timeout)


class RefreshingDownloadBatchSession(FakeBatchSession):
    def __init__(self, zip_bytes: bytes = b"", data_id: str = "") -> None:
        super().__init__(zip_bytes=zip_bytes)
        self.data_id = data_id

    def get(self, url, headers=None, timeout=None):  # noqa: ANN001
        self.gets.append((url, headers))
        if "old.zip" in url:
            raise requests.exceptions.SSLError("expired cdn url")
        if "/extract-results/batch/" in url:
            return FakeResponse(
                payload={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "batch_id": url.rsplit("/", 1)[-1],
                        "extract_result": [
                            {
                                "data_id": self.data_id,
                                "state": "done",
                                "full_zip_url": "https://example.test/new.zip",
                                "err_msg": "",
                            }
                        ],
                    },
                },
            )
        return FakeResponse(content=self.zip_bytes)


class DelayedSecondBatchSession(FakeBatchSession):
    def __init__(self, zip_bytes: bytes = b"") -> None:
        super().__init__(zip_bytes=zip_bytes)
        self.files_by_batch: dict[str, list[dict]] = {}
        self.batch_query_counts: dict[str, int] = {}
        self.events: list[str] = []

    def post(self, url, headers=None, json=None, timeout=None):  # noqa: ANN001
        self.batch_counter += 1
        batch_id = f"batch-{self.batch_counter}"
        files = list((json or {}).get("files", []))
        self.posts.append((url, headers or {}, json or {}))
        self.posted_files = files
        self.files_by_batch[batch_id] = files
        return FakeResponse(payload={"code": 0, "msg": "ok", "data": {"batch_id": batch_id}})

    def get(self, url, headers=None, timeout=None):  # noqa: ANN001
        self.gets.append((url, headers))
        if "/extract-results/batch/" in url:
            batch_id = url.rsplit("/", 1)[-1]
            count = self.batch_query_counts.get(batch_id, 0) + 1
            self.batch_query_counts[batch_id] = count
            state = "done"
            if batch_id == "batch-2" and count == 1:
                state = "running"
            self.events.append(f"query:{batch_id}:{state}")
            return FakeResponse(
                payload={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "batch_id": batch_id,
                        "extract_result": [
                            {
                                "data_id": file["data_id"],
                                "state": state,
                                "full_zip_url": f"https://example.test/{file['data_id']}.zip"
                                if state == "done"
                                else "",
                                "err_msg": "",
                            }
                            for file in self.files_by_batch.get(batch_id, [])
                        ],
                    },
                },
            )
        self.events.append(f"download:{url.rsplit('/', 1)[-1]}")
        return FakeResponse(content=self.zip_bytes)


def make_zip(full_md: str) -> bytes:
    zip_path = Path(__file__).parent / "__tmp_mineru_result.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("full.md", full_md)
    data = zip_path.read_bytes()
    zip_path.unlink()
    return data


def make_parser(tmp_path: Path, session: FakeSession) -> MinerUApiParser:
    metadata_dir = tmp_path / "data" / "metadata"
    pdf_dir = tmp_path / "data" / "pdf"
    parsed_dir = tmp_path / "data" / "parsed"
    metadata_dir.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)
    parsed_dir.mkdir(parents=True)
    (metadata_dir / "metadata.csv").write_text(
        "doc_id,pdf_url,local_pdf_path,download_status\n"
        "doc347,https://static.cninfo.com.cn/doc347.pdf,data/pdf/doc347.pdf,success\n",
        encoding="utf-8",
    )
    (pdf_dir / "doc347.pdf").write_bytes(b"%PDF-1.7")
    return MinerUApiParser(
        metadata_path=str(metadata_dir / "metadata.csv"),
        pdf_dir=str(pdf_dir),
        output_dir=str(parsed_dir),
        task_log_path=str(parsed_dir / "mineru_api_tasks.jsonl"),
        raw_dir=str(parsed_dir / "mineru_api_raw"),
        api_key="test-token",
        session=session,
        poll_interval=0,
    )


def make_batch_parser(tmp_path: Path, session: FakeBatchSession) -> MinerUApiBatchParser:
    metadata_dir = tmp_path / "data" / "metadata"
    pdf_dir = tmp_path / "data" / "pdf"
    parsed_dir = tmp_path / "data" / "parsed"
    metadata_dir.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)
    parsed_dir.mkdir(parents=True)
    (metadata_dir / "metadata.csv").write_text(
        "doc_id,pdf_url,local_pdf_path,download_status\n"
        "doc347,https://static.cninfo.com.cn/doc347.pdf,data/pdf/doc347.pdf,success\n",
        encoding="utf-8",
    )
    (pdf_dir / "doc347.pdf").write_bytes(b"%PDF-1.7")
    return MinerUApiBatchParser(
        metadata_path=str(metadata_dir / "metadata.csv"),
        pdf_dir=str(pdf_dir),
        output_dir=str(parsed_dir),
        task_log_path=str(parsed_dir / "mineru_api_tasks.jsonl"),
        raw_dir=str(parsed_dir / "mineru_api_raw"),
        api_key="test-token",
        session=session,
        poll_interval=0,
        batch_size=10,
    )


def make_multi_doc_batch_parser(
    tmp_path: Path,
    session: FakeBatchSession,
    doc_ids: list[str] | None = None,
) -> MinerUApiBatchParser:
    doc_ids = doc_ids or ["docA", "docB"]
    metadata_dir = tmp_path / "data" / "metadata"
    pdf_dir = tmp_path / "data" / "pdf"
    parsed_dir = tmp_path / "data" / "parsed"
    metadata_dir.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)
    parsed_dir.mkdir(parents=True)
    metadata_lines = ["doc_id,pdf_url,local_pdf_path,download_status"]
    for doc_id in doc_ids:
        metadata_lines.append(
            f"{doc_id},https://static.cninfo.com.cn/{doc_id}.pdf,data/pdf/{doc_id}.pdf,success"
        )
        (pdf_dir / f"{doc_id}.pdf").write_bytes(b"%PDF-1.7")
    (metadata_dir / "metadata.csv").write_text("\n".join(metadata_lines) + "\n", encoding="utf-8")

    return MinerUApiBatchParser(
        metadata_path=str(metadata_dir / "metadata.csv"),
        pdf_dir=str(pdf_dir),
        output_dir=str(parsed_dir),
        task_log_path=str(parsed_dir / "mineru_api_tasks.jsonl"),
        raw_dir=str(parsed_dir / "mineru_api_raw"),
        api_key="test-token",
        session=session,
        poll_interval=0,
        batch_size=10,
        download_max_retries=1,
    )


def test_split_page_ranges_splits_at_200_pages() -> None:
    assert split_page_ranges(150) == ["1-150"]
    assert split_page_ranges(200) == ["1-200"]
    assert split_page_ranges(347) == ["1-200", "201-347"]
    assert split_page_ranges(374) == ["1-200", "201-374"]


def test_api_batch_parser_uses_aggressive_defaults_and_worker_env(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("MINERU_API_BATCH_SIZE", raising=False)
    monkeypatch.setenv("MINERU_API_DOWNLOAD_WORKERS", "6")
    monkeypatch.setenv("MINERU_API_EXTRACT_WORKERS", "3")
    metadata_dir = tmp_path / "data" / "metadata"
    pdf_dir = tmp_path / "data" / "pdf"
    parsed_dir = tmp_path / "data" / "parsed"
    metadata_dir.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)

    parser = MinerUApiBatchParser(
        metadata_path=str(metadata_dir / "metadata.csv"),
        pdf_dir=str(pdf_dir),
        output_dir=str(parsed_dir),
        api_key="test-token",
        session=FakeBatchSession(),
    )

    assert parser.batch_size == 50
    assert parser.download_workers == 6
    assert parser.extract_workers == 3


def test_build_task_payload_uses_precise_api_defaults(tmp_path: Path) -> None:
    session = FakeSession()
    parser = make_parser(tmp_path, session)

    payload = parser.build_task_payload(
        pdf_url="https://static.cninfo.com.cn/doc347.pdf",
        doc_id="doc347",
        part_index=1,
        page_range="1-200",
    )

    assert payload["url"] == "https://static.cninfo.com.cn/doc347.pdf"
    assert payload["page_ranges"] == "1-200"
    assert payload["model_version"] == "pipeline"
    assert payload["enable_table"] is True
    assert payload["enable_formula"] is False
    assert payload["is_ocr"] is False
    assert payload["language"] == "ch"
    assert payload["data_id"] == "doc347_part1"


def test_create_task_url_can_be_overridden_by_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("MINERU_API_URL", "https://example.test/custom/task")
    session = FakeSession()
    parser = make_parser(tmp_path, session)

    parser.submit_task(
        parser.build_task_payload(
            pdf_url="https://static.cninfo.com.cn/doc347.pdf",
            doc_id="doc347",
            part_index=1,
            page_range="1-200",
        )
    )

    assert session.posts[0][0] == "https://example.test/custom/task"


def test_poll_task_returns_done_and_raises_failed(tmp_path: Path) -> None:
    class PollSession(FakeSession):
        def __init__(self) -> None:
            super().__init__()
            self.states = ["pending", "running", "done"]

        def get(self, url, headers=None, timeout=None):  # noqa: ANN001
            state = self.states.pop(0)
            return FakeResponse(
                payload={
                    "code": 0,
                    "data": {
                        "task_id": "task-1",
                        "state": state,
                        "full_zip_url": "https://example.test/result.zip",
                        "err_msg": "",
                    },
                    "msg": "ok",
                },
            )

    parser = make_parser(tmp_path, PollSession())
    result = parser.poll_task("task-1")

    assert result["state"] == "done"
    assert result["full_zip_url"] == "https://example.test/result.zip"

    class FailedSession(FakeSession):
        def get(self, url, headers=None, timeout=None):  # noqa: ANN001
            return FakeResponse(
                payload={
                    "code": 0,
                    "data": {"task_id": "task-2", "state": "failed", "err_msg": "bad file"},
                    "msg": "ok",
                },
            )

    parser = make_parser(tmp_path / "failed", FailedSession())
    with pytest.raises(MinerUApiError, match="bad file"):
        parser.poll_task("task-2")


def test_parse_one_pdf_downloads_segments_and_merges_markdown(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeSession(zip_bytes=make_zip("# segment\ncontent\n"))
    parser = make_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 347)

    stats = parser.run(limit=1)
    output_md = parser.output_dir / "doc347.md"
    records = [
        json.loads(line)
        for line in parser.task_log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert output_md.read_text(encoding="utf-8").count("# segment") == 2
    assert [post[2]["page_ranges"] for post in session.posts] == ["1-200", "201-347"]
    assert [record["status"] for record in records].count("success") == 2
    assert records[-1]["doc_id"] == "doc347"
    assert records[-1]["page_range"] == "201-347"


def test_parse_reuses_successful_segment_raw_markdown(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeSession(zip_bytes=make_zip("# second\n"))
    parser = make_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 347)
    part_dir = parser.raw_dir / "doc347" / "part_01" / "extracted"
    part_dir.mkdir(parents=True)
    (part_dir / "full.md").write_text("# first cached\n", encoding="utf-8")
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-200",
                "task_id": "old-task",
                "status": "success",
                "full_zip_url": "https://example.test/old.zip",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)
    output_md = parser.output_dir / "doc347.md"

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert output_md.read_text(encoding="utf-8").count("# first cached") == 1
    assert output_md.read_text(encoding="utf-8").count("# second") == 1
    assert [post[2]["page_ranges"] for post in session.posts] == ["201-347"]


def test_parse_resumes_submitted_segment_without_resubmitting(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeSession(zip_bytes=make_zip("# first resumed\n"))
    parser = make_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-150",
                "task_id": "existing-task",
                "status": "submitted",
                "full_zip_url": "",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)
    output_md = parser.output_dir / "doc347.md"

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert "# first resumed" in output_md.read_text(encoding="utf-8")
    assert session.posts == []
    assert any("/existing-task" in url for url, _headers in session.gets)


def test_download_full_markdown_retries_transient_ssl_error(tmp_path: Path) -> None:
    class FlakyZipSession(FakeSession):
        def __init__(self) -> None:
            super().__init__(zip_bytes=make_zip("# recovered\n"))
            self.download_attempts = 0

        def get(self, url, headers=None, timeout=None):  # noqa: ANN001
            if url == "https://example.test/result.zip":
                self.download_attempts += 1
                if self.download_attempts == 1:
                    raise requests.exceptions.SSLError("transient eof")
            return super().get(url, headers=headers, timeout=timeout)

    session = FlakyZipSession()
    parser = make_parser(tmp_path, session)

    full_md = parser.download_full_markdown(
        full_zip_url="https://example.test/result.zip",
        doc_id="doc347",
        part_index=1,
    )

    assert full_md == "# recovered\n"
    assert session.download_attempts == 2


def test_poll_task_logs_running_progress(tmp_path: Path, caplog) -> None:
    class ProgressSession(FakeSession):
        def __init__(self) -> None:
            super().__init__()
            self.responses = [
                {"state": "running", "extract_progress": {"extracted_pages": 50, "total_pages": 200}},
                {"state": "done", "full_zip_url": "https://example.test/result.zip"},
            ]

        def get(self, url, headers=None, timeout=None):  # noqa: ANN001
            data = self.responses.pop(0)
            return FakeResponse(
                payload={
                    "code": 0,
                    "data": {"task_id": "task-1", "err_msg": "", **data},
                    "msg": "ok",
                },
            )

    parser = make_parser(tmp_path, ProgressSession())
    caplog.set_level("INFO")

    parser.poll_task("task-1", doc_id="doc347", page_range="1-200")
    messages = "\n".join(record.getMessage() for record in caplog.records)

    assert "task-1" in messages
    assert "running" in messages
    assert "50/200" in messages


def test_missing_api_key_fails_clearly(tmp_path: Path) -> None:
    parser = MinerUApiParser(
        metadata_path=str(tmp_path / "missing.csv"),
        pdf_dir=str(tmp_path),
        output_dir=str(tmp_path / "parsed"),
        api_key="",
    )

    with pytest.raises(MinerUApiError, match="MINERU_API_KEY"):
        parser.run(limit=1)


def test_batch_file_payload_uses_url_batch_shape(tmp_path: Path) -> None:
    parser = make_batch_parser(tmp_path, FakeBatchSession())

    file_payload = parser.build_batch_file_payload(
        pdf_url="https://static.cninfo.com.cn/doc347.pdf",
        doc_id="doc347",
        part_index=2,
        page_range="201-347",
    )

    assert file_payload["url"] == "https://static.cninfo.com.cn/doc347.pdf"
    assert file_payload["page_ranges"] == "201-347"
    assert file_payload["is_ocr"] is False
    assert file_payload["data_id"].startswith("p2_")
    assert len(file_payload["data_id"]) <= 128


def test_api_batch_parser_submits_batch_and_merges_segments(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# batch segment\n"))
    parser = make_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 347)

    stats = parser.run(limit=1)
    output_md = parser.output_dir / "doc347.md"
    records = [
        json.loads(line)
        for line in parser.task_log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert output_md.read_text(encoding="utf-8").count("# batch segment") == 2
    assert session.posts[0][0] == "https://mineru.net/api/v4/extract/task/batch"
    assert session.posts[0][2]["model_version"] == "pipeline"
    assert [file["page_ranges"] for file in session.posts[0][2]["files"]] == ["1-200", "201-347"]
    assert [record["status"] for record in records].count("submitted") == 2
    assert [record["status"] for record in records].count("success") == 2


def test_api_batch_parser_downloads_all_zips_before_extracting(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# batch segment\n"))
    parser = make_multi_doc_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)

    stats = parser.run(limit=2)
    records = [
        json.loads(line)
        for line in parser.task_log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    statuses = [record["status"] for record in records]

    assert stats == {"total": 2, "success": 2, "failed": 0}
    assert statuses.count("zip_downloaded") == 2
    assert statuses.count("success") == 2
    assert max(index for index, status in enumerate(statuses) if status == "zip_downloaded") < min(
        index for index, status in enumerate(statuses) if status == "success"
    )
    assert (parser.output_dir / "docA.md").exists()
    assert (parser.output_dir / "docB.md").exists()


def test_api_batch_parser_downloads_ready_segments_before_all_batches_finish(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = DelayedSecondBatchSession(zip_bytes=make_zip("# streamed batch\n"))
    parser = make_multi_doc_batch_parser(tmp_path, session)
    parser.batch_size = 1
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)

    stats = parser.run(limit=2)

    assert stats == {"total": 2, "success": 2, "failed": 0}
    first_download_index = next(
        index for index, event in enumerate(session.events) if event.startswith("download:")
    )
    second_batch_done_index = session.events.index("query:batch-2:done")
    assert first_download_index < second_batch_done_index


def test_api_batch_parser_extracts_existing_result_zip_without_downloading(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# should not download\n"))
    parser = make_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    zip_path = parser.raw_dir / "doc347" / "part_01" / "result.zip"
    zip_path.parent.mkdir(parents=True)
    zip_path.write_bytes(make_zip("# cached zip\n"))
    data_id = parser.build_batch_file_payload(
        pdf_url="https://static.cninfo.com.cn/doc347.pdf",
        doc_id="doc347",
        part_index=1,
        page_range="1-150",
    )["data_id"]
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-150",
                "task_id": "batch-ready",
                "batch_id": "batch-ready",
                "data_id": data_id,
                "status": "ready",
                "full_zip_url": "https://example.test/cached.zip",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert "# cached zip" in (parser.output_dir / "doc347.md").read_text(encoding="utf-8")
    assert session.posts == []
    assert not any("cached.zip" in url for url, _headers in session.gets)


def test_api_batch_parser_keeps_merging_other_docs_when_one_download_fails(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = SelectiveDownloadBatchSession(zip_bytes=make_zip("# good doc\n"))
    parser = make_multi_doc_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    session.fail_url_fragment = parser._make_data_id("docB", 1, "1-150")

    stats = parser.run(limit=2)
    records = [
        json.loads(line)
        for line in parser.task_log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert stats == {"total": 2, "success": 1, "failed": 1}
    assert (parser.output_dir / "docA.md").exists()
    assert not (parser.output_dir / "docB.md").exists()
    assert any(
        record["doc_id"] == "docB" and record["status"] == "download_failed"
        for record in records
    )


def test_api_batch_parser_reuses_successful_segment_raw_markdown(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# second batch\n"))
    parser = make_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 347)
    part_dir = parser.raw_dir / "doc347" / "part_01" / "extracted"
    part_dir.mkdir(parents=True)
    (part_dir / "full.md").write_text("# first cached\n", encoding="utf-8")
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-200",
                "task_id": "batch-old",
                "batch_id": "batch-old",
                "data_id": "p2_old_1",
                "status": "success",
                "full_zip_url": "https://example.test/old.zip",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)
    output_text = (parser.output_dir / "doc347.md").read_text(encoding="utf-8")

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert "# first cached" in output_text
    assert "# second batch" in output_text
    assert [file["page_ranges"] for file in session.posts[0][2]["files"]] == ["201-347"]


def test_api_batch_parser_resumes_submitted_batch_without_resubmitting(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# resumed batch\n"))
    parser = make_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    file_payload = parser.build_batch_file_payload(
        pdf_url="https://static.cninfo.com.cn/doc347.pdf",
        doc_id="doc347",
        part_index=1,
        page_range="1-150",
    )
    session.posted_files = [file_payload]
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-150",
                "task_id": "batch-existing",
                "batch_id": "batch-existing",
                "data_id": file_payload["data_id"],
                "status": "submitted",
                "full_zip_url": "",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert session.posts == []
    assert any("/batch-existing" in url for url, _headers in session.gets)
    assert "# resumed batch" in (parser.output_dir / "doc347.md").read_text(encoding="utf-8")


def test_api_batch_parser_retries_failed_download_record_without_resubmitting(
    tmp_path: Path,
    monkeypatch,
) -> None:
    session = FakeBatchSession(zip_bytes=make_zip("# retry download\n"))
    parser = make_batch_parser(tmp_path, session)
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    data_id = parser.build_batch_file_payload(
        pdf_url="https://static.cninfo.com.cn/doc347.pdf",
        doc_id="doc347",
        part_index=1,
        page_range="1-150",
    )["data_id"]
    session.posted_files = [{"data_id": data_id}]
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-150",
                "task_id": "batch-existing",
                "batch_id": "batch-existing",
                "data_id": data_id,
                "status": "download_failed",
                "full_zip_url": "https://example.test/old.zip",
                "error": "transient ssl",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert session.posts == []
    assert any("old.zip" in url for url, _headers in session.gets)
    assert "# retry download" in (parser.output_dir / "doc347.md").read_text(encoding="utf-8")


def test_api_batch_parser_refreshes_expired_ready_zip_url(
    tmp_path: Path,
    monkeypatch,
) -> None:
    data_id = MinerUApiBatchParser._make_data_id("doc347", 1, "1-150")
    session = RefreshingDownloadBatchSession(
        zip_bytes=make_zip("# refreshed download\n"),
        data_id=data_id,
    )
    parser = make_batch_parser(tmp_path, session)
    parser.download_max_retries = 1
    monkeypatch.setattr("src.parse.mineru_api_parser.get_pdf_page_count", lambda _path: 150)
    parser.task_log_path.write_text(
        json.dumps(
            {
                "doc_id": "doc347",
                "part_index": 1,
                "page_range": "1-150",
                "task_id": "batch-existing",
                "batch_id": "batch-existing",
                "data_id": data_id,
                "status": "ready",
                "full_zip_url": "https://example.test/old.zip",
                "error": "",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    stats = parser.run(limit=1)

    assert stats == {"total": 1, "success": 1, "failed": 0}
    assert session.posts == []
    requested_urls = [url for url, _headers in session.gets]
    assert "https://example.test/old.zip" in requested_urls
    assert any("/batch-existing" in url for url in requested_urls)
    assert "https://example.test/new.zip" in requested_urls
    assert "# refreshed download" in (parser.output_dir / "doc347.md").read_text(
        encoding="utf-8"
    )
