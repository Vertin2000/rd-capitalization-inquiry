"""研发资本化数据抽取 Schema

定义 Pydantic 模型用于校验抽取结果，支持扩展方案（评分模型 + 问询函闭环）。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, computed_field


class FieldEvidence(BaseModel):
    """字段级证据追溯结构

    用于 extract 阶段输出，每个核心字段包含独立的值、证据文本、页码和置信度。
    """

    value: float | str | None = Field(
        default=None, description="字段值（数值或文本）"
    )
    evidence_text: str = Field(
        default="", description="证据原文片段"
    )
    page_no: int | None = Field(
        default=None, description="所在页码（MinerU 可能缺失）"
    )
    confidence: float | None = Field(
        default=None, description="置信度（0-1，由 LLM 自评或规则估算）"
    )


class SectionSlice(BaseModel):
    """章节切片结构

    用于 route 阶段输出，记录从 Markdown 中提取的章节文本片段。
    """

    doc_id: str = Field(description="文档唯一标识")
    section_name: str = Field(description="规则匹配到的章节名称")
    matched_keyword: str = Field(description="实际命中的关键词")
    text: str = Field(description="切片后的完整 Markdown 文本")
    line_start: int = Field(description="在原始 Markdown 中的起始行号")
    line_end: int = Field(description="在原始 Markdown 中的结束行号")
    page_hint: int | None = Field(
        default=None, description="页码提示（MinerU 可能缺失）"
    )
    match_score: float | None = Field(
        default=None, description="章节候选匹配分数，用于 route 人工抽查"
    )
    match_reason: str = Field(
        default="", description="章节候选入选原因摘要"
    )


class RDCapitalizationRecord(BaseModel):
    """单家公司研发资本化数据记录（基础层）

    用于 validate 及之后阶段的标准记录格式。
    核心字段为扁平数值类型，便于评分和计算。
    evidence_text / page_no 为记录级回退字段（兼容 extract 展平后的数据）。
    """

    doc_id: str = Field(description="文档唯一标识")
    company_name: str = Field(description="公司名称")
    company_code: str = Field(description="股票代码")
    year: int = Field(description="年报年份")

    # 核心研发数据
    # 口径优先级（必须严格遵循，无法确认时输出 null）：
    #   1. 优先使用年报"研发投入"章节中披露的"研发投入合计"
    #   2. 次选"研发费用"科目金额（利润表）
    #   3. 无法确认时输出 null，不强行计算
    rd_expense_total: float | None = Field(
        description="研发支出总额（万元）= 资本化金额 + 费用化金额 + 减值准备", default=None
    )

    # 口径优先级（必须严格遵循，无法确认时输出 null）：
    #   1. 优先使用年报"研发投入"章节中直接披露的"资本化金额"
    #   2. 次选开发支出附注中"本期增加——资本化金额"
    #   3. 若附注中仅列"开发支出本期增加"未区分资本化/费用化，输出 null
    #   4. 禁止将"开发支出期末余额"直接当作"本期资本化金额"
    #   5. 无法确认时输出 null，不强行计算
    rd_capitalized_amount: float | None = Field(
        description="研发投入资本化金额（万元）", default=None
    )

    # 口径优先级：
    #   1. 优先使用年报"研发投入"章节中直接披露的"费用化金额"
    #   2. 次选"研发费用"科目金额（利润表）减去资本化部分
    #   3. 无法确认时输出 null
    rd_expensed_amount: float | None = Field(
        description="研发投入费用化金额（万元）", default=None
    )
    dev_cost_opening: float | None = Field(
        description="开发支出期初余额（万元）", default=None
    )
    dev_cost_closing: float | None = Field(
        description="开发支出期末余额（万元）", default=None
    )
    impairment: float | None = Field(
        description="减值准备（万元）", default=None
    )

    # 计算字段
    # 计算公式：capitalization_rate = rd_capitalized_amount / (rd_capitalized_amount + rd_expensed_amount) * 100
    # 校验规则：若 rd_expense_total 已提供，则 capitalization_rate 应约等于 rd_capitalized_amount / rd_expense_total * 100
    # 差异 > 5% 时标记 identity_check_score 异常
    capitalization_rate: float | None = Field(
        description="资本化率（%）= 资本化金额 / (资本化金额 + 费用化金额) × 100", default=None
    )
    prev_year_rate: float | None = Field(
        description="上一年资本化率（%）", default=None
    )
    change_pct: float | None = Field(
        description="资本化率年度变化（百分点）", default=None
    )

    # 文本字段
    capitalization_condition: str | None = Field(
        description="资本化条件描述", default=None
    )

    # 证据追溯（记录级回退字段）
    evidence_text: str = Field(default="", description="证据原文片段")
    page_no: int = Field(default=0, description="页码")
    source_pdf_path: str = Field(description="原始PDF路径")
    null_reason: str | None = Field(
        description="字段缺失原因说明", default=None
    )

    # 扩展方案：评分模型字段
    industry_percentile: float | None = Field(
        description="行业百分位（0-1）", default=None
    )
    change_zscore: float | None = Field(
        description="跨期变化Z分数", default=None
    )
    fuzziness_score: float | None = Field(
        description="条件模糊度评分（0-1）", default=None
    )
    identity_check_score: float | None = Field(
        description="会计恒等式验证得分（0-1）", default=None
    )
    aggressiveness_score: float | None = Field(
        description="激进程度总分（0-100）", default=None
    )

    # 扩展方案：异常标记
    is_anomaly: bool | None = Field(
        description="是否标记为异常", default=None
    )
    anomaly_type: Literal[
        "industry_outlier",
        "change_spike",
        "fuzziness",
        "identity_error",
        "multiple",
    ] | None = Field(description="异常类型", default=None)

    @computed_field
    @property
    def calculated_capitalization_rate(self) -> float | None:
        """自动计算资本化率（用于校验）

        优先使用 资本化 / 总额（rd_expense_total）校验，
        若 rd_expense_total 缺失，则退化为 资本化 / (资本化 + 费用化)。
        """
        if self.rd_capitalized_amount is None:
            return None

        # 优先分母：rd_expense_total（研发支出总额）
        if self.rd_expense_total is not None and self.rd_expense_total > 0:
            return round(
                self.rd_capitalized_amount / self.rd_expense_total * 100, 2
            )

        # 退化分母：资本化 + 费用化
        if (
            self.rd_expensed_amount is not None
            and self.rd_capitalized_amount + self.rd_expensed_amount > 0
        ):
            total = self.rd_capitalized_amount + self.rd_expensed_amount
            return round(self.rd_capitalized_amount / total * 100, 2)

        return None

    def model_post_init(self, __context: object) -> None:
        """初始化后自动计算资本化率（如果未提供）"""
        if self.capitalization_rate is None:
            calculated = self.calculated_capitalization_rate
            if calculated is not None:
                self.capitalization_rate = calculated


class InquiryLoopRecord(BaseModel):
    """问询函闭环记录（关联层）"""

    # 关联键
    stock_code: str = Field(description="股票代码")
    year: int = Field(description="年报年份")

    # 年报侧
    annual_doc_id: str = Field(description="年报文档ID")
    capitalization_rate: float | None = Field(
        description="资本化率", default=None
    )
    aggressiveness_score: float | None = Field(
        description="激进程度评分", default=None
    )
    is_anomaly: bool | None = Field(
        description="是否被标记为异常", default=None
    )

    # 问询函侧
    inquiry_doc_id: str | None = Field(
        description="问询函文档ID", default=None
    )
    inquiry_title: str | None = Field(
        description="问询函标题", default=None
    )
    inquiry_date: str | None = Field(
        description="问询日期", default=None
    )
    inquiry_keywords: list[str] | None = Field(
        description="问询关键词", default=None
    )
    inquiry_questions: list[str] | None = Field(
        description="问询关键问题列表", default=None
    )

    # 回复侧
    reply_doc_id: str | None = Field(
        description="回复函文档ID", default=None
    )
    reply_date: str | None = Field(
        description="回复日期", default=None
    )
    reply_summary: str | None = Field(
        description="回复核心内容摘要", default=None
    )
    reply_satisfactory: float | None = Field(
        description="回复充分性评分（1-5）", default=None
    )

    # 闭环评估
    anomaly_predicted_inquiry: bool = Field(
        description="异常模型预测'应该被问询'", default=False
    )
    inquiry_actually_received: bool = Field(
        description="实际是否收到研发资本化相关问询（与 capitalization_related 同义，保留兼容）",
        default=False,
    )
    inquiry_received: bool = Field(
        description="是否收到任何问询函/关注函/监管工作函候选", default=False
    )
    reply_received: bool = Field(
        description="是否存在回复函/延期公告/专项说明等回应类公告", default=False
    )
    capitalization_related: bool = Field(
        description="收到的监管函件是否实质针对研发资本化/开发支出/无形资产确认", default=False
    )
    capitalization_confidence: float | None = Field(
        description="capitalization_related 的置信度（1.0=Tier-1关键词，<1.0=LLM置信度）",
        default=None,
    )
    capitalization_evidence: str | None = Field(
        description="LLM 或关键词给出的判断依据片段", default=None
    )
    capitalization_aspect: str | None = Field(
        description="资本化相关维度：资本化条件/开发支出/无形资产/费用化口径/其他", default=None
    )
    prediction_result: Literal["TP", "FP", "TN", "FN"] | None = Field(
        description="预测结果分类", default=None
    )

    def model_post_init(self, __context: object) -> None:
        """自动计算预测结果分类"""
        if self.prediction_result is None:
            if self.anomaly_predicted_inquiry and self.inquiry_actually_received:
                self.prediction_result = "TP"
            elif self.anomaly_predicted_inquiry and not self.inquiry_actually_received:
                self.prediction_result = "FP"
            elif not self.anomaly_predicted_inquiry and not self.inquiry_actually_received:
                self.prediction_result = "TN"
            elif not self.anomaly_predicted_inquiry and self.inquiry_actually_received:
                self.prediction_result = "FN"


class ScoringResult(BaseModel):
    """评分结果"""

    company_code: str
    year: int
    industry_percentile: float
    change_score: float
    fuzziness_score: float
    identity_score: float
    total_score: float


class LoopEvaluationResult(BaseModel):
    """闭环评估结果"""

    total: int
    tp: int
    fp: int
    tn: int
    fn: int
    precision: float
    recall: float
    f1: float
