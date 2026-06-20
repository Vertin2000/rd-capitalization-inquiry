"""PDF 下载器

从 metadata.csv 读取 pdf_url，下载年报 PDF 到 data/pdf/，
并进行完整性校验。

Usage:
    from src.download.downloader import PDFDownloader
    downloader = PDFDownloader()
    downloader.run()

讲义依据: Week 12 Lab §5.5 — PDF 下载与质量检查
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)

# 巨潮域名白名单
ALLOWED_DOMAINS = {"static.cninfo.com.cn", "www.cninfo.com.cn"}
MIN_FILE_SIZE = 100 * 1024  # 100KB
PDF_MAGIC = b"%PDF"
DEFAULT_TIMEOUT = 60


class PDFDownloader:
    """PDF 下载器

    特性：
    - 跳过已存在且校验通过的 PDF
    - URL 域名白名单
    - PDF 魔数 + 大小 + SHA256 校验
    - 更新 metadata.csv download_status
    - JSONL 下载日志
    """

    def __init__(
        self,
        metadata_path: str = "data/metadata/metadata.csv",
        pdf_dir: str = "data/pdf",
        log_path: str = "outputs/logs/download_log.jsonl",
        delay_seconds: float = 3.0,
        max_retries: int = 3,
        limit: int | None = None,
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.metadata_path = self.project_root / metadata_path
        self.pdf_dir = self.project_root / pdf_dir
        self.log_path = self.project_root / log_path
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.limit = limit

        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
        }

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def run(self) -> dict[str, int]:
        """执行批量下载，返回统计信息。"""
        if not self.metadata_path.exists():
            logger.error("metadata.csv 不存在: %s", self.metadata_path)
            raise FileNotFoundError(f"metadata.csv 不存在: {self.metadata_path}")

        records = self._read_metadata()
        if not records:
            logger.error("metadata.csv 为空")
            raise ValueError("metadata.csv 为空")

        all_records = records
        if self.limit is not None:
            records = all_records[: self.limit]
            logger.info("限制模式: 仅下载前 %d 条记录", self.limit)

        logger.info("开始下载 %d 份 PDF...", len(records))

        stats = {"success": 0, "failed": 0, "skipped": 0, "collision": 0}
        logs: list[dict[str, Any]] = []

        for record in tqdm(records, desc="下载 PDF", unit="份", ncols=80):
            doc_id = record["doc_id"]
            pdf_url = record.get("pdf_url", "")
            local_path = record.get("local_pdf_path", "")

            if not pdf_url or not local_path:
                logger.warning("[%s] 缺少 pdf_url 或 local_pdf_path，跳过", doc_id)
                record["download_status"] = "skipped"
                record["error_message"] = "缺少 pdf_url 或 local_pdf_path"
                stats["skipped"] += 1
                continue

            # 域名白名单
            if not self._is_allowed_domain(pdf_url):
                logger.warning("[%s] URL 不在白名单内: %s", doc_id, pdf_url)
                record["download_status"] = "skipped"
                record["error_message"] = f"URL 不在白名单: {pdf_url}"
                stats["skipped"] += 1
                continue

            # 检查是否已存在且有效
            existing = self._check_existing(local_path)
            if existing:
                logger.info("[%s] 已存在且有效，跳过", doc_id)
                record["download_status"] = "success"
                record["error_message"] = ""
                stats["success"] += 1
                continue

            # 下载
            success, file_size, sha256, error = self._download(
                pdf_url, local_path
            )

            if success:
                # Hash 碰撞检测
                collision_doc = self._check_hash_collision(sha256, doc_id)
                if collision_doc:
                    logger.warning(
                        "[%s] 发现 hash 碰撞 (与 %s 相同)",
                        doc_id, collision_doc,
                    )
                    record["notes"] = f"hash_collision_with:{collision_doc}"
                    stats["collision"] += 1

                record["download_status"] = "success"
                record["error_message"] = ""
                stats["success"] += 1
            else:
                record["download_status"] = "failed"
                record["error_message"] = error
                stats["failed"] += 1

            logs.append({
                "doc_id": doc_id,
                "pdf_url": pdf_url,
                "local_path": local_path,
                "status": record["download_status"],
                "file_size": file_size,
                "sha256": sha256,
                "error": error,
                "timestamp": datetime.now().isoformat(),
            })

            time.sleep(self.delay_seconds)

        self._write_metadata(all_records)
        self._write_log(logs)

        logger.info(
            "下载完成: success=%d, failed=%d, skipped=%d, collision=%d",
            stats["success"], stats["failed"], stats["skipped"],
            stats["collision"],
        )
        return stats

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _read_metadata(self) -> list[dict[str, str]]:
        """读取 metadata.csv。"""
        with open(self.metadata_path, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _write_metadata(self, records: list[dict[str, str]]) -> None:
        """回写 metadata.csv（更新 download_status）。"""
        if not records:
            return
        with open(
            self.metadata_path, "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            for record in records:
                writer.writerow(record)

    def _write_log(self, logs: list[dict[str, Any]]) -> None:
        """追加下载日志到 JSONL。"""
        with open(self.log_path, "a", encoding="utf-8") as f:
            for entry in logs:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _is_allowed_domain(self, url: str) -> bool:
        """检查 URL 域名是否在白名单内。"""
        try:
            domain = urlparse(url).netloc
            return domain in ALLOWED_DOMAINS
        except Exception:
            return False

    def _resolve_path(self, local_path: str) -> Path:
        """解析 local_pdf_path：相对路径基于 project_root，绝对路径原样使用。"""
        path = Path(local_path)
        if not path.is_absolute():
            return self.project_root / path
        return path

    def _check_existing(self, local_path: str) -> bool:
        """检查 PDF 是否已存在且有效。"""
        path = self._resolve_path(local_path)
        if not path.exists():
            return False
        if path.stat().st_size < MIN_FILE_SIZE:
            return False
        with open(path, "rb") as f:
            return f.read(4) == PDF_MAGIC

    def _download(
        self, url: str, local_path: str
    ) -> tuple[bool, int, str, str]:
        """下载单个 PDF。

        Returns:
            (success, file_size, sha256, error_message)
        """
        path = self._resolve_path(local_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(self.max_retries):
            try:
                resp = requests.get(
                    url,
                    headers=self.headers,
                    timeout=DEFAULT_TIMEOUT,
                    allow_redirects=True,
                )
                resp.raise_for_status()

                # 内容校验
                content = resp.content
                if not content[:4] == PDF_MAGIC:
                    return (
                        False,
                        0,
                        "",
                        f"非 PDF 文件 (magic={content[:4]})",
                    )

                # 写入文件
                with open(path, "wb") as f:
                    f.write(content)

                file_size = path.stat().st_size
                if file_size < MIN_FILE_SIZE:
                    path.unlink()
                    return (
                        False,
                        0,
                        "",
                        f"文件过小 ({file_size} bytes < {MIN_FILE_SIZE})",
                    )

                sha256 = hashlib.sha256(content).hexdigest()
                return True, file_size, sha256, ""

            except requests.RequestException as e:
                wait = 5 * (attempt + 1)
                logger.warning(
                    "下载失败 (尝试 %d/%d): %s, %ds 后重试",
                    attempt + 1,
                    self.max_retries,
                    e,
                    wait,
                )
                time.sleep(wait)

        return False, 0, "", f"重试 {self.max_retries} 次后仍失败"

    def _check_hash_collision(self, sha256: str, doc_id: str) -> str | None:
        """检查 hash 碰撞。

        遍历已下载的 PDF，如果发现相同 SHA256 但不同 doc_id，返回碰撞的 doc_id。
        """
        if not self.pdf_dir.exists():
            return None

        for pdf_path in self.pdf_dir.glob("*.pdf"):
            other_doc_id = pdf_path.stem
            if other_doc_id == doc_id:
                continue
            try:
                with open(pdf_path, "rb") as f:
                    other_hash = hashlib.sha256(f.read()).hexdigest()
                if other_hash == sha256:
                    return other_doc_id
            except Exception:
                continue
        return None


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    downloader = PDFDownloader()
    stats = downloader.run()
    print(f"\n✅ 下载完成: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
