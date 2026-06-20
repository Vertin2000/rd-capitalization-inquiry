# AI Usage Statement

## 使用的 AI coding agent

- **Claude Code**（Anthropic 官方 CLI，主力 agent，负责工作流串联、代码生成与重构、文档同步、提交前审查）
- **Kimi Code CLI**（月之暗面，作为 LLM 抽取/问询语义分类的后端，见 `.env.example` 的 `LLM_BACKEND=kimi_code_cli`）
- **MinerU 官方精准解析 API**（OpenDataLab，用于年报 PDF → Markdown 结构化解析，非 coding agent，列为数据处理工具）

## AI 帮助完成的内容

- 数据抓取、下载、解析、章节定位、LLM 字段抽取、校验、评分、问询打标、报告生成各阶段脚本的编写与调试（`src/` 下各模块）。
- `src/main.py --stage <stage>` 统一命令行入口与阶段串联。
- 确定性表格提取 `src/extract/rd_table_extractor.py`（从 MinerU Markdown 的 HTML 表格解析研发投入/开发支出数值）。
- 问询相关性标签 `src/analysis/inquiry_labeler.py`（Tier-1 关键词 + LLM 语义二分类）。
- pytest 测试用例（`tests/`）。
- 项目文档（README、SPEC、docs/methodology.md、HANDOFF、demo_script、worklog）的撰写与同步。
- Git 仓库初始化、公开仓库推送、敏感信息排查。

## 学生人工完成的内容

- 选题方向与金融问题定义（研发资本化风险排序 + 交易所问询函闭环可行性测试）。
- 四维度风险评分模型的口径设计与阈值确定（统一记录于 `docs/methodology.md`，作为单一真源）。
- 资本化率口径优先级的人工裁定（年报"研发投入"章节直接披露 > 开发支出附注 > 输出 null，禁止强行计算）。
- 150 份年报样本的公司池选择与公告范围圈定。
- 抽取字段的人工抽样校验、错误分类与 prompt 迭代优化。
- 会计恒等式（资本化 + 费用化 ≈ 总额）交叉验证规则的制定。
- 评估结果的人工复核、局限性认定与难度档位声明（挑战档 1.1）。
- 答辩展示材料的内容把关与现场答辩。

## 我们如何验证 AI 生成内容

- **Pydantic Schema 校验**：所有抽取结果必须通过 `src/model/schemas.py` 的 Pydantic 模型校验，字段类型/必填/evidence 约束强制生效。
- **会计恒等式交叉验证**：资本化 + 费用化 ≈ 总额，不一致则标记异常。
- **pytest 全量测试**：`uv run pytest` 覆盖 crawl/parse/extract/validate/route/inquiry/schemas/main 等模块，回归保护。
- **Mini pipeline 烟测**：任何代码改动后先用 `--limit 1` 或 `--limit 3` 跑通 crawl → download → audit，确认无误再跑全量（见 CLAUDE.md Coding Rules）。
- **人工抽样评估**：`outputs/reports/eval_report_final.md` 记录人工评估样本、逐字段准确率与错误分类。
- **提交前审查**：推送前核查 `.env` 不入库、无真实 API Key、无个人敏感信息泄漏（`git log --all -- .env` 复核）。

## 发现过的 AI 错误

- **fuzziness 词表污染**：风险评分所用模糊词表早期含「等/相关/未来」等无信息量泛词，导致评分失真，已人工剔除。
- **change_zscore 误用 abs()**：变化方向信息被绝对值抹平，已修正为保留方向的有符号 z-score。
- **行业归属靠顺序推断**：早期版本用列表顺序推断公司行业，不可靠，已改为按 metadata 显式字段。
- **section_router project_root 硬编码**：`__init__` 中 project_root 硬编码导致 pytest 重跑污染真实 `section_check_report.csv`（已知后续项 F1，shipped 文件为正确全量版，未改代码）。
- **问询标签简单关键词 OR**：早期对问询公告做关键词 OR 判定，误判多，已改为先按 `document_role` 排除回复类公告、再 Tier-1 关键词命中、仅泛词命中时送 LLM 语义二分类。

## API Key 与数据合规说明

- **不绕过访问限制**：所有数据来自巨潮资讯网公开公告，不绕过登录、验证码或访问限制，只抓取公开可访问数据（见 CLAUDE.md Data Rules）。
- **API Key 不入库**：`MINERU_API_KEY`、`LLM_API_KEY`、`CNINFO_ACCESS_KEY/SECRET` 等真实密钥只写本地 `.env`，`.env` 已被 `.gitignore` 忽略，仓库只维护 `.env.example` 占位符模板。
- **敏感信息脱敏**：公开仓库 `team_info.md` 仅保留学号，姓名与联系方式以 `—` 占位，不写入公开代码。
- **原始 PDF 不得修改**：原始公告 PDF 保持原样，Metadata 与下载日志保留用于数据溯源。
