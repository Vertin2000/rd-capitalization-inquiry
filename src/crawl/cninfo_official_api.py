"""深证信（巨潮）官方 API 年报公告查询封装

通过 OAuth2 client_credentials 获取 access_token，
调用 `p_info3015`（公告基本信息）获取年报 PDF URL，
输出与前端 AJAX crawler 兼容的 metadata.csv。

Usage:
    from src.crawl.cninfo_official_api import CninfoOfficialCrawler
    crawler = CninfoOfficialCrawler("configs/crawl.yaml")
    crawler.run()
"""

from __future__ import annotations

import csv
import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests
from tqdm import tqdm

from src.common import load_config, load_env
from src.crawl._common import (
    METADATA_COLUMNS,
    generate_human_doc_id,
    infer_market,
)

logger = logging.getLogger(__name__)

CNINFO_BASE_URL = "http://webapi.cninfo.com.cn"
CNINFO_TOKEN_URL = f"{CNINFO_BASE_URL}/api-cloud-platform/oauth2/token"
CNINFO_P_INFO3015_URL = f"{CNINFO_BASE_URL}/api/info/p_info3015"
CNINFO_P_INFO3005_URL = f"{CNINFO_BASE_URL}/api/info/p_info3005"
CNINFO_DOWNLOAD_BASE = "http://static.cninfo.com.cn/"
ANNUAL_REPORT_TITLE_EXCLUDE_KEYWORDS = (
    "摘要",
    "半年度报告",
    "季度报告",
    "持续督导",
    "保荐",
    "核查",
    "专项",
    "独立意见",
    "监管工作函",
    "问询函",
    "回复",
    "更正",
    "提示性公告",
)


class CninfoOfficialCrawler:
    """深证信官方 API 年报公告爬虫。

    支持：
    - 从 .env 读取 AccessKey / AccessSecret
    - OAuth2 token 自动获取与过期刷新
    - 断点续传与指数退避重试
    """

    def __init__(self, config_path: str = "configs/crawl.yaml", limit: int | None = None) -> None:
        load_env()
        self.config = load_config(config_path)
        self.companies: list[dict[str, str]] = self.config["companies"]
        self.years: list[int] = self.config["years"]

        official_cfg = self.config.get("cninfo_official_api", {})
        self.delay_seconds: float = official_cfg.get("delay_seconds", 3.0)
        self.max_retries: int = official_cfg.get("max_retries", 3)
        self.page_size: int = official_cfg.get("page_size", 100)
        self.max_failure_rate: float = official_cfg.get("max_failure_rate", 0.15)
        self.token_cache_path: Path | None = None
        if official_cfg.get("token_cache_path"):
            self.token_cache_path = (
                Path(__file__).resolve().parent.parent.parent
                / official_cfg["token_cache_path"]
            )

        self.access_key: str | None = os.getenv("CNINFO_ACCESS_KEY")
        self.access_secret: str | None = os.getenv("CNINFO_ACCESS_SECRET")
        if not self.access_key or not self.access_secret:
            raise RuntimeError(
                "CNINFO_ACCESS_KEY / CNINFO_ACCESS_SECRET 未设置，"
                "请检查 .env 文件"
            )

        self.limit: int | None = limit

        # 项目路径
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.metadata_path = self.project_root / "data" / "metadata" / "metadata.csv"
        self.cache_path = self.project_root / "data" / "crawl_cache_official.json"
        self.log_path = self.project_root / "outputs" / "logs" / "crawl_log.jsonl"
        self.progress_path = self.project_root / "outputs" / "crawl_progress.json"

        # 确保目录存在
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.progress_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if self.token_cache_path:
            self.token_cache_path.parent.mkdir(parents=True, exist_ok=True)

        # 断点续传缓存
        self.cache: set[str] = self._load_cache()

        # token 状态
        self._token: str | None = None
        self._token_expires_at: datetime | None = None

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def preflight(self) -> None:
        """起飞前检查：验证凭证、token、网络和一个样例请求。"""
        logger.info("=== 官方 API 预检开始 ===")

        # 1. 凭证
        if not self.access_key or not self.access_secret:
            raise RuntimeError("CNINFO_ACCESS_KEY / CNINFO_ACCESS_SECRET 未设置")
        logger.info("✅ 凭证已配置")

        # 2. token 接口
        try:
            token = self._refresh_token()
            logger.info("✅ OAuth2 token 接口正常，token 长度=%d", len(token))
        except Exception as e:
            raise RuntimeError(f"OAuth2 token 获取失败: {e}") from e

        # 3. 样例请求：用恒瑞医药 2023 年报做探测
        try:
            sample = self._call_api(
                CNINFO_P_INFO3015_URL,
                {
                    "scode": "600276",
                    "sdate": "20240101",
                    "edate": "20241231",
                    "pageNum": 1,
                    "pageSize": 10,
                },
            )
            total = sample.get("total", 0)
            logger.info("✅ p_info3015 样例请求正常，返回记录数=%d", total)
        except Exception as e:
            raise RuntimeError(f"p_info3015 样例请求失败: {e}") from e

        logger.info("=== 官方 API 预检通过 ===")

    def run(self) -> Path:
        """执行完整爬虫流程，返回 metadata.csv 路径。"""
        self.preflight()

        companies = self.companies
        if self.limit is not None:
            companies = companies[: self.limit]
            logger.info("限制模式: 仅处理前 %d 家公司", self.limit)

        total_tasks = len(companies) * len(self.years)
        results: list[dict[str, Any]] = []
        crawl_log: list[dict[str, Any]] = []
        failures = 0

        logger.info(
            "开始爬取深证信官方 API 年报数据: 公司=%d, 年份=%s, 总任务=%d",
            len(companies),
            self.years,
            total_tasks,
        )

        with tqdm(
            total=total_tasks,
            desc="官方 API 年报抓取",
            unit="条",
            ncols=80,
        ) as pbar:
            for year in self.years:
                year_str = str(year)
                year_results, year_failures = self._crawl_year(year_str, companies, pbar)
                results.extend(year_results)
                failures += year_failures

                crawl_log.append({
                    "year": year_str,
                    "companies_crawled": len(companies),
                    "records_found": len(year_results),
                    "failures": year_failures,
                    "crawl_time": datetime.now().isoformat(),
                    "status": "success" if year_results else "empty",
                    "backend": "official_api",
                })
                logger.info(
                    "%s年: 获取 %d 条, 失败 %d 条",
                    year_str, len(year_results), year_failures,
                )

                # 跨年份也要检查失败率
                processed = len(results) + failures
                if processed > 0 and failures / processed > self.max_failure_rate:
                    self._write_progress(total_tasks, len(results), failures, "failed")
                    raise RuntimeError(
                        f"失败率 {failures / processed:.1%} 超过阈值 "
                        f"{self.max_failure_rate:.1%}，自动中止"
                    )

        self._write_metadata(results)
        self._write_log(crawl_log)
        self._write_progress(total_tasks, len(results), failures, "completed")
        logger.info(
            "爬虫完成: metadata.csv 共 %d 条记录, 失败 %d 条",
            len(results), failures,
        )
        return self.metadata_path

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _crawl_year(
        self,
        year: str,
        companies: list[dict[str, str]] | None = None,
        pbar: tqdm | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        """爬取指定年份的所有公司年报。

        Returns:
            (results, failure_count)
        """
        if companies is None:
            companies = self.companies

        results: list[dict[str, Any]] = []
        failures = 0

        for company in companies:
            code = company["code"]
            cache_key = f"{code}_{year}"

            if cache_key in self.cache:
                logger.debug("跳过已缓存: %s", cache_key)
                if pbar:
                    pbar.update(1)
                continue

            record = self._search_company_year(code, company["name"], year)

            if record:
                results.append(record)
                self.cache.add(cache_key)
                self._save_cache()
            else:
                failures += 1
                logger.warning("未找到 %s %s年 年报", code, year)

            if pbar:
                pbar.update(1)
                pbar.set_postfix({
                    "year": year,
                    "ok": len(results),
                    "fail": failures,
                })

            time.sleep(self.delay_seconds)

        return results, failures

    def _search_company_year(
        self, code: str, name: str, year: str
    ) -> dict[str, Any] | None:
        """通过官方 API 搜索单家公司指定年份的年报。"""
        market, _, _ = infer_market(code)
        search_year = str(int(year) + 1)

        params = {
            "scode": code,
            "sdate": f"{search_year}0101",
            "edate": f"{search_year}1231",
            "pageNum": 1,
            "pageSize": self.page_size,
        }

        for attempt in range(self.max_retries):
            try:
                result = self._call_api(CNINFO_P_INFO3015_URL, params)

                records = result.get("records", [])
                if not records:
                    return None

                candidate = self._select_best_candidate(records, name, year)
                if candidate is None:
                    return None

                title = candidate.get("F002V", "")
                pdf_url = candidate.get("F003V", "")
                publish_date = str(candidate.get("F001D", ""))[:10]
                doc_id = generate_human_doc_id(code, name, publish_date)
                local_pdf_path = (Path("data") / "pdf" / f"{doc_id}.pdf").as_posix()

                return {
                    "doc_id": doc_id,
                    "stock_code": code,
                    "stock_name": name,
                    "market": market,
                    "announcement_title": title,
                    "announcement_type": "年度报告",
                    "publish_date": publish_date,
                    "url": pdf_url,
                    "pdf_url": pdf_url,
                    "local_pdf_path": local_pdf_path,
                    "download_status": "pending",
                    "source": "cninfo_official_api",
                    "crawl_time": datetime.now().isoformat(),
                    "error_message": "",
                    "notes": "",
                }

            except requests.RequestException as e:
                wait = 2 ** attempt
                logger.warning(
                    "官方 API 请求失败 %s %s (尝试 %d/%d): %s, %ds 后重试",
                    code, year, attempt + 1, self.max_retries, e, wait,
                )
                time.sleep(wait)

        logger.error("%s %s年 重试耗尽，放弃", code, year)
        return None

    def _select_best_candidate(
        self, records: list[dict[str, Any]], name: str, year: str
    ) -> dict[str, Any] | None:
        """从 p_info3015 返回记录中选出最佳年报。"""
        candidates = []
        for item in records:
            title = item.get("F002V", "")
            if "年度报告" not in title:
                continue
            if any(
                keyword in title
                for keyword in ANNUAL_REPORT_TITLE_EXCLUDE_KEYWORDS
            ):
                continue
            pdf_url = item.get("F003V", "")
            if not pdf_url:
                continue

            score = 1
            if name in title:
                score = 2
            if title == f"{name}：{name}{year}年年度报告":
                score = 4
            elif title.endswith(f"{year}年年度报告"):
                score = 3

            candidates.append((score, item))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def _call_api(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        """调用官方 API，自动附加 access_token 并处理过期。"""
        token = self._ensure_token()
        full_url = f"{url}?access_token={token}"

        resp = requests.post(full_url, data=params, timeout=15)
        if resp.status_code == 401:
            logger.info("token 可能已过期，尝试刷新")
            self._refresh_token()
            token = self._ensure_token()
            full_url = f"{url}?access_token={token}"
            resp = requests.post(full_url, data=params, timeout=15)

        resp.raise_for_status()
        data = resp.json()

        # 业务级错误码
        if data.get("resultcode") not in (200, None):
            msg = data.get("resultmsg", "unknown")
            code = data.get("resultcode", "unknown")
            raise RuntimeError(f"官方 API 业务错误: code={code}, msg={msg}")

        return data

    def _ensure_token(self) -> str:
        """确保 token 有效并返回。"""
        if self._token and self._token_expires_at and datetime.now() < self._token_expires_at:
            return self._token
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """刷新 OAuth2 token。"""
        logger.info("正在刷新 CNINFO OAuth2 token")
        resp = requests.post(
            CNINFO_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.access_key,
                "client_secret": self.access_secret,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        self._token = data["access_token"]
        expires_in = data.get("expires_in", 3599)
        # 预留 60 秒缓冲
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
        logger.info("token 刷新成功，有效期约 %s 秒", expires_in)

        self._save_token_cache()
        return self._token

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

    def _save_token_cache(self) -> None:
        """保存 token 缓存到文件（不提交）。"""
        if not self.token_cache_path or not self._token or not self._token_expires_at:
            return
        with open(self.token_cache_path, "w", encoding="utf-8") as f:
            json.dump({
                "access_token": self._token,
                "expires_at": self._token_expires_at.isoformat(),
            }, f, ensure_ascii=False)

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

    def _write_progress(
        self,
        total: int,
        success: int,
        failed: int,
        status: str,
    ) -> None:
        """写入机器可读的进度文件，方便外部监控。"""
        with open(self.progress_path, "w", encoding="utf-8") as f:
            json.dump({
                "backend": "official_api",
                "total": total,
                "success": success,
                "failed": failed,
                "status": status,
                "updated_at": datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------- #
# CLI 入口（独立运行）
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    crawler = CninfoOfficialCrawler()
    metadata_path = crawler.run()
    print(f"\n✅ 官方 API 爬虫完成，metadata 写入: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
