# Agent Instructions for CNINFO Project

## Project Goal

本项目从巨潮资讯网公告 PDF 中抽取结构化金融事件信息，构建研发资本化风险排序模型，并通过交易所问询函进行问询闭环可行性测试。

## Data Rules

- 主数据必须来自巨潮资讯网公开公告。
- 不绕过登录、验证码或访问限制。
- 原始 PDF 不得修改。
- Metadata 和下载日志必须保留，用于数据溯源。

## Secret Rules

- 不要把 API Key 写入代码。
- 不要提交 `.env`。
- 只维护 `.env.example`。
- 不要把个人学号、联系方式等敏感信息写入公开代码。

## Coding Rules

- 每个脚本必须支持命令行运行（通过 `src/main.py --stage <stage>` 统一入口）。
- 所有中间输出写入 `data/` 目录。
- 所有最终报告写入 `outputs/` 目录。
- 修改代码后必须说明运行哪个命令验证。
- 新增功能必须配套 pytest 用例。
- 文件编码永远显式写 `encoding="utf-8"`。
- 依赖管理使用 `uv`，不直接 `pip install`。
- Mini pipeline 验证：任何改动后先用 `--limit 1` 或 `--limit 3` 跑通 crawl → download → audit，确认无误后再跑完整数据。

## Extraction Rules

- 字段值必须来自公告文本。
- 每个关键字段要有 `evidence_text`。
- 无法判断时输出 `null`。
- 抽取结果必须通过 Pydantic 校验。
- 会计恒等式（资本化 + 费用化 ≈ 总额）必须交叉验证。
- **资本化率口径优先级**（见 `src/model/schemas.py` 注释）：
  1. 优先使用年报"研发投入"章节直接披露的"资本化金额"
  2. 次选开发支出附注中"本期增加——资本化金额"
  3. 无法确认时输出 `null`，禁止强行计算
- **确定性表格提取**：`src/extract/rd_table_extractor.py` 从 MinerU Markdown 的 HTML 表格解析研发投入/开发支出数值，写入 `data/extracted/tables/tables.jsonl`；`validate` 阶段在 LLM 字段缺失时按 `TABLE_FALLBACK_MAP` 回填并标记 `table_fallback`。变更公式或口径前先看 `docs/methodology.md`（单一真源）。
- **问询相关性标签**：`src/analysis/inquiry_labeler.py` 不再做简单关键词 OR。先按 `document_role` 排除回复类公告，再 Tier-1 关键词命中即判相关，仅命中泛词时送 LLM 语义二分类。`capitalization_related` 是问询闭环可行性测试的 Y 标签。
- **公式与阈值**：所有财会公式、风险评分、异常阈值统一记录在 `docs/methodology.md`（LaTeX），其他文档只引用不复制。

## MinerU 配置

MinerU 有两条可用路线：本地 CLI 和官方精准解析 API。当前 150 份年报已用 `--parse-backend api-batch` 全量解析成功；本地 CLI 仍作为 fallback 保留，详见 `docs/mineru_setup.md` 与 `docs/mineru_api_reference.md`。

- **工具环境**：优先使用 `uv tool install "mineru[all]" --python 3.12 --torch-backend cu126`
- **版本**：`mineru>=3.2.0`（包名从旧版 `magic-pdf` 改为 `mineru`）
- **命令**：`mineru -p <pdf> -o <output> -b pipeline`（不是 `magic-pdf`）
- **推荐复跑**：`uv run python src/main.py --stage parse --parse-backend api-batch`
- **API Key**：`MINERU_API_KEY` 只写 `.env`，不得提交；`.env.example` 只保留占位符
- **本地 fallback**：长年报本地解析仍可能耗时很久，优先用 `--limit` 烟测后再跑
- **安装**：执行 `scripts/setup_mineru.ps1` 一键安装（uv tool → 安装 `mineru[all]` → 解析 CUDA 版 PyTorch → 验证 CUDA）
- **模型**：MinerU 3.x 首次运行时自动从 HuggingFace 下载，无需手动配置 `models-dir`
- **旧版配置已废弃**：`configs/mineru_config_legacy.json` 和 `magic-pdf.json` 不再需要（新版通过 CLI 参数和环境变量控制）
- **失败经验**：不要手动降级到 `torch==2.4.0+cu121`；MinerU 3.2.3 元数据要求 `torch>=2.6,<3`

## Decision Rules

当遇到以下情况时，Agent 必须暂停并向用户确认，不得自行假设：

- 文档与代码不一致。
- 老师讲义要求与当前实现冲突。
- 需要新增、删除或重命名用户文档。
- 数据口径、Schema、评分标准或验收标准发生变更。
- 任何可能影响课程评分或项目验收的决策。
