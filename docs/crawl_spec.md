# 抓取规格（Crawl Specification）

## 项目信息

- **项目名称**：研发资本化风险排序与问询函可行性测试
- **数据来源**：巨潮资讯网（cninfo.com.cn）公开公告
- **数据类型**：上市公司年度报告（PDF）+ 问询验证候选公告
- **难度档位**：挑战档 1.1x

---

## 1. 股票池与行业范围

### 1.1 行业选择依据

研发资本化行为在不同行业间差异显著。研发密集型行业（医药制造、电子设备、软件信息）具有以下特征，使其成为本项目的理想研究对象：

- **研发支出规模大**：年报中研发投入占比高，资本化决策具有显著的经济影响
- **资本化率差异大**：同行业公司间资本化策略存在显著差异，便于识别异常值
- **问询函案例丰富**：研发密集型公司更易因资本化问题收到交易所问询函

### 1.2 股票池与示例公告

| 行业 | 公司数量 | 示例公司 | 选择依据 |
|------|----------|----------|----------|
| 医药制造 | 20 家 | 恒瑞医药(600276)、迈瑞医疗(300760) | 研发支出占比高，资本化率差异大 |
| 电子设备 | 20 家 | 中芯国际(688981)、京东方A(000725) | 技术迭代快，研发投入大 |
| 软件信息 | 10 家 | 金山办公(688111)、科大讯飞(002230) | 无形资产占比高，资本化策略多样 |
| **合计** | **50 家** | — | — |

完整股票池见 [`configs/crawl.yaml`](../configs/crawl.yaml)。

**示例公告（真实可溯源）**：

以下示例来自巨潮资讯网公开数据，展示 `announcementId` 与 `pdf_url` 的完整格式。实际爬取时通过 API 批量获取。

| 公司 | 股票代码 | 年报年份 | announcementId | 巨潮详情页 URL | PDF 下载 URL |
|------|----------|----------|----------------|----------------|--------------|
| 恒瑞医药 | 600276 | 2023 | `1217095082` | `http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1217095082` | `http://static.cninfo.com.cn/finalpage/2024-04-18/1217095082.PDF` |
| 迈瑞医疗 | 300760 | 2023 | `1217810263` | `http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300760&announcementId=1217810263` | `http://static.cninfo.com.cn/finalpage/2024-04-20/1217810263.PDF` |
| 金山办公 | 688111 | 2023 | `1216932748` | `http://www.cninfo.com.cn/new/disclosure/detail?stockCode=688111&announcementId=1216932748` | `http://static.cninfo.com.cn/finalpage/2024-04-10/1216932748.PDF` |

> **数据溯源说明**：以上 `announcementId` 和 `pdf_url` 均来自巨潮资讯网公开 API 返回的真实字段。`announcementId` 是巨潮系统内公告的唯一标识，通过 `http://www.cninfo.com.cn/new/hisAnnouncement/query` 接口获取。PDF 文件托管在 `static.cninfo.com.cn`，路径格式为 `finalpage/{发布日期}/{announcementId}.PDF`。

### 1.3 股票池筛选标准

- 属于申万一级行业分类中的"医药生物"、"电子"、"计算机"
- 市值排名前 50%（确保数据披露质量较高）
- 排除 ST/*ST 公司（避免异常财务状态干扰）

---

## 2. 时间范围

| 维度 | 范围 |
|------|------|
| 年报年份 | 2021、2022、2023 |
| 发布时间 | 2022-04-01 至 2024-06-30（年报通常在次年 4 月前披露） |
| 问询函查询窗口 | 年报发布日期后 180 天 |

选择 2021–2023 年的原因：
- 覆盖完整的"疫情后恢复期"，财务数据具有分析价值
- 巨潮资讯网 PDF 下载链路稳定，无访问限制
- 三年数据可计算"跨期变化"（Z 分数），是评分模型的关键维度

---

## 3. 公告关键词

### 3.1 主公告（年报）

- **公告标题关键词**：`"年度报告"`、`"年报"`
- **排除关键词**：`"摘要"`、`"修订"`、`"更正"`、`"补充"`
- **公告类型 API 编码**：`category_ndbg_szsh`（深交所/上交所/北交所年度报告）

### 3.2 辅助公告（问询函）

- **公告标题关键词**：`"年报问询函"`、`"问询函"`、`"问询函回复"`、`"关注函"`、`"监管工作函"`
- **内容关键词**：`"研发"`、`"资本化"`、`"开发支出"`、`"无形资产"`、`"费用化"`
- **查询方案**：官方 API 的问询函接口当前无套餐权限；问询候选走巨潮前端公开查询接口 `hisAnnouncement/query`。
- **当前实现**：`--stage inquiry` 读取年报 `metadata.csv`，按年报发布日期后 180 天查询候选公告，输出 `data/inquiry/inquiry_candidates.csv`，逐条写入 `data/inquiry/inquiry_discovery_cache.json`；候选 PDF 下载拆到 `--stage inquiry-download`。
- **查询参数**：当前实现不向 `hisAnnouncement/query` 发送裸股票代码，使用 `stock=""` + `searchkey=公司名` 查询，并用返回字段 `secCode` 二次校验，避免裸代码返回空结果。
- **命名与校验**：问询候选 `doc_id` 使用 `{stock_code}_{stock_name}_{report_year}_{publish_date}_{document_role}_{announcement_id}`；`inquiry-download` 下载后尝试抽取 PDF 首页标题，写回 `pdf_title`、`pdf_title_status` 和 `title_match_status`。
- **分类码状态**：`category_dshgszz` 仅为历史候选配置，尚未通过小样本校准，不作为当前已验证事实。当前实现不依赖该分类码，先以公司、日期窗口和标题关键词过滤候选。

---

## 4. 公告类型

| 公告类型 | API 编码 | 用途 | 预计数量 |
|----------|----------|------|----------|
| 年度报告 | `category_ndbg_szsh` | 主数据：抽取研发资本化字段 | 150 份（50 家 × 3 年） |
| 年报问询函 | 前端公开查询接口，分类码待校准 | 扩展方案：可行性测试风险排序结果 | 由 discovery 决定 |
| 问询函回复 | 前端公开查询接口，分类码待校准；标题含"回复" | 扩展方案：评估回复充分性 | 由 discovery 决定 |
| 关注函、监管工作函 | 前端公开查询接口，分类码待校准 | 问询样本不足时的扩展验证材料 | 由 discovery 决定 |

---

## 5. 数据量目标

### 5.1 课程最低要求

| 指标 | 基础档 | 挑战档 |
|------|--------|--------|
| 年报 PDF | ≥ 50 份 | ≥ 150 份 |
| 核心字段 | ≥ 10 个 | ≥ 10 个 |
| 人工校验样本 | ≥ 10 条 | ≥ 30 条 |

### 5.2 本项目目标

| 指标 | 目标 | 计算依据 |
|------|------|----------|
| 年报 PDF | 150 份 | 50 家公司 × 3 年 |
| 核心字段 | 14 个 | 见 `src/model/schemas.py` |
| 问询候选发现 | 覆盖 150 个 company-year | 先不预设命中数量，只记录候选数量和候选 metadata；候选 PDF 下载由 `inquiry-download` 独立执行，有效标签数量由后续 label 阶段确定 |
| 人工校验样本 | ≥ 30 条 | 随机抽样 + 异常样本优先 |

---

## 6. 多公告匹配

### 6.1 年报 ↔ 问询函配对逻辑

本项目需要实现**年报与问询函的跨公告匹配**：

```
候选发现条件：
1. 同一 stock_code
2. 问询函、回复函、关注函或监管工作函发布日期在年报发布日期后 180 天内
3. 标题命中问询类关键词

内容标签条件：
1. 解析候选 PDF 或公告正文
2. 正文包含研发、资本化、开发支出、无形资产或费用化相关问询
3. 将每个 company-year 标记为有相关问询或无相关问询；无候选也必须保留记录
```

### 6.2 匹配用途

- 如果模型标记某公司为异常，且该公司在相近时间收到问询函 → **TP（True Positive）**
- 如果模型标记异常但无问询函 → **FP（False Positive）**
- 如果模型未标记异常但存在相关问询 → **FN（False Negative）**
- 如果模型未标记异常且无相关问询 → **TN（True Negative）**
- 样本充足时构建混淆矩阵，计算 Precision / Recall / F1；样本不足时输出 Top-K 命中率、候选覆盖率和典型案例分析

---

## 7. 限速策略

### 7.1 请求频率

| 接口 | 请求间隔 | 并发数 | 说明 |
|------|----------|--------|------|
| 巨潮公告查询 API | 3 秒 | 1 | 单线程顺序请求，避免触发限流 |
| PDF 下载 | 3 秒 | 1 | 单线程顺序下载，保护巨潮服务器 |
| MinerU 解析 | 无限制（本地）| 根据机器配置 | 本地 CLI 调用，不受网络限速影响 |

### 7.2 失败处理

| 失败类型 | 行为 | 记录方式 |
|----------|------|----------|
| API 返回非 200 | 指数退避重试（1s → 2s → 4s），最多 3 次 | metadata.csv `error_message` |
| PDF 下载超时 | 重试 3 次后标记为 failed | metadata.csv `download_status` |
| PDF 文件损坏（非 PDF 头）| 跳过，标记为 failed | metadata.csv `error_message` |
| hash 碰撞 | 保留第一个文件，后续标记为 collision | audit 报告 + metadata.csv `notes` |

### 7.3 断点续传

- crawl 阶段：已查询的公司-年度组合写入 `data/crawl_cache.json`，重跑自动跳过
- download 阶段：已存在且校验通过的 PDF 自动跳过
- inquiry discovery 阶段：每处理完一条年报 metadata，就追加候选、写入 `outputs/logs/inquiry_log.jsonl` 并更新 `data/inquiry/inquiry_discovery_cache.json`；`--force` 可重建候选 CSV 和 cache
- inquiry-download 阶段：读取 `data/inquiry/inquiry_candidates.csv`，已存在且校验通过的候选 PDF 自动跳过，失败或缺失项可重跑补下载
- parse 阶段：已解析的 PDF 自动跳过

---

## 8. Metadata 字段定义

`data/metadata/metadata.csv` 必须包含以下字段：

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `doc_id` | str | 文档唯一标识：`{stock_code}_{publish_date}_{hash(title, 8)}` | 生成 |
| `stock_code` | str | 股票代码（如 600276） | crawl |
| `stock_name` | str | 公司名称（如 恒瑞医药） | crawl |
| `market` | str | 市场（sz/sh/bj） | crawl |
| `announcement_title` | str | 公告标题 | crawl |
| `announcement_type` | str | 公告类型编码 | crawl |
| `publish_date` | str | 发布日期（YYYY-MM-DD） | crawl |
| `url` | str | 公告详情页 URL | crawl |
| `pdf_url` | str | PDF 下载 URL | crawl |
| `local_pdf_path` | str | 本地 PDF 保存路径 | download |
| `download_status` | str | `success` / `failed` / `skipped` | download |
| `source` | str | 固定值 `cninfo` | 固定 |
| `crawl_time` | str | 抓取时间 ISO 格式 | crawl |
| `error_message` | str | 失败原因，成功时留空 | crawl / download |
| `notes` | str | 备注（如 hash 碰撞、内容异常等） | audit |

`data/inquiry/inquiry_candidates.csv` 在通用 metadata 字段之外增加以下字段：

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `document_role` | str | 候选角色：收到问询、正式回复、延期公告、专项说明、关注函或监管工作函 | inquiry |
| `pdf_title` | str | PDF 首页抽取到的大标题；无文字层时留空 | inquiry-download |
| `pdf_title_status` | str | `ok` / `empty` / `missing` / `error` | inquiry-download |
| `title_match_status` | str | `match` / `mismatch` / `unknown`，只做轻量一致性校验 | inquiry-download |

---

## 9. 数据溯源要求

- 所有原始 PDF 文件**不得修改**，保留原始文件名和 hash
- metadata.csv 是后续所有步骤的主键，必须非空
- `source` 统一填 `cninfo`，确保可追溯
- 下载日志 `data/download_log.jsonl` 保留完整下载历史

---

## 10. 配置映射

本规格文件与代码配置的对应关系：

| 规格条目 | 代码配置 | 文件 |
|----------|----------|------|
| 股票池 | `companies` | `configs/crawl.yaml` |
| 时间范围 | `years` | `configs/crawl.yaml` |
| API 参数 | `cninfo.*` | `configs/crawl.yaml` |
| 限速参数 | `download.delay_seconds` | `configs/crawl.yaml` |
| 问询函关键词 | `inquiry_keywords` | `configs/crawl.yaml` |
| 问询分类码 | 前端接口小样本校准结果 | 当前不把 `category_dshgszz` 视为已验证分类码 |
| 阶段依赖 | `stages` | `configs/workflow.yaml` |

---

> 本抓取规格遵循老师讲义 Week 12 要求（详见 `../00-课程讲义/Week12-巨潮数据抓取/讲义.md` §4.3）。
