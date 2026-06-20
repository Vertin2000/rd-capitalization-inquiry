# `project2/docs/` 文档索引

本目录存放项目过程文档、老师模板留档、AI 工作日志和参考材料。本文档说明每份文件的来源、当前状态和用途，便于人和 AI 快速定位。

---

## 活跃文档

| 文档 | 用途 | 来源 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| [`methodology.md`](methodology.md) | 研究方法、财会公式、风险评分模型与启发式匹配逻辑（单一真源） | 项目自定义 | 活跃 | LaTeX 公式与参数审计表 |
| [`architecture.md`](architecture.md) | 已验证/进行中阶段的架构与数据流 | 项目自定义 | 活跃 | 核心架构文档 |
| [`crawl_spec.md`](crawl_spec.md) | 抓取范围、股票池、公告类型、限速策略 | 老师模板 | 活跃 | 随 crawler 迭代同步 |
| [`HANDOFF.md`](HANDOFF.md) | 工作交接、历史问题诊断、下一步清单 | 项目自定义 | 活跃 | 按会话持续更新 |
| [`cninfo_official_api_annual_report.md`](cninfo_official_api_annual_report.md) | 官方 API 年报抓取接口切片说明 | 项目自定义 | 活跃 | 含 API 文档原文与代码规则 |
| [`cninfo_external_references.md`](cninfo_external_references.md) | CNINFO 外部开源参考、license、影响范围与复用边界 | 项目自定义 | 活跃 | 记录 token 端点和前端公告查询参考来源 |
| [`mineru_setup.md`](mineru_setup.md) | MinerU API batch 与本地 CLI fallback 配置指南 | 项目自定义 | 活跃 | 当前主解析配置文档 |
| [`topic_proposal.md`](topic_proposal.md) | 研究问题、变量定义、课程要求映射 | 老师模板 | 活跃 | 已合并扩展方案内容 |
| [`workflow_design.md`](workflow_design.md) | Pipeline 节点 canonical 表、人工检查点、最小运行命令 | 老师模板 | 活跃 | 阶段详细说明以此为准 |

## 老师模板留档

| 文档 | 用途 | 来源 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| [`ai_usage_statement.md`](ai_usage_statement.md) | AI 使用声明 | 老师模板 | 留档 | 课程要求文档 |
| [`cninfo_data_discovery.md`](cninfo_data_discovery.md) | 巨潮数据探索记录 | 老师模板 | 留档 | Week 11 数据观察 |
| [`eval_report_template.md`](eval_report_template.md) | 人工评估报告模板 | 老师模板 | 待填写 | 原 `evaluation_report.md`，已改名对齐模板 |
| [`output_sample.md`](output_sample.md) | 输出样例 | 老师模板 | 留档 | 目标输出格式示例 |
| [`parse_check.md`](parse_check.md) | 解析质量检查清单 | 老师模板 | 留档 | MinerU 输出检查项 |
| [`presentation_checklist.md`](presentation_checklist.md) | 期末展示检查清单 | 老师模板 | 留档 | 展示前逐项确认 |
| [`tool_setup_check.md`](tool_setup_check.md) | 工具安装检查 | 老师模板 | 留档 | TRAE / Claude Code 等环境确认 |
| [`topic_ideas.md`](topic_ideas.md) | 选题思路 | 老师模板 | 历史 | 候选方向记录 |

## 进行中（WIP）

| 文档 | 用途 | 来源 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| [`cninfo_official_api_reference.md`](cninfo_official_api_reference.md) | 深证信官方 API 目录、典型接口元数据、参数校准参考 | 项目自定义 | WIP | API 文档本地化产物，用于校准 crawler |
| [`cninfo_official_api_catalog.md`](cninfo_official_api_catalog.md) | 2465 个接口全量层级目录 | 项目自定义 | WIP | 含可见 + 隐藏类目 |
| [`cninfo_official_api_catalog.json`](cninfo_official_api_catalog.json) | 全量目录机器可读版本 | 项目自定义 | WIP | 含研究相关接口子集 |
| [`mineru_api_reference.md`](mineru_api_reference.md) | MinerU API 参考备份 | 项目自定义 | WIP / 参考 | 官方 API 文档抓取备份 |
| [`mineru_api_docs_extracted.md`](mineru_api_docs_extracted.md) | MinerU API 文档提取 | 项目自定义 | WIP / 参考 | 从官方文档提取的 Markdown |
| [`mineru_readme_zh.md`](mineru_readme_zh.md) | MinerU 中文 README 备份 | 项目自定义 | WIP / 参考 | 官方仓库 README 中文翻译 |
| [`mineru_api_docs.html`](mineru_api_docs.html) | MinerU API 文档 HTML 备份 | 项目自定义 | WIP / 参考 | 官方文档 HTML 存档（已 untrack） |

> 说明：MinerU 相关资料以 [`mineru_setup.md`](mineru_setup.md) 为活跃主文档，其余为探索过程中抓取的参考备份，后续可整理归档。

## AI 工作日志

[`worklogs/`](worklogs/) 目录按周记录过程：

| 文件 | 周次 |
| --- | --- |
| [`worklogs/ai_worklog_week11.md`](worklogs/ai_worklog_week11.md) | Week 11 |
| [`worklogs/ai_worklog_week12.md`](worklogs/ai_worklog_week12.md) | Week 12 |
| [`worklogs/ai_worklog_week13.md`](worklogs/ai_worklog_week13.md) | Week 13 |
| [`worklogs/ai_worklog_week14.md`](worklogs/ai_worklog_week14.md) | Week 14 |
| [`worklogs/ai_worklog_week15.md`](worklogs/ai_worklog_week15.md) | Week 15 |
| [`worklogs/ai_worklog_week16.md`](worklogs/ai_worklog_week16.md) | Week 16 |

## 已删除/归档文档

| 文档 | 处理原因 |
| --- | --- |
| `prompt_v1.md` | 早期原型阶段的 Prompt 计划记录，作为历史参考保留 |
| `topic_expansion_proposal.md` | 已采纳并合并到 `topic_proposal.md`，作为独立文档已完成使命 |

---

## 快速入口

- 想跑项目 → [`../README.md`](../README.md)
- 想看项目总纲和当前进度 → [`../SPEC.md`](../SPEC.md)
- 想看 Agent 指令 → [`../AGENTS.md`](../AGENTS.md) / [`../CLAUDE.md`](../CLAUDE.md)
- 想看本周重点和遗留问题 → [`HANDOFF.md`](HANDOFF.md)
- 想看研究方法、公式与参数说明 → [`methodology.md`](methodology.md)
- 想看架构设计 → [`architecture.md`](architecture.md)
- 想查 CNINFO 外部来源边界 → [`cninfo_external_references.md`](cninfo_external_references.md)
- 想看最终答辩报告（手写版）→ [`../final_report.md`](../final_report.md)（根目录）
- 想看自动生成技术底稿 → [`../outputs/final_report_auto.md`](../outputs/final_report_auto.md)
