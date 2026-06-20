"""crawl 模块共享工具函数

供前端 AJAX crawler 与官方 API crawler 复用，避免重复实现。
"""

from __future__ import annotations

import hashlib


METADATA_COLUMNS = [
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
]


def infer_market(code: str) -> tuple[str, str, str]:
    """根据股票代码推断市场。

    Args:
        code: 6 位股票代码。

    Returns:
        (market, column, plate)
        - market: sh / sz / bj
        - column: sse / szse / bjse
        - plate: sh / sz / bj
    """
    if code.startswith("60") or code.startswith("688"):
        return "sh", "sse", "sh"
    if code.startswith("00") or code.startswith("30"):
        return "sz", "szse", "sz"
    if code.startswith("8") or code.startswith("4"):
        return "bj", "bse", "bj"
    return "sh", "sse", "sh"  # 默认沪市


def generate_doc_id(code: str, publish_date: str, title: str) -> str:
    """生成文档唯一标识。

    格式: {stock_code}_{publish_date}_{title_hash前8位}
    """
    title_hash = hashlib.sha256(title.encode("utf-8")).hexdigest()[:8]
    return f"{code}_{publish_date}_{title_hash}"


def report_year_from_publish_date(publish_date: str) -> int:
    """根据披露日期推断所属会计年度。

    年报在下一自然年披露，因此 report_year = publish_year - 1。
    """
    publish_year = int(str(publish_date)[:4])
    return publish_year - 1


def generate_human_doc_id(code: str, name: str, publish_date: str) -> str:
    """生成人可读的文档唯一标识，同时用作 PDF 文件名 stem。

    格式: {stock_code}_{stock_name}_{report_year}年报
    """
    year = report_year_from_publish_date(publish_date)
    return f"{code}_{name}_{year}年报"
