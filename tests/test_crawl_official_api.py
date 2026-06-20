"""Tests for CNINFO official API crawler."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests

import src.crawl.cninfo_official_api as official_module
from src.crawl._common import generate_human_doc_id
from src.crawl.cninfo_official_api import CninfoOfficialCrawler


def test_generate_human_doc_id() -> None:
    """人可读 doc_id 应包含股票代码、公司简称与报告年度。"""
    assert generate_human_doc_id("600276", "恒瑞医药", "2022-04-23") == "600276_恒瑞医药_2021年报"
    assert generate_human_doc_id("300760", "迈瑞医疗", "2022-04-20") == "300760_迈瑞医疗_2021年报"


@pytest.fixture
def crawler(tmp_path: Path, monkeypatch) -> CninfoOfficialCrawler:
    """构造一个使用临时目录的官方 API crawler。"""
    monkeypatch.setenv("CNINFO_ACCESS_KEY", "test_ak")
    monkeypatch.setenv("CNINFO_ACCESS_SECRET", "test_as")
    monkeypatch.setattr(official_module, "load_env", lambda: None)
    monkeypatch.setattr(
        official_module,
        "load_config",
        lambda _path: {
            "companies": [{"name": "恒瑞医药", "code": "600276"}],
            "years": [2021, 2022, 2023],
            "cninfo_official_api": {
                "delay_seconds": 0,
                "max_retries": 1,
                "page_size": 100,
                "token_cache_path": "data/cninfo_official_token.json",
            },
            "download": {"delay_seconds": 0, "max_retries": 1},
        },
    )

    c = CninfoOfficialCrawler()
    # 重定向到临时目录，避免污染项目数据
    c.metadata_path = tmp_path / "metadata.csv"
    c.cache_path = tmp_path / "crawl_cache.json"
    c.log_path = tmp_path / "crawl_log.jsonl"
    c.progress_path = tmp_path / "crawl_progress.json"
    c.token_cache_path = tmp_path / "token.json"
    return c


def test_infer_market_shared() -> None:
    """复用的市场推断逻辑应保持不变。"""
    from src.crawl._common import infer_market

    assert infer_market("600276") == ("sh", "sse", "sh")
    assert infer_market("000001") == ("sz", "szse", "sz")
    assert infer_market("688981") == ("sh", "sse", "sh")
    assert infer_market("430047") == ("bj", "bse", "bj")


def test_select_best_candidate_prefers_exact_year(crawler: CninfoOfficialCrawler) -> None:
    """优先选择标题完全匹配当年年报的记录。"""
    records = [
        {
            "F002V": "恒瑞医药：恒瑞医药2021年半年度报告",
            "F003V": "http://static.cninfo.com.cn/a.pdf",
            "F001D": "2021-08-20 00:00:00",
        },
        {
            "F002V": "恒瑞医药：恒瑞医药2021年年度报告",
            "F003V": "http://static.cninfo.com.cn/b.pdf",
            "F001D": "2022-04-23 00:00:00",
        },
        {
            "F002V": "恒瑞医药：恒瑞医药关于药品注册进度的提示性公告",
            "F003V": "http://static.cninfo.com.cn/c.pdf",
            "F001D": "2022-01-04 00:00:00",
        },
    ]
    best = crawler._select_best_candidate(records, "恒瑞医药", "2021")
    assert best is not None
    assert "2021年年度报告" in best["F002V"]


def test_select_best_candidate_skips_abstract(crawler: CninfoOfficialCrawler) -> None:
    """排除摘要和修订版。"""
    records = [
        {
            "F002V": "恒瑞医药：恒瑞医药2021年年度报告摘要",
            "F003V": "http://static.cninfo.com.cn/abstract.pdf",
            "F001D": "2022-04-23 00:00:00",
        },
    ]
    assert crawler._select_best_candidate(records, "恒瑞医药", "2021") is None


def test_select_best_candidate_skips_sponsor_supervision_report(
    crawler: CninfoOfficialCrawler,
) -> None:
    """排除持续督导报告，避免把保荐机构文件当作公司年报。"""
    records = [
        {
            "F002V": "韦尔股份：平安证券股份有限公司关于上海韦尔半导体股份有限公司2021年度持续督导年度报告书",
            "F003V": "http://static.cninfo.com.cn/sponsor.pdf",
            "F001D": "2022-04-19 00:00:00",
        },
        {
            "F002V": "韦尔股份：2021年年度报告",
            "F003V": "http://static.cninfo.com.cn/annual.pdf",
            "F001D": "2022-04-19 00:00:00",
        },
    ]

    best = crawler._select_best_candidate(records, "韦尔股份", "2021")

    assert best is not None
    assert best["F003V"].endswith("annual.pdf")


def test_select_best_candidate_returns_none_for_only_sponsor_report(
    crawler: CninfoOfficialCrawler,
) -> None:
    """只有持续督导报告时应返回 None，而不是误当年报。"""
    records = [
        {
            "F002V": "韦尔股份：平安证券股份有限公司关于上海韦尔半导体股份有限公司2021年度持续督导年度报告书",
            "F003V": "http://static.cninfo.com.cn/sponsor.pdf",
            "F001D": "2022-04-19 00:00:00",
        },
    ]

    assert crawler._select_best_candidate(records, "韦尔股份", "2021") is None


def test_refresh_token_success(crawler: CninfoOfficialCrawler, monkeypatch) -> None:
    """token 刷新成功时更新内存状态与缓存文件。"""
    fake_resp = MagicMock()
    fake_resp.raise_for_status = MagicMock()
    fake_resp.json.return_value = {
        "access_token": "test_token_xyz",
        "expires_in": 3599,
    }
    monkeypatch.setattr(requests, "post", lambda _url, **_kwargs: fake_resp)

    token = crawler._refresh_token()
    assert token == "test_token_xyz"
    assert crawler._token == "test_token_xyz"
    assert crawler._token_expires_at is not None
    assert crawler.token_cache_path.exists()

    cached = json.loads(crawler.token_cache_path.read_text(encoding="utf-8"))
    assert cached["access_token"] == "test_token_xyz"


def test_search_company_year_maps_fields(
    crawler: CninfoOfficialCrawler, monkeypatch
) -> None:
    """成功获取公告后，字段应正确映射到 metadata 格式。"""

    def fake_call_api(_url: str, _params: dict) -> dict:
        return {
            "resultcode": 200,
            "records": [
                {
                    "F001D": "2022-04-23 00:00:00",
                    "F002V": "恒瑞医药：恒瑞医药2021年年度报告",
                    "F003V": "http://static.cninfo.com.cn/finalpage/2022-04-23/1213053755.PDF",
                    "SECCODE": "600276",
                    "SECNAME": "恒瑞医药",
                },
            ],
        }

    monkeypatch.setattr(crawler, "_call_api", fake_call_api)

    record = crawler._search_company_year("600276", "恒瑞医药", "2021")
    assert record is not None
    assert record["stock_code"] == "600276"
    assert record["stock_name"] == "恒瑞医药"
    assert record["market"] == "sh"
    assert record["announcement_title"].endswith("2021年年度报告")
    assert record["publish_date"] == "2022-04-23"
    assert record["pdf_url"].endswith(".PDF")
    assert record["source"] == "cninfo_official_api"
    assert record["download_status"] == "pending"
    assert record["doc_id"] == "600276_恒瑞医药_2021年报"
    assert record["local_pdf_path"] == "data/pdf/600276_恒瑞医药_2021年报.pdf"


def test_search_company_year_returns_none_when_empty(
    crawler: CninfoOfficialCrawler, monkeypatch
) -> None:
    """无公告记录时返回 None。"""
    monkeypatch.setattr(
        crawler, "_call_api", lambda _url, _params: {"resultcode": 200, "records": []}
    )
    assert crawler._search_company_year("600276", "恒瑞医药", "2021") is None


def test_call_api_refreshes_token_on_401(
    crawler: CninfoOfficialCrawler, monkeypatch
) -> None:
    """收到 401 时应自动刷新 token 并重试。"""
    crawler._token = "old_token"
    crawler._token_expires_at = None

    responses = []

    def fake_post(url: str, **_kwargs) -> MagicMock:
        resp = MagicMock()
        if "oauth2/token" in url:
            resp.raise_for_status = MagicMock()
            resp.json.return_value = {
                "access_token": "new_token",
                "expires_in": 3599,
            }
        else:
            # 第一次返回 401，第二次返回成功
            if len(responses) == 0:
                resp.status_code = 401
                resp.text = "unauthorized"
                resp.raise_for_status.side_effect = requests.HTTPError("401")
            else:
                resp.status_code = 200
                resp.raise_for_status = MagicMock()
                resp.json.return_value = {"resultcode": 200, "records": []}
            responses.append(resp)
        return resp

    monkeypatch.setattr(requests, "post", fake_post)

    result = crawler._call_api("http://webapi.cninfo.com.cn/api/info/p_info3015", {})
    assert result["resultcode"] == 200
    assert crawler._token == "new_token"
    assert len(responses) >= 2


def test_write_progress(crawler: CninfoOfficialCrawler) -> None:
    """进度文件应被正确写入。"""
    crawler._write_progress(total=150, success=140, failed=10, status="running")

    data = json.loads(crawler.progress_path.read_text(encoding="utf-8"))
    assert data["backend"] == "official_api"
    assert data["total"] == 150
    assert data["success"] == 140
    assert data["failed"] == 10
    assert data["status"] == "running"
    assert "updated_at" in data


def test_preflight_success(crawler: CninfoOfficialCrawler, monkeypatch) -> None:
    """预检通过时 token 和样例请求都应成功。"""

    def fake_refresh_token() -> str:
        crawler._token = "test_token"
        crawler._token_expires_at = datetime.now() + timedelta(hours=1)
        return "test_token"

    def fake_call_api(url: str, _params: dict) -> dict:
        assert "p_info3015" in url
        return {"resultcode": 200, "total": 5, "records": []}

    monkeypatch.setattr(crawler, "_refresh_token", fake_refresh_token)
    monkeypatch.setattr(crawler, "_call_api", fake_call_api)

    crawler.preflight()
    assert crawler._token == "test_token"


def test_preflight_missing_credentials(monkeypatch) -> None:
    """未设置凭证时应抛出 RuntimeError。"""
    monkeypatch.setenv("CNINFO_ACCESS_KEY", "")
    monkeypatch.setenv("CNINFO_ACCESS_SECRET", "")
    monkeypatch.setattr(official_module, "load_env", lambda: None)
    monkeypatch.setattr(
        official_module,
        "load_config",
        lambda _path: {
            "companies": [],
            "years": [],
            "cninfo_official_api": {},
        },
    )

    with pytest.raises(RuntimeError, match="CNINFO_ACCESS_KEY"):
        CninfoOfficialCrawler()


def test_failure_rate_circuit_breaker(
    crawler: CninfoOfficialCrawler, monkeypatch
) -> None:
    """失败率超过阈值时应自动熔断。"""
    crawler.companies = [
        {"name": "A", "code": "600001"},
        {"name": "B", "code": "600002"},
    ]
    crawler.years = [2021]
    crawler.max_failure_rate = 0.1  # 10% 阈值

    monkeypatch.setattr(
        crawler, "_search_company_year", lambda _code, _name, _year: None
    )
    monkeypatch.setattr(crawler, "preflight", lambda: None)

    with pytest.raises(RuntimeError, match="失败率"):
        crawler.run()

    progress = json.loads(crawler.progress_path.read_text(encoding="utf-8"))
    assert progress["failed"] == 2
    assert progress["status"] == "failed"
