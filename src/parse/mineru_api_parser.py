"""MinerU 精准解析 API backend.

通过 MinerU 官方精准解析 API 解析年报 PDF，输出仍保持
`data/parsed/{doc_id}.md`，以便下游 route/extract 阶段复用。
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import shutil
import time
import zipfile
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

CREATE_TASK_URL = "https://mineru.net/api/v4/extract/task"
QUERY_TASK_URL = "https://mineru.net/api/v4/extract/task/{task_id}"
CREATE_BATCH_TASK_URL = "https://mineru.net/api/v4/extract/task/batch"
QUERY_BATCH_TASK_URL = "https://mineru.net/api/v4/extract-results/batch/{batch_id}"
MAX_PAGES_PER_TASK = 200
DEFAULT_BATCH_SIZE = 50
DEFAULT_SUBMIT_FILE_LIMIT_PER_MINUTE = 50
DEFAULT_DOWNLOAD_WORKERS = 8
DEFAULT_EXTRACT_WORKERS = 4


class MinerUApiError(RuntimeError):
    """MinerU API parse failure."""


def split_page_ranges(total_pages: int, max_pages: int = MAX_PAGES_PER_TASK) -> list[str]:
    """Split a PDF page count into MinerU API page_ranges values."""
    if total_pages <= 0:
        raise ValueError("total_pages must be positive")

    ranges: list[str] = []
    start = 1
    while start <= total_pages:
        end = min(start + max_pages - 1, total_pages)
        ranges.append(f"{start}-{end}")
        start = end + 1
    return ranges


def get_pdf_page_count(pdf_path: Path) -> int:
    """Return PDF page count."""
    return len(PdfReader(str(pdf_path)).pages)


class MinerUApiParser:
    """Parse CNINFO annual report PDFs with MinerU precise API."""

    def __init__(
        self,
        metadata_path: str = "data/metadata/metadata.csv",
        pdf_dir: str = "data/pdf",
        output_dir: str = "data/parsed",
        task_log_path: str = "data/parsed/mineru_api_tasks.jsonl",
        raw_dir: str = "data/parsed/mineru_api_raw",
        api_key: str | None = None,
        session: requests.Session | None = None,
        poll_interval: float = 5.0,
        poll_timeout: float = 1800.0,
        model_version: str = "pipeline",
        download_max_retries: int | None = None,
        download_retry_delay: float | None = None,
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        load_dotenv(self.project_root / ".env")

        self.metadata_path = self._resolve_path(metadata_path)
        self.pdf_dir = self._resolve_path(pdf_dir)
        self.output_dir = self._resolve_path(output_dir)
        self.task_log_path = self._resolve_path(task_log_path)
        self.raw_dir = self._resolve_path(raw_dir)
        self.api_key = api_key if api_key is not None else os.getenv("MINERU_API_KEY", "")
        self.create_task_url = os.getenv("MINERU_API_URL", CREATE_TASK_URL)
        self.query_task_url = self._derive_query_task_url(self.create_task_url)
        self.session = session or requests.Session()
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout
        self.model_version = model_version
        self.download_max_retries = download_max_retries or int(
            os.getenv("MINERU_API_DOWNLOAD_RETRIES", "3")
        )
        self.download_retry_delay = (
            download_retry_delay
            if download_retry_delay is not None
            else float(os.getenv("MINERU_API_DOWNLOAD_RETRY_DELAY", "2.0"))
        )

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.task_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, path: str | Path) -> Path:
        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj
        return self.project_root / path_obj

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise MinerUApiError("MINERU_API_KEY 未设置，无法运行 MinerU API backend")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

    @staticmethod
    def _derive_query_task_url(create_task_url: str) -> str:
        """Derive task query URL from the create-task URL."""
        return create_task_url.rstrip("/") + "/{task_id}"

    def _load_metadata(self) -> dict[str, dict[str, str]]:
        if not self.metadata_path.exists():
            raise MinerUApiError(f"metadata.csv 不存在: {self.metadata_path}")

        with open(self.metadata_path, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        return {row["doc_id"]: row for row in rows if row.get("doc_id")}

    def build_task_payload(
        self,
        *,
        pdf_url: str,
        doc_id: str,
        part_index: int,
        page_range: str,
    ) -> dict[str, Any]:
        """Build MinerU precise API task payload for one page segment."""
        data_id = f"{doc_id}_part{part_index}"
        return {
            "url": pdf_url,
            "page_ranges": page_range,
            "model_version": self.model_version,
            "enable_table": True,
            "enable_formula": False,
            "is_ocr": False,
            "language": "ch",
            "data_id": data_id[:128],
        }

    def submit_task(self, payload: dict[str, Any]) -> str:
        """Submit one MinerU API parse task."""
        response = self.session.post(
            self.create_task_url,
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise MinerUApiError(f"MinerU 创建任务失败: {data}")
        task_id = data.get("data", {}).get("task_id")
        if not task_id:
            raise MinerUApiError(f"MinerU 创建任务响应缺少 task_id: {data}")
        return str(task_id)

    def poll_task(
        self,
        task_id: str,
        *,
        doc_id: str = "",
        page_range: str = "",
    ) -> dict[str, Any]:
        """Poll one MinerU API task until done or failed."""
        deadline = time.monotonic() + self.poll_timeout
        while True:
            response = self.session.get(
                self.query_task_url.format(task_id=task_id),
                headers={"Authorization": f"Bearer {self.api_key}", "Accept": "*/*"},
                timeout=60,
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("code") != 0:
                raise MinerUApiError(f"MinerU 查询任务失败: {payload}")

            data = payload.get("data", {})
            state = data.get("state")
            progress = data.get("extract_progress") or {}
            extracted_pages = progress.get("extracted_pages")
            total_pages = progress.get("total_pages")
            progress_text = (
                f"{extracted_pages}/{total_pages}"
                if extracted_pages is not None and total_pages is not None
                else "n/a"
            )
            logger.info(
                "[%s] task %s state=%s page_range=%s progress=%s",
                doc_id or "unknown-doc",
                task_id,
                state,
                page_range or "unknown-range",
                progress_text,
            )
            if state == "done":
                if not data.get("full_zip_url"):
                    raise MinerUApiError(f"MinerU 任务完成但缺少 full_zip_url: {payload}")
                return data
            if state == "failed":
                raise MinerUApiError(data.get("err_msg") or f"MinerU 任务失败: {payload}")
            if state not in {"pending", "running", "converting"}:
                raise MinerUApiError(f"MinerU 未知任务状态: {payload}")
            if time.monotonic() >= deadline:
                raise MinerUApiError(f"MinerU 任务轮询超时: {task_id}")
            time.sleep(self.poll_interval)

    def _write_task_record(self, record: dict[str, Any]) -> None:
        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            **record,
        }
        with open(self.task_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _find_cached_full_md(self, doc_id: str, part_index: int) -> Path | None:
        """Find cached full.md for one successful API segment."""
        candidates = sorted(self._extract_dir(doc_id, part_index).rglob("full.md"))
        for candidate in candidates:
            if candidate.exists() and candidate.stat().st_size > 0:
                return candidate
        return None

    def _part_dir(self, doc_id: str, part_index: int) -> Path:
        return self.raw_dir / doc_id / f"part_{part_index:02d}"

    def _zip_path(self, doc_id: str, part_index: int) -> Path:
        return self._part_dir(doc_id, part_index) / "result.zip"

    def _extract_dir(self, doc_id: str, part_index: int) -> Path:
        return self._part_dir(doc_id, part_index) / "extracted"

    def _find_cached_result_zip(self, doc_id: str, part_index: int) -> Path | None:
        zip_path = self._zip_path(doc_id, part_index)
        if zip_path.exists() and zip_path.stat().st_size > 0:
            return zip_path
        return None

    def _extract_full_markdown_from_zip(
        self,
        zip_path: Path,
        *,
        doc_id: str,
        part_index: int,
    ) -> str:
        """Extract one MinerU result zip and return full.md content."""
        extract_dir = self._extract_dir(doc_id, part_index)
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        full_md_candidates = sorted(extract_dir.rglob("full.md"))
        if not full_md_candidates:
            raise MinerUApiError(f"MinerU 结果包缺少 full.md: {zip_path}")
        full_md = full_md_candidates[0].read_text(encoding="utf-8")
        if not full_md.strip():
            raise MinerUApiError(f"MinerU 结果包 full.md 为空: {zip_path}")
        return full_md

    def _load_successful_segments(self) -> set[tuple[str, int, str]]:
        """Load successful segment keys that have reusable raw markdown."""
        if not self.task_log_path.exists():
            return set()

        successful: set[tuple[str, int, str]] = set()
        with open(self.task_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("status") != "success":
                    continue
                doc_id = str(record.get("doc_id", ""))
                part_index = int(record.get("part_index", 0))
                page_range = str(record.get("page_range", ""))
                if self._find_cached_full_md(doc_id, part_index) is not None:
                    successful.add((doc_id, part_index, page_range))
        return successful

    def _load_submitted_segments(self) -> dict[tuple[str, int, str], str]:
        """Load submitted segment task IDs that have not reached a final state."""
        if not self.task_log_path.exists():
            return {}

        latest_status: dict[tuple[str, int, str], tuple[str, str]] = {}
        with open(self.task_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                doc_id = str(record.get("doc_id", ""))
                part_index = int(record.get("part_index", 0))
                page_range = str(record.get("page_range", ""))
                task_id = str(record.get("task_id", ""))
                status = str(record.get("status", ""))
                if not doc_id or not part_index or not page_range or not task_id:
                    continue
                latest_status[(doc_id, part_index, page_range)] = (status, task_id)
        return {
            key: task_id
            for key, (status, task_id) in latest_status.items()
            if status == "submitted"
        }

    def download_full_markdown(
        self,
        *,
        full_zip_url: str,
        doc_id: str,
        part_index: int,
    ) -> str:
        """Download MinerU result zip and return extracted full.md content."""
        part_dir = self._part_dir(doc_id, part_index)
        zip_path = self._zip_path(doc_id, part_index)
        last_error: Exception | None = None
        for attempt in range(1, self.download_max_retries + 1):
            if part_dir.exists():
                shutil.rmtree(part_dir)
            part_dir.mkdir(parents=True, exist_ok=True)
            try:
                response = self.session.get(full_zip_url, timeout=120)
                response.raise_for_status()

                zip_path.write_bytes(response.content)
                return self._extract_full_markdown_from_zip(
                    zip_path,
                    doc_id=doc_id,
                    part_index=part_index,
                )
            except (
                requests.exceptions.RequestException,
                zipfile.BadZipFile,
                OSError,
                MinerUApiError,
            ) as exc:
                last_error = exc
                if attempt >= self.download_max_retries:
                    break
                logger.warning(
                    "[%s] 下载 MinerU 结果包失败，%.1fs 后重试 (%d/%d): %s",
                    doc_id,
                    self.download_retry_delay,
                    attempt,
                    self.download_max_retries,
                    exc,
                )
                time.sleep(self.download_retry_delay)

        if last_error is not None:
            raise last_error
        raise MinerUApiError(f"MinerU 结果包下载失败: {full_zip_url}")

    def parse_pdf(self, pdf_path: Path, metadata: dict[str, str]) -> Path | None:
        """Parse one PDF through segmented MinerU API tasks."""
        doc_id = pdf_path.stem
        pdf_url = metadata.get("pdf_url") or metadata.get("url") or ""
        if not pdf_url:
            raise MinerUApiError(f"[{doc_id}] metadata 缺少 pdf_url")

        total_pages = get_pdf_page_count(pdf_path)
        page_ranges = split_page_ranges(total_pages)
        logger.info(
            "[%s] MinerU API parse: pages=%d, segments=%d",
            doc_id,
            total_pages,
            len(page_ranges),
        )

        markdown_parts: list[str] = []
        successful_segments = self._load_successful_segments()
        submitted_segments = self._load_submitted_segments()
        for part_index, page_range in enumerate(page_ranges, start=1):
            cached_full_md = self._find_cached_full_md(doc_id, part_index)
            if (doc_id, part_index, page_range) in successful_segments and cached_full_md:
                logger.info(
                    "[%s] reuse segment %d/%d: %s",
                    doc_id,
                    part_index,
                    len(page_ranges),
                    page_range,
                )
                markdown_parts.append(cached_full_md.read_text(encoding="utf-8"))
                continue

            segment_key = (doc_id, part_index, page_range)
            if segment_key in submitted_segments:
                task_id = submitted_segments[segment_key]
                logger.info(
                    "[%s] resume submitted segment %d/%d: %s task=%s",
                    doc_id,
                    part_index,
                    len(page_ranges),
                    page_range,
                    task_id,
                )
            else:
                payload = self.build_task_payload(
                    pdf_url=pdf_url,
                    doc_id=doc_id,
                    part_index=part_index,
                    page_range=page_range,
                )
                logger.info("[%s] submit segment %d/%d: %s", doc_id, part_index, len(page_ranges), page_range)
                task_id = self.submit_task(payload)
                self._write_task_record(
                    {
                        "doc_id": doc_id,
                        "part_index": part_index,
                        "page_range": page_range,
                        "task_id": task_id,
                        "status": "submitted",
                        "full_zip_url": "",
                        "error": "",
                    },
                )
            try:
                task_data = self.poll_task(
                    task_id,
                    doc_id=doc_id,
                    page_range=page_range,
                )
                full_md = self.download_full_markdown(
                    full_zip_url=task_data["full_zip_url"],
                    doc_id=doc_id,
                    part_index=part_index,
                )
                if not full_md.strip():
                    raise MinerUApiError(f"[{doc_id}] segment {page_range} full.md 为空")
                markdown_parts.append(full_md)
                self._write_task_record(
                    {
                        "doc_id": doc_id,
                        "part_index": part_index,
                        "page_range": page_range,
                        "task_id": task_id,
                        "status": "success",
                        "full_zip_url": task_data["full_zip_url"],
                        "error": "",
                    },
                )
            except Exception as exc:
                self._write_task_record(
                    {
                        "doc_id": doc_id,
                        "part_index": part_index,
                        "page_range": page_range,
                        "task_id": task_id,
                        "status": "failed",
                        "full_zip_url": "",
                        "error": str(exc),
                    },
                )
                raise

        merged = "\n\n<!-- mineru-api-segment-break -->\n\n".join(
            part.strip() for part in markdown_parts if part.strip()
        )
        if not merged.strip():
            raise MinerUApiError(f"[{doc_id}] 合并 Markdown 为空")

        target_md = self.output_dir / f"{doc_id}.md"
        target_md.write_text(merged + "\n", encoding="utf-8")
        logger.info("[%s] MinerU API parse 完成: %s", doc_id, target_md)
        return target_md

    def run(self, limit: int | None = None) -> dict[str, int]:
        """Run MinerU API parse for annual report PDFs."""
        self._headers()
        metadata = self._load_metadata()
        pdf_files = sorted(self.pdf_dir.glob("*.pdf"))
        if limit:
            pdf_files = pdf_files[:limit]
        if not pdf_files:
            logger.warning("未找到 PDF 文件: %s", self.pdf_dir)
            return {"total": 0, "success": 0, "failed": 0}

        total = len(pdf_files)
        success = 0
        failed = 0
        for index, pdf_path in enumerate(pdf_files, start=1):
            doc_id = pdf_path.stem
            start = time.monotonic()
            logger.info("[%d/%d] MinerU API parse 开始: %s", index, total, doc_id)
            try:
                row = metadata.get(doc_id)
                if row is None:
                    raise MinerUApiError(f"[{doc_id}] metadata 中找不到对应记录")
                self.parse_pdf(pdf_path, row)
                success += 1
                status = "success"
            except Exception as exc:
                failed += 1
                status = "failed"
                logger.error("[%s] MinerU API parse 失败: %s", doc_id, exc)
            elapsed = time.monotonic() - start
            logger.info(
                "[%d/%d] MinerU API parse %s: %s (耗时 %.1fs)",
                index,
                total,
                status,
                doc_id,
                elapsed,
            )

        return {"total": total, "success": success, "failed": failed}


class MinerUApiBatchParser(MinerUApiParser):
    """Parse annual reports with MinerU precise API URL batch endpoint."""

    def __init__(
        self,
        metadata_path: str = "data/metadata/metadata.csv",
        pdf_dir: str = "data/pdf",
        output_dir: str = "data/parsed",
        task_log_path: str = "data/parsed/mineru_api_tasks.jsonl",
        raw_dir: str = "data/parsed/mineru_api_raw",
        api_key: str | None = None,
        session: requests.Session | None = None,
        poll_interval: float = 5.0,
        poll_timeout: float = 1800.0,
        model_version: str = "pipeline",
        batch_size: int | None = None,
        submit_file_limit_per_minute: int = DEFAULT_SUBMIT_FILE_LIMIT_PER_MINUTE,
        download_max_retries: int | None = None,
        download_retry_delay: float | None = None,
    ) -> None:
        super().__init__(
            metadata_path=metadata_path,
            pdf_dir=pdf_dir,
            output_dir=output_dir,
            task_log_path=task_log_path,
            raw_dir=raw_dir,
            api_key=api_key,
            session=session,
            poll_interval=poll_interval,
            poll_timeout=poll_timeout,
            model_version=model_version,
            download_max_retries=download_max_retries,
            download_retry_delay=download_retry_delay,
        )
        env_batch_size = os.getenv("MINERU_API_BATCH_SIZE")
        self.batch_size = batch_size or int(env_batch_size or str(DEFAULT_BATCH_SIZE))
        self.download_workers = max(
            1,
            int(os.getenv("MINERU_API_DOWNLOAD_WORKERS", str(DEFAULT_DOWNLOAD_WORKERS))),
        )
        self.extract_workers = max(
            1,
            int(os.getenv("MINERU_API_EXTRACT_WORKERS", str(DEFAULT_EXTRACT_WORKERS))),
        )
        self.create_batch_url = os.getenv("MINERU_API_BATCH_URL", CREATE_BATCH_TASK_URL)
        self.query_batch_url = os.getenv("MINERU_API_BATCH_QUERY_URL", QUERY_BATCH_TASK_URL)
        self.submit_file_limit_per_minute = submit_file_limit_per_minute
        self._submit_timestamps: deque[float] = deque()

    @staticmethod
    def _segment_key(doc_id: str, part_index: int, page_range: str) -> tuple[str, int, str]:
        return (doc_id, part_index, page_range)

    @staticmethod
    def _make_data_id(doc_id: str, part_index: int, page_range: str) -> str:
        digest = hashlib.sha1(f"{doc_id}|{part_index}|{page_range}".encode("utf-8")).hexdigest()
        return f"p{part_index}_{digest}"[:128]

    def build_batch_file_payload(
        self,
        *,
        pdf_url: str,
        doc_id: str,
        part_index: int,
        page_range: str,
    ) -> dict[str, Any]:
        """Build one files[] item for MinerU URL batch task."""
        return {
            "url": pdf_url,
            "data_id": self._make_data_id(doc_id, part_index, page_range),
            "page_ranges": page_range,
            "is_ocr": False,
        }

    def _wait_for_submit_capacity(self, file_count: int) -> None:
        """Respect MinerU's shared 50 files/min submit limit."""
        if file_count <= 0 or self.submit_file_limit_per_minute <= 0:
            return

        window_seconds = 60.0
        while True:
            now = time.monotonic()
            while self._submit_timestamps and now - self._submit_timestamps[0] >= window_seconds:
                self._submit_timestamps.popleft()
            if len(self._submit_timestamps) + file_count <= self.submit_file_limit_per_minute:
                self._submit_timestamps.extend([now] * file_count)
                return
            wait_seconds = window_seconds - (now - self._submit_timestamps[0]) + 0.1
            logger.info(
                "MinerU API batch submit 限速: 等待 %.1fs 后提交 %d 个文件",
                max(wait_seconds, 0.1),
                file_count,
            )
            time.sleep(max(wait_seconds, 0.1))

    def submit_batch(self, file_payloads: list[dict[str, Any]]) -> str:
        """Submit one MinerU URL batch task."""
        self._wait_for_submit_capacity(len(file_payloads))
        payload = {
            "files": file_payloads,
            "model_version": self.model_version,
            "enable_table": True,
            "enable_formula": False,
            "language": "ch",
        }
        response = self.session.post(
            self.create_batch_url,
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise MinerUApiError(f"MinerU 批量创建任务失败: {data}")
        batch_id = data.get("data", {}).get("batch_id")
        if not batch_id:
            raise MinerUApiError(f"MinerU 批量创建任务响应缺少 batch_id: {data}")
        return str(batch_id)

    def _query_batch_results(self, batch_id: str) -> dict[str, dict[str, Any]]:
        """Query one batch once and return results keyed by data_id."""
        response = self.session.get(
            self.query_batch_url.format(batch_id=batch_id),
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "*/*"},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise MinerUApiError(f"MinerU 批量查询任务失败: {payload}")

        results = payload.get("data", {}).get("extract_result") or []
        return {
            str(item.get("data_id", "")): item
            for item in results
            if item.get("data_id")
        }

    def poll_batch(
        self,
        batch_id: str,
        *,
        expected_data_ids: set[str],
    ) -> dict[str, dict[str, Any]]:
        """Poll one batch until all expected data_id values are done."""
        deadline = time.monotonic() + self.poll_timeout
        while True:
            by_data_id = self._query_batch_results(batch_id)
            states = {
                data_id: by_data_id.get(data_id, {}).get("state", "missing")
                for data_id in expected_data_ids
            }
            logger.info("batch %s states=%s", batch_id, states)

            failed = {
                data_id: by_data_id[data_id]
                for data_id, state in states.items()
                if state == "failed" and data_id in by_data_id
            }
            if failed:
                first_data_id, first_result = next(iter(failed.items()))
                raise MinerUApiError(
                    first_result.get("err_msg")
                    or f"MinerU 批量任务失败: {batch_id} {first_data_id}"
                )

            if all(state == "done" for state in states.values()):
                missing_zip = [
                    data_id
                    for data_id in expected_data_ids
                    if not by_data_id[data_id].get("full_zip_url")
                ]
                if missing_zip:
                    raise MinerUApiError(f"MinerU 批量任务完成但缺少 full_zip_url: {missing_zip}")
                return {data_id: by_data_id[data_id] for data_id in expected_data_ids}

            if time.monotonic() >= deadline:
                raise MinerUApiError(f"MinerU 批量任务轮询超时: {batch_id}")
            time.sleep(self.poll_interval)

    def _load_resumable_batch_segments(self) -> dict[tuple[str, int, str], dict[str, str]]:
        """Load batch segment records that can resume without resubmitting."""
        if not self.task_log_path.exists():
            return {}

        latest_status: dict[tuple[str, int, str], dict[str, str]] = {}
        with open(self.task_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                doc_id = str(record.get("doc_id", ""))
                part_index = int(record.get("part_index", 0))
                page_range = str(record.get("page_range", ""))
                batch_id = str(record.get("batch_id") or record.get("task_id") or "")
                data_id = str(record.get("data_id", ""))
                status = str(record.get("status", ""))
                if not doc_id or not part_index or not page_range or not batch_id or not data_id:
                    continue
                latest_status[self._segment_key(doc_id, part_index, page_range)] = {
                    "status": status,
                    "batch_id": batch_id,
                    "data_id": data_id,
                    "full_zip_url": str(record.get("full_zip_url", "")),
                    "error": str(record.get("error", "")),
                }

        return {
            key: record
            for key, record in latest_status.items()
            if record["status"]
            in {"submitted", "ready", "zip_downloaded", "download_failed", "extract_failed", "failed"}
        }

    def _prepare_segments(
        self,
        pdf_files: list[Path],
        metadata: dict[str, dict[str, str]],
    ) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], int]:
        successful_segments = self._load_successful_segments()
        resumable_segments = self._load_resumable_batch_segments()
        segments_to_submit: list[dict[str, Any]] = []
        segments_by_doc: dict[str, list[dict[str, Any]]] = defaultdict(list)
        prepared_docs = 0

        for pdf_path in pdf_files:
            doc_id = pdf_path.stem
            row = metadata.get(doc_id)
            if row is None:
                logger.error("[%s] metadata 中找不到对应记录", doc_id)
                continue
            pdf_url = row.get("pdf_url") or row.get("url") or ""
            if not pdf_url:
                logger.error("[%s] metadata 缺少 pdf_url", doc_id)
                continue

            total_pages = get_pdf_page_count(pdf_path)
            page_ranges = split_page_ranges(total_pages)
            logger.info(
                "[%s] MinerU API batch prepare: pages=%d, segments=%d",
                doc_id,
                total_pages,
                len(page_ranges),
            )
            prepared_docs += 1
            for part_index, page_range in enumerate(page_ranges, start=1):
                key = self._segment_key(doc_id, part_index, page_range)
                segment = {
                    "doc_id": doc_id,
                    "part_index": part_index,
                    "page_range": page_range,
                    "pdf_url": pdf_url,
                    "data_id": self._make_data_id(doc_id, part_index, page_range),
                    "batch_id": "",
                    "full_zip_url": "",
                    "error": "",
                    "status": "pending",
                }
                cached_full_md = self._find_cached_full_md(doc_id, part_index)
                cached_zip = self._find_cached_result_zip(doc_id, part_index)
                if key in successful_segments and cached_full_md:
                    segment["status"] = "success"
                    segment["cached_md"] = cached_full_md
                elif cached_zip is not None:
                    segment["status"] = "zip_downloaded"
                    segment["zip_path"] = cached_zip
                    if key in resumable_segments:
                        segment["batch_id"] = resumable_segments[key]["batch_id"]
                        segment["data_id"] = resumable_segments[key]["data_id"]
                        segment["full_zip_url"] = resumable_segments[key].get("full_zip_url", "")
                elif key in resumable_segments:
                    resume = resumable_segments[key]
                    segment["batch_id"] = resume["batch_id"]
                    segment["data_id"] = resume["data_id"]
                    segment["full_zip_url"] = resume.get("full_zip_url", "")
                    segment["error"] = resume.get("error", "")
                    if segment["full_zip_url"]:
                        segment["status"] = "ready"
                    else:
                        segment["status"] = "submitted"
                else:
                    segments_to_submit.append(segment)
                segments_by_doc[doc_id].append(segment)

        return segments_to_submit, segments_by_doc, prepared_docs

    def _submit_pending_segments(self, segments: list[dict[str, Any]]) -> None:
        for start in range(0, len(segments), self.batch_size):
            chunk = segments[start : start + self.batch_size]
            file_payloads = [
                self.build_batch_file_payload(
                    pdf_url=segment["pdf_url"],
                    doc_id=segment["doc_id"],
                    part_index=segment["part_index"],
                    page_range=segment["page_range"],
                )
                for segment in chunk
            ]
            logger.info("submit MinerU API batch: files=%d", len(file_payloads))
            batch_id = self.submit_batch(file_payloads)
            for segment, file_payload in zip(chunk, file_payloads, strict=True):
                segment["status"] = "submitted"
                segment["batch_id"] = batch_id
                segment["data_id"] = file_payload["data_id"]
                self._write_task_record(
                    {
                        "doc_id": segment["doc_id"],
                        "part_index": segment["part_index"],
                        "page_range": segment["page_range"],
                        "task_id": batch_id,
                        "batch_id": batch_id,
                        "data_id": segment["data_id"],
                        "status": "submitted",
                        "full_zip_url": "",
                        "error": "",
                    },
                )

    @staticmethod
    def _iter_segments(
        segments_by_doc: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        return [segment for segments in segments_by_doc.values() for segment in segments]

    def _poll_submitted_segments(self, segments_by_doc: dict[str, list[dict[str, Any]]]) -> None:
        """Poll all submitted batches together and mark done segments as ready."""
        segments_by_batch: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for segment in self._iter_segments(segments_by_doc):
            if segment["status"] == "submitted":
                segments_by_batch[segment["batch_id"]].append(segment)

        if not segments_by_batch:
            return

        pending_by_batch = {
            batch_id: {str(segment["data_id"]) for segment in segments}
            for batch_id, segments in segments_by_batch.items()
        }
        deadline = time.monotonic() + self.poll_timeout
        while pending_by_batch:
            for batch_id in list(pending_by_batch):
                pending_data_ids = pending_by_batch[batch_id]
                try:
                    by_data_id = self._query_batch_results(batch_id)
                except Exception as exc:
                    if time.monotonic() < deadline:
                        logger.warning("batch %s query failed, will retry: %s", batch_id, exc)
                        continue
                    for segment in segments_by_batch[batch_id]:
                        if str(segment["data_id"]) not in pending_data_ids:
                            continue
                        segment["status"] = "failed"
                        segment["error"] = str(exc)
                        self._write_task_record(
                            {
                                "doc_id": segment["doc_id"],
                                "part_index": segment["part_index"],
                                "page_range": segment["page_range"],
                                "task_id": batch_id,
                                "batch_id": batch_id,
                                "data_id": segment["data_id"],
                                "status": "failed",
                                "full_zip_url": segment.get("full_zip_url", ""),
                                "error": str(exc),
                            },
                        )
                    del pending_by_batch[batch_id]
                    continue

                states = {
                    data_id: by_data_id.get(data_id, {}).get("state", "missing")
                    for data_id in pending_data_ids
                }
                ready_count = sum(1 for state in states.values() if state == "done")
                logger.info(
                    "batch %s progress: ready=%d/%d states=%s",
                    batch_id,
                    ready_count,
                    len(states),
                    states,
                )
                for segment in segments_by_batch[batch_id]:
                    data_id = str(segment["data_id"])
                    if data_id not in pending_data_ids:
                        continue
                    result = by_data_id.get(data_id, {})
                    state = result.get("state", "missing")
                    if state == "done":
                        full_zip_url = str(result.get("full_zip_url", ""))
                        if full_zip_url:
                            segment["status"] = "ready"
                            segment["full_zip_url"] = full_zip_url
                            self._write_task_record(
                                {
                                    "doc_id": segment["doc_id"],
                                    "part_index": segment["part_index"],
                                    "page_range": segment["page_range"],
                                    "task_id": batch_id,
                                    "batch_id": batch_id,
                                    "data_id": data_id,
                                    "status": "ready",
                                    "full_zip_url": full_zip_url,
                                    "error": "",
                                },
                            )
                        else:
                            segment["status"] = "failed"
                            segment["error"] = "MinerU 批量任务完成但缺少 full_zip_url"
                            self._write_task_record(
                                {
                                    "doc_id": segment["doc_id"],
                                    "part_index": segment["part_index"],
                                    "page_range": segment["page_range"],
                                    "task_id": batch_id,
                                    "batch_id": batch_id,
                                    "data_id": data_id,
                                    "status": "failed",
                                    "full_zip_url": "",
                                    "error": segment["error"],
                                },
                            )
                        pending_data_ids.remove(data_id)
                    elif state == "failed":
                        segment["status"] = "failed"
                        segment["error"] = str(result.get("err_msg") or "MinerU 批量任务失败")
                        self._write_task_record(
                            {
                                "doc_id": segment["doc_id"],
                                "part_index": segment["part_index"],
                                "page_range": segment["page_range"],
                                "task_id": batch_id,
                                "batch_id": batch_id,
                                "data_id": data_id,
                                "status": "failed",
                                "full_zip_url": str(result.get("full_zip_url", "")),
                                "error": segment["error"],
                            },
                        )
                        pending_data_ids.remove(data_id)
                    elif state not in {"pending", "running", "converting", "missing"}:
                        segment["status"] = "failed"
                        segment["error"] = f"MinerU 未知批量任务状态: {state}"
                        self._write_task_record(
                            {
                                "doc_id": segment["doc_id"],
                                "part_index": segment["part_index"],
                                "page_range": segment["page_range"],
                                "task_id": batch_id,
                                "batch_id": batch_id,
                                "data_id": data_id,
                                "status": "failed",
                                "full_zip_url": str(result.get("full_zip_url", "")),
                                "error": segment["error"],
                            },
                        )
                        pending_data_ids.remove(data_id)

                if not pending_data_ids:
                    del pending_by_batch[batch_id]

            self._download_ready_zips(segments_by_doc)
            self._extract_downloaded_zips(segments_by_doc)

            if pending_by_batch:
                if time.monotonic() >= deadline:
                    for batch_id, pending_data_ids in list(pending_by_batch.items()):
                        for segment in segments_by_batch[batch_id]:
                            if str(segment["data_id"]) not in pending_data_ids:
                                continue
                            segment["status"] = "failed"
                            segment["error"] = f"MinerU 批量任务轮询超时: {batch_id}"
                            self._write_task_record(
                                {
                                    "doc_id": segment["doc_id"],
                                    "part_index": segment["part_index"],
                                    "page_range": segment["page_range"],
                                    "task_id": batch_id,
                                    "batch_id": batch_id,
                                    "data_id": segment["data_id"],
                                    "status": "failed",
                                    "full_zip_url": segment.get("full_zip_url", ""),
                                    "error": segment["error"],
                                },
                            )
                        del pending_by_batch[batch_id]
                    break
                time.sleep(self.poll_interval)

    def _download_segment_zip(self, segment: dict[str, Any]) -> tuple[Path, int, float]:
        """Download one ready MinerU result zip."""
        doc_id = str(segment["doc_id"])
        part_index = int(segment["part_index"])
        zip_path = self._zip_path(doc_id, part_index)
        existing_zip = self._find_cached_result_zip(doc_id, part_index)
        if existing_zip is not None:
            return existing_zip, existing_zip.stat().st_size, 0.0

        zip_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = zip_path.with_name("result.zip.tmp")
        last_error: Exception | None = None
        start_time = time.monotonic()
        for attempt in range(1, self.download_max_retries + 1):
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
                response = self.session.get(str(segment["full_zip_url"]), timeout=120)
                response.raise_for_status()
                tmp_path.write_bytes(response.content)
                if tmp_path.stat().st_size <= 0:
                    raise MinerUApiError(f"MinerU 结果包为空: {segment['full_zip_url']}")
                tmp_path.replace(zip_path)
                elapsed = time.monotonic() - start_time
                return zip_path, zip_path.stat().st_size, elapsed
            except (
                requests.exceptions.RequestException,
                OSError,
                MinerUApiError,
            ) as exc:
                last_error = exc
                if attempt >= self.download_max_retries:
                    break
                logger.warning(
                    "[%s] 下载 MinerU 结果包失败，%.1fs 后重试 (%d/%d): %s",
                    doc_id,
                    self.download_retry_delay,
                    attempt,
                    self.download_max_retries,
                    exc,
                )
                time.sleep(self.download_retry_delay)

        if last_error is not None:
            raise last_error
        raise MinerUApiError(f"MinerU 结果包下载失败: {segment['full_zip_url']}")

    def _refresh_segment_full_zip_url(self, segment: dict[str, Any]) -> str:
        """Refresh a segment result URL from its batch result."""
        batch_id = str(segment.get("batch_id", ""))
        data_id = str(segment.get("data_id", ""))
        if not batch_id or not data_id:
            return ""

        by_data_id = self._query_batch_results(batch_id)
        result = by_data_id.get(data_id, {})
        state = result.get("state", "missing")
        if state == "failed":
            raise MinerUApiError(str(result.get("err_msg") or "MinerU 批量任务失败"))
        if state != "done":
            return ""

        full_zip_url = str(result.get("full_zip_url", ""))
        if not full_zip_url:
            return ""

        segment["full_zip_url"] = full_zip_url
        self._write_task_record(
            {
                "doc_id": segment["doc_id"],
                "part_index": segment["part_index"],
                "page_range": segment["page_range"],
                "task_id": batch_id,
                "batch_id": batch_id,
                "data_id": data_id,
                "status": "ready",
                "full_zip_url": full_zip_url,
                "error": "",
            },
        )
        return full_zip_url

    def _download_ready_zips(self, segments_by_doc: dict[str, list[dict[str, Any]]]) -> None:
        ready_segments = [
            segment
            for segment in self._iter_segments(segments_by_doc)
            if segment["status"] == "ready" and segment.get("full_zip_url")
        ]
        if not ready_segments:
            return

        workers = min(self.download_workers, len(ready_segments))
        logger.info(
            "MinerU API batch zip download: ready=%d workers=%d",
            len(ready_segments),
            workers,
        )
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_segment = {
                executor.submit(self._download_segment_zip, segment): segment
                for segment in ready_segments
            }
            for future in as_completed(future_to_segment):
                segment = future_to_segment[future]
                try:
                    zip_path, zip_size, elapsed = future.result()
                    segment["status"] = "zip_downloaded"
                    segment["zip_path"] = zip_path
                    logger.info(
                        "[%s] segment %s zip downloaded: %.2f MB in %.1fs",
                        segment["doc_id"],
                        segment["page_range"],
                        zip_size / 1024 / 1024,
                        elapsed,
                    )
                    self._write_task_record(
                        {
                            "doc_id": segment["doc_id"],
                            "part_index": segment["part_index"],
                            "page_range": segment["page_range"],
                            "task_id": segment.get("batch_id", ""),
                            "batch_id": segment.get("batch_id", ""),
                            "data_id": segment["data_id"],
                            "status": "zip_downloaded",
                            "full_zip_url": segment.get("full_zip_url", ""),
                            "zip_size_bytes": zip_size,
                            "error": "",
                        },
                    )
                except Exception as exc:
                    old_url = str(segment.get("full_zip_url", ""))
                    try:
                        refreshed_url = self._refresh_segment_full_zip_url(segment)
                        if refreshed_url and refreshed_url != old_url:
                            logger.warning(
                                "[%s] MinerU 结果包旧 URL 下载失败，已刷新 URL 后重试: %s",
                                segment["doc_id"],
                                exc,
                            )
                            zip_path, zip_size, elapsed = self._download_segment_zip(segment)
                            segment["status"] = "zip_downloaded"
                            segment["zip_path"] = zip_path
                            logger.info(
                                "[%s] segment %s refreshed zip downloaded: %.2f MB in %.1fs",
                                segment["doc_id"],
                                segment["page_range"],
                                zip_size / 1024 / 1024,
                                elapsed,
                            )
                            self._write_task_record(
                                {
                                    "doc_id": segment["doc_id"],
                                    "part_index": segment["part_index"],
                                    "page_range": segment["page_range"],
                                    "task_id": segment.get("batch_id", ""),
                                    "batch_id": segment.get("batch_id", ""),
                                    "data_id": segment["data_id"],
                                    "status": "zip_downloaded",
                                    "full_zip_url": segment.get("full_zip_url", ""),
                                    "zip_size_bytes": zip_size,
                                    "error": "",
                                },
                            )
                            continue
                    except Exception as refresh_exc:
                        exc = refresh_exc
                    segment["status"] = "download_failed"
                    segment["error"] = str(exc)
                    self._write_task_record(
                        {
                            "doc_id": segment["doc_id"],
                            "part_index": segment["part_index"],
                            "page_range": segment["page_range"],
                            "task_id": segment.get("batch_id", ""),
                            "batch_id": segment.get("batch_id", ""),
                            "data_id": segment["data_id"],
                            "status": "download_failed",
                            "full_zip_url": segment.get("full_zip_url", ""),
                            "error": str(exc),
                        },
                    )

    def _extract_segment_markdown(self, segment: dict[str, Any]) -> tuple[Path, int]:
        """Extract one downloaded zip and return the full.md path."""
        doc_id = str(segment["doc_id"])
        part_index = int(segment["part_index"])
        cached_md = self._find_cached_full_md(doc_id, part_index)
        if cached_md is not None:
            return cached_md, cached_md.stat().st_size

        zip_path = Path(segment.get("zip_path") or self._zip_path(doc_id, part_index))
        full_md = self._extract_full_markdown_from_zip(
            zip_path,
            doc_id=doc_id,
            part_index=part_index,
        )
        cached_md = self._find_cached_full_md(doc_id, part_index)
        if cached_md is None:
            raise MinerUApiError(f"[{doc_id}] segment {segment['page_range']} full.md 未落盘")
        return cached_md, len(full_md.encode("utf-8"))

    def _extract_downloaded_zips(self, segments_by_doc: dict[str, list[dict[str, Any]]]) -> None:
        downloaded_segments = [
            segment
            for segment in self._iter_segments(segments_by_doc)
            if segment["status"] == "zip_downloaded"
        ]
        if not downloaded_segments:
            return

        workers = min(self.extract_workers, len(downloaded_segments))
        logger.info(
            "MinerU API batch zip extract: downloaded=%d workers=%d",
            len(downloaded_segments),
            workers,
        )
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_segment = {
                executor.submit(self._extract_segment_markdown, segment): segment
                for segment in downloaded_segments
            }
            for future in as_completed(future_to_segment):
                segment = future_to_segment[future]
                try:
                    cached_md, md_size = future.result()
                    segment["status"] = "success"
                    segment["cached_md"] = cached_md
                    logger.info(
                        "[%s] segment %s extracted full.md: %.2f MB",
                        segment["doc_id"],
                        segment["page_range"],
                        md_size / 1024 / 1024,
                    )
                    self._write_task_record(
                        {
                            "doc_id": segment["doc_id"],
                            "part_index": segment["part_index"],
                            "page_range": segment["page_range"],
                            "task_id": segment.get("batch_id", ""),
                            "batch_id": segment.get("batch_id", ""),
                            "data_id": segment["data_id"],
                            "status": "success",
                            "full_zip_url": segment.get("full_zip_url", ""),
                            "error": "",
                        },
                    )
                except Exception as exc:
                    segment["status"] = "extract_failed"
                    segment["error"] = str(exc)
                    self._write_task_record(
                        {
                            "doc_id": segment["doc_id"],
                            "part_index": segment["part_index"],
                            "page_range": segment["page_range"],
                            "task_id": segment.get("batch_id", ""),
                            "batch_id": segment.get("batch_id", ""),
                            "data_id": segment["data_id"],
                            "status": "extract_failed",
                            "full_zip_url": segment.get("full_zip_url", ""),
                            "error": str(exc),
                        },
                    )

    def _complete_submitted_segments(self, segments_by_doc: dict[str, list[dict[str, Any]]]) -> None:
        self._poll_submitted_segments(segments_by_doc)
        self._download_ready_zips(segments_by_doc)
        self._extract_downloaded_zips(segments_by_doc)

    def _merge_docs(self, segments_by_doc: dict[str, list[dict[str, Any]]]) -> tuple[int, int]:
        success = 0
        failed = 0
        for doc_id, segments in segments_by_doc.items():
            markdown_parts: list[str] = []
            doc_failed = False
            for segment in sorted(segments, key=lambda item: item["part_index"]):
                cached_md = segment.get("cached_md") or self._find_cached_full_md(
                    doc_id,
                    int(segment["part_index"]),
                )
                if segment.get("status") != "success" or cached_md is None:
                    logger.error("[%s] segment 未完成: %s", doc_id, segment["page_range"])
                    doc_failed = True
                    break
                markdown_parts.append(cached_md.read_text(encoding="utf-8"))

            if doc_failed:
                failed += 1
                continue
            merged = "\n\n<!-- mineru-api-segment-break -->\n\n".join(
                part.strip() for part in markdown_parts if part.strip()
            )
            if not merged.strip():
                logger.error("[%s] 合并 Markdown 为空", doc_id)
                failed += 1
                continue
            target_md = self.output_dir / f"{doc_id}.md"
            target_md.write_text(merged + "\n", encoding="utf-8")
            logger.info("[%s] MinerU API batch parse 完成: %s", doc_id, target_md)
            success += 1
        return success, failed

    def run(self, limit: int | None = None) -> dict[str, int]:
        """Run MinerU API URL batch parse for annual report PDFs."""
        self._headers()
        metadata = self._load_metadata()
        pdf_files = sorted(self.pdf_dir.glob("*.pdf"))
        if limit:
            pdf_files = pdf_files[:limit]
        if not pdf_files:
            logger.warning("未找到 PDF 文件: %s", self.pdf_dir)
            return {"total": 0, "success": 0, "failed": 0}

        segments_to_submit, segments_by_doc, total = self._prepare_segments(pdf_files, metadata)
        if total == 0:
            return {"total": len(pdf_files), "success": 0, "failed": len(pdf_files)}

        self._submit_pending_segments(segments_to_submit)
        self._complete_submitted_segments(segments_by_doc)
        success, failed = self._merge_docs(segments_by_doc)
        return {"total": total, "success": success, "failed": failed}
