"""Tests for quick downstream workflow scaffold."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _base_record(
    doc_id: str,
    code: str,
    year: int,
    rate: float | None,
) -> dict:
    return {
        "doc_id": doc_id,
        "company_name": f"公司{code}",
        "company_code": code,
        "year": year,
        "rd_expense_total": 100.0 if rate is not None else None,
        "rd_capitalized_amount": rate if rate is not None else None,
        "rd_expensed_amount": 100.0 - rate if rate is not None else None,
        "dev_cost_opening": None,
        "dev_cost_closing": None,
        "impairment": None,
        "capitalization_rate": rate,
        "prev_year_rate": None,
        "change_pct": None,
        "capitalization_condition": "满足条件后资本化" if rate is not None else None,
        "evidence_text": "sample",
        "page_no": 1,
        "source_pdf_path": f"data/pdf/{doc_id}.pdf",
        "null_reason": None if rate is not None else "TODO: waiting for extract",
        "industry_percentile": None,
        "change_zscore": None,
        "fuzziness_score": None,
        "identity_check_score": None,
        "aggressiveness_score": None,
        "is_anomaly": None,
        "anomaly_type": None,
        "calculated_capitalization_rate": rate,
    }


def test_scorer_handles_missing_values_and_writes_partial_scores(tmp_path: Path) -> None:
    from src.analysis.scorer import RiskScorer

    input_path = tmp_path / "data" / "validated" / "records.jsonl"
    output_path = tmp_path / "data" / "scored" / "records.jsonl"
    _write_jsonl(
        input_path,
        [
            _base_record("600276_恒瑞医药_2021年报", "600276", 2021, 10.0),
            _base_record("600276_恒瑞医药_2022年报", "600276", 2022, 30.0),
            _base_record("000001_缺字段_2022年报", "000001", 2022, None),
        ],
    )

    stats = RiskScorer(input_path=input_path, output_path=output_path).run()

    rows = _read_jsonl(output_path)
    assert stats == {"total": 3, "scored": 2, "partial": 1}
    assert rows[1]["prev_year_rate"] == 10.0
    assert rows[1]["change_pct"] == 20.0
    assert rows[1]["aggressiveness_score"] is not None
    assert rows[2]["aggressiveness_score"] is None
    assert "TODO: waiting for extract" in ";".join(rows[2]["data_quality_notes"])


def test_scorer_downward_change_does_not_raise_score(tmp_path: Path) -> None:
    """P1-2: 资本化率下降（如项目完结转无形资产）不应被算作激进。"""
    from src.analysis.scorer import RiskScorer

    input_path = tmp_path / "data" / "validated" / "records.jsonl"
    output_path = tmp_path / "data" / "scored" / "records.jsonl"
    # 公司 A：2021 资本化率 80%，2022 降到 0%（项目完结，非激进）
    # 公司 B：2021 资本化率 0%，2022 升到 80%（典型激进）
    _write_jsonl(
        input_path,
        [
            _base_record("600276_A_2021年报", "600276", 2021, 80.0),
            _base_record("600276_A_2022年报", "600276", 2022, 0.0),
            _base_record("600277_B_2021年报", "600277", 2021, 0.0),
            _base_record("600277_B_2022年报", "600277", 2022, 80.0),
        ],
    )

    RiskScorer(input_path=input_path, output_path=output_path).run()
    rows = {r["doc_id"]: r for r in _read_jsonl(output_path)}

    # A 公司 2022 资本化率骤降，change_zscore 为负，change_score 应为 0（不激进）
    a_2022 = rows["600276_A_2022年报"]
    assert a_2022["change_zscore"] is not None
    assert a_2022["change_zscore"] < 0
    # B 公司 2022 资本化率骤升，change_zscore 为正，应贡献正向 change_score
    b_2022 = rows["600277_B_2022年报"]
    assert b_2022["change_zscore"] is not None
    assert b_2022["change_zscore"] > 0
    # 对称的 abs() 会让两者 change 分相等；正向修复后 B 的风险分应高于 A
    assert b_2022["aggressiveness_score"] > a_2022["aggressiveness_score"]


def test_fuzziness_excludes_high_frequency_words(tmp_path: Path) -> None:
    """P1-1: 「等/相关/未来」等高频正向词不应触发模糊度。"""
    from src.analysis.scorer import _fuzziness_score, FUZZY_KEYWORDS

    # 高频词不应在词表里
    for word in ("等", "相关", "未来", "合理", "预计"):
        assert word not in FUZZY_KEYWORDS, f"{word} 不应在模糊词表中"
    # CAS6 合规披露（含「未来」）不应被判高模糊
    compliant = "未来经济利益很可能流入企业，完成该无形资产以使其能够使用或出售"
    assert _fuzziness_score(compliant) is not None
    assert _fuzziness_score(compliant) <= 0.2


def test_detector_marks_top_scores_and_writes_csv(tmp_path: Path) -> None:
    from src.analysis.detector import AnomalyDetector

    scored_path = tmp_path / "data" / "scored" / "records.jsonl"
    anomaly_path = tmp_path / "data" / "anomaly" / "anomaly_list.csv"
    _write_jsonl(
        scored_path,
        [
            {"doc_id": "a", "company_code": "000001", "year": 2021, "aggressiveness_score": 10.0},
            {"doc_id": "b", "company_code": "000002", "year": 2021, "aggressiveness_score": 90.0},
            {"doc_id": "c", "company_code": "000003", "year": 2021, "aggressiveness_score": None},
        ],
    )

    stats = AnomalyDetector(
        input_path=scored_path,
        output_path=scored_path,
        anomaly_path=anomaly_path,
        anomaly_percentile=0.80,
    ).run()

    rows = _read_jsonl(scored_path)
    with anomaly_path.open("r", encoding="utf-8", newline="") as f:
        anomaly_rows = list(csv.DictReader(f))
    assert stats == {"total": 3, "anomalies": 1, "unscored": 1}
    assert rows[1]["is_anomaly"] is True
    assert rows[2]["is_anomaly"] is False
    assert "TODO: waiting for score" in ";".join(rows[2]["data_quality_notes"])
    assert anomaly_rows[0]["doc_id"] == "b"


def test_inquiry_labeler_covers_all_annual_records(tmp_path: Path) -> None:
    from src.analysis.inquiry_labeler import InquiryLabeler

    metadata_path = tmp_path / "data" / "metadata" / "metadata.csv"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        "doc_id,stock_code,stock_name,publish_date\n"
        "ann1,600276,恒瑞医药,2022-04-20\n"
        "ann2,000001,平安银行,2022-04-21\n",
        encoding="utf-8",
    )
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_path.write_text(
        "annual_doc_id,report_year,doc_id,stock_code,stock_name,announcement_title,document_role,publish_date,pdf_title\n"
        "ann1,2021,inq1,600276,恒瑞医药,关于研发资本化事项的问询函,inquiry_notice,2022-05-01,关于研发资本化事项的问询函\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "data" / "inquiry" / "inquiry_records.jsonl"

    stats = InquiryLabeler(
        metadata_path=metadata_path,
        candidates_path=candidates_path,
        output_path=output_path,
    ).run()

    rows = _read_jsonl(output_path)
    assert stats == {"total": 2, "with_candidates": 1, "related": 1}
    assert {row["annual_doc_id"] for row in rows} == {"ann1", "ann2"}
    assert rows[0]["inquiry_actually_received"] is True
    assert rows[1]["inquiry_actually_received"] is False


def test_inquiry_labeler_uses_pdf_text_for_relevance(tmp_path: Path) -> None:
    from src.analysis.inquiry_labeler import InquiryLabeler

    metadata_path = tmp_path / "data" / "metadata" / "metadata.csv"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        "doc_id,stock_code,stock_name,publish_date\n"
        "ann1,600276,恒瑞医药,2022-04-20\n",
        encoding="utf-8",
    )
    candidates_path = tmp_path / "data" / "inquiry" / "inquiry_candidates.csv"
    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_path.write_text(
        "annual_doc_id,report_year,doc_id,stock_code,stock_name,announcement_title,document_role,publish_date,pdf_title,local_pdf_path\n"
        "ann1,2021,inq1,600276,恒瑞医药,关于年度报告的信息披露监管工作函,regulatory_work_letter,2022-05-01,监管工作函,data/inquiry/pdf/inq1.pdf\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "data" / "inquiry" / "inquiry_records.jsonl"

    def fake_pdf_text(_path: Path) -> str:
        return "请公司说明研发投入资本化金额、开发支出转入无形资产的依据。"

    stats = InquiryLabeler(
        metadata_path=metadata_path,
        candidates_path=candidates_path,
        output_path=output_path,
        project_root=tmp_path,
        pdf_text_extractor=fake_pdf_text,
    ).run()

    rows = _read_jsonl(output_path)
    assert stats == {"total": 1, "with_candidates": 1, "related": 1}
    assert rows[0]["inquiry_actually_received"] is True
    # Tier-1 keywords should be present; exact order depends on implementation.
    assert set(rows[0]["inquiry_keywords"]) >= {"资本化", "开发支出"}
    assert rows[0]["inquiry_questions"]


def test_evaluator_and_reporter_generate_partial_outputs(tmp_path: Path) -> None:
    from src.analysis.evaluator import LoopEvaluator
    from src.analysis.reporter import FinalReporter

    scored_path = tmp_path / "data" / "scored" / "records.jsonl"
    inquiry_path = tmp_path / "data" / "inquiry" / "inquiry_records.jsonl"
    evaluation_path = tmp_path / "outputs" / "loop_evaluation.json"
    report_path = tmp_path / "outputs" / "final_report.md"
    _write_jsonl(
        scored_path,
        [
            {
                "doc_id": "ann1",
                "company_code": "600276",
                "company_name": "恒瑞医药",
                "year": 2021,
                "capitalization_rate": 30.0,
                "aggressiveness_score": 90.0,
                "is_anomaly": True,
            },
            {
                "doc_id": "ann2",
                "company_code": "000001",
                "company_name": "平安银行",
                "year": 2021,
                "capitalization_rate": None,
                "aggressiveness_score": None,
                "is_anomaly": False,
            },
        ],
    )
    _write_jsonl(
        inquiry_path,
        [
            {"annual_doc_id": "ann1", "inquiry_actually_received": True},
            {"annual_doc_id": "ann2", "inquiry_actually_received": False},
        ],
    )

    eval_stats = LoopEvaluator(
        scored_path=scored_path,
        inquiry_path=inquiry_path,
        output_path=evaluation_path,
    ).run()
    report_stats = FinalReporter(
        evaluation_path=evaluation_path,
        scored_path=scored_path,
        report_path=report_path,
    ).run()

    evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
    report = report_path.read_text(encoding="utf-8")
    assert eval_stats["total"] == 2
    assert evaluation["confusion_matrix"]["tp"] == 1
    assert report_stats == {"written": 1}
    assert "## 数据质量说明" in report
    assert "Full annual sample is joined" in report
    assert "## 课堂展示摘要" in report
    assert "## Pipeline 完成度" in report
    assert "## 研究问题与方法" in report

    # baselines 对比 + TN 水分（P2-1/P2-2）
    assert "baselines" in evaluation
    bl = evaluation["baselines"]
    assert bl["positive_count"] == 1
    # 规则评分：ann1 是 TP
    assert bl["rule_scoring"]["tp"] == 1
    assert bl["rule_scoring"]["precision"] == 1.0
    # 按资本化率 top20%：ann1 唯一有 cap_rate，命中 → TP
    assert bl["cap_rate_top20pct"]["tp"] == 1
    # 全标正：recall=1, precision=正例率
    assert bl["all_positive"]["recall"] == 1.0
    assert bl["all_positive"]["precision"] == 0.5
    # TN 水分：ann2 无风险分被默认归非异常
    tw = evaluation["tn_water"]
    assert tw["tn_total"] == 1
    assert tw["tn_unscored_defaulted_non_anomaly"] == 1


def test_main_dispatches_downstream_stages(monkeypatch) -> None:
    import src.main as main

    calls = []

    monkeypatch.setattr(main, "run_score", lambda: calls.append("score") or 0)
    monkeypatch.setattr(main, "run_detect", lambda: calls.append("detect") or 0)
    monkeypatch.setattr(
        main,
        "run_inquiry_label",
        lambda: calls.append("inquiry-label") or 0,
    )
    monkeypatch.setattr(main, "run_analyze", lambda: calls.append("analyze") or 0)
    monkeypatch.setattr(main, "run_report", lambda: calls.append("report") or 0)

    for stage in ["score", "detect", "inquiry-label", "analyze", "report"]:
        assert stage in main.IMPLEMENTED
        assert main.run_stage(stage) == 0

    assert calls == ["score", "detect", "inquiry-label", "analyze", "report"]
