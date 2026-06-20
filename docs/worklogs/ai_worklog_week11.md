# AI Worklog Week 11

## 使用的工具

Claude Code + TRAE

- TRAE 用于队友初期的文档模板编写和项目骨架搭建。
- Claude Code 用于后续的重构、Schema 设计和挑战档扩展方案的细化。

## 本周让 AI 帮助的任务

1. 分析课程 Week 11-16 要求并确定选题方向（研发资本化异常检测 + 问询函闭环验证）
2. 设计项目整体架构和目录结构
3. 编写 Week 11 所有模板文档（`topic_proposal.md`、`team_info.md`、`cninfo_data_discovery.md`、`topic_ideas.md`、`output_sample.md` 等）
4. 创建项目配置文件（`workflow.yaml`、`model_config.yaml`、`section_rules.yaml`、`crawl.yaml` 等）
5. 设计目标字段 Schema（`src/model/schemas.py`），包含 14 个核心字段 + 8 个扩展字段
6. 制定 6 周项目计划（Week 11 骨架 → Week 16 答辩）
7. 编写 Agent 指令（`CLAUDE.md`）和编码规范（`CODING_RULES.md`）

## 我给 AI 的上下文

- 课程要求：数据挖掘与机器学习课程 Week 11-16 金融文本智能项目
- 选题方向：上市公司研发资本化异常检测与交易所问询函触发机制分析
- 数据源：仅巨潮资讯网公开公告（年报 + 问询函 + 回复函）
- 难度档位：挑战档（1.1x）
- 目标字段：14 个核心字段 + 8 个扩展字段（含证据追溯、评分模型、闭环分析）

## AI 生成或修改的文件

- `docs/cninfo_data_discovery.md`
- `docs/topic_ideas.md`
- `docs/topic_proposal.md`
- `docs/output_sample.md`
- `docs/workflow_design.md`
- `docs/tool_setup_check.md`
- `docs/worklogs/ai_worklog_week11.md`
- `configs/workflow.yaml`
- `configs/model_config.yaml`
- `configs/section_rules.yaml`
- `configs/crawl.yaml`
- `src/model/schemas.py`
- `src/main.py`
- `src/common.py`
- `tests/test_schemas.py`
- `CLAUDE.md`
- `CODING_RULES.md`
- `.env.example`
- `.gitignore`
- `pyproject.toml`

## 我实际运行的命令

- 创建项目目录结构（`data/`、`src/`、`configs/`、`docs/`、`outputs/`、`tests/`）
- `uv sync` 安装依赖
- `uv run pytest` 验证 Schema 测试
- `uv run python src/main.py --help` 验证 CLI 入口

## 报错与修复

- 无（本周主要是文档编写和骨架搭建，尚未运行完整 Pipeline）

## 我人工检查了什么

- 确认所有文档内容符合课程 Week 11 讲义要求
- 确认字段设计合理、可操作、可校验
- 确认数据源限定为巨潮资讯网公开公告，不编造数据
- 确认 `.env.example` 不包含真实 API Key
- 确认 `.gitignore` 已排除 `.env` 和 `data/pdf/`、`outputs/` 等目录

## 我理解的关键代码

- 项目工作流：`crawl -> download -> audit -> parse -> route -> extract -> validate -> score -> detect -> inquiry -> analyze -> report`
- 数据追溯机制：每个关键字段必须包含 `evidence_text`、`page_no`、`source_pdf_path`
- Pydantic 校验：`RDCapitalizationRecord` 自动计算资本化率；`InquiryLoopRecord` 自动推导 TP/FP/TN/FN
- 评分模型：四维度评分（行业偏离度、跨期变化、条件模糊度、会计恒等式）加权计算 `aggressiveness_score`
