# Output Sample

## 目标输出说明

- **格式**：JSONL（每行一条 JSON 记录）
- **每条记录对应的公告粒度**：一家公司的一个会计年度
- **每条记录是否需要 evidence**：是，每个关键字段需提供 `evidence_text` 和 `page_no`

## 示例表格

### RDCapitalizationRecord（基础层）

| doc_id | company_name | company_code | year | rd_expense_total | rd_capitalized_amount | rd_expensed_amount | capitalization_rate | evidence_text | page_no |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | --------: |
| 600276_2023_annual | 恒瑞医药 | 600276 | 2023 | 49800.0 | 15000.0 | 34800.0 | 30.12 | "报告期内，公司研发投入合计49,800万元，其中费用化34,800万元，资本化15,000万元" | 145 |
| 300760_2023_annual | 迈瑞医疗 | 300760 | 2023 | 356000.0 | 0.0 | 356000.0 | 0.0 | "公司研发支出全部费用化，计入当期损益" | 132 |

### ScoringResult（评分层）

| company_code | year | industry_percentile | change_score | fuzziness_score | identity_score | total_score |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| 600276 | 2023 | 0.85 | 0.60 | 0.40 | 0.95 | 70.0 |
| 300760 | 2023 | 0.10 | 0.00 | 0.00 | 1.00 | 2.5 |

### InquiryLoopRecord（闭环层）

| stock_code | year | annual_doc_id | aggressiveness_score | is_anomaly | inquiry_title | inquiry_date | reply_satisfactory | prediction_result |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| 600276 | 2023 | 600276_2023_annual | 70.0 | true | 关于研发支出资本化的问询函 | 2024-05-15 | 3.5 | TP |
| 300760 | 2023 | 300760_2023_annual | 2.5 | false | null | null | null | TN |

## 字段解释

| 字段 | 类型 | 是否必填 | 金融含义 | 如何判断对错 |
| -------- | -------- | -------- | -------- | -------- |
| `company_name` | str | 是 | 公司名称 | 与年报封面一致 |
| `company_code` | str | 是 | 股票代码 | 6 位数字 |
| `year` | int | 是 | 年报年份 | 2021-2023 |
| `rd_expense_total` | float | 是 | 研发支出总额（万元） | 应为正数，等于资本化 + 费用化 |
| `rd_capitalized_amount` | float | 是 | 资本化金额（万元） | 可为 0，不应大于总额 |
| `rd_expensed_amount` | float | 是 | 费用化金额（万元） | 可为 0，不应大于总额 |
| `capitalization_rate` | float | 是 | 资本化率（%） | 资本化 / (资本化 + 费用化) × 100 |
| `aggressiveness_score` | float | 否 | 激进程度评分（0-100） | 越高越激进 |
| `is_anomaly` | bool | 否 | 是否异常 | 基于评分阈值 + 统计离群点 |
| `prediction_result` | str | 否 | TP/FP/TN/FN | 模型预测 vs 实际问询的匹配结果 |

## 资本化率口径优先级（必须严格遵循）

| 优先级 | 数据来源 | 字段 | 说明 |
| ------ | -------- | ---- | ---- |
| **1（优先）** | 年报"研发投入"章节 | `rd_capitalized_amount` | 直接使用年报披露的"研发投入资本化金额" |
| **2（次选）** | 开发支出附注 | `rd_capitalized_amount` | 使用"本期增加——资本化金额" |
| **3（退化）** | 无法确认 | — | 输出 `null`，**禁止强行计算** |

**禁止行为**：

- 禁止将"开发支出期末余额"直接当作"本期资本化金额"
- 禁止将"研发费用"（利润表科目）直接当作"资本化金额"
- 禁止在口径不明确时自行估算

**计算公式**（仅在三项数据均明确时执行）：

```python
capitalization_rate = rd_capitalized_amount / (rd_capitalized_amount + rd_expensed_amount) * 100
```
