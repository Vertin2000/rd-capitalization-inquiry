# CNINFO 外部参考来源登记

> 记录日期：2026-06-14
> 适用范围：巨潮 CNINFO 年报抓取、问询函/回复函抓取、官方 API 认证与前端公告查询。

本文只登记“外部来源线索”和“本项目实际采用边界”。它不替代官方文档、当前代码测试或真实运行日志。

---

## 快速结论

- `p_info3015` 年报公告接口来自巨潮官方 API 文档树，可作为官方文档依据。
- `/api-cloud-platform/oauth2/token` 认证端点没有出现在本项目导出的官方 API 文档树中；其发现线索来自 `haspower/cninfo_api`，最终可靠性来自本项目实测。
- 问询函与回复函首版使用巨潮前端公开公告查询接口 `hisAnnouncement/query`；`legeling/Annualreport_tools` 只作为请求方式、Session 重试和限速思路参考。
- 队友原始代码和外部开源项目都不能直接作为正确性证据。进入正式实现前，必须由本项目测试、小样本实证或完整运行日志确认。

---

## 来源清单

| 来源 | License / 权利状态 | 相关内容 | 本项目使用情况 | 复用边界 |
| --- | --- | --- | --- | --- |
| [`haspower/cninfo_api`](https://github.com/haspower/cninfo_api)；关键文件：[`main.py`](https://github.com/haspower/cninfo_api/blob/master/main.py) | GitHub metadata 标识为 `MPL-2.0` | `client_credentials` 获取 token；数据接口 URL 附加 `access_token` | 作为 `/api-cloud-platform/oauth2/token` 调用方式的发现线索 | 不复制源码；不归档其中示例凭证；不把它写成官方文档依据 |
| [`legeling/Annualreport_tools`](https://github.com/legeling/Annualreport_tools)；关键文件：[`1.report_link_crawler.py`](https://github.com/legeling/Annualreport_tools/blob/main/1.report_link_crawler.py) | GitHub metadata 未标识 license；未见明确 `LICENSE` 文件 | `hisAnnouncement/query`、请求头、Session、重试、分页、限速 | 作为前端公告查询工程实现参考，尤其是问询候选发现阶段 | 不复制源码；只借鉴公开接口调用模式和工程防抖思路 |
| `../temp-队友做的东西原件/` | 本地团队历史存档，不视为可信外部来源 | Week 12 年报爬虫思路、历史错误样例 | 只作为理解历史和反面排查材料 | 不能作为接口来源证据；不能直接迁移代码、Schema、Prompt 或结论 |

### 搜到但未采用的弱相关来源

| 来源 | 原因 |
| --- | --- |
| `Ryukin0/Blockchain_SupplyChain_TextMining` | 搜索中出现，但与当前 CNINFO 年报/问询抓取链路弱相关；未作为本项目实现依据 |

---

## OAuth2 Token 端点追溯

本项目年报抓取使用：

```http
POST http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token
```

该端点的来源链条应这样表述：

1. **不是官方文档树来源**：`cninfo_api_doc_tree.json` 和本地化 API catalog 中未发现该认证端点。
2. **外部线索来源**：原会话复盘显示，AI 通过 GitHub 搜索读到 `haspower/cninfo_api`，其中使用 `grant_type=client_credentials`、`client_id`、`client_secret` 获取 token，并把 `access_token` 附加到数据接口 URL。
3. **本项目验证来源**：我们用自己的 `CNINFO_ACCESS_KEY` / `CNINFO_ACCESS_SECRET` 实测获取 token，并通过 `p_info3015` 完成 150 份年报 `crawl -> download -> audit`。

因此，后续文档中应写：

> token 端点是“外部开源项目提供的线索 + 本项目实测可用”的认证方式，不是“已在官方 API 文档树中找到”的接口。

如果后续认证失败，应按以下顺序排查：

1. 账号凭证是否仍有效；
2. token 端点是否仍返回 `access_token`；
3. 数据接口是否仍接受 URL 查询参数形式的 `access_token`；
4. 官方 API 平台是否调整了认证文档或权限策略。

---

## 问询函与回复函抓取参考边界

官方 API 文档树中存在问询函相关接口线索，但当前账号访问 `p_info3064` / `p_info3064t` 返回 415，表示未购买对应服务。因此首版问询函与回复函抓取继续走公开前端公告查询：

```http
POST https://www.cninfo.com.cn/new/hisAnnouncement/query
```

`legeling/Annualreport_tools` 对本项目的价值是工程层面的：

- 使用 `requests.Session()` 保持请求上下文；
- 对 429 / 5xx 等状态码做重试；
- 分页拉取公告列表；
- 在请求之间加入等待，降低被限流概率。

本项目没有照搬其年报筛选逻辑。问询抓取的正式口径以 `SPEC.md`、`docs/crawl_spec.md` 和 `src/crawl/inquiry_crawler.py` 为准：覆盖全部 company-year，窗口为年报发布日期后 180 天，标题优先识别问询函、回复函、关注函和监管工作函。

---

## 维护规则

- 若后续新增外部仓库、博客、代码片段或接口抓包作为实现线索，必须先补到本文档，再在相关代码或文档中引用。
- 如需临时 clone 外部仓库，只能放在忽略目录，例如 `project2/.tmp/open-source-references/`；核查后删除，不进入 git。
- 文档可记录 URL、license、观察到的接口行为和本项目验证结果；不要提交第三方源码、第三方凭证、抓包原文中的敏感字段。
- 任何外部来源都必须降级为“线索”。能支撑项目结论的证据只能是官方文档、本项目代码测试、真实运行日志和人工复核结果。
