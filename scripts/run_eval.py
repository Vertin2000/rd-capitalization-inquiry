"""人工评估脚本：抽取质量交叉验证 + 四类指标汇总。

评估口径（诚实分层）：
1. 程序交叉验证层（全 35 条 × 数值字段）：用 rd_table_extractor 的确定性表格值作 gold，
   与 extracted/validated 的 LLM 值比对。两条代码路径独立（LLM vs 确定性解析），
   共同错误只能由 parse 上游引入——这一点在局限性中说明。
2. AI 语义复核层（10 条子集）：派独立 AI agent 读原文 markdown，对数值字段和
   capitalization_condition 做语义核对。覆盖确定性提取器拿不到的文本字段与分歧样本。
3. Section / Evidence / Pipeline Quality：程序从 section_check_report / validated / run_log 算。

输出：
- outputs/reports/eval_per_field.csv（per-field 行，讲义固定字段 + error_type 枚举）
- outputs/reports/eval_report_final.md（五类指标汇总 + 局限性）

讲义依据：Week 15 10.2.1（评估字段、error_type 枚举）、Week 16 11.6（人工评估）。
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 确定性表格 row_label -> 评估字段名
# impairment 的 current_reductions 口径不等于 impairment 字段，不纳入程序交叉验证，
# 仅在 AI 复核层评估。
TABLE_FIELD_MAP = {
    ("rd_investment", "total_amount"): "rd_expense_total",
    ("rd_investment", "capitalized_amount"): "rd_capitalized_amount",
    ("rd_investment", "expensed_amount"): "rd_expensed_amount",
    ("rd_investment", "capitalization_rate"): "capitalization_rate",
    ("development_expenditure", "opening_balance"): "dev_cost_opening",
    ("development_expenditure", "closing_balance"): "dev_cost_closing",
}

# 程序层不评估的文本/口径不确定字段，仅 AI 复核层评
AI_ONLY_FIELDS = ["impairment", "capitalization_condition"]

# Week 15 讲义 error_type 固定枚举
ERROR_TYPES = {
    "data_error", "parse_error", "section_error", "prompt_error",
    "schema_error", "hallucination", "normalization_error",
    "workflow_error", "human_label_unclear",
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_table_gold() -> dict[str, dict[str, float]]:
    """doc_id -> {field: value}，取确定性表格值作 gold。"""
    rows = load_jsonl(PROJECT_ROOT / "data" / "extracted" / "tables" / "tables.jsonl")
    gold: dict[str, dict[str, float]] = {}
    for r in rows:
        field = TABLE_FIELD_MAP.get((r["table_type"], r["row_label"]))
        if not field or r.get("value") is None:
            continue
        gold.setdefault(r["doc_id"], {})[field] = float(r["value"])
    return gold


def load_predicted() -> dict[str, dict[str, Any]]:
    """doc_id -> {field: value}，从 validated 取 predicted。"""
    rows = load_jsonl(PROJECT_ROOT / "data" / "validated" / "records.jsonl")
    pred: dict[str, dict[str, Any]] = {}
    fields = list(TABLE_FIELD_MAP.values())
    for r in rows:
        pred[r["doc_id"]] = {f: r.get(f) for f in fields}
        pred[r["doc_id"]]["capitalization_condition"] = r.get("capitalization_condition")
    return pred


def values_match(pred: Any, gold: float, *, rel_tol: float = 0.05) -> bool:
    """数值相对误差 <= 5% 视为一致（容忍单位换算四舍五入与表格口径小差异）。"""
    if pred is None:
        return False
    try:
        p = float(pred)
    except (TypeError, ValueError):
        return False
    if gold == 0:
        return abs(p) < 1.0
    return abs(p - gold) / abs(gold) <= rel_tol


def classify_error(pred: Any, gold: float | None, *, predicted_has: bool, gold_has: bool) -> str:
    """按 Week 15 枚举判 error_type。"""
    if not gold_has and predicted_has and pred is not None:
        return "hallucination"  # gold 无值但模型填了
    if gold_has and not predicted_has:
        return "section_error"  # gold 有值但模型漏抽（多因 section 未定位到）
    if gold_has and predicted_has and not values_match(pred, gold):
        # 有值但不一致：判断是单位/归一化还是数据错误
        try:
            ratio = float(pred) / gold if gold else 0
            if ratio in (0.01, 0.0001, 100, 10000) or abs(ratio - 0.01) < 0.001:
                return "normalization_error"  # 单位未换算
        except (TypeError, ValueError, ZeroDivisionError):
            pass
        return "data_error"
    return ""


def build_per_field_rows(
    sample_ids: list[str],
    gold: dict[str, dict[str, float]],
    predicted: dict[str, dict[str, Any]],
    ai_review: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    fields = list(TABLE_FIELD_MAP.values())
    for doc_id in sample_ids:
        pred = predicted.get(doc_id, {})
        g = gold.get(doc_id, {})
        review = (ai_review or {}).get(doc_id, {})
        for field in fields:
            pred_val = pred.get(field)
            gold_val = g.get(field)
            gold_has = field in g
            pred_has = pred_val is not None
            is_correct = gold_has and pred_has and values_match(pred_val, gold_val)
            # gold 缺失：确定性提取器也没抽到，无法判定对错，不算错误、不计入分母
            if not gold_has:
                rows.append({
                    "doc_id": doc_id,
                    "field_name": field,
                    "predicted_value": pred_val,
                    "gold_value": "",
                    "is_correct": "unverified",
                    "evidence_correct": "n/a",
                    "error_type": "",
                    "notes": "gold缺失(确定性表格未抽到,交AI复核)",
                })
                continue
            error_type = "" if is_correct else classify_error(
                pred_val, gold_val, predicted_has=pred_has, gold_has=gold_has
            )
            # AI 复核覆盖（若有）：以 AI 判断覆盖 error_type
            if field in review:
                rv = review[field]
                if rv.get("override_error"):
                    error_type = rv["override_error"]
                if "is_correct" in rv:
                    is_correct = rv["is_correct"]
            rows.append({
                "doc_id": doc_id,
                "field_name": field,
                "predicted_value": pred_val,
                "gold_value": gold_val,
                "is_correct": "yes" if is_correct else "no",
                "evidence_correct": "n/a",  # 程序层不评 evidence 语义，AI 复核层覆盖
                "error_type": error_type or ("data_error" if not is_correct else ""),
                "notes": "gold=确定性表格值",
            })
        # capitalization_condition：文本字段，仅 AI 复核层评
        cond_pred = pred.get("capitalization_condition")
        rv = review.get("capitalization_condition")
        if rv:
            rows.append({
                "doc_id": doc_id,
                "field_name": "capitalization_condition",
                "predicted_value": "(文本)",
                "gold_value": "(AI复核原文)",
                "is_correct": "yes" if rv.get("is_correct") else "no",
                "evidence_correct": "yes" if rv.get("evidence_correct") else "no",
                "error_type": rv.get("override_error", "") or ("" if rv.get("is_correct") else "prompt_error"),
                "notes": rv.get("notes", "AI语义复核"),
            })
        # impairment：口径不确定（current_reductions ≠ impairment），仅 AI 复核层评
        rv_imp = review.get("impairment")
        if rv_imp:
            rows.append({
                "doc_id": doc_id,
                "field_name": "impairment",
                "predicted_value": pred.get("impairment"),
                "gold_value": rv_imp.get("gold_value"),
                "is_correct": "yes" if rv_imp.get("is_correct") else "no",
                "evidence_correct": "yes" if rv_imp.get("evidence_correct") else "no",
                "error_type": rv_imp.get("override_error", "") or ("" if rv_imp.get("is_correct") else "data_error"),
                "notes": rv_imp.get("notes", "AI语义复核(口径不确定)"),
            })
    return rows


def write_per_field_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "doc_id", "field_name", "predicted_value", "gold_value",
        "is_correct", "evidence_correct", "error_type", "notes",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def compute_extraction_quality(rows: list[dict[str, Any]]) -> dict[str, Any]:
    # 只对有 gold 且可判定的行算 accuracy（排除 unverified / 文本字段占位）
    judged = [r for r in rows if r["is_correct"] in ("yes", "no")]
    correct = sum(1 for r in judged if r["is_correct"] == "yes")
    by_field: dict[str, dict[str, int]] = {}
    by_error: dict[str, int] = {}
    for r in judged:
        f = r["field_name"]
        by_field.setdefault(f, {"total": 0, "correct": 0})
        by_field[f]["total"] += 1
        if r["is_correct"] == "yes":
            by_field[f]["correct"] += 1
        if r["error_type"]:
            by_error[r["error_type"]] = by_error.get(r["error_type"], 0) + 1
    return {
        "total_rows": len(rows),
        "judged": len(judged),
        "correct": correct,
        "accuracy": round(correct / len(judged), 4) if judged else None,
        "by_field": by_field,
        "error_distribution": by_error,
    }


def compute_evidence_quality() -> dict[str, Any]:
    rows = load_jsonl(PROJECT_ROOT / "data" / "extracted" / "records.jsonl")
    fields = list(TABLE_FIELD_MAP.values())
    total = 0
    non_empty = 0
    for r in rows:
        for f in fields:
            fe = r.get(f)
            if not isinstance(fe, dict):
                continue
            total += 1
            if fe.get("evidence_text"):
                non_empty += 1
    return {
        "evidence_fields_total": total,
        "evidence_non_empty": non_empty,
        "evidence_non_empty_rate": round(non_empty / total, 4) if total else None,
    }


def compute_section_quality() -> dict[str, Any]:
    csv_path = PROJECT_ROOT / "outputs" / "reports" / "section_check_report.csv"
    if not csv_path.exists():
        return {"available": False}
    found = 0
    not_found = 0
    issues: dict[str, int] = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["found"] == "yes":
                found += 1
            else:
                not_found += 1
            for tag in r["quality_issue"].split(";"):
                if tag:
                    issues[tag] = issues.get(tag, 0) + 1
    return {
        "available": True,
        "found_rows": found,
        "not_found_rows": not_found,
        "issue_distribution": issues,
    }


def compute_pipeline_stability() -> dict[str, Any]:
    log_path = PROJECT_ROOT / "outputs" / "logs" / "run_log.jsonl"
    if not log_path.exists():
        return {"available": False}
    by_step: dict[str, dict[str, float]] = {}
    for l in log_path.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        step = e["step"]
        by_step.setdefault(step, {"count": 0, "success": 0, "elapsed": 0.0})
        by_step[step]["count"] += 1
        if e["status"] == "success":
            by_step[step]["success"] += 1
        by_step[step]["elapsed"] += e.get("elapsed", 0)
    return {"available": True, "by_step": by_step}


def compute_data_quality() -> dict[str, Any]:
    audit_path = PROJECT_ROOT / "outputs" / "dataset_check_report.md"
    validated = load_jsonl(PROJECT_ROOT / "data" / "validated" / "records.jsonl")
    total = len(validated)
    cap_rate = sum(1 for r in validated if r.get("capitalization_rate") is not None)
    return {
        "audit_report_exists": audit_path.exists(),
        "validated_records": total,
        "capitalization_rate_available": cap_rate,
        "capitalization_rate_rate": round(cap_rate / total, 4) if total else None,
    }


def main() -> int:
    sample_ids = json.loads(
        (PROJECT_ROOT / "outputs" / "reports" / "eval_sample_doc_ids.json").read_text(encoding="utf-8")
    )
    gold = load_table_gold()
    predicted = load_predicted()

    # AI 复核结果（若已生成）
    ai_review_path = PROJECT_ROOT / "outputs" / "reports" / "eval_ai_review.json"
    ai_review: dict[str, dict[str, Any]] = {}
    if ai_review_path.exists():
        data = json.loads(ai_review_path.read_text(encoding="utf-8"))
        ai_review = {d: v for d, v in data.items()}

    rows = build_per_field_rows(sample_ids, gold, predicted, ai_review)
    write_per_field_csv(rows, PROJECT_ROOT / "outputs" / "reports" / "eval_per_field.csv")

    stats = {
        "sample_count": len(sample_ids),
        "extraction_quality": compute_extraction_quality(rows),
        "evidence_quality": compute_evidence_quality(),
        "section_quality": compute_section_quality(),
        "pipeline_stability": compute_pipeline_stability(),
        "data_quality": compute_data_quality(),
        "ai_review_covered": len(ai_review),
    }
    (PROJECT_ROOT / "outputs" / "reports" / "eval_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
