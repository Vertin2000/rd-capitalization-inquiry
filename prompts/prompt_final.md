# Prompt Final — 研发资本化字段抽取（最终版）

> 本文件是 `src/extract/llm_extractor.py` 当前 `DEFAULT_PROMPT_TEMPLATE` 的快照，作为 prompt 最终版归档（Week 15 讲义要求 `prompts/prompt_final.md`）。代码即真源，若代码变更请同步本文件。

## System 指令

由 `src/extract/llm_client.py` `call_json` 方法在每次调用时自动追加（无独立 system persona，persona 写在 user prompt 里）：

```text
你必须以有效的 JSON 格式输出，不要包含任何其他文本。
```

## User Prompt 模板

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
- capitalization_rate: 资本化率（%）
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
2. capitalization_rate 优先使用年报直接披露值；若没有披露，可返回 null，由校验阶段计算
3. 禁止把开发支出期末余额直接当作本期资本化金额
4. 原文明确为 0 时才能填 0；无法判断或未披露时 value 返回 null，evidence_text 说明原因
5. confidence 为 0-1 的浮点数，表示你对该字段提取结果的确信程度
6. page_no 为整数，如无法确定则填 null
7. 确保资本化金额 + 费用化金额 ≈ 总额

文本内容：
{section_text}

请直接返回 JSON，不要添加任何解释。
```

## 调用说明

- **占位符**：`{section_text}` 由 `LLMExtractor._build_prompt` 注入。
- **章节挑选**：按 `match_score` 降序挑选章节切片；单段超过 `MAX_SECTION_CHARS=4000` 字符截断；合计超过 `MAX_COMBINED_SECTION_CHARS=16000` 字符截断；多段用 `\n\n---\n\n` 拼接。
- **后端**：
  - HTTP（默认）：`messages=[{system: json_system}, {user: 模板}]`，走 `LLM_BASE_URL`（默认 `https://api.siliconflow.cn`）。
  - Kimi Code CLI（`LLM_BACKEND=kimi_code_cli`）：system + user 合并为单条文本 `"系统指令：\n{system}\n\n用户任务：\n{user}"`，通过 `-p` 传给 kimi CLI。
- **模型参数**：默认 `Qwen/Qwen2.5-72B-Instruct`，`temperature=0`，`max_tokens=2048`，可通过 `.env` 的 `LLM_MODEL` / `LLM_BASE_URL` / `LLM_API_KEY` 覆盖。

## 与 prompt_v1 的差异

1. 新增字段 `capitalization_rate: 资本化率（%）`。
2. 规则从 5 条扩到 7 条：
   - 原 v1 规则 2「无法找到返回 null」拆为规则 2（capitalization_rate 披露值优先）+ 规则 4（明确 0 才填 0）。
   - 新增规则 3「禁止把开发支出期末余额直接当作本期资本化金额」。
3. 模型从 v1 计划的 `Qwen/Qwen3-8B` 演进为 `Qwen/Qwen2.5-72B-Instruct`，并新增 Kimi Code CLI 后端。

详见 `prompt_v1.md`。
