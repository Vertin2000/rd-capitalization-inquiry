# AI Worklog Week 16

## 使用的工具

Claude Code

## 本周让 AI 帮助的任务

- [x] route / extract / validate 快速推进
- [x] Kimi Code CLI 高并发 extract 执行层改造
- [x] 年报源文件错抓排查与补抓清单记录
- [ ] 最终报告生成
- [ ] 展示材料准备
- [ ] 答辩问题准备
- [ ] `presentation_checklist.md` 逐项确认

## 我给 AI 的上下文

- `README.md`、`SPEC.md`、`docs/HANDOFF.md`
- 已完成 150 份年报 MinerU Markdown 解析
- 需要尽快推进到结构化研发资本化数据
- 本机可用 Kimi Code CLI，API 成本不是约束
- 高并发优先，但出错时要 fail-fast，不要后台挂住

## AI 生成或修改的文件

- `src/route/section_router.py`
- `configs/section_rules.yaml`
- `src/extract/llm_client.py`
- `src/extract/llm_extractor.py`
- `src/validate/validator.py`
- `src/crawl/cninfo_official_api.py`
- `src/main.py`
- `src/model/schemas.py`
- `tests/test_section_router.py`
- `tests/test_llm_extractor.py`
- `tests/test_validator.py`
- `tests/test_main.py`
- `tests/test_crawl_official_api.py`
- `data/metadata/metadata.csv`（临时修正 1 条错抓年报来源，后续需补下载和补 MinerU）

## 我实际运行的命令

- `uv run pytest tests/test_llm_extractor.py tests/test_main.py -q`
- `uv run pytest -q`
- `uv run python src/main.py --stage extract --workers 149 --fail-fast`
- `uv run pytest tests/test_crawl_official_api.py -q`
- `uv run python -c "... CninfoOfficialCrawler()._search_company_year('603501','韦尔股份','2021') ..."`
- `uv run python -c "... scan metadata suspicious annual titles ..."`

## 报错与修复

### Kimi Code CLI 高并发抽取

- 直接 HTTP 调 Kimi Code API 返回 `403 access_terminated_error`，原因是 Kimi For Coding 限 Coding Agent 身份；改走本机已登录的 Kimi Code CLI。
- 全量 `extract --workers 149` 曾出现大量失败：
  - Windows `[WinError 206] 文件名或扩展名太长`：CLI 参数携带 prompt 过长。
  - Kimi `429 rate_limit`：高并发触发限流。
  - `high risk`：单条调用被 Kimi 拒绝，重试后可继续。
- 修复：
  - prompt 截断到可控长度。
  - `LLMClient` 使用 `subprocess.Popen` 追踪活跃 Kimi 进程。
  - `extract` 增加 `--workers` 和 `--fail-fast`。
  - 任一 worker 异常时取消 pending futures，并调用 `terminate_active_processes()` 清理活跃 Kimi 进程。
  - 每完成一条输出 `进度: done=X/Y success=S failed=F pending=P`。

### 年报源文件错抓

已确认 1 条前置数据源错误，不计作 LLM 抽取失败：

| doc_id | 问题 | 错误 URL | 正确 URL | 当前处理 |
| --- | --- | --- | --- | --- |
| `603501_韦尔股份_2021年报` | `metadata.csv` 原来把《平安证券股份有限公司关于上海韦尔半导体股份有限公司2021年度持续督导年度报告书》误标成年报，导致 PDF 只有 33 行 Markdown，route 为空 | `http://static.cninfo.com.cn/finalpage/2022-04-19/1212960525.PDF` | `http://static.cninfo.com.cn/finalpage/2022-04-19/1212960545.PDF` | 已把 metadata 临时改成正确标题和 URL；后续集中重新下载该 PDF、重跑 MinerU、重跑 route |

修复源头：

- `src/crawl/cninfo_official_api.py` 的年报候选选择器新增负面标题过滤：
  - `持续督导`
  - `保荐`
  - `核查`
  - `专项`
  - `独立意见`
  - `监管工作函`
  - `问询函`
  - `回复`
  - `摘要`
  - `半年度报告`
  - `季度报告`
  - `更正`
  - `提示性公告`
- 新增回归测试，保证只有持续督导报告时返回 `None`，不会误当年报。
- 修正后扫描当前 `metadata.csv`，可疑标题命中数为 0。

后续补跑建议：

1. 只重新下载 `603501_韦尔股份_2021年报.pdf`。
2. 只重跑这一条 MinerU API batch parse，覆盖 `data/parsed/603501_韦尔股份_2021年报.md`。
3. 只重跑这一条 route，覆盖 `data/sections/603501_韦尔股份_2021年报_sections.jsonl`。
4. 然后再跑全量 `extract --workers 149` 或按需跳过该 known bad 项继续抽剩余 146 条。

## 我人工检查了什么

- 抽查 `603501_韦尔股份_2021年报.md`，发现标题是持续督导年度报告书，不是真正年报。
- 查询官方 API 后确认真正年报标题为 `韦尔股份：2021年年度报告全文`，PDF URL 为 `1212960545.PDF`。
- 扫描当前 `metadata.csv` 的可疑公告标题，修正后命中数为 0。

## 我理解的关键代码

- `route` 阶段只从 `data/parsed/{doc_id}.md` 找研发相关 section；如果上游 PDF 错了，route 为空是正确报警，不应该强行喂给 LLM。
- `extract` 阶段的 resume 依赖 `data/extracted/records.jsonl` 中已有 `doc_id`；并行 worker 只做单条抽取，JSONL 写入必须留在主线程。
- `--fail-fast` 的作用是调试和断点：发现本地空 section、LLM 异常或 worker 异常时立刻退出并清理活跃 Kimi 进程。
- 年报 crawler 不能只看标题里有“年度报告”，还要排除“持续督导年度报告书”等非上市公司年度报告文件。
