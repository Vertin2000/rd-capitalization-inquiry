"""Inquiry candidate naming and lightweight PDF quality checks."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Callable

import pdfplumber


def sanitize_filename_part(value: str) -> str:
    """Return a Windows-safe, compact filename segment."""
    cleaned = re.sub(r"<.*?>", "", value or "")
    cleaned = re.sub(r'[\\/:*?"<>|]', "", cleaned)
    cleaned = re.sub(r"\s+", "", cleaned)
    return cleaned.strip("_") or "unknown"


def classify_document_role(title: str) -> str:
    """Classify an inquiry candidate into a finer document role."""
    cleaned = re.sub(r"<.*?>", "", title or "")
    if "监管工作函" in cleaned:
        return "regulatory_work_letter"
    if "关注函" in cleaned:
        return "attention_letter"
    if "延期" in cleaned and ("回复" in cleaned or "答复" in cleaned):
        return "delay_notice"
    if any(keyword in cleaned for keyword in ("专项说明", "核查意见", "独立意见", "法律意见书")):
        return "supporting_statement"
    if "问询函" in cleaned and any(keyword in cleaned for keyword in ("回复", "答复")):
        return "substantive_reply"
    if "问询函" in cleaned:
        return "inquiry_notice"
    return "process_other"


def build_inquiry_doc_id(
    *,
    stock_code: str,
    stock_name: str,
    report_year: str,
    publish_date: str,
    document_role: str,
    announcement_id: str,
) -> str:
    """Build a readable and stable inquiry document id."""
    parts = [
        sanitize_filename_part(stock_code),
        sanitize_filename_part(stock_name),
        sanitize_filename_part(report_year),
        sanitize_filename_part(publish_date),
        sanitize_filename_part(document_role),
        sanitize_filename_part(announcement_id),
    ]
    return "_".join(parts)


def extract_title_from_pdf_text(text: str) -> str:
    """Extract the first likely announcement title block from first-page text."""
    lines = [line.strip() for line in (text or "").splitlines()]
    content_lines = [
        line
        for line in lines
        if line
        and "证券简称" not in line
        and "证券代码" not in line
        and "编号" not in line
        and "本公司董事会" not in line
        and "重大遗漏" not in line
    ]
    selected: list[str] = []
    for line in content_lines:
        selected.append(line)
        if line.endswith("公告") or line.endswith("问询函") or line.endswith("说明"):
            break
        if len(selected) >= 3:
            break
    return " ".join(selected).strip()


def extract_pdf_title(pdf_path: Path) -> tuple[str, str]:
    """Extract first-page PDF title without OCR."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                return "", "empty"
            text = pdf.pages[0].extract_text() or ""
    except Exception:
        return "", "error"

    title = extract_title_from_pdf_text(text)
    if title:
        return title, "ok"
    return "", "empty"


def _stock_name_matches(stock_name: str, actual: str) -> bool:
    """Return True when a stock short name plausibly appears in a PDF title."""
    cleaned = re.sub(r"<.*?>", "", stock_name or "")
    cleaned = re.sub(r"\s+", "", cleaned)
    if not cleaned:
        return False
    if cleaned in actual:
        return True

    suffixes = ("股份", "科技", "医疗", "生物", "网络", "药业", "电子", "集团")
    stem = cleaned
    for suffix in suffixes:
        if stem.endswith(suffix) and len(stem) > len(suffix) + 1:
            stem = stem[: -len(suffix)]
            break
    return len(stem) >= 2 and stem in actual


def title_match_status(row: dict[str, str], pdf_title: str, pdf_title_status: str) -> str:
    """Lightweight consistency check between CNINFO title and PDF title."""
    if pdf_title_status != "ok" or not pdf_title:
        return "unknown"
    expected = re.sub(r"\s+", "", row.get("announcement_title", ""))
    actual = re.sub(r"\s+", "", pdf_title)
    stock_name = row.get("stock_name", "")
    role = row.get("document_role", "")
    if expected and (expected in actual or actual in expected):
        return "match"
    if _stock_name_matches(stock_name, actual):
        if role == "delay_notice" and "延期" in actual:
            return "match"
        if role == "substantive_reply" and "回复" in actual and "问询函" in actual:
            return "match"
        if role == "inquiry_notice" and "问询函" in actual:
            return "match"
        if role in {"attention_letter", "regulatory_work_letter"}:
            return "match"
    return "mismatch"


def _resolve_path(project_root: Path, local_path: str) -> Path:
    path = Path(local_path)
    if path.is_absolute():
        return path
    return project_root / path


def audit_inquiry_pdf_titles(
    *,
    candidates_path: Path,
    project_root: Path,
    limit: int | None = None,
    extractor: Callable[[Path], tuple[str, str]] = extract_pdf_title,
) -> dict[str, int]:
    """Write PDF title audit fields back to inquiry_candidates.csv."""
    with candidates_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    for column in ("pdf_title", "pdf_title_status", "title_match_status"):
        if column not in fieldnames:
            fieldnames.append(column)

    stats = {"ok": 0, "empty": 0, "needs_ocr": 0, "missing": 0, "error": 0}
    rows_to_audit = rows[:limit] if limit is not None else rows
    for row in rows_to_audit:
        local_path = row.get("local_pdf_path", "")
        pdf_path = _resolve_path(project_root, local_path) if local_path else Path()
        if not local_path or not pdf_path.exists():
            row["pdf_title"] = ""
            row["pdf_title_status"] = "missing"
            row["title_match_status"] = "unknown"
            stats["missing"] += 1
            continue

        title, status = extractor(pdf_path)
        if status not in stats:
            status = "error"
        row["pdf_title"] = title
        row["pdf_title_status"] = status
        row["title_match_status"] = title_match_status(row, title, status)
        stats[status] += 1

    with candidates_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return stats


def write_orphan_pdf_report(
    candidates_path: Path,
    pdf_dir: Path,
    report_path: Path,
    *,
    project_root: Path,
) -> dict[str, int]:
    """Report PDFs under pdf_dir that are not referenced by candidates_path."""
    with candidates_path.open("r", encoding="utf-8", newline="") as f:
        referenced = {
            _resolve_path(project_root, row.get("local_pdf_path", "")).resolve()
            for row in csv.DictReader(f)
            if row.get("local_pdf_path")
        }
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    orphans = [path for path in pdf_files if path.resolve() not in referenced]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Inquiry Orphan PDF Report",
        "",
        f"- referenced: {len(referenced)}",
        f"- pdf_files: {len(pdf_files)}",
        f"- orphans: {len(orphans)}",
        "",
    ]
    lines.extend(f"- `{path.name}`" for path in orphans)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"referenced": len(referenced), "pdf_files": len(pdf_files), "orphans": len(orphans)}
