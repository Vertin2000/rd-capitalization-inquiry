# Prompt v1 — 研发资本化字段抽取（初版）

> 本文件归档 prompt 初版，来源为 git 首版 `src/extract/llm_extractor.py`（commit `cd1bb9a`）的 `DEFAULT_PROMPT_TEMPLATE`。Week 15 讲义要求 `prompts/prompt_v1.md` 与 `prompt_final.md` 对照，展示 prompt 迭代过程。

## System 指令

v1 与 final 共用同一句 system 指令（`src/extract/llm_client.py` `call_json` 自动追加），整个相关时期稳定未变：

```text
你必须以有效的 JSON 格式输出，不要包含任何其他文本。
```

## User Prompt 模板（v1）

```text
你是一位资深财务分析师，擅长从上市公司年报中提取研发支出相关数据。

请从以下年报文本中提取以下字段，以 JSON 格式返回。

需要提取的字段（每个字段必须包含 value、evidence_text、page_no、confidence）：
- rd_expense_total: 研发支出总额（万元）
- rd_capitalized_amount: 资本化金额（万元）
- rd_expensed_amount: 费用化金额（万元）
- dev_cost_opening: 开发支出期初余额（万元）
- dev_cost_closing: 开发支出期末余额（万元）
- impairment: 减值准备（万元）
- capitalization_condition: 资本化条件描述（原文）

输出格式要求：
{{
  "company_name": "公司名称",
  "company_code": "股票代码（6位数字）",
  "year": 2023,
  "rd_expense_total": {{"value": 49896.36, "evidence_text": "研发投入合计 49,896.36 万元", "page_no": 156, "confidence": 0.95}},
  "rd_capitalized_amount": {{"value": 0, "evidence_text": "资本化金额 0 万元", "page_no": 156, "confidence": 0.90}},
  ...
}}

规则：
1. 金额单位为万元，如果原文为元请转换
2. 如果某字段无法找到，value 返回 null，evidence_text 说明原因
3. confidence 为 0-1 的浮点数，表示你对该字段提取结果的确信程度
4. page_no 为整数，如无法确定则填 null
5. 确保资本化金额 + 费用化金额 ≈ 总额

文本内容：
{section_text}

请直接返回 JSON，不要添加任何解释。
```

## v1 配置说明

Week 13 早期原型计划参数（见 `temp-队友做的东西原件/week13_extracted/week13/llm_parameters.md`，仅作历史参考）：

- `LLM_PROVIDER=siliconflow`
- `LLM_MODEL=Qwen/Qwen3-8B`
- `temperature=0`
- `max_tokens=2048`

> 注意：上述参数为早期计划记录，最终可靠性以当前代码实测为准。后续演进为 `Qwen/Qwen2.5-72B-Instruct` + Kimi Code CLI 后端。

## v1 的不足（驱动迭代的动机）

1. **缺 `capitalization_rate` 字段**：v1 不抽取资本化率，导致下游评分缺少该字段，需在校验阶段补算。
2. **Null 规则过于笼统**：v1 规则 2 只说「无法找到返回 null」，未区分「原文明确为 0」与「未披露」，易把披露为 0 的样本误标 null。
3. **未禁止口径混淆**：v1 没有「禁止把开发支出期末余额当作本期资本化金额」这条，存在把期末余额误当资本化金额的风险。

这些不足在 `prompt_final.md` 中通过新增字段和规则 2/3/4 修复。详见 `prompt_final.md` 的「与 prompt_v1 的差异」。
