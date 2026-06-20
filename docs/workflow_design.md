# Workflow Design

## 项目目标

构建从年报 PDF 到结构化数据再到风险排序与问询闭环可行性测试的完整 Pipeline，实现研发资本化风险排序与交易所问询函可行性测试。

## 节点表

| 节点 | 输入 | 输出 | 成功标准 | 失败处理 | 日志 |
| -------- | -------- | -------- | -------- | -------- | -------- |
| crawl | 无 | `data/metadata/metadata.csv` | 成功抓取 150 条年报元数据 | 记录失败条目到 `failed_downloads.csv`，支持重跑 | `crawl.log` |
| download | `data/metadata/metadata.csv` | `data/pdf/` | 所有 PDF 成功下载，文件大小正常 | 标记失败文件，支持断点续传 | `download.log` |
| audit | `data/pdf/` | `outputs/dataset_check_report.md` | 100% PDF 通过完整性检查 | 生成异常文件清单，人工确认后处理 | `audit.log` |
| parse | `data/pdf/` | `data/parsed/*.md` | 所有 PDF 成功解析为 Markdown | 扫描版 PDF 标记跳过 | `parse.log` |
| route | `data/parsed/*.md` | `data/sections/*.jsonl` | 目标章节定位成功率 ≥ 90% | 未定位到的章节记录原因 | `route.log` |
| extract | `data/sections/*.jsonl` | `data/extracted/records.jsonl` | 14 个核心字段抽取率 ≥ 85% | 记录缺失字段和原因 | `extract.log` |
| validate | `data/extracted/records.jsonl` | `data/validated/records.jsonl` | Pydantic 校验通过率 ≥ 90% | 分类错误类型（类型/范围/交叉），回流修复 | `validate.log` |
| score | `data/validated/records.jsonl` | `data/scored/records.jsonl` | 所有记录完成风险评分和数据质量校验 | 字段缺失导致无法评分时记录原因 | `score.log` |
| detect | `data/scored/records.jsonl` | `data/anomaly/anomaly_list.csv` | 成功标记异常公司 | 检查评分分布是否合理 | `detect.log` |
| inquiry | `data/metadata/metadata.csv` | `data/inquiry/inquiry_candidates.csv` | 覆盖全部 150 个 company-year 的问询候选查询；逐条写入 checkpoint，可中断恢复 | 记录无候选、查询失败和需人工校准的分类码 | `inquiry.log` |
| inquiry-download | `data/inquiry/inquiry_candidates.csv` | `data/inquiry/pdf/*.pdf` + `outputs/reports/inquiry_orphan_pdf_report.md` | 按候选 metadata 下载问询函、回复函等 PDF，回写下载状态与首页标题校验结果 | 标记失败文件，支持重跑补下载；旧 PDF 只进入 orphan 报告，不自动删除 | `inquiry_download_log.jsonl` |
| inquiry-label | `data/inquiry/inquiry_candidates.csv` | `data/inquiry/inquiry_records.jsonl` | 完成问询内容判断并生成全样本 company-year 标签 | 无相关问询也保留记录，用于 FN/TN | `inquiry.log` |
| analyze | `data/scored/records.jsonl` + `data/anomaly/anomaly_list.csv` + `data/inquiry/inquiry_records.jsonl` | `outputs/loop_evaluation.json` | 成功生成混淆矩阵和条件式指标 | 检查 TP/FP/TN/FN 分布；样本不足时转为 Top-K 和案例分析 | `analyze.log` |
| report | `outputs/loop_evaluation.json` | `outputs/final_report.md` | 生成完整 Markdown 报告 | — | `report.log` |

## 流程图

```
    crawl → download → audit → parse → route → extract → validate → score → detect
      ↓                                                       ↓
 inquiry → inquiry-download → inquiry-label ─────────────────┘
                              ↓
                            analyze
                              ↓
                            report
```

## 人工检查点

| 检查点 | 位置 | 检查内容 |
| -------- | -------- | -------- |
| CP1 | audit 后 | PDF 完整性、文件大小异常 |
| CP2 | parse 后 | 解析质量检查（页码保留、表格完整、无乱码） |
| CP3 | route 后 | 目标章节是否正确定位 |
| CP4 | extract 后 | 30 条样本人工校验 |
| CP5 | validate 后 | 校验失败记录分析 |
| CP6 | score 后 | 评分分布合理性检查 |
| CP7a | inquiry 后 | 候选标题是否属于问询函、回复函、关注函或监管工作函；PDF URL 是否存在，抽查是否可下载 |
| CP7a-download | inquiry-download 后 | 候选 PDF 下载状态是否为 success；PDF 首页标题是否与候选标题基本一致；orphan 报告中的旧 PDF 是否需要人工保留 |
| CP7b | inquiry-label 后 | 问询候选标题/正文是否确实涉及研发、资本化、开发支出、无形资产或费用化 |
| CP8 | analyze 后 | 混淆矩阵结果合理性确认；样本不足时检查 Top-K 和案例分析是否更合适 |

## 最小运行命令

```powershell
# 1. 安装依赖
cd project2
uv sync

# 2. 配置环境
copy .env.example .env
# 编辑 .env 填入 API Key

# 3. 验证环境
uv run pytest
uv run python src/main.py --stage audit

# 4. 运行完整 Pipeline
uv run python src/main.py --stage all

# 或分阶段执行
uv run python src/main.py --stage crawl
uv run python src/main.py --stage download
uv run python src/main.py --stage parse
uv run python src/main.py --stage route
uv run python src/main.py --stage extract
uv run python src/main.py --stage validate
uv run python src/main.py --stage score
uv run python src/main.py --stage detect
uv run python src/main.py --stage inquiry    # 问询候选 discovery，可断点恢复
uv run python src/main.py --stage inquiry-download    # 下载已发现的问询候选 PDF
uv run python src/main.py --stage inquiry-label    # 生成全样本问询弱标签
uv run python src/main.py --stage analyze
uv run python src/main.py --stage report
```

extract 已完成后可直接刷新后段：

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```
