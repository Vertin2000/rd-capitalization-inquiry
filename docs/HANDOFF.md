# 工作交接文档

> 生成时间：2026-06-14
> 最近更新：2026-06-20
> 分支：`experiment/cninfo-official-api`
> 交接人：Claude ↔ 项目团队

---

## 一、当前完成度总览

 | 模块 | 状态 | 关键文件 | 备注 |
 | ------ | ------ | ---------- | ------ |
 | crawl（巨潮 API 爬取） | ✅ 完整验证通过 | `src/crawl/cninfo_api.py`, `src/crawl/cninfo_official_api.py` | official API 路线 150/150，前端 AJAX 路线保留为备选 |
 | download（PDF 下载） | ✅ 完整验证通过 | `src/download/downloader.py` | 150/150，collision=0 |
 | audit（数据质量审计） | ✅ 完整验证通过 | `src/audit/auditor.py` | 150 个唯一 SHA256，质量检查通过 |
 | parse / route / extract / validate | ✅ 全量主线已跑通 | `src/parse/`, `src/route/`, `src/extract/`, `src/validate/` | parse 150/150；extract 产出 150 条；validate 150/150 passed |
 | score / detect / analyze / report | ✅ 下游闭环已接入 | `src/analysis/` 等 | score 83 scored / 67 no-score；detect 17 anomalies；analyze TP=0 / FP=17 / TN=132 / FN=1；report 已生成 |
 | inquiry | ✅ 候选、下载、弱标签收口 | `src/crawl/inquiry_crawler.py`, `src/analysis/inquiry_labeler.py`, `src/main.py` | 固定当前 28 条候选，PDF 28/28 下载成功，orphan=0；`inquiry-label` 输出 150 条 company-year 标签，1 条 related |
 | CLI 调度 | ✅ 代码完成 | `src/main.py` | 支持 `--stage` 独立运行 |
 | 文档 | ✅ 已更新 | `docs/architecture.md`, `docs/crawl_spec.md`, `docs/topic_proposal.md`, `docs/mineru_setup.md` | 架构、规格、选题方案、MinerU GPU 配置均已记录 |
 | 测试 | ✅ 合并后通过 | `tests/` | `uv run pytest tests -q`：exit 0 |

**白话总结**：Week 12 要求的 crawl → download → audit 已在 official API 路线完整跑通：150 条 metadata、150 份 PDF、collision=0，audit 通过。Week 13 的 parse 阶段已从本地 MinerU 长跑切到 MinerU 精准 API batch：最终 150 份年报 Markdown 全部生成，275 个 page segment 全部 success。2026-06-15 按全量 extract 结果重跑后段，2026-06-20 又做 P1 方法论修复（fuzziness 词表去毒、change_zscore 改正向、industry 显式化）并重跑：`uv run python src/main.py --from-stage validate --to-stage report` 成功，输出 validate 150/150、score 83/150 可评分（67 no-score）、detect 17 条异常、inquiry-label 1 条相关问询弱标签、analyze 矩阵 TP=0 / FP=17 / TN=132 / FN=1、`outputs/final_report_auto.md` 自动版（单源真值见 §12.10）；根级 `final_report.md` 为手写答辩版。

---

## 二、已交付代码说明

### 2.1 `src/crawl/cninfo_api.py` / `src/crawl/cninfo_official_api.py`

- `cninfo_api.py` 保留公开前端 AJAX crawler，作为问询函和备选年报抓取路线
- `cninfo_official_api.py` 实现官方 API crawler，支持 OAuth2 token 刷新和 `p_info3015` 年报查询
- 市场推断：`60/688` → sh，`00/30` → sz，`8/4` → bj
- 年报搜索使用 `searchkey=公司名称` + `seDate=次年全年`
- 候选评分：标题含公司名称（1 分）→ 完全匹配 `{year}年年度报告`（3 分）
- 自动过滤摘要、修订、更正
- `announcementTime` 同时支持毫秒时间戳和字符串
- official API 路线 `doc_id`：`{stock_code}_{stock_name}_{report_year}年报`；前端 AJAX 旧路线仍可使用 `{stock_code}_{publish_date}_{title_hash[:8]}`

### 2.2 `src/download/downloader.py`

- 域名白名单：`static.cninfo.com.cn`, `www.cninfo.com.cn`
- PDF 魔数 + 最小 100KB + SHA256 校验
- Hash 碰撞检测：如果不同 doc_id 对应相同 SHA256，在 `notes` 字段标注
- 回写 `metadata.csv` 的 `download_status` 和 `error_message`

### 2.3 `src/audit/auditor.py`

检查 7 项：
1. metadata.csv 非空
2. 无重复 doc_id
3. PDF 文件存在
4. PDF 完整性（魔数 + 大小）
5. 标题含关键词（"年报"/"年度报告"）
6. download_status / error_message 一致性
7. PDF SHA256 唯一性（直接检测 hash 碰撞）

输出：`outputs/dataset_check_report.md`

### 2.4 `src/main.py`

- 已修复 `ModuleNotFoundError: No module named 'src'`（`sys.path.insert`）
- 14 个阶段已注册，`crawl/download/audit/parse/route/extract/validate/score/detect/inquiry/inquiry-download/inquiry-label/analyze/report` 均已接入 CLI
- 支持 `--stage`、`--from-stage`/`--to-stage`、`--inquiry-loop`
- `--limit` 参数**已实际传递**给 `crawl` 和 `download` 阶段（`cninfo_api.py` / `downloader.py` 均支持），用于 mini pipeline 快速验证

---

## 三、已知问题与注意事项

### 3.1 official API 与 parse 完整数据验证已跑通

- **已完成**：official API 路线完整验证
  ```powershell
  uv run python src/main.py --stage crawl --crawl-backend official
  uv run python src/main.py --stage download
  uv run python src/main.py --stage audit
  ```
  结果：metadata.csv 150 条记录，150 份 PDF 全部下载成功，collision=0，audit 通过。
- **已完成**：inquiry 下载层收口
  - `data/inquiry/inquiry_candidates.csv`：28 条候选、28 个唯一 `doc_id`、28 个唯一 PDF 路径
  - `data/inquiry/pdf/*.pdf`：28 个 PDF，全部由当前候选表引用
  - `outputs/reports/inquiry_orphan_pdf_report.md`：referenced=28、pdf_files=28、orphans=0
  - `title_match_status`：22 个 match、6 个 unknown（无文字层或空标题），0 个 mismatch
  - `.tmp/` 与 `outputs/reports/inquiry_broad_audit_*` / `inquiry_label_audit.*` 属于探索性 scratch，不作为正式数据契约
- **已完成**：完整 150 份 parse 验证
  ```powershell
  uv run python src/main.py --stage parse --parse-backend api-batch
  ```
  结果：150 份年报全部解析为非空 Markdown，275 个 page segment 全部 success，失败 0。

### 3.2 Hash 碰撞历史教训

此前早期爬虫出现 131 份 PDF 只有 6 个唯一 hash 的问题，原因是：
- 错误使用 `stock=f"{code},"`（API 会忽略该参数，返回市场-wide 第一条）
- 错误使用 `searchkey=002230`（API 会模糊匹配到其他公司）
- 未校验 `announcementTime` 类型（有时是毫秒时间戳）

当前 official API 路线已验证 `collision=0`；后续如果切回前端 AJAX 路线，仍需重复检查 `download_log.jsonl` 和 audit 报告。

### 3.3 Auditor 已加入 SHA256 唯一性检查

`DataAuditor` 已增加 `pdf_hash_unique` 检查项，会遍历成功下载的 PDF 计算 SHA256；若不同 doc_id 对应同一 hash，会标记为 FAIL。

### 3.4 讲义要求对齐检查

Week 12 最低要求：
- [x] metadata.csv ≥ 50 条（official API 路线已生成 150 条）
- [x] 字段完整 15 列（metadata 输出已验证）
- [x] PDF 与 metadata 一一对应（下载器已验证 150/150）
- [x] audit 报告 ≥ 5 项检查（含 SHA256 唯一性检查）
- [x] 限速策略文档化（`crawl_spec.md` 已写）

### 3.5 MinerU 环境 — 旧 `.mineru` 环境依赖组合错误（历史记录）

> **状态**：旧 `C:\Users\Vertin2000\.mineru` 环境已废弃。当前可用方案是用户级 `uv tool` 安装 MinerU，并通过项目内 `MinerUParser` 调用 CLI。

**旧环境**：`.mineru` venv（Python 3.12.13，uv 管理），`torch==2.4.0+cu121`，`mineru==3.2.3`

**错误**：`OSError: [WinError 126] 找不到指定的模块。Error loading "...torch\lib\fbgemm.dll"`

**诊断过程**：

 | 步骤 | 结果 |
 | --- | --- |
 | 检查 `.mineru` venv 完整性 | ✅ venv 存在，torch/mineru 已安装 |
 | 检查 PATH | ❌ `.mineru\Scripts` 不在用户 PATH（需后续配置） |
 | 检查 fbgemm.dll 文件 | ✅ 文件存在（4.9MB），x64 架构正确 |
 | 检查 libiomp5md.dll | ✅ 存在且可单独加载 |
 | 检查 VC++ Redistributable | ✅ 已安装 2022 x64（14.44.35211） |
 | 检查 CUDA DLL | ✅ cublas/cudnn/cudart 等全部可加载 |
 | 检查 api-ms-win-crt-* | ✅ 全部在 `System32\downlevel` |
 | 用 pefile 解析 fbgemm.dll 导入表 | `libomp140.x86_64.dll` 标记为 MISSING |
 | 尝试从 libtorch 发行包提取 | ❌ libtorch 中**不包含** `libomp140.x86_64.dll` |
 | 全系统搜索 | ❌ 全系统（含 conda）均未找到 |

**更新判断**：`fbgemm.dll` 缺 DLL 是表层症状；更关键的根因是旧环境被手动降到了 `torch==2.4.0+cu121`，但 `mineru==3.2.3` 的包元数据要求 `torch>=2.6,<3`。继续手补 DLL 不专业，优先重建符合依赖约束的工具环境。

**已尝试未成功的方案**：

1. 临时加 Git MinGW 到 PATH → 无效
2. 安装 VC++ Redistributable 2022 x64 → 无效
3. 下载 libtorch 发行包提取 DLL → libtorch 中无此文件

**建议的下一步**：

- **首选**：执行 `scripts/setup_mineru.ps1`，使用 `uv tool install "mineru[all]" --python 3.12 --torch-backend cu126` 重建用户级工具环境
- **若 uv tool 被 Windows/CUDA 兼容性阻塞**：再考虑 conda 作为外部工具环境
- **不建议**：手动复制未知来源 DLL 到 `torch\lib`

### 3.6 Week 13 讲义 API 取舍

Week13 Lab 第 31 行写到正式项目中使用 MinerU API 将真实巨潮 PDF 转为 Markdown。当前项目已落地两套 backend：

- `local`：本地 MinerU CLI，保留为 fallback。
- `api-batch`：MinerU 精准解析 URL batch backend，已完成 150/150 年报全量解析。

两条路线的稳定输出入口一致：`data/parsed/{doc_id}.md`。API 原始 zip 与解压结果只放在 `data/parsed/mineru_api_raw/{doc_id}/part_*/`，任务断点与审计日志只放在 `data/parsed/mineru_api_tasks.jsonl`，均为 ignored data，不提交 git。

---

## 四、下一步工作清单

### 立刻要做（交接当天）

1. **复核字段缺失样本**
   - 优先看 `data/scored/records.jsonl` 中 `data_quality_notes` 含 `TODO: waiting for extract capitalization_rate` 的记录
   - 回到 `data/sections/` 和年报原文确认是披露缺失、章节定位问题，还是 LLM 抽取漏掉
   - 不要为了凑分数把缺失值强行填 0；只有原文明确为 0 才能写 0

2. **复核问询弱标签**
   - 当前 `inquiry-label` 只读候选标题、PDF 首页标题和前 5 页文本
   - 需要人工抽查 related 和 17 条 anomaly 的交集/错配样本（related 06-15 时为 7 条，06-20 v2 语义标签重跑后为 1 条，见 §12.10）
   - 后续若时间允许，再做问询函全文语义标签

### 近期要做（Week 13 → Week 14）

3. **解析阶段（parse）** ✅ 已收口
   - ~~旧方案~~：conda + `magic-pdf` 1.3.12（已废弃，模型路径错误）
   - **当前主方案**：`uv run python src/main.py --stage parse --parse-backend api-batch`
   - **已验证**：150 份年报 Markdown 全部生成，275 个 page segment 全部 success，失败 0
   - **fallback**：本地 `MinerUParser` 继续保留，适合 API 不可用或小样本复核

4. **章节定位（route）**
   - 校准 `src/route/section_router.py` 与 `configs/section_rules.yaml`
   - 关键词匹配研发相关章节（财务报表附注、研发投入、开发支出等）
   - 输出 JSONL：`data/sections/{doc_id}_sections.jsonl`

5. **字段抽取（extract）**
   - 准备 LLM API Key（写入 `.env`，不要提交）
   - 实现 `src/extract/llm_extractor.py`
   - Prompt 设计参考待创建的 Prompt 迭代记录，字段定义见 `src/model/schemas.py`

### 中期要做（Week 13-14）

6. 人工校验 ≥ 30 条样本，优先覆盖 17 条异常和问询 related 样本（related 06-15 时为 7 条，06-20 重跑后为 1 条，见 §12.10）
7. 补问询函全文语义标签，替代当前关键词 MVP
8. Prompt / 抽取规则迭代，并记录到 worklog 或待创建的 Prompt 迭代记录中

---

## 五、关键文件速查

 | 目的 | 文件 |
 | ------ | ------ |
 | 了解项目做什么 | `README.md`, `SPEC.md`, `docs/architecture.md` |
 | 了解爬取规则 | `docs/crawl_spec.md`, `configs/crawl.yaml` |
 | 跑 Pipeline | `uv run python src/main.py --stage <stage>` |
 | 看数据质量 | `outputs/dataset_check_report.md` |
 | 字段 Schema | `src/model/schemas.py` |
 | 运行测试 | `uv run pytest` |

---

## 六、环境确认

- Python ≥ 3.10，推荐使用仓库锁定的版本
- 依赖管理用 `uv`：`uv sync`
- 已安装依赖包含 `requests`, `pydantic`, `pytest` 等
- **MinerU 安装状态**（uv tool 方案，已跑通）：
  - 推荐安装：`uv tool install "mineru[all]" --python 3.12 --torch-backend cu126`
  - 版本：`mineru>=3.2.0`（包名从旧版 `magic-pdf` 改为 `mineru`）
  - Windows 下使用 Python 3.12，避开 `ray` 对 Python 3.13 的限制
  - 详见：`docs/mineru_setup.md`
- LLM API Key **已配置**（`.env` 已创建），extract 阶段开始之前确认 Key 有效即可

---

## 七、变更记录

### 2026-06-09

- 完成 crawl/download/audit 三段代码
- 修复 API 参数、hash 碰撞、时间戳解析等历史 bug
- 更新架构/规格文档
- 单元测试 7 项全部通过

### 2026-06-10

- 根据老师 5 条反馈逐项修复
- 补充真实 announcementId 示例（`docs/crawl_spec.md`）
- 新建 `docs/topic_proposal.md` 对齐研究问题与数据范围
- 写死 `schemas.py` 资本化率口径（5 级优先级 + 禁止行为清单）
- 填充 `worklog_week12.md` 实际运行记录
- 跑通 mini pipeline（恒瑞医药 2021–2023，3 份 PDF，audit 全部通过）
- `main.py` 的 `--limit` 参数实际传递给 crawl/download
- **MinerU 重装**：从旧版 `magic-pdf` 1.3.12 迁移到新版 `mineru` 3.2.3
  - 安装方案从 conda 改为 **uv 系统级 venv**（`C:\Users\Vertin2000\.mineru`）
  - PyTorch GPU（cu121）安装成功，但 `fbgemm.dll` 依赖问题待修复
  - `src/parse/mineru_parser.py` 代码已更新（`magic-pdf` → `mineru`）
  - `docs/mineru_setup.md` 待同步为 uv 方案
- 清理根目录旧文件（`crawl_spec.md`, `topic_proposal.md`, `difficulty_declaration.md`）

### 2026-06-10（晚间）

- **MinerU 环境深度诊断**：`import torch` 失败问题排查
  - 已确认根因：`fbgemm.dll` 依赖 `libomp140.x86_64.dll`（LLVM OpenMP 运行时）缺失
  - 已排除：MinGW PATH、VC++ Redistributable、libtorch 发行包提取
  - `api-ms-win-crt-*` 实际存在（在 `System32\downlevel`），pefile 路径检查有误
  - 全系统搜索（含 conda）均未找到 `libomp140.x86_64.dll`
  - 已尝试方案未解决，详见 3.5
- 更新 `docs/HANDOFF.md`：新增 3.5 详细诊断记录、更新环境确认状态
- **MinerU 3.x 解析跑通**：
  - 改用用户级 `uv tool` 安装的 `mineru==3.2.3`，工具 Python 为 3.12
  - 项目绕开 Windows `mineru.exe` launcher，调用 `python.exe -B -m mineru.cli.client`
  - 解析子进程 stdout/stderr 写入 `data/parsed/mineru_logs/`，避免 Windows 管道悬挂
  - 默认 `-b pipeline`，可通过 `MINERU_BACKEND=hybrid-auto-engine` 切换高精度后端
  - `parse --limit 1` 已成功，`tests/test_mineru_parser.py` 覆盖路径发现、日志、超时、后端切换与输出搬运

---

## 八、2026-06-12 官方 API 文档本地化（进行中）

> **状态：进行中（WIP）**。API 文档树、gateway code 索引和参考文档已本地化，但 crawler 代码重构、参数对照校准、mini pipeline 验证仍在继续。本章记录的是已完成的本地化步骤和待验证的下一步，不应被视为最终结论。

### 8.1 交付物

 | 文件 | 位置 | 说明 | git 状态 |
 | --- | --- | --- | --- |
 | 原始 API 文档树 | `cninfo_api_doc_tree.json` | 前端 `bfd.apiDocTree.data` 的完整导出（1.5 MB，2465 个接口） | 已加入 `.gitignore`，不提交 |
 | gateway code 索引 | `cninfo_api_gateway_codes.json` | 全部接口的 name / alias / code / requestPath / 分类路径 | 已加入 `.gitignore`，不提交 |
 | CNINFO API 原始归档 | `data/cninfo-api-archive/` | 自己抓取的 tree/codes/探索脚本（`mine/`）与朋友抓取的完整 `_doc` 版本（`friend/`） | 已加入 `.gitignore`，不提交 |
 | 生成脚本 | `scripts/generate_cninfo_api_docs.py` | 从 tree 生成 catalog + reference | 提交 |
 | 机器可读目录 | `docs/cninfo_official_api_catalog.json` | 全量目录 + 608 条研究相关接口子集；类目含 `display` 可见性标记 | 提交 |
 | 人工参考文档 | `docs/cninfo_official_api_reference.md` | 目录总览、相关接口表、典型接口元数据、Plan A 建议 | 提交 |
 | 全量 Markdown 目录 | `docs/cninfo_official_api_catalog.md` | 2465 个接口按类目层级展开；可见类目在前，隐藏类目在后 | 提交 |

### 8.2 提取方法（可复现）

1. 页面加载的 `/js/apiDocTree.js` 暴露全局对象 `bfd.apiDocTree`，其 `getTree()` 方法会 POST `api-cloud-gateway-manage/apiDoc/apiDocTree` 并缓存到 `sessionStorage`。
2. 在浏览器 Console 中执行：

   ```javascript
   bfd.apiDocTree.getTree().done(t => downloadJSON(t, 'cninfo_api_doc_tree.json'));
   ```

   即可导出完整文档树。
3. `info?gatewayCode=<code>` 中的 `<code>` 对应 tree 叶子节点的 `code` 字段（UUID），不是 `name`（如 `p_public0001`）。
4. 接口元数据端点 `GET /api-cloud-gateway-manage/apiDoc/info?gatewayCode=<code>` **无需登录即可访问**，返回 baseInfo / requestConfig / serviceConfig / resultContent。

### 8.3 关键发现

- **全量规模**：2465 个 API 接口，593 个分类节点，31 个一级类目。
- **研究相关接口**：共 608 个，分布在：
  - 公司数据（274）：财务报表、业绩预告、股本、股东、高管等；
  - 巨潮网使用接口（200）：定期报告披露事件、公开信息事件等；
  - 公告资讯（106）：公告查询、分类、PDF 相关；
  - 证券提示库数据服务（12）：问询函、监管关注等；
  - 新闻研报（9）、公共信息（7）。
- **官方数据接口需要授权**：直接访问数据端点（如 `http://webapi.cninfo.com.cn/api/cninfo/p_cninfo5001`）返回：

  ```json
  {"resultcode": 401, "resultmsg": "未经授权的访问,..."}
  ```

  `resultContent.errorCodeResult` 进一步列出 token 无效 / 过期 / 套餐余额不足 / 试用次数用完等错误码。
- **公开文档可用**：虽然数据不能无授权拉取，但字段、校验规则、输出列名等元数据已完整本地化，可用于校准现有 crawler。

### 8.4 crawler 重构决策

- **采用 Plan A**：数据仍走现有公开前端接口 `www.cninfo.com.cn/new/hisAnnouncement/query`。
- **不采用 Plan B 的官方认证接口**，原因：
  1. 官方数据端点 401，需要有效 token / 套餐授权；
  2. 项目规则明确“不绕过登录、验证码或访问限制”；
  3. 研究所需数据为**已公开的上市公司公告**，公开前端接口已能满足。
- 官方文档的用途：
  1. 核对 `cninfo_api.py` 中参数命名、日期格式、分页方式；
  2. 对照公告类接口的输出字段，验证 metadata.csv 15 列的完整性；
  3. 作为后续字段抽取和风险排序的语义参考。

### 8.5 下一对话继续事项

1. 逐条审查 `src/crawl/cninfo_api.py` 与 `docs/cninfo_official_api_reference.md` 中公告/年报相关接口的参数映射。
2. 如有必要，做一个小规模对照实验：用公开 `hisAnnouncement/query` 拉取几条公告，与官方文档中的输出字段比对。
3. 修正 crawler 参数和异常处理后，跑 mini pipeline（`--limit 1/3`）验证 crawl → download → audit。
4. 验证通过后，再跑完整 150 份数据。

---

## 九、2026-06-13 架构审查与 crawl 双路线实验

### 9.1 审查动因

`docs/architecture.md` 已过度前置：详细写入了 score / detect / inquiry / analyze / report 等尚未跑通阶段的设计、数据契约和评估指标，容易让人误以为项目已经推进到更后面。本次整理按“**没跑通就是没实现**”的标准重新校准文档。

### 9.2 当时完成度（2026-06-13 校准后）

 | 模块 | 状态 | 判定标准 | 关键文件 |
 | ------ | ------ | ---------- | ---------- |
 | crawl（巨潮公告查询） | ✅ 已跑通 | mini pipeline 3/3 通过 | `src/crawl/cninfo_api.py` |
 | download（PDF 下载） | ✅ 已跑通 | mini pipeline 3/3 通过 | `src/download/downloader.py` |
 | audit（数据质量审计） | ✅ 已跑通 | mini pipeline 3/3 通过 | `src/audit/auditor.py` |
 | parse（MinerU PDF → Markdown） | 🔄 进行中 | 当时仅完成小样本验证；最新状态见 §11.10，已 150/150 完成 | `src/parse/mineru_parser.py` |
 | route / extract / validate | ⏸️ 未跑通 | 代码存在但无端到端验证 | `src/route/`, `src/extract/`, `src/validate/` |
 | score / detect / inquiry / analyze / report | ⏸️ 未跑通 | 仅 Schema / 占位 | `src/analysis/`（不存在） |
 | CLI 调度 | ✅ 已跑通 | crawl/download/audit 可 `--stage` 调用 | `src/main.py` |

**白话总结（历史记录）**：截至 2026-06-13，Week 12 三段（crawl → download → audit）已跑通；Week 13 的 parse 仍算“进行中”；其余全部不算实现。最新状态见本文开头总览与 §11.10。

### 9.3 architecture.md 清理内容

- **删除** Section 7 “扩展与闭环（挑战档）”全部：四维度评分模型、问询函配对逻辑、混淆矩阵。
- **删除** 数据流表中 score / detect / inquiry / analyze / report 行。
- **删除** `records.jsonl` 详细数据契约（尚未跑通）。
- **修正** Week 14–16 课程映射为一句话“尚未推进”。
- **修正** 模块职责矩阵：crawl/download/audit → ✅ 已跑通；parse → 🔄 进行中；其余 → ⏸️ 未跑通。

### 9.4 crawl 技术路线对比

 | 维度 | 野路子：前端 AJAX 接口 | 官方 API |
 | ------ | ------------------------ | ---------- |
 | 入口 | `http://www.cninfo.com.cn/new/hisAnnouncement/query` | `http://webapi.cninfo.com.cn/api/...` |
 | 来源 | 巨潮搜索页面 JS 动态调用，非官方文档接口 | 深证信官方 API 文档所列接口 |
 | 认证 | 不需要 | 需要 appKey / token / 套餐授权 |
 | 当前状态 | 已跑通 mini pipeline | 数据端点返回 401，未验证 |
 | 合规性 | 公开访问，不绕过登录 | 需授权，项目规则禁止绕过访问限制 |
 | 风险 | 可能随前端改版失效 | 官方较稳定，但需付费/机构授权 |

### 9.5 分支实验计划

从 `week11-deliverables` 切出两个分支：

```bash
git checkout -b experiment/cninfo-frontend-ajax
git checkout week11-deliverables
git checkout -b experiment/cninfo-official-api
```

 | 分支 | 用途 | 预期动作 |
 | ------ | ------ | ---------- |
 | `experiment/cninfo-frontend-ajax` | 保留并优化当前公开前端接口实现 | 参数调优、限速策略、异常处理、json 解析增强 |
 | `experiment/cninfo-official-api` | 尝试接入官方 API | 配置 token、调用官方公告类接口、映射返回字段到 metadata.csv、验证 mini pipeline |

**决策规则**：
- 若官方 API 在用户提供凭证后可跑通 mini pipeline，且字段/稳定性优于前端接口，则合并到主路线；
- 若官方 API 因授权、配额、字段不全等原因无法稳定使用，则保留前端接口为最终方案，官方 API 文档仅作字段对照参考。

### 9.6 当时的下一步推进顺序（历史记录）

以下是 2026-06-13 当天的推进计划，不是当前待办。最新状态以本文开头总览和 §11.11 为准：parse、route、extract、validate、score、detect、inquiry-label、analyze、report 已接入并重跑。

1. **先跑通 parse**：完整 150 份 PDF MinerU 解析，确认输出稳定。
2. **并行实验 crawl 双路线**：在 `experiment/cninfo-frontend-ajax` 优化当前实现，在 `experiment/cninfo-official-api` 尝试官方 API。
3. **选定最终 crawl 方案**：比较两条分支的 mini pipeline 结果，决定主分支采用哪条路线。
4. **才进入 route / extract / validate**：等 parse 和 crawl 都稳定后再推进。

---

**交接状态**：`architecture.md` 已精简，`HANDOFF.md` 已更新双路线实验计划。下一步：创建两个实验分支并分别验证。

---

## 十、2026-06-13 文档整合与总纲确立

### 10.1 整合动因

`SPEC.md` 已经承担“项目承诺做什么、做到什么算完成、当前代码支持到哪里”的职能，但此前未明确将其作为**项目总纲**，导致研究问题、数据范围、文档入口分散在 `topic_proposal.md`、`README.md`、`SPEC.md` 等多处。同时 `docs/topic_expansion_proposal.md` 已标注“已采纳并合并为主方案”，作为独立文档继续存在造成冗余。

### 10.2 整合动作

1. **确立 `SPEC.md` 为项目总纲**
   - 增加 §0 快速定位表。
   - 在 §1 增加“研究问题”小节，引用 `docs/topic_proposal.md`。
   - 更新 §9 文档地图，明确各文档职责。

2. **归档 `docs/topic_expansion_proposal.md`**
   - 将其独特内容（与参考选题差异化、工作量估算、风险评估、方案对比）合并到 `docs/topic_proposal.md` 第 7-11 节。
   - 删除原文件 `docs/topic_expansion_proposal.md`。

3. **精简 `docs/architecture.md`**
   - §6 模块职责矩阵删除“职责”列，避免与 `docs/workflow_design.md` 重复。
   - 矩阵前增加提示，指向 `docs/workflow_design.md` 获取完整节点表。
   - §7 变更日志删除，变更历史统一由 `docs/HANDOFF.md` 记录。

4. **简化 `README.md`**
   - “Pipeline 阶段详解”改为“Pipeline 阶段简介”，只保留阶段、命令、一句话说明。
   - 完整节点表指向 `docs/workflow_design.md`。
   - 文档地图更新，删除 `topic_expansion_proposal.md`，增加 `HANDOFF.md` 和 `workflow_design.md`。
   - 项目结构树中删除 `topic_expansion_proposal.md`。

5. **更新 `docs/README.md`**
   - 活跃文档表中删除 `topic_expansion_proposal.md`。
   - 新增“已删除/归档文档”表，记录 `topic_expansion_proposal.md` 的归档原因。
   - 快速入口指向更新为“项目总纲”的 `SPEC.md`。

### 10.3 整合后的文档地图

| 文档 | 职责 |
| --- | --- |
| `README.md` | 安装、运行、快速开始 |
| `SPEC.md` | **项目总纲**：契约、研究问题、验收标准、当前能力快照 |
| `AGENTS.md` | Agent 指令入口（老师模板要求） |
| `CLAUDE.md` | Agent 指令、编码约束、数据规则 |
| `docs/architecture.md` | 已验证/进行中阶段的架构与数据流 |
| `docs/crawl_spec.md` | 抓取范围、股票池、公告类型、限速策略 |
| `docs/HANDOFF.md` | 会话交接、变更历史、下一步 |
| `docs/topic_proposal.md` | 研究问题、变量定义、课程要求映射 |
| `docs/workflow_design.md` | Pipeline 节点 canonical 表、人工检查点、最小运行命令 |

### 10.4 不变约定

- `AGENTS.md` 保持原样，作为非 Claude Code Agent 的轻量入口（老师模板要求）。
- 所有老师模板类文档（`crawl_spec.md`、`topic_proposal.md`、`workflow_design.md`、`output_sample.md`、`parse_check.md` 等）均保留。
- 参考备份类文档（`cninfo_official_api_*.md`、`mineru_api_*.md`）保留，不进入总纲核心索引。

### 10.5 当时状态

- 文档整理完成，`topic_expansion_proposal.md` 已删除。
- 下一步继续执行 §9.6 的推进顺序：先跑通 parse，再并行实验 crawl 双路线。

---

## 十一、2026-06-14 official API 分支验证结果

### 11.1 实现内容

在 `experiment/cninfo-official-api` 分支完成以下改动：

- 新建 `src/crawl/_common.py`：提取 `infer_market()`、`generate_doc_id()`、`METADATA_COLUMNS`，供两种 crawler 复用。
- 重构 `src/crawl/cninfo_api.py`：改用共享的市场推断与 doc_id 生成逻辑。
- 新建 `src/crawl/cninfo_official_api.py`：实现官方 API crawler，包含 OAuth2 token 自动刷新、`p_info3015` 年报查询、字段映射。
- 修改 `src/main.py`：新增 `--crawl-backend {frontend,official}`，默认仍为 `frontend`。
- 修改 `configs/crawl.yaml`：新增 `cninfo_official_api` 配置段。
- 修改 `.env.example`：新增 `CNINFO_ACCESS_KEY` / `CNINFO_ACCESS_SECRET` 占位。
- 新增 `tests/test_crawl_official_api.py`：覆盖 token 刷新、候选选择、字段映射、metadata 写入。

### 11.2 验证结果

| 验证项 | 命令 | 结果 |
|--------|------|------|
| 单元测试 | `uv run pytest -q` | 51 passed |
| 官方 API mini pipeline | `uv run python src/main.py --stage crawl --crawl-backend official --limit 1` | ✅ 3 条 metadata |
| 下载 | `uv run python src/main.py --stage download --limit 3` | ✅ success=3, collision=0 |
| 审计 | `uv run python src/main.py --stage audit` | ✅ 全部检查通过 |
| 与前端 crawler 对照 | 分别跑 `--crawl-backend official/frontend --limit 1` | PDF URL、publish_date 完全一致；doc_id 因标题格式差异不同 |
| **完整 150 份官方 API crawl** | `uv run python src/main.py --stage crawl --crawl-backend official` | ✅ 150/150，失败 0 |
| **完整 150 份 PDF 下载** | `uv run python src/main.py --stage download` | ✅ 150/150，collision=0（1 次连接超时后重试成功） |
| **完整 150 份审计** | `uv run python src/main.py --stage audit` | ✅ 8 项检查全部通过，150 个唯一 SHA256 |

### 11.3 关键发现

- **OAuth2 认证方式**：`POST /api-cloud-platform/oauth2/token`，`grant_type=client_credentials`，然后在数据端点 URL 附加 `?access_token=xxx`。该认证端点未出现在 `cninfo_api_doc_tree.json`；原会话复盘显示，发现线索来自外部开源项目 `haspower/cninfo_api`，最终可靠性来自本项目实测。不要写成官方文档树原文。
- **可用接口**：`p_info3015`（公告基本信息）可稳定获取年报 PDF URL；`p_stock2101` 可获取股票基本信息。
- **不可用接口**：`p_cninfo5001`、`p_info3064`、`p_info3064t` 返回 415 “该用户没有购买包时长服务”，当前账号无权限。
- **标题差异**：官方 API 返回标题为 `恒瑞医药：恒瑞医药2021年年度报告`，前端 AJAX 返回 `<em>恒瑞医药</em>2021年年度报告`。PDF URL 和发布日期完全一致，但 doc_id 因标题不同而不同。
- **稳定性**：完整 150 份 crawl + download 全程仅出现 1 次 `static.cninfo.com.cn` 连接超时，下载器重试后成功。
- **早期原型边界**：`temp-队友做的东西原件/` 中 Week 12 年报爬虫走的是前端公开接口 `hisAnnouncement/query`，不是官方 OAuth API；早期原型作为历史参考保留，接口来源与正确性以官方文档和当前代码实测为准。

### 11.4 决策与下一步

- **official API 可用于年报 PDF 抓取**，作为前端 AJAX 的替代/并行方案。
- **问询函仍需前端方案**：官方 API 问询函接口无套餐权限，无法使用。
- 若后续决定合并 official API 到主路线，需考虑 doc_id 与前端版本的兼容性问题（可通过统一清洗标题解决）。
- 当前分支状态已可跑通 `crawl → download → audit` mini pipeline，可作为双路线对比实验的 baseline。

### 11.5 2026-06-14 最终整理（neat-freak）

在确认 official API 文档与实现后，进行最后一轮收尾整理：

- **PDF / `doc_id` 人可读改造**：
  - 官方 API crawler 的 `doc_id` 与 PDF 文件名统一为 `{stock_code}_{stock_name}_{report_year}年报`。
  - `local_pdf_path` 改为相对路径 `data/pdf/{doc_id}.pdf`，`download` 与 `audit` 阶段兼容相对/绝对路径。
- **文档同步**：
  - 更新 [`docs/cninfo_official_api_annual_report.md`](docs/cninfo_official_api_annual_report.md)，补入 `p_info3015` / `p_info3005` 官方 API 文档字段，并记录 OAuth2 token 端点的实测来源边界。
  - 更新 [`docs/README.md`](docs/README.md) 索引。
  - 更新 [`docs/architecture.md`](docs/architecture.md) metadata 示例为新人可读格式。
  - 更新 [`docs/mineru_setup.md`](docs/mineru_setup.md) 烟测示例为当前 PDF 文件名与正斜杠路径。
- **代码清理**：
  - 简化 `src/crawl/cninfo_official_api.py` 中 `local_pdf_path` 与业务错误码的冗余写法。
  - 删除一次性迁移脚本 `scripts/migrate_pdf_names.py`。
- **数据清理**：
  - 删除旧 `doc_id` 格式的 `data/parsed/`、`data/sections/` 样例输出，避免与当前 150 份年报混淆。
- **Bug 修复**：
  - 修复 `src/download/downloader.py` 在 `--limit` 模式下会截断 `metadata.csv` 的 bug（保存时保留未处理记录）。
  - 修复后重新跑通官方 API crawl，因网络波动缺失 4 条记录，从 `download_log.jsonl` 补回，最终 `metadata.csv` 恢复为 150 条。

#### 最终验证

| 验证项 | 命令 | 结果 |
| -------- | ------ | ------ |
| 单元测试 | `uv run pytest -q` | 51 passed |
| 官方 API crawl | `uv run python src/main.py --stage crawl --crawl-backend official` | 150 条 metadata（含 4 条从日志补回） |
| 下载校验 | `uv run python src/main.py --stage download` | success=150, collision=0 |
| 数据审计 | `uv run python src/main.py --stage audit` | ✅ 全部检查通过 |

**分支当前状态（历史记录）**：截至本节整理时，`crawl → download → audit` 全链路 150/150 通过，PDF 文件名与 metadata 已统一；parse 当时仍待推进。最新状态见本文开头总览与 §11.11：parse、route、extract、validate 和下游闭环已完成，下一步是人工复核字段缺失样本与问询弱标签。

### 11.6 2026-06-14 CNINFO 外部参考来源登记

本轮只补文档来源记录，不改爬虫逻辑。

- 新增 `docs/cninfo_external_references.md`，集中记录 CNINFO 相关开源参考、license、影响范围和复用边界。
- 补正 token 来源：`/api-cloud-platform/oauth2/token` 的调用方式来自 `haspower/cninfo_api` 这一外部线索；它仍不是官方 API 文档树来源，项目可靠性来自实际跑通的 150 份年报链路。
- 记录 `legeling/Annualreport_tools` 只作为前端公告查询 `hisAnnouncement/query` 的工程参考；由于未见明确 LICENSE，不复制源码，不提交第三方代码。
- 再次明确早期原型存档边界：早期原型作为历史参考保留，接口来源与正确性以官方文档和当前代码实测为准。

### 11.7 2026-06-14 问询抓取修复：先发现、可断点、后下载

本轮修复问询 discovery 返回 0 条候选的问题，并把长流程拆成可观察的两段。

- 根因：`hisAnnouncement/query` 使用裸股票代码传入 `stock=600276` 时，部分公司会返回空列表；前端接口需要空 `stock` 或 `code,orgId`。由于 `orgId` 不稳定，当前实现改为 `stock=""` + `searchkey=公司名`，再用返回字段 `secCode` 校验股票代码。
- `--stage inquiry` 现在只做候选发现，不下载 PDF。每处理一条年报 metadata，立即追加 `data/inquiry/inquiry_candidates.csv`、写入 `outputs/logs/inquiry_log.jsonl`、更新 `data/inquiry/inquiry_discovery_cache.json`，并在控制台打印进度、raw/parsed 候选数、耗时和 ETA。
- 新增 `--stage inquiry-download`，只读取 `inquiry_candidates.csv` 并调用 `PDFDownloader` 下载候选 PDF。候选文件不存在时会提示先运行 discovery。
- 新增 `--force` 用于重建 discovery 的候选 CSV 和 cache。历史日志保持 append-only，便于追踪修复前后的查询表现。
- 后续已完成全量 discovery 与候选下载收口；本节保留为当时修复过程记录。

### 11.8 2026-06-14 问询候选质量收敛：命名、角色、PDF 标题校验

本轮继续收敛 inquiry crawl 的候选质量，先稳定命名、角色和标题校验，再进入全量候选下载。

- 新增 `src/crawl/inquiry_quality.py`，负责候选角色分类、可读 `doc_id`、PDF 首页标题抽取和 orphan PDF 报告。
- `inquiry_candidates.csv` 新增 `document_role`、`pdf_title`、`pdf_title_status`、`title_match_status`。旧候选 CSV 缺少新列时会自动补齐 schema。
- 问询 PDF 新命名为 `{stock_code}_{stock_name}_{report_year}_{publish_date}_{document_role}_{announcement_id}.pdf`；`stock_name` 会清理巨潮高亮标签。
- `--stage inquiry-download` 下载后会尝试用 `pdfplumber` 抽取首页标题并回写候选表。无文字层或缺失文件只标记状态，不阻断流程。
- `outputs/reports/inquiry_orphan_pdf_report.md` 只列出未被当前候选表引用的旧 PDF，不自动删除，避免误删 scratch 缓存。

### 11.9 2026-06-15 下载层收口与 parse 前保护

本轮不再继续扩大 inquiry 规则，先把 download part 收尾，并为年报 150 份 parse 做全量前保护。

- 年报下载层：`metadata.csv` 150 条、150 个唯一 `doc_id`、150 个唯一 PDF 路径，`download_status=success` 150 条。
- 问询下载层：固定当前 28 条候选，28 个唯一 `doc_id`、28 个候选 PDF 全部下载成功，orphan report 为 0；标题校验 22 个 match、6 个 unknown、0 个 mismatch。
- 临时 broad audit 和 label audit 继续保留在 ignored scratch 输出中，只作为策略讨论参考，不升级为正式 schema 或验收数据。
- `MinerUParser` 的 resume 逻辑收紧：只有 `parsed_docs.jsonl` 中 success 且 `data/parsed/{doc_id}.md` 存在、非空时才跳过。
- `MinerUParser.run()` 增加逐 PDF 进度日志，记录 `[当前/总数]`、`doc_id`、状态和耗时，避免全量 parse 长跑时不可观察。
- 当时的下一步执行顺序：先 `parse --limit 1`，再 `parse --limit 5`，确认输出 Markdown 非空可读后再跑完整 150 份年报 parse。最新状态见开头总览与 §11.11：150 份 parse 与后段闭环已完成。

### 11.10 2026-06-15 MinerU API 分段 parse smoke backend

本轮暂停本地全量 parse，先验证 MinerU 精准解析 API 是否适合长年报批量解析。

- 新增 `src/parse/mineru_api_parser.py`：显式 API backend，默认仍保留本地 CLI backend。
- 新增 CLI 参数：`--parse-backend local|api|api-batch`。默认 `local`；API smoke 使用：
  ```powershell
  uv run python src/main.py --stage parse --parse-backend api --limit 1
  ```
- 新增 URL batch backend：
  ```powershell
  uv run python src/main.py --stage parse --parse-backend api-batch --limit 2
  ```
- API backend 使用 `metadata.csv` 中的 `pdf_url`，按本地 PDF 页数生成 `page_ranges`；超过 200 页的年报拆为 `1-200` 与 `201-end`。
- API 输出契约保持不变：最终写入 `data/parsed/{doc_id}.md`；原始 zip 与解压结果保留在 `data/parsed/mineru_api_raw/{doc_id}/part_*/`。
- 任务断点与审计记录写入 `data/parsed/mineru_api_tasks.jsonl`。记录 task_id、page_range、status、full_zip_url 与 error。
- 断点恢复口径：已成功且本地 raw `full.md` 非空的 segment 会直接复用；只有 `submitted` 但未完成的 segment 会继续轮询原 task_id，不重复提交。
- 监控口径：轮询日志打印 `task_id`、`state`、`page_range` 和 `extracted_pages/total_pages`；每份 PDF 打印 `[当前/总数]`、状态和耗时。
- `MINERU_API_KEY` 只从环境变量或 `.env` 读取，不能写入 git、README 或 HANDOFF。
- 线上复核 `https://mineru.net/apiManage/docs` 后确认：精准 API 支持 `/api/v4/extract/task`、`GET /api/v4/extract/task/{task_id}`、`page_ranges`、200 页限制和 `full_zip_url`；同时支持 URL batch 提交 `/api/v4/extract/task/batch` 和批量查询 `/api/v4/extract-results/batch/{batch_id}`。
- 限流记录：提交任务接口共享 50 files/min 限流；单用户每天最多 5000 个文件，html 文件最多 100 个；结果查询 1000 次/min。`api-batch` 默认每批 50 个 page segment，并有滑窗提交限速；本地结果包默认 8 worker 并发下载、4 worker 并发解压。
- 2026-06-15 smoke 结果：
  - `uv run python src/main.py --stage parse --parse-backend api-batch --limit 2` 成功，2 份年报、共 4 个 segment；其中已有 raw 的 2021 年报被复用，2022 年报 2 个 segment 经 batch 提交后成功。二次运行同命令约 5 秒完成，没有重复提交 batch。
  - `uv run python src/main.py --stage parse --parse-backend api-batch --limit 5` 成功，5 份年报全部生成 Markdown。第一次 `limit 5` 在结果 zip 下载阶段遇到 `cdn-mineru.openxlab.org.cn` SSL EOF，疑似 VPN/网络短断；修复后下次运行复用原 batch，不重提任务，只补下载并合并。
- `uv run python src/main.py --stage parse --parse-backend api-batch --limit 20` 已生成 20 份非空 Markdown，研发/开发支出/无形资产/资本化等关键词抽查有命中。
- `uv run python src/main.py --stage parse --parse-backend api-batch` 已完成 150 份年报全量解析：`data/parsed/*.md` 为 150，`mineru_api_tasks.jsonl` 最新状态为 275 个 segment 全部 `success`，失败 0。
- 结果 zip 下载保护：`download_full_markdown()` 保留 `MINERU_API_DOWNLOAD_RETRIES` / `MINERU_API_DOWNLOAD_RETRY_DELAY` 控制的应用层重试；batch segment 断点新增 `ready`、`zip_downloaded`、`download_failed`、`extract_failed`。后续运行优先复用已有 `full.md`，其次补解压已有 `result.zip`，再用原 `full_zip_url` 补下载；如果 CDN URL 失效，会用原 `batch_id/data_id` 刷新 `full_zip_url` 后再补下载，避免重复消耗提交额度。
- 文件管理约定：最终 Markdown 只放 `data/parsed/{doc_id}.md`；API 原始 zip/解压只放 `data/parsed/mineru_api_raw/{doc_id}/part_XX/`；任务断点只放 `data/parsed/mineru_api_tasks.jsonl`。这些产物属于 ignored data，不提交 git。
- `$pdf-vision-mineru` 全局 skill 暂不更新；等 project2 的 API smoke 跑通后再把“长文档优先 API 分段”的经验反哺。

### 11.11 2026-06-15 文档收口与下一阶段 handoff

本轮做 end-of-session 文档同步，不改业务代码。正式交接入口继续使用本文档，不再新增 `.claude/handoffs/` 下的项目阶段 handoff。

- 同步当前状态：
  - `crawl → download → audit`：年报 150/150 已验证通过。
  - `parse`：MinerU API batch 已完成 150/150 年报 Markdown，`data/parsed/*.md` 为 150，`mineru_api_tasks.jsonl` 最新状态为 275 个 segment 全部 `success`。
  - `inquiry`：固定当前 28 条候选，`inquiry-download` 28/28 成功，orphan=0；问询 PDF 暂不进入 parse 主线。
- 同步文档：
  - `SPEC.md` 当前能力快照已改为全链路 MVP 完成：parse 150/150、extract 150 条、validate 150/150、score 83/150、detect 17 条异常、inquiry-label related、analyze 矩阵。（此为 06-15 快照数字：related=7、TN=126/FN=7；06-20 P1 重跑后更新为 related=1、TN=132/FN=1，单源真值见 §12.10）
  - `docs/architecture.md` 当前架构图已改为“全链路已跑通，后续做人工复核与标签增强”。
  - `docs/mineru_setup.md` 已改为“API batch 主路线 + 本地 CLI fallback”。
  - `CLAUDE.md` 与 `.env.example` 已补充 `api-batch` 推荐复跑口径和 `MINERU_API_KEY` 只写 `.env` 的约束。
- 清理口径：
  - 早期 `HANDOFF.md` 历史章节中“parse 1 份样本/150 未验证”的表述已标注为历史状态，避免和当前总览冲突。
  - 临时生成的 `.claude/handoffs/2026-06-15-092322-project2-route-extract-next.md` 已删除，不作为正式项目交接文件。

**下一对话第一步（已按 2026-06-15 全量后段结果更新）**：

```powershell
cd project2
uv run python src/main.py --from-stage validate --to-stage report
```

然后人工抽查 `data/scored/records.jsonl` 中 `data_quality_notes` 非空的记录、`data/anomaly/anomaly_list.csv` 中 17 条异常，以及 `data/inquiry/inquiry_records.jsonl` 中 related 弱标签（06-15 时为 7 条，06-20 重跑后为 1 条，见 §12.10）。优先确认缺失字段是披露缺失、章节定位问题，还是 LLM 抽取漏掉。

**当前不建议立刻做的事**：

- 不把当前 `inquiry-label` 弱标签当成人工真值。它只基于标题、PDF 首页标题和前几页关键词，适合课堂展示闭环，最终实证仍需全文语义标签或人工复核。
- 不继续扩大 inquiry 候选关键词。当前下载层已经收口，继续打转的边际收益低。
- 不提交 `data/parsed/`、MinerU raw zip、日志、`.env` 或第三方源码。

---

## 十二、2026-06-20 排查与交差计划

### 12.1 排查动因

对照老师 Week11–16 讲义逐项核查 project2 是否真正达到项目要求，回答「这样是否真的达到了老师的要求」。排查方法：读 README/SPEC/CLAUDE.md + 讲义 + 实际数据文件统计 + 评分模型代码审查，数字均来自实际文件。

### 12.2 排查结论

**抽取流水线扎实、对齐课程要求；评分/问询闭环是 ambition 超出 evidence。** 课程不要求训练 ML 模型（讲义明确「不训练大模型」，Rubric 无预测性能项），所以「规则评分 + 问询闭环」定位上没偏离。真正会塌的是两块没做的硬性事 + 一处诚信风险。

按老师 Rubric 估分：当前 ≈76/100；补完 P0（人工评估 + 提交清单缺件）可到 ≈90/100。边际收益 +14 分几乎全在 P0，且都是「补了就拿分」的机械工作。

### 12.3 三个必修塌点

1. **人工评估完全没做，但 `ai_usage_statement.md` 声称做了 30+ 条** → 诚信风险 + 课程强制项双失。
2. **老师提交清单大面积缺件**（prompts/、demo_script、difficulty_declaration、run_log.jsonl、section_check_report、ai_worklog_all、final_slides、GitHub 公开仓库）→ Week16 自查清单逐项不达标。
3. **风险评分方法论 3 个 30 秒崩盘型硬伤**（fuzziness 词表含「等/相关/未来」、change_zscore 用 abs()、行业靠顺序推断）+ 文档措辞「异常检测/闭环验证」超出证据（实际 TP=0）→ 答辩风险。

### 12.4 数据实况（文件统计，非文档转述）

| 项 | 文档声称 | 实际 | 问题 |
| --- | --- | --- | --- |
| validated 行数 | 150 | 150 | ✅ |
| 可算资本化率 | 60 | 60 | ✅ |
| 有风险分 | 83 | 83 | ✅ |
| 67 条无风险分原因 | "字段缺失保留 notes" | `data_quality_notes` 全是 `TODO: waiting for...` 占位符 | 占位符当说明 |
| `null_reason` 字段 | CLAUDE.md 规定要写 | validated 阶段 100% 空 | 违反自家规则 |
| 异常类型分布 | 表列 5 种 | 实际 2 种（industry_outlier 15 / change_spike 2） | 另外 3 种是死的 |
| 问询 related（company-year 层） | README/SPEC 说「7 条」 | `inquiry_records.jsonl` 中 `capitalization_related=True` 仅 1 条 | 候选层 7 ≠ company-year 层 1，跨层数字混用 |
| 闭环矩阵 | README: TP=0/FP=17/TN=133/FN=0；SPEC: TP=0/FP=17/TN=126/FN=7 | `loop_evaluation.json`: TP=0/FP=17/TN=132/FN=1 | 三处数字不一致 |
| TN=132 含水 | 未点明 | 其中 67 条是缺数据无法评分被默认归非异常 | TN 虚高 |
| 公司池 industry | "申万一级"（topic_proposal） | crawl.yaml 0 家显式写，靠顺序推断 | 文档代码不一致 |
| 人工校验 ≥30 条 | ai_usage_statement 称「已做」 | 0 条 | 声明性造假 |

> 上表为 2026-06-20 排查时的**修复前快照**（「文档声称」列反映当时文档状态）。相关问题已在 P0-5/P1/P2 及本次 review 中修复：README/SPEC/architecture 等已统一为 related=1、TN=132/FN=1（单源真值见 §12.10）；ai_usage_statement 虚假声明已改为 AI agent 辅助 35 样本交叉验证。

### 12.5 问询闭环定位决策

7 个正例、TP=0、TN 含 67 条缺数据记录，统计上空。受限于数据量难做成真正「验证」。**定位为 A+B 轻量**：措辞降级为「可行性测试」+ 加最简 baseline 对比（按资本化率排序 top20% vs 规则评分），即使都=0 也能诚实说「在当前样本上无差异，信号不足」。底线是措辞降级（零代码）。

### 12.6 行动计划与状态

#### P0 交差刚需（+14 分）

| # | 任务 | 状态 |
| --- | --- | --- |
| P0-1 | 人工评估 35 条（AI agent per-field + 四类指标程序算 + 局限） | ✅ 完成，见 `outputs/reports/eval_report_final.md` + `eval_per_field.csv` |
| P0-2 | section_check_report（router 末尾汇总 + csv/md + pytest） | ✅ 完成，`outputs/reports/section_check_report.{csv,md}` |
| P0-3 | 统一 run_log.jsonl（common.log_step + main.py run_stage 包装 + pytest） | ✅ 完成，`outputs/logs/run_log.jsonl` |
| P0-4 | 提交清单缺件（prompts/demo_script/difficulty_declaration/ai_worklog_all/final_results/parsed_docs_sample） | ✅ 完成 |
| P0-5 | 修正虚假声明 + 闭环数字统一（以 P1 重跑后为准） | ✅ 完成，`ai_usage_statement.md` 删除「30+ 条已做」改为指向 `eval_report_final.md`；README/SPEC/architecture/topic_proposal/presentation_checklist 矩阵统一为 TP=0/FP=17/TN=132/FN=1 |
| P0-6 | HANDOFF §十二 + 删除独立诊断文件 | ✅ 本节 |
| P0-7 | GitHub 公开仓库 + final_slides | ⏳ 用户最后做 |

#### P1 方法论硬伤（改代码 + 重跑）

| # | 任务 | 状态 |
| --- | --- | --- |
| P1-1 | fuzziness 词表去毒 + 长度归一化 | ✅ 完成，scorer.py FUZZY_KEYWORDS 换为会计估计模糊语 + FUZZY_NORM_CHARS=200 |
| P1-2 | change_zscore abs() → 正向跳升 | ✅ 完成，`min(100, max(0,Z)/2*100)`，重跑后 change_spike 2→1 |
| P1-3 | crawl.yaml 显式写 industry | ✅ 完成，50 家全显式（20/20/10），scorer 优先读显式 industry |
| P1-4 | 措辞统一（异常检测→风险排序，闭环验证→可行性测试，逐句人工改） | ✅ 完成，methodology/SPEC/README/reporter/topic_proposal 等逐句改 |
| P1-5 | 重跑 `--from-stage validate --to-stage report` + P0-5 数字统一 + 修虚假声明 | ✅ 完成，重跑数字见 §12.10 |

#### P2 问询闭环 A+B 轻量

| # | 任务 | 状态 |
| --- | --- | --- |
| P2-1 | 最简 baseline 对比（按 CR 排序 top20% / 全标正 vs 规则评分） | ✅ 完成，`evaluator.py` 新增 `_compute_baselines`，写入 `loop_evaluation.json` `baselines` 字段 + final_report「Baseline 对比」小节；当前正样本仅 1 条，三者 precision/recall 接近 0，诚实呈现「信号不足」而非「验证成功」 |
| P2-2 | 报告点明 TN 水分 | ✅ 完成，`evaluator.py` 新增 `tn_water`（TN=132 含 67 条缺数据默认归非异常），final_report「TN 水分说明」小节 |

### 12.7 人工评估关键发现（P0-1）

35 条样本（17 异常 + 9 问询 + 随机），110 个可判定字段行，准确率 46.4%。错误分布：section_error 27（漏抽开发支出附注最多）、data_error 20、hallucination 8、parse_error 6（capitalization_condition 占位符）、prompt_error 1。

按字段：研发投入主表字段准确率 50-85%（资本化率 84.6% 最高），开发支出附注字段 25-30%（期初/期末混淆 + 漏抽）。三个失败案例：汇顶 2022 期初/期末余额混淆、韦尔 2021/2022 研发投入金额幻觉、capitalization_condition 占位符。诚实标注 eval agent 与 extractor 同源 LLM 共错风险。

### 12.8 下一步

P1 已全部完成并重跑（基准数字见 §12.10），P0-5 数字统一与虚假声明已修。剩余：

1. **P2-1** 最简 baseline 对比（按资本化率排序 top20% / 随机 vs 规则评分），写入 `outputs/loop_evaluation.json` 与 final_report。
2. **P2-2** final_report 点明 TN 水分（TN=132 含 67 条缺数据无法评分被默认归非异常）。
3. **P0-7** 用户最后：推 GitHub 公开仓库 + 制 `final_slides.pdf`（推送前 `git log --all -- .env` 核查无密钥泄漏）。

### 12.9 不变约定

- 接力与进度跟踪统一写本文件（HANDOFF），不再维护独立诊断文档（已删除 `docs/diagnosis_and_plan_2026-06-20.md`）。
- 每完成一项回写本节状态列。
- 禁止在 P0-1 完成前声称「人工评估已做」（P0-1 已完成，但需与 `ai_usage_statement.md` 同步后才算闭环）。

### 12.10 P1 重跑后基准数字（2026-06-20，单源真值）

`uv run python src/main.py --from-stage validate --to-stage report` 全量重跑后，以下为后续所有文档应引用的统一数字（来自 `outputs/loop_evaluation.json` 与 `data/scored|anomaly|inquiry` 文件统计）：

| 指标 | 值 |
| --- | ---: |
| validate | 150/150 passed |
| score | 83 有可用风险分 / 67 未评分（关键字段缺失，`aggressiveness_score` 为 null；scorer `stats` 字段名为 `partial`） |
| detect | 17 anomalies（industry_outlier 16 / change_spike 1）|
| 可算资本化率 | 60，均值 11.57% / 中位 2.67% |
| 异常组 / 非异常组资本化率均值 | 23.81% / 6.73% |
| inquiry-label | 150 条标签，10 条有候选，1 条 related（v2 语义标签）|
| 闭环矩阵 | TP=0 / FP=17 / TN=132 / FN=1 |
| TN 水分 | TN=132 中含 67 条缺数据无法评分被默认归非异常的记录（见 P2-2）|

注：§12.4 的「数据实况」表为 P1 改码前的排查快照（异常类型当时为 industry_outlier 15 / change_spike 2、问询 related 已是 1）；改码重跑后以本节为准。

### 12.11 提交前终审 review（2026-06-20，含 /neat-freak）

P0/P1/P2 完成后做的提交前系统性 review（三轮并行 Explore 审查 + 修复 + neat-freak 对齐），确认并修复了以下残留问题：

| 编号 | 严重度 | 问题 | 处理 |
| --- | --- | --- | --- |
| F1 | 🔴 高 | `section_check_report.csv` 仅有 docA/docB 合成数据，非真实 corpus | 重跑 `--stage route`（150 doc × 5 规则 = 750 行真实）+ 重跑 `scripts/run_eval.py`，Section Quality 基于真实数据 |
| F2 | 🟠 中 | methodology.md §6.2/§8 仍是旧 fuzziness 词表 + `hits/6`，与 §3.3 矛盾 | §6.2 改为指向 §3.3 新词表 + 长度归一化公式；§8 审计表分母改 `max(1,len/200)` |
| F3 | 🟠 中 | methodology.md §3.1/§8 + reporter.py 仍称行业「顺序启发式…待修复」 | 改为「显式 industry 优先，顺序仅 fallback」 |
| F4 | 🟠 中 | HANDOFF 早期章节 7 行过期数字（TN=126/FN=7、related=7） | 当前态行更新；历史快照行加「修复前快照 / 见 §12.10」标注 |
| F5 | 🟡 低 | SPEC/README/architecture/topic_proposal 残留「顺序启发式」+ SPEC 残留 `abs(change_zscore)` | 统一为显式优先措辞；SPEC 改 `max(0, change_zscore)` |
| F6 | 🟡 低 | HANDOFF/cninfo_data_discovery/topic_ideas overclaim（异常检测定位语、闭环有真实意义） | 降级为风险排序 / 可行性测试 |
| F7 | 🟡 低 | 「67 partial」术语错配 | README/SPEC/architecture 改 no-score；§12.10 删除虚假 58/25 拆分（数据实测不支持） |
| F8 | 🟢 信息 | 未跟踪文件待纳入 | `prompts/`、`demo_script.md`、`difficulty_declaration.md`、`ai_worklog_all.md`、`scripts/build_ai_review.py`、`scripts/run_eval.py` 已确认无敏感信息，建议纳入提交 |
| F9 | 🟢 信息 | 历史 worklog 含旧框架措辞 | 保留不改（时间戳历史记录） |

neat-freak 自检：CLAUDE.md 路由清单/环境变量/MinerU 版本与代码一致；README 安装运行步骤与 `pyproject.toml`+`src/main.py` 一致；AGENTS.md 指向 CLAUDE.md（单一源）；memory `cninfo-api-archive-location` 经核实仍准确（mine/friend/scripts 三子目录齐备）；相对时间仅余 API 字段描述中的合法「最近」（如「最近 100 条记录」），无漂移。

剩余：P0-7 GitHub 公开推送 + `final_slides.pdf`（用户最后做，推送前 `git log --all -- .env` 复核）。

