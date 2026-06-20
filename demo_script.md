# Demo Script — 一条完整证据链

> Week 16 讲义要求：Demo 不要求现场跑完整数据集，但必须展示一条完整证据链 `PDF → metadata → MinerU 解析片段 → section 定位 → LLM 抽取 → Pydantic 校验 → final result → evidence_text/page_no`。本脚本以 `000063_中兴通讯_2021年报` 为样本，逐步展示该证据链。网络或 API 不稳定时，可展示提前保存的小样本输出，并说明如何由项目代码生成。

## 0. 样本选择

- **公司**：中兴通讯（000063），医药制造/电子设备/软件信息中的电子设备行业
- **报告年度**：2021
- **doc_id**：`000063_中兴通讯_2021年报`
- **选择理由**：研发投入字段完整披露，资本化率可直接计算，会计恒等式成立，适合展示完整链路。

## 1. 原始 PDF

```text
文件：data/pdf/000063_中兴通讯_2021年报.pdf
来源：巨潮资讯网公开公告（official API 路线抓取）
```

展示要点：打开 PDF，翻到「研发投入」表格所在页，指出「研发投入金额 / 资本化的金额 / 费用化的金额」三行。

## 2. metadata 记录

```powershell
uv run python -c "import csv; [print(r) for r in csv.DictReader(open('data/metadata/metadata.csv',encoding='utf-8')) if r['doc_id']=='000063_中兴通讯_2021年报']"
```

关键字段：`doc_id`、`stock_code=000063`、`stock_name=中兴通讯`、`publish_date`、`pdf_url`、`download_status=success`、`source=cninfo_official_api`。

## 3. MinerU 解析片段

```text
文件：data/parsed/000063_中兴通讯_2021年报.md
```

展示要点：在 Markdown 中定位「研发投入」HTML 表格片段：

```text
## 研发投入情况
<table>
<tr><td>项目</td><td>2021年</td></tr>
<tr><td>研发投入金额</td><td>18,804.0</td></tr>
<tr><td>费用化的金额</td><td>16,997.5</td></tr>
<tr><td>资本化的金额</td><td>1,806.5</td></tr>
<tr><td>资本化研发投入占研发投入的比例</td><td>9.61%</td></tr>
</table>
```

> 原文单位为百万元人民币，抽取时换算为万元（×100）。

## 4. Section 定位

```text
文件：data/sections/000063_中兴通讯_2021年报_sections.jsonl
```

route 阶段按 `configs/section_rules.yaml` 的「研发费用」规则匹配到该切片，`match_reason` 含 `positive:研发投入金额,资本化的金额,...`，`match_score` 高。

可在 `outputs/reports/section_check_report.csv` 中查到该 doc 的 `found=yes`、`section_title`、`quality_issue`。

## 5. LLM 抽取结果

```text
文件：data/extracted/records.jsonl
```

LLM 按 `prompts/prompt_final.md` 模板抽取，关键字段（FieldEvidence 嵌套结构）：

| 字段 | value | evidence_text（原文片段） | page_no | confidence |
| -------- | --------: | -------- | --------: | --------: |
| rd_expense_total | 1,880,400.0 | 研发投入金额 18,804.0（百万元）→ 换算万元 | 0 | 0.95 |
| rd_capitalized_amount | 180,650.0 | 资本化的金额 1,806.5（百万元）→ 万元 | 0 | 0.90 |
| rd_expensed_amount | 1,699,750.0 | 费用化的金额 16,997.5（百万元）→ 万元 | 0 | 0.90 |
| capitalization_rate | 9.61 | 资本化研发投入占研发投入的比例 9.61% | 0 | 0.95 |
| capitalization_condition | （原文） | CAS6 资本化五条件描述 | 0 | 0.90 |

> evidence_text 必须是输入文本中的原文片段，不得编造（Week 13 Null Rule）。

## 6. Pydantic 校验

```powershell
uv run python -c "import json; [print(json.dumps({k:r[k] for k in ['doc_id','rd_expense_total','rd_capitalized_amount','rd_expensed_amount','capitalization_rate','calculated_capitalization_rate']},ensure_ascii=False)) for r in (json.loads(l) for l in open('data/validated/records.jsonl',encoding='utf-8')) if r['doc_id']=='000063_中兴通讯_2021年报']"
```

校验通过（validate 150/150 passed）。会计恒等式检查：

```text
rd_capitalized_amount + rd_expensed_amount = 180,650 + 1,699,750 = 1,880,400 = rd_expense_total ✓
capitalization_rate = 180,650 / 1,880,400 × 100 = 9.61% ✓（与披露值一致）
```

## 7. final result

在 `data/scored/records.jsonl` 中该 doc 的风险评分行；在 `outputs/results/final_results.csv` 终表中可查到该公司年份的完整记录（含 industry、capitalization_rate、aggressiveness_score、is_anomaly、问询标签）。

## 8. evidence_text / page_no 解释

- **evidence_text**：每个关键字段都带原文片段，可回到 `data/parsed/*.md` 或原始 PDF 复核。
- **page_no**：MinerU 解析的 Markdown 未保留稳定页码，本项目 `page_no` 多为 0/null，作为已知局限（见 `outputs/reports/section_check_report.csv` 的 `page_unavailable` 标记）。证据回溯主要依赖 evidence_text 原文片段，而非页码。

## 现场演示命令（小样本）

```powershell
cd project2
uv run python src/main.py --stage audit
uv run python src/main.py --stage route --limit 5   # 查看 section_check_report 产出
```

完整重跑后段（API 稳定时）：

```powershell
uv run python src/main.py --from-stage validate --to-stage report
```
