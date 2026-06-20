"""Schema 测试"""

from __future__ import annotations

import pytest
from model.schemas import (
    FieldEvidence,
    InquiryLoopRecord,
    LoopEvaluationResult,
    RDCapitalizationRecord,
    ScoringResult,
    SectionSlice,
)


# -------------------------------------------------------------------------- #
# FieldEvidence
# -------------------------------------------------------------------------- #

def test_field_evidence_basic():
    fe = FieldEvidence(
        value=49896.36,
        evidence_text="研发投入合计 49,896.36 万元",
        page_no=156,
        confidence=0.95,
    )
    assert fe.value == 49896.36
    assert fe.evidence_text == "研发投入合计 49,896.36 万元"
    assert fe.page_no == 156
    assert fe.confidence == 0.95


def test_field_evidence_null_value():
    fe = FieldEvidence(value=None, evidence_text="未找到该字段")
    assert fe.value is None
    assert fe.page_no is None
    assert fe.confidence is None


def test_field_evidence_string_value():
    fe = FieldEvidence(
        value="资本化条件：完成该无形资产以使其能够使用或出售"
    )
    assert isinstance(fe.value, str)


# -------------------------------------------------------------------------- #
# SectionSlice
# -------------------------------------------------------------------------- #

def test_section_slice_basic():
    slice_obj = SectionSlice(
        doc_id="600276_2023-04-22_79eb2720",
        section_name="研发费用",
        matched_keyword="研发投入",
        text="本年度研发投入合计 49,896.36 万元...",
        line_start=245,
        line_end=312,
        page_hint=45,
    )
    assert slice_obj.doc_id == "600276_2023-04-22_79eb2720"
    assert slice_obj.section_name == "研发费用"
    assert slice_obj.line_start == 245
    assert slice_obj.page_hint == 45


def test_section_slice_optional_page_hint():
    slice_obj = SectionSlice(
        doc_id="600276_2023",
        section_name="开发支出",
        matched_keyword="开发支出",
        text="开发支出期初余额...",
        line_start=400,
        line_end=420,
    )
    assert slice_obj.page_hint is None


# -------------------------------------------------------------------------- #
# RDCapitalizationRecord
# -------------------------------------------------------------------------- #

def test_rd_capitalization_record_basic():
    record = RDCapitalizationRecord(
        doc_id="600276_2023",
        company_name="恒瑞医药",
        company_code="600276",
        year=2023,
        rd_expense_total=10000.0,
        rd_capitalized_amount=2000.0,
        rd_expensed_amount=8000.0,
        evidence_text="研发支出总额10,000万元，其中资本化2,000万元",
        page_no=156,
        source_pdf_path="data/pdf/600276_2023.pdf",
    )

    assert record.company_code == "600276"
    assert record.year == 2023
    assert record.capitalization_rate == 20.0
    assert record.calculated_capitalization_rate == 20.0


def test_rd_capitalization_record_auto_calculate_rate():
    """测试自动计算资本化率"""
    record = RDCapitalizationRecord(
        doc_id="test",
        company_name="测试公司",
        company_code="000001",
        year=2023,
        rd_expense_total=5000.0,
        rd_capitalized_amount=1000.0,
        evidence_text="test",
        page_no=1,
        source_pdf_path="test.pdf",
    )

    assert record.capitalization_rate == 20.0


def test_rd_capitalization_record_null_fields():
    """测试 Null 字段允许"""
    record = RDCapitalizationRecord(
        doc_id="test_null",
        company_name="测试公司",
        company_code="000001",
        year=2023,
        rd_expense_total=None,
        rd_capitalized_amount=None,
        evidence_text="数据缺失",
        page_no=1,
        source_pdf_path="test.pdf",
        null_reason="年报中未披露研发支出明细",
    )

    assert record.capitalization_rate is None
    assert record.null_reason is not None


def test_rd_capitalization_record_extended_fields():
    """测试扩展评分字段"""
    record = RDCapitalizationRecord(
        doc_id="600276_2023",
        company_name="恒瑞医药",
        company_code="600276",
        year=2023,
        rd_expense_total=10000.0,
        rd_capitalized_amount=5000.0,
        aggressiveness_score=85.5,
        is_anomaly=True,
        anomaly_type="industry_outlier",
        evidence_text="test",
        page_no=1,
        source_pdf_path="test.pdf",
    )

    assert record.aggressiveness_score == 85.5
    assert record.is_anomaly is True
    assert record.anomaly_type == "industry_outlier"


def test_rd_capitalization_record_default_evidence():
    """测试 evidence_text 和 page_no 有默认值"""
    record = RDCapitalizationRecord(
        doc_id="test_defaults",
        company_name="测试公司",
        company_code="000001",
        year=2023,
        source_pdf_path="test.pdf",
    )
    assert record.evidence_text == ""
    assert record.page_no == 0


# -------------------------------------------------------------------------- #
# InquiryLoopRecord
# -------------------------------------------------------------------------- #

def test_inquiry_loop_record_auto_prediction():
    """测试自动计算预测结果分类"""
    # TP: 预测异常且实际被问询
    tp = InquiryLoopRecord(
        stock_code="600276",
        year=2023,
        annual_doc_id="600276_2023",
        anomaly_predicted_inquiry=True,
        inquiry_actually_received=True,
    )
    assert tp.prediction_result == "TP"

    # FP: 预测异常但实际未被问询
    fp = InquiryLoopRecord(
        stock_code="600276",
        year=2023,
        annual_doc_id="600276_2023",
        anomaly_predicted_inquiry=True,
        inquiry_actually_received=False,
    )
    assert fp.prediction_result == "FP"

    # TN: 预测正常且实际未被问询
    tn = InquiryLoopRecord(
        stock_code="600276",
        year=2023,
        annual_doc_id="600276_2023",
        anomaly_predicted_inquiry=False,
        inquiry_actually_received=False,
    )
    assert tn.prediction_result == "TN"

    # FN: 预测正常但实际被问询
    fn = InquiryLoopRecord(
        stock_code="600276",
        year=2023,
        annual_doc_id="600276_2023",
        anomaly_predicted_inquiry=False,
        inquiry_actually_received=True,
    )
    assert fn.prediction_result == "FN"


# -------------------------------------------------------------------------- #
# ScoringResult / LoopEvaluationResult
# -------------------------------------------------------------------------- #

def test_scoring_result():
    result = ScoringResult(
        company_code="600276",
        year=2023,
        industry_percentile=0.95,
        change_score=20.0,
        fuzziness_score=15.0,
        identity_score=25.0,
        total_score=85.0,
    )

    assert result.total_score == 85.0


def test_loop_evaluation_result():
    result = LoopEvaluationResult(
        total=50,
        tp=10,
        fp=5,
        tn=30,
        fn=5,
        precision=0.667,
        recall=0.667,
        f1=0.667,
    )

    assert result.total == 50
    assert result.f1 == pytest.approx(0.667, rel=1e-3)
