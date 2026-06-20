# 项目2：研发资本化风险排序与问询函可行性测试

> 期末项目（挑战档 1.1x）

## 项目背景

上市公司在财务处理中可以选择将研发支出**资本化**（计入资产，分年摊销）或**费用化**（计入当期损益）。资本化比例过高往往意味着利润操纵空间增大——企业可能通过激进资本化来平滑利润、规避亏损或满足业绩承诺。

本项目从上市公司年报 PDF 中自动抽取研发相关财务字段，构建**风险评分模型**识别资本化激进公司，并通过交易所实际发出的**问询函**进行问询闭环可行性测试：

- **模型预测为异常**的 company-year 是否真的收到研发资本化相关问询？（验证 Precision）
- **收到相关问询**的 company-year 是否被模型提前识别？（验证 Recall）
- 监管关注的核心模式是什么？企业回复是否充分？

最终构建"年报抽取 → 风险排序 → 全样本问询标签 → 模式总结"的完整分析闭环。

> ⚠️ **队友原始工作存档声明（必读）**
>
> [`../temp-队友做的东西原件/`](../temp-队友做的东西原件/) 存放的是队友 Week 11–14 的原始产物。**该存档被明确标记为不可信来源（UNTRUSTED SOURCE）。**
>
> - **禁止直接取用**：其中的代码、Schema、Prompt、数据、结论均不能直接采用到 `project2/` 中。
> - **仅可作重构参考**：只能把它当作“主题方向参考”和“反面教材”，帮助理解队友当时的思路。
> - **必须以老师讲义和当前代码为准**：所有核心实现、字段口径、评分逻辑、验证方式都需重新审阅、重写或确认。
> - **采用前必须复核**：若确需参考其中某段实现，必须先说明它解决的问题、逐行审查关键假设、写入测试或做小样本实证，再迁移到正式代码。
> - **不得作为接口来源证据**：外部 API 端点、参数、字段含义和研究结论，必须能被官方文档、当前代码测试或真实运行日志独立验证；队友原件本身不算证据。
> - **开源参考需登记**：CNINFO 相关外部仓库只作为线索或工程参考，来源、license 和采用边界记录在 [`docs/cninfo_external_references.md`](docs/cninfo_external_references.md)。
> - **AI 提示**：阅读该存档时，请默认其内容可能存在事实错误、逻辑漏洞、未验证假设和过时报错，不要将其作为真相源。

---

## 核心假设

1. **资本化率异常**：某年度研发资本化率显著高于历史均值或行业均值，存在激进确认嫌疑
2. **资本化增速异常**：资本化金额同比增速远超研发费用整体增速，存在结构调节嫌疑
3. **行业偏离**：资本化水平显著偏离同行业可比公司中位数，可能存在会计政策选择偏好
4. **问询函信号**：交易所问询函是外部监管关注信号，可用于描述性验证模型有效性

---

## 数据覆盖

| 指标 | 目标要求 | 当前进度 |
| -------- | ---------- | ---------- |
| 年报 PDF | ≥ 150 份 | **official API 路线已完成 150/150**：crawl → download → audit 全链路通过，PDF 文件名与 metadata 已统一 |
| 核心抽取字段 | ≥ 10 个 | 14 个 Schema 已定义，口径已写死 |
| Pipeline 阶段 | 年报主线 + 问询闭环 | **后段已全量跑通**：crawl/download/audit/parse 150/150；validate 150/150；score 83 scored / 67 no-score（未评分）；detect 17 anomalies；analyze 已输出混淆矩阵；report 已生成课堂展示版 |
| 已评分公司 | — | 150 条 company-year 已进入评分文件；83 条有可用风险分，字段不足的 67 条保留 `null` 和 `data_quality_notes` |
| 问询候选与标签 | 覆盖 150 个 company-year | 候选发现与 PDF 下载已形成稳定输入：28 条候选、28 个 PDF、orphan=0；`inquiry-label` 已生成 150 条标签，其中 10 条有候选、1 条命中实质研发资本化问询（v2 语义标签） |
| 人工校验样本 | ≥ 30 条 | 已由 AI agent 辅助交叉验证 35 条（见 `outputs/reports/eval_report_final.md`）；优先覆盖 17 条异常和 1 条问询 related 样本 |

### 核心抽取字段

| 字段 | 来源 | 说明 |
| -------- | -------- | -------- |
| `company_name` | 年报封面 | 公司名称 |
| `company_code` | 年报封面 | 股票代码 |
| `year` | 年报封面 | 报告年度 |
| `rd_expense_total` | 财务报表附注 | 研发支出总额（万元） |
| `rd_capitalized_amount` | 财务报表附注 | 资本化研发支出（万元） |
| `rd_expensed_amount` | 财务报表附注 | 费用化研发支出（万元） |
| `capitalization_rate` | 计算字段 | 资本化率 = 资本化 / (资本化 + 费用化) |
| `dev_cost_opening` | 财务报表附注 | 开发支出期初余额（万元） |
| `dev_cost_closing` | 财务报表附注 | 开发支出期末余额（万元） |
| `impairment` | 财务报表附注 | 减值准备（万元） |
| `capitalization_condition` | 财务报表附注 | 资本化条件描述 |

> 字段清单定义于 [`src/model/schemas.py`](src/model/schemas.py)（Pydantic Schema），校验规则见 [`configs/model_config.yaml`](configs/model_config.yaml)。

## 当前研究结果

2026-06-15 已按 extract 全量结果重跑：

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```

| 指标 | 最新结果 | 研究含义 |
| --- | ---: | --- |
| 理论样本 | 150 | 50 家研发密集型上市公司 × 2021-2023 年 |
| validate | 150/150 passed | 年报字段已形成可复核的结构化记录 |
| 可计算资本化率 | 60 | 这些记录可直接比较资本化水平 |
| 有风险分记录 | 83 | 进入异常排序；其余记录因关键字段缺失保留说明 |
| 异常样本 | 17 | 在 83 条可评分记录中取前 20% 左右；换算到 150 全样本为 11.33% |
| 平均 / 中位资本化率 | 11.57% / 2.67% | 分布右偏，风险主要集中在少数尾部样本 |
| 异常组 / 非异常组资本化率 | 23.81% / 6.73% | 异常组整体资本化率更高，但异常名单仍是混合信号 |
| 问询相关标签 | 1 | 已改用脚本剪枝 + LLM 语义二分类；候选集中 1 条 company-year 命中实质针对研发资本化的问询函 |
| 闭环矩阵 | TP=0 / FP=17 / TN=132 / FN=1 | 链路跑通；当前标签严格，正样本极少，统计上接近空 |

课堂展示的结论应写得保守：本项目已经把年报 PDF、LLM 字段抽取、财务风险评分和问询函验证接成闭环；当前样本显示研发资本化风险更像尾部风险，而不是全样本普遍风险；问询函闭环能跑，但还需要全文语义标签和人工复核来提高监管解释力。

## 风险模型与建模口径

本项目没有直接训练监督学习分类器。原因是研发资本化相关问询样本少，而且当前问询标签仍是 MVP 弱标签。现阶段采用可解释的金融规则评分模型，把每个 company-year 映射成 `aggressiveness_score`。

模型核心思路：

- **资本化率**：按 disclosure → 重算 → 拆分 → 总额的顺序取值；
- **行业偏离度**：在同行业同年度内计算资本化率百分位；
- **跨期变化**：对资本化率年度变化做 Z 评分；
- **条件模糊度**：统计资本化条件文本中的模糊词命中数；
- **恒等式置信度**：把“资本化 + 费用化 ≈ 总额”的一致性作为最终风险分乘数（折扣），而不是激进信号。

完整公式、变量定义、阈值与启发式参数审计表见 [`docs/methodology.md`](docs/methodology.md)。

> **注意**：行业归属优先读 `configs/crawl.yaml` 的显式 `industry` 字段（20 医药制造 / 20 电子设备 / 10 软件信息），缺失时才回退到公司排列顺序启发式。异常名单是混合信号，少数资本化率为 0% 的样本可能由披露模糊度或跨期变化触发，不能直接解释为激进资本化。

---

## 环境要求

- **Python** ≥ 3.10（推荐 3.11）
- **uv** ≥ 0.5.0（依赖管理）
- **MinerU**（用户级外部 CLI，**建议 GPU**，详见 [`docs/mineru_setup.md`](docs/mineru_setup.md)）
  - 默认通过 `uv tool` 安装一份全局 `mineru[all]`，多个项目共用
  - 项目调用 `mineru -p <pdf> -o <output> -b pipeline`，并设置 `MINERU_DEVICE_MODE=cuda`
- **LLM API Key**（字段抽取阶段使用，支持 OpenAI / 智谱 / DeepSeek 等）

## 执行原则

- **时间进度**：由项目团队自行把控，以讲义周次为参照，不赶 deadline。
- **API 成本**：API 调用成本在可接受范围内，以结果质量优先，不过度优化成本。
- **代码质量**：所有代码必须优雅、规范、可测试，不为了追求速度而牺牲质量。

---

## 文档地图

| 文档 | 用途 |
| -------- | -------- |
| [`SPEC.md`](SPEC.md) | **项目总纲**：契约、研究问题、验收标准、当前能力快照 |
| [`AGENTS.md`](AGENTS.md) | Agent 指令入口（老师模板要求） |
| [`CLAUDE.md`](CLAUDE.md) | Agent 指令、编码约束、数据规则 |
| [`docs/README.md`](docs/README.md) | `docs/` 目录索引 |
| [`docs/HANDOFF.md`](docs/HANDOFF.md) | 会话交接、变更历史、下一步 |
| [`docs/architecture.md`](docs/architecture.md) | 已验证/进行中阶段的架构与数据流 |
| [`docs/crawl_spec.md`](docs/crawl_spec.md) | 抓取范围、股票池、公告类型、限速策略 |
| [`docs/topic_proposal.md`](docs/topic_proposal.md) | 研究问题、变量定义、课程要求映射 |
| [`docs/workflow_design.md`](docs/workflow_design.md) | Pipeline 节点 canonical 表、人工检查点、最小运行命令 |
| [`docs/cninfo_external_references.md`](docs/cninfo_external_references.md) | CNINFO 外部开源参考、license、影响范围与复用边界 |
| [`docs/cninfo_official_api_reference.md`](docs/cninfo_official_api_reference.md) | 深证信官方 API 目录、典型接口元数据、参数校准参考（进行中） |
| [`docs/cninfo_official_api_catalog.md`](docs/cninfo_official_api_catalog.md) | 2465 个接口全量层级目录（可见 + 隐藏类目，进行中） |
| [`docs/worklogs/`](docs/worklogs/) | 周次过程、AI 使用记录、实际命令、问题修复 |

---

## 快速开始

### 1. 安装依赖

```powershell
# 进入项目目录
cd project2

# 同步依赖
uv sync
```

### 2. 配置环境变量

```powershell
# 复制模板
copy .env.example .env

# 编辑 .env，填入你的 API Key
# LLM_API_KEY=sk-...
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL=gpt-4o-mini  # 或使用 .env.example 中的其它兼容接口
# 本机已登录 Kimi Code CLI 时可改用：LLM_BACKEND=kimi_code_cli
```

### 3. 验证环境

```powershell
# 运行测试，确保环境正常
uv run pytest

# 运行数据质量审计（无需 API Key）
uv run python src/main.py --stage audit
```

### 4. 运行最小 Pipeline（测试用）

```powershell
# 仅跑前三个阶段，验证全流程通顺
uv run python src/main.py --stage crawl
uv run python src/main.py --stage download
uv run python src/main.py --stage parse --parse-backend local
# MinerU API 分段 smoke（需先设置 MINERU_API_KEY）
uv run python src/main.py --stage parse --parse-backend api --limit 1
# MinerU API URL batch 小批量验证（推荐推进路线）
uv run python src/main.py --stage parse --parse-backend api-batch --limit 2
```

> 当前推荐使用 `api-batch` 复跑或补跑年报 parse：它会按 200 页拆分、通过 URL batch endpoint 提交、记录 task、支持断点恢复。官方提交限流为 50 files/min，本项目默认 `MINERU_API_BATCH_SIZE=50`，并用 `MINERU_API_DOWNLOAD_WORKERS=8` / `MINERU_API_EXTRACT_WORKERS=4` 并发下载和解压结果包；查询限流 1000/min，5 秒轮询不会接近上限。
> 跑 API parse 时建议关闭 VPN 或确认 MinerU CDN 连接稳定。若只在结果 zip 下载阶段遇到 SSL/网络短断，直接重跑同一命令即可复用原 batch、刷新 `full_zip_url` 并补下载，不会重复提交已完成 segment。当前 150 份年报 Markdown、route、extract、validate 和下游闭环都已跑通；后续重点是人工复核字段缺失样本与问询弱标签。

### 5. 运行完整 Pipeline

```powershell
# 一键运行全部阶段
uv run python src/main.py --stage all

# 或分阶段执行（推荐首次使用，便于排查问题）
uv run python src/main.py --stage crawl      # 抓取公告元数据
uv run python src/main.py --stage download   # 下载 PDF
uv run python src/main.py --stage audit      # 数据质量检查
uv run python src/main.py --stage parse      # MinerU 本地解析（默认 local backend）
uv run python src/main.py --stage parse --parse-backend api --limit 1  # MinerU API 分段 smoke
uv run python src/main.py --stage parse --parse-backend api-batch --limit 2  # MinerU API URL batch smoke
uv run python src/main.py --stage route      # 章节定位
uv run python src/main.py --stage extract    # LLM 字段抽取
uv run python src/main.py --stage validate   # Pydantic 校验
uv run python src/main.py --stage score      # 风险评分与数据质量校验
uv run python src/main.py --stage detect     # 风险排序（标记重点复核样本）
uv run python src/main.py --stage inquiry    # 问询候选发现，可断点恢复
uv run python src/main.py --stage inquiry-download  # 下载已发现的问询候选 PDF
uv run python src/main.py --stage inquiry-label  # 标记问询是否涉及研发资本化
uv run python src/main.py --stage analyze    # 闭环分析
uv run python src/main.py --stage report     # 报告生成
```

extract 已完成后，推荐直接刷新后段：

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```

---

## Pipeline 阶段简介

完整节点表（输入、输出、成功标准、失败处理、日志）见 [`docs/workflow_design.md`](docs/workflow_design.md)。

| 阶段 | 命令 | 一句话说明 |
| -------- | -------- | -------- |
| **crawl** | `--stage crawl` | 抓取公告元数据 |
| **download** | `--stage download` | 下载 PDF |
| **audit** | `--stage audit` | 数据质量审计 |
| **parse** | `--stage parse` | MinerU 解析 PDF 为 Markdown |
| **route** | `--stage route` | 定位研发相关章节 |
| **extract** | `--stage extract` | LLM 抽取结构化字段 |
| **validate** | `--stage validate` | Pydantic Schema 校验 |
| **score** | `--stage score` | 风险评分与数据质量校验 |
| **detect** | `--stage detect` | 风险排序（前 20% 重点样本） |
| **inquiry** | `--stage inquiry` | 问询候选发现；逐条写入候选、日志和 checkpoint |
| **inquiry-download** | `--stage inquiry-download` | 下载已发现的问询候选 PDF，并回写首页标题校验结果 |
| **inquiry-label** | `--stage inquiry-label` | 标记候选问询是否涉及研发、资本化、开发支出、无形资产或费用化 |
| **analyze** | `--stage analyze` | 构建混淆矩阵与指标 |
| **report** | `--stage report` | 生成最终报告 |

### 阶段依赖关系

```
crawl → download → audit → parse → route → extract → validate → score → detect
  ↓                                                       ↓
inquiry → inquiry-download → inquiry-label ─────────────┘
                          ↓
                        analyze
                          ↓
                        report
```

> **注意**：`audit` 可随时独立运行检查数据质量；`validate` 失败时可单独修复后重跑 `extract` → `validate` 子链，无需从头开始。

---

## 项目结构

```
project2/
├── src/                          # 源代码
│   ├── main.py                   # CLI 入口：统一调度各阶段
│   ├── common.py                 # 公共工具：配置加载、JSONL 读写、日志
│   ├── crawl/                    # 巨潮 API 封装（已实现）
│   │   ├── __init__.py
│   │   └── cninfo_api.py         # 年报公告爬虫（含断点续传）
│   ├── download/                 # PDF 下载器（已实现）
│   │   ├── __init__.py
│   │   └── downloader.py         # PDF 下载 + 完整性校验
│   ├── audit/                    # 数据质量审计（已实现）
│   │   ├── __init__.py
│   │   └── auditor.py            # 6 项数据质量检查
│   ├── parse/                    # MinerU 解析（年报 150/150 已跑通）
│   │   └── __init__.py
│   ├── route/                    # 章节定位（已实现）
│   │   └── __init__.py
│   ├── extract/                  # LLM 字段抽取 + 确定性表格提取
│   │   ├── __init__.py
│   │   ├── llm_client.py         # LLM API 调用封装
│   │   ├── llm_extractor.py      # 章节切片 → 结构化字段（FieldEvidence）
│   │   └── rd_table_extractor.py # 从 MinerU Markdown HTML 表格确定性提取研发数值（LLM fallback）
│   ├── model/                    # Pydantic Schema
│   │   ├── __init__.py
│   │   └── schemas.py            # 核心字段 Pydantic Schema
│   ├── validate/                 # Pydantic 校验 + 表格回填（已实现）
│   │   └── __init__.py
│   ├── analysis/                 # 评分、检测、问询标签、分析、报告逻辑（已实现）
│   │   ├── __init__.py
│   │   ├── scorer.py             # 四维度风险评分（aggressiveness_score）
│   │   ├── detector.py           # 风险排序（前 20% + 异常类型）
│   │   ├── inquiry_labeler.py    # 问询相关性标签（脚本剪枝 + LLM 语义二分类）
│   │   ├── evaluator.py          # 闭环混淆矩阵与指标
│   │   └── reporter.py           # 课堂展示报告生成
│   └── pipeline/                 # 预留目录；当前由 src/main.py 统一编排
│       └── __init__.py
├── tests/                        # pytest 测试套件
│   ├── __init__.py
│   └── test_*.py                 # 覆盖 schemas / crawler / router / extractor / labeler / validator / main
├── configs/                      # YAML 配置文件
│   ├── crawl.yaml                # 爬取参数（并发数、重试策略）
│   ├── mineru_config_legacy.json # 旧版 magic-pdf 配置存档（MinerU 3.x 不再使用）
│   ├── model_config.yaml         # 模型配置（Schema 规则、评分权重、表格 fallback）
│   ├── section_rules.yaml        # 章节定位规则（关键词匹配）
│   └── workflow.yaml             # 工作流编排（阶段依赖、跳过逻辑）
├── data/                         # 数据目录（gitignored）
│   ├── metadata/                 # 爬取元数据（CSV）
│   ├── pdf/                      # 原始 PDF
│   ├── parsed/                   # MinerU 解析后的 Markdown
│   ├── sections/                 # 章节定位切片
│   ├── extracted/                # LLM 抽取的原始 JSONL + tables/（确定性表格值）
│   ├── validated/                # Pydantic 校验后的 JSONL
│   ├── scored/                   # 风险评分与数据质量结果 JSONL
│   ├── anomaly/                  # 风险排序输出（CSV）
│   └── inquiry/                  # 问询函 PDF 与解析结果
├── docs/                         # 项目文档
│   ├── README.md                 # docs 目录索引
│   ├── methodology.md            # 方法论单一真源：LaTeX 公式、阈值、启发式审计表
│   ├── ai_usage_statement.md     # AI 使用声明
│   ├── architecture.md           # 项目架构与决策文档
│   ├── cninfo_data_discovery.md  # 巨潮数据探索记录
│   ├── crawl_spec.md             # 爬取规范
│   ├── cninfo_external_references.md # CNINFO 外部参考来源登记
│   ├── eval_report_template.md   # 人工评估报告模板
│   ├── HANDOFF.md                # 工作交接文档
│   ├── mineru_setup.md           # MinerU GPU 配置指南
│   ├── output_sample.md          # 输出样例
│   ├── parse_check.md            # 解析质量检查清单
│   ├── presentation_checklist.md # 期末展示检查清单
│   ├── topic_ideas.md            # 选题思路
│   ├── topic_proposal.md         # 选题方案
│   ├── workflow_design.md        # 工作流设计
│   └── worklogs/                 # AI 工作日志
│       ├── ai_worklog_week11.md
│       ├── ai_worklog_week12.md
│       ├── ai_worklog_week13.md
│       ├── ai_worklog_week14.md
│       ├── ai_worklog_week15.md
│       └── ai_worklog_week16.md
├── outputs/                      # 输出目录（gitignored）
│   ├── dataset_check_report.md   # 数据质量审计报告
│   ├── loop_evaluation.json      # 闭环评估结果（混淆矩阵 + 指标）
│   └── final_report.md           # 最终分析报告
├── SPEC.md                       # 项目契约与验收标准
├── pyproject.toml                # uv 依赖配置
├── .env.example                  # 环境变量模板
└── README.md                     # 本文件
```

---

## 输出产物

运行完整 Pipeline 后，各目录将生成以下关键文件：

### `data/` 中间产物

| 文件 | 说明 | 产生阶段 |
| -------- | -------- | -------- |
| `data/metadata/metadata.csv` | 巨潮爬取的公告元数据 | crawl |
| `data/parsed/{doc_id}.md` | MinerU 解析后的年报 Markdown，供 route/extract 使用 | parse |
| `data/parsed/mineru_api_raw/{doc_id}/part_*/` | MinerU API 原始 zip 和解压结果 | parse --parse-backend api/api-batch |
| `data/parsed/mineru_api_tasks.jsonl` | MinerU API task/batch 断点与审计日志 | parse --parse-backend api/api-batch |
| `data/sections/*.jsonl` | 章节定位切片 | route |
| `data/extracted/records.jsonl` | LLM 抽取的原始字段 | extract |
| `data/extracted/tables/tables.jsonl` | 确定性表格提取的研发投入/开发支出数值（validate fallback） | rd_table_extractor |
| `data/validated/records.jsonl` | Pydantic 校验后数据（含表格回填） | validate |
| `data/scored/records.jsonl` | 风险评分与数据质量明细 | score |
| `data/anomaly/anomaly_list.csv` | 风险排序结果 | detect |
| `data/inquiry/inquiry_candidates.csv` | 全样本问询候选 metadata | inquiry |
| `data/inquiry/inquiry_discovery_cache.json` | 问询候选 discovery 断点文件 | inquiry |
| `data/inquiry/pdf/*.pdf` | 问询函、回复函等候选 PDF | inquiry-download |
| `data/inquiry/inquiry_records.jsonl` | 问询标签与配对结果 | inquiry-label |

### `outputs/` 最终产物

| 文件 | 说明 | 产生阶段 |
| -------- | -------- | -------- |
| `outputs/dataset_check_report.md` | 数据质量审计报告 | audit |
| `outputs/reports/inquiry_orphan_pdf_report.md` | 未被当前候选表引用的旧问询 PDF 清单 | inquiry-download |
| `outputs/loop_evaluation.json` | 混淆矩阵与条件式评估指标 | analyze |
| `final_report.md`（根目录） | 最终答辩报告（手写版，老师看的交付物） | Phase 3 写作工作台 |
| `outputs/final_report_auto.md` | 自动生成的技术底稿（可复现） | report |

---

## 扩展方案：问询函闭环分析

本项目在课程基础要求之上增加**问询函可行性测试**模块：

| 步骤 | 动作 | 目的 |
| -------- | -------- | -------- |
| 1 | 从年报抽取研发资本化核心字段 | 构建结构化数据集 |
| 2 | 风险评分模型识别激进 company-year | 产生异常预测标签 |
| 3 | 对全部 150 个 company-year 查询问询候选 | 避免只查异常样本造成验证偏差 |
| 4 | 解析问询文本并生成研发资本化相关标签 | 获取外部监管关注信号 |
| 5 | 构建 TP/FP/TN/FN 混淆矩阵 | 量化模型有效性 |
| 6 | 分析问询关注模式与回复充分性 | 提炼监管逻辑，反哺模型优化 |

### 评估指标

| 指标 | 公式 | 说明 |
| -------- | -------- | -------- |
| Precision | TP / (TP + FP) | 模型标记为异常的 company-year 中，实际存在相关问询的比例 |
| Recall | TP / (TP + FN) | 存在相关问询的 company-year 中，被模型提前标记的比例 |
| F1-Score | 2 × Precision × Recall / (Precision + Recall) | 综合衡量 |
| Specificity | TN / (TN + FP) | 模型标记为正常的公司中，实际未被问询的比例 |

当研发资本化相关问询样本不足时，Precision / Recall / F1 只作描述性参考或不输出，报告改用 Top-K 命中率、候选覆盖率和典型案例分析。

---

## 项目历史与重构说明

本项目主题方向由团队共同确定，代码实现经历了渐进式重构：先逐周审读队友 Week 11–14 的代码，理解思路并识别问题；再在此基础上逐步替换不合理部分，保留可用设计；最终叠加挑战档要求的评分模型与问询闭环可行性测试，形成当前版本。

队友原始工作存档于 [`../temp-队友做的东西原件/`](../temp-队友做的东西原件/)，**为不可信来源（UNTRUSTED SOURCE），禁止直接取用，仅可作重构参考**。

关键升级：

- 分散脚本 → 统一 CLI 入口（`src/main.py --stage`）
- 基础字段抽取 → 风险评分 + 数据质量校验 + 风险排序
- 零验证 → 全样本问询标签闭环（条件式 Precision / Recall / F1）
- 无测试 → pytest 覆盖

## 课程依据

本项目核心 Pipeline 与方法论严格遵循老师讲义要求。

<details>
<summary>📋 点击展开：课程讲义对照表</summary>

| 项目内容 | 讲义依据 |
| -------- | -------- |
| 巨潮公告爬取与下载 | Week 12 讲义 + Lab |
| MinerU PDF 解析 | Week 13 讲义 + Lab |
| Pydantic Schema 设计、字段抽取与校验 | Week 13 讲义 |
| 工作流编排（Pipeline 串联） | Week 14 讲义 + Lab |
| 结果评估与 Prompt 优化 | Week 15 讲义 |
| 期末展示与报告要求 | Week 16 讲义 |

**执行原则**：所有开发必须以老师讲义为根本依据。扩展功能（如问询函闭环分析）仅在满足讲义基础要求的前提下增加，确保以下核心指标不缩水：

- 数据规模：≥ 150 份年报 PDF
- 字段数量：≥ 10 个核心字段
- Pipeline 完整度：爬取 → 解析 → 抽取 → 校验 → 评分 → 报告
- 人工评估：≥ 30 条样本的人工校验

完整讲义索引见仓库根目录 [`00-课程讲义/`](../00-课程讲义/)。

</details>

---

## 编码规范

- **文件编码**：`open()` / `pd.read_csv()` / `pd.to_csv()` 永远显式写 `encoding="utf-8"`
- **依赖管理**：使用 `uv sync` / `uv run` / `uv add`，不直接 `pip install`
- **测试**：新增功能必须配套 pytest 用例，运行 `uv run pytest` 通过后方可提交
- **详细规范**：见 [`CLAUDE.md`](CLAUDE.md)；项目验收标准见 [`SPEC.md`](SPEC.md)

---

## 更新日志

| 日期 | 变更 |
| -------- | -------- |
| 2026-06-07 | 项目初始化：uv + pyproject.toml + Pipeline 骨架（队友） |
| 2026-06-07 | 迁移核心模块：爬取、解析、抽取、Schema（队友） |
| 2026-06-08 | 重构项目目录结构，完善 Week 11 交付文档与配置 |
| 2026-06-13 | 文档整理：强化队友存档不可信声明、修正数据覆盖进度、删除来源不明的故障排查章节、重命名评估模板、删除队友遗留 prompt_v1.md、新增 docs/README.md 与 AGENTS.md |
| 2026-06-09 | 完成项目架构与决策文档，补齐抓取规格；统一执行原则；创建 download/ 和 audit/ 目录 |

---

上海对外经贸大学 · 数据挖掘与机器学习 · 期末项目 · 2025-2026 学年
