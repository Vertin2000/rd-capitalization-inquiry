# AI Usage Statement

## 使用的 AI coding agent

- **主要工具**：Claude Code
- **备用工具**：GitHub Copilot（IDE 内代码补全）

## AI 帮助完成的内容

| 内容类型 | AI 参与度 | 说明 |
| -------- | -------- | -------- |
| 项目结构设计 | 高 | Pipeline 架构设计、目录结构规划 |
| Schema 设计 | 高 | Pydantic 模型定义、字段校验规则 |
| 配置文件编写 | 中 | YAML 配置文件、环境变量模板 |
| 文档撰写 | 高 | README、选题方案、技术文档 |
| 代码框架生成 | 中 | 模块骨架、CLI 入口、通用工具函数 |
| 测试用例编写 | 中 | pytest 测试模板 |
| Prompt 设计 | 高 | LLM 字段抽取 Prompt 模板 |

## 学生人工完成的内容

| 内容类型 | 说明 |
| -------- | -------- |
| 金融逻辑设计 | 四维度评分模型的业务逻辑和阈值设定 |
| 数据验证 | 实际爬取数据后的质量检查和人工校验 |
| Prompt 迭代优化 | 根据实际抽取结果调整 Prompt |
| 结果解读 | 对模型输出和闭环评估结果的金融意义分析 |
| 最终报告 | 金融洞察和结论性内容 |

## 我们如何验证 AI 生成内容

1. **代码验证**：所有代码必须通过 `uv run pytest` 测试
2. **数据验证**：抽取结果通过 Pydantic Schema 校验 + 会计恒等式交叉验证
3. **金融逻辑验证**：评分模型阈值和异常判定标准由团队成员讨论确定
4. **文档验证**：技术文档由团队成员审核，确保与代码一致
5. **人工抽检（AI agent 辅助交叉验证）**：按 Week15 评估要求对 35 条样本（17 异常 + 问询相关 company-year + 随机补齐）做逐字段交叉验证，由独立 AI agent 重读 MinerU Markdown 与章节切片、独立定位 evidence 后与 `data/validated/records.jsonl` 的预测值比对，逐条标注 `is_correct / evidence_correct / error_type`（Week15 枚举）。完整结果见 [`outputs/reports/eval_report_final.md`](../outputs/reports/eval_report_final.md) 与 [`outputs/reports/eval_per_field.csv`](../outputs/reports/eval_per_field.csv)。需诚实说明的局限：评估 agent 与抽取 agent 同属 LLM 家族，存在共错风险，故该结果仅作为抽取质量参考，不替代人工终判。

## 发现过的 AI 错误

| 错误类型 | 描述 | 修复方式 |
| -------- | -------- | -------- |
| hallucination | 韦尔股份 2021/2022 年报开发支出附注字段被 LLM 编造数值，与表格原文不符 | 评估标注为 hallucination，记入 eval_per_field.csv；后续以确定性表格提取值覆盖 |
| section_error | 部分样本研发投入章节定位到释义/目录页，导致字段抽取来源错位 | route 阶段产出 section_check_report，标注 quality_issue 供复核 |
| normalization_error | 汇顶科技 2022 期初/期末余额混淆，单位（元/万元）归一化不一致 | 评估标注 normalization_error，提示 Prompt 增加期初期末区分约束 |
| placeholder 误填 | capitalization_condition 字段被填入占位符「(文本)」而非真实条件文本 | 评估标注，列为 Prompt 迭代待办 |

## API Key 与数据合规说明

- API Key 仅存储在本地 `.env` 文件中，不提交到版本控制
- 所有数据来自巨潮资讯网公开公告，不绕过访问限制
- 原始 PDF 文件未被修改，解析结果可追溯
- 爬取过程保留完整日志，符合课程合规要求
