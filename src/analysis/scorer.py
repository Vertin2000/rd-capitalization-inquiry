"""Quick downstream risk scoring scaffold.

This module is intentionally tolerant of partial extract/validate outputs. Missing
inputs stay as nulls and are explained in ``data_quality_notes`` so downstream
stages can run while extraction continues.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 资本化条件披露的模糊信号词。
# 刻意排除「等/相关/合理/未来/预计/预期/可能」等高频正向词：
#   - 「等」是汉语最高频字之一，命中即 +1 等于给所有非空文本加分；
#   - 「未来经济利益很可能流入」本是 CAS6 资本化五条件的合规披露，是正向证据而非模糊证据。
# 改为会计估计中真正体现「主观判断空间」的措辞。
FUZZY_KEYWORDS = (
    "视情况",
    "根据情况",
    "管理层判断",
    "必要时",
    "综合评估",
    "谨慎判断",
    "视具体",
    "具体情况",
    "重大判断",
    "估计",
)

# 长度归一化基准：披露文本每 FUZZY_NORM_CHARS 字符预期 1 个模糊词命中，
# 避免长披露因命中数多而被高估模糊度。
FUZZY_NORM_CHARS = 200


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


def _rate(record: dict[str, Any]) -> float | None:
    direct = _as_float(record.get("capitalization_rate"))
    if direct is not None:
        return direct
    calculated = _as_float(record.get("calculated_capitalization_rate"))
    if calculated is not None:
        return calculated
    cap = _as_float(record.get("rd_capitalized_amount"))
    exp = _as_float(record.get("rd_expensed_amount"))
    if cap is not None and exp is not None and cap + exp > 0:
        return round(cap / (cap + exp) * 100, 2)
    total = _as_float(record.get("rd_expense_total"))
    if cap is not None and total is not None and total > 0:
        return round(cap / total * 100, 2)
    return None


def _percentile(value: float, values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(1 for item in values if item <= value) / len(values), 4)


def _industry_for_code(company_code: str) -> str:
    """Infer the configured industry from crawl.yaml ordering.

    The current course dataset is 20 pharma + 20 electronics + 10 software
    companies. If the config later gains explicit industry fields, use those.
    """
    config_path = PROJECT_ROOT / "configs" / "crawl.yaml"
    if not config_path.exists():
        return "unknown"
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    companies = config.get("companies", [])
    for index, company in enumerate(companies):
        if str(company.get("code", "")) != str(company_code):
            continue
        explicit = company.get("industry")
        if explicit:
            return str(explicit)
        if index < 20:
            return "医药制造"
        if index < 40:
            return "电子设备"
        return "软件信息"
    return "unknown"


def _identity_score(record: dict[str, Any]) -> float | None:
    cap = _as_float(record.get("rd_capitalized_amount"))
    exp = _as_float(record.get("rd_expensed_amount"))
    total = _as_float(record.get("rd_expense_total"))
    if cap is None or exp is None or total is None or total <= 0:
        return None
    diff_ratio = abs(cap + exp - total) / total
    return round(max(0.0, 1.0 - diff_ratio / 0.20), 4)


def _fuzziness_score(text: Any) -> float | None:
    if not text:
        return None
    content = str(text)
    hits = sum(1 for keyword in FUZZY_KEYWORDS if keyword in content)
    # 长度归一化：hits / (len / NORM_CHARS)，再封顶 1.0。
    # 避免长披露因绝对命中数多而被高估，也避免极短文本一次命中即满分。
    norm_factor = max(1.0, len(content) / FUZZY_NORM_CHARS)
    return round(min(1.0, hits / norm_factor), 4)


class RiskScorer:
    """Compute a best-effort aggressiveness score for validated records."""

    def __init__(
        self,
        input_path: str | Path = "data/validated/records.jsonl",
        output_path: str | Path = "data/scored/records.jsonl",
        config_path: str | Path = "configs/model_config.yaml",
    ) -> None:
        self.input_path = self._resolve(input_path)
        self.output_path = self._resolve(output_path)
        self.config_path = self._resolve(config_path)

    @staticmethod
    def _resolve(path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def _weights(self) -> dict[str, float]:
        if not self.config_path.exists():
            return {
                "industry_weight": 0.25,
                "change_weight": 0.25,
                "fuzziness_weight": 0.25,
            }
        with self.config_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        scoring = config.get("scoring", {})
        return {
            "industry_weight": float(scoring.get("industry_weight", 0.25)),
            "change_weight": float(scoring.get("change_weight", 0.25)),
            "fuzziness_weight": float(scoring.get("fuzziness_weight", 0.25)),
        }

    def run(self) -> dict[str, int]:
        records = _read_jsonl(self.input_path)
        weights = self._weights()

        for record in records:
            record["industry"] = record.get("industry") or _industry_for_code(
                str(record.get("company_code", ""))
            )
            record["capitalization_rate"] = _rate(record)

        rates_by_industry_year: dict[tuple[str, int], list[float]] = {}
        rates_by_company: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            rate = _as_float(record.get("capitalization_rate"))
            if rate is not None:
                key = (str(record.get("industry", "unknown")), int(record.get("year", 0) or 0))
                rates_by_industry_year.setdefault(key, []).append(rate)
            rates_by_company.setdefault(str(record.get("company_code", "")), []).append(record)

        change_values: list[float] = []
        for company_records in rates_by_company.values():
            company_records.sort(key=lambda row: int(row.get("year", 0) or 0))
            previous_rate: float | None = None
            for record in company_records:
                current_rate = _as_float(record.get("capitalization_rate"))
                record["prev_year_rate"] = previous_rate
                if previous_rate is not None and current_rate is not None:
                    change = round(current_rate - previous_rate, 4)
                    record["change_pct"] = change
                    change_values.append(change)
                else:
                    record["change_pct"] = None
                if current_rate is not None:
                    previous_rate = current_rate

        change_mean = mean(change_values) if change_values else 0.0
        change_std = pstdev(change_values) if len(change_values) > 1 else 0.0

        scored = 0
        partial = 0
        output: list[dict[str, Any]] = []
        for record in records:
            notes = list(record.get("data_quality_notes") or [])
            rate = _as_float(record.get("capitalization_rate"))
            if rate is None:
                notes.append("TODO: waiting for extract capitalization_rate")

            industry_values = rates_by_industry_year.get(
                (str(record.get("industry", "unknown")), int(record.get("year", 0) or 0)),
                [],
            )
            industry_percentile = _percentile(rate, industry_values) if rate is not None else None
            record["industry_percentile"] = industry_percentile

            change = _as_float(record.get("change_pct"))
            if change is not None and change_std > 0:
                change_zscore = round((change - change_mean) / change_std, 4)
            elif change is not None:
                change_zscore = 0.0
            else:
                change_zscore = None
            record["change_zscore"] = change_zscore

            fuzziness = _fuzziness_score(record.get("capitalization_condition"))
            record["fuzziness_score"] = fuzziness

            identity = _identity_score(record)
            record["identity_check_score"] = identity
            if identity is None:
                notes.append("TODO: waiting for extract identity inputs")

            components: list[tuple[float, float]] = []
            if industry_percentile is not None:
                components.append((industry_percentile * 100, weights["industry_weight"]))
            if change_zscore is not None:
                # 只捕捉资本化率正向跳升（变激进），不把「突然降到 0」算激进。
                # 原先用 abs() 会把项目完结转无形资产导致的下降误判为激进。
                change_score = min(100.0, max(0.0, change_zscore) / 2 * 100)
                components.append((change_score, weights["change_weight"]))
            if fuzziness is not None:
                components.append((fuzziness * 100, weights["fuzziness_weight"]))

            if components:
                weighted_sum = sum(score * weight for score, weight in components)
                weight_sum = sum(weight for _score, weight in components)
                raw_score = weighted_sum / weight_sum if weight_sum else None
            else:
                raw_score = None

            if raw_score is None:
                record["aggressiveness_score"] = None
                notes.append("TODO: waiting for score inputs")
                partial += 1
            else:
                multiplier = identity if identity is not None else 1.0
                record["aggressiveness_score"] = round(raw_score * multiplier, 4)
                scored += 1

            record["data_quality_notes"] = sorted(set(notes))
            output.append(record)

        _write_jsonl(self.output_path, output)
        return {"total": len(output), "scored": scored, "partial": partial}
