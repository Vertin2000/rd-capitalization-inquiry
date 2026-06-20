"""巨潮资讯网问询函/回复函候选发现。

首版只负责 discovery：读取年报 metadata，按年报发布日期后 180 天查询
巨潮前端公开公告接口，输出可被 PDFDownloader 复用的候选 metadata。
"""

from __future__ import annotations

import csv
import json
import logging
import re
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.common import load_config
from src.crawl._common import infer_market, report_year_from_publish_date
from src.crawl.inquiry_quality import build_inquiry_doc_id, classify_document_role

logger = logging.getLogger(__name__)

CNINFO_SEARCH_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_DOWNLOAD_BASE = "http://static.cninfo.com.cn/"
CNINFO_DETAIL_BASE = "http://www.cninfo.com.cn/new/disclosure/detail"
CNINFO_TZ = timezone(timedelta(hours=8))

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.cninfo.com.cn",
    "Referer": (
        "https://www.cninfo.com.cn/new/commonUrl/pageOfSearch"
        "?url=disclosure/list/search"
    ),
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
}

INQUIRY_METADATA_COLUMNS = [
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
    "pdf_title",
    "pdf_title_status",
    "title_match_status",
    "source",
    "crawl_time",
    "error_message",
    "notes",
]

TITLE_KEYWORDS = (
    "年报问询函",
    "问询函",
    "关注函",
    "监管工作函",
)

EXCLUDED_TITLE_KEYWORDS = (
    "审核问询函",
    "审核中心意见落实函",
    "反馈意见落实函",
    "发行注册环节",
    "发行人及保荐机构",
    "保荐机构",
    "募集说明书",
    "向特定对象发行",
    "非公开发行",
    "公开发行",
    "首次公开发行",
    "可转换公司债券",
    "可转债",
    "再融资",
    "重大资产重组",
    "发行股份购买资产",
    "上市委",
    "IPO",
)


def clean_title(title: str) -> str:
    """清理巨潮标题中的 HTML 高亮标签和多余空白。"""
    cleaned = re.sub(r"<.*?>", "", title or "")
    return cleaned.strip()


def add_days(date_text: str, days: int) -> date:
    """返回 date_text 后 days 天的日期。"""
    start = datetime.strptime(date_text[:10], "%Y-%m-%d").date()
    return start + timedelta(days=days)


def classify_inquiry_title(title: str) -> str:
    """按标题粗分问询候选类型。"""
    cleaned = clean_title(title)
    normalized = re.sub(r"\s+", "", cleaned).upper()
    if any(keyword.upper() in normalized for keyword in EXCLUDED_TITLE_KEYWORDS):
        return "other"
    if "监管工作函" in cleaned:
        return "regulatory_work_letter"
    if "关注函" in cleaned:
        return "attention"
    if "问询函" in cleaned:
        if "回复" in cleaned or "答复" in cleaned:
            return "reply"
        return "inquiry"
    return "other"


class InquiryCrawler:
    """问询函/回复函候选发现 crawler。"""

    def __init__(self, config_path: str = "configs/crawl.yaml", limit: int | None = None) -> None:
        self.config = load_config(config_path)
        download_cfg = self.config.get("download", {})
        self.delay_seconds: float = download_cfg.get("delay_seconds", 3.0)
        self.max_retries: int = download_cfg.get("max_retries", 3)
        self.timeout_seconds: int = download_cfg.get("timeout_seconds", 30)
        self.max_pages: int = self.config.get("inquiry", {}).get("max_pages", 20)
        self.limit = limit

        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.annual_metadata_path = self.project_root / "data" / "metadata" / "metadata.csv"
        self.candidates_path = self.project_root / "data" / "inquiry" / "inquiry_candidates.csv"
        self.cache_path = self.project_root / "data" / "inquiry" / "inquiry_discovery_cache.json"
        self.log_path = self.project_root / "outputs" / "logs" / "inquiry_log.jsonl"
        self.download_pdf_dir = self.project_root / "data" / "inquiry" / "pdf"

        self.candidates_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.download_pdf_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=2,
                backoff_factor=0.6,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["POST"],
                raise_on_status=False,
            )
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def run(self, discover_only: bool = True, force: bool = False) -> Path:
        """执行候选发现，返回 inquiry_candidates.csv 路径。"""
        annual_records = self._read_annual_metadata()
        if self.limit is not None:
            annual_records = annual_records[: self.limit]
            logger.info("限制模式: 仅处理前 %d 条年报 metadata", self.limit)

        if force:
            self._reset_discovery_outputs()

        completed = self._load_cache()
        all_candidates = self._read_existing_candidates()
        seen = self._seen_candidate_keys(all_candidates)
        self._ensure_candidates_file(all_candidates)

        total = len(annual_records)
        started_at = time.monotonic()
        for index, annual_record in enumerate(annual_records, start=1):
            annual_doc_id = annual_record.get("doc_id", "")
            report_year = self._report_year(annual_record)
            if annual_doc_id in completed:
                self._print_progress(
                    index=index,
                    total=total,
                    annual_record=annual_record,
                    report_year=report_year,
                    raw_count=0,
                    parsed_count=0,
                    elapsed_seconds=time.monotonic() - started_at,
                    skipped=True,
                )
                continue

            item_started_at = time.monotonic()
            raw_items = self._search_for_annual_record(annual_record, report_year)
            parsed_count = 0
            new_rows: list[dict[str, str]] = []

            for item in raw_items:
                record = self._parse_candidate(item, annual_record, report_year)
                if record is None:
                    continue

                dedupe_key = record["announcement_id"] or record["pdf_url"]
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                new_rows.append(record)
                parsed_count += 1

            if new_rows:
                self._append_candidates(new_rows)
                all_candidates.extend(new_rows)

            log_entry = {
                "annual_doc_id": annual_record.get("doc_id", ""),
                "stock_code": annual_record.get("stock_code", ""),
                "stock_name": annual_record.get("stock_name", ""),
                "report_year": report_year,
                "raw_candidates": len(raw_items),
                "parsed_candidates": parsed_count,
                "query_window_start": annual_record.get("publish_date", "")[:10],
                "query_window_end": self._query_window_end(annual_record),
                "timestamp": datetime.now().isoformat(),
                "elapsed_seconds": round(time.monotonic() - item_started_at, 3),
            }
            self._append_log(log_entry)
            completed.add(annual_doc_id)
            self._save_cache(completed)
            self._print_progress(
                index=index,
                total=total,
                annual_record=annual_record,
                report_year=report_year,
                raw_count=len(raw_items),
                parsed_count=parsed_count,
                elapsed_seconds=time.monotonic() - started_at,
            )
            time.sleep(self.delay_seconds)

        logger.info("问询候选发现完成: %d 条候选", len(all_candidates))
        return self.candidates_path

    def _read_annual_metadata(self) -> list[dict[str, str]]:
        if not self.annual_metadata_path.exists():
            raise FileNotFoundError(f"metadata.csv 不存在: {self.annual_metadata_path}")
        with self.annual_metadata_path.open("r", encoding="utf-8", newline="") as f:
            records = list(csv.DictReader(f))
        if not records:
            raise ValueError("metadata.csv 为空")
        return records

    def _search_for_annual_record(
        self,
        annual_record: dict[str, str],
        report_year: str,
    ) -> list[dict[str, Any]]:
        code = annual_record.get("stock_code", "")
        name = annual_record.get("stock_name", "")
        start = annual_record.get("publish_date", "")[:10]
        end = self._query_window_end(annual_record)
        date_range = f"{start}~{end}"

        first_page = self._fetch_page(1, code, name, date_range)
        if not first_page:
            return []

        results = list(first_page.get("announcements") or [])
        total_pages = int(first_page.get("totalpages") or 0)
        page_count = min(total_pages, self.max_pages)

        for page_num in range(2, page_count + 1):
            page = self._fetch_page(page_num, code, name, date_range)
            if page:
                results.extend(page.get("announcements") or [])

        return results

    def _fetch_page(
        self,
        page_num: int,
        code: str,
        name: str,
        date_range: str,
    ) -> dict[str, Any] | None:
        _market, column, plate = infer_market(code)
        data = {
            "pageNum": str(page_num),
            "pageSize": "30",
            "column": column,
            "tabName": "fulltext",
            "plate": plate,
            # CNINFO frontend expects blank stock or "code,orgId".
            # Bare stock codes return empty lists for many companies.
            "stock": "",
            "searchkey": name,
            "secid": "",
            "category": "",
            "trade": "",
            "seDate": date_range,
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }

        for attempt in range(self.max_retries):
            try:
                resp = self.session.post(
                    CNINFO_SEARCH_URL,
                    data=data,
                    timeout=self.timeout_seconds,
                )
                if resp.status_code == 429 and attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                resp.raise_for_status()
                return resp.json()
            except (requests.RequestException, ValueError) as e:
                wait = 2 ** attempt
                logger.warning(
                    "问询候选请求失败 %s %s 第%d页 (尝试 %d/%d): %s",
                    code,
                    date_range,
                    page_num,
                    attempt + 1,
                    self.max_retries,
                    e,
                )
                if attempt < self.max_retries - 1:
                    time.sleep(wait)
        return None

    def _parse_candidate(
        self,
        item: dict[str, Any],
        annual_record: dict[str, str],
        report_year: str,
    ) -> dict[str, str] | None:
        title = clean_title(str(item.get("announcementTitle", "")))
        announcement_type = classify_inquiry_title(title)
        if announcement_type == "other" or not any(keyword in title for keyword in TITLE_KEYWORDS):
            return None

        adjunct_url = str(item.get("adjunctUrl", ""))
        if not adjunct_url:
            return None

        annual_code = annual_record.get("stock_code", "")
        sec_code = str(item.get("secCode", "") or annual_code)
        if sec_code and annual_code and sec_code != annual_code:
            return None

        stock_name = clean_title(str(item.get("secName", "") or annual_record.get("stock_name", "")))
        market = annual_record.get("market", "") or infer_market(annual_code)[0]
        publish_date = self._publish_date(item)
        announcement_id = str(item.get("announcementId", ""))
        pdf_url = self._pdf_url(adjunct_url)
        document_role = classify_document_role(title)
        doc_id = build_inquiry_doc_id(
            stock_code=annual_code,
            stock_name=stock_name,
            report_year=report_year,
            publish_date=publish_date,
            document_role=document_role,
            announcement_id=announcement_id,
        )
        local_pdf_path = (Path("data") / "inquiry" / "pdf" / f"{doc_id}.pdf").as_posix()
        detail_url = (
            f"{CNINFO_DETAIL_BASE}?stockCode={annual_code}"
            f"&announcementId={announcement_id}"
        )

        return {
            "annual_doc_id": annual_record.get("doc_id", ""),
            "report_year": report_year,
            "query_window_start": annual_record.get("publish_date", "")[:10],
            "query_window_end": self._query_window_end(annual_record),
            "doc_id": doc_id,
            "stock_code": annual_code,
            "stock_name": stock_name,
            "market": market,
            "announcement_id": announcement_id,
            "announcement_title": title,
            "announcement_type": announcement_type,
            "document_role": document_role,
            "publish_date": publish_date,
            "url": detail_url,
            "pdf_url": pdf_url,
            "local_pdf_path": local_pdf_path,
            "download_status": "pending",
            "pdf_title": "",
            "pdf_title_status": "",
            "title_match_status": "",
            "source": "cninfo_frontend_inquiry",
            "crawl_time": datetime.now().isoformat(),
            "error_message": "",
            "notes": "",
        }

    def _publish_date(self, item: dict[str, Any]) -> str:
        value = item.get("announcementTime", "")
        if isinstance(value, int):
            return datetime.fromtimestamp(value / 1000, tz=CNINFO_TZ).strftime("%Y-%m-%d")
        text = str(value)
        if len(text) >= 10:
            return text[:10]
        return ""

    def _pdf_url(self, adjunct_url: str) -> str:
        if adjunct_url.startswith("http://") or adjunct_url.startswith("https://"):
            return adjunct_url
        return f"{CNINFO_DOWNLOAD_BASE}{adjunct_url.lstrip('/')}"

    def _report_year(self, annual_record: dict[str, str]) -> str:
        title = annual_record.get("announcement_title", "")
        match = re.search(r"(\d{4})年年度报告", title)
        if match:
            return match.group(1)
        return str(report_year_from_publish_date(annual_record["publish_date"]))

    def _query_window_end(self, annual_record: dict[str, str]) -> str:
        start = annual_record.get("publish_date", "")[:10]
        return add_days(start, 180).strftime("%Y-%m-%d")

    def _reset_discovery_outputs(self) -> None:
        if self.candidates_path.exists():
            self.candidates_path.unlink()
        if self.cache_path.exists():
            self.cache_path.unlink()

    def _load_cache(self) -> set[str]:
        if not self.cache_path.exists():
            return set()
        with self.cache_path.open("r", encoding="utf-8") as f:
            return set(json.load(f))

    def _save_cache(self, completed: set[str]) -> None:
        with self.cache_path.open("w", encoding="utf-8") as f:
            json.dump(sorted(completed), f, ensure_ascii=False, indent=2)

    def _read_existing_candidates(self) -> list[dict[str, str]]:
        if not self.candidates_path.exists():
            return []
        with self.candidates_path.open("r", encoding="utf-8", newline="") as f:
            return [self._normalize_candidate_row(row) for row in csv.DictReader(f)]

    def _seen_candidate_keys(self, rows: list[dict[str, str]]) -> set[str]:
        return {
            row.get("announcement_id") or row.get("pdf_url", "")
            for row in rows
            if row.get("announcement_id") or row.get("pdf_url")
        }

    def _ensure_candidates_file(self, rows: list[dict[str, str]]) -> None:
        if not self.candidates_path.exists():
            self._write_candidates(rows)
            return
        with self.candidates_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames == INQUIRY_METADATA_COLUMNS:
                return
        self._write_candidates(rows)

    def _write_candidates(self, rows: list[dict[str, str]]) -> None:
        with self.candidates_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=INQUIRY_METADATA_COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow(self._normalize_candidate_row(row))

    def _append_candidates(self, rows: list[dict[str, str]]) -> None:
        file_exists = self.candidates_path.exists()
        with self.candidates_path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=INQUIRY_METADATA_COLUMNS)
            if not file_exists:
                writer.writeheader()
            for row in rows:
                writer.writerow(self._normalize_candidate_row(row))

    def _normalize_candidate_row(self, row: dict[str, str]) -> dict[str, str]:
        return {column: row.get(column, "") for column in INQUIRY_METADATA_COLUMNS}

    def _append_log(self, entry: dict[str, Any]) -> None:
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _write_log(self, logs: list[dict[str, Any]]) -> None:
        with self.log_path.open("a", encoding="utf-8") as f:
            for entry in logs:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _print_progress(
        self,
        index: int,
        total: int,
        annual_record: dict[str, str],
        report_year: str,
        raw_count: int,
        parsed_count: int,
        elapsed_seconds: float,
        skipped: bool = False,
    ) -> None:
        avg = elapsed_seconds / index if index else 0
        eta = max(total - index, 0) * avg
        status = "resume-skip" if skipped else "done"
        print(
            "[inquiry] "
            f"{index}/{total} {status} "
            f"{annual_record.get('stock_code', '')} "
            f"{annual_record.get('stock_name', '')} "
            f"{report_year} "
            f"raw={raw_count} parsed={parsed_count} "
            f"elapsed={elapsed_seconds:.1f}s eta={eta:.1f}s",
            flush=True,
        )


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    crawler = InquiryCrawler()
    path = crawler.run(discover_only=True)
    print(f"\n✅ 问询候选发现完成: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
