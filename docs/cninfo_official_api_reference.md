# 深证信（巨潮）官方 API 文档本地参考

> 来源：[https://webapi.cninfo.com.cn/#/apiDoc](https://webapi.cninfo.com.cn/#/apiDoc)
> 提取时间：2026-06-12T13:18:50.717487+00:00
> 全量接口数：2465
> 与研究相关接口数：608

## 1. 关键结论

- 官方 API 文档树通过前端脚本 `/js/apiDocTree.js` 暴露，整棵树已导出为 `cninfo_api_doc_tree.json`。
- 每个接口的元数据可通过公开接口 `GET /api-cloud-gateway-manage/apiDoc/info?gatewayCode=<uuid>` 获取，无需登录。
- **接口文档是公开的，但实际数据接口需要授权**。直接请求数据端点（如 `http://webapi.cninfo.com.cn/api/cninfo/p_cninfo5001`）会返回 `401 未经授权的访问`。
- 因此 crawler 重构建议采用 **Plan A**：数据仍走公开前端接口 `www.cninfo.com.cn/new/hisAnnouncement/query`，本官方文档仅用于校准参数、字段语义和输出结构。

## 2. 目录结构

| 一级类目 | 接口数 | 说明 |
|----------|--------|------|
| 公共信息 | 7 | （与研究相关） |
| 公司数据 | 274 | （与研究相关） |
| 公告资讯 | 106 | （与研究相关） |
| 知识库服务 | 28 |  |
| 证券知识库在线检索接口 | 18 |  |
| 债券 | 87 |  |
| 基金 | 32 |  |
| 指数 | 5 |  |
| ENGLISH APIS | 220 |  |
| 深证信量化数据服务 | 26 |  |
| 新闻研报 | 9 | （与研究相关） |
| 工商大数据 | 46 |  |
| 拟上市公司数据 | 17 |  |
| 深证信专题数据服务 | 83 |  |
| 深证信金融科技专区 | 2 |  |
| ESG专题数据 | 5 |  |
| TTM | 10 |  |
| 指数样本 | 1 |  |
| 海外数据 | 749 |  |
| 宏观数据 | 67 |  |
| 证券提示库数据服务 | 12 | （与研究相关） |
| 深证信VIP数据服务 | 27 |  |
| 深证信专业订制数据 | 58 |  |
| 数据浏览器 | 27 |  |
| 专题统计 | 76 |  |
| 内部服务-服务平台接口 | 242 |  |
| 巨潮网使用接口 | 200 | （与研究相关） |
| 第三方数据 | 7 |  |
| 小巨人 | 3 |  |
| 产业链数据服务 | 4 |  |
| 上市公司官网嵌入服务 | 17 |  |

## 3. 与研究相关的重点类目

### 3.1 公司数据（274 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_company3201` | 股票背景资料 | `stock/p_company3201` | `ab1e8e280a9d4045a6885b259b3dfe01` |
| `p_public0004` | 板块成份股数据 | `stock/p_public0004` | `9ab168b31df84d8e98076bef67073537` |
| `p_stock0004` | 股票所属板块 | `stock/p_stock0004` | `f77d3bb0dd724bbe8b3d8459ed32e79a` |
| `p_stock2100` | 公司基本信息 | `stock/p_stock2100` | `f712909f097f4dfcb62ec69006439ac6` |
| `p_stock2101` | 股票基本信息 | `stock/p_stock2101` | `337da212118b47b2b3cecda598d4ac43` |
| `p_stock2102` | 公司管理人员任职情况 | `stock/p_stock2102` | `4162a2c365be421b906fc7e8aa33c307` |
| `p_stock2108` | 机构基本信息变更情况 | `stock/p_stock2108` | `b98805acb3404598834d513940851eba` |
| `p_stock2109` | 证券简称变更情况 | `stock/p_stock2109` | `c35b6f12399b4b03b34b2b9001ef1896` |
| `p_stock2110` | 上市公司行业归属的变动情况 | `stock/p_stock2110` | `ae97ed4ddce54d87ab10d038d9b1640a` |
| `p_stock2117` | 公司上市状态变动情况表 | `stock/p_stock2117` | `9573d5af2b7d465dbdf0c355abeff0c3` |
| `p_ods3302` | 公司主要行业收入数据 | `stock/p_ods3302` | `73d88cc4b67a49d49e61454f63fa53e3` |
| `p_stock2237` | 定期报告预披露时间 | `stock/p_stock2237` | `9f7e8fe1ad404dffab2003dbaa12bcd6` |
| `p_stock2238` | 上市公司业绩预告 | `stock/p_stock2238` | `97c2b582835244c1bdafc704c8fc9408` |
| `p_stock2239` | 定期报告审计意见 | `stock/p_stock2239` | `734d284aed754ab186cfdc00374ceecd` |
| `p_stock2300` | 个股报告期资产负债表 | `stock/p_stock2300` | `5474f0bfcc0a497197b3fe9cdf37befb` |
| `p_stock2301` | 个股报告期利润表 | `stock/p_stock2301` | `0838f71fe00e4d00bb4d9a8d45df8472` |
| `p_stock2302` | 个股报告期现金表 | `stock/p_stock2302` | `dff987d3d00e4c62afeb042bb3f6a84b` |
| `p_stock2303` | 个股报告期指标表 | `stock/p_stock2303` | `87701f2530ae482ab2a999dae0dde022` |
| `p_stock2325` | 金融类资产负债表2007版 | `stock/p_stock2325` | `e0ad51bd4c2743ce88ef0932503e51e9` |
| `p_stock2326` | 金融类利润表2007版 | `stock/p_stock2326` | `e8945e68ef5247f8ba51b58151407cef` |
| `p_stock2327` | 金融类现金流量表2007版 | `stock/p_stock2327` | `c77eaa699e2b42dcb2889c55dfdc554c` |
| `p_stock2328` | 业绩快报 | `stock/p_stock2328` | `7ab8b9987e3e45789fb3426dcdcfd5b9` |
| `p_stock2387` | 个股指标快速版 | `stock/p_stock2387` | `260ba5c84d6c4f778c82aa2d1da820c9` |
| `p_stock2399` | 沪深股票最新的财务报告日期 | `stock/p_stock2399` | `07dd101c94ee46088ab1acc0afb03201` |
| `p_rzrq3104` |  融资融券明细数据 | `stock/p_rzrq3104` | `6e9e5d07f7dc42e1a69dae2ce82da33f` |
| `p_rzrq3106` | 单一股票质押比例 | `stock/p_rzrq3106` | `fe029a72e7fc4b5da736a62e8b7de0ec` |
| `p_stock2202` | 证券交易特别提示 | `stock/p_stock2202` | `f968156887bd46319d98a31b93c25d4a` |
| `p_stock2204` | 沪深异动证券公开信息 | `stock/p_stock2204` | `7958c463073c4f8da684e43b8d1bc60c` |
| `p_stock2401` | 股票最新日行情 | `stock/p_stock2401` | `f16b697db4724bc69f972fa291d03d12` |
| `p_stock2402` | 股票历史日行情 | `stock/p_stock2402` | `c3c41c16bf0f420e863fdad34b0d6648` |
| `p_stock2406` | 证券复权因子 | `stock/p_stock2406` | `19affbd27dc94fe1be8fe356a1579f66` |
| `p_stock2416` | 大宗交易数据 | `stock/p_stock2416` | `4cb90e94909f489592f4ab9e201bac62` |
| `p_stock2426` | 多市场交易日报 | `stock/p_stock2426` | `b51f2add2fc140158d820a36c8ddabd6` |
| `p_stock2107` | 公司员工情况表 | `stock/p_stock2107` | `61b83bdd6b6749ac8b50f97b86aacc2e` |
| `p_stock2209` | 十大流通股东持股情况 | `stock/p_stock2209` | `8ba9ce1601b74276abbaaefbc9307c6d` |
| `p_stock2210` | 十大股东持股情况 | `stock/p_stock2210` | `c4715e41b04d42d4a5f96c64b0700bd4` |
| `p_stock2211` | 公司股东人数 | `stock/p_stock2211` | `b9539e5d54944c969621d60bf5921b0c` |
| `p_stock2212` | 股东持股集中度 | `stock/p_stock2212` | `348fa111fe01473e97cf84a6528c5001` |
| `p_stock2213` | 公司股东实际控制人 | `stock/p_stock2213` | `b2555f4def9447d28a60f61766935877` |
| `p_stock2215` | 公司股本变动 | `stock/p_stock2215` | `1a4ac5994044470a9759d3675f9ac372` |
| `p_stock2217` | 主要股东持股变化 | `stock/p_stock2217` | `fe617cd78ec0487f91e79a8aefee4de6` |
| `p_stock2218` | 上市公司高管持股变动 | `stock/p_stock2218` | `fd626eec701c40fe90f79c63add6325f` |
| `p_stock2219` | 公司股东股份冻结 | `stock/p_stock2219` | `2a15324ddd634d7f8baea60a0f3c7bb3` |
| `p_stock2220` | 公司股东股份质押 | `stock/p_stock2220` | `9f91bd4f952f4f86ba0a1e72b4256c79` |
| `p_stock2226` | 股东增（减）持情况 | `stock/p_stock2226` | `9000cd76f0d640b9ba8cb79eb90748a0` |
| `p_stock2227` | 受限股份实际解禁日期 | `stock/p_stock2227` | `3b669b640d0d40cc8b6ac9d66466ecbe` |
| `p_stock2228` | 受限股份预计解禁日期表 | `stock/p_stock2228` | `ccd0ef43841a4336b41368278fecdadd` |
| `p_stock2268` | 境外投资者持股变化表 | `stock/p_stock2268` | `e0039a3e669b437698d1a2f3584062f4` |
| `p_stock2222` | 股东大会召开情况 | `stock/p_stock2222` | `9afafd22fb6044a5af05506fe67d1d1f` |
| `p_stock2223` | 股东大会议案 | `stock/p_stock2223` | `29d6a4172d274db69f4267b87931738c` |
| `p_stock2224` | 股东大会相关事项变动 | `stock/p_stock2224` | `e5a75dbe084a4bf8a44a00e6d813a505` |
| `p_stock2245` | 对外担保 | `stock/p_stock2245` | `69c376374137446e9e8ec046bc8b52ca` |
| `p_stock2246` | 公司诉讼 | `stock/p_stock2246` | `deb2a395fede4fdea309f8d4d70b48b9` |
| `p_stock2248` | 公司受处罚表 | `stock/p_stock2248` | `d65cb2deaf6049a4a4ca98ba474f3d3b` |
| `p_stock2249` | 公司资产冻结表 | `stock/p_stock2249` | `8ee3bcd6855b4cf9b6a084c52cb76647` |
| `p_stock2250` | 公司仲裁 | `stock/p_stock2250` | `75161e27e03347df97d7732d2bfdc22a` |
| `p_stock2201` | 分红转增信息 | `stock/p_stock2201` | `c415950bd0dd416f8853d1b2097825bc` |
| `p_stock2229` | 公司增发股票预案 | `stock/p_stock2229` | `f47f4d5304b34d77b10a843685282bcc` |
| `p_stock2230` | 公司增发股票实施方案 | `stock/p_stock2230` | `28e105950c7d4d8bb4ef9679a525c06a` |
| `p_stock2231` | 公司配股预案 | `stock/p_stock2231` | `ac6ecb8efb7b4101ac1f3a69cef50252` |
| `p_stock2232` | 公司配股实施方案 | `stock/p_stock2232` | `71a7162a7ebe434c81ef0c45c8c60240` |
| `p_stock2233` | 公司首发股票 | `stock/p_stock2233` | `012c8b73e1a4420b853c494ffb78b4ce` |
| `p_stock2234` | 募集资金来源 | `stock/p_stock2234` | `cc8c3efa394949ebbc2c0e596175d35b` |
| `p_stock2235` | 股票发行中介机构及承销情况 | `stock/p_stock2235` | `62097ff3b6174b7799e59c03605cf498` |
| `p_stock2236` | 募集资金投资项目计划 | `stock/p_stock2236` | `6127230e36604142833d86f114c3dcfa` |
| `p_stock2247` | 公司首发股票审核信息表 | `stock/p_stock2247` | `b02066746431496da4d7f4ccc24d5f9d` |
| `p_stock2262` | 新股过会情况表 | `stock/p_stock2262` | `4b825b8dcf40492a94028f14ce00c1cd` |
| `p_stock2263` | 优先股派息表 | `stock/p_stock2263` | `77be88dc924e4102a4aa65334c953a5c` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3015` | 公告基本信息 | `info/p_info3015` | `a0fec4cde3bf4f83821fb5a769231100` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_sub_latest_status` | 接口最新更新状态 | `load/p_sub_latest_status` | `8976a5662c5a4d6eb61b225cabe765d4` |
| `p_stock2100_inc` | 公司基本信息 | `load/p_stock2100_inc` | `7e33330155c1477d80b9a10ccb9d3d6e` |
| `p_stock2101_inc` | 股票基本信息 | `load/p_stock2101_inc` | `e5ed155b084b48f19995537f4c95bd89` |
| `p_stock2102_inc` | 公司管理人员任职情况 | `load/p_stock2102_inc` | `63c700e98cb84d8eb01461190229af64` |
| `p_stock2107_inc` | 公司员工情况表 | `load/p_stock2107_inc` | `cc7d367dcf054e789512516f8519644e` |
| `p_stock2108_inc` | 机构基本信息变更情况 | `load/p_stock2108_inc` | `474f9487dff44d6dbddda141c1e905c1` |
| `p_stock2109_inc` | 证券简称变更情况 | `load/p_stock2109_inc` | `b7018c59fc3445d493669cd5e2115c77` |
| `p_stock2110_inc` | 上市公司行业归属的变动情况 | `load/p_stock2110_inc` | `5988bbaf78294be2868b572623765499` |
| `p_stock2117_inc` | 公司上市状态变动情况表 | `load/p_stock2117_inc` | `b31b833b27b34bee84ec9fda59565cb2` |
| `p_stock2237_inc` | 定期报告预披露时间 | `load/p_stock2237_inc` | `39ad0f3bf1e342afbfb395617fc2dc15` |
| `p_stock2238_inc` | 上市公司业绩预告 | `load/p_stock2238_inc` | `efe7d8a52a55412dbf58973715a76d9a` |
| `p_stock2239_inc` | 定期报告审计意见 | `load/p_stock2239_inc` | `01f4a98dc47047d18d10b788882762f0` |
| `p_stock2300_inc` | 个股报告期资产负债表 | `load/p_stock2300_inc` | `89c3c103d1904a5ab32a26ecf9938c16` |
| `p_stock2301_inc` | 个股报告期利润表 | `load/p_stock2301_inc` | `eddecf2656194bd9a5f4b792f369af7a` |
| `p_stock2302_inc` | 个股报告期现金表 | `load/p_stock2302_inc` | `3f15e07dbd5a4aa5b7c6a847de76688a` |
| `p_stock2303_inc` | 个股报告期指标表 | `load/p_stock2303_inc` | `e2d9bf7db58a498487e47a4a5354c018` |
| `p_stock2325_inc` | 金融类资产负债表2007版 | `load/p_stock2325_inc` | `ddb05d3a663b46e7a7ae6f8e2751f921` |
| `p_stock2326_inc` | 金融类利润表2007版 | `load/p_stock2326_inc` | `7a24d604398044b7806aef6042bcaf41` |
| `p_stock2327_inc` | 金融类现金流量表2007版 | `load/p_stock2327_inc` | `ac854fa338c8434eaa76f68938851c46` |
| `p_stock2328_inc` | 业绩快报 | `load/p_stock2328_inc` | `5095eff6ec1e4685b98d5e298cac9107` |
| `p_stock2202_inc` | 证券交易特别提示 | `load/p_stock2202_inc` | `696dfef0eb234f2bb69f9281dfbc8e76` |
| `p_stock2204_inc` | 沪深异动证券公开信息 | `load/p_stock2204_inc` | `4f01bfdabb1b4bdf96093e4963bd183f` |
| `p_stock2401_inc` | 股票最新日行情 | `load/p_stock2401_inc` | `d8c818f61e914321973602788a14796f` |
| `p_stock2402_inc` | 股票历史日行情 | `load/p_stock2402_inc` | `c0fdfe80ea644bcebdd11e3c4c78c7c5` |
| `p_stock2406_inc` | 证券复权因子 | `load/p_stock2406_inc` | `83c13a379e6b47969f46871da7c282df` |
| `p_stock2209_inc` | 十大流通股东持股情况 | `load/p_stock2209_inc` | `fadfc22a8c8c4f519988fd1c1c8033eb` |
| `p_stock2210_inc` | 十大股东持股情况 | `load/p_stock2210_inc` | `c824571d25c7482bbb3f5e1a7e531bb7` |
| `p_stock2211_inc` | 公司股东人数 | `load/p_stock2211_inc` | `f98bc39140814fdc9f01e64a1886a024` |
| `p_stock2213_inc` | 公司股东实际控制人 | `load/p_stock2213_inc` | `6f85ee3368184c27b0f4a78d1c67aaf2` |
| `p_stock2215_inc` | 公司股本变动 | `load/p_stock2215_inc` | `ce6ea40eeccb47f5a462f110a69367a5` |
| `p_stock2218_inc` | 上市公司高管持股变动 | `load/p_stock2218_inc` | `668a5e2faa6f4948ae1e445d5b92780a` |
| `p_stock2219_inc` | 公司股东股份冻结 | `load/p_stock2219_inc` | `cb0d60377f6142669276ceb8267cf9ed` |
| `p_stock2220_inc` | 公司股东股份质押 | `load/p_stock2220_inc` | `ed53f811f1d940b1982f4fe8bebc910c` |
| `p_stock2226_inc` | 股东增（减）持情况 | `load/p_stock2226_inc` | `9fbc3a53d16a45cfac72d4b2b8e86431` |
| `p_stock2227_inc` | 受限股份实际解禁日期 | `load/p_stock2227_inc` | `5183c1b497be4849a7f0501d48f5674b` |
| `p_stock2228_inc` | 受限股份预计解禁日期表 | `load/p_stock2228_inc` | `8dc761f08ea4493aa3ee0ac6dc0e0ad0` |
| `p_stock2240_inc` | 上市公司股东变动汇总表 | `load/p_stock2240_inc` | `4eefcaf0892e41498a27fed54cee630d` |
| `p_stock2268_inc` | 境外投资者持股变化表 | `load/p_stock2268_inc` | `363ad494b4024858813ec5e41943385a` |
| `p_stock2222_inc` | 股东大会召开情况 | `load/p_stock2222_inc` | `ed05dd045c224683859ed2b69414e837` |
| `p_stock2223_inc` | 股东大会议案 | `load/p_stock2223_inc` | `021699a888ac40e180a514fa5fa514d4` |
| `p_stock2224_inc` | 股东大会相关事项变动 | `load/p_stock2224_inc` | `b08fb71abba14c9281f726165de7d64f` |
| `p_stock2245_inc` | 对外担保 | `load/p_stock2245_inc` | `ba2018662069440fb663889ccb04c044` |
| `p_stock2246_inc` | 公司诉讼 | `load/p_stock2246_inc` | `ec336c16fadb43c1922bb05014f2cd39` |
| `p_stock2248_inc` | 公司受处罚表 | `load/p_stock2248_inc` | `4397edd3f2394dc09080e1e10ec3e322` |
| `p_stock2249_inc` | 公司资产冻结表 | `load/p_stock2249_inc` | `8f5fd23e8f3f484b8ebd6179d5e4ecd2` |
| `p_stock2250_inc` | 公司仲裁 | `load/p_stock2250_inc` | `7734877116bf4c1eaa86b7ab8cfc83c1` |
| `p_stock2201_inc` | 分红转增信息 | `load/p_stock2201_inc` | `60dd83d9aa264f658f05f806611c9aca` |
| `p_stock2229_inc` | 公司增发股票预案 | `load/p_stock2229_inc` | `be3c9d3f13284c3aa5c5ac355a796406` |
| `p_stock2230_inc` | 公司增发股票实施方案 | `load/p_stock2230_inc` | `360c8dddb24a4f1583588e9203cd5fb9` |
| `p_stock2231_inc` | 公司配股预案 | `load/p_stock2231_inc` | `74c2e1ba04a84cf9a8e67b168dd05b9f` |
| `p_stock2232_inc` | 公司配股实施方案 | `load/p_stock2232_inc` | `70c3e887fcc8412e97450a7609776346` |
| `p_stock2233_inc` | 公司首发股票 | `load/p_stock2233_inc` | `4e7a68b3585f491f8a63dee2d0452db2` |
| `p_stock2234_inc` | 募集资金来源 | `load/p_stock2234_inc` | `4e8d645bc7554753bccb0aeda0d9c61b` |
| `p_stock2235_inc` | 股票发行中介机构及承销情况 | `load/p_stock2235_inc` | `9bb0788bcfd2456bbd89010951284d39` |
| `p_stock2236_inc` | 募集资金投资项目计划 | `load/p_stock2236_inc` | `c5ca7f2ed832493eb1be74d9a08d8e80` |
| `p_stock2247_inc` | 公司首发股票审核信息表 | `load/p_stock2247_inc` | `f396a97d84c14b18b1436c21e5f17441` |
| `p_stock2262_inc` | 新股过会情况表 | `load/p_stock2262_inc` | `4e6c8abb60184fdf877e4445b43a1072` |
| `p_stock2263_inc` | 优先股派息表 | `load/p_stock2263_inc` | `837fa542e3224eec988c7ebbb07bc3ee` |
| `p_stock2241_inc` | 公司资产重组概况 | `load/p_stock2241_inc` | `e9a06dacf36b4f4c8024447391c0aab1` |
| `p_stock2242_inc` | 公司债务重组 | `load/p_stock2242_inc` | `fa5b6531393743acb7171540e2a5ab08` |
| `p_stock2243_inc` | 公司吸收合并 | `load/p_stock2243_inc` | `a295b39dc7b0487ea90752dc08631641` |
| `p_stock2244_inc` | 上市公司股权被转让变更的情况 | `load/p_stock2244_inc` | `a77cd0358243488486fd961edea5f17f` |
| `p_stock2251_inc` | 公司产品出让表 | `load/p_stock2251_inc` | `a39a6c75677c4baa9b83a876cf33f286` |
| `p_stock2252_inc` | 公司资产收购表 | `load/p_stock2252_inc` | `430ab7699cca4ab1ada9d6daf1872f8b` |
| `p_stock2253_inc` | 公司资产置换表 | `load/p_stock2253_inc` | `58edaa58332b414a985d4c90a6f42aa9` |
| `p_stock2254_inc` | 并购重组基本信息表 | `load/p_stock2254_inc` | `6ca2a9ac2b02448ea7401661cee508aa` |
| `p_stock2255_inc` | 并购重组标的表 | `load/p_stock2255_inc` | `bc6ae537d7354f679c4f870221db2dbf` |
| `p_stock2256_inc` | 并购重组标的公司财务指标表 | `load/p_stock2256_inc` | `8052cd9d6d014154aec7f97443599dca` |
| `p_stock2257_inc` | 并购重组交易对手情况表 | `load/p_stock2257_inc` | `965546bcca8e455a9309fb43e68e0e76` |
| `p_stock2258_inc` | 并购重组客户供应商情况表 | `load/p_stock2258_inc` | `43798876d16748bc9ea3ae31aac3f563` |
| `p_stock2336` | 主营业务收入行业分布 | `stock/p_stock2336` | `bfc3a2230b6e4123b040b1c1de2d975a` |
| `p_stock2337` | 非经常性损益表 | `stock/p_stock2337` | `b3aebaabb46344a8a04e3fc819c459f6` |
| `p_stock2338` | 应收账款 | `stock/p_stock2338` | `c14b8212f2de4f479a2c7a8013d8f4a0` |
| `p_stock2339` | 其它应收账款 | `stock/p_stock2339` | `d6cb123e2fd34c1996cc187a1c4b0995` |
| `p_stock2340` | 其他应收款前五名 | `stock/p_stock2340` | `6206af5730574ffc84de1cc0bc19c97b` |
| `p_stock2341` | 应交税费 | `stock/p_stock2341` | `a6fdae8c4f7f4c1b96039dc39538786e` |
| `p_stock2342` | 应付股利 | `stock/p_stock2342` | `adfd30509f2d4b72bd611437745e7361` |
| `p_stock2343` | 应收账款前五名 | `stock/p_stock2343` | `e8f88b3d21b34d25a67467c1d593ae6b` |
| `p_stock2344` | 税金及附加 | `stock/p_stock2344` | `4d2e6fab3c39478391c4a27abb5667a2` |
| `p_stock2345` | 财务费用 | `stock/p_stock2345` | `dd184c16cae04dcea613282ca38ca813` |
| `p_stock2346` | 货币资金 | `stock/p_stock2346` | `8dc77d01b0654527ad9bd83f1624a128` |
| `p_stock2347` | 资产减值损失 | `stock/p_stock2347` | `9a177e00e8464c9d81d10482afbda2c6` |
| `p_stock2349` | 预付款项 | `stock/p_stock2349` | `a6d2dedfea1043899fb37e97ceab411b` |
| `p_stock2350` | 预付款项前五名 | `stock/p_stock2350` | `9bd387df154d401bbccb998a3c64d674` |
| `p_stock2351` | 存货 | `stock/p_stock2351` | `0351794b67bf419cb050e6535e30be50` |
| `p_stock2352` | 主营业务收入分产品数据 | `stock/p_stock2352` | `9c9f16ef6c044108ae7ac97f4d482049` |
| `p_stock2368` | 主营业务收入地区分布 | `stock/p_stock2368` | `bab58e144c1b41ee8d326b41d4c5be72` |
| `p_stock2336_inc` | 主营业务收入行业分布 | `load/p_stock2336_inc` | `b1ba31565c9b42ed82db8f530775a44a` |
| `p_stock2337_inc` | 非经常性损益表 | `load/p_stock2337_inc` | `1a8d3850a6c64aeebd91e74201e51106` |
| `p_stock2338_inc` | 应收账款 | `load/p_stock2338_inc` | `40ba4aa9db9e42e6a47c57053a4804f4` |
| `p_stock2339_inc` | 其它应收账款 | `load/p_stock2339_inc` | `5362c50b736b4c9998a1ecc058c05384` |
| `p_stock2340_inc` | 其他应收款前五名 | `load/p_stock2340_inc` | `d2af196b6d204765811f1460abef0f2b` |
| `p_stock2341_inc` | 应交税费 | `load/p_stock2341_inc` | `6e64acf30a9d4b23ba64d07084f433b2` |
| `p_stock2342_inc` | 应付股利 | `load/p_stock2342_inc` | `7120b707f6e541cc890cfdfc5b2aeec3` |
| `p_stock2343_inc` | 应收账款前五名 | `load/p_stock2343_inc` | `8a19bea71a5b446ea109e67679bc0cbe` |
| `p_stock2344_inc` | 税金及附加 | `load/p_stock2344_inc` | `7050a94335f245d184d8bec0883b4de7` |
| `p_stock2345_inc` | 财务费用 | `load/p_stock2345_inc` | `70d0070471f84e39a0faed0c263fbc38` |
| `p_stock2346_inc` | 货币资金 | `load/p_stock2346_inc` | `6fb9967d9d7041e4a06b3df57d7f67da` |
| `p_stock2347_inc` | 资产减值损失 | `load/p_stock2347_inc` | `7badcdf85a4b421da01b2d83eec5e36a` |
| `p_stock2349_inc` | 预付款项 | `load/p_stock2349_inc` | `958168b31e7c465fb35d43cb72a5e02e` |
| `p_stock2350_inc` | 预付款项前五名 | `load/p_stock2350_inc` | `baf06d7aa8c94463aa5f32a3d785eb80` |
| `p_stock2351_inc` | 存货 | `load/p_stock2351_inc` | `7a485830171d48c084aa90e8aa79a254` |
| `p_stock2352_inc` | 主营业务收入分产品数据 | `load/p_stock2352_inc` | `941c18f9d5e048989ef29aedd816435a` |
| `p_sub_latest_status` | 接口最新更新状态 | `load/p_sub_latest_status` | `8976a5662c5a4d6eb61b225cabe765d4` |
| `p_neeq6002` | 新三板机构信息表 | `neeq/p_neeq6002` | `ace58c1ee1a04a24a3729e9785bb9f1b` |
| `p_neeq6003` | 新三板证券信息表 | `neeq/p_neeq6003` | `727d591433e547ea8739cbdb072fd5b7` |
| `p_neeq6004` | 新三板机构基本信息变更表 | `neeq/p_neeq6004` | `34a2fb3664144a809bbdcd73d2dbaa27` |
| `p_neeq6005` | 新三板证券简称变更 | `neeq/p_neeq6005` | `b8127c9671ee410798f18e65003d406f` |
| `p_neeq6006` | 新三板公司挂牌状态表 | `neeq/p_neeq6006` | `34b212184e2f4b878c92fbc31265bcd4` |
| `p_neeq6007` | 新三板公司中介机构 | `neeq/p_neeq6007` | `c4193a143e9e4fed9f0839c62d1370db` |
| `p_neeq6008` | 新三板公司所属地区 | `neeq/p_neeq6008` | `1a6d06c6c9f7450bbd9ac76a27fb5f7c` |
| `p_neeq6009` | 新三板公司所属行业表 | `neeq/p_neeq6009` | `c4c035bf249c4fdbbf8f9dc30e7d18ea` |
| `p_neeq6011` | 新三板公司管理人员任职情况 | `neeq/p_neeq6011` | `22ab5426d0e64bd3a346a964b628ddaa` |
| `p_neeq6012` | 新三板公司员工情况 | `neeq/p_neeq6012` | `efbca71eeacf493da74e25433b52c838` |
| `p_neeq6010` | 新三板公司股本变动表 | `neeq/p_neeq6010` | `e985ec79b9d14d2ca1dade597867ac6d` |
| `p_neeq6013` | 新三板公司十大股东表 | `neeq/p_neeq6013` | `1108eda012294889bd27833f6249437d` |
| `p_neeq6026` | 新三板公司股东人数 | `neeq/p_neeq6026` | `ffa625ff85aa44399ee308a48de0c172` |
| `p_neeq6014` | 新三板公司分红转增 | `neeq/p_neeq6014` | `d3fd168769124505ae42deaf7864785d` |
| `p_neeq6016` | 新三板公司股东大会召开情况 | `neeq/p_neeq6016` | `8fa75138f2f54fd5844768db181746e8` |
| `p_neeq6022` | 新三板公司股东大会议案表 | `neeq/p_neeq6022` | `c7a5620fb0e64b37908764a4f9c21a9e` |
| `p_neeq6023` | 新三板公司受限股份实际解禁日期表 | `neeq/p_neeq6023` | `fe8a1a1cec0144f39680a7ea1267c2ca` |
| `p_neeq6024` | 新三板公司增发股票预案表 | `neeq/p_neeq6024` | `a002bed3cf1d4625aab624899a650ad6` |
| `p_neeq6025` | 新三板公司增发股票实施方案 | `neeq/p_neeq6025` | `11be447254d24f02a45301239555b116` |
| `p_neeq6028` | 新三板股份报价日行情信息 | `neeq/p_neeq6028` | `98c49db2f12447dd99615883b562a2de` |
| `p_neeq6015` | 新三板公司定期报告审计意见 | `neeq/p_neeq6015` | `854b726e977c4f479f4a13345119b410` |
| `p_neeq6017` | 新三板公司通用主要财务指标 | `neeq/p_neeq6017` | `4042fe32eeff49d2a011eea7351f711e` |
| `p_neeq6018` | 新三板公司通用资产负债表 | `neeq/p_neeq6018` | `aea1337f05bd446e84af166a2197188d` |
| `p_neeq6019` | 新三板公司通用利润表 | `neeq/p_neeq6019` | `453eed44893c4ed7a94426f93b8cba88` |
| `p_neeq6020` | 新三板公司通用现金流量表及补充资料表 | `neeq/p_neeq6020` | `6f6ecbf51c2447e5b8b94c74d5b0f640` |
| `p_neeq6021` | 新三版财务衍生指标数据 | `neeq/p_neeq6021` | `9622a5fe38b34832ad92204bd94fab7b` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3014` | 新三板公告信息 | `info/p_info3014` | `64dab2ef2f95445dad641bd63d025c5b` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_public0002` | 行业分类数据 | `stock/p_public0002` | `04add00012fc4101bb2e2303b314a6d7` |
| `p_public0003` | 地区分类数据 | `stock/p_public0003` | `361a41a0ce5146db9f5675e2a7d2e371` |
| `p_public0006` | 公共编码数据 | `public/p_public0006` | `577bb53e77984aa9b92c3f843013a39d` |
| `p_neeq6015_inc` | 新三板公司定期报告审计意见 | `load/p_neeq6015_inc` | `b1c9b55482bb45218f924cf22bba9375` |
| `p_neeq6017_inc` | 新三板公司通用主要财务指标 | `load/p_neeq6017_inc` | `c2be8b6d317f4003bfd143f9c6bab0e7` |
| `p_neeq6018_inc` | 新三板公司通用资产负债表 | `load/p_neeq6018_inc` | `1c08487df93e4e0280f17566255e6579` |
| `p_neeq6019_inc` | 新三板公司通用利润表 | `load/p_neeq6019_inc` | `f7335d8df95d41fd9e47de136ca13c31` |
| `p_neeq6020_inc` | 新三板公司通用现金流量表及补充资料表 | `load/p_neeq6020_inc` | `d1e78186eefd41868fa07cc143f35183` |
| `p_neeq6021_inc` | 新三版财务衍生指标数据 | `load/p_neeq6021_inc` | `3eb654321ae942db951f2bae60f6e3b8` |
| `p_hk4001` | 港股公司概况 | `hk/p_hk4001` | `67b27bc83ca94f2aa773fc1c878b6935` |
| `p_hk4009` | 港股董事及高级管理人员简历 | `hk/p_hk4009` | `3234db6f51954ef9a449598ad2de7f6d` |
| `p_hk4010` | 主要股东股权变动 | `hk/p_hk4010` | `e448ebbd35e04caeb7e379dc49fbc1bc` |
| `p_hk4011` | 董事任职变动 | `hk/p_hk4011` | `c6fef91e428049c0a8fa8808b100c57f` |
| `p_hk4039` | 港股证券信息表 | `hk/p_hk4039` | `65c7f0b440464741aecd8366ca4c45d3` |
| `p_hk4042` | 股东持股资料表 | `hk/p_hk4042` | `134e707c7fff4950ae4a8225fd28b64d` |
| `p_hk4043` | 高管持股变动表 | `hk/p_hk4043` | `0e7f169d21754656ac0d67869fc7422b` |
| `p_hk4045` | 港股股本表 | `hk/p_hk4045` | `0cd0027a859e4584aff0d79d8da234e6` |
| `p_hk4049` | 港股市值指标 | `hk/p_hk4049` | `4263490ce1ab45f9b7f37ef4ce72e736` |
| `p_hk4008` | 港股业绩公布预告 | `hk/p_hk4008` | `35073701934d43a1914ef25bf94cdc7f` |
| `p_hk4019` | 现金流量表(通用) | `hk/p_hk4019` | `5ad4b4b0ff59409982311aa3ea86e90b` |
| `p_hk4020` | 资产负债表(银行) | `hk/p_hk4020` | `344b5a045cb24e0b9276b1f973b85625` |
| `p_hk4021` | 综合损益表(银行) | `hk/p_hk4021` | `fcf776ed9b6b48b19d96097853b31daf` |
| `p_hk4022` | 重要指标表（银行） | `hk/p_hk4022` | `3835146015a34d6598a7c3e1cde8804d` |
| `p_hk4023` | 资产负债表(非银行) | `hk/p_hk4023` | `1b53fca9f8b04e1c847d0b679a3563b0` |
| `p_hk4024` | 综合损益表(非银行) | `hk/p_hk4024` | `6de15be9f2244a1a888ce1707de964c6` |
| `p_hk4025` | 重要指标表（非银行） | `hk/p_hk4025` | `18db744911e74cdb9ef8e1130e06c8b5` |
| `p_hk4026` | 香港股票行情日报 | `hk/p_hk4026` | `eef452767ac44d90932d677a6c56caf6` |
| `p_hk4027` | 香港股票行情周报 | `hk/p_hk4027` | `38e9b1f8f0bb41059b83d7bad81e4885` |
| `p_hk4028` | 香港股票行情月报 | `hk/p_hk4028` | `741e73aa7de94d50ae6d904127022582` |
| `p_hk4029` | 香港股票行情季报 | `hk/p_hk4029` | `3ad88628bb7c4f2486491550daf3b9f4` |
| `p_hk4030` | 香港股票行情年报 | `hk/p_hk4030` | `560043c741244e61bf79d0dda1e50a3d` |
| `p_hk4031` | 香港股票行业市场表现日报 | `hk/p_hk4031` | `da78c0729beb46879b8e7869b54cbe1b` |
| `p_hk4032` | 香港股票行业市场表现周报 | `hk/p_hk4032` | `2e5b3dd66b194d8d940dd8e1c9b4b0aa` |
| `p_hk4033` | 香港股票行业市场表现月报 | `hk/p_hk4033` | `118fce87c64c4ab68d9c520338608d49` |
| `p_hk4034` | 香港股票行业市场表现季报 | `hk/p_hk4034` | `b467c462f8384d4ea5a121c8df95fe8d` |
| `p_hk4035` | 香港股票行业市场表现年报 | `hk/p_hk4035` | `ffe32a711be7448fb7766308ab6c938e` |
| `p_hk4051` | 香港股票行情日报(调整前) | `hk/p_hk4051` | `c528ae791b7b49f8af58711a9d1ad9d7` |
| `p_hk4015` | 香港新股发行参与各方表 | `hk/p_hk4015` | `fb4741a224f64757ac2a761a32f3e4bc` |
| `p_hk4017` | 港股股本表 | `hk/p_hk4017` | `d761cdfae4b442a4ab746b2a657fe191` |
| `p_hk4018` | 分红派息表 | `hk/p_hk4018` | `a0097b7038ed43ffa453a4dc8f25e7b1` |
| `p_hk4002` | 港股业务回顾 | `hk/p_hk4002` | `b19c3402ee5448d9b504248e3121572f` |
| `p_hk4003` | 港股业务展望 | `hk/p_hk4003` | `da4a818c3c834ef5871f310334566859` |
| `p_hk4006` | 港股公司停牌 | `hk/p_hk4006` | `c7d6319b90244590a2edef3db0d33600` |
| `p_hk4007` | 港股公司复牌 | `hk/p_hk4007` | `7290d8950bac4ea4baa6f6996ba6df65` |
| `p_hk4013` | 股份回购 | `hk/p_hk4013` | `f50ee6e48f3045f2a95e5dfdebeef9a6` |
| `p_hk4014` | 股份卖空 | `hk/p_hk4014` | `6d8ff36327c04f85a56182521ad9341b` |
| `p_hk4004` | 港股收购与合并 | `hk/p_hk4004` | `f90121f6b212452698c0e5ffa0df585d` |
| `p_hk4005` | 港股集资记录 | `hk/p_hk4005` | `4474f2e6755b4901a16a3fa154300492` |
| `p_hk4012` | 首次公开募股概况 | `hk/p_hk4012` | `83401e7edd994e12a0a84cc87bc076ad` |
| `p_hk4015` | 香港新股发行参与各方表 | `hk/p_hk4015` | `fb4741a224f64757ac2a761a32f3e4bc` |
| `p_hk4018` | 分红派息表 | `hk/p_hk4018` | `a0097b7038ed43ffa453a4dc8f25e7b1` |
| `p_hk4040` | 派息-其他权益记录 | `hk/p_hk4040` | `dad51fcc4b00412888227411afdd7e2d` |
| `p_hk4041` | 并行交易表 | `hk/p_hk4041` | `d1381eb87fca4ef8ac143f62cb28af67` |
| `p_hk4044` | 吸收及合并表 | `hk/p_hk4044` | `bfa4f50dd8d248c7ab489467f65d8d54` |
| `p_hk4047` | 配股资讯 | `hk/p_hk4047` | `895c82754be34dbfb8c46a20f1b3bcce` |
| `p_hk4048` | 供股或公开发售资讯表 | `hk/p_hk4048` | `8f2ce5f3034349fcbfb40b19714787b7` |
| `p_hk4049` | 港股市值指标 | `hk/p_hk4049` | `4263490ce1ab45f9b7f37ef4ce72e736` |
| `p_stock2237_BSE` | 北交所定期报告预披露时间 | `stock/p_stock2237_BSE` | `bccce18d01944a979983465e20251210` |
| `p_stock2238_BSE` | 北交所上市公司业绩预告 | `stock/p_stock2238_BSE` | `4808df19e1504715bf31b972f907a403` |
| `p_stock2239_BSE` | 北交所定期报告审计意见 | `stock/p_stock2239_BSE` | `839595de06bd41be918cfd28c562c63c` |
| `p_stock2300_BSE` | 北交所报告期资产负债表 | `stock/p_stock2300_BSE` | `efa9c2aa942044a39641c8004edbff3f` |
| `p_stock2301_BSE` | 北交所个股报告期利润表 | `stock/p_stock2301_BSE` | `f40ec503fd474b9a8565486a0ebf6cc2` |
| `p_stock2302_BSE` | 北交所个股报告期现金表 | `stock/p_stock2302_BSE` | `57f6fb46c39a42e38240a30a3230f770` |
| `p_stock2303_BSE` | 北交所个股报告期指标表 | `stock/p_stock2303_BSE` | `0ef1f7bf862c41fd832a13b057de34b3` |
| `p_stock2325_BSE` | 北交所金融类资产负债表2007版 | `stock/p_stock2325_BSE` | `b145827c416245fe888262bf626fdd4d` |
| `p_stock2326_BSE` | 北交所金融类利润表2007版 | `stock/p_stock2326_BSE` | `ee1e104036f64e7c967935c04d7cbaef` |
| `p_stock2327_BSE` | 北交所金融类现金流量表2007版 | `stock/p_stock2327_BSE` | `adb4f2907ecf40198a3fbc6e9624565f` |
| `p_stock2328_BSE` | 北交所业绩快报 | `stock/p_stock2328_BSE` | `744379d7e9a741d6993e81d7aebaf071` |
| `p_stock2399_BSE` | 北交所沪深股票最新的财务报告日期 | `stock/p_stock2399_BSE` | `0073a2bf2795432285063d5f523c40be` |

### 3.2 巨潮网使用接口（200 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cninfo5001` | 定期报告披露事件 | `cninfo/p_cninfo5001` | `a2eac0ef2ed14b0bb71dccf4f630f8da` |
| `p_cninfo5002` | 业绩预告披露事件 | `cninfo/p_cninfo5002` | `4445ce00db824066a28c26bfd104ef93` |
| `p_cninfo5003` | 公开信息/龙虎榜披露事件 | `cninfo/p_cninfo5003` | `3f204599c7984bca933c60405d1560dd` |
| `p_cninfo5004` | 分红披露事件 | `cninfo/p_cninfo5004` | `0a6b3d63278946ca8482366cf0baf0d4` |
| `p_cninfo5005` | 融资披露事件 | `cninfo/p_cninfo5005` | `68b2d5612c804bf59a1b3842bcd5d6c9` |
| `p_cninfo5006` | 高管交易披露事件 | `cninfo/p_cninfo5006` | `8e5ff1399b2e4b2fb5fa5c602a9282d4` |
| `p_cninfo5007` | 股东交易披露事件 | `cninfo/p_cninfo5007` | `01dacc4bb98242f3ad35e91f7f479c52` |
| `p_cninfo5008` | 大宗交易披露事件 | `cninfo/p_cninfo5008` | `1439d775725f4c63b6187ed454a1da7e` |
| `p_cninfo5009` | 投资日历事件 | `cninfo/p_cninfo5009` | `07255e40b66a4560a5743ccc01b5ebc0` |
| `p_cninfo5010` | 猜一猜事件 | `cninfo/p_cninfo5010` | `0b72b05fdde54180bf04765dc3fa760b` |
| `p_cninfo5011` | 宏观信息事件 | `cninfo/p_cninfo5011` | `73e4d0f677d04a72836d5c7384a7dac1` |
| `p_cninfo5012` | 交易指标数据 | `cninfo/p_cninfo5012` | `9fecbb9065e247bba69d117feb5f8a5a` |
| `p_cninfo5013` | 深港通股票列表 | `yellowpages/p_cninfo5013` | `2b1c12923307491a877d0ff185e7cda9` |
| `p_cninfo5015` | 交易公开信息 | `cninfo/p_cninfo5015` | `0cfa3c97750848dbb662f1c54eb38c84` |
| `p_cninfo5016` | 公司市场公开信息 | `cninfo/p_cninfo5016` | `91018b16032741b58ff6b3431bbcee01` |
| `p_cninfo5017` | 股本结构 | `cninfo/p_cninfo5017` | `a31e288fd6444d9f952fb17a47170513` |
| `p_cninfo5038` | 融资融券市场汇总数据 | `cninfo/p_cninfo5038` | `ab4bc8cb0b06437d90ff9e36b453a59b` |
| `p_cninfo5039` | 两市融资融券交易明细数据 | `cninfo/p_cninfo5039` | `45da801891d844509c635090f8580f83` |
| `p_cninfo5040` | 限售解禁接口 | `cninfo/p_cninfo5040` | `69280e7aa21d4008b40f12145f8d85c2` |
| `p_cninfo5041` | 高管持股变动汇总 | `cninfo/p_cninfo5041` | `2b675d982b0043899ef704f48dad22bc` |
| `p_cninfo5042` | 证券异动公开信息统计 | `cninfo/p_cninfo5042` | `180d5c16aa274b6e8fa072cd0c9421e8` |
| `p_cninfo5043` | 大宗交易汇总统计 | `cninfo/p_cninfo5043` | `e0a9e7152ae043a992abcc70b55e7861` |
| `p_cninfo5045` | 深沪股通十大成交活跃股 | `cninfo/p_cninfo5045` | `972bfe3781294717920b7d3b5bc37a88` |
| `p_cninfo5046` | 大宗交易报表明细 | `cninfo/p_cninfo5046` | `f6a71f7194344385b8ca2dbfe395635b` |
| `p_cninfo5047` | 股东人数 | `cninfo/p_cninfo5047` | `710c89b098a54f12adfa7a8f0f05c5af` |
| `p_cninfo5056` | 大宗交易 | `cninfo/p_cninfo5056` | `43d0376b408a42e9a25502329ec72175` |
| `p_cninfo5057` | 限售解禁 | `cninfo/p_cninfo5057` | `29313b94047b4e34a1a8adddc76335cf` |
| `p_cninfo5058` | 股东增（减）持 | `cninfo/p_cninfo5058` | `ce36d22968674fe495b8918edea8cd01` |
| `p_info3055_h5` | 沪深H5公告 | `info/p_info3055_h5` | `d5e83195084a4c4293c0523121ee9e66` |
| `p_public0004` | 板块成份股数据 | `stock/p_public0004` | `9ab168b31df84d8e98076bef67073537` |
| `p_stock0004` | 股票所属板块 | `stock/p_stock0004` | `f77d3bb0dd724bbe8b3d8459ed32e79a` |
| `p_stock2426` | 多市场交易日报 | `stock/p_stock2426` | `b51f2add2fc140158d820a36c8ddabd6` |
| `p_sysapi1000` | 交易所列表 | `sysapi/p_sysapi1000` | `4c0744ccb8f94da9849a4e56f49e783b` |
| `p_sysapi1001` | 证券代码简称 | `sysapi/p_sysapi1001` | `8288d839639f4cf08465993180a13d82` |
| `p_sysapi1002` | 通用资产负债表 | `sysapi/p_sysapi1002` | `cdc4fdb4564a460190f9882663686195` |
| `p_sysapi1003` | 通用利润表 | `sysapi/p_sysapi1003` | `f83afd47cfcf400a9c58144ce29cf70c` |
| `p_sysapi1004` | 通用现金流量表 | `sysapi/p_sysapi1004` | `e4a028a44f2f4fcea1aadd5f9347642d` |
| `p_sysapi1005` | 收盘日行情 | `sysapi/p_sysapi1005` | `0e7767bcb6c44c7583e44078606d08e0` |
| `p_sysapi1006` | 海外标准产业分类与国证对应关系查询 | `oversea/p_sysapi1006` | `779f9ba43cfc4d3ba26e9be96d437a99` |
| `p_sysapi1007` | 行情数据-交易所时间点查询 | `sysapi/p_sysapi1007` | `d8932cfcf4604f42a09c98e1eabdc975` |
| `p_sysapi1008` | 行情数据-股票代码时间区间查询接口 | `sysapi/p_sysapi1008` | `58524805c9934689a307db7bc9def604` |
| `p_sysapi1009` | 行情数据-环球收盘行情接口 | `sysapi/p_sysapi1009` | `cc611b1feb564545938de96a5fbdfba1` |
| `p_sysapi1012` | 港股行业板块成份股 | `sysapi/p_sysapi1012` | `22ae1b2eb382466289c214a8f89a1755` |
| `p_sysapi1013` | 股票行情周报月报 | `sysapi/p_sysapi1013` | `e28ef72454704bdbb4099b75f96af62c` |
| `p_sysapi1014` | 指数代码 | `sysapi/p_sysapi1014` | `eb6f5eac5406470a8d2e45c55950edbe` |
| `p_sysapi1015` | 按指数查询成分股日行情 | `sysapi/p_sysapi1015` | `f40f1d031cfb4a8c96a879165e74e4a6` |
| `p_sysapi1016` | 证券标的股查询 | `sysapi/p_sysapi1016` | `294a791c7b794d36bfbcdb3a2a8052da` |
| `p_sysapi1017` | 接口查询条件 | `sysapi/p_sysapi1017` | `80100cb112204b9fa9fcb60beec67721` |
| `p_sysapi1018` | 基本资料 | `sysapi/p_sysapi1018` | `613f2062eea24447b9df4cbc203bfb6d` |
| `p_sysapi1019` | 分红指标 | `sysapi/p_sysapi1019` | `66ac85d341c4484a9d287f31ba59cc80` |
| `p_sysapi1020` | 持股集中度 | `sysapi/p_sysapi1020` | `399f3a274f404cddb0df3908125869c8` |
| `p_sysapi1022` | 大宗交易报表 | `sysapi/p_sysapi1022` | `2f27105bcfa7487ba6d70560dd6fbfd1` |
| `p_sysapi1023` | 融资融券明细 | `sysapi/p_sysapi1023` | `dec022e037f045c484a32347e8ed9f02` |
| `p_sysapi1024` | 解禁明细 | `sysapi/p_sysapi1024` | `7e7a0a099af9494c8bc21c585dc19e06` |
| `p_sysapi1025` | 减持明细 | `sysapi/p_sysapi1025` | `6c58758094c94c60848ad8932455e398` |
| `p_sysapi1026` | 增持明细 | `sysapi/p_sysapi1026` | `eff062877e544b7bb7f4932f3d52860b` |
| `p_sysapi1027` | 减持汇总 | `sysapi/p_sysapi1027` | `b6e72791e72e43619db3945b8cc7088a` |
| `p_sysapi1028` | 增持汇总 | `sysapi/p_sysapi1028` | `8a3adf9961354584869a651fbc3f5786` |
| `p_sysapi1029` | 股本变动 | `sysapi/p_sysapi1029` | `8d7ece3cd6264f6b8ce8f694a0b735a4` |
| `p_sysapi1030` | 高管持股变动明细 | `sysapi/p_sysapi1030` | `f35ebd579b0d4e649bc74ebb9383609b` |
| `p_sysapi1031` | 高管持股变动汇总 | `sysapi/p_sysapi1031` | `088a5868f8774a549338574fd9e4c3dd` |
| `p_sysapi1033` | 实际控制人持股变动 | `sysapi/p_sysapi1033` | `a32edb5668b641d2b546588a3a5bd8f2` |
| `p_sysapi1034` | 股东人数及持股集中度 | `sysapi/p_sysapi1034` | `53ed7d2fc4a5474da25b7994ed334047` |
| `p_sysapi1037` | 业绩预告 | `sysapi/p_sysapi1037` | `6f7156ad0a044170b15e70da1a5bb552` |
| `p_sysapi1038` | 预告业绩扭亏个股 | `sysapi/p_sysapi1038` | `b9ea31b969b74ead8639aa1dc163b8b7` |
| `p_sysapi1039` | 预告业绩大幅下降个股 | `sysapi/p_sysapi1039` | `1219ab371d3346a3b597156e137e92d9` |
| `p_sysapi1040` | 预告业绩大幅上升个股 | `sysapi/p_sysapi1040` | `16de11a7a37742a4bbe53060dd33630f` |
| `p_sysapi1041` | 个股主要指标 | `sysapi/p_sysapi1041` | `51e2ad1a3ed6446788f245c78d6e11e2` |
| `p_sysapi1042` | 分地区财务指标 | `sysapi/p_sysapi1042` | `3cecdf45234640ec9720e7aa139f39c9` |
| `p_sysapi1043` | 分行业财务指标 | `sysapi/p_sysapi1043` | `27da2508e0db40d0b9e2672c8a449457` |
| `p_sysapi1044` | 分市场财务指标 | `sysapi/p_sysapi1044` | `d9ba0a1015b04492b1f6b7740355ab87` |
| `p_sysapi1045` | 地区分红明细 | `sysapi/p_sysapi1045` | `4939ba7be4a243ad82de96307d1e571f` |
| `p_sysapi1046` | 行业分红明细 | `sysapi/p_sysapi1046` | `032dc0fca63847e480cb66ac048b3c3f` |
| `p_sysapi1047` | 股东大会召开情况 | `sysapi/p_sysapi1047` | `befc13dd5fa74dddaf68934c414b1cff` |
| `p_sysapi1048` | 股东大会相关事项变动 | `sysapi/p_sysapi1048` | `07ad2d226fec4365be7c8c3bae7b3829` |
| `p_sysapi1049` | 股东大会议案表 | `sysapi/p_sysapi1049` | `aaf5eae5932d498aa0cf3eff930770c2` |
| `p_sysapi1050` | 资产重组 | `sysapi/p_sysapi1050` | `fa4940f2c1d24bf8978f0b83dee9298b` |
| `p_sysapi1051` | 债务重组 | `sysapi/p_sysapi1051` | `c80d41b6461c445d84e6fc00ef1f22ef` |
| `p_sysapi1052` | 吸收合并 | `sysapi/p_sysapi1052` | `cd26153220594c64a6084bed1cc0d915` |
| `p_sysapi1053` | 股权变更 | `sysapi/p_sysapi1053` | `a46fd7123089462f96bfdc81442bce25` |
| `p_sysapi1054` | 对外担保 | `sysapi/p_sysapi1054` | `19e31288c6644eaeb11476f504e09301` |
| `p_sysapi1055` | 公司诉讼 | `sysapi/p_sysapi1055` | `58578c60916444cbaafe351aa2d371ff` |
| `p_sysapi1056` | 首发审核 | `sysapi/p_sysapi1056` | `140900f6d30c48ed81df564663f71ea2` |
| `p_sysapi1057` | 首发筹资 | `sysapi/p_sysapi1057` | `1757ad36ad9544468a96623feb707c1e` |
| `p_sysapi1058` | 增发筹资 | `sysapi/p_sysapi1058` | `83cfd75000154ee8a78033dc7a6cc504` |
| `p_sysapi1059` | 配股筹资 | `sysapi/p_sysapi1059` | `f81e96468f044257873340c550c7bcab` |
| `p_sysapi1060` | 公司债或可转债 | `sysapi/p_sysapi1060` | `1fb119598802429e8d48e1cc6002b941` |
| `p_sysapi1061` | 停复牌 | `sysapi/p_sysapi1061` | `a9f40e6e08ea49889c8d19f0e08a41e4` |
| `p_sysapi1062` | 市场公开信息汇总 | `sysapi/p_sysapi1062` | `0155851e88514932b46500a30009f217` |
| `p_sysapi1063` | 拟上市公司清单 | `sysapi/p_sysapi1063` | `8247dd4d1ad34db3bf5c39a55873f014` |
| `p_sysapi1064` | 暂停上市公司清单 | `sysapi/p_sysapi1064` | `1365097f6dc84087ae1957edbd1cbd86` |
| `p_sysapi1065` | 终止上市公司清单 | `sysapi/p_sysapi1065` | `e2073480827a43ff8e291aa8e9c80b78` |
| `p_sysapi1066` | 数据专题条件参数接口 | `sysapi/p_sysapi1066` | `61376499fc184203b3e47a45d6634d60` |
| `p_sysapi1067` | 股票列表接口 | `sysapi/p_sysapi1067` | `2e170255dd544176a09c80b299be787d` |
| `p_sysapi1068` | 公司基本资料 | `sysapi/p_sysapi1068` | `fdfdba79f8834cf1943d9dad01e1d7e4` |
| `p_sysapi1069` | 公司高管 | `sysapi/p_sysapi1069` | `abbd8f92303e4b4a80fdc7d128c7369f` |
| `p_sysapi1070` | 前十大股东 | `sysapi/p_sysapi1070` | `9bb8168051d24a5faf9f52d97229c9ad` |
| `p_sysapi1071` | 前十大流通股东 | `sysapi/p_sysapi1071` | `b3b0f1b9d2004de5a494a1007a5c9659` |
| `p_sysapi1072` | 历史行情 | `sysapi/p_sysapi1072` | `9f49e4c5b5994d9698b7961d85862a80` |
| `p_sysapi1073` | 分红数据 | `sysapi/p_sysapi1073` | `73051e8a430c4add9bd52d71853ff208` |
| `p_sysapi1074` | 主要指标 | `sysapi/p_sysapi1074` | `a8eecc8a54854fc99b20979d11e84542` |
| `p_sysapi1075` | 利润表 | `sysapi/p_sysapi1075` | `8eda72c67a934251b708be0e7ce152a3` |
| `p_sysapi1076` | 现金流表表 | `sysapi/p_sysapi1076` | `9a0fb8cf339f4bc99dfa54a6760a59d5` |
| `p_sysapi1077` | 资产负债表 | `sysapi/p_sysapi1077` | `1c953113cf914500aae5b13e68df8520` |
| `p_sysapi1078` | 股票智能摘要 | `sysapi/p_sysapi1078` | `af27590f813d4a4ea67cc5eb62efcdf9` |
| `p_sysapi1079` | 行业市盈率 | `sysapi/p_sysapi1079` | `06f27c9c98ad48a88cd77ed537b23e15` |
| `p_sysapi1080` | 投资评级 | `sysapi/p_sysapi1080` | `93ee6ebd27c34a75bbd47f9ab00cf3cd` |
| `p_sysapi1081` | 预告业绩大幅上升个股 | `sysapi/p_sysapi1081` | `a4c96ccbe7d14e218dfa33e6211ea632` |
| `p_sysapi1082` | 预告业绩大幅下降个股 | `sysapi/p_sysapi1082` | `d4fc1618f19a4c318604fb2ae527131e` |
| `p_sysapi1083` | LOF基金净值增长率 | `sysapi/p_sysapi1083` | `505da5a4406148f096ef3c0e8c055340` |
| `p_sysapi1084` | ETF基金净值增长率 | `sysapi/p_sysapi1084` | `0e0b519e77ac4091ba1a1e8531e8f5fc` |
| `p_sysapi1085` | 公告分类信息 | `sysapi/p_sysapi1085` | `b60d8edf350346f0935e05b7175110ea` |
| `p_sysapi1086` | 新三板行业分类成份股 | `sysapi/p_sysapi1086` | `8dbf6891032c465ebad606fa45f5bd6f` |
| `p_sysapi1087` | 行业市盈率 | `sysapi/p_sysapi1087` | `4d7f5b84cd9a498ebc5208f02b038cf6` |
| `p_sysapi1088` | 基金净值增长率 | `sysapi/p_sysapi1088` | `125cd59853c64710b1b749234883dbe9` |
| `p_sysapi1089` | 投资评级 | `sysapi/p_sysapi1089` | `054cb0d30c87435e8dd37c8e0e429abc` |
| `p_sysapi1090` | 小程序栏目数据接口 | `sysapi/p_sysapi1090` | `0ef9f6bc59bf475c957371de5919b899` |
| `p_sysapi1091` | 公告信息数据 | `sysapi/p_sysapi1091` | `bc18adc0fce4447aab22423302ab38c4` |
| `p_sysapi1092` | 商城显示分类接口（内部使用） | `sysapi/p_sysapi1092` | `fd8f6241206b46e9a81de01699ce868f` |
| `p_sysapi1093` | 并购重组 | `sysapi/p_sysapi1093` | `a0901f3df14a4f33a6e53df64ae671da` |
| `p_sysapi1094` | 股权质押 | `sysapi/p_sysapi1094` | `5f7a56f60df8475c8457cdddf623f19f` |
| `p_sysapi1095` | 指数行情数据接口 | `sysapi/p_sysapi1095` | `e44c514103e94dc287a758e44dbbc44a` |
| `p_sysapi1096` | 新股申购 | `sysapi/p_sysapi1096` | `7daff00f76034071ac1f3e626c51006e` |
| `p_sysapi1097` | 新股发行 | `sysapi/p_sysapi1097` | `cbf469fc3f674a3c83680cb8034f76c1` |
| `p_sysapi1098` | 新股过会 | `sysapi/p_sysapi1098` | `c27434e6d4c048bbaf04acc421fafe5f` |
| `p_sysapi1099` | 债券固收-发行人/机构查询 | `sysapi/p_sysapi1099` | `6cc6ca23cd264d5eb2c74832f4b39b53` |
| `p_sysapi1100` | 债券固收-债券代码查询接口 | `sysapi/p_sysapi1100` | `1a2bc2d6cd154bc5a1d0d522c099e315` |
| `p_sysapi1101` | 债券基本信息查询 | `sysapi/p_sysapi1101` | `ec56f402026b47e397f70178e7694f33` |
| `p_sysapi1102` | 债券发行相关中介机构查询 | `sysapi/p_sysapi1102` | `e9f7f619d79a4440a461e83f344b7ea4` |
| `p_sysapi1103` | 债券信用评级查询 | `sysapi/p_sysapi1103` | `55d1628117644e60b930de85cd8cf6f2` |
| `p_sysapi1104` | 债券发行机构信用评级查询 | `sysapi/p_sysapi1104` | `3c8a261ed38641099ae167f789c70a40` |
| `p_sysapi1105` | 债券特殊条款及其细项 | `sysapi/p_sysapi1105` | `49a969b493254a9595c74acb6f309fba` |
| `p_sysapi1106` | 债券担保信息 | `sysapi/p_sysapi1106` | `015fada345a24b6a99e92f78c50bc729` |
| `p_sysapi1107` | 债券利率 | `sysapi/p_sysapi1107` | `20ac34c7532e4cf0ab9205d0de8fb80a` |
| `p_sysapi1108` | 债券现金流明细 | `sysapi/p_sysapi1108` | `14dce4a12c6e496f9ea6495747fa4b0b` |
| `p_sysapi1109` | 可转债转股 | `sysapi/p_sysapi1109` | `096f9ef650324c17b885b5924f73eca9` |
| `p_sysapi1110` | 可转债转股价格调整 | `sysapi/p_sysapi1110` | `cafc232f2a5d438db8c25e48c9a5fead` |
| `p_sysapi1111` | 上市基金行情 | `sysapi/p_sysapi1111` | `a8aebc578f62481d8d35dbba66b92675` |
| `p_sysapi1112` | 基金重仓股 | `sysapi/p_sysapi1112` | `96ae45d78e47467d98c93cfed8f6bffb` |
| `p_sysapi1113` | 基金行业配置 | `sysapi/p_sysapi1113` | `a4ef89821c874e85968ec73294df87cf` |
| `p_sysapi1114` | 基金资产配置 | `sysapi/p_sysapi1114` | `36c55c4be8e74ca5b280b7aa13cf2161` |
| `p_sysapi1115` | 盈利能力 | `sysapi/p_sysapi1115` | `aa1a9f28c8324bb8b41048fd78e13cbc` |
| `p_sysapi1116` | 运营能力 | `sysapi/p_sysapi1116` | `53852b866dba468892e4ab95de11c88f` |
| `p_sysapi1117` | 成长能力 | `sysapi/p_sysapi1117` | `9219fe432eec442e86ebce1f9f42a4a4` |
| `p_sysapi1118` | 偿债能力 | `sysapi/p_sysapi1118` | `3ebb88b1c9e5494eb4c73bf14d382e2e` |
| `p_sysapi1119` | 定期报告披露预约时间表 | `sysapi/p_sysapi1119` | `a024077c6afe4d638abce288789ac363` |
| `p_sysapi1120` | 国债发行 | `sysapi/p_sysapi1120` | `07686917147b428891b7c82bb3bc9425` |
| `p_sysapi1121` | 地方债发行 | `sysapi/p_sysapi1121` | `abef9394a91c4d86bdbf07c60f00297e` |
| `p_sysapi1122` | 企业债发行 | `sysapi/p_sysapi1122` | `4e499a8785d140b8b31e650cc9121631` |
| `p_sysapi1123` | 可转债发行 | `sysapi/p_sysapi1123` | `6f6a7887e42248d69467d57f2228ef50` |
| `p_sysapi1124` | 可转债转股 | `sysapi/p_sysapi1124` | `908968cae4d6463dbc169579353d8316` |
| `p_sysapi1125` | 科创板已发行定制 | `sysapi/p_sysapi1125` | `ec832ddb55a848ebb39b341a079351f4` |
| `p_sysapi1126` | 基金智能资讯 | `sysapi/p_sysapi1126` | `5efd7a9d7bb345ab88805cab7b3ad8ee` |
| `p_sysapi1127` | 数据智能资讯 | `sysapi/p_sysapi1127` | `8cd2885fdd0d406c8de3ecf999b4b835` |
| `p_sysapi1128` | 最新智能资讯 | `sysapi/p_sysapi1128` | `28ec7a373a8b4242a90fa5b8238a6ccb` |
| `p_sysapi1129` | 报告期分红明细 | `sysapi/p_sysapi1129` | `c01f01725662494db5e8e7b3987f61e9` |
| `p_sysapi1130` | 公司透视-市场表现 | `sysapi/p_sysapi1130` | `2a9d4bc8604940c9801dfeafe8df8e37` |
| `p_sysapi1131` | 公司透视-投资评级 | `sysapi/p_sysapi1131` | `3e1fab0c599745c5b1ea1a1caba6b64d` |
| `p_sysapi1132` | 公司透视-主要财务指标 | `sysapi/p_sysapi1132` | `9a61b63864bc486ba42ab6cdfc62ab57` |
| `p_sysapi1133` | 新f10基本资料 | `sysapi/p_sysapi1133` | `902f9066f79c4d869719dfeeea0bd75a` |
| `p_sysapi1134` | 新F10上市相关 | `sysapi/p_sysapi1134` | `5f17d7689d4c4c38860db90dc30cc4ff` |
| `p_sysapi1135` | 新F10公司高管  | `sysapi/p_sysapi1135` | `545163177d8049cf8257f677f14c2a13` |
| `p_sysapi1136` | 新F10股本结构 | `sysapi/p_sysapi1136` | `5252f3a746c8406f8d876c30d46ff445` |
| `p_sysapi1137` | 新F10大宗交易 | `sysapi/p_sysapi1137` | `c6dd9ebbbf95420380e1b0c96071be0a` |
| `p_sysapi1138` | 新F10融资融券 | `sysapi/p_sysapi1138` | `41207f07b2214e1fa5677c64c96158d1` |
| `p_sysapi1139` | 新F10历史分红 | `sysapi/p_sysapi1139` | `e9be6f9282bf457cb6eab865b311afb6` |
| `p_sysapi1140` | 新F10-主要财务指标 | `sysapi/p_sysapi1140` | `1849c5edbbde4a08952ccf32b060b111` |
| `p_sysapi1141` | 新F10利润表 | `sysapi/p_sysapi1141` | `37a2883c09564d40be9fb74d1d19453e` |
| `p_sysapi1142` | 新F10现金流表表 | `sysapi/p_sysapi1142` | `25fb4b60a9d046a7b6990dc553239719` |
| `p_sysapi1143` | 新F10资产负债表 | `sysapi/p_sysapi1143` | `9e89aa83323c479983408573492a47fe` |
| `p_sysapi1144` | 公司透视-最近五个报告期 | `sysapi/p_sysapi1144` | `3722e6860d8c42a0b50d45bee69d7dec` |
| `p_sysapi1145` | 创业板已发行定制 | `sysapi/p_sysapi1145` | `6adda2aba2444f05be93f8dd042f07de` |
| `p_cninfo5048` | IPO公司情况列表 | `cninfo/p_cninfo5048` | `4b5455c928484b0d9a8d2ae6c025e926` |
| `p_cninfo5049` | IPO创业板上市进展 | `cninfo/p_cninfo5049` | `05f1bceb4a5b4910ab90d1261b8c7e84` |
| `p_cninfo5050` | IPO主要股东 | `cninfo/p_cninfo5050` | `729adc67cc034257bd6385e635cabbfd` |
| `p_cninfo5051` | IPO实际控制人 | `cninfo/p_cninfo5051` | `a16f986aa58d45c690790ddb2aab4582` |
| `p_cninfo5052` | IPO核心技术及研发技术人员 | `cninfo/p_cninfo5052` | `9496acba3f81464c9ac3b489f758f6f1` |
| `p_cninfo5053` | IPO主要竞争对手 | `cninfo/p_cninfo5053` | `63e07f6b45ef4bb4923e9dafc4b21678` |
| `p_cninfo5054` | IPO前5大供应商占比情况 | `cninfo/p_cninfo5054` | `da1607e35f694c11a214005e78f3d24a` |
| `p_cninfo5055` | IPO前5大客户占比情况 | `cninfo/p_cninfo5055` | `35ba3907674d493080e82bd27a665a78` |
| `p_cninfo5067` | ESG指数信息视图 | `cninfo/p_cninfo5067` | `0143bfbde7ca4a6a95b40dca4ebbd0aa` |
| `p_ESG8701` | 二级行业评级分布 | `stock/p_ESG8701` | `0c0aabcf75264978b87120cc0511ac17` |
| `p_ESG8702` | 深沪市场评级分布 | `stock/p_ESG8702` | `a65369742ba546f9972f7620f43b68fb` |
| `p_ESG8703` | ESG细项评分 | `stock/p_ESG8703` | `e96ed46b0432426482ba04e206a8614f` |
| `p_ESG8704` | 上市公司ESG综合评分 | `stock/p_ESG8704` | `6cd7ec5a07c24807af4dc5efa8e4ee2b` |
| `p_ESGCODE` | ESG键盘精灵订制接口 | `stock/p_ESGCODE` | `6df5084746f1430c9f0dd00dfc344818` |
| `p_cninfo5059` | 上交所公告-信息中心订制 | `load/p_cninfo5059` | `0e4bc7f7c8744c4f92e69c481871630a` |
| `p_cninfo5059_new` | 上交所互换公告-信息中心订制 | `load/p_cninfo5059_new` | `07af1efd1590444e8ca28b1bb105df53` |
| `p_cninfo5060` | 北交所公告-信息中心订制 | `load/p_cninfo5060` | `a7b2b77076cf4d8a9509bdec39e924e5` |
| `p_cninfo5061` | 三板公告-信息中心订制 | `cninfo/p_cninfo5061` | `f0ad9a11bc5a4abbaf45c85ebfde5605` |
| `p_cninfo5062` | 沪市债券公告-信息中心订制 | `cninfo/p_cninfo5062` | `12effbf6d33b4677a6a6eb50bd7a81c7` |
| `p_cninfo5063` | 监管机构公告-信息中心订制 | `cninfo/p_cninfo5063` | `39af36c671d143898627e601e7d796fd` |
| `p_cninfo5064` | 预披露公告-信息中心订制 | `cninfo/p_cninfo5064` | `b5ede90f582e4a7fb0572fc57dd4410b` |
| `p_cninfo5065` | 港股中英文公告-信息中心订制 | `cninfo/p_cninfo5065` | `b9470e6f43f44bc39a834dc5d41478e2` |
| `p_cninfo5066` | 再融资/重大资产重组/转板PDF公告-信息中心订制 | `cninfo/p_cninfo5066` | `dcd3e8450f684903b7d5c265378b9752` |
| `p_info3012` | 债券公告信息表 | `info/p_info3012` | `65750815e8c747168b9668bcb1e04834` |
| `p_info3014` | 新三板公告信息 | `info/p_info3014` | `64dab2ef2f95445dad641bd63d025c5b` |
| `p_info3024` | 港股中英文公告 | `info/p_info3024` | `cf4b0c8397de416fae4268df11168834` |
| `p_info3060` | 预披露公告 | `info/p_info3060` | `37f15dbddf044179a33e13f7936b5eed` |
| `p_info3063` | 监管机构公告 | `info/p_info3063` | `024698146b7f47938f43120be19e1847` |

### 3.3 公告资讯（106 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3015` | 公告基本信息 | `info/p_info3015` | `a0fec4cde3bf4f83821fb5a769231100` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3085` | 上市公司公告(DataCloud) | `info/p_info3085` | `8b5bc11ae8984aec8d78b7f934791f44` |
| `p_info3092` | 深沪北交易所临时停牌公告 | `info/p_info3092` | `dfb32325f1894591bc945ee6ab678283` |
| `p_info3125` | 新增再融资/重大资产重组/转板公告 | `info/p_info3125` | `d77788ae3ce24d4d96ba11c87e624696` |
| `p_info3125t` | 最新再融资/重大资产重组/转板PDF公告 | `info/p_info3125t` | `f2504b377ed84edf98e5727a324be179` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3011` | 基金公告信息表 | `info/p_info3011` | `d37f45e94bfb4c318d7ec934f5910cb6` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3012` | 债券公告信息表 | `info/p_info3012` | `65750815e8c747168b9668bcb1e04834` |
| `p_info3012_inc` | 债券公告数据表 | `load/p_info3012_inc` | `8e02a4fd9cea486ba368846dc51120a3` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3066` | 银行间公告 | `info/p_info3066` | `c150c8e0a9ff44748e2a8696d5f25760` |
| `p_info3066_inc` | 银行间公告 | `load/p_info3066_inc` | `360b2702af2d41d58e1249f6a4e44dee` |
| `p_info3070_client` | 银行间债券PDF公告 | `info/p_info3070_client` | `5ac100f43ed046068dfef626dd113de2` |
| `p_info3102` | 定制银行间债接口 | `info/p_info3102` | `9136cc7ed5854cfe9d6e0aa14c55363e` |
| `p_info3171` | 银行间债券(债项维度)公告 | `info/p_info3171` | `86d84b14f49746c9936b95e39d7f3cef` |
| `p_info3171_inc` | 银行间债券(债项维度)公告 | `load/p_info3171_inc` | `98f4f6cdc81840b3966d762bdad37af4` |
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3013` | 港股公告数据 | `info/p_info3013` | `3161b164a72b40ec8d26bbb266d29b70` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3023` | 港股中英文公告 | `info/p_info3023` | `accac5bd04d5415ba4af96ef22684f2f` |
| `p_info3024` | 港股中英文公告 | `info/p_info3024` | `cf4b0c8397de416fae4268df11168834` |
| `p_info3065` | 港股IPO公告 | `info/p_info3065` | `2e39ec9f5f9348fb9f23eddb6f14b97b` |
| `p_info3060` | 预披露公告 | `info/p_info3060` | `37f15dbddf044179a33e13f7936b5eed` |
| `p_info3062` | 预披露-定制 | `info/p_info3062` | `07a5cef02109449f8f9ac7cd933f124e` |
| `p_info3065` | 港股IPO公告 | `info/p_info3065` | `2e39ec9f5f9348fb9f23eddb6f14b97b` |
| `p_info3072` | 港股预披露公告 | `info/p_info3072` | `b96cc75e46484301aeeaf8747bf7d9e0` |
| `p_info3014` | 新三板公告信息 | `info/p_info3014` | `64dab2ef2f95445dad641bd63d025c5b` |
| `p_info3061` | 四板公告 | `info/p_info3061` | `a5b00692329a46c6b5d23bc606d34c02` |
| `p_info3016` | 其他公告信息 | `info/p_info3016` | `c794a864abb242fea2f08527b455ffcf` |
| `p_info3063` | 监管机构公告 | `info/p_info3063` | `024698146b7f47938f43120be19e1847` |
| `p_info3064` | 交易所问询函 | `info/p_info3064` | `93032df83b9d4dd4a30b21bf96ecf144` |
| `p_info3076` | 辅导企业公告 | `info/p_info3076` | `f0f91648b59f4a2cb8db2ece57daa889` |
| `p_info3089` | 英文监管动态 | `info/p_info3089` | `f9d67cf6e5ca4466b0f757fa2739e992` |
| `p_info3095` | 地方证监局监管动态公告 | `info/p_info3095` | `11db51f866b946cfbe316d376764b924` |
| `p_info3067` | 深市公告摘要 | `info/p_info3067` | `a61dd57ad1c649edaae4745acadadd48` |
| `p_info3085t` | 最新深沪北上市公司PDF公告 | `info/p_info3085t` | `341141e24b3e413a9ef12d60675e21e2` |
| `p_info3085t_inc` | 最新深沪北上市公司PDF增量公告 | `load/p_info3085t_inc` | `d079293ff21547c1a1dc1e82f1ba0c02` |
| `p_info3125t` | 最新再融资/重大资产重组/转板PDF公告 | `info/p_info3125t` | `f2504b377ed84edf98e5727a324be179` |
| `p_info3011t` | 最新基金PDF公告 | `info/p_info3011t` | `563c0d71f914431aa66a4de754ca32e8` |
| `p_info3011t_inc` | 最新基金PDF增量公告 | `load/p_info3011t_inc` | `20b512c5bc8b4c2da66933f56922d64f` |
| `p_info3011_inc` | 最新基金PDF增量公告 | `load/p_info3011_inc` | `f64337b5a7174d109b79c7f28a1a4912` |
| `p_info3012t` | 最新债券PDF公告 | `info/p_info3012t` | `736f28a3ba99426aba621448a9914847` |
| `p_info3012t_inc` | 最新债券PDF增量公告 | `load/p_info3012t_inc` | `cf25f7c3c2f4402493b56782338c3c49` |
| `p_info3066t` | 最新银行间PDF公告 | `info/p_info3066t` | `f68589d2b9bc46ce925e2adbd3af7a8b` |
| `p_info3066t_inc` | 最新银行间PDF增量公告 | `load/p_info3066t_inc` | `fe354390e49a4d7e858364a1dde5cf3b` |
| `p_info3171t` | 银行间债券(债项维度)公告 | `info/p_info3171t` | `0331eae199ea46dea66523ac63faf28f` |
| `p_info3024t` | 最新港股中英文PDF公告 | `info/p_info3024t` | `c0b55dd1941b4ac88ca87697c328ed2e` |
| `p_info3024t_inc` | 最新港股中英文PDF增量公告 | `load/p_info3024t_inc` | `a897879cb25d4b1eb1b373d6080b1fa7` |
| `p_info3060t` | 最新预披露PDF公告 | `info/p_info3060t` | `270c8c92e4d946fda216a63c9b3e3561` |
| `p_info3060t_inc` | 最新预披露PDF增量公告 | `load/p_info3060t_inc` | `38666ae4af2f403486aa23788e95a1e7` |
| `p_info3072t` | 最新港股预披露PDF公告 | `info/p_info3072t` | `8503d5dfac254f7885db3efa00ff1ea8` |
| `p_info3072t_inc` | 最新港股预披露PDF增量公告 | `load/p_info3072t_inc` | `82fe7dabf41540ccb8d7c490a454076e` |
| `p_info3014t` | 最新新三板PDF公告 | `info/p_info3014t` | `963958ab8078462f914330beef2198cb` |
| `p_info3014t_inc` | 最新新三板PDF增量公告 | `load/p_info3014t_inc` | `7272e11a333f42e684cb42c1386516e7` |
| `p_info3061t` | 最新四板PDF公告 | `info/p_info3061t` | `a105e7f8ee9a425193a496d9982f8236` |
| `p_info3061t_inc` | 最新四板PDF增量公告 | `load/p_info3061t_inc` | `0d41943f76924a8497c17cca9b57a95c` |
| `p_info3063t` | 最新监管机构PDF公告 | `info/p_info3063t` | `78d4e7042c2848c7b04e7e4eccb8efe8` |
| `p_info3063t_inc` | 最新监管机构PDF增量公告 | `load/p_info3063t_inc` | `0d8c05d6f6cf4e0c9914372deda44564` |
| `p_info3064t` | 最新交易所PDF问询函 | `info/p_info3064t` | `b87cfa1335a64ad195e3afb19943fb91` |
| `p_info3064t_inc` | 最新交易所PDF增量问询函 | `load/p_info3064t_inc` | `099dbda84a6a4b10999e625f95446637` |
| `p_info3076t` | 最新辅导企业PDF公告 | `info/p_info3076t` | `6597fcade2c746a5b58ddcd4e661b73d` |
| `p_info3076t_inc` | 最新辅导企业PDF增量公告 | `load/p_info3076t_inc` | `960d0a1fbb924411851b6b554648e5d1` |
| `p_info3095t` | 最新地方证监局监管动态PDF公告 | `info/p_info3095t` | `c545952540f749eca96620c100e50703` |
| `p_info3024c` | 最新港股中英文PDF公告无历史 | `info/p_info3024c` | `d2ad6da5fb6b42ac84469939cf598392` |
| `p_info3085c` | 最新深沪北上市公司PDF公告无历史 | `info/p_info3085c` | `194ab2863ef7479d994919279ec94ecc` |
| `p_info3051` | 公募基金H5公告 | `info/p_info3051` | `17472ed043164d3ca3584ec60596e134` |
| `p_info3052` | 交易所债券H5公告 | `info/p_info3052` | `04659f4653984f33a6699306e7dd8854` |
| `p_info3053` | 港股H5公告 | `info/p_info3053` | `f8573b63fbba44e28e9e4b68c89efcb3` |
| `p_info3054` | 新三板H5公告 | `info/p_info3054` | `a6cc709cba5b4d52bd01672fd200c502` |
| `p_info3055` | 沪深股票H5公告 | `info/p_info3055` | `8cfe7672748c41a0b7ade949b8731162` |
| `p_info3073` | 银行间H5公告 | `info/p_info3073` | `a6bb4423a8504789a40e88abf763a2b5` |
| `p_info3073_client` | 银行间债券PDF公告 | `info/p_info3073_client` | `1df5fc2688414034916c4d8d7de01b62` |
| `p_info3075` | 四板H5公告 | `info/p_info3075` | `783f149290874cb4bfca96fc2a232283` |
| `p_info3135` | 监管动态Html5公告 | `info/p_info3135` | `2d1066b61bd94ac6bcddccf8bace52c1` |
| `p_info3185t` | 最新深沪北上市公司H5公告 | `info/p_info3185t` | `8bbbe2700f984712ab9bba46b65604b7` |
| `p_info3051t` | 最新公募基金H5公告 | `info/p_info3051t` | `2a6ec8f6fd00491fabb47078aadbfff8` |
| `p_info3052t` | 最新交易所债券H5公告 | `info/p_info3052t` | `ad4f1e0fdbba498c99a95aabb28a7762` |
| `p_info3053t` | 最新港股H5公告 | `info/p_info3053t` | `5d83bb1f55fb49648809357e1f224627` |
| `p_info3055t` | 最新深沪北上市公司H5公告 | `info/p_info3055t` | `75922700fd7847039ec7fdf0aa77309b` |
| `p_info3073t` | 最新银行间H5公告 | `info/p_info3073t` | `0427b951e6424852b320a06613f8b7db` |
| `p_info3075t` | 最新四板H5公告 | `info/p_info3075t` | `f8aa211a3cf04c75af0d26738e850209` |
| `p_info3131t` | 最新深沪北交易所IPO预披露H5公告 | `info/p_info3131t` | `6cf45a349a1246c29dfa4c42660ece51` |
| `p_info3132t` | 最新深沪北交易所监管函件H5公告 | `info/p_info3132t` | `eb5704afa32f4118a5ff8f5a93c62d18` |
| `p_info3133t` | 最新各地证监局辅导企业H5公告 | `info/p_info3133t` | `fec190a40d3142f496535c1047378117` |
| `p_info3135t` | 监管动态Html5公告 | `info/p_info3135t` | `5e41753cf5624c4e8b9b8397c14bf810` |
| `p_info3137t` | 再融资/重大资产重组/转板H5公告 | `info/p_info3137t` | `02583095ffcd429daf71d83336954539` |
| `p_info3185c` | 最近半年深沪北上市公司H5公告 | `info/p_info3185c` | `d5628ea1ef2a44c1b64794bdf1999b55` |
| `p_info3011_client` | 基金公告信息表 | `info/p_info3011_client` | `842e1c51a4164577a92a14e20009d720` |
| `p_info3012_client` | 债券公告信息表 | `info/p_info3012_client` | `0131dc4abcec4f0e8bfb31737beddc71` |
| `p_info3013_client` | 港股公告数据  | `info/p_info3013_client` | `09999b995526445abe096e4aefd734d8` |
| `p_info3014_client` | 新三板公告信息 | `info/p_info3014_client` | `d8fbec1e475545db95152845af370723` |
| `p_info3015_client` | 公告基本信息 | `info/p_info3015_client` | `4509a59fce294f57bf7007b854709b17` |
| `p_info3085_client` | 上市公司公告(DataCloud) | `info/p_info3085_client` | `4b4ebc4052274398bbd43840e1f6f77b` |
| `p_info3085_inc` | 沪深AB股公告基本信息 | `load/p_info3085_inc` | `aef4747e8d46433d975305638a1834a1` |
| `p_info3171_client` | 银行间债券(债项维度)公告 | `info/p_info3171_client` | `699c9347bfe7499f97d835877f6be2c5` |
| `p_info3035` | 数据智能资讯 | `info/p_info3035` | `1bd92189272d4eb1bb16985bcb9e09b0` |
| `p_info3079_AI` | 港股智能资讯接口 | `info/p_info3079_AI` | `24e2f94faa544fe594ecce77166cc13b` |
| `p_info3086` | 行情资讯 | `info/p_info3086` | `164da388d2c241c58275d11965b64636` |
| `p_info3087` | 市场动态资讯 | `info/p_info3087` | `97acc2ac50994049b7973d72cb25f528` |
| `p_info3088` | 港股行情资讯 | `info/p_info3088` | `ffcf1b84aa754eeb9236ab41eb38fb37` |
| `p_info3091` | 上市公司互动信息智能摘要 | `info/p_info3091` | `68d977f1d3f14779b98b9012566d35b0` |
| `p_info3139` | 上市公司互动信息明细 | `info/p_info3139` | `397d4be050a24922866d35f5e7ea61a5` |

### 3.4 证券提示库数据服务（12 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3039` | 股票类资讯内容全量记录 | `info/p_info3039` | `0891ada8a8f44118990f25e7c83efc9c` |
| `p_info3041` | 股票类提示内容全量记录 | `info/p_info3041` | `9ad1aac088c044de9d5081ad83c0bab3` |
| `p_info3091` | 上市公司互动信息智能摘要 | `info/p_info3091` | `68d977f1d3f14779b98b9012566d35b0` |
| `p_info3043` | 基金类资讯内容全量记录 | `info/p_info3043` | `bf20606042c34cc5a56c0abb25083c21` |
| `p_info3045` | 基金类提示内容全量记录 | `info/p_info3045` | `bc8e4d9b4a72404a87ce8963cf090a7d` |
| `p_info3047` | 债券类资讯内容全量记录 | `info/p_info3047` | `c48089fa745644f590308727d53af854` |
| `p_info3049` | 债券类提示内容全量记录 | `info/p_info3049` | `8abbffc7e8e04410849823ab22231aa9` |
| `p_info3057` | 新三板资讯内容全量记录 | `info/p_info3057` | `1611f2dc9f2447d9a0dda0b5f2bd5379` |
| `p_info3059` | 新三板提示内容全量记录 | `info/p_info3059` | `cb86f853ac2d4887ac8fc357402870f9` |
| `p_info3078` | 港股提示内容全量记录 | `info/p_info3078` | `bedeb7ef0a0249b7bf82ce6d762f2539` |
| `p_info3079_AI` | 港股智能资讯接口 | `info/p_info3079_AI` | `24e2f94faa544fe594ecce77166cc13b` |
| `p_info3080` | 港股资讯内容全量记录 | `info/p_info3080` | `ab39458230fc41f4937cf6db90098d3a` |

### 3.5 新闻研报（9 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3097_inc` | 个股研报摘要 | `load/p_info3097_inc` | `63bd34c18e214772832425065a5ef13f` |
| `p_stock2205` | 投资评级 | `sysapi/p_stock2205` | `d7afdca660264fc28253479e627935b7` |
| `p_info3029` | 研报摘要 | `info/p_info3029` | `be3f791d452048048061529b6a2ef77b` |
| `p_info3032` | 公司研报数据 | `info/p_info3032` | `dd45c07bdf2b46ddacfc4492744b1627` |
| `p_info3033` | 行业研报数据 | `info/p_info3033` | `c05ade3a35634513b688d22847973d9b` |
| `p_info3034` | 宏观研报数据 | `info/p_info3034` | `3c25a8126178463dab243ecc808e3675` |
| `p_info3097` | 个股研报摘要 | `info/p_info3097` | `c7095df0abc14cb7aa1c8c0732c3b1e5` |
| `p_stock2205` | 投资评级 | `sysapi/p_stock2205` | `d7afdca660264fc28253479e627935b7` |
| `p_info3030` | 新闻数据查询 | `info/p_info3030` | `7aba8a88d224499886309ab515d3fd0b` |

### 3.6 公共信息（7 个接口）

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_public0001` | 交易日历数据 | `stock/p_public0001` | `0bf76273eb724e38bf32c30cfac5ddda` |
| `p_public0002` | 行业分类数据 | `stock/p_public0002` | `04add00012fc4101bb2e2303b314a6d7` |
| `p_public0003` | 地区分类数据 | `stock/p_public0003` | `361a41a0ce5146db9f5675e2a7d2e371` |
| `p_public0005` | 证券类别编码数据 | `public/p_public0005` | `57aab6472d7d434e91aeab51f2a56586` |
| `p_public0006` | 公共编码数据 | `public/p_public0006` | `577bb53e77984aa9b92c3f843013a39d` |
| `p_public0007` | 人民币汇率中间价 | `public/p_public0007` | `f694148a21e146d39f9297b882eefdcc` |
| `p_public0009` | 机构信息数据 | `public/p_public0009` | `cb9b62f3820c4815b2c86f8033eb406e` |

## 4. 典型接口元数据示例

### 4.1 p_cninfo5001 — 定期报告披露事件

```json
{
  "baseInfo": {
    "maxRecordsParam": 0,
    "name": "p_cninfo5001",
    "alias": "定期报告披露事件",
    "describe": "取数据魔方中财务批露时间事件统计数据。\n请求方式：支持GET 和 POST\n",
    "maxNum": 20000
  },
  "requestConfig": {
    "inputParameter": [
      {
        "fieldName": "scode",
        "checkRule": "[0-9]{6}",
        "defaultValue": "",
        "isNeed": 1,
        "dataType": "string",
        "name": "scode",
        "alias": "股票代码",
        "chooseFlag": 1,
        "describe": "只能输入一只股票",
        "validRule": "[0-9]{6}",
        "fieldChineseName": "股票代码",
        "fieldType": "string"
      },
      {
        "fieldName": "sdate",
        "checkRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "sdate",
        "alias": "开始日期",
        "chooseFlag": 0,
        "describe": "支持格式示例：20161101 或2016-11-01 或2016/11/01",
        "validRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "fieldChineseName": "开始日期",
        "fieldType": "string"
      },
      {
        "fieldName": "edate",
        "checkRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "edate",
        "alias": "截止日期",
        "chooseFlag": 0,
        "describe": "支持格式示例：20161101 或2016-11-01 或2016/11/01",
        "validRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "fieldChineseName": "截止日期",
        "fieldType": "string"
      },
      {
        "fieldName": "format",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "format",
        "alias": "结果集格式",
        "chooseFlag": 0,
        "describe": "设置结果返回的格式，可选的有xml、json、csv、dbf",
        "validRule": "",
        "fieldChineseName": "结果集格式",
        "fieldType": "string"
      },
      {
        "fieldName": "@column",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "@column",
        "alias": "结果列选择",
        "chooseFlag": 0,
        "describe": "选择结果集中所需要的字段，多列用逗号分隔，如@column=a,b",
        "validRule": "",
        "fieldChineseName": "结果列选择",
        "fieldType": "string"
      },
      {
        "fieldName": "@limit",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "int",
        "name": "@limit",
        "alias": "结果条数限制",
        "chooseFlag": 0,
        "describe": "设置结果返回的条数",
        "validRule": "",
        "fieldChineseName": "结果条数限制",
        "fieldType": "int"
      },
      {
        "fieldName": "@orderby",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "@orderby",
        "alias": "结果集排序",
        "chooseFlag": 0,
        "describe": "设置结果集的格式，如 @orderby=id:desc  @orderby=id:asc",
        "validRule": "",
        "fieldChineseName": "结果集排序",
        "fieldType": "string"
      }
    ],
    "fullUrl": "http://webapi.cninfo.com.cn/api/cninfo/p_cninfo5001",
    "requestMethod": "get,post",
    "requestPath": "http://webapi.cninfo.com.cn/api/cninfo/p_cninfo5001"
  },
  "serviceConfig": {},
  "resultContent": {
    "apiCode": "0800c4cae0b4a0610a9fd83d832e6176",
    "errorResult": "",
    "successResult": "",
    "id": 38,
    "outputDescribes": "取数据魔方中财务批露时间事件统计数据。\n请求方式：支持GET 和 POST\n",
    "errorCodeResult": "[{\"code\":\"-1\",\"describe\":\"系统繁忙，此时请开发者稍候再试\",\"msg\":\"系统繁忙，此时请开发者稍候再试\"},{\"code\":\"200\",\"describe\":\"success\",\"msg\":\"success\"},{\"code\":\"401\",\"describe\":\"未经授权的访问\",\"msg\":\"未经授权的访问\"},{\"code\":\"402\",\"describe\":\"不合法的参数\",\"msg\":\"不合法的参数\"},{\"code\":\"403\",\"describe\":\"脚本服务器异常\",\"msg\":\"脚本服务器异常\"},{\"code\":\"404\",\"describe\":\"token 无效\",\"msg\":\"token 无效\"},{\"code\":\"405\",\"describe\":\"token过期\",\"msg\":\"token过期\"},{\"code\":\"406\",\"describe\":\"用户已被禁用\",\"msg\":\"用户已被禁用\"},{\"code\":\"407\",\"describe\":\"免费试用次数已用完\",\"msg\":\"免费试用次数已用完\"},{\"code\":\"408\",\"describe\":\"用户没有余额\",\"msg\":\"用户没有余额\"},{\"code\":\"409\",\"describe\":\"验证权限错误\",\"msg\":\"验证权限错误\"},{\"code\":\"410\",\"describe\":\"验证权限异常\",\"msg\":\"验证权限异常\"},{\"code\":\"411\",\"describe\":\"获取用户信息失败\",\"msg\":\"获取用户信息失败\"},{\"code\":\"412\",\"describe\":\"包时长已超期\",\"msg\":\"包时长已超期\"}]",
    "outputParameter": "[{\"alias\":\"证券代码\",\"dataType\":\"varchar\",\"describe\":\"\",\"fieldChineseName\":\"证券代码\",\"fieldName\":\"SECCODE\",\"fieldType\":\"varchar\",\"name\":\"SECCODE\"},{\"alias\":\"统计日期\",\"dataType\":\"date\",\"describe\":\"实际使用字段，已做了非交易日公告处理\",\"fieldChineseName\":\"统计日期\",\"fieldName\":\"F001D\",\"fieldType\":\"date\",\"name\":\"F001D\"},{\"alias\":\"公告日期\",\"dataType\":\"date\",\"describe\":\"公告发布日期\",\"fieldChineseName\":\"公告日期\",\"fieldName\":\"F002D\",\"fieldType\":\"date\",\"name\":\"F002D\"},{\"alias\":\"事件内容\",\"dataType\":\"varchar\",\"describe\":\"\",\"fieldChineseName\":\"事件内容\",\"fieldName\":\"F003V\",\"fieldType\":\"varchar\",\"name\":\"F003V\"}]",
    "version": 2,
    "apiType": 0
  }
}
```

### 4.2 p_public0001 — 交易日历数据

```json
{
  "baseInfo": {
    "maxRecordsParam": 0,
    "name": "p_public0001",
    "alias": "交易日历数据",
    "describe": "按照交易日历表维度查询其指定维度的交易日期数据。\n输入需查询的交易日历期间、市场交易状态和日期状态，根据输入的参数条件输出所需的交易日历信息 \n请求方式：GET 和 POST\n\n",
    "maxNum": 20000
  },
  "requestConfig": {
    "inputParameter": [
      {
        "fieldName": "sdate",
        "checkRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "sdate",
        "alias": "开始日期",
        "chooseFlag": 0,
        "describe": "支持格式示例：20161101 或2016-11-01 或2016/11/01",
        "validRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "fieldChineseName": "开始日期",
        "fieldType": "string"
      },
      {
        "fieldName": "edate",
        "checkRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "edate",
        "alias": "截止日期",
        "chooseFlag": 0,
        "describe": "支持格式示例：20161101 或2016-11-01 或2016/11/01",
        "validRule": "[0-9]{8}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}/[0-9]{2}/[0-9]{2}",
        "fieldChineseName": "截止日期",
        "fieldType": "string"
      },
      {
        "fieldName": "state",
        "checkRule": "[0-1]{1}",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "state",
        "alias": "状态",
        "chooseFlag": 0,
        "describe": "1表示A股开市，0表示A股休市，不支持多项输入",
        "validRule": "[0-1]{1}",
        "fieldChineseName": "状态",
        "fieldType": "string"
      },
      {
        "fieldName": "format",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "format",
        "alias": "结果集格式",
        "chooseFlag": 0,
        "describe": "设置结果返回的格式，可选的有xml、json、csv、dbf",
        "validRule": "",
        "fieldChineseName": "结果集格式",
        "fieldType": "string"
      },
      {
        "fieldName": "@column",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "@column",
        "alias": "结果列选择",
        "chooseFlag": 0,
        "describe": "选择结果集中所需要的字段，多列用逗号分隔，如@column=a,b",
        "validRule": "",
        "fieldChineseName": "结果列选择",
        "fieldType": "string"
      },
      {
        "fieldName": "@limit",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "int",
        "name": "@limit",
        "alias": "结果条数限制",
        "chooseFlag": 0,
        "describe": "设置结果返回的条数",
        "validRule": "",
        "fieldChineseName": "结果条数限制",
        "fieldType": "int"
      },
      {
        "fieldName": "@orderby",
        "checkRule": "",
        "defaultValue": "",
        "isNeed": 0,
        "dataType": "string",
        "name": "@orderby",
        "alias": "结果集排序",
        "chooseFlag": 0,
        "describe": "设置结果集的格式，如 @orderby=id:desc  @orderby=id:asc",
        "validRule": "",
        "fieldChineseName": "结果集排序",
        "fieldType": "string"
      }
    ],
    "fullUrl": "http://webapi.cninfo.com.cn/api/stock/p_public0001",
    "requestMethod": "get,post",
    "requestPath": "http://webapi.cninfo.com.cn/api/stock/p_public0001"
  },
  "serviceConfig": {},
  "resultContent": {
    "apiCode": "f4964f7e0732160a067a620594b8c46a",
    "errorResult": "",
    "successResult": "",
    "id": 1238,
    "outputDescribes": "按照交易日历表维度查询其指定维度的交易日期数据。\n输入需查询的交易日历期间、市场交易状态和日期状态，根据输入的参数条件输出所需的交易日历信息 \n请求方式：GET 和 POST\n\n",
    "errorCodeResult": "[{\"code\":\"-1\",\"describe\":\"系统繁忙，此时请开发者稍候再试\",\"msg\":\"系统繁忙，此时请开发者稍候再试\"},{\"code\":\"200\",\"describe\":\"success\",\"msg\":\"success\"},{\"code\":\"401\",\"describe\":\"未经授权的访问\",\"msg\":\"未经授权的访问\"},{\"code\":\"402\",\"describe\":\"不合法的参数\",\"msg\":\"不合法的参数\"},{\"code\":\"403\",\"describe\":\"脚本服务器异常\",\"msg\":\"脚本服务器异常\"},{\"code\":\"404\",\"describe\":\"token 无效\",\"msg\":\"token 无效\"},{\"code\":\"405\",\"describe\":\"token过期\",\"msg\":\"token过期\"},{\"code\":\"406\",\"describe\":\"用户已被禁用\",\"msg\":\"用户已被禁用\"},{\"code\":\"407\",\"describe\":\"免费试用次数已用完\",\"msg\":\"免费试用次数已用完\"},{\"code\":\"408\",\"describe\":\"用户没有余额\",\"msg\":\"用户没有余额\"},{\"code\":\"409\",\"describe\":\"验证权限错误\",\"msg\":\"验证权限错误\"},{\"code\":\"410\",\"describe\":\"验证权限异常\",\"msg\":\"验证权限异常\"},{\"code\":\"411\",\"describe\":\"获取用户信息失败\",\"msg\":\"获取用户信息失败\"},{\"code\":\"412\",\"describe\":\"包时长已超期\",\"msg\":\"包时长已超期\"}]",
    "outputParameter": "[{\"alias\":\"日期\",\"dataType\":\"date\",\"describe\":\"\",\"fieldChineseName\":\"日期\",\"fieldName\":\"F001D\",\"fieldType\":\"date\",\"name\":\"F001D\"},{\"alias\":\"是否周初\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否周初\",\"fieldName\":\"F002C\",\"fieldType\":\"varchar\",\"name\":\"F002C\"},{\"alias\":\"是否周末\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否周末\",\"fieldName\":\"F003C\",\"fieldType\":\"varchar\",\"name\":\"F003C\"},{\"alias\":\"是否月初\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否月初\",\"fieldName\":\"F004C\",\"fieldType\":\"varchar\",\"name\":\"F004C\"},{\"alias\":\"是否月末\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否月末\",\"fieldName\":\"F005C\",\"fieldType\":\"varchar\",\"name\":\"F005C\"},{\"alias\":\"是否交易日\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否交易日\",\"fieldName\":\"F006C\",\"fieldType\":\"varchar\",\"name\":\"F006C\"},{\"alias\":\"是否季末\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否季末\",\"fieldName\":\"F007C\",\"fieldType\":\"varchar\",\"name\":\"F007C\"},{\"alias\":\"是否半年末\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否半年末\",\"fieldName\":\"F008C\",\"fieldType\":\"varchar\",\"name\":\"F008C\"},{\"alias\":\"是否年末\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否年末\",\"fieldName\":\"F009C\",\"fieldType\":\"varchar\",\"name\":\"F009C\"},{\"alias\":\"是否银行间交易日\",\"dataType\":\"varchar\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否银行间交易日\",\"fieldName\":\"F010C\",\"fieldType\":\"varchar\",\"name\":\"F010C\"},{\"alias\":\"前一交易日\",\"dataType\":\"date\",\"describe\":\"\",\"fieldChineseName\":\"前一交易日\",\"fieldName\":\"F011D\",\"fieldType\":\"date\",\"name\":\"F011D\"},{\"alias\":\"后一交易日\",\"dataType\":\"date\",\"describe\":\"\",\"fieldChineseName\":\"后一交易日\",\"fieldName\":\"F012D\",\"fieldType\":\"date\",\"name\":\"F012D\"},{\"alias\":\"是否港股交易日\",\"dataType\":\"char(1)\",\"describe\":\"0-否；1-是；默认为0\",\"fieldChineseName\":\"是否港股交易日\",\"fieldName\":\"F013C\",\"fieldType\":\"char(1)\",\"name\":\"F013C\"},{\"alias\":\"港股通交易日\",\"dataType\":\"char(1)\",\"describe\":\"\",\"fieldChineseName\":\"港股通交易日\",\"fieldName\":\"F014C\",\"fieldType\":\"char(1)\",\"name\":\"F014C\"},{\"alias\":\"陆股通交易日\",\"dataType\":\"char(1)\",\"describe\":\"\",\"fieldChineseName\":\"陆股通交易日\",\"fieldName\":\"F015C\",\"fieldType\":\"char(1)\",\"name\":\"F015C\"}]",
    "version": 25,
    "apiType": 0
  }
}
```

## 5. crawler 重构建议

1. **保留现有公开接口**：`hisAnnouncement/query` 仍是获取公告列表和 PDF 链接的主力接口。
2. **用官方文档校准字段**：本参考文档中的 `p_cninfo5001`/`p_cninfo5002` 等接口参数可与现有 crawler 参数互相对照，避免传错字段名或日期格式。
3. **不尝试绕过官方认证**：官方数据端点 401 说明存在 token/授权机制，项目规则不允许绕过登录，因此不纳入爬取方案。

## 6. 文件索引

- `cninfo_api_doc_tree.json`：原始完整文档树（raw，已加入 `.gitignore`）。
- `cninfo_api_gateway_codes.json`：全部 2465 个接口的 `gatewayCode` 索引（raw，已加入 `.gitignore`）。
- `data/cninfo-api-archive/`：自己抓取与朋友抓取的 CNINFO API 原始归档（含 tree、codes、探索脚本与朋友完整 `_doc` 版本，已加入 `.gitignore`）。
- `docs/cninfo_official_api_catalog.json`：机器可读的全量目录与相关接口子集。
- `docs/cninfo_official_api_reference.md`：本 human-readable 参考文档。
