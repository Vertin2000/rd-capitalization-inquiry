"""数据质量审计器

检查 metadata 与 PDF 的对应关系，生成审计报告。

Usage:
    from src.audit.auditor import DataAuditor
    auditor = DataAuditor()
    auditor.run()

讲义依据: Week 12 Lab §5.6 — 数据质量检查
"""

from __future__ import annotations

import csv
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

MIN_FILE_SIZE = 100 * 1024
PDF_MAGIC = b"%PDF"
REQUIRED_KEYWORDS = ["年报", "年度报告"]


class DataAuditor:
    """数据质量审计器

    检查项（对齐讲义 Lab §5.6）：
    1. metadata.csv 非空
    2. 是否有重复 doc_id
    3. metadata 中记录的文件是否真的存在
    4. 标题是否包含选题关键词
    5. 下载失败是否写入日志
    6. PDF 文件完整性（大小 + 魔数）
    """

    def __init__(
        self,
        metadata_path: str = "data/metadata/metadata.csv",
        pdf_dir: str = "data/pdf",
        report_path: str = "outputs/dataset_check_report.md",
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.metadata_path = self.project_root / metadata_path
        self.pdf_dir = self.project_root / pdf_dir
        self.report_path = self.project_root / report_path
        self.report_path.parent.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, local_path: str) -> Path:
        """解析 local_pdf_path：相对路径基于 project_root，绝对路径原样使用。"""
        path = Path(local_path)
        if not path.is_absolute():
            return self.project_root / path
        return path

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def run(self) -> dict[str, Any]:
        """执行审计，返回检查结果，同时生成 Markdown 报告。"""
        logger.info("开始数据质量审计...")

        issues: list[dict[str, Any]] = []

        # 1. metadata 存在且非空
        records = self._read_metadata()
        if not records:
            issues.append({
                "check": "metadata_non_empty",
                "status": "FAIL",
                "detail": "metadata.csv 为空或不存在",
            })
            self._write_report(issues, 0, 0)
            logger.error("metadata.csv 为空或不存在")
            return {"passed": False, "issues": issues}

        total = len(records)
        issues.append({
            "check": "metadata_non_empty",
            "status": "PASS",
            "detail": f"metadata.csv 共 {total} 条记录",
        })

        # 2. 无重复 doc_id
        doc_ids = [r["doc_id"] for r in records]
        duplicates = self._find_duplicates(doc_ids)
        if duplicates:
            issues.append({
                "check": "no_duplicate_doc_id",
                "status": "FAIL",
                "detail": f"发现 {len(duplicates)} 个重复 doc_id: {duplicates[:5]}",
            })
        else:
            issues.append({
                "check": "no_duplicate_doc_id",
                "status": "PASS",
                "detail": "所有 doc_id 唯一",
            })

        # 3. PDF 文件存在性 + 完整性
        pdf_exists = 0
        pdf_missing = 0
        pdf_corrupted = 0
        for record in records:
            local_path = record.get("local_pdf_path", "")
            if not local_path:
                pdf_missing += 1
                continue
            path = self._resolve_path(local_path)
            if not path.exists():
                pdf_missing += 1
                continue
            if path.stat().st_size < MIN_FILE_SIZE:
                pdf_corrupted += 1
                continue
            with open(path, "rb") as f:
                if f.read(4) != PDF_MAGIC:
                    pdf_corrupted += 1
                    continue
            pdf_exists += 1

        if pdf_missing > 0:
            issues.append({
                "check": "pdf_exists",
                "status": "FAIL",
                "detail": f"{pdf_missing} 个 PDF 文件缺失",
            })
        else:
            issues.append({
                "check": "pdf_exists",
                "status": "PASS",
                "detail": f"所有 {pdf_exists} 个 PDF 文件存在",
            })

        if pdf_corrupted > 0:
            issues.append({
                "check": "pdf_integrity",
                "status": "FAIL",
                "detail": f"{pdf_corrupted} 个 PDF 文件损坏（大小或魔数异常）",
            })
        else:
            issues.append({
                "check": "pdf_integrity",
                "status": "PASS",
                "detail": "所有 PDF 文件完整性校验通过",
            })

        # 4. 标题包含关键词
        title_mismatch = 0
        for record in records:
            title = record.get("announcement_title", "")
            if not any(kw in title for kw in REQUIRED_KEYWORDS):
                title_mismatch += 1

        if title_mismatch > 0:
            issues.append({
                "check": "title_keywords",
                "status": "WARN",
                "detail": f"{title_mismatch} 条记录标题不含关键词 {REQUIRED_KEYWORDS}",
            })
        else:
            issues.append({
                "check": "title_keywords",
                "status": "PASS",
                "detail": "所有标题包含必要关键词",
            })

        # 5. download_status 覆盖
        status_counts: dict[str, int] = {}
        missing_status = 0
        for record in records:
            status = record.get("download_status", "")
            if not status:
                missing_status += 1
            else:
                status_counts[status] = status_counts.get(status, 0) + 1

        if missing_status > 0:
            issues.append({
                "check": "download_status",
                "status": "FAIL",
                "detail": f"{missing_status} 条记录缺少 download_status",
            })
        else:
            issues.append({
                "check": "download_status",
                "status": "PASS",
                "detail": f"download_status 覆盖完整: {status_counts}",
            })

        # 6. error_message 规范（成功时为空，失败时非空）
        bad_errors = 0
        for record in records:
            status = record.get("download_status", "")
            error = record.get("error_message", "")
            if status == "success" and error:
                bad_errors += 1
            elif status == "failed" and not error:
                bad_errors += 1

        if bad_errors > 0:
            issues.append({
                "check": "error_message",
                "status": "WARN",
                "detail": f"{bad_errors} 条记录 error_message 与 download_status 不一致",
            })
        else:
            issues.append({
                "check": "error_message",
                "status": "PASS",
                "detail": "error_message 与 download_status 一致",
            })

        # 7. PDF SHA256 唯一性（直接检测 hash 碰撞）
        hash_to_docs: dict[str, list[str]] = {}
        for record in records:
            if record.get("download_status") != "success":
                continue
            local_path = record.get("local_pdf_path", "")
            if not local_path:
                continue
            path = self._resolve_path(local_path)
            if not path.exists():
                continue
            sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
            hash_to_docs.setdefault(sha256, []).append(record["doc_id"])

        collisions = {h: docs for h, docs in hash_to_docs.items() if len(docs) > 1}
        if collisions:
            issues.append({
                "check": "pdf_hash_unique",
                "status": "FAIL",
                "detail": f"发现 {len(collisions)} 组 hash 碰撞: {list(collisions.values())[:3]}",
            })
        else:
            issues.append({
                "check": "pdf_hash_unique",
                "status": "PASS",
                "detail": f"所有 PDF SHA256 唯一（共 {len(hash_to_docs)} 个）",
            })

        passed = sum(1 for i in issues if i["status"] == "FAIL") == 0
        self._write_report(issues, total, pdf_exists)

        logger.info(
            "审计完成: total=%d, pdf_exists=%d, passed=%s",
            total, pdf_exists, passed,
        )
        return {"passed": passed, "issues": issues}

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _read_metadata(self) -> list[dict[str, str]]:
        """读取 metadata.csv。"""
        if not self.metadata_path.exists():
            return []
        with open(self.metadata_path, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _find_duplicates(items: list[str]) -> list[str]:
        """查找重复项。"""
        seen = set()
        dupes = set()
        for item in items:
            if item in seen:
                dupes.add(item)
            seen.add(item)
        return list(dupes)

    def _write_report(
        self, issues: list[dict[str, Any]], total: int, pdf_count: int
    ) -> None:
        """生成 Markdown 审计报告。"""
        lines = [
            "# 数据质量审计报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            f"metadata 记录数: {total}",
            f"PDF 文件数: {pdf_count}",
            "",
            "## 检查项汇总",
            "",
            "| 检查项 | 状态 | 说明 |",
            "|--------|------|------|",
        ]

        for issue in issues:
            icon = "✅" if issue["status"] == "PASS" else "⚠️" if issue["status"] == "WARN" else "❌"
            lines.append(
                f"| {issue['check']} | {icon} {issue['status']} | {issue['detail']} |"
            )

        fail_count = sum(1 for i in issues if i["status"] == "FAIL")
        warn_count = sum(1 for i in issues if i["status"] == "WARN")

        lines.extend([
            "",
            "## 结论",
            "",
        ])

        if fail_count == 0 and warn_count == 0:
            lines.append("✅ **全部检查通过**，数据质量合格。")
        elif fail_count == 0:
            lines.append(f"⚠️ 无致命错误，但有 {warn_count} 项警告，建议关注。")
        else:
            lines.append(f"❌ 发现 {fail_count} 项致命错误，{warn_count} 项警告，数据质量不合格。")

        lines.append("")

        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        logger.info("审计报告已生成: %s", self.report_path)


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    auditor = DataAuditor()
    result = auditor.run()
    passed = result["passed"]
    print(f"\n{'✅' if passed else '❌'} 审计结果: {'通过' if passed else '未通过'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
