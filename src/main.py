"""研发资本化分析项目 - CLI 入口

端到端 Pipeline 运行器，支持分阶段执行和断点续跑。

Usage:
    uv run python src/main.py --stage all
    uv run python src/main.py --stage crawl --limit 10
    uv run python src/main.py --from-stage crawl --to-stage audit
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 确保 src 在 Python 路径中（支持直接运行 python src/main.py）
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志（在导入模块前设置）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="研发资本化风险排序与问询函可行性测试 Pipeline",
    )
    parser.add_argument(
        "--stage",
        type=str,
        choices=[
            "crawl",
            "download",
            "audit",
            "parse",
            "route",
            "extract",
            "validate",
            "score",
            "detect",
            "inquiry",
            "inquiry-download",
            "inquiry-label",
            "analyze",
            "report",
            "all",
        ],
        help="要运行的阶段",
    )
    parser.add_argument(
        "--from-stage",
        type=str,
        choices=[
            "crawl",
            "download",
            "audit",
            "parse",
            "route",
            "extract",
            "validate",
            "score",
            "detect",
            "inquiry",
            "inquiry-download",
            "inquiry-label",
            "analyze",
            "report",
        ],
        help="起始阶段（利用已有中间结果）",
    )
    parser.add_argument(
        "--to-stage",
        type=str,
        choices=[
            "crawl",
            "download",
            "audit",
            "parse",
            "route",
            "extract",
            "validate",
            "score",
            "detect",
            "inquiry",
            "inquiry-download",
            "inquiry-label",
            "analyze",
            "report",
        ],
        help="结束阶段",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="限制处理的样本数量（用于测试）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="重建 inquiry discovery 输出，或让 inquiry-download 重新扫描候选并补下载",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="extract 阶段并发 worker 数；默认 1",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="extract 阶段任一文档失败即终止活跃 Kimi 进程并退出",
    )
    parser.add_argument(
        "--skip-empty-sections",
        action="store_true",
        help="extract 阶段跳过空 section 文档，适合已记录待补抓的错源年报",
    )
    parser.add_argument(
        "--crawl-backend",
        type=str,
        choices=["frontend", "official"],
        default="frontend",
        help="crawl 阶段使用的后端：frontend（公开前端 AJAX）或 official（深证信官方 API）",
    )
    parser.add_argument(
        "--parse-backend",
        type=str,
        choices=["local", "api", "api-batch"],
        default="local",
        help="parse 阶段使用的后端：local（本地 MinerU CLI）、api（MinerU 单任务 API）或 api-batch（MinerU URL 批量 API）",
    )
    parser.add_argument(
        "--inquiry-loop",
        action="store_true",
        help="运行扩展方案：包含问询函闭环分析",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/workflow.yaml",
        help="工作流配置文件路径",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------- #
# 阶段注册表
# ---------------------------------------------------------------------- #

STAGES = [
    "crawl",
    "download",
    "audit",
    "parse",
    "route",
    "extract",
    "validate",
    "score",
    "detect",
    "inquiry",
    "inquiry-download",
    "inquiry-label",
    "analyze",
    "report",
]

IMPLEMENTED = {
    "crawl",
    "download",
    "audit",
    "parse",
    "route",
    "extract",
    "validate",
    "score",
    "detect",
    "inquiry",
    "inquiry-download",
    "inquiry-label",
    "analyze",
    "report",
}


def run_crawl(limit: int | None = None, backend: str = "frontend") -> int:
    """运行爬虫阶段。"""
    if backend == "official":
        from src.crawl.cninfo_official_api import CninfoOfficialCrawler

        crawler = CninfoOfficialCrawler(limit=limit)
    else:
        from src.crawl.cninfo_api import CninfoCrawler

        crawler = CninfoCrawler(limit=limit)

    path = crawler.run()
    print(f"\n✅ crawl 完成: {path} (backend={backend})")
    return 0


def run_download(limit: int | None = None) -> int:
    """运行下载阶段。"""
    from src.download.downloader import PDFDownloader

    downloader = PDFDownloader(limit=limit)
    stats = downloader.run()
    print(f"\n✅ download 完成: {stats}")
    return 0


def run_audit() -> int:
    """运行审计阶段。"""
    from src.audit.auditor import DataAuditor

    auditor = DataAuditor()
    result = auditor.run()
    passed = result["passed"]
    print(f"\n{'✅' if passed else '❌'} audit 完成: {'通过' if passed else '未通过'}")
    return 0 if passed else 1


def run_parse(limit: int | None = None, parse_backend: str = "local") -> int:
    """运行 MinerU 解析阶段。"""
    if parse_backend == "api-batch":
        from src.parse.mineru_api_parser import MinerUApiBatchParser

        parser = MinerUApiBatchParser()
    elif parse_backend == "api":
        from src.parse.mineru_api_parser import MinerUApiParser

        parser = MinerUApiParser()
    else:
        from src.parse.mineru_parser import MinerUParser

        parser = MinerUParser()
    stats = parser.run(limit=limit)
    print(
        f"\n{'✅' if stats['failed'] == 0 else '⚠️'} "
        f"parse 完成: {stats} (backend={parse_backend})"
    )
    return 0 if stats["failed"] == 0 else 1


def run_route(limit: int | None = None, force: bool = False) -> int:
    """运行章节定位阶段。"""
    from src.route.section_router import SectionRouter

    router = SectionRouter()
    stats = router.run(limit=limit, force=force)
    print(f"\n✅ route 完成: {stats}")
    return 0


def run_extract(
    limit: int | None = None,
    workers: int = 1,
    fail_fast: bool = False,
    skip_empty_sections: bool = False,
) -> int:
    """运行 LLM 字段抽取阶段。"""
    from src.extract.llm_extractor import LLMExtractor

    extractor = LLMExtractor()
    stats = extractor.run(
        limit=limit,
        workers=workers,
        fail_fast=fail_fast,
        skip_empty_sections=skip_empty_sections,
    )
    print(f"\n{'✅' if stats['failed'] == 0 else '⚠️'} extract 完成: {stats}")
    return 0 if stats["failed"] == 0 else 1


def run_validate() -> int:
    """运行数据校验阶段。"""
    from src.validate.validator import DataValidator

    validator = DataValidator()
    stats = validator.run()
    print(f"\n{'✅' if stats['failed'] == 0 else '⚠️'} validate 完成: {stats}")
    return 0


def run_score() -> int:
    """运行风险评分阶段。"""
    from src.analysis.scorer import RiskScorer

    scorer = RiskScorer()
    stats = scorer.run()
    print(f"\n✅ score 完成: {stats}")
    return 0


def run_detect() -> int:
    """运行风险排序阶段。"""
    from src.analysis.detector import AnomalyDetector

    detector = AnomalyDetector()
    stats = detector.run()
    print(f"\n✅ detect 完成: {stats}")
    return 0


def _csv_has_rows(path: str | Path) -> bool:
    """判断 CSV 除表头外是否有数据行。"""
    with open(path, "r", encoding="utf-8", newline="") as f:
        return next(csv.DictReader(f), None) is not None


def run_inquiry(limit: int | None = None, force: bool = False) -> int:
    """运行问询候选发现阶段。"""
    from src.crawl.inquiry_crawler import InquiryCrawler

    crawler = InquiryCrawler(limit=limit)
    candidates_path = crawler.run(discover_only=True, force=force)
    print(f"\n✅ inquiry discovery 完成: {candidates_path}")
    print("   PDF 下载请单独运行: uv run python src/main.py --stage inquiry-download")
    return 0


def run_inquiry_download(limit: int | None = None, force: bool = False) -> int:
    """运行问询候选 PDF 下载阶段。"""
    from src.crawl.inquiry_quality import audit_inquiry_pdf_titles, write_orphan_pdf_report
    from src.download.downloader import PDFDownloader

    candidates_path = PROJECT_ROOT / "data" / "inquiry" / "inquiry_candidates.csv"
    if not candidates_path.exists():
        print("   inquiry_candidates.csv 不存在，请先运行: uv run python src/main.py --stage inquiry")
        return 1
    if not _csv_has_rows(candidates_path):
        print("   未发现问询/回复候选，跳过 PDF 下载")
        return 0
    if force:
        print("   force: 重新扫描候选，保留已存在且有效的 PDF，补下载缺失或失败项")

    downloader = PDFDownloader(
        metadata_path="data/inquiry/inquiry_candidates.csv",
        pdf_dir="data/inquiry/pdf",
        log_path="outputs/logs/inquiry_download_log.jsonl",
        limit=limit,
    )
    stats = downloader.run()
    title_stats = audit_inquiry_pdf_titles(
        candidates_path=candidates_path,
        project_root=PROJECT_ROOT,
        limit=limit,
    )
    orphan_stats = write_orphan_pdf_report(
        candidates_path,
        PROJECT_ROOT / "data" / "inquiry" / "pdf",
        PROJECT_ROOT / "outputs" / "reports" / "inquiry_orphan_pdf_report.md",
        project_root=PROJECT_ROOT,
    )
    print(f"\n✅ inquiry download 完成: {stats}")
    print(f"   PDF 标题校验: {title_stats}")
    print(f"   orphan PDF 报告: {orphan_stats}")
    return 0


def run_inquiry_label() -> int:
    """运行问询内容标签阶段。"""
    from src.analysis.inquiry_labeler import InquiryLabeler

    labeler = InquiryLabeler()
    stats = labeler.run()
    print(f"\n✅ inquiry-label 完成: {stats}")
    return 0


def run_analyze() -> int:
    """运行闭环分析阶段。"""
    from src.analysis.evaluator import LoopEvaluator

    evaluator = LoopEvaluator()
    stats = evaluator.run()
    print(f"\n✅ analyze 完成: {stats}")
    return 0


def run_report() -> int:
    """运行报告生成阶段。"""
    from src.analysis.reporter import FinalReporter

    reporter = FinalReporter()
    stats = reporter.run()
    print(f"\n✅ report 完成: {stats}")
    return 0


def run_stage(
    stage: str,
    limit: int | None = None,
    backend: str = "frontend",
    force: bool = False,
    parse_backend: str = "local",
    workers: int = 1,
    fail_fast: bool = False,
    skip_empty_sections: bool = False,
) -> int:
    """运行单个阶段。"""
    if stage not in IMPLEMENTED:
        print(f"\n⏸️  阶段 '{stage}' 尚未实现")
        print(f"   已实现阶段: {', '.join(sorted(IMPLEMENTED))}")
        return 0

    print(f"\n{'='*60}")
    print(f"运行阶段: {stage}")
    print(f"{'='*60}")

    dispatch = {
        "crawl": run_crawl,
        "download": run_download,
        "audit": run_audit,
        "parse": run_parse,
        "route": run_route,
        "extract": run_extract,
        "validate": run_validate,
        "score": run_score,
        "detect": run_detect,
        "inquiry": run_inquiry,
        "inquiry-download": run_inquiry_download,
        "inquiry-label": run_inquiry_label,
        "analyze": run_analyze,
        "report": run_report,
    }

    # 按阶段装配参数
    kwargs: dict[str, Any] = {}
    if stage == "crawl":
        kwargs = {"limit": limit, "backend": backend}
    elif stage in {"inquiry", "inquiry-download", "route"}:
        kwargs = {"limit": limit, "force": force}
    elif stage == "parse":
        kwargs = {"limit": limit, "parse_backend": parse_backend}
    elif stage == "extract":
        kwargs = {
            "limit": limit,
            "workers": workers,
            "fail_fast": fail_fast,
            "skip_empty_sections": skip_empty_sections,
        }
    elif stage == "download":
        kwargs = {"limit": limit}

    # 统一包装：计时 + try/except + run_log.jsonl（Week 14 讲义要求）
    import time

    from src.common import log_step

    start = time.monotonic()
    status = "success"
    error = ""
    rc = 0
    try:
        rc = dispatch[stage](**kwargs)
        if rc != 0:
            status = "failed"
    except Exception as e:  # noqa: BLE001 — 顶层调度需捕获并记录所有阶段异常
        rc = 1
        status = "error"
        error = repr(e)
        print(f"\n❌ 阶段 '{stage}' 异常: {e}")
    elapsed = time.monotonic() - start
    log_step(
        stage,
        doc_id="*",
        status=status,
        elapsed=elapsed,
        error=error,
        log_path=PROJECT_ROOT / "outputs" / "logs" / "run_log.jsonl",
    )
    return rc


def run_pipeline(
    from_stage: str | None,
    to_stage: str | None,
    limit: int | None = None,
    backend: str = "frontend",
    force: bool = False,
    parse_backend: str = "local",
    workers: int = 1,
    fail_fast: bool = False,
    skip_empty_sections: bool = False,
) -> int:
    """运行 Pipeline 片段。"""
    start_idx = STAGES.index(from_stage) if from_stage else 0
    end_idx = STAGES.index(to_stage) if to_stage else len(STAGES) - 1

    if start_idx > end_idx:
        print("错误: --from-stage 不能晚于 --to-stage")
        return 1

    for stage in STAGES[start_idx : end_idx + 1]:
        rc = run_stage(
            stage,
            limit=limit,
            backend=backend,
            force=force,
            parse_backend=parse_backend,
            workers=workers,
            fail_fast=fail_fast,
            skip_empty_sections=skip_empty_sections,
        )
        if rc != 0:
            print(f"\n❌ 阶段 '{stage}' 失败，Pipeline 中断")
            return rc

    return 0


def main() -> int:
    args = parse_args()

    if not args.stage and not args.from_stage:
        print("错误：必须指定 --stage 或 --from-stage")
        print("\n示例:")
        print("  uv run python src/main.py --stage crawl")
        print("  uv run python src/main.py --stage all")
        print("  uv run python src/main.py --from-stage crawl --to-stage audit")
        return 1

    print("=" * 60)
    print("研发资本化风险排序与问询函可行性测试")
    print("=" * 60)
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"配置文件: {args.config}")
    if args.limit:
        print(f"限制样本数: {args.limit}")
    if args.force:
        print("force: enabled")
    if args.workers != 1 and (args.stage == "extract" or args.from_stage == "extract"):
        print(f"extract workers: {args.workers}")
    if args.fail_fast and (args.stage == "extract" or args.from_stage == "extract"):
        print("extract fail-fast: enabled")
    if args.skip_empty_sections and (args.stage == "extract" or args.from_stage == "extract"):
        print("extract skip-empty-sections: enabled")
    if args.stage == "crawl" or args.from_stage == "crawl":
        print(f"crawl 后端: {args.crawl_backend}")
    if args.stage == "parse" or args.from_stage == "parse":
        print(f"parse 后端: {args.parse_backend}")
    if args.inquiry_loop:
        print("模式: 扩展方案（含问询函闭环）")
    else:
        print("模式: 基础方案")
    print("=" * 60)

    if args.stage == "all":
        return run_pipeline(
            "crawl",
            "report",
            limit=args.limit,
            backend=args.crawl_backend,
            force=args.force,
            parse_backend=args.parse_backend,
            workers=args.workers,
            fail_fast=args.fail_fast,
            skip_empty_sections=args.skip_empty_sections,
        )
    elif args.stage:
        return run_stage(
            args.stage,
            limit=args.limit,
            backend=args.crawl_backend,
            force=args.force,
            parse_backend=args.parse_backend,
            workers=args.workers,
            fail_fast=args.fail_fast,
            skip_empty_sections=args.skip_empty_sections,
        )
    else:
        return run_pipeline(
            args.from_stage,
            args.to_stage,
            limit=args.limit,
            backend=args.crawl_backend,
            force=args.force,
            parse_backend=args.parse_backend,
            workers=args.workers,
            fail_fast=args.fail_fast,
            skip_empty_sections=args.skip_empty_sections,
        )


if __name__ == "__main__":
    sys.exit(main())
