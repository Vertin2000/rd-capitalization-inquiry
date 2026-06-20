# Project2 SPEC: 研发资本化风险排序与问询函可行性测试

本文档是 `project2/` 的**项目总纲**。它回答三个问题：项目承诺做什么，做到什么算完成，当前代码已经支持到哪里。

README 负责安装、运行和 Pipeline 使用；worklogs 记录每周过程；本 SPEC 维护稳定契约、研究问题和一张当前能力快照。

## 0. 快速定位

| 你想知道什么 | 看哪里 |
| --- | --- |
| 项目目标与研究问题 | 本文档 §1 + [`docs/topic_proposal.md`](docs/topic_proposal.md) |
| Pipeline 阶段与运行命令 | [`docs/workflow_design.md`](docs/workflow_design.md) |
| 架构设计与数据流 | [`docs/architecture.md`](docs/architecture.md) |
| 抓取规则与股票池 | [`docs/crawl_spec.md`](docs/crawl_spec.md) |
| 当前代码能力快照 | 本文档 §5 |
| 交接记录与下一步 | [`docs/HANDOFF.md`](docs/HANDOFF.md) |
| Agent 指令 | [`AGENTS.md`](AGENTS.md) |

## 1. Project Contract

本项目从巨潮资讯网公开年报 PDF 中抽取研发资本化相关字段，识别资本化激进公司，并用交易所问询函作为外部验证信号评估风险排序结果。

项目最终交付一条可复现 Pipeline：

```text
crawl -> download -> audit -> parse -> route -> extract -> validate
  -> score -> detect

annual metadata -> inquiry -> inquiry-download -> inquiry-label

scored records + anomaly labels + inquiry labels -> analyze -> report
```

### 研究问题

完整研究问题、变量定义和课程要求映射见 [`docs/topic_proposal.md`](docs/topic_proposal.md)。核心问题如下：

- **核心问题**：哪些研发资本化特征与交易所问询相关？
- **子问题 1**：高资本化率是否更容易与问询相关？（资本化率水平 vs 行业偏离度）
- **子问题 2**：资本化率的剧烈变化是否更容易与问询相关？（跨期变化幅度）
- **子问题 3**：资本化条件描述模糊是否更容易与问询相关？（条件文本模糊度评分）

### 目标

- 抓取并下载 50 家研发密集型上市公司在 2021-2023 年的年度报告。
- 从年报中抽取研发投入、资本化金额、费用化金额、开发支出、资本化条件等字段。
- 对抽取结果做 Pydantic 校验和会计恒等式检查。
- 用风险评分模型识别研发资本化异常记录，并用恒等式检查辅助判断数据质量。
- 对全部 150 个 company-year 查询研发资本化相关问询候选，解析后形成问询标签。
- 在有效问询样本充足时生成 Precision / Recall / F1；样本不足时改用 Top-K 命中率、候选覆盖率和案例分析。
- 生成最终 Markdown 报告，可用于课程提交和展示。

### 非目标

- 不绕过登录、验证码、限流或访问控制。
- 不修改原始 PDF。
- 不保证交易所问询函等同于监管最终认定，只将其作为外部验证信号。
- 不做严格因果推断；本项目做风险排序和问询闭环可行性测试（描述性）。
- 不做 2021-2023 年时间序列回归；三年数据用于跨期变化比较。

### 数据合规

- 主数据只来自巨潮资讯网公开公告。
- `metadata.csv` 是数据溯源主表，后续阶段必须保留 `doc_id`。
- `.env`、API Key、个人身份信息不得提交。
- 原始 PDF 只读保存；派生文件写入 `data/` 和 `outputs/`。

## 2. Success Criteria

| 维度 | 课程基础要求 | 本项目挑战目标 | 验收口径 |
| --- | --- | --- | --- |
| 年报 PDF | >= 50 份 | 150 份 | 50 家公司 x 3 年 |
| 核心字段 | >= 10 个 | >= 14 个 | 见 `src/model/schemas.py` |
| Pipeline | 下载、解析、抽取、输出 | 年报主线 + 问询闭环 | `crawl` 到 `report` 已接入 `src/main.py --stage`；当前可从 `validate` 一次跑到 `report` |
| 证据追溯 | 有人工核验依据 | 字段级 `evidence_text` | 无法判断输出 `null` |
| 人工校验 | >= 10 条 | >= 30 条 | 随机样本 + 异常样本优先 |
| 风险排序 | 可解释指标 | 风险评分 + 数据质量校验 | 行业偏离、跨期变化、条件模糊、恒等式一致性 |
| 问询闭环可行性测试 | 可选扩展 | 全样本问询标签 | 条件式 Precision / Recall / F1；样本不足时输出 Top-K 命中率和案例分析 |

## 3. Data Scope

| 维度 | 规格 |
| --- | --- |
| 数据源 | 巨潮资讯网公开公告 |
| 公司池 | 50 家：医药制造 20 家、电子设备 20 家、软件信息 10 家 |
| 年报年份 | 2021、2022、2023 |
| 年报数量 | 150 份 |
| 主公告 | 年度报告，排除摘要、修订、更正、补充公告 |
| 辅助公告 | 优先年报问询函、问询函回复；样本不足时扩展关注函、监管工作函 |
| 问询窗口 | 年报发布日期后 180 天；发布前记录可作背景，不进入触发标签 |
| 关键词 | 研发、资本化、开发支出、无形资产、费用化 |

完整股票池、年份和关键词以 `configs/crawl.yaml` 为准；抓取规则见 `docs/crawl_spec.md`。

## 4. Pipeline Contract

| 阶段 | 输入 | 输出 | 验收标准 |
| --- | --- | --- | --- |
| `crawl` | `configs/crawl.yaml` | `data/metadata/metadata.csv` | 生成可追溯 metadata，含 `doc_id`、公告标题、URL、PDF URL |
| `download` | metadata | `data/pdf/*.pdf` | PDF 存在、可读、记录下载状态和 hash |
| `audit` | metadata + PDF | `outputs/dataset_check_report.md` | 检查 metadata、PDF 数量、重复 ID、文件完整性 |
| `parse` | PDF | `data/parsed/*.md` | MinerU 解析为非空 Markdown，并保留原始解析目录 |
| `route` | Markdown | `data/sections/*_sections.jsonl` | 定位研发投入、开发支出、研发费用等目标章节 |
| `extract` | section JSONL | `data/extracted/records.jsonl` | 结构化字段有值或明确 `null`，并带证据文本 |
| `validate` | extracted JSONL | `data/validated/records.jsonl` | 通过 Pydantic 校验、口径校验和恒等式检查 |
| `score` | validated JSONL | `data/scored/records.jsonl` | 计算风险评分、数据质量校验和总分 |
| `detect` | scored JSONL | `data/anomaly/anomaly_list.csv` | 标记异常记录和异常类型 |
| `inquiry` | annual metadata + CNINFO 前端公开查询 | `data/inquiry/inquiry_candidates.csv` + `data/inquiry/inquiry_discovery_cache.json` | 覆盖全部 150 个 company-year，生成问询/回复候选 metadata；逐条写入候选、日志和 checkpoint |
| `inquiry-download` | inquiry candidates | `data/inquiry/pdf/*.pdf` | 下载候选 PDF，回写 `download_status`、PDF 首页标题校验结果，并生成 orphan PDF 报告 |
| `inquiry-label` | inquiry candidates + 问询文本 + annual metadata | `data/inquiry/inquiry_records.jsonl` | 判断候选是否与研发资本化相关，并关联到 company-year |
| `analyze` | scored records + anomaly list + inquiry records | `outputs/loop_evaluation.json` | 生成 TP / FP / TN / FN 和条件式评估指标 |
| `report` | evaluation JSON | `outputs/final_report_auto.md` | 输出自动版技术报告；根级 `final_report.md` 为手写答辩版 |

## 5. 当前能力快照

此表是代码状态快照，不替代 `docs/worklogs/`。过程、命令和报错记录继续写入 worklogs。

| 阶段 | 当前状态 | 依据 | 说明 |
| --- | --- | --- | --- |
| `crawl` | official API 路线完整 150/150 验证通过 | `src/main.py` `IMPLEMENTED` | 生成 150 条年报 metadata，失败 0 |
| `download` | 完整 150/150 验证通过 | `src/main.py` `IMPLEMENTED` | PDF 下载、状态回写、hash 检查；collision=0 |
| `audit` | 完整 150/150 验证通过 | `src/main.py` `IMPLEMENTED` | metadata 和 PDF 质量审计 8 项检查通过，150 个唯一 SHA256 |
| `parse` | MinerU API batch 完整 150/150 验证通过 | `src/main.py` `IMPLEMENTED` | 年报 Markdown 已全部生成；默认 local backend 保留作 fallback，复跑/补跑推荐 `--parse-backend api-batch` |
| `route` | 已全量产出章节切片 | `src/main.py` `IMPLEMENTED` | 基于章节规则输出 JSONL 切片，供 extract 读取 |
| `extract` | 已全量产出抽取记录 | `src/main.py` `IMPLEMENTED` | `data/extracted/records.jsonl` 覆盖 150 个 company-year；缺字段保留 `null` 和证据说明 |
| `validate` | 已全量通过 | `src/main.py` `IMPLEMENTED` | 2026-06-15 重跑：150/150 passed，failed=0 |
| `score` | 已接入并全量重跑 | `src/main.py` `IMPLEMENTED` | 150 条输入，83 条有可用风险分，67 条因关键字段缺失未评分（no-score，scorer `stats` 字段名为 `partial`） |
| `detect` | 已接入并全量重跑 | `src/main.py` `IMPLEMENTED` | 标出 17 条异常，未评分记录 67 条不标异常 |
| `inquiry` | 已接入可断点候选发现 | `src/main.py` `IMPLEMENTED` | 覆盖 150 个 company-year；当前固定 28 条候选 |
| `inquiry-download` | 已接入候选 PDF 下载与标题校验 | `src/main.py` `IMPLEMENTED` | 28/28 PDF 已下载，orphan=0，标题校验 ok=22、empty=6 |
| `inquiry-label` | 已接入 v2 标签 | `src/main.py` `IMPLEMENTED` | 输出 150 条 company-year 标签；10 条有候选，1 条命中实质研发资本化问询（按 `document_role` 排除回复类 + Tier-1 关键词剪枝 + LLM 语义二分类） |
| `analyze` | 已接入并全量重跑 | `src/main.py` `IMPLEMENTED` | 输出 TP=0、FP=17、TN=132、FN=1 |
| `report` | 已接入并全量重跑 | `src/main.py` `IMPLEMENTED` | 生成 `outputs/final_report_auto.md`（自动版）；根级 `final_report.md` 为手写答辩版 |

### 最新全量运行结果（2026-06-20）

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```

| 指标 | 最新结果 | 解释 |
| --- | ---: | --- |
| validate | 150/150 passed | extract 已形成全样本结构化记录，Schema 与会计校验通过 |
| score | 83 scored / 67 partial | 字段缺失不会阻塞后续流程，缺失原因写入 `data_quality_notes` |
| detect | 17 anomalies | 在 83 条可评分记录中按 `anomaly_percentile=0.80` 取前 20% 左右；换算到 150 全样本为 11.33% |
| inquiry-label | 150 total / 10 with candidates / 1 related | v2 标签：排除回复类公告 + Tier-1 关键词剪枝 + LLM 语义二分类，单独命中泛词不再判相关 |
| analyze | TP=0 / FP=17 / TN=132 / FN=1 | 闭环跑通，但当前弱标签下预测效果较弱；正样本极少，统计上接近空 |
| report | written=1 | `outputs/final_report_auto.md` 为自动版技术报告；`final_report.md`（根目录）为手写答辩版 |

## 6. Data Contracts

### `metadata.csv`

`metadata.csv` 是 `crawl -> download` 的主契约。必须包含：

```text
doc_id, stock_code, stock_name, market, announcement_title,
announcement_type, publish_date, url, pdf_url, local_pdf_path,
download_status, source, crawl_time, error_message, notes
```

规则：

- `doc_id` 全局唯一，后续文件命名必须沿用。
- `download_status` 只能表达成功、失败或跳过。
- 失败记录必须写明 `error_message`。
- `source` 标识抓取后端，当前可为 `cninfo` 或 `cninfo_official_api`。

### Parsed Markdown

`parse` 阶段提供稳定入口：

- `data/parsed/{doc_id}.md`
- 可选 `data/parsed/{doc_id}_content_list.json`
- 原始 MinerU 输出保留在 `data/parsed/mineru_raw/{doc_id}/`

Markdown 标题层级、表格和页码提示用于后续章节定位。页码可能缺失，不能作为唯一依据。

### Section JSONL

`route` 阶段每个文档输出 `data/sections/{doc_id}_sections.jsonl`。每行应符合 `SectionSlice`：

- `doc_id`
- `section_name`
- `matched_keyword`
- `text`
- `line_start`
- `line_end`
- `page_hint`

### Extracted and Validated JSONL

`extract` 阶段输出嵌套 `FieldEvidence`；`validate` 阶段输出扁平 `RDCapitalizationRecord`。

`FieldEvidence` 必须表达：

- `value`
- `evidence_text`
- `page_no`
- `confidence`

无法判断的字段写 `null`，不是 0。只有原文明确为 0 时才能写 0。

### Scoring and Inquiry Outputs

后续阶段必须使用这些文件作为契约：

- `data/scored/records.jsonl`
- `data/anomaly/anomaly_list.csv`
- `data/inquiry/inquiry_candidates.csv`
- `data/inquiry/inquiry_discovery_cache.json`
- `data/inquiry/pdf/*.pdf`
- `data/inquiry/inquiry_records.jsonl`
- `outputs/loop_evaluation.json`
- `outputs/final_report_auto.md`
- `final_report.md`

`inquiry_candidates.csv` 是候选层，只记录公开公告查询返回的问询函、回复函、关注函或监管工作函 metadata。`--stage inquiry` 只负责发现候选并逐条写入 `inquiry_discovery_cache.json`；`--stage inquiry-download` 再调用 `PDFDownloader` 下载到 `data/inquiry/pdf/`。`inquiry_records.jsonl` 是标签层，必须覆盖全部 150 个 company-year；没有候选或候选不相关的记录也要保留，才能计算 FN/TN。

`inquiry_candidates.csv` 必须保留旧 metadata 字段，并新增：

- `document_role`：细分候选角色，取值为 `inquiry_notice`、`substantive_reply`、`delay_notice`、`supporting_statement`、`attention_letter`、`regulatory_work_letter` 或 `process_other`。
- `pdf_title`、`pdf_title_status`、`title_match_status`：`inquiry-download` 下载后尝试抽取 PDF 首页标题。普通文字型 PDF 写 `ok`，无文字层写 `empty`，缺失文件写 `missing`，不阻断下载阶段。

问询 PDF 的 `doc_id` 使用可读稳定格式：`{stock_code}_{stock_name}_{report_year}_{publish_date}_{document_role}_{announcement_id}`。`data/inquiry/pdf/` 是缓存目录，当前候选表引用的文件才进入后续标签流程；未被候选表引用的旧 PDF 写入 `outputs/reports/inquiry_orphan_pdf_report.md`，不自动删除。

## 7. Field and Metric Contract

### 核心字段

基础记录必须覆盖：

- 公司与年份：`doc_id`、`company_name`、`company_code`、`year`
- 研发金额：`rd_expense_total`、`rd_capitalized_amount`、`rd_expensed_amount`
- 开发支出：`dev_cost_opening`、`dev_cost_closing`
- 减值与口径：`impairment`、`capitalization_rate`、`capitalization_condition`
- 追溯信息：`evidence_text`、`page_no`、`source_pdf_path`、`null_reason`

### 资本化率口径

`rd_capitalized_amount` 优先级：

1. 年报“研发投入”章节直接披露的资本化金额。
2. 开发支出附注中“本期增加--资本化金额”。
3. 无法区分时输出 `null`。

禁止把开发支出期末余额直接当作本期资本化金额。

`capitalization_rate` 主口径：

1. 优先使用年报直接披露的研发投入资本化率。
2. 若未直接披露，优先使用 validate 阶段写入的 `calculated_capitalization_rate`。
3. 若仍缺失，使用资本化金额与费用化金额计算：

```text
capitalization_rate = rd_capitalized_amount / (rd_capitalized_amount + rd_expensed_amount) * 100
```

4. 最后才退到研发投入总额口径：

```text
capitalization_rate = rd_capitalized_amount / rd_expense_total * 100
```

`rd_expense_total` 主要用于交叉校验和末位 fallback。若年报中的研发支出总额与资本化金额、费用化金额存在差异，应记录校验结果和缺失原因，不直接覆盖主口径。

### 风险评分与数据质量校验

最终评分使用 `configs/model_config.yaml` 中的权重：

- `industry_percentile`：同行业同年份偏离。
- `change_zscore`：资本化率跨期变化。
- `fuzziness_score`：资本化条件描述模糊度。
- `identity_check_score`：资本化 + 费用化 与总额的一致性，用作数据质量和置信度校验，不作为公司激进资本化的正向证据。

`aggressiveness_score` 是 0-100 的综合分。异常阈值默认取前 20%，即 `anomaly_percentile: 0.80`；该阈值只作用在有风险分的记录上，不作用在全体 150 条样本上。若关键字段缺失或 `identity_check_score` 显示抽取口径不可靠，应降低记录置信度或进入人工复核，而不是直接提高异常分。

完整公式、变量定义、阈值与启发式参数审计表见 [`docs/methodology.md`](docs/methodology.md)。

`identity_multiplier` 保留在配置中，表示恒等式一致性作为最终风险分乘数（不是加权项）。这样更符合金融解释：金额关系不稳首先是数据质量风险，不能直接解释为公司更激进。validate 阶段已经用 5% 恒等式阈值拦截严重不一致记录，因此进入评分且三金额齐全的记录 `identity_check_score` 通常不低于 0.75；`identity_error` 异常类型在当前阈值组合下基本不会触发，保留为接口占位。当前 `change_score` 使用 `max(0, change_zscore)`，只取正向跳升（资本化率突然上升=变激进）；资本化率骤降（如项目完结转无形资产）不视为激进信号。

行业归属优先读 `configs/crawl.yaml` 中各公司显式配置的 `industry` 字段（20 医药制造 / 20 电子设备 / 10 软件信息）；仅当某公司缺失显式 `industry` 时，才回退到按公司排列顺序启发式推断。后续应移除顺序 fallback，避免调整股票池顺序后行业百分位错位。

异常类型中，`industry_outlier` 既表示 `industry_percentile >= 0.8`，也可能是所有细分原因都未命中时的默认归类；该标签不保证百分位达标，需要回看原始 `industry_percentile`。

### 问询闭环指标

`InquiryLoopRecord` 负责关联年报侧和问询函侧。问询标签必须来自全部 150 个 company-year 的候选发现和内容判断，不能只对异常列表查询。

当前标签逻辑见 [`docs/methodology.md` §6.3](docs/methodology.md#63-问询函相关性-v2)：

- 脚本层先排除回复函 / 延期公告 / 专项说明，仅保留问询函 / 关注函 / 监管工作函；
- 命中“资本化”“开发支出”等高置信度 Tier-1 关键词即判相关；
- 仅命中“研发”“研发费用”“研发投入”“无形资产”等泛词时，将标题 + PDF 首页 / 关键词片段送入 LLM 做语义二分类；
- 输出字段包括 `inquiry_received`、`reply_received`、`capitalization_related`，其中 `capitalization_related` 是问询闭环可行性测试的 $Y$ 标签。

预测结果按以下矩阵分类：

| 模型预测 | 实际收到问询 | 结果 |
| --- | --- | --- |
| 异常 | 是 | TP |
| 异常 | 否 | FP |
| 正常 | 否 | TN |
| 正常 | 是 | FN |

当研发资本化相关问询样本充足时，最终评估至少输出 Precision、Recall、F1，可扩展输出 Specificity。当有效样本过少时，`analyze` 输出 Top-K 命中率、候选覆盖率和典型案例分析，并明确说明 Precision / Recall / F1 仅作描述性参考或不输出。

## 8. Verification and Deliverables

### 开发验证

代码改动后至少运行：

```powershell
uv run pytest
```

涉及数据阶段时，先跑小样本：

```powershell
uv run python src/main.py --stage crawl --limit 1
uv run python src/main.py --stage download --limit 3
uv run python src/main.py --stage audit
```

涉及 MinerU、抽取或校验时，使用 `--limit` 做阶段级验证，再扩大到完整数据。

extract 已完成后，刷新后段报告使用：

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```

### 最终交付物

- `data/metadata/metadata.csv`
- `data/pdf/*.pdf`
- `data/parsed/*.md`
- `data/sections/*_sections.jsonl`
- `data/extracted/records.jsonl`
- `data/validated/records.jsonl`
- `data/scored/records.jsonl`
- `data/anomaly/anomaly_list.csv`
- `data/inquiry/inquiry_candidates.csv`
- `data/inquiry/inquiry_discovery_cache.json`
- `data/inquiry/pdf/*.pdf`
- `data/inquiry/inquiry_records.jsonl`
- `outputs/dataset_check_report.md`
- `outputs/reports/inquiry_orphan_pdf_report.md`
- `outputs/loop_evaluation.json`
- `outputs/final_report_auto.md`
- `final_report.md`
- `docs/eval_report_template.md`
- `docs/worklogs/*.md`

## 9. Document Map

| 文档 | 职责 |
| --- | --- |
| `README.md` | 安装、运行、快速开始 |
| `SPEC.md` | **项目总纲**：契约、研究问题、验收标准、当前能力快照 |
| `AGENTS.md` | Agent 指令入口（指向 `CLAUDE.md`） |
| `docs/README.md` | `docs/` 目录索引 |
| `docs/architecture.md` | 已验证/进行中阶段的架构与数据流 |
| `docs/crawl_spec.md` | 抓取范围、股票池、公告类型、限速策略 |
| `docs/HANDOFF.md` | 会话交接、变更历史、下一步 |
| `docs/topic_proposal.md` | 研究问题、变量定义、课程要求映射 |
| `docs/workflow_design.md` | Pipeline 节点 canonical 表、人工检查点、最小运行命令 |
| `docs/cninfo_official_api_reference.md` | 深证信官方 API 目录、典型接口元数据、参数校准参考（进行中） |
| `docs/cninfo_official_api_catalog.md` | 2465 个接口全量层级目录（可见 + 隐藏类目，进行中） |
| `docs/worklogs/` | 周次过程、AI 使用记录、实际命令、问题修复 |
