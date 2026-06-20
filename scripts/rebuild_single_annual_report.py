"""一次性修复脚本：仅重建 603501_韦尔股份_2021年报 单条产物。

背景：该 doc 上游错抓成"持续督导年度报告书"，本地 PDF/md/sections 均为错文件。
metadata.csv 已修正为正确年报 URL。本脚本只处理这一条，绝不触碰其他 149 条。

链路：删旧产物 -> 下载正确 PDF -> MinerU API 解析 -> force route -> extract resume

用法：
    uv run python scripts/rebuild_single_annual_report.py
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("rebuild_single_annual_report")

DOC_ID = "603501_韦尔股份_2021年报"


def main() -> int:
    from src.download.downloader import PDFDownloader
    from src.parse.mineru_api_parser import MinerUApiBatchParser
    from src.route.section_router import SectionRouter
    from src.extract.llm_extractor import LLMExtractor

    pdf_path = PROJECT_ROOT / "data" / "pdf" / f"{DOC_ID}.pdf"
    md_path = PROJECT_ROOT / "data" / "parsed" / f"{DOC_ID}.md"
    sections_path = (
        PROJECT_ROOT / "data" / "sections" / f"{DOC_ID}_sections.jsonl"
    )
    raw_dir = PROJECT_ROOT / "data" / "parsed" / "mineru_api_raw" / DOC_ID

    # 1. 删除旧的错误产物（PDF/md/sections/raw），强制全部重建
    for target in (pdf_path, md_path, sections_path):
        if target.exists():
            target.unlink()
            logger.info("已删除旧产物: %s", target.name)
    if raw_dir.exists():
        import shutil

        shutil.rmtree(raw_dir)
        logger.info("已删除旧 MinerU raw: %s", raw_dir.name)

    # 2. 下载正确 PDF（downloader 读 metadata.csv 全表，但只有缺失项才会下，
    #    其余 149 条已存在且有效会被 _check_existing 跳过）
    logger.info("=== 步骤 1/4: 下载正确 PDF ===")
    PDFDownloader().run()
    if not pdf_path.exists():
        logger.error("PDF 下载失败，终止")
        return 1

    # 3. MinerU API 单条解析（直接调 parse_pdf，不走 run() 的全量 glob）
    logger.info("=== 步骤 2/4: MinerU API 单条解析 ===")
    parser = MinerUApiBatchParser()
    parser._headers()
    metadata = parser._load_metadata()
    row = metadata.get(DOC_ID)
    if row is None:
        logger.error("metadata 中找不到 %s，终止", DOC_ID)
        return 1
    parser.parse_pdf(pdf_path, row)
    if not md_path.exists() or md_path.stat().st_size == 0:
        logger.error("MinerU 解析未产出非空 Markdown，终止")
        return 1

    # 4. 单条 force route
    logger.info("=== 步骤 3/4: force route ===")
    router = SectionRouter()
    router.route(md_path, DOC_ID, force=True)
    if sections_path.stat().st_size == 0:
        logger.warning("route 后 sections 仍为空：该 md 可能仍无研发章节，请人工核对")

    # 5. 单条 extract（直接抽韦尔这一条，不走 run() 的全量 resume，
    #    避免连带重跑 run6 未完成的其它失败项）
    logger.info("=== 步骤 4/4: extract 单条 ===")
    extractor = LLMExtractor()
    # 强制重抽：先从已抽集合中排除本条（若之前误写过空记录）
    extracted = extractor._load_extracted_set()
    extracted.discard(DOC_ID)
    record = extractor.extract(DOC_ID, extracted=extracted, raise_on_error=True)
    if record is None:
        logger.error("extract 未产出记录（section 可能仍为空），终止")
        return 1
    extractor._save_record(record)
    logger.info("extract 完成: 韦尔股份单条已写入 records.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
