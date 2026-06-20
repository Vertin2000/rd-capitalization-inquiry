"""Quick anomaly detection scaffold for scored records."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


class AnomalyDetector:
    """Mark the top scored records as anomalies."""

    def __init__(
        self,
        input_path: str | Path = "data/scored/records.jsonl",
        output_path: str | Path = "data/scored/records.jsonl",
        anomaly_path: str | Path = "data/anomaly/anomaly_list.csv",
        config_path: str | Path = "configs/model_config.yaml",
        anomaly_percentile: float | None = None,
    ) -> None:
        self.input_path = self._resolve(input_path)
        self.output_path = self._resolve(output_path)
        self.anomaly_path = self._resolve(anomaly_path)
        self.config_path = self._resolve(config_path)
        self.anomaly_percentile = anomaly_percentile

    @staticmethod
    def _resolve(path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def _percentile(self) -> float:
        if self.anomaly_percentile is not None:
            return self.anomaly_percentile
        if not self.config_path.exists():
            return 0.80
        with self.config_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return float(config.get("scoring", {}).get("anomaly_percentile", 0.80))

    @staticmethod
    def _anomaly_type(record: dict[str, Any]) -> str:
        reasons: list[str] = []
        if _as_float(record.get("industry_percentile")) is not None and float(record["industry_percentile"]) >= 0.8:
            reasons.append("industry_outlier")
        if _as_float(record.get("change_zscore")) is not None and abs(float(record["change_zscore"])) >= 1.5:
            reasons.append("change_spike")
        if _as_float(record.get("fuzziness_score")) is not None and float(record["fuzziness_score"]) >= 0.5:
            reasons.append("fuzziness")
        if _as_float(record.get("identity_check_score")) is not None and float(record["identity_check_score"]) < 0.5:
            reasons.append("identity_error")
        if len(reasons) > 1:
            return "multiple"
        if reasons:
            return reasons[0]
        return "industry_outlier"

    def run(self) -> dict[str, int]:
        records = _read_jsonl(self.input_path)
        scored_records = [
            record
            for record in records
            if _as_float(record.get("aggressiveness_score")) is not None
        ]
        scored_records.sort(
            key=lambda row: float(row.get("aggressiveness_score") or 0),
            reverse=True,
        )
        top_count = 0
        if scored_records:
            top_count = max(1, math.ceil(len(scored_records) * (1 - self._percentile())))
        anomaly_ids = {record.get("doc_id") for record in scored_records[:top_count]}

        anomaly_rows: list[dict[str, Any]] = []
        unscored = 0
        for record in records:
            notes = list(record.get("data_quality_notes") or [])
            score = _as_float(record.get("aggressiveness_score"))
            if score is None:
                record["is_anomaly"] = False
                record["anomaly_type"] = None
                notes.append("TODO: waiting for score")
                unscored += 1
            elif record.get("doc_id") in anomaly_ids:
                record["is_anomaly"] = True
                record["anomaly_type"] = self._anomaly_type(record)
                anomaly_rows.append(record)
            else:
                record["is_anomaly"] = False
                record["anomaly_type"] = None
            record["data_quality_notes"] = sorted(set(notes))

        self.anomaly_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "doc_id",
            "company_code",
            "company_name",
            "year",
            "industry",
            "capitalization_rate",
            "aggressiveness_score",
            "anomaly_type",
            "data_quality_notes",
        ]
        with self.anomaly_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in anomaly_rows:
                writer.writerow({field: row.get(field, "") for field in fieldnames})

        _write_jsonl(self.output_path, records)
        return {"total": len(records), "anomalies": len(anomaly_rows), "unscored": unscored}
