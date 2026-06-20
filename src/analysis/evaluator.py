"""Partial loop evaluation for anomaly predictions and inquiry labels."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


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


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def _prediction_result(predicted: bool, actual: bool) -> str:
    if predicted and actual:
        return "TP"
    if predicted and not actual:
        return "FP"
    if not predicted and actual:
        return "FN"
    return "TN"


class LoopEvaluator:
    """Build confusion matrix and descriptive partial metrics."""

    def __init__(
        self,
        scored_path: str | Path = "data/scored/records.jsonl",
        inquiry_path: str | Path = "data/inquiry/inquiry_records.jsonl",
        output_path: str | Path = "outputs/loop_evaluation.json",
    ) -> None:
        self.scored_path = self._resolve(scored_path)
        self.inquiry_path = self._resolve(inquiry_path)
        self.output_path = self._resolve(output_path)

    @staticmethod
    def _resolve(path: str | Path) -> Path:
        path = Path(path)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def run(self) -> dict[str, int | None]:
        scored_records = _read_jsonl(self.scored_path)
        inquiry_records = _read_jsonl(self.inquiry_path)
        inquiry_by_doc_id = {
            row.get("annual_doc_id"): row
            for row in inquiry_records
            if row.get("annual_doc_id")
        }

        matrix = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
        joined_rows: list[dict[str, Any]] = []
        for scored in scored_records:
            annual_doc_id = scored.get("doc_id", "")
            inquiry = inquiry_by_doc_id.get(annual_doc_id, {})
            predicted = bool(scored.get("is_anomaly"))
            actual = bool(
                inquiry.get("capitalization_related")
                if "capitalization_related" in inquiry
                else inquiry.get("inquiry_actually_received")
            )
            result = _prediction_result(predicted, actual)
            matrix[result.lower()] += 1
            joined_rows.append(
                {
                    "annual_doc_id": annual_doc_id,
                    "stock_code": scored.get("company_code", ""),
                    "year": scored.get("year"),
                    "company_name": scored.get("company_name", ""),
                    "capitalization_rate": scored.get("capitalization_rate"),
                    "aggressiveness_score": scored.get("aggressiveness_score"),
                    "is_anomaly": predicted,
                    "inquiry_actually_received": actual,
                    "inquiry_received": inquiry.get("inquiry_received", False),
                    "capitalization_related": inquiry.get("capitalization_related", actual),
                    "inquiry_title": inquiry.get("inquiry_title"),
                    "inquiry_keywords": inquiry.get("inquiry_keywords") or [],
                    "prediction_result": result,
                    "notes": inquiry.get("notes") or [],
                }
            )

        precision = _safe_ratio(matrix["tp"], matrix["tp"] + matrix["fp"])
        recall = _safe_ratio(matrix["tp"], matrix["tp"] + matrix["fn"])
        if precision is None or recall is None or precision + recall == 0:
            f1 = None
        else:
            f1 = round(2 * precision * recall / (precision + recall), 4)

        top_k = sorted(
            joined_rows,
            key=lambda row: row.get("aggressiveness_score") or -1,
            reverse=True,
        )[:10]
        evaluated_doc_ids = {row.get("annual_doc_id") for row in joined_rows}
        inquiry_only_count = sum(
            1
            for row in inquiry_records
            if row.get("annual_doc_id") not in evaluated_doc_ids
        )

        baselines = self._compute_baselines(joined_rows, matrix)

        # TN 水分：未评分（无 aggressiveness_score）的记录被默认归非异常，计入 TN。
        tn_unscored = sum(
            1
            for row in joined_rows
            if not row.get("is_anomaly") and row.get("aggressiveness_score") is None
        )

        output = {
            "status": "partial",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "total": len(joined_rows),
            "scored_records": len(scored_records),
            "inquiry_records": len(inquiry_records),
            "inquiry_only_records": inquiry_only_count,
            "confusion_matrix": matrix,
            "metrics": {
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "top_k_hit_rate": _safe_ratio(
                    sum(1 for row in top_k if row["inquiry_actually_received"]),
                    len(top_k),
                ),
            },
            "baselines": baselines,
            "tn_water": {
                "tn_total": matrix["tn"],
                "tn_unscored_defaulted_non_anomaly": tn_unscored,
                "note": (
                    f"TN={matrix['tn']} 中含 {tn_unscored} 条因关键字段缺失无风险分、"
                    "被默认归为非异常的记录；这些记录并未真正通过模型判定。"
                ),
            },
            "caveats": [
                "Inquiry labels use Tier-1 keyword pruning plus LLM semantic classification; only inquiry/attention/regulatory letters are counted, and reply documents are excluded.",
                "Full annual sample is joined, but some extracted financial fields remain null and are carried as data-quality notes.",
                f"TN contains {tn_unscored} records with missing data that were defaulted to non-anomaly; positive labels are too few for meaningful precision/recall.",
            ],
            "top_k": top_k,
            "records": joined_rows,
        }
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return {
            "total": len(joined_rows),
            "tp": matrix["tp"],
            "fp": matrix["fp"],
            "tn": matrix["tn"],
            "fn": matrix["fn"],
        }

    @staticmethod
    def _pr_for(predicted_ids: set[str], rows: list[dict[str, Any]]) -> dict[str, Any]:
        """Precision/recall for a given predicted-positive set against the actual labels."""
        tp = sum(1 for r in rows if r["annual_doc_id"] in predicted_ids and r["inquiry_actually_received"])
        fp = sum(1 for r in rows if r["annual_doc_id"] in predicted_ids and not r["inquiry_actually_received"])
        fn = sum(1 for r in rows if r["annual_doc_id"] not in predicted_ids and r["inquiry_actually_received"])
        precision = _safe_ratio(tp, tp + fp)
        recall = _safe_ratio(tp, tp + fn)
        return {
            "predicted_positive": len(predicted_ids),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
        }

    def _compute_baselines(
        self, rows: list[dict[str, Any]], rule_matrix: dict[str, int]
    ) -> dict[str, Any]:
        """最简 baseline 对比：规则评分 vs 按资本化率排序 top20% vs 全标正。

        目的是回答「规则评分比随机/单变量排序好吗」。即使当前正样本极少、
        三者 precision/recall 都接近 0，也能诚实说明「在当前样本上无差异，信号不足」。
        """
        rule_ids = {r["annual_doc_id"] for r in rows if r.get("is_anomaly")}

        # baseline A: 按资本化率降序取 top20%（仅在可评分且有资本化率的记录上排序）
        cr_rows = [r for r in rows if r.get("capitalization_rate") is not None]
        cr_sorted = sorted(cr_rows, key=lambda r: r["capitalization_rate"], reverse=True)
        top_n = max(1, round(len(cr_sorted) * 0.2))
        cr_ids = {r["annual_doc_id"] for r in cr_sorted[:top_n]}

        # baseline B: 全标正（等价于随机恒判异常的下界 recall=1, precision=实际正例率）
        all_positive_ids = {r["annual_doc_id"] for r in rows}

        total = len(rows)
        positives = sum(1 for r in rows if r["inquiry_actually_received"])
        return {
            "purpose": "Compare rule scoring against a single-variable baseline (capitalization-rate top20%) and an all-positive baseline. With only 1 positive label all approaches score near zero; this honestly documents that the sample carries no usable signal rather than claiming the rule model 'works'.",
            "positive_count": positives,
            "evaluated_count": total,
            "rule_scoring": {
                **self._pr_for(rule_ids, rows),
                "tn": rule_matrix["tn"],
            },
            "cap_rate_top20pct": self._pr_for(cr_ids, rows),
            "all_positive": self._pr_for(all_positive_ids, rows),
        }
