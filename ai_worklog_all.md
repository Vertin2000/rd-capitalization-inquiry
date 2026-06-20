# AI Worklog All — 全程 AI 使用记录汇总

> Week 16 11.5 / 11.6 要求：提交 `ai_worklog_all.md`（全程汇总）+ `ai_usage_statement.md`（声明）+ 分周 `docs/worklogs/ai_worklog_weekNN.md`。本文件是全程汇总索引，详细过程见各周 worklog。

## 使用的工具

- **Claude Code**（主力）：Week 11 起用于重构、Schema 设计、挑战档扩展、评分模型、问询闭环、文档整理、本次排查与交差计划。
- **TRAE**：Week 11 队友初期文档模板与项目骨架搭建。
- **MinerU API**：PDF 解析（非 AI coding agent，但属 AI 工具链）。
- **LLM API**（SiliconFlow Qwen2.5-72B / Kimi Code CLI）：字段抽取与问询语义二分类。

## 全程主线（按周）

| 周次 | 主线 | 详细记录 |
| -------- | -------- | -------- |
| Week 11 | 选题、项目骨架、Vibe Coding 入门 | [`docs/worklogs/ai_worklog_week11.md`](docs/worklogs/ai_worklog_week11.md) |
| Week 12 | 巨潮公告抓取（crawl → download → audit），official API 路线 150/150 | [`docs/worklogs/ai_worklog_week12.md`](docs/worklogs/ai_worklog_week12.md) |
| Week 13 | MinerU 解析（api-batch 150/150）、Pydantic Schema、Section Routing、LLM 抽取 | [`docs/worklogs/ai_worklog_week13.md`](docs/worklogs/ai_worklog_week13.md) |
| Week 14 | 工作流串联（统一 CLI `--stage`）、validate/score/detect 接入 | [`docs/worklogs/ai_worklog_week14.md`](docs/worklogs/ai_worklog_week14.md) |
| Week 15 | 评估与 Prompt 优化、问询闭环标签器 v2、风险评分模型 | [`docs/worklogs/ai_worklog_week15.md`](docs/worklogs/ai_worklog_week15.md) |
| Week 16 | 期末展示准备、本次排查与交差计划（人工评估、提交清单、方法论修复） | [`docs/worklogs/ai_worklog_week16.md`](docs/worklogs/ai_worklog_week16.md) |

## AI 帮了什么 / 学生如何验证 / AI 出过什么错

### AI 帮了什么

- 爬虫参数调校、OAuth2 token 刷新、doc_id 人可读化。
- Pydantic Schema 与资本化率口径（5 级优先级）设计。
- 确定性表格提取作为 LLM fallback。
- 四维度风险评分模型与问询标签器 v2。
- 文档整理（SPEC/README/HANDFF/methodology 单一真源）。
- 本次排查：对照老师讲义逐项核查、Rubric 估分、识别方法论硬伤与诚信风险。

### 学生如何验证 AI 生成内容

- **数据层**：metadata/PDF 一一对应、SHA256 唯一性检查（audit）、hash 碰撞历史教训（131 份 6 hash → 0 collision）。
- **抽取层**：Pydantic 校验 + 会计恒等式（资本化+费用化≈总额）+ evidence_text 原文回溯。
- **人工评估**：35 条样本由独立 AI agent 读原文复核（详见 `outputs/reports/eval_report_final.md`），并诚实标注「eval agent 与 extractor 同源 LLM 可能共错」的局限。
- **方法层**：`docs/methodology.md` 作为单一真源，所有公式/阈值透明记录并标注「待复核」。

### AI 出过的错（已修正）

- 早期爬虫 hash 碰撞（曾用 `stock=f"{code},"` 和 `searchkey=002230`）→ official API 路线重写，collision=0。
- 旧 MinerU 环境手降到 `torch==2.4.0+cu121` 与 `mineru==3.2.3` 元数据冲突 → 改用 `uv tool install "mineru[all]" --torch-backend cu126`。
- 问询标签 v1 简单关键词 OR 误判 → v2 脚本剪枝 + Tier-1 + LLM 语义二分类。
- 文档措辞「异常检测/闭环验证」超出证据（TP=0）→ 统一降级为「风险排序/可行性测试」（详见 HANDOFF §十二）。

## AI 使用声明

详见 [`docs/ai_usage_statement.md`](docs/ai_usage_statement.md)。

## 交接与下一步

详见 [`docs/HANDOFF.md`](docs/HANDOFF.md)（含 §十二 2026-06-20 排查与交差计划）。
