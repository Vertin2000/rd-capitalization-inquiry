# Evaluation Report

## 评估样本

TODO：描述评估样本的选取方式（随机抽样 / 重点关注 / 分层抽样）

- 总样本数：
- 人工评估样本数：≥ 30 条
- 评估人员：
- 评估日期：

## Data Quality

### PDF 完整性

| 检查项 | 结果 |
| -------- | -------- |
| 下载成功率 | |
| 文件损坏率 | |
| 扫描版占比 | |

### 解析质量

| 检查项 | 结果 |
| -------- | -------- |
| 页码保留率 | |
| 表格完整率 | |
| 乱码率 | |

## Section Quality

| 章节类型 | 定位成功率 | 定位失败原因 |
| -------- | -------- | -------- |
| 会计政策 | | |
| 研发费用 | | |
| 开发支出 | | |
| 管理层讨论 | | |

## Extraction Quality

| 字段 | 抽取成功率 | 主要错误类型 |
| -------- | -------- | -------- |
| rd_expense_total | | |
| rd_capitalized_amount | | |
| rd_expensed_amount | | |
| dev_cost_opening | | |
| dev_cost_closing | | |
| impairment | | |
| capitalization_rate | | |
| capitalization_condition | | |

## Evidence Quality

| 检查项 | 合格率 |
| -------- | -------- |
| evidence_text 非空 | |
| page_no 正确 | |
| evidence_text 与字段值对应 | |

## Pipeline Stability

| 阶段 | 运行成功率 | 平均耗时 |
| -------- | -------- | -------- |
| crawl | | |
| download | | |
| parse | | |
| route | | |
| extract | | |
| validate | | |
| score | | |
| detect | | |
| inquiry | | |
| analyze | | |
| report | | |

## 错误分类

| 错误类型 | 数量 | 示例 | 修复策略 |
| -------- | --------: | -------- | -------- |
| 字段缺失 | | | |
| 类型错误 | | | |
| 范围异常 | | | |
| 交叉验证失败 | | | |
| 证据缺失 | | | |

## 优化前后对比

TODO：如果进行了多轮优化，记录优化前后的指标对比

| 指标 | 优化前 | 优化后 | 提升幅度 |
| -------- | -------- | -------- | -------- |
| 字段抽取成功率 | | | |
| 校验通过率 | | | |
| 评分准确率 | | | |

## 局限性

TODO：记录本项目的已知局限

1.
2.
3.
