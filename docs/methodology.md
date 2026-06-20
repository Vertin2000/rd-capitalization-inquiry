# 方法论：研发资本化风险排序

> 本文档是 `project2/` 研究方法的单一真源（single source of truth）。
> 所有财会公式、风险评分公式、阈值规则与启发式匹配逻辑统一记录在此，
> 其他文档只保留 high-level 说明并链接到本文档。

---

## 目录

- [1. 研究问题与变量定义](#1-研究问题与变量定义)
- [2. 会计恒等式与资本化率](#2-会计恒等式与资本化率)
- [3. 风险评分模型](#3-风险评分模型)
- [4. 风险排序规则](#4-风险排序规则)
- [5. 校验阈值](#5-校验阈值)
- [6. 启发式匹配方法](#6-启发式匹配方法)
- [7. 表格提取与 LLM fallback](#7-表格提取与-llm-fallback)
- [8. 启发式参数与待审计项](#8-启发式参数与待审计项)

---

## 1. 研究问题与变量定义

### 1.1 研究问题

**核心问题**：哪些研发资本化特征与交易所问询相关？

- **子问题 1**：高资本化率是否更容易与问询相关？
- **子问题 2**：资本化率的剧烈变化是否更容易与问询相关？
- **子问题 3**：资本化条件描述模糊是否更容易与问询相关？

### 1.2 观察单位

观察单位是 **company-year**：公司 $i$ 在年报年度 $t$ 的研发资本化记录。

### 1.3 变量符号

| 符号 | 字段名 | 定义 |
| --- | --- | --- |
| $RD_{i,t}$ | `rd_expense_total` | 研发支出总额（万元） |
| $CAP_{i,t}$ | `rd_capitalized_amount` | 资本化研发支出（万元） |
| $EXP_{i,t}$ | `rd_expensed_amount` | 费用化研发支出（万元） |
| $CR_{i,t}$ | `capitalization_rate` | 研发资本化率（%） |
| $DEV^{open}_{i,t}$ | `dev_cost_opening` | 开发支出期初余额（万元） |
| $DEV^{close}_{i,t}$ | `dev_cost_closing` | 开发支出期末余额（万元） |
| $IMP_{i,t}$ | `impairment` | 减值准备（万元） |
| $COND_{i,t}$ | `capitalization_condition` | 资本化条件描述原文 |
| $Y_{i,t}$ | `capitalization_related` | 是否收到研发资本化相关问询 |
| $\hat{Y}_{i,t}$ | `is_anomaly` | 模型是否标记为异常 |

---

## 2. 会计恒等式与资本化率

### 2.1 研发投入拆分恒等式

年报披露的研发投入总额应约等于资本化金额与费用化金额之和：

$$
RD_{i,t} \approx CAP_{i,t} + EXP_{i,t}
$$

相对偏差：

$$
D^{idt}_{i,t} = \frac{|CAP_{i,t} + EXP_{i,t} - RD_{i,t}|}{RD_{i,t}}
$$

### 2.2 资本化率

主口径：

$$
CR_{i,t} = \frac{CAP_{i,t}}{CAP_{i,t} + EXP_{i,t}} \times 100
$$

Fallback 优先级（当分子分母不全时）：

1. 年报直接披露的 `capitalization_rate`；
2. 校验阶段重算的 `calculated_capitalization_rate`：
   $$CR^{calc}_{i,t} = \frac{CAP_{i,t}}{RD_{i,t}} \times 100$$
   若 $RD_{i,t}$ 缺失，则退化为 $CAP_{i,t} / (CAP_{i,t} + EXP_{i,t})$；
3. 用 $CAP_{i,t} / (CAP_{i,t} + EXP_{i,t})$ 计算；
4. 最后用 $CAP_{i,t} / RD_{i,t}$ 计算。

> **注意**：禁止把开发支出期末余额 $DEV^{close}_{i,t}$ 直接当作本期资本化金额 $CAP_{i,t}$。

---

## 3. 风险评分模型

综合风险分 `aggressiveness_score` 由三个正向信号和一个置信度乘数组成。

### 3.1 行业偏离度评分

在同一行业、同一年度内，计算本公司资本化率的百分位：

$$
P_{i,t} = \frac{\sum_{j \in \text{Peer}(i,t)} \mathbf{1}\{CR_{j,t} \le CR_{i,t}\}}{|\text{Peer}(i,t)|}
$$

$$
IS_{i,t} = P_{i,t} \times 100
$$

其中 $\text{Peer}(i,t)$ 为与公司 $i$ 同行业、同年度的其他公司集合。

> **行业归属来源**：优先读取 `configs/crawl.yaml` 中各公司显式配置的 `industry` 字段
> （20 医药制造 / 20 电子设备 / 10 软件信息）；仅当某公司缺失显式 `industry` 时，
> 才回退到按公司排列顺序启发式推断。代码见 `src/analysis/scorer.py::_industry_for_code`。

### 3.2 跨期变化评分

先计算资本化率年度变化：

$$
\Delta_{i,t} = CR_{i,t} - CR_{i,t-1}
$$

再对全样本变化值做 Z 标准化：

$$
Z_{i,t} = \frac{\Delta_{i,t} - \mu_{\Delta}}{\sigma_{\Delta}}
$$

其中 $\mu_{\Delta}$ 和 $\sigma_{\Delta}$ 分别用总体标准差（`pstdev`）计算。

变化评分：

$$
CS_{i,t} = \min\left(100, \frac{\max(0, Z_{i,t})}{2} \times 100\right)
$$

> **当前口径**：只取正向跳升 $\max(0, Z_{i,t})$，仅捕捉资本化率突然上升（变激进）。
> 资本化率骤降（如项目完结转无形资产）不视为激进信号。
> 若后续需研究“波动度”而非“激进程度”，可改回 $|Z_{i,t}|$。

### 3.3 条件模糊度评分

对资本化条件文本 $COND_{i,t}$ 统计模糊关键词命中数：

$$
FH_{i,t} = \sum_{k \in \mathcal{K}} \mathbf{1}\{k \in COND_{i,t}\}
$$

当前模糊词表 $\mathcal{K}$：

```text
视情况、根据情况、管理层判断、必要时、综合评估、谨慎判断、视具体、具体情况、重大判断、估计
```

> **词表设计**：刻意排除「等/相关/合理/未来/预计/预期/可能」等高频正向词。
> 「等」是汉语最高频字之一，命中即 +1 等于给所有非空文本加分；
> 「未来经济利益很可能流入」本是 CAS6 资本化五条件的合规披露，是正向证据而非模糊证据。
> 改为会计估计中真正体现「主观判断空间」的措辞。

模糊度评分（长度归一化）：

$$
FS_{i,t} = \min\left(1, \frac{FH_{i,t}}{\max(1, |COND_{i,t}| / N_c)}\right)
$$

其中 $N_c = 200$ 为归一化基准（每 200 字符预期 1 个模糊词命中）。

模糊度分量：

$$
FC_{i,t} = FS_{i,t} \times 100
$$

> **长度归一化**：避免长披露因绝对命中数多而被高估模糊度，也避免极短文本一次命中即满分。

### 3.4 恒等式置信度乘数

金额关系越一致，置信度越高：

$$
I_{i,t} = \max\left(0, 1 - \frac{D^{idt}_{i,t}}{0.20}\right)
$$

其中 $D^{idt}_{i,t}$ 为 2.1 中的相对偏差。

> **金融解释**：$I_{i,t}$ 不是公司激进程度的正向证据，而是数据质量与口径一致性的
> 置信度折扣。金额关系不稳时，先降低风险分置信度，不直接解释为公司更激进。

### 3.5 综合激进程度评分

设三个正向信号权重为 $w_1, w_2, w_3$（默认各 0.25）：

$$
RS_{i,t} = \frac{w_1 \cdot IS_{i,t} + w_2 \cdot CS_{i,t} + w_3 \cdot FC_{i,t}}{w_1 + w_2 + w_3}
$$

若某个分量缺失，则只对已有分量加权平均。

最终风险分：

$$
AS_{i,t} = RS_{i,t} \cdot I_{i,t}
$$

$AS_{i,t}$ 取值范围为 $[0, 100]$，即 `aggressiveness_score`。

---

## 4. 风险排序规则

风险排序不是另训分类器，而是按 `aggressiveness_score` 排序取前 $k$ 名作为重点复核样本：

$$
k = \lceil |\{AS_{i,t} \text{ 非空}\}| \times (1 - \theta) \rceil
$$

其中 $\theta = 0.80$ 为 `anomaly_percentile`。

异常类型按以下规则粗分类（多原因命中时标记为 `multiple`）：

| 异常类型 | 规则 | 说明 |
| --- | --- | --- |
| `industry_outlier` | $P_{i,t} \ge 0.80$ | 行业偏离度高；也是默认兜底类型 |
| `change_spike` | $Z_{i,t} \ge 1.5$ | 资本化率正向跳升异常（仅上升） |
| `fuzziness` | $FS_{i,t} \ge 0.5$ | 资本化条件描述模糊 |
| `identity_error` | $I_{i,t} < 0.5$ | 当前阈值组合下基本不触发 |

> **重要**：$k$ 只在“有风险分”的记录上计算，不是对 150 条全样本取分位数。
> 因此异常占全样本比例可能低于 $1 - \theta$。

---

## 5. 校验阈值

| 检查项 | 阈值 | 说明 |
| --- | --- | --- |
| 研发投入拆分恒等式 | $D^{idt}_{i,t} \le 5\%$ | `validate` 阶段硬门槛，超过则记录失败 |
| 资本化率一致性 | $\|CR_{i,t} - CR^{calc}_{i,t}\| \le 5$ 个百分点 | 披露值与重算值偏差过大则失败 |

---

## 6. 启发式匹配方法

本节把当前代码中“只存在于代码里”的匹配逻辑文档化，
并标注其假设、局限与后续改进方向。

### 6.1 章节定位（route）

`src/route/section_router.py` 基于 `configs/section_rules.yaml` 做关键词匹配。

**当前逻辑**：

1. 对每条规则中的 `keywords`，扫描 Markdown 每一行；
2. 命中后提取上下文切片；
3. 用 `positive_keywords` 加分、`negative_keywords` 减分；
4. 额外奖励 `<table>`、标题层级（`#` 开头）、`附注`；
5. 对“资产负债表”里的“开发支出”做惩罚；
6. 每个规则最多返回 `max_slices` 个切片。

**局限**：

- 严格的子串包含，对 OCR 错字、换行、空格不鲁棒；
- 未利用 Markdown 标题层级做结构定位；
- 未使用真正的模糊字符串距离（如 Levenshtein）。

**后续方向**：

- 引入 `rapidfuzz` 做标题模糊匹配；
- 利用 `#`、`##` 层级做基于结构的定位；
- 对表格区域单独处理，避免把资产负债表中的“开发支出”误当附注。

### 6.2 资本化条件模糊度

`src/analysis/scorer.py` 用会计估计模糊词表统计命中数，并做长度归一化。

**当前逻辑**（与 §3.3 单源一致，详见 §3.3 词表与公式）：

```text
FUZZY_KEYWORDS = {视情况, 根据情况, 管理层判断, 必要时, 综合评估, 谨慎判断, 视具体, 具体情况, 重大判断, 估计}
norm_factor = max(1, len(content) / 200)
fuzziness_score = min(1, hits / norm_factor)
```

**词表设计**：刻意排除「等/相关/合理/未来/预计/预期/可能」等高频正向词（详见 §3.3）。

**局限**：

- 没有处理否定语境；
- 没有限定只在“资本化条件”段落内统计；

**后续方向**：

- 把统计范围限定在资本化条件附近；
- 用 LLM 对句子级语义做模糊度评分；
- 建立“具体条件关键词”白名单（技术可行性、完成意图、经济利益可计量等）。

### 6.3 问询函相关性（v2）

`src/analysis/inquiry_labeler.py` 当前采用“脚本剪枝 + LLM 语义二分类”。

**脚本层剪枝**：

- 只保留 `document_role ∈ {inquiry_notice, attention_letter, regulatory_work_letter, process_other}`；
- 排除 `substantive_reply`、`delay_notice`、`supporting_statement`；
- Tier-1 关键词命中即判相关：

  ```text
  资本化, 开发支出, 研发费用资本化, 研发支出资本化, 研发投入资本化,
  研发资本化, 资本化条件, 资本化政策, 资本化时点, 资本化标准,
  开发支出余额, 开发支出减值, 开发支出转无形资产, 研发无形资产
  ```

- `费用化` 仅在与 `研发 / 研发费用 / 研发支出 / 研发投入 / 资本化` 同现时判相关。

**LLM 层确认**：

- 仅当候选只命中 Tier-2 泛词时触发：

  ```text
  研发, 研发费用, 研发投入, 无形资产
  ```

- LLM 输入：公告标题 + PDF 前 3 页 / 关键词片段；
- LLM 输出 JSON：`is_about_rd_capitalization`, `confidence`, `evidence_snippet`, `aspect`。

**输出字段**：

- `inquiry_received`：是否收到任何监管函件；
- `reply_received`：是否存在回复/延期/专项说明；
- `capitalization_related`：监管函件是否实质针对研发资本化（即问询闭环可行性测试的 $Y$ 标签）；
- `inquiry_actually_received`：与 `capitalization_related` 同义，保留兼容。

---

## 7. 表格提取与 LLM fallback

`src/extract/rd_table_extractor.py` 从 MinerU 输出的 Markdown HTML 表格中
确定性提取研发相关数值，作为 LLM 抽取的 fallback 与校验依据。

### 7.1 提取范围

| 表格类型 | 提取字段 | 用途 |
| --- | --- | --- |
| 研发投入情况表 | `expensed_amount`, `capitalized_amount`, `total_amount`, `capitalization_rate` | 计算资本化率、校验拆分 |
| 开发支出明细表 | `opening_balance`, `internal_development`, `current_additions`, `recognized_intangible`, `transferred_to_expense`, `closing_balance` | 校验开发支出变动 |
| 无形资产附注 | `internal_development`, `development_expenditure_category` | 交叉校验资本化转出 |

### 7.2 单位归一化

表格原始单位可能是元、万元或百万元。提取器统一归一化为 **万元**：

$$
\text{万元} =
\begin{cases}
\text{元} / 10000 \\
\text{万元} \\
\text{百万元} \times 100
\end{cases}
$$

### 7.3 LLM fallback

`src/validate/validator.py` 支持在 LLM 抽取字段缺失时读取
`data/extracted/tables/tables.jsonl` 中的对应值回填，并在 `data_quality_notes`
中标记 `table_fallback`。回填字段映射见 `TABLE_FALLBACK_MAP`。

> **当前默认关闭**：`configs/model_config.yaml` 中 `table_extraction.fallback_to_tables: false`。
> 表格提取器先作为独立工具运行，输出结构化表格供人工/后续校验；
> 待小样本验证表格值与 LLM 值的一致性后，再开启自动回填。

---

## 8. 启发式参数与待审计项

| 参数 | 当前值 | 代码位置 | 状态 |
| --- | --- | --- | --- |
| `anomaly_percentile` | 0.80 | `configs/model_config.yaml` / `src/analysis/detector.py` | 待复核：是否应做敏感性分析 |
| `industry_weight` | 0.25 | `configs/model_config.yaml` / `src/analysis/scorer.py` | 待复核：权重设定缺乏实证 |
| `change_weight` | 0.25 | `configs/model_config.yaml` / `src/analysis/scorer.py` | 待复核 |
| `fuzziness_weight` | 0.25 | `configs/model_config.yaml` / `src/analysis/scorer.py` | 待复核 |
| `identity_multiplier` | 0.25 | `configs/model_config.yaml` | 文档化：表示 20% 偏差时乘数为 0 |
| `change_zscore` 阈值 | 1.5 | `src/analysis/detector.py` | 待复核 |
| `fuzziness_score` 阈值 | 0.5 | `src/analysis/detector.py` | 待复核 |
| `identity_check_score` 阈值 | 0.5 | `src/analysis/detector.py` | 待复核 |
| `change_score` 缩放因子 | 2 | `src/analysis/scorer.py` | 待复核：任意缩放 |
| `fuzziness_score` 归一化 | `max(1, len(content)/200)` | `src/analysis/scorer.py` | 每 200 字符预期 1 个模糊词命中 |
| 行业归属来源 | 显式 `industry` 字段优先，顺序推断仅 fallback | `src/analysis/scorer.py` | 已落地显式配置；fallback 顺序推断待移除 |
| 章节定位 | 关键词包含 + 打分 | `src/route/section_router.py` | 待改进：引入模糊匹配 |
| 问询 LLM 页数 | 3 | `src/analysis/inquiry_labeler.py` | 待复核 |

---

## 参考

- 企业会计准则第 6 号——无形资产（CAS 6）
- `src/model/schemas.py`：字段 Schema 定义
- `src/analysis/scorer.py`：评分实现
- `src/analysis/detector.py`：风险排序实现
- `src/route/section_router.py`：章节定位实现
- `src/analysis/inquiry_labeler.py`：问询标签实现
- `src/extract/rd_table_extractor.py`：表格提取实现
