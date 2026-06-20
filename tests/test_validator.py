"""Tests for extracted-record validation."""

from __future__ import annotations

import json
from pathlib import Path

from src.validate.validator import DataValidator


def valid_extracted_record(doc_id: str = "doc") -> dict:
    return {
        "doc_id": doc_id,
        "company_name": "真实公司",
        "company_code": "000001",
        "year": 2023,
        "rd_expense_total": {"value": 100.0, "evidence_text": "研发投入金额 100 万元"},
        "rd_capitalized_amount": {"value": 20.0, "evidence_text": "资本化的金额 20 万元"},
        "rd_expensed_amount": {"value": 80.0, "evidence_text": "费用化的金额 80 万元"},
        "capitalization_rate": {"value": 20.0, "evidence_text": "资本化率 20%"},
        "source_pdf_path": "data/pdf/doc.pdf",
    }


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def test_validator_flattens_field_evidence_and_calculates_rate(tmp_path: Path) -> None:
    """Nested FieldEvidence values should validate into flat records."""
    input_path = tmp_path / "extracted" / "records.jsonl"
    output_path = tmp_path / "validated" / "records.jsonl"
    error_path = tmp_path / "validated" / "validation_errors.jsonl"
    record = valid_extracted_record()
    record.pop("capitalization_rate")
    write_jsonl(input_path, [record])

    stats = DataValidator(
        input_path=str(input_path),
        output_path=str(output_path),
        error_path=str(error_path),
    ).run()

    assert stats == {"total": 1, "passed": 1, "failed": 0}
    validated = json.loads(output_path.read_text(encoding="utf-8"))
    assert validated["rd_capitalized_amount"] == 20.0
    assert validated["capitalization_rate"] == 20.0


def test_validator_overwrites_outputs_on_each_run(tmp_path: Path) -> None:
    """Rerunning validate should not append duplicate stale records."""
    input_path = tmp_path / "extracted" / "records.jsonl"
    output_path = tmp_path / "validated" / "records.jsonl"
    error_path = tmp_path / "validated" / "validation_errors.jsonl"
    write_jsonl(input_path, [valid_extracted_record()])
    validator = DataValidator(
        input_path=str(input_path),
        output_path=str(output_path),
        error_path=str(error_path),
    )

    assert validator.run() == {"total": 1, "passed": 1, "failed": 0}
    assert validator.run() == {"total": 1, "passed": 1, "failed": 0}

    assert len(output_path.read_text(encoding="utf-8").splitlines()) == 1
    assert error_path.read_text(encoding="utf-8") == ""


def test_validator_writes_identity_errors(tmp_path: Path) -> None:
    """Large capitalization + expensed vs total gaps should go to error JSONL."""
    input_path = tmp_path / "extracted" / "records.jsonl"
    output_path = tmp_path / "validated" / "records.jsonl"
    error_path = tmp_path / "validated" / "validation_errors.jsonl"
    record = valid_extracted_record()
    record["rd_expensed_amount"]["value"] = 10.0
    write_jsonl(input_path, [record])

    stats = DataValidator(
        input_path=str(input_path),
        output_path=str(output_path),
        error_path=str(error_path),
    ).run()

    assert stats == {"total": 1, "passed": 0, "failed": 1}
    error = json.loads(error_path.read_text(encoding="utf-8"))
    assert "恒等式偏差" in error["error"]
    assert output_path.read_text(encoding="utf-8") == ""
