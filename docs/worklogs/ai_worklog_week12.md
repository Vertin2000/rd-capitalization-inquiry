# AI Worklog Week 12

## 使用的工具

Claude Code

## 本周让 AI 帮助的任务

- [x] 巨潮 API 封装与测试
- [x] 年报元数据抓取（50 家 × 3 年）
- [x] PDF 下载模块开发
- [x] `crawl_spec.md` 完善（补充真实 announcementId 示例）
- [x] 数据质量审计模块开发

## 我给 AI 的上下文

- 巨潮资讯网 API 响应格式（`hisAnnouncement/query`）
- `configs/crawl.yaml` 配置（50 家公司 + 3 年）
- 老师反馈（5 条）

## AI 生成或修改的文件

| 文件 | 修改内容 | 原因 |
|------|----------|------|
| `src/main.py` | 添加 `--limit` 参数传递至 crawl/download | 支持 mini pipeline 快速验证 |
| `src/crawl/cninfo_api.py` | `__init__` 和 `run()` 增加 `limit` 参数；`_crawl_year()` 接收 companies 参数 | 同上 |
| `src/download/downloader.py` | `__init__` 和 `run()` 增加 `limit` 参数 | 同上 |
| `docs/crawl_spec.md` | §1.2 增加"示例公告（真实可溯源）"表格，含 announcementId 和 pdf_url | 老师反馈#1 |
| `docs/topic_proposal.md` | **新建**：明确研究问题与数据范围的一致性 | 老师反馈#2 |
| `src/model/schemas.py` | 添加资本化率口径优先级注释（3 级 fallback） | 老师反馈#3 |
| `docs/output_sample.md` | 新增"资本化率口径优先级"表格和禁止行为清单 | 老师反馈#3 |

## 我实际运行的命令

### 1. CLI 入口验证

```powershell
uv run python src/main.py --help
```

**输出**：

```
usage: main.py [-h]
               [--stage {crawl,download,audit,parse,route,extract,validate,score,detect,inquiry,analyze,report,all}]
               [--from-stage {crawl,download,audit,parse,route,extract,validate,score,detect,inquiry,analyze,report}]
               [--to-stage {crawl,download,audit,parse,route,extract,validate,score,detect,inquiry,analyze,report}]
               [--limit LIMIT] [--inquiry-loop] [--config CONFIG]

研发资本化异常检测与问询函触发机制分析 Pipeline
```

✅ `--stage` 支持 12 个阶段 + `all`
✅ `--limit` 参数可用于限制样本数（测试用）
✅ `--from-stage` / `--to-stage` 支持 Pipeline 片段运行

### 2. Mini Pipeline 运行（3 份 PDF）

#### Stage 1: crawl（限制 1 家公司 × 3 年 = 3 条记录）

```powershell
uv run python src/main.py --stage crawl --limit 1
```

**输出**：

```
2026-06-09 23:40:45 [INFO] 开始爬取巨潮资讯网年报数据: 公司=50, 年份=[2021, 2022, 2023]
2026-06-09 23:40:45 [INFO] 限制模式: 仅处理前 1 家公司
2026-06-09 23:40:45 [INFO] 搜索 2021年: 600276 - 恒瑞医药
2026-06-09 23:40:49 [INFO] 2021年: 获取 1 条记录
2026-06-09 23:40:49 [INFO] 搜索 2022年: 600276 - 恒瑞医药
2026-06-09 23:40:52 [INFO] 2022年: 获取 1 条记录
2026-06-09 23:40:52 [INFO] 搜索 2023年: 600276 - 恒瑞医药
2026-06-09 23:40:55 [INFO] 2023年: 获取 1 条记录
✅ crawl 完成: data\metadata\metadata.csv
```

**metadata.csv 内容验证**（前 3 行）：

| doc_id | stock_code | stock_name | announcementId | pdf_url | download_status |
|--------|-----------|-----------|----------------|---------|----------------|
| 600276_2022-04-23_9d762a3d | 600276 | 恒瑞医药 | 1213053754 | `http://static.cninfo.com.cn/finalpage/2022-04-23/1213053755.PDF` | success |
| 600276_2023-04-22_79eb2720 | 600276 | 恒瑞医药 | 1216518769 | `http://static.cninfo.com.cn/finalpage/2023-04-22/1216518776.PDF` | success |
| 600276_2024-04-18_752e9011 | 600276 | 恒瑞医药 | 1219650094 | `http://static.cninfo.com.cn/finalpage/2024-04-18/1219650115.PDF` | success |

✅ **数据可溯源**：每条记录包含 announcementId 和完整 pdf_url

#### Stage 2: download（限制 3 条记录）

```powershell
uv run python src/main.py --stage download --limit 3
```

**输出**：

```
2026-06-09 23:41:19 [INFO] 限制模式: 仅下载前 3 条记录
2026-06-09 23:41:19 [INFO] 开始下载 3 份 PDF...
2026-06-09 23:41:42 [INFO] 下载完成: success=3, failed=0, skipped=0, collision=0
✅ download 完成: {'success': 3, 'failed': 0, 'skipped': 0, 'collision': 0}
```

**下载文件验证**：

| 文件名 | 大小 |
|--------|------|
| `600276_2022-04-23_9d762a3d.pdf` | 4,692,408 bytes |
| `600276_2023-04-22_79eb2720.pdf` | 5,089,679 bytes |
| `600276_2024-04-18_752e9011.pdf` | 6,014,937 bytes |

✅ 所有 PDF 文件均大于 100KB 且 `%PDF` 头校验通过

#### Stage 3: audit

```powershell
uv run python src/main.py --stage audit
```

**输出**：

```
2026-06-09 23:41:58 [INFO] 开始数据质量审计...
2026-06-09 23:41:58 [INFO] 审计报告已生成: outputs\dataset_check_report.md
2026-06-09 23:41:58 [INFO] 审计完成: total=3, pdf_exists=3, passed=True
✅ audit 完成: 通过
```

**审计报告摘要**：

| 检查项 | 状态 |
|--------|------|
| metadata_non_empty | ✅ PASS |
| no_duplicate_doc_id | ✅ PASS |
| pdf_exists | ✅ PASS |
| pdf_integrity | ✅ PASS |
| title_keywords | ✅ PASS |
| download_status | ✅ PASS |
| error_message | ✅ PASS |

✅ **全部检查通过**

### 3. 完整 Pipeline 片段（crawl → download → audit）

```powershell
uv run python src/main.py --from-stage crawl --to-stage audit --limit 1
```

✅ 从 crawl 到 audit 的 Pipeline 片段可一键运行

## 报错与修复

| 问题 | 原因 | 修复方式 |
|------|------|----------|
| `--limit` 参数在 `main.py` 中被解析但未传递给 `run_crawl()` / `run_download()` | `main.py` 中 `run_stage()` 不接收 limit | 修改 `main.py`：`run_stage(limit)` → `dispatch[stage](limit=limit)` |
| `CninfoCrawler` 不支持 `limit` 参数 | `__init__` 和 `run()` 未定义 limit | 修改 `cninfo_api.py`：添加 `self.limit`，在 `run()` 中截断 companies 列表 |
| `PDFDownloader` 不支持 `limit` 参数 | 同上 | 修改 `downloader.py`：添加 `self.limit`，在 `run()` 中截断 records 列表 |

## 我人工检查了什么

1. **metadata.csv 字段完整性**：确认 15 个字段全部存在（doc_id, stock_code, stock_name, market, announcement_title, announcement_type, publish_date, url, pdf_url, local_pdf_path, download_status, source, crawl_time, error_message, notes）
2. **announcementId 可追溯性**：确认 `url` 字段包含 `announcementId=...`，`pdf_url` 为 `static.cninfo.com.cn` 的真实下载链接
3. **PDF 文件完整性**：用二进制查看器确认 `%PDF` 头存在，文件大小合理（4.6MB–6MB）
4. **doc_id 唯一性**：3 条记录 doc_id 各不相同（日期 + hash 区分）
5. **标题关键词**：均包含"年度报告"

## 我理解的关键代码

### `cninfo_api.py` 的核心逻辑

- `_infer_market(code)`：通过代码前缀判断市场（60/688→sh, 00/30→sz, 8/4→bj）
- `_search_company_year()`：POST `hisAnnouncement/query`，按 `searchkey`（公司名）+ `category_ndbg_szsh` 查询年报
- `_select_best_record()`：对同一公司-年份的多条结果按标题匹配度打分，选最高分
- 断点续传：`crawl_cache.json` 存储已查询的 `code_year` 组合，重跑自动跳过

### `downloader.py` 的核心逻辑

- `_download_pdf()`：带重试的 HTTP 下载，校验 `%PDF` 头和最小 100KB
- `_check_integrity()`：SHA256 校验，hash 碰撞检测
- 回写 metadata：下载完成后更新 `download_status` 和 `error_message`

### `auditor.py` 的核心逻辑

- 6 项检查：metadata 非空、无重复 doc_id、PDF 存在性、PDF 完整性、标题关键词、download_status 一致性
- 输出 Markdown 报告：`outputs/dataset_check_report.md`

## 下一步计划

1. **完整 crawl**：移除 `--limit`，运行全部 50 家 × 3 年 = 150 条记录
2. **完整 download**：下载 150 份 PDF（预计耗时 ~8 分钟，含 3 秒间隔）
3. **Week 13**：MinerU 解析 + 章节定位 + LLM 字段抽取

## 后续整理（2026-06-13）

- 根目录 `巨潮json/` 已归档到 `project2/data/cninfo-api-archive/`，目录结构为：
  - `mine/`：自己抓取的 `cninfo_api_doc_tree.json`、`cninfo_api_gateway_codes.json` 与三个探索脚本；
  - `friend/`：朋友抓取的完整 `_doc` 版本（含 RAR / PDF / HTML）。
- 三个探索脚本里的硬编码路径已改为相对路径，可直接运行。
- `data/cninfo-api-archive/` 已加入 `.gitignore`。
- 生产脚本仍使用 `project2/` 根目录的 `cninfo_api_doc_tree.json` 与 `cninfo_api_gateway_codes.json`。
