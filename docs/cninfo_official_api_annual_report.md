# 巨潮官方 API 年报抓取接口切片文档

> 目标读者：不了解本项目、但懂 CS 的新人。读完本文后，应能独立理解 `src/crawl/cninfo_official_api.py` 为什么写成现在这样。

---

## 1. 我们要抓什么数据

本项目研究“上市公司研发资本化风险排序与问询函可行性测试”。
在 **crawl** 阶段，我们需要先拿到每家目标公司的**年度报告 PDF**。

目前目标数据集：

- 50 家上市公司（医药制造 20 家 + 电子设备 20 家 + 软件信息 10 家）
- 3 个会计年度：2021、2022、2023
- 每家公司每年 1 份年报 PDF
- 预期共 150 条记录 / 150 个 PDF

公司列表与年份配置在 [`configs/crawl.yaml`](configs/crawl.yaml) 的 `companies` 与 `years` 字段。

---

## 2. 为什么选官方 API 而不是前端 AJAX

巨潮资讯网（cninfo.com.cn）其实有两套接口可以查公告：

| 维度 | 前端 AJAX 接口 | 官方 API |
| ------ | ---------------- | ---------- |
| URL | `http://www.cninfo.com.cn/new/hisAnnouncement/query` | `http://webapi.cninfo.com.cn/api/info/p_info3015` |
| 认证 | 无 | OAuth2 `client_credentials`，需 `AccessKey` / `AccessSecret` |
| 稳定性 | 可能随前端改版失效 | 官方文档接口，相对稳定 |
| 权限 | 公开访问 | 部分接口需额外购买套餐 |

我们当前在 `experiment/cninfo-official-api` 分支验证官方 API。验证结果是：

- `p_info3015`（公告基本信息）**可用**，能准确返回年报 PDF URL。
- `p_info3064` / `p_info3064t`（交易所问询函）**不可用**，返回 415 “未购买包时长服务”。
- 因此**官方 API 只负责年报 PDF**，问询函仍走前端 AJAX 方案。

---

## 3. 认证：OAuth2 client_credentials

### 3.1 凭证来源

代码从 `.env` 读取两个环境变量：

```bash
CNINFO_ACCESS_KEY=你的AccessKey
CNINFO_ACCESS_SECRET=你的AccessSecret
```

`.env` 已加入 `.gitignore`，**禁止把真实凭证写入代码**。
`.env.example` 中只放占位符，见 [`.env.example`](.env.example)。

### 3.2 Token 获取

```http
POST http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
client_id={CNINFO_ACCESS_KEY}
client_secret={CNINFO_ACCESS_SECRET}
```

返回示例：

```json
{
  "access_token": "eyJ0...",
  "token_type": "bearer",
  "expires_in": 3599
}
```

### 3.3 认证接口来源边界

`/api-cloud-platform/oauth2/token` **未出现在**我们导出的官方 API 文档树（`cninfo_api_doc_tree.json`）中；文档树能证明的是 `p_info3015` 等数据接口的元数据，不包括认证端点本身。

当前可确认的事实是：

- 原会话复盘显示，该端点的发现线索来自外部开源项目 [`haspower/cninfo_api`](https://github.com/haspower/cninfo_api)，不是来自项目归档或官方文档树。
- 代码通过该端点能获取 `access_token`，并已支撑 `crawl -> download -> audit` 跑通 150 份年报。
- `p_info3015` 在官方 API 文档树中有明确条目，网关码为 `a0fec4cde3bf4f83821fb5a769231100`。
- 队友 Week 12 原始爬虫只使用 `www.cninfo.com.cn/new/hisAnnouncement/query` 和 `static.cninfo.com.cn`，未发现 OAuth2 官方 API 实现。
- `data/cninfo-api-archive/friend/pi-session-conversation.txt` 记录的是官方 API 文档树抓取过程，也未记录该 token 端点。

因此本文把 token 端点记为“**外部开源线索 + 本项目实测可用的认证接口**”，而不是“已在公开 API 文档树中找到的接口”。外部来源边界见 [`cninfo_external_references.md`](cninfo_external_references.md)。如果后续认证失败，应优先复核该端点是否仍可用、账号权限是否变化、token 是否需要改用请求头或其它参数位置。

### 3.4 Token 使用方式

所有数据接口调用时，把 token 以 **URL 查询参数**形式附加：

```http
POST http://webapi.cninfo.com.cn/api/info/p_info3015?access_token=eyJ0...
```

这是我们在实验中试出来的官方实际用法（文档页面未明确写明参数位置，但返回 401 时尝试 refresh 后通过）。

### 3.5 Token 刷新策略

- token 有效期约 1 小时（`expires_in=3599`）。
- 代码在内存中缓存 token，并预留 60 秒缓冲期。
- 遇到 HTTP 401 时自动重新获取 token并重试请求。
- 可额外缓存到 `data/cninfo_official_token.json`（不提交），避免重复申请。

对应代码：

- [`src/crawl/cninfo_official_api.py`](src/crawl/cninfo_official_api.py) 中的 `_refresh_token()`、`_ensure_token()`、`_call_api()`。

---

## 4. 核心接口：`p_info3015` 公告基本信息

### 4.1 接口元信息

| 项目 | 内容 |
| ------ | ------ |
| 端点 | `http://webapi.cninfo.com.cn/api/info/p_info3015` |
| 方法 | GET / POST |
| 别名 | 公告基本信息 |
| 文档网关码 | `a0fec4cde3bf4f83821fb5a769231100` |

### 4.2 我们使用的请求参数

| 参数 | 类型 | 必填 | 我们怎么填 | 说明 |
| ------ | ------ | ------ | ------------ | ------ |
| `scode` | string | 是 | 公司 6 位股票代码，如 `600276` | 证券代码 |
| `sdate` | string | 是 | 披露年开始日，如 `20220101` | 开始查询时间 |
| `edate` | string | 是 | 披露年结束日，如 `20221231` | 结束查询时间 |
| `pageNum` | int | 是 | `1` | 页码 |
| `pageSize` | int | 是 | `100`（配置见 `cninfo_official_api.page_size`） | 每页条数 |

**注意**：API 文档支持 `page` / `pagesize`，但实测使用 `pageNum` / `pageSize` 才能正确分页。

**日期区间为什么是披露年而不是会计年度？**

- 2021 年报通常在 2022 年 3–4 月披露。
- 所以查询 2021 年报时，代码把 `year=2021` 映射为 `search_year = 2022`，区间就是 `20220101` 到 `20221231`。
- 对应代码：

```python
search_year = str(int(year) + 1)
params = {
    "scode": code,
    "sdate": f"{search_year}0101",
    "edate": f"{search_year}1231",
    ...
}
```

### 4.3 返回字段中我们用到的字段

| 返回字段 | 类型 | 含义 | 映射到 metadata.csv 的字段 |
| ---------- | ------ | ------ | ----------------------------- |
| `SECCODE` | VARCHAR | 证券代码 | `stock_code` |
| `SECNAME` | VARCHAR | 证券简称 | `stock_name` |
| `F001D` | DATE | 公告日期（披露日期） | `publish_date`（取前 10 位） |
| `F002V` | VARCHAR | 公告标题 | `announcement_title` |
| `F003V` | VARCHAR | 公告地址（PDF URL） | `url`、`pdf_url` |

其他字段如 `F004V`（公告格式）、`F005N`（公告大小）等暂不写入 metadata。

### 4.4 一个真实请求示例

请求：

```http
POST http://webapi.cninfo.com.cn/api/info/p_info3015?access_token=...
Content-Type: application/x-www-form-urlencoded

scode=600276&sdate=20220101&edate=20221231&pageNum=1&pageSize=100
```

返回片段（恒瑞医药 2021 年报）：

```json
{
  "resultcode": 200,
  "records": [
    {
      "SECCODE": "600276",
      "SECNAME": "恒瑞医药",
      "F001D": "2022-04-23 00:00:00",
      "F002V": "恒瑞医药：恒瑞医药2021年年度报告",
      "F003V": "http://static.cninfo.com.cn/finalpage/2022-04-23/1213053755.PDF"
    },
    ...
  ]
}
```

PDF 最终下载地址就是 `F003V`，由 `static.cninfo.com.cn` 静态服务器提供。

---

## 5. 从 API 返回选出“真正的年报”

一只股票在一年里会发几十甚至上百条公告。`p_info3015` 返回的是**该日期区间内所有公告**，因此必须做过滤和排序。

### 5.1 过滤规则

1. 标题中必须包含 `年度报告`。
2. 标题中必须**不包含** `摘要`（排除年报摘要）。
3. 必须有 `F003V`（PDF URL），否则无法下载。

> 为什么不直接排除“修订”“更正”？
> 实验中未发现官方 API 返回带“修订”“更正”字样的年报标题；若后续出现，可再增强过滤。

### 5.2 排序/打分规则

对通过过滤的记录，按以下优先级赋分，取最高分：

| 得分 | 条件 | 例子 |
| ------ | ------ | ------ |
| 4 | 标题完全等于 `{name}：{name}{year}年年度报告` | `恒瑞医药：恒瑞医药2021年年度报告` |
| 3 | 标题以 `{year}年年度报告` 结尾 | `片仔癀：漳州片仔癀药业股份有限公司2021年年度报告` |
| 2 | 标题中包含公司简称 | `爱尔眼科：2021年年度报告` |
| 1 | 仅包含“年度报告” | 兜底 |

代码实现：[`_select_best_candidate()`](src/crawl/cninfo_official_api.py)。

### 5.3 为什么需要“披露年 = 会计年度 + 1”

- 如果直接查 `year=2021` 的 2021 年区间，会漏掉 2022 年披露的年报。
- 如果查 2021–2023 三年全区间，可能返回多份年报，增加歧义。
- 所以代码固定：查询 `(year+1)` 全年，再选标题匹配 `year` 的那一条。

---

## 6. 生成 metadata.csv 的规则

### 6.1 metadata 15 列 Schema

```python
METADATA_COLUMNS = [
    "doc_id",              # 文档唯一标识
    "stock_code",          # 股票代码
    "stock_name",          # 公司简称
    "market",              # sh / sz / bj
    "announcement_title",  # 公告标题
    "announcement_type",   # 年度报告
    "publish_date",        # 公告披露日期
    "url",                 # 原始 URL
    "pdf_url",             # PDF 下载 URL
    "local_pdf_path",      # 本地保存路径
    "download_status",     # pending / success / failed
    "source",              # cninfo_official_api
    "crawl_time",          # 抓取时间
    "error_message",       # 错误信息
    "notes",               # 备注
]
```

完整定义见 [`src/crawl/_common.py`](src/crawl/_common.py)。

### 6.2 `market` 推断规则（与 API 无关，项目中统一约定）

| 代码前缀 | market | 交易所 |
| ---------- | -------- | -------- |
| `60*` / `688*` | `sh` | 上海证券交易所 |
| `00*` / `30*` | `sz` | 深圳证券交易所 |
| `8*` / `4*` | `bj` | 北京证券交易所 |
| 其他 | 默认 `sh` | 兜底 |

### 6.3 `doc_id` 与 PDF 文件名生成规则

官方 API crawler 使用人可读的 `doc_id`，同时作为 PDF 文件名 stem：

```python
def generate_human_doc_id(code: str, name: str, publish_date: str) -> str:
    report_year = int(str(publish_date)[:4]) - 1
    return f"{code}_{name}_{report_year}年报"
```

例如：

```
600276_恒瑞医药_2021年报
```

- 包含股票代码、公司简称、报告年度。
- 文件名与 `doc_id` 完全一致，因此 `parse`/`route`/`extract` 等通过文件名 stem 推导 `doc_id` 的阶段不会断裂。
- 经 150 条记录验证，该格式无碰撞。

> 前端 AJAX crawler 仍使用旧的哈希版 `generate_doc_id`（`{code}_{publish_date}_{title_hash}`）。这是双路线实验期间的暂时差异；若后续合并到主分支，再统一 `doc_id` 策略。

### 6.4 `local_pdf_path` 规则

```
data/pdf/{doc_id}.pdf
```

例如：

```
data/pdf/600276_恒瑞医药_2021年报.pdf
```

- 使用**相对路径**，以项目根目录为基准，便于跨平台协作。
- `download` 和 `audit` 阶段在读取时会自动把相对路径解析为绝对路径。

---

## 7. 速率控制、重试与熔断

这些不是 API 文档要求，而是项目为了保证 150 份数据稳定跑完加的策略。

### 7.1 请求间隔

配置项：

```yaml
cninfo_official_api:
  delay_seconds: 3
```

每查一家公司之间休眠 3 秒，降低被封或限流风险。

### 7.2 指数退避重试

查询单家公司失败时（网络异常、超时等），最多重试 `max_retries: 3` 次，等待时间分别为 1s、2s、4s。

### 7.3 失败熔断

配置项：

```yaml
cninfo_official_api:
  max_failure_rate: 0.15
```

当累计失败率超过 15% 时，立即抛异常停止爬虫，避免在接口大面积异常时浪费时间和流量。

### 7.4 断点续传

已处理过的 `(code, year)` 会写入 `data/crawl_cache_official.json`。重新运行时直接跳过，避免重复请求。

---

## 8. 预检（Preflight）

长任务开始前，代码会先执行 `preflight()`，验证三件事：

1. `.env` 中凭证已配置。
2. OAuth2 token 接口能正常换取 token。
3. 用一个样例请求（恒瑞医药 2023 年报区间）测试 `p_info3015` 是否返回数据。

任一失败立即报错，而不是等到跑了一堆公司才发现接口不可用。

---

## 9. 进度监控

代码向 `outputs/crawl_progress.json` 写入实时进度：

```json
{
  "backend": "official_api",
  "total": 150,
  "success": 150,
  "failed": 0,
  "status": "completed",
  "updated_at": "2026-06-14T15:53:33.415254"
}
```

同时终端显示 tqdm 进度条：

```
官方 API 年报抓取: 100%|████████| 150/150 [09:12<00:00, 3.67s/条, year=2023, ok=150, fail=0]
```

---

## 10. 附录：其他相关接口

### 10.1 `p_info3005` 公告分类信息

| 项目 | 内容 |
| ------ | ------ |
| 端点 | `http://webapi.cninfo.com.cn/api/info/p_info3005` |
| 用途 | 查询公告分类编码与名称 |
| 关键参数 | `sortcode`（分类编码）、`parentcode`（父类编码） |
| 关键返回 | `SORTCODE`、`SORTNAME`、`PARENTCODE` |

当前 crawler **没有使用**该接口，因为通过标题关键词过滤已能准确选出年报。若后续需要按分类码精确筛选，可引入该接口。

### 10.2 不可用接口

| 接口 | 用途 | 不可用原因 |
| ------ | ------ | ------------ |
| `p_info3064` | 上交所问询函 | 415 未购买包时长服务 |
| `p_info3064t` | 深交所/北交所问询函 | 415 未购买包时长服务 |
| `p_cninfo5001` | 定期报告披露事件 | 415 未购买包时长服务 |

因此问询函数据仍需通过前端 AJAX 或其他渠道获取。

---

## 11. 总结：代码为什么这么写

1. **为什么用 `POST` 而不是 `GET`**：官方文档说 GET/POST 都支持，但带 `access_token` 的 URL 较长，POST 更稳妥。
2. **为什么把 token 放 URL 参数**：实验中只有通过 `?access_token=xxx` 才能成功调用数据接口。
3. **为什么查询 `year+1` 全年**：因为年报在下一自然年披露。
4. **为什么标题打分而不是直接取第一条**：同一公司一年内会有大量公告，必须选出最匹配的年报。
5. **为什么 `doc_id` 要用人可读格式**：让 `data/pdf/` 目录对人类可浏览，同时保证文件名 stem 与 `doc_id` 一致，下游 `parse`/`route`/`extract` 无需改动。
6. **为什么 `local_pdf_path` 用相对路径**：便于跨平台运行，避免 Windows 绝对路径写死在 metadata 里。
7. **为什么有预检、熔断、进度条**：150 份数据抓取耗时数分钟，必须在早期暴露问题、避免白等。

---

## 12. 官方文档与实测补充

本节分两类记录：`12.1` 是认证接口的实测补充；`12.2` 之后是从官方 API 文档页面（`https://webapi.cninfo.com.cn/api-cloud-gateway-manage/apiDoc/info?gatewayCode=...`）抓取并整理的字段与参数说明。这样写是为了避免把“实测可用”误写成“官方文档树已收录”。

### 12.1 实测认证接口：`/api-cloud-platform/oauth2/token`

该接口未出现在 API 文档树（`cninfo_api_doc_tree.json`）中。原会话复盘显示，发现线索来自 [`haspower/cninfo_api`](https://github.com/haspower/cninfo_api)，其中使用 `client_credentials` 方式获取 token，并把 `access_token` 附加到数据端点 URL。

本项目没有把该仓库作为官方依据，也没有复制其源码。该端点的可靠性来自本项目自己的 `preflight()`、150 份年报抓取和后续下载审计验证。来源登记见 [`cninfo_external_references.md`](cninfo_external_references.md)。

**端点**

```http
POST http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token
```

**请求参数（form-data）**

| 参数 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `grant_type` | string | 是 | 固定值 `client_credentials` |
| `client_id` | string | 是 | 即 `CNINFO_ACCESS_KEY` |
| `client_secret` | string | 是 | 即 `CNINFO_ACCESS_SECRET` |

**返回字段**

| 字段 | 类型 | 说明 |
| ------ | ------ | ------ |
| `access_token` | string | 访问令牌 |
| `token_type` | string | 固定为 `bearer` |
| `expires_in` | int | 有效期秒数，通常为 3599 |

### 12.2 `p_info3015` 公告基本信息

**接口元信息**

| 项目 | 内容 |
| ------ | ------ |
| 文档网关码 | `a0fec4cde3bf4f83821fb5a769231100` |
| 接口名称 | `p_info3015` |
| 接口别名 | 公告基本信息 |
| 请求路径 | `info/p_info3015` |
| 完整端点 | `http://webapi.cninfo.com.cn/api/info/p_info3015` |
| 支持方法 | GET、POST |

**请求参数原文**

| 名称 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `scode` | string | 否 | 输入 1 个股票；`scode` 和 `edate` 同时为空时，默认返回最近 100 条记录 |
| `sdate` | string | 否 | 开始查询时间；支持 `20161101`、`2016-11-01`、`2016/11/01` |
| `edate` | string | 否 | 结束查询时间；`scode` 和 `edate` 同时为空时，默认返回最近 100 条记录；`scode` 为空且 `edate` 有值时返回单日数据 |
| `market` | string | 否 | 市场编码，例如 `012001`（沪市）、`012029`（科创板）、`012002`（深市主板）、`012015`（创业板） |
| `maxid` | int | 否 | 增量起始 ID |
| `textid` | string | 否 | 正文 ID |
| `page` | int | 否 | 页码 |
| `pagesize` | int | 否 | 每页大小 |
| `format` | string | 否 | 结果集格式：`xml`、`json`、`csv`、`dbf` |
| `@column` | string | 否 | 结果列选择，多列逗号分隔 |
| `@limit` | int | 否 | 结果条数限制 |
| `@orderby` | string | 否 | 结果集排序，例如 `id:desc`、`id:asc` |

**官方约束**

- 暂定 API 的每次返回记录数最多为 20000 条。
- 同一个类别的公告一次只能请求一天的数据（本 crawler 通过 `scode` 按股票查询，未按类别过滤，因此该限制未触发）。

**响应字段原文**

| 名称 | 类型 | 说明 |
| ------ | ------ | ------ |
| `TEXTID` | VARCHAR | 正文 ID |
| `RECID` | VARCHAR | 主体 ID |
| `SECCODE` | VARCHAR | 证券代码 |
| `SECNAME` | VARCHAR | 证券简称 |
| `F001D` | DATE | 公告日期 |
| `F002V` | VARCHAR | 公告标题 |
| `F003V` | VARCHAR | 公告地址 |
| `F004V` | VARCHAR | 公告格式 |
| `F005N` | DECIMAL | 公告大小 |
| `F006V` | VARCHAR | 信息分类 |
| `F007V` | VARCHAR | 证券类别编码 |
| `F008V` | VARCHAR | 证券类别名称 |
| `F009V` | VARCHAR | 证券市场编码 |
| `F010V` | VARCHAR | 证券市场名称 |
| `OBJECTID` | BIGINT | OBJECTID |
| `RECTIME` | DATETIME | 发布时间 |

### 12.3 `p_info3005` 公告分类信息

**接口元信息**

| 项目 | 内容 |
| ------ | ------ |
| 文档网关码 | `89f5d71e8ddd4422bb91d1e89516192b` |
| 接口名称 | `p_info3005` |
| 接口别名 | 公告分类信息 |
| 请求路径 | `info/p_info3005` |
| 完整端点 | `http://webapi.cninfo.com.cn/api/info/p_info3005` |
| 支持方法 | GET、POST |

**请求参数原文**

| 名称 | 别名 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ | ------ |
| `sortcode` | 分类编码 | string | 否 | 只能查询一个分类代码 |
| `parentcode` | 父类编码 | string | 否 | 传入父类编码可查询对应所属分类编码；顶级分类为 `01` |
| `format` | 结果集格式 | string | 否 | 可选 `xml`、`json`、`csv`、`dbf` |
| `@column` | 结果列选择 | string | 否 | 多列逗号分隔 |
| `@limit` | 结果条数限制 | int | 否 | 限制返回条数 |
| `@orderby` | 结果集排序 | string | 否 | 例如 `@orderby=id:desc` |

**响应字段原文**

| 名称 | 别名 | 类型 |
| ------ | ------ | ------ |
| `SORTCODE` | 类目编码 | VARCHAR |
| `PARENTCODE` | 父类编码 | VARCHAR |
| `SORTNAME` | 类目名称 | VARCHAR |
| `F001D` | 启用时间 | DATE |
| `F002D` | 停用时间 | DATE |

> 当前 crawler 未使用 `p_info3005`，因为通过标题关键词过滤已能准确筛选年报。保留此文档原文供后续扩展。
