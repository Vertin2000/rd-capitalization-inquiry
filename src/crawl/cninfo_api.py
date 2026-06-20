"""巨潮资讯网公告查询 API 封装

调用巨潮资讯网公开查询接口，按股票代码和年份搜索年报公告，
输出符合讲义规范的 metadata.csv。

Usage:
    from src.crawl.cninfo_api import CninfoCrawler
    crawler = CninfoCrawler("configs/crawl.yaml")
    crawler.run()

讲义依据: Week 12 §4.3 — metadata.csv 字段规范
"""

from __future__ import annotations

import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

from src.common import load_config
from src.crawl._common import (
    METADATA_COLUMNS,
    generate_doc_id,
    infer_market,
)

logger = logging.getLogger(__name__)

CNINFO_SEARCH_URL = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_DOWNLOAD_BASE = "http://static.cninfo.com.cn/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": (
        "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch"
        "?url=disclosure/list/search&lastPage=index"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}


class CninfoCrawler:
    """巨潮资讯网年报公告爬虫

    支持：
    - 按股票代码 + 年份批量查询
    - 自动判断市场（sh/sz/bj）
    - 断点续传（跳过已缓存的公司-年度组合）
    - 指数退避重试
    """

    def __init__(self, config_path: str = "configs/crawl.yaml", limit: int | None = None) -> None:
        self.config = load_config(config_path)
        self.companies: list[dict[str, str]] = self.config["companies"]
        self.years: list[int] = self.config["years"]
        self.delay_seconds: float = self.config.get("download", {}).get(
            "delay_seconds", 3.0
        )
        self.max_retries: int = self.config.get("download", {}).get("max_retries", 3)
        self.max_pages: int = 10
        self.limit: int | None = limit

        # 项目路径
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.metadata_path = self.project_root / "data" / "metadata" / "metadata.csv"
        self.cache_path = self.project_root / "data" / "crawl_cache.json"
        self.log_path = self.project_root / "outputs" / "logs" / "crawl_log.jsonl"

        # 确保目录存在
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        # 断点续传缓存
        self.cache: set[str] = self._load_cache()

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def run(self) -> Path:
        """执行完整爬虫流程，返回 metadata.csv 路径。"""
        logger.info(
            "开始爬取巨潮资讯网年报数据: 公司=%d, 年份=%s",
            len(self.companies),
            self.years,
        )

        # 如果指定了 limit，只取前 limit 家公司
        companies = self.companies
        if self.limit is not None:
            companies = companies[: self.limit]
            logger.info("限制模式: 仅处理前 %d 家公司", self.limit)

        results: list[dict[str, Any]] = []
        crawl_log: list[dict[str, Any]] = []

        for year in self.years:
            year_str = str(year)
            year_results = self._crawl_year(year_str, companies)
            results.extend(year_results)

            crawl_log.append({
                "year": year_str,
                "companies_crawled": len(companies),
                "records_found": len(year_results),
                "crawl_time": datetime.now().isoformat(),
                "status": "success" if year_results else "empty",
            })
            logger.info("%s年: 获取 %d 条记录", year_str, len(year_results))

        self._write_metadata(results)
        self._write_log(crawl_log)
        logger.info("爬虫完成: metadata.csv 共 %d 条记录", len(results))
        return self.metadata_path

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _crawl_year(self, year: str, companies: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
        """爬取指定年份的所有公司年报。"""
        if companies is None:
            companies = self.companies

        results: list[dict[str, Any]] = []

        for company in companies:
            code = company["code"]
            cache_key = f"{code}_{year}"

            if cache_key in self.cache:
                logger.debug("跳过已缓存: %s", cache_key)
                continue

            logger.info("搜索 %s年: %s - %s", year, code, company["name"])
            record = self._search_company_year(code, company["name"], year)

            if record:
                results.append(record)
                self.cache.add(cache_key)
                self._save_cache()
            else:
                logger.warning("未找到 %s %s年 年报", code, year)

            time.sleep(self.delay_seconds)

        return results

    def _search_company_year(
        self, code: str, name: str, year: str
    ) -> dict[str, Any] | None:
        """搜索单家公司指定年份的年报。"""
        market, column, plate = infer_market(code)
        # 年报在次年的 1-4 月披露，因此搜索 year+1 年的发布日期
        search_year = str(int(year) + 1)

        for attempt in range(self.max_retries):
            data = {
                "pageNum": "1",
                "pageSize": "30",
                "column": column,
                "tabName": "fulltext",
                "plate": plate,
                "stock": "",
                "searchkey": name,
                "secid": "",
                "category": "category_ndbg_szsh",
                "trade": "",
                "seDate": f"{search_year}-01-01~{search_year}-12-31",
                "sortName": "",
                "sortType": "",
                "isHLtitle": "true",
            }

            try:
                resp = requests.post(
                    CNINFO_SEARCH_URL,
                    data=data,
                    headers=HEADERS,
                    timeout=15,
                )
                resp.raise_for_status()
                result = resp.json()

                announcements = result.get("announcements", [])
                if not announcements:
                    return None

                # 清理标题中的高亮标签
                clean_name = name.replace("<em>", "").replace("</em>", "")
                candidates = []
                for item in announcements:
                    title = item.get("announcementTitle", "")
                    clean_title = title.replace("<em>", "").replace("</em>", "")
                    if "年度报告" not in clean_title or "摘要" in clean_title:
                        continue
                    adjunct_url = item.get("adjunctUrl", "")
                    if not adjunct_url:
                        continue
                    # 优先选择标题中包含公司名称的
                    score = 2 if clean_name in clean_title else 1
                    # 更优先选择完全匹配 "YYYY年年度报告" 的
                    if clean_title == f"{year}年年度报告":
                        score = 3
                    candidates.append((score, item))

                if not candidates:
                    return None

                # 按得分降序排列，选择最佳匹配
                candidates.sort(key=lambda x: x[0], reverse=True)
                best_item = candidates[0][1]
                title = best_item.get("announcementTitle", "")
                adjunct_url = best_item.get("adjunctUrl", "")
                pdf_url = f"{CNINFO_DOWNLOAD_BASE}{adjunct_url}"
                _announce_time = best_item.get("announcementTime", "")
                if isinstance(_announce_time, int):
                    from datetime import datetime as _dt
                    publish_date = _dt.fromtimestamp(_announce_time / 1000).strftime("%Y-%m-%d")
                else:
                    publish_date = str(_announce_time)[:10]  # YYYY-MM-DD
                doc_id = generate_doc_id(code, publish_date, title)
                local_pdf_path = (
                    self.project_root
                    / "data"
                    / "pdf"
                    / f"{doc_id}.pdf"
                )

                return {
                        "doc_id": doc_id,
                        "stock_code": code,
                        "stock_name": name,
                        "market": market,
                        "announcement_title": title,
                        "announcement_type": "category_ndbg_szsh",
                        "publish_date": publish_date,
                        "url": (
                            f"http://www.cninfo.com.cn/new/disclosure/detail"
                            f"?stockCode={code}&announcementId="
                            f"{item.get('announcementId', '')}"
                        ),
                        "pdf_url": pdf_url,
                        "local_pdf_path": str(local_pdf_path),
                        "download_status": "pending",
                        "source": "cninfo",
                        "crawl_time": datetime.now().isoformat(),
                        "error_message": "",
                        "notes": "",
                    }

            except requests.RequestException as e:
                wait = 2 ** attempt
                logger.warning(
                    "请求失败 %s %s (尝试 %d/%d): %s, %ds 后重试",
                    code, year, attempt + 1, self.max_retries, e, wait,
                )
                time.sleep(wait)

        logger.error("%s %s年 重试耗尽，放弃", code, year)
        return None

    # ------------------------------------------------------------------ #
    # 辅助方法
    # ------------------------------------------------------------------ #

    def _load_cache(self) -> set[str]:
        """加载断点续传缓存。"""
        if self.cache_path.exists():
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def _save_cache(self) -> None:
        """保存断点续传缓存。"""
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(list(self.cache), f, ensure_ascii=False)

    def _write_metadata(self, results: list[dict[str, Any]]) -> None:
        """写入 metadata.csv。"""
        with open(
            self.metadata_path, "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.DictWriter(f, fieldnames=METADATA_COLUMNS)
            writer.writeheader()
            for record in results:
                writer.writerow(record)

    def _write_log(self, crawl_log: list[dict[str, Any]]) -> None:
        """写入 crawl_log.jsonl。"""
        with open(self.log_path, "a", encoding="utf-8") as f:
            for entry in crawl_log:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------- #
# CLI 入口（独立运行）
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    crawler = CninfoCrawler()
    metadata_path = crawler.run()
    print(f"\n✅ 爬虫完成，metadata 写入: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
