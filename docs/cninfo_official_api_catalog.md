# 深证信（巨潮）官方 API 目录（全量）

> 来源：[https://webapi.cninfo.com.cn/#/apiDoc](https://webapi.cninfo.com.cn/#/apiDoc)
> 提取时间：2026-06-12T13:18:50.717487+00:00
> 全量接口数：2465
> 一级类目数：31
> 与研究相关接口数：608
>
> 注：本目录包含网页左侧未显示的隐藏类目（`display: 0`）。类目顺序与网页左侧目录树一致：可见类目在前，隐藏类目在后。

## 一级类目概览

| 一级类目 | 接口数 | 可见性 |
|----------|--------|--------|
| 公共信息 | 7 | 可见 |
| 公司数据 | 274 | 可见 |
| 公告资讯 | 106 | 可见 |
| 知识库服务 | 28 | 可见 |
| 证券知识库在线检索接口 | 18 | 可见 |
| 债券 | 87 | 可见 |
| 基金 | 32 | 可见 |
| 指数 | 5 | 可见 |
| ENGLISH APIS | 220 | 可见 |
| 深证信量化数据服务 | 26 | 可见 |
| 新闻研报 | 9 | 可见 |
| 工商大数据 | 46 | 可见 |
| 拟上市公司数据 | 17 | 可见 |
| 深证信专题数据服务 | 83 | 可见 |
| 深证信金融科技专区 | 2 | 可见 |
| ESG专题数据 | 5 | 可见 |
| TTM | 10 | 可见 |
| 指数样本 | 1 | 可见 |
| 海外数据 | 749 | 隐藏 |
| 宏观数据 | 67 | 隐藏 |
| 证券提示库数据服务 | 12 | 隐藏 |
| 深证信VIP数据服务 | 27 | 隐藏 |
| 深证信专业订制数据 | 58 | 隐藏 |
| 数据浏览器 | 27 | 隐藏 |
| 专题统计 | 76 | 隐藏 |
| 内部服务-服务平台接口 | 242 | 隐藏 |
| 巨潮网使用接口 | 200 | 隐藏 |
| 第三方数据 | 7 | 隐藏 |
| 小巨人 | 3 | 隐藏 |
| 产业链数据服务 | 4 | 隐藏 |
| 上市公司官网嵌入服务 | 17 | 隐藏 |

## 公共信息

### 公共信息Api

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_public0001` | 交易日历数据 | `stock/p_public0001` | `0bf76273eb724e38bf32c30cfac5ddda` |
| `p_public0002` | 行业分类数据 | `stock/p_public0002` | `04add00012fc4101bb2e2303b314a6d7` |
| `p_public0003` | 地区分类数据 | `stock/p_public0003` | `361a41a0ce5146db9f5675e2a7d2e371` |
| `p_public0005` | 证券类别编码数据 | `public/p_public0005` | `57aab6472d7d434e91aeab51f2a56586` |
| `p_public0006` | 公共编码数据 | `public/p_public0006` | `577bb53e77984aa9b92c3f843013a39d` |
| `p_public0007` | 人民币汇率中间价 | `public/p_public0007` | `f694148a21e146d39f9297b882eefdcc` |
| `p_public0009` | 机构信息数据 | `public/p_public0009` | `cb9b62f3820c4815b2c86f8033eb406e` |

## 公司数据

### 沪深北上市公司

#### 上市公司全量数据

##### 上市公司基础数据

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

##### 上市公司财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_rzrq3104` |  融资融券明细数据 | `stock/p_rzrq3104` | `6e9e5d07f7dc42e1a69dae2ce82da33f` |
| `p_rzrq3106` | 单一股票质押比例 | `stock/p_rzrq3106` | `fe029a72e7fc4b5da736a62e8b7de0ec` |
| `p_stock2202` | 证券交易特别提示 | `stock/p_stock2202` | `f968156887bd46319d98a31b93c25d4a` |
| `p_stock2204` | 沪深异动证券公开信息 | `stock/p_stock2204` | `7958c463073c4f8da684e43b8d1bc60c` |
| `p_stock2401` | 股票最新日行情 | `stock/p_stock2401` | `f16b697db4724bc69f972fa291d03d12` |
| `p_stock2402` | 股票历史日行情 | `stock/p_stock2402` | `c3c41c16bf0f420e863fdad34b0d6648` |
| `p_stock2406` | 证券复权因子 | `stock/p_stock2406` | `19affbd27dc94fe1be8fe356a1579f66` |
| `p_stock2416` | 大宗交易数据 | `stock/p_stock2416` | `4cb90e94909f489592f4ab9e201bac62` |
| `p_stock2426` | 多市场交易日报 | `stock/p_stock2426` | `b51f2add2fc140158d820a36c8ddabd6` |

##### 上市公司股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司重大事项

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2222` | 股东大会召开情况 | `stock/p_stock2222` | `9afafd22fb6044a5af05506fe67d1d1f` |
| `p_stock2223` | 股东大会议案 | `stock/p_stock2223` | `29d6a4172d274db69f4267b87931738c` |
| `p_stock2224` | 股东大会相关事项变动 | `stock/p_stock2224` | `e5a75dbe084a4bf8a44a00e6d813a505` |
| `p_stock2245` | 对外担保 | `stock/p_stock2245` | `69c376374137446e9e8ec046bc8b52ca` |
| `p_stock2246` | 公司诉讼 | `stock/p_stock2246` | `deb2a395fede4fdea309f8d4d70b48b9` |
| `p_stock2248` | 公司受处罚表 | `stock/p_stock2248` | `d65cb2deaf6049a4a4ca98ba474f3d3b` |
| `p_stock2249` | 公司资产冻结表 | `stock/p_stock2249` | `8ee3bcd6855b4cf9b6a084c52cb76647` |
| `p_stock2250` | 公司仲裁 | `stock/p_stock2250` | `75161e27e03347df97d7732d2bfdc22a` |

##### 上市公司分红及募资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司公告资讯

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3015` | 公告基本信息 | `info/p_info3015` | `a0fec4cde3bf4f83821fb5a769231100` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |

#### 上市公司增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sub_latest_status` | 接口最新更新状态 | `load/p_sub_latest_status` | `8976a5662c5a4d6eb61b225cabe765d4` |

##### 上市公司基础数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2100_inc` | 公司基本信息 | `load/p_stock2100_inc` | `7e33330155c1477d80b9a10ccb9d3d6e` |
| `p_stock2101_inc` | 股票基本信息 | `load/p_stock2101_inc` | `e5ed155b084b48f19995537f4c95bd89` |
| `p_stock2102_inc` | 公司管理人员任职情况 | `load/p_stock2102_inc` | `63c700e98cb84d8eb01461190229af64` |
| `p_stock2107_inc` | 公司员工情况表 | `load/p_stock2107_inc` | `cc7d367dcf054e789512516f8519644e` |
| `p_stock2108_inc` | 机构基本信息变更情况 | `load/p_stock2108_inc` | `474f9487dff44d6dbddda141c1e905c1` |
| `p_stock2109_inc` | 证券简称变更情况 | `load/p_stock2109_inc` | `b7018c59fc3445d493669cd5e2115c77` |
| `p_stock2110_inc` | 上市公司行业归属的变动情况 | `load/p_stock2110_inc` | `5988bbaf78294be2868b572623765499` |
| `p_stock2117_inc` | 公司上市状态变动情况表 | `load/p_stock2117_inc` | `b31b833b27b34bee84ec9fda59565cb2` |

##### 上市公司财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2202_inc` | 证券交易特别提示 | `load/p_stock2202_inc` | `696dfef0eb234f2bb69f9281dfbc8e76` |
| `p_stock2204_inc` | 沪深异动证券公开信息 | `load/p_stock2204_inc` | `4f01bfdabb1b4bdf96093e4963bd183f` |
| `p_stock2401_inc` | 股票最新日行情 | `load/p_stock2401_inc` | `d8c818f61e914321973602788a14796f` |
| `p_stock2402_inc` | 股票历史日行情 | `load/p_stock2402_inc` | `c0fdfe80ea644bcebdd11e3c4c78c7c5` |
| `p_stock2406_inc` | 证券复权因子 | `load/p_stock2406_inc` | `83c13a379e6b47969f46871da7c282df` |

##### 上市公司股本股东数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司重大事项数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2222_inc` | 股东大会召开情况 | `load/p_stock2222_inc` | `ed05dd045c224683859ed2b69414e837` |
| `p_stock2223_inc` | 股东大会议案 | `load/p_stock2223_inc` | `021699a888ac40e180a514fa5fa514d4` |
| `p_stock2224_inc` | 股东大会相关事项变动 | `load/p_stock2224_inc` | `b08fb71abba14c9281f726165de7d64f` |
| `p_stock2245_inc` | 对外担保 | `load/p_stock2245_inc` | `ba2018662069440fb663889ccb04c044` |
| `p_stock2246_inc` | 公司诉讼 | `load/p_stock2246_inc` | `ec336c16fadb43c1922bb05014f2cd39` |
| `p_stock2248_inc` | 公司受处罚表 | `load/p_stock2248_inc` | `4397edd3f2394dc09080e1e10ec3e322` |
| `p_stock2249_inc` | 公司资产冻结表 | `load/p_stock2249_inc` | `8f5fd23e8f3f484b8ebd6179d5e4ecd2` |
| `p_stock2250_inc` | 公司仲裁 | `load/p_stock2250_inc` | `7734877116bf4c1eaa86b7ab8cfc83c1` |

##### 上市公司分红募资数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

##### 上市公司并购重组数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

#### 财务附注全量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

#### 财务附注增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 新三板公司

#### 新三板基础数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

#### 新三板股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6010` | 新三板公司股本变动表 | `neeq/p_neeq6010` | `e985ec79b9d14d2ca1dade597867ac6d` |
| `p_neeq6013` | 新三板公司十大股东表 | `neeq/p_neeq6013` | `1108eda012294889bd27833f6249437d` |
| `p_neeq6026` | 新三板公司股东人数 | `neeq/p_neeq6026` | `ffa625ff85aa44399ee308a48de0c172` |

#### 新三板分红送配

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6014` | 新三板公司分红转增 | `neeq/p_neeq6014` | `d3fd168769124505ae42deaf7864785d` |

#### 新三板重大事项

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6016` | 新三板公司股东大会召开情况 | `neeq/p_neeq6016` | `8fa75138f2f54fd5844768db181746e8` |
| `p_neeq6022` | 新三板公司股东大会议案表 | `neeq/p_neeq6022` | `c7a5620fb0e64b37908764a4f9c21a9e` |
| `p_neeq6023` | 新三板公司受限股份实际解禁日期表 | `neeq/p_neeq6023` | `fe8a1a1cec0144f39680a7ea1267c2ca` |

#### 新三板发行募资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6024` | 新三板公司增发股票预案表 | `neeq/p_neeq6024` | `a002bed3cf1d4625aab624899a650ad6` |
| `p_neeq6025` | 新三板公司增发股票实施方案 | `neeq/p_neeq6025` | `11be447254d24f02a45301239555b116` |

#### 新三板行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6028` | 新三板股份报价日行情信息 | `neeq/p_neeq6028` | `98c49db2f12447dd99615883b562a2de` |

#### 新三板财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6015` | 新三板公司定期报告审计意见 | `neeq/p_neeq6015` | `854b726e977c4f479f4a13345119b410` |
| `p_neeq6017` | 新三板公司通用主要财务指标 | `neeq/p_neeq6017` | `4042fe32eeff49d2a011eea7351f711e` |
| `p_neeq6018` | 新三板公司通用资产负债表 | `neeq/p_neeq6018` | `aea1337f05bd446e84af166a2197188d` |
| `p_neeq6019` | 新三板公司通用利润表 | `neeq/p_neeq6019` | `453eed44893c4ed7a94426f93b8cba88` |
| `p_neeq6020` | 新三板公司通用现金流量表及补充资料表 | `neeq/p_neeq6020` | `6f6ecbf51c2447e5b8b94c74d5b0f640` |
| `p_neeq6021` | 新三版财务衍生指标数据 | `neeq/p_neeq6021` | `9622a5fe38b34832ad92204bd94fab7b` |

#### 新三板公告资讯

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3014` | 新三板公告信息 | `info/p_info3014` | `64dab2ef2f95445dad641bd63d025c5b` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |

#### 新三板-辅助信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_public0002` | 行业分类数据 | `stock/p_public0002` | `04add00012fc4101bb2e2303b314a6d7` |
| `p_public0003` | 地区分类数据 | `stock/p_public0003` | `361a41a0ce5146db9f5675e2a7d2e371` |
| `p_public0006` | 公共编码数据 | `public/p_public0006` | `577bb53e77984aa9b92c3f843013a39d` |

#### 新三板增量数据

##### 新三板增量财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6015_inc` | 新三板公司定期报告审计意见 | `load/p_neeq6015_inc` | `b1c9b55482bb45218f924cf22bba9375` |
| `p_neeq6017_inc` | 新三板公司通用主要财务指标 | `load/p_neeq6017_inc` | `c2be8b6d317f4003bfd143f9c6bab0e7` |
| `p_neeq6018_inc` | 新三板公司通用资产负债表 | `load/p_neeq6018_inc` | `1c08487df93e4e0280f17566255e6579` |
| `p_neeq6019_inc` | 新三板公司通用利润表 | `load/p_neeq6019_inc` | `f7335d8df95d41fd9e47de136ca13c31` |
| `p_neeq6020_inc` | 新三板公司通用现金流量表及补充资料表 | `load/p_neeq6020_inc` | `d1e78186eefd41868fa07cc143f35183` |
| `p_neeq6021_inc` | 新三版财务衍生指标数据 | `load/p_neeq6021_inc` | `3eb654321ae942db951f2bae60f6e3b8` |

### 港股上市公司

#### 港股-基本数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_hk4001` | 港股公司概况 | `hk/p_hk4001` | `67b27bc83ca94f2aa773fc1c878b6935` |
| `p_hk4009` | 港股董事及高级管理人员简历 | `hk/p_hk4009` | `3234db6f51954ef9a449598ad2de7f6d` |
| `p_hk4010` | 主要股东股权变动 | `hk/p_hk4010` | `e448ebbd35e04caeb7e379dc49fbc1bc` |
| `p_hk4011` | 董事任职变动 | `hk/p_hk4011` | `c6fef91e428049c0a8fa8808b100c57f` |
| `p_hk4039` | 港股证券信息表 | `hk/p_hk4039` | `65c7f0b440464741aecd8366ca4c45d3` |
| `p_hk4042` | 股东持股资料表 | `hk/p_hk4042` | `134e707c7fff4950ae4a8225fd28b64d` |
| `p_hk4043` | 高管持股变动表 | `hk/p_hk4043` | `0e7f169d21754656ac0d67869fc7422b` |
| `p_hk4045` | 港股股本表 | `hk/p_hk4045` | `0cd0027a859e4584aff0d79d8da234e6` |
| `p_hk4049` | 港股市值指标 | `hk/p_hk4049` | `4263490ce1ab45f9b7f37ef4ce72e736` |

#### 港股-财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_hk4008` | 港股业绩公布预告 | `hk/p_hk4008` | `35073701934d43a1914ef25bf94cdc7f` |
| `p_hk4019` | 现金流量表(通用) | `hk/p_hk4019` | `5ad4b4b0ff59409982311aa3ea86e90b` |
| `p_hk4020` | 资产负债表(银行) | `hk/p_hk4020` | `344b5a045cb24e0b9276b1f973b85625` |
| `p_hk4021` | 综合损益表(银行) | `hk/p_hk4021` | `fcf776ed9b6b48b19d96097853b31daf` |
| `p_hk4022` | 重要指标表（银行） | `hk/p_hk4022` | `3835146015a34d6598a7c3e1cde8804d` |
| `p_hk4023` | 资产负债表(非银行) | `hk/p_hk4023` | `1b53fca9f8b04e1c847d0b679a3563b0` |
| `p_hk4024` | 综合损益表(非银行) | `hk/p_hk4024` | `6de15be9f2244a1a888ce1707de964c6` |
| `p_hk4025` | 重要指标表（非银行） | `hk/p_hk4025` | `18db744911e74cdb9ef8e1130e06c8b5` |

#### 港股-行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

#### 港股-重要指标

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_hk4015` | 香港新股发行参与各方表 | `hk/p_hk4015` | `fb4741a224f64757ac2a761a32f3e4bc` |
| `p_hk4017` | 港股股本表 | `hk/p_hk4017` | `d761cdfae4b442a4ab746b2a657fe191` |
| `p_hk4018` | 分红派息表 | `hk/p_hk4018` | `a0097b7038ed43ffa453a4dc8f25e7b1` |

#### 港股-重大事项

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_hk4002` | 港股业务回顾 | `hk/p_hk4002` | `b19c3402ee5448d9b504248e3121572f` |
| `p_hk4003` | 港股业务展望 | `hk/p_hk4003` | `da4a818c3c834ef5871f310334566859` |
| `p_hk4006` | 港股公司停牌 | `hk/p_hk4006` | `c7d6319b90244590a2edef3db0d33600` |
| `p_hk4007` | 港股公司复牌 | `hk/p_hk4007` | `7290d8950bac4ea4baa6f6996ba6df65` |
| `p_hk4013` | 股份回购 | `hk/p_hk4013` | `f50ee6e48f3045f2a95e5dfdebeef9a6` |
| `p_hk4014` | 股份卖空 | `hk/p_hk4014` | `6d8ff36327c04f85a56182521ad9341b` |

#### 港股-公司行为

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 北交所公司

#### 北交所公司财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

## 公告资讯

### PDF公告

#### 上市公司公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3015` | 公告基本信息 | `info/p_info3015` | `a0fec4cde3bf4f83821fb5a769231100` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3085` | 上市公司公告(DataCloud) | `info/p_info3085` | `8b5bc11ae8984aec8d78b7f934791f44` |
| `p_info3092` | 深沪北交易所临时停牌公告 | `info/p_info3092` | `dfb32325f1894591bc945ee6ab678283` |
| `p_info3125` | 新增再融资/重大资产重组/转板公告 | `info/p_info3125` | `d77788ae3ce24d4d96ba11c87e624696` |
| `p_info3125t` | 最新再融资/重大资产重组/转板PDF公告 | `info/p_info3125t` | `f2504b377ed84edf98e5727a324be179` |

#### 基金公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3011` | 基金公告信息表 | `info/p_info3011` | `d37f45e94bfb4c318d7ec934f5910cb6` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |

#### 债券公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

#### 港股公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3005` | 公告分类信息 | `info/p_info3005` | `89f5d71e8ddd4422bb91d1e89516192b` |
| `p_info3013` | 港股公告数据 | `info/p_info3013` | `3161b164a72b40ec8d26bbb266d29b70` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |
| `p_info3023` | 港股中英文公告 | `info/p_info3023` | `accac5bd04d5415ba4af96ef22684f2f` |
| `p_info3024` | 港股中英文公告 | `info/p_info3024` | `cf4b0c8397de416fae4268df11168834` |
| `p_info3065` | 港股IPO公告 | `info/p_info3065` | `2e39ec9f5f9348fb9f23eddb6f14b97b` |

#### 预披露公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3060` | 预披露公告 | `info/p_info3060` | `37f15dbddf044179a33e13f7936b5eed` |
| `p_info3062` | 预披露-定制 | `info/p_info3062` | `07a5cef02109449f8f9ac7cd933f124e` |
| `p_info3065` | 港股IPO公告 | `info/p_info3065` | `2e39ec9f5f9348fb9f23eddb6f14b97b` |
| `p_info3072` | 港股预披露公告 | `info/p_info3072` | `b96cc75e46484301aeeaf8747bf7d9e0` |

#### 新三板公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3014` | 新三板公告信息 | `info/p_info3014` | `64dab2ef2f95445dad641bd63d025c5b` |

#### 四板公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3061` | 四板公告 | `info/p_info3061` | `a5b00692329a46c6b5d23bc606d34c02` |

#### 其他公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3016` | 其他公告信息 | `info/p_info3016` | `c794a864abb242fea2f08527b455ffcf` |
| `p_info3063` | 监管机构公告 | `info/p_info3063` | `024698146b7f47938f43120be19e1847` |
| `p_info3064` | 交易所问询函 | `info/p_info3064` | `93032df83b9d4dd4a30b21bf96ecf144` |
| `p_info3076` | 辅导企业公告 | `info/p_info3076` | `f0f91648b59f4a2cb8db2ece57daa889` |
| `p_info3089` | 英文监管动态 | `info/p_info3089` | `f9d67cf6e5ca4466b0f757fa2739e992` |
| `p_info3095` | 地方证监局监管动态公告 | `info/p_info3095` | `11db51f866b946cfbe316d376764b924` |

#### 深市摘要

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3067` | 深市公告摘要 | `info/p_info3067` | `a61dd57ad1c649edaae4745acadadd48` |

### 最新PDF公告

#### 最新上市公司PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3085t` | 最新深沪北上市公司PDF公告 | `info/p_info3085t` | `341141e24b3e413a9ef12d60675e21e2` |
| `p_info3085t_inc` | 最新深沪北上市公司PDF增量公告 | `load/p_info3085t_inc` | `d079293ff21547c1a1dc1e82f1ba0c02` |
| `p_info3125t` | 最新再融资/重大资产重组/转板PDF公告 | `info/p_info3125t` | `f2504b377ed84edf98e5727a324be179` |

#### 最新基金PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3011_inc` | 最新基金PDF增量公告 | `load/p_info3011_inc` | `f64337b5a7174d109b79c7f28a1a4912` |
| `p_info3011t` | 最新基金PDF公告 | `info/p_info3011t` | `563c0d71f914431aa66a4de754ca32e8` |
| `p_info3011t_inc` | 最新基金PDF增量公告 | `load/p_info3011t_inc` | `20b512c5bc8b4c2da66933f56922d64f` |

#### 最新债券PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3012t` | 最新债券PDF公告 | `info/p_info3012t` | `736f28a3ba99426aba621448a9914847` |
| `p_info3012t_inc` | 最新债券PDF增量公告 | `load/p_info3012t_inc` | `cf25f7c3c2f4402493b56782338c3c49` |
| `p_info3066t` | 最新银行间PDF公告 | `info/p_info3066t` | `f68589d2b9bc46ce925e2adbd3af7a8b` |
| `p_info3066t_inc` | 最新银行间PDF增量公告 | `load/p_info3066t_inc` | `fe354390e49a4d7e858364a1dde5cf3b` |
| `p_info3171t` | 银行间债券(债项维度)公告 | `info/p_info3171t` | `0331eae199ea46dea66523ac63faf28f` |

#### 最新港股PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3024t` | 最新港股中英文PDF公告 | `info/p_info3024t` | `c0b55dd1941b4ac88ca87697c328ed2e` |
| `p_info3024t_inc` | 最新港股中英文PDF增量公告 | `load/p_info3024t_inc` | `a897879cb25d4b1eb1b373d6080b1fa7` |

#### 最新预披露PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3060t` | 最新预披露PDF公告 | `info/p_info3060t` | `270c8c92e4d946fda216a63c9b3e3561` |
| `p_info3060t_inc` | 最新预披露PDF增量公告 | `load/p_info3060t_inc` | `38666ae4af2f403486aa23788e95a1e7` |
| `p_info3072t` | 最新港股预披露PDF公告 | `info/p_info3072t` | `8503d5dfac254f7885db3efa00ff1ea8` |
| `p_info3072t_inc` | 最新港股预披露PDF增量公告 | `load/p_info3072t_inc` | `82fe7dabf41540ccb8d7c490a454076e` |

#### 最新新三板PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3014t` | 最新新三板PDF公告 | `info/p_info3014t` | `963958ab8078462f914330beef2198cb` |
| `p_info3014t_inc` | 最新新三板PDF增量公告 | `load/p_info3014t_inc` | `7272e11a333f42e684cb42c1386516e7` |

#### 最新四板PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3061t` | 最新四板PDF公告 | `info/p_info3061t` | `a105e7f8ee9a425193a496d9982f8236` |
| `p_info3061t_inc` | 最新四板PDF增量公告 | `load/p_info3061t_inc` | `0d41943f76924a8497c17cca9b57a95c` |

#### 最新其他PDF公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3063t` | 最新监管机构PDF公告 | `info/p_info3063t` | `78d4e7042c2848c7b04e7e4eccb8efe8` |
| `p_info3063t_inc` | 最新监管机构PDF增量公告 | `load/p_info3063t_inc` | `0d8c05d6f6cf4e0c9914372deda44564` |
| `p_info3064t` | 最新交易所PDF问询函 | `info/p_info3064t` | `b87cfa1335a64ad195e3afb19943fb91` |
| `p_info3064t_inc` | 最新交易所PDF增量问询函 | `load/p_info3064t_inc` | `099dbda84a6a4b10999e625f95446637` |
| `p_info3076t` | 最新辅导企业PDF公告 | `info/p_info3076t` | `6597fcade2c746a5b58ddcd4e661b73d` |
| `p_info3076t_inc` | 最新辅导企业PDF增量公告 | `load/p_info3076t_inc` | `960d0a1fbb924411851b6b554648e5d1` |
| `p_info3095t` | 最新地方证监局监管动态PDF公告 | `info/p_info3095t` | `c545952540f749eca96620c100e50703` |

### 最新PDF公告无历史

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3024c` | 最新港股中英文PDF公告无历史 | `info/p_info3024c` | `d2ad6da5fb6b42ac84469939cf598392` |
| `p_info3085c` | 最新深沪北上市公司PDF公告无历史 | `info/p_info3085c` | `194ab2863ef7479d994919279ec94ecc` |

### H5公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 最新H5公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 最近半年H5公告

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3185c` | 最近半年深沪北上市公司H5公告 | `info/p_info3185c` | `d5628ea1ef2a44c1b64794bdf1999b55` |

### 公告推送

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3011_client` | 基金公告信息表 | `info/p_info3011_client` | `842e1c51a4164577a92a14e20009d720` |
| `p_info3012_client` | 债券公告信息表 | `info/p_info3012_client` | `0131dc4abcec4f0e8bfb31737beddc71` |
| `p_info3013_client` | 港股公告数据  | `info/p_info3013_client` | `09999b995526445abe096e4aefd734d8` |
| `p_info3014_client` | 新三板公告信息 | `info/p_info3014_client` | `d8fbec1e475545db95152845af370723` |
| `p_info3015_client` | 公告基本信息 | `info/p_info3015_client` | `4509a59fce294f57bf7007b854709b17` |
| `p_info3085_client` | 上市公司公告(DataCloud) | `info/p_info3085_client` | `4b4ebc4052274398bbd43840e1f6f77b` |
| `p_info3085_inc` | 沪深AB股公告基本信息 | `load/p_info3085_inc` | `aef4747e8d46433d975305638a1834a1` |
| `p_info3171_client` | 银行间债券(债项维度)公告 | `info/p_info3171_client` | `699c9347bfe7499f97d835877f6be2c5` |

### 智能资讯

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3035` | 数据智能资讯 | `info/p_info3035` | `1bd92189272d4eb1bb16985bcb9e09b0` |
| `p_info3079_AI` | 港股智能资讯接口 | `info/p_info3079_AI` | `24e2f94faa544fe594ecce77166cc13b` |
| `p_info3086` | 行情资讯 | `info/p_info3086` | `164da388d2c241c58275d11965b64636` |
| `p_info3087` | 市场动态资讯 | `info/p_info3087` | `97acc2ac50994049b7973d72cb25f528` |
| `p_info3088` | 港股行情资讯 | `info/p_info3088` | `ffcf1b84aa754eeb9236ab41eb38fb37` |
| `p_info3091` | 上市公司互动信息智能摘要 | `info/p_info3091` | `68d977f1d3f14779b98b9012566d35b0` |
| `p_info3139` | 上市公司互动信息明细 | `info/p_info3139` | `397d4be050a24922866d35f5e7ea61a5` |

## 知识库服务

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_know3011t` | 公募基金公告语料接口 | `info/p_know3011t` | `8e9c3a9774774505932173bab085412d` |
| `p_know3012t` | 交易所债券公告语料接口 | `info/p_know3012t` | `3c436f095cca4cacb142aae1cf9329ab` |
| `p_know3014t` | 股转市场公告语料表接口 | `info/p_know3014t` | `fc8da5bb21e143c28c61a74d08a30a4e` |
| `p_know3024t` | 港交所公告语料表接口 | `info/p_know3024t` | `224a6c46a4ec413ea0f0660b9e963f1e` |
| `p_know3032t` | 研究报告语料 | `info/p_know3032t` | `9590a8a7e6f048f1a65f05fd659e149d` |
| `p_know3060t` | 深沪北交易所IPO预披露公告语料接口 | `info/p_know3060t` | `51b942499d784667ad9137c088fc6f6f` |
| `p_know3061t` | 地方股权（四板）公告语料表 | `info/p_know3061t` | `8f2f764b20f34fb38a5d0455fa64061d` |
| `p_know3063t` | 监管动态公告语料表 | `info/p_know3063t` | `a560e1f9214d403aabb6d4cfa43c30af` |
| `p_know3064t` | 监管函件公告语料 | `info/p_know3064t` | `c4a1e45459b24f4d8f249ef11f086956` |
| `p_know3076t` | 各地证监局辅导企业公告语料 | `info/p_know3076t` | `339ab567374941269b2fea9cb51c6c36` |
| `p_know3085t` | 上市公司公告语料 | `info/p_know3085t` | `c418c679d79447f2bcf6738bf3ba591b` |
| `p_know3095t` | 地方监管公告语料表 | `info/p_know3095t` | `63ccdea8fb134536a8a0bdf896a48ab7` |
| `p_know3125t` | 再融资申报公告语料 | `info/p_know3125t` | `a0631f5cb748402d86a29e483214df65` |
| `p_know3171t` | 银行间交易债券公告语料 | `info/p_know3171t` | `067ee5ad594c4d238bd766223af04764` |

### 全量知识库

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_know3011` | 公募基金公告语料接口 | `info/p_know3011` | `c40f37be88c449f6af2da932740ce1af` |
| `p_know3012` | 交易所债券公告语料接口 | `info/p_know3012` | `c1c8c0e36533405b9fab454cb7a79aa8` |
| `p_know3014` | 股转市场公告语料表接口 | `info/p_know3014` | `3fd7afeedb2843e7b59f657b9dfb1c82` |
| `p_know3024` | 港交所公告语料表接口 | `info/p_know3024` | `727a8877be1f483d8e23c17a84451a77` |
| `p_know3032` | 研究报告语料 | `info/p_know3032` | `01029fc7b2f8427abd4f0852a54e4ca2` |
| `p_know3060` | 深沪北交易所IPO预披露公告语料接口 | `info/p_know3060` | `bfb978764c964e84abd3a6c9706e3bd8` |
| `p_know3061` | 地方股权（四板）公告语料 | `info/p_know3061` | `4a6ea50a57a74ee280af127f58f24183` |
| `p_know3063` | 监管动态公告语料表 | `info/p_know3063` | `d2ec10d7150a44f89ef330ec80dd56ed` |
| `p_know3064` | 监管函件公告语料 | `info/p_know3064` | `d791b09e9ccc4ce4bef37f8827c342f6` |
| `p_know3076` | 各地证监局辅导企业公告语料 | `info/p_know3076` | `8eb2065f5cbd4913880d44534694847f` |
| `p_know3085` | 上市公司公告语料 | `info/p_know3085` | `883bedd5cbb8461ba9ca46cfcb805b47` |
| `p_know3095` | 地方监管公告语料表 | `info/p_know3095` | `dbe7d9d4d86f4d708274efc04e995ca8` |
| `p_know3125` | 再融资申报公告语料 | `info/p_know3125` | `46511856d8b64ad881f23a181921f4a3` |
| `p_know3171` | 银行间交易债券公告语料 | `info/p_know3171` | `244d08bb550b4126babb666b618d7aed` |

## 证券知识库在线检索接口

### 文档知识库在线检索接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `asharesretrieval` | 上市公司公告知识库检索接口 | `/aicloud/asharesretrieval` | `8c8235ca632147699c5ec2cc8b41d347` |
| `bankretrieval` | 银行间交易债券公告知识库检索接口 | `/aicloud/bankretrieval` | `0b0e182961b54d73aaa461c6cc1107f1` |
| `companiestogopublicretrieval` | 各地证监局辅导企业公告知识库检索接口 | `/aicloud/companiestogopublicretrieval` | `a9ee1686737745d2882abd8fde620568` |
| `dynamicsretrieval` | 监管动态公告知识库检索接口 | `/aicloud/dynamicsretrieval` | `404f99e9abe445568a84bb804db9901a` |
| `exchangebondretrieval` | 交易所债券公告知识库检索接口 | `/aicloud/exchangebondretrieval` | `c67583f5403941149ecd1a6110941208` |
| `hongkongretrieval` | 港交所公告知识库检索接口 | `/aicloud/hongkongretrieval` | `33f30214d5cf443987aa113d7b336b99` |
| `letterretrieval` | 监管函件公告知识库检索接口 | `/aicloud/letterretrieval` | `baf2a0726d57499e878004c4d28ec1b4` |
| `localregulatoryannouncementretrieval` | 各地证监局监管公告知识库检索接口 | `/aicloud/localregulatoryannouncementretrieval` | `41e4bf5a91844f699b1dfb0994b3d14d` |
| `mutualfundsretrieval` | 公募基金公告知识库检索接口 | `/aicloud/mutualfundsretrieval` | `9781af1f53e34e5e977c0517f794b0ac` |
| `predisclosureretrieval` | 深沪北交易所IPO预披露公告知识库检索接口 | `/aicloud/predisclosureretrieval` | `aead985e9c4247dca40c489b74cd60fb` |
| `refinancingdeclarationretrieval` | 再融资申报公告知识库检索接口 | `/aicloud/refinancingdeclarationretrieval` | `3266ff61f426447c83fa5908f7e4e4f9` |
| `regionalexchangesretrieval` | 地方股权四板公告知识库检索接口 | `/aicloud/regionalexchangesretrieval` | `6906c0f2e91643e996dbe59d61815278` |
| `researchretrieval` | 研究报告知识库检索接口 | `/aicloud/researchretrieval` | `a90b2df157ce4327b72ad2e4ce599e17` |
| `stockconversionretrieval` | 股转市场公告知识库检索接口 | `/aicloud/stockconversionretrieval` | `0d937eeb746e4b239468a0f1dad8b9cd` |

### 定制化知识库在线检索接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `search_ashares` | search_ashares | `bigdata/search_ashares` | `9b7da3f667364b8c8b8c43f376026f62` |

### 检索测试接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `ai_announcement_extraction` | 公告全文抽取 | `bigdata/ai_announcement_extraction` | `df180aeb82a1444195f5a2f5609ad24b` |
| `ai_announcement_retrieval_prod` | 公告智能检索 | `bigdata/ai_announcement_retrieval_prod` | `5e6fba78263e48da85084f45deb26a02` |
| `industry_nl2api` | NL2API数据查询 | `bigdata/industry_nl2api` | `3012f329ee454b8fa1c415eae5e428c0` |

## 债券

### 债券（固定收益）

#### 债券基础数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2800` | 债券代码对照表 | `bond/p_bond2800` | `38a2520bc1cd4996a2436120cc4c60a4` |
| `p_bond2801` | 债券基本信息 | `bond/p_bond2801` | `7f89fff597fb417186ec149a1a95b7b2` |
| `p_bond2802` | 债券票面利率 | `bond/p_bond2802` | `d0769ce43a9a4664a85037c53c7cdf54` |
| `p_bond2811` | 可转债转股价调整 | `bond/p_bond2811` | `6cead92eeda640528be942d27e302b40` |
| `p_bond2815` | 债券信用评级表 | `bond/p_bond2815` | `ab58e9f052414baea2e436bd9568d296` |
| `p_bond2815_inc` | 债券信用评级表 | `load/p_bond2815_inc` | `82ab13bf74f842d8a0065a98a4a45aba` |
| `p_bond2816` | 债券发行人评级 | `bond/p_bond2816` | `67bf68296257413b98ea5b5f47a8ac23` |
| `p_bond2816_inc` | 债券发行人评级 | `load/p_bond2816_inc` | `395315b311b84216b12d9c763b0a3eac` |
| `p_bond2818` | 债券担保说明 | `bond/p_bond2818` | `b24a199fe2b5467fbbb9e569ac50ecd3` |
| `p_bond2819` | 债券特殊条款 | `bond/p_bond2819` | `397296ee0d224acc857feea4a7770c6d` |
| `p_bond2888` | 债券持有人信息表 | `bond/p_bond2888` | `0a313258e25049e8bb6f9eb27b906eba` |
| `p_bond2891` | 债券违约信息 | `bond/p_bond2891` | `511c8cc2ae9e41ebbb12b799c8686f0a` |
| `p_bond2891_inc` | 债券违约信息 | `load/p_bond2891_inc` | `02a667fc91b04b8f8816525ddb87d4a7` |
| `p_bond2895` | 违约信息 | `bond/p_bond2895` | `4cd6f636f7904851ab78e3914a5fbb93` |
| `p_bond2896` | 违约解决明细 | `bond/p_bond2896` | `e0749afb81bd43e48422778ade90126d` |
| `p_bondcode` | 债券代码维度表 | `bond/p_bondcode` | `07e05580e9bb4d7ea82a63e86acb69e7` |

#### 债券发行付息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2805` | 企业债发行 | `bond/p_bond2805` | `927e59cc2ac342569acb2911ffb56f58` |
| `p_bond2806` | 国债发行 | `bond/p_bond2806` | `90af692c43954f07930d02e5fa570cd1` |
| `p_bond2807` | 可转债发行 | `bond/p_bond2807` | `ae65e4f01ca34c2ba91071991083c319` |
| `p_bond2808` | 债券付息 | `bond/p_bond2808` | `ecbc35a80a2d466094401d5642ff2365` |
| `p_bond2810` | 债券发行中介机构 | `bond/p_bond2810` | `b691b22e7bcd4aa7aa1b54036ac6cc53` |
| `p_bond2821` | 政策性银行债发行 | `bond/p_bond2821` | `f7f986af6b474a738f1cc8fb7a4e6bf9` |
| `p_bond2822` | 资产支持证券发行 | `bond/p_bond2822` | `38a5b702002b40129609c013578cd946` |
| `p_bond2823` | 商业银行债发行 | `bond/p_bond2823` | `3755314d4a3045aba19827ac6c08fb79` |
| `p_bond2824` | 短期融资券、中期票据发行 | `bond/p_bond2824` | `80ebc9c4997b47d282c8928e8ef60279` |
| `p_bond2825` | 央行票据发行 | `bond/p_bond2825` | `314b21875a424bce85829898962b8cec` |
| `p_bond2897` | 债券招标情况 | `bond/p_bond2897` | `fa1a2860249c4e898603bac1a6ef64ab` |
| `p_bond2898` | 发行失败债券基本信息 | `bond/p_bond2898` | `5330a4fc4aec413cae903baa6be487be` |

#### 债券行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2803` | 债券大宗交易 | `bond/p_bond2803` | `3ad2d23bfcbd45b7b31975c2d5085c1a` |
| `p_bond2804` | 债券行情 | `bond/p_bond2804` | `92fb2958fbda498c84d600c01b38e93d` |
| `p_bond2804_inc` | 债券行情增量 | `load/p_bond2804_inc` | `ceb063772c064d269b8bea91f97e6c24` |
| `p_bond2814` | 银行间现券市场汇总行情 | `bond/p_bond2814` | `96e5d3495d47421f9bba9dc7ff23248c` |

#### 债券统计

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2812` | 债券每日统计数据 | `bond/p_bond2812` | `bd8d10a7e74e43e59f5bbbbb7df45b5a` |
| `p_bond2813` | 债券每日成交概况 | `bond/p_bond2813` | `8e659fff2c73456a88138fd21a764e28` |

#### 债券公告资讯

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3012` | 债券公告信息表 | `info/p_info3012` | `65750815e8c747168b9668bcb1e04834` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |

#### 资产支持证券

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2893` | ABS资产池概况 | `bond/p_bond2893` | `5127739bd5af42a88704b0c399a0836a` |
| `p_bond2894` | ABS资产池贷款本金和利息 | `bond/p_bond2894` | `7f3a02617b8c4ff3b6d1ccae9f31a916` |
| `p_bond2899` | 资产支持证券信息 | `bond/p_bond2899` | `f7ccf3c76d2f4afe928450bd97ba79c4` |

### 债券发行企业财务数据

#### 发债企业通用财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2930` | 通用发债企业资产负债表 | `bond/p_bond2930` | `a40e525ab6114155b4d40f440e663f18` |
| `p_bond2931` | 通用发债企业利润表 | `bond/p_bond2931` | `7a556d55af9b401a999caee5a6a74821` |
| `p_bond2932` | 通用发债企业现金流量表 | `bond/p_bond2932` | `d12bfdc51c664584ab1db8b33f33b4ca` |
| `p_bond2948` | 发债企业主要财务指标 | `bond/p_bond2948` | `0b91ee36b93e4a3b92e440085e2760c0` |

#### 发债企业银行财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2933` | 银行发债企业资产负债表 | `bond/p_bond2933` | `209739211a414317931673de5eba4ef3` |
| `p_bond2934` | 银行发债企业利润表 | `bond/p_bond2934` | `56bd0bd24db84954bd836164f91e581a` |
| `p_bond2935` | 银行发债企业现金流量表 | `bond/p_bond2935` | `68e283f745914612b59647a2fcbe82db` |
| `p_bond2950` | 银行发债企业专项指标 | `bond/p_bond2950` | `744df555283b4a4db3a84cdbd6d9fa01` |

#### 发债企业保险财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2936` | 保险发债企业资产负债表 | `bond/p_bond2936` | `82bc1158935d43adad27c227c325f251` |
| `p_bond2937` | 保险发债企业利润表 | `bond/p_bond2937` | `ec39d0209d6145efaaefffb7045bc950` |
| `p_bond2938` | 保险发债企业现金流量表 | `bond/p_bond2938` | `6e28d959aa3b4bcea621387055d47e57` |

#### 发债企业证券财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2939` | 证券发债企业资产负债表 | `bond/p_bond2939` | `fd5c0447eb1443b6a6cf5f9df1f17db4` |
| `p_bond2940` | 证券发债企业利润表 | `bond/p_bond2940` | `1e784b84405c4ff18b10a25d570f40ef` |
| `p_bond2941` | 证券发债企业现金流量表 | `bond/p_bond2941` | `bced3b368e244b8283b7ef746711cefb` |
| `p_bond2951` | 证券发债企业专项指标 | `bond/p_bond2951` | `5b02c66ac9834e29a871076b7fb3dd33` |

#### 发债企业信托财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2942` | 信托发债企业资产负债表 | `bond/p_bond2942` | `9354b9f99ac14edf984a0715159da7cd` |
| `p_bond2943` | 信托发债企业利润表 | `bond/p_bond2943` | `85bc29e81e784e57bddfe6ae43305166` |
| `p_bond2944` | 信托发债企业现金流量表 | `bond/p_bond2944` | `b304f2dad72a44eb9a96adb9a129bccd` |
| `p_bond2952` | 信托发债企业专项指标 | `bond/p_bond2952` | `e0277a644424463087cf56c6678acd93` |

#### 发债企业财务公司数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2945` | 财务公司发债企业资产负债表 | `bond/p_bond2945` | `cb6f6f4bfe2642ec8580e2953b9ceb6b` |
| `p_bond2946` | 财务公司发债企业利润表 | `bond/p_bond2946` | `485bbd761813448293ce0c3923c159ae` |
| `p_bond2947` | 财务公司发债企业现金流量表 | `bond/p_bond2947` | `005925e089b24c3598ccda31c007e157` |

#### 发债企业衍生财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2949` | 发债企业衍生财务指标 | `bond/p_bond2949` | `84eaf7de8e984266a77967cce3dd447a` |
| `p_bond2953` | 发债企业衍生财务指标副表 | `bond/p_bond2953` | `91471f02eaf6448ebbcf4de14806e332` |

### 债券发行企业财务增量数据

#### 发债企业通用财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2930_inc` | 通用发债企业资产负债表 | `load/p_bond2930_inc` | `06d86046722d4397844666f58edd42b9` |
| `p_bond2931_inc` | 通用发债企业利润表 | `bond/p_bond2931_inc` | `2ed74076876a4651b5b4a5907476254c` |
| `p_bond2932_inc` | 通用发债企业现金流量表 | `bond/p_bond2932_inc` | `12854f5ea92c4a19b0eb41fa8cce059b` |

#### 发债企业银行财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2933_inc` | 银行发债企业资产负债表 | `bond/p_bond2933_inc` | `6e503bb1d68d4e5a99de913b63b8da8c` |
| `p_bond2934_inc` | 银行发债企业利润表 | `bond/p_bond2934_inc` | `1cb684e494244cff90728167c0d850fb` |
| `p_bond2935_inc` | 银行发债企业现金流量表 | `bond/p_bond2935_inc` | `b8f8d5e9d44c4eb0a9aae46ffc464e57` |
| `p_bond2950_inc` | 银行发债企业专项指标 | `bond/p_bond2950_inc` | `cc5d8e221f2f4e0e9ee7b83936833bd0` |

#### 发债企业保险财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2936_inc` | 保险发债企业资产负债表 | `bond/p_bond2936_inc` | `61e4a3b16f4649e68f224241008dc405` |
| `p_bond2937_inc` | 保险发债企业利润表 | `bond/p_bond2937_inc` | `94d64256f80d45d2ab8c5724247c4c43` |
| `p_bond2938_inc` | 保险发债企业现金流量表 | `bond/p_bond2938_inc` | `877158aee88a4c2d88ad64371a5ac574` |

#### 发债企业证券财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2939_inc` | 证券发债企业资产负债表 | `bond/p_bond2939_inc` | `875b7e409cfd48b9b245872d8ceeee72` |
| `p_bond2940_inc` | 证券发债企业利润表 | `bond/p_bond2940_inc` | `eb5181ba682f470aa6050241035c6a52` |
| `p_bond2941_inc` | 证券发债企业现金流量表 | `bond/p_bond2941_inc` | `f115959bc9434428adca65c05400a508` |
| `p_bond2951_inc` | 证券发债企业专项指标 | `bond/p_bond2951_inc` | `356993807f86438b95dfca64982dc68e` |

#### 发债企业信托财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2942_inc` | 信托发债企业资产负债表 | `bond/p_bond2942_inc` | `9776decb4cb04b45a57503a56c71a132` |
| `p_bond2943_inc` | 信托发债企业利润表 | `bond/p_bond2943_inc` | `065551ec0cba40578e08ae54fe275168` |
| `p_bond2944_inc` | 信托发债企业现金流量表 | `bond/p_bond2944_inc` | `8c457aa8be4e4eb3b03d65c5931ce5f3` |
| `p_bond2952_inc` | 信托发债企业专项指标 | `bond/p_bond2952_inc` | `50719a169159442283bf84d86ae7e777` |

#### 发债企业财务公司增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2945_inc` | 财务公司发债企业资产负债表 | `bond/p_bond2945_inc` | `7164064dc33b417bafde89f6b1b9d510` |
| `p_bond2946_inc` | 财务公司发债企业利润表 | `bond/p_bond2946_inc` | `9fc7ded4c23a4c4ba495698917d52090` |
| `p_bond2947_inc` | 财务公司发债企业现金流量表 | `bond/p_bond2947_inc` | `4419f68e57a64ce4925c279175a93201` |

#### 发债企业衍生财务增量数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2949_inc` | 衍生发债企业财务指标 | `bond/p_bond2949_inc` | `3d53cb661d574da8b0a700025d64b3ed` |
| `p_bond2953_inc` | 衍生发债企业财务指标副表 | `bond/p_bond2953_inc` | `323a9ff0b9fb435c832b5e1909b6cbd0` |

### 债券估值

#### 债券估值

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bondvaluation` | 债券估值 | `bond/p_bondvaluation` | `fa3f1bb97f094036b0f2b7135d34d39a` |

## 基金

### 基础库-基金基础信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_fund2600` | 基金基本信息 | `fund/p_fund2600` | `532886967fe24dc1b04d910fb0f580d3` |
| `p_fund2600_inc` | 基金基本信息 | `load/p_fund2600_inc` | `75aba558b657431988c5ed19ccf756a3` |
| `p_fund2602` | 基金管理公司基本信息 | `fund/p_fund2602` | `c058a3a4730c45998c152589787ec834` |
| `p_fund2603` | 基金管理公司股东 | `fund/p_fund2603` | `74e0e78bc6494fef8f5fb33bf7183a66` |
| `p_fund2604` | 基金经理任职情况 | `fund/p_fund2604` | `9d1b70c3668a4b428e0f99b743497083` |
| `p_fund2607` | 基金发行相关中介机构 | `fund/p_fund2607` | `106e837544a8472883fa30c27ca89b9b` |
| `p_fund2608` | 开放式基金份额变动情况 | `fund/p_fund2608` | `1b0556a86259426280b99f8d3c53779c` |
| `p_fund2609` | 开放式基金募集情况 | `fund/p_fund2609` | `63fdd20bb4e944b28caca992852758f6` |

### 基础库-基金净值

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_fund2611` | 基金净值 | `fund/p_fund2611` | `3b1b9349c44949efaad35a6c20d143f6` |
| `p_fund2616` | 货币基金收益日报 | `fund/p_fund2616` | `2f52047a8289402f9c9363abf45d12ec` |
| `p_fund2634` | 基金日行情数据 | `fund/p_fund2634` | `20380d4fccaf41e599de729fa72a67dd` |

### 基础库-基金财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_fund2610` | 基金主要财务指标2009版 | `fund/p_fund2610` | `7534b844b84049d08edc0d8a1cfabade` |
| `p_fund2614` | 基金经营业绩及收益分配表2009版 | `fund/p_fund2614` | `ff180efe3e0f4e77a6a1008803fa49f5` |
| `p_fund2615` | 基金资产负债表2009版 | `fund/p_fund2615` | `ee4d2c7014f247b0aeb046279e4327ba` |

### 基础库-基金投资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_fund2617` | QDII前五名金融衍生品投资明细 | `fund/p_fund2617` | `1220d1c6d2b848bd975293851be7b927` |
| `p_fund2618` | QDII前十名基金投资明细 | `fund/p_fund2618` | `aaa906d62acc4bd79084d93ec0a9a7c4` |
| `p_fund2619` | QDII按债券信用等级分类的债券投资组合 | `fund/p_fund2619` | `baa8995d79924b88a90560fa3e2d7261` |
| `p_fund2620` | QDII股票及存托凭证投资分布——国家（地区） | `fund/p_fund2620` | `0574a5be90404a048dc390b310f630e9` |
| `p_fund2621` | 基金前十名持有人 | `fund/p_fund2621` | `3333027e4e414021be1ad7dd945836c9` |
| `p_fund2622` | 基金投资前五名债券 | `fund/p_fund2622` | `e04fe124f05b4455984c8afeb86dbc40` |
| `p_fund2623` | 基金投资前十名股票 | `fund/p_fund2623` | `1ead7150ce584de1a8512887bd7ecf3e` |
| `p_fund2624` | 基金投资行业组合 | `fund/p_fund2624` | `b21818d113e1451aafaef3d61ab0e17f` |
| `p_fund2625` | 基金持仓股票明细 | `fund/p_fund2625` | `98ffaf26ee5348708617420d391a1ae2` |
| `p_fund2626` | 基金持有债券品种组合 | `fund/p_fund2626` | `614e7294e76f4ee6966435ac74e3e3dd` |
| `p_fund2627` | 期末基金资产组合情况2009版 | `fund/p_fund2627` | `90eb5d10ed0147358c18fda2a1094d90` |
| `p_fund2637` | 基金持有人结构与户数 | `fund/p_fund2637` | `904bc95cce0149d9863d878d1b1f0358` |

### 基础库-基金经营信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_fund2605` | ETF成份股信息 | `fund/p_fund2605` | `66e7eb7e0c344693a49953b0befee10d` |
| `p_fund2606` | ETF申购赎回信息 | `fund/p_fund2606` | `c074a1af43214899b96b20aed2dff4c8` |
| `p_fund2612` | 基金分红、分拆和合并方案 | `fund/p_fund2612` | `3645039d259244a7a76859477fc72f78` |
| `p_fund2613` | 基金持有人大会召开情况表 | `fund/p_fund2613` | `10fd829c35f84c0f9459347d600bb7c3` |

### 基础库-基金公告资讯

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3011` | 基金公告信息表 | `info/p_info3011` | `d37f45e94bfb4c318d7ec934f5910cb6` |
| `p_info3018` | 公告更新信息 | `info/p_info3018` | `c62c460ba90f4337a94d46f1e8bcfbd9` |

## 指数

### 指数-基础信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_index2903` | 国证指数基本信息 | `index/p_index2903` | `26afccd478734364ac28740cbb216c6b` |
| `p_index2904` | 国证指数行情表 | `index/p_index2904` | `50a6eb578a1344d09b1d55e800a2d105` |
| `p_index2905` | 交易所指数日行情 | `index/p_index2905` | `099b7af98af04ef9b37a118f82ce2356` |
| `p_index2911` | 交易所指数基本信息 | `index/p_index2911` | `78e68f259799412790353db0e2682898` |
| `p_swindex` | 申万指数行情 | `index/p_swindex` | `a52f67996d5d49708364b597245016a6` |

## ENGLISH APIS

### Stocks

#### Basic Information

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7001` | Basic Information | `en/p_ENS7001` | `6dc4880bb730457491786b2a59dd77a4` |
| `p_ENS7001o` | Basic Information | `en/p_ENS7001o` | `ce26cc7303914d64970b30221d2de14b` |
| `p_ENS7005` | Industry of Company | `en/p_ENS7005` | `4ace84b9bd684ee89a56c7ebf4c18b28` |
| `p_ENS7042` | Eligible Securities under Stock Connect | `en/p_ENS7042` | `a278ebccaf394a5aab7386a8c9a95ac0` |
| `p_ENS7045` | Registration-based IPO Listing Standards | `en/p_ENS7045` | `fbcf4fe8933d480eb83c776e171d1aa3` |

#### Corporate Action

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7002` | Company Name Change | `en/p_ENS7002` | `557f830be78c4fa1963e20afac86f274` |
| `p_ENS7003` | Stock Abbreviation Change | `en/p_ENS7003` | `c48e67f2189f4175a862e16ceebd7148` |
| `p_ENS7004` | Listing Status Change | `en/p_ENS7004` | `ab9faa875a2a4ad6b9ae6f42c8e6721c` |
| `p_ENS7009` | IPO | `en/p_ENS7009` | `a68a8b14c8f944b3a1ba63dfe2c27139` |
| `p_ENS7010` | Public Additional Offering | `en/p_ENS7010` | `e188013e6ed84b1793ca41c909162b0c` |
| `p_ENS7011` | Non-public Additional Offering | `en/p_ENS7011` | `b16346b037ab4973b8507dbcc932463e` |
| `p_ENS7012` | Rights Issue  | `en/p_ENS7012` | `0df2066623fb40a1af9e301b054af6c9` |
| `p_ENS7013` | Meeting Dates | `en/p_ENS7013` | `b72fc582a1d94719b7c6ef98454228a7` |
| `p_ENS7014` | Meeting Proposals | `en/p_ENS7014` | `92c994247a014eb885ce02eba1904359` |
| `p_ENS7017` | Cash Dividends and Bonus Shares | `en/p_ENS7017` | `0d5add5b8f0040bdb492ae1113a5b2c0` |
| `p_ENS7031` | Merger and Acquisition  | `en/p_ENS7031` | `884aa82dc865451091ceebf1edb350dc` |
| `p_ENS7032` | Tender Offer and Cash Option | `en/p_ENS7032` | `97d191cd5c234113baedfadb0be7a9d2` |
| `p_ENS7036` | Special Tips | `en/p_ENS7036` | `fd2a1aa55e6d4b39b6901ff1aaacb634` |
| `p_ENS7037` | Suspension or Resumption Tips | `en/p_ENS7037` | `ef05df4a1f824451ba1efc84d9c55438` |
| `p_ENS7046` | Meeting Change | `en/p_ENS7046` | `eeda64c5b69642b3afca270345e936ac` |
| `p_ENS7061` | Rights Issue Plan | `en/p_ENS7061` | `b7b478ac4db44410811635435e42b2d7` |

#### Ownership

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7006` | Equity Structure | `en/p_ENS7006` | `cdc28cf81b0f46f9925796bfd491012e` |
| `p_ENS7015` | Top 10 Shareholders | `en/p_ENS7015` | `e539edda6f294602b15e708f457b980b` |
| `p_ENS7034` | Restricted Share Listing | `en/p_ENS7034` | `256dd031993142d49e203dc0f80c45e5` |
| `p_ENS7043` | Top 10 Floating Shareholders | `en/p_ENS7043` | `dccd08a7dbc54b76b51cdabbd4ff6297` |
| `p_ENS7047` | Foreign Investors' Shareholding Exceeds 24 PCT of Share Capital | `en/p_ENS7047` | `db04cf9c628a42438180b297b10949e0` |
| `p_ENS7056` | Movements in Shareholding | `en/p_ENS7056` | `ac35d3644b904bd0bba46a3e07b21a7b` |

#### Corporate Finance

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7018` | Major Financial Indicators | `en/p_ENS7018` | `068ecdf2188242699f4c5fab60268579` |
| `p_ENS7019` | Income Statement for Non-financial-type Companies | `en/p_ENS7019` | `8cb586b601f34acf96b81ed55c315dc9` |
| `p_ENS7020` | Balance Sheet for Non-financial-type Companies | `en/p_ENS7020` | `9a0ee5caec2647adb6fb083c5d8d3aff` |
| `p_ENS7021` | Cash Flow Statement for Non-financial-type Companies | `en/p_ENS7021` | `09671286412a443aa5213c240c09fc27` |
| `p_ENS7022` | Income Statement for Banks | `en/p_ENS7022` | `184760204e574e2da57f1516df7c5181` |
| `p_ENS7023` | Balance Sheet for Banks | `en/p_ENS7023` | `08a726a81d2d411bb432ff4ced377096` |
| `p_ENS7024` | Cash Flow Statement for Banks | `en/p_ENS7024` | `acdbe715b361436fb63c4a169ded5faf` |
| `p_ENS7025` | Income Statement for Securities Companies | `en/p_ENS7025` | `9c9257e561dd49d6b9c8d2d9b9b3a44d` |
| `p_ENS7026` | Balance Sheet for Securities Companies | `en/p_ENS7026` | `f6bf8a5a735940f88f8cb8e907d7d717` |
| `p_ENS7027` | Cash Flow Statement for Securities Companies | `en/p_ENS7027` | `5ef37672eed94f4e82c263f724c55147` |
| `p_ENS7028` | Income Statement for Insurance Companies | `en/p_ENS7028` | `79116fdbe6a544c69cb429c92c21fc8f` |
| `p_ENS7029` | Balance Sheet for Insurance Companies | `en/p_ENS7029` | `d7ad8aca5f2048ec83926506b3c52c58` |
| `p_ENS7030` | Cash Flow Statement for Insurance Companies | `en/p_ENS7030` | `baf4a8e98758486abacf714feb232a58` |
| `p_ENS7033` | Periodic Report Disclosure Schedule | `en/p_ENS7033` | `8d10abbb2d1d494ea70566f8c1654f5e` |
| `p_ENS7035` | Performance Forecast | `en/p_ENS7035` | `4704e812396648559e59e2591fb04f38` |
| `p_ENS7048` | Audit Opinion on Annual Report | `en/p_ENS7048` | `0de82b1a1eae4b029b146b67ced49983` |
| `p_ENS7049` | Balance Sheet for Non-financial Co. (Point-in-Time) | `en/p_ENS7049` | `fdc4b9412ca64de8bf420073c9845a58` |
| `p_ENS7050` | Income Statement for Non-financial Co. (Point-in-Time) | `en/p_ENS7050` | `73814b82826d4ffb897c9215179d029d` |
| `p_ENS7051` | Cash Flow Statement for Non-financial Co. (Point-in-Time) | `en/p_ENS7051` | `8361345a503b46deb5619a03159f5874` |
| `p_ENS7052` | Balance Sheet for Financial Co. (Point-in-Time) | `en/p_ENS7052` | `954ad90b9a804b968782ddec27a9d651` |
| `p_ENS7053` | Income Statement for Financial Co. (Point-in-Time) | `en/p_ENS7053` | `9bf6aeb1198e4baf95e7f0f414b56750` |
| `p_ENS7054` | Cash Flow Statement for Financial Co. (Point-in-Time) | `en/p_ENS7054` | `7627b87ad13640f48a0aac8e3dfd0219` |
| `p_ENS7055` | Preliminary Earnings Estimate | `en/p_ENS7055` | `c81deec31ce44f21ac68a9a2084c166c` |
| `p_ENS7058` | Income Statement for Financial-type Companies | `en/p_ENS7058` | `4e27ebef4503483a9387c7b3b9ddba83` |
| `p_ENS7059` | Balance Sheet for Financial-type Companies | `en/p_ENS7059` | `a68973708604452aa1145fa7c8dd6845` |
| `p_ENS7060` | Cash Flow Statement for Financial-type Companies | `en/p_ENS7060` | `f1133e37a17e42be9ec6411ab5830d2d` |

#### Quotes

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7038` | Daily Quotes | `en/p_ENS7038` | `ee5e6ae8359b4e0bb4f51b10dac7791b` |
| `p_ENS7039` | Weekly Quotes | `en/p_ENS7039` | `b2369ad738d5437c9ab2f6263a389f46` |
| `p_ENS7040` | Monthly Quotes | `en/p_ENS7040` | `273190d66db240baa40efb2d58794cfb` |

### Bonds

#### Basic Information

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENB7101` | Basic Information | `en/p_ENB7101` | `c2e7556f01db4d49a1ca6ebb7f582531` |
| `p_ENB7102` | Bond Interest Rate | `en/p_ENB7102` | `b8e63a30476f44128d246ba437dd95a4` |
| `p_ENB7103` | Bond Principal Change | `en/p_ENB7103` | `88aec265f3d8474398b53b754658120d` |

#### Corporate Action

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENB7104` | T-bond Issue | `en/p_ENB7104` | `360a05d8024f4adbaae68bf989dc34d2` |
| `p_ENB7105` | Corporate Bond Issue | `en/p_ENB7105` | `96fef3a93cdc4d80864b04673b6d1ac6` |
| `p_ENB7106` | Convertible Bond Issue | `en/p_ENB7106` | `50a11fa94d6c431bb9966bc682562152` |
| `p_ENB7107` | Meeting Dates | `en/p_ENB7107` | `5d84d2d8ed34402e9839e532807d94ab` |
| `p_ENB7108` | Meeting Proposals | `en/p_ENB7108` | `b28bbb140d254131974d08a94122ab84` |
| `p_ENB7109` | Bond Interests | `en/p_ENB7109` | `02519d1f113942b382ae1fcf756c5645` |
| `p_ENB7110` | Bond Maturity | `en/p_ENB7110` | `b4e99ce30a6c4d719de4295414e3bda7` |
| `p_ENB7111` | Bond Redemption | `en/p_ENB7111` | `ff9dac12ca7b48b5a2a586383e20baca` |
| `p_ENB7112` | Bond Resale | `en/p_ENB7112` | `4b102fa5aed443b48b208bb236c7ac72` |
| `p_ENB7113` | Debt-to-equity Conversion | `en/p_ENB7113` | `fadcc256a2564c198f17cbe11267035d` |
| `p_ENB7114` | Debt-to-equity Price Change | `en/p_ENB7114` | `b9e0ed90408f45d4a1291139ecd93ebc` |
| `p_ENB7115` | Special Tips | `en/p_ENB7115` | `2beb747d3fa44d62a6d56562c621b7f8` |
| `p_ENB7116` | Suspension or Resumption Tips | `en/p_ENB7116` | `4ed5d4e5fe064787a982783c838d7aab` |

#### Quotes

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENB7117` | Daily Quotes | `en/p_ENB7117` | `01e45139c88c46dda719c461c700036e` |
| `p_ENB7118` | Weekly Quotes | `en/p_ENB7118` | `4d2584accf7940ac85348a0cb8bda467` |
| `p_ENB7119` | Monthly Quotes | `en/p_ENB7119` | `cfa755f7af694478839a95b5e1866b92` |

### Funds

#### Basic Information

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENF7201` | Basic Information | `en/p_ENF7201` | `40668a830448409ca031d9d2bfaa4e45` |
| `p_ENF7213` | Fund NAV | `en/p_ENF7213` | `5661e8096a7a4115877df5fa975e3d6e` |
| `p_ENF7214` | Daily Income for Monetary Fund | `en/p_ENF7214` | `8433d83375b74d029846c23a60cec333` |
| `p_ENF7215` | ETF Constituents | `en/p_ENF7215` | `69180b06c423452d89633894fe0fb3fc` |
| `p_ENF7218` | ETF Creation & Redemption | `en/p_ENF7218` | `ee5d055c85354e7ca585eb9e421242f3` |

#### Corporate Action

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENF7202` | Meeting Dates | `en/p_ENF7202` | `1d4f6b41f7d54588ba1c12170ff17d70` |
| `p_ENF7203` | Meeting Proposals | `en/p_ENF7203` | `eef9da13191445f3aa81609fb1cc6b71` |
| `p_ENF7204` | Fund Dividends | `en/p_ENF7204` | `3421cbff84704b0a80f0f26e4cf17dc7` |
| `p_ENF7205` | Fund Conversion | `en/p_ENF7205` | `65e2aa1a25b64d1195a81ec7a6e63af8` |
| `p_ENF7206` | Fund Split or Reverse Split | `en/p_ENF7206` | `baf0a1e000584f138295bf567607cfc4` |
| `p_ENF7207` | Open-ended Fund Unit Change | `en/p_ENF7207` | `2f09df752acc465ab2ad4eabbd0b16d5` |
| `p_ENF7208` | Special Tips | `en/p_ENF7208` | `cc325b652b83459fa1995ef179dfc802` |
| `p_ENF7209` | Suspension or Resumption Tips | `en/p_ENF7209` | `8da38fd3e3334e52bba2afcbbaddf41b` |

#### Quotes

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENF7210` | Daily Quotes | `en/p_ENF7210` | `9ffa6305ded644beb34417b9438bd848` |
| `p_ENF7211` | Weekly Quotes | `en/p_ENF7211` | `72f3a348ac0e4664adb454b177faa4df` |
| `p_ENF7212` | Monthly Quotes | `en/p_ENF7212` | `d07274df56c14322bb68e17d1bf7e24e` |

### Indices

#### Basic Information

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENI7301` | Basic Information | `en/p_ENI7301` | `e6f52e18ea6343a384de6754155a6f20` |

#### Quotes

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENI7302` | Daily Quotes | `en/p_ENI7302` | `ae468a9b2d4341d2b4fb82181e60edd2` |
| `p_ENI7303` | Weekly Quotes | `en/p_ENI7303` | `8f545af13543469d9f5a601b50067ad8` |
| `p_ENI7304` | Monthly Quotes | `en/p_ENI7304` | `e0bb9fd46d214307b0a3ff500af04835` |

### Hong Kong Stocks

#### Basic Information

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENHK7501` | Basic Information | `en/p_ENHK7501` | `8e175ea2d193497fa3cad17abcc6c66c` |

#### Corporate Action

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENHK7502` | Company Name Change | `en/p_ENHK7502` | `5dca6b008cce495fb552dfea5a1ec86a` |
| `p_ENHK7503` | Stock Abbreviation Change | `en/p_ENHK7503` | `40548d26eafe469eacdc7ab400d840f0` |
| `p_ENHK7504` | Merger and Acquisition | `en/p_ENHK7504` | `56c0b95448af4a31ae4588ae90887d39` |
| `p_ENHK7505` | Performance Forecast  | `en/p_ENHK7505` | `1f880dcc3a794db3836774d96f0f92f5` |

#### Company Financials

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENHK7506` | Major Financial Indicators for Non-financial-type Companies | `en/p_ENHK7506` | `64fedd40fd93451380d38752b224a0b6` |
| `p_ENHK7507` | Income Statement for Non-financial-type Companies | `en/p_ENHK7507` | `71fe62195c0845b385f2328e3a98d01c` |
| `p_ENHK7508` | Balance Sheet for Non-financial-type Companies | `en/p_ENHK7508` | `9bb87c211c33451c8b07c4c8d4a95136` |
| `p_ENHK7509` | Cash Flow Statement | `en/p_ENHK7509` | `b06c29b25e1c46ea8c2c32eee58564b6` |
| `p_ENHK7510` | Major Financial Indicators for Banks | `en/p_ENHK7510` | `1f0fc02a4ba944ae8a27a5bddd792e03` |
| `p_ENHK7511` | Balance Sheet for Banks | `en/p_ENHK7511` | `685020f9193a49ed9d04d624caf4862c` |
| `p_ENHK7512` | Income Statement for Banks | `en/p_ENHK7512` | `70a13525d80d4866bca1def7731bf0f1` |
| `p_ENHK7513` | Major Financial Indicators for Insurance Companies | `en/p_ENHK7513` | `d7156be1e9c045798ff4de3546e866fe` |
| `p_ENHK7514` | Balance Sheet for Insurance Companies | `en/p_ENHK7514` | `778df93d5ebc4a2297a4265a434a6425` |
| `p_ENHK7515` | Income Statement for Insurance Companies | `en/p_ENHK7515` | `eacef662fc53436e98473b7872545dd9` |

### CA Summaries

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENB7120` | CA Summary (Bonds) | `en/p_ENB7120` | `50e9ab6b1ed845c0bffa6bddda8db220` |
| `p_ENF7217` | CA Summary (Funds) | `en/p_ENF7217` | `510202dfb7ee420d948ab3d98dfda969` |
| `p_ENS7041` | CA Summary (Stocks) | `en/p_ENS7041` | `d379349cf6614642bad8dde09eae491b` |

### CA SWIFT Messages

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENB7121` | CA SWIFT Messages (Bonds) | `en/p_ENB7121` | `70b650a43a7744abb3af8b4ec45da60a` |
| `p_ENF7216` | CA SWIFT Messages (Funds) | `en/p_ENF7216` | `1582747372f743b38738e1999a4db069` |
| `p_ENS7044` | CA SWIFT Messages (Stocks) | `en/p_ENS7044` | `56cd0d68c1224bc5b1704afb265a1fd6` |

### China Corporate News

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_INFO3081` | China Corporate News | `en/p_INFO3081` | `7ee4934cebd345b194049bff170c7f0e` |
| `p_info3093` | China Market News | `info/p_info3093` | `afca0eb2f71c4a80bd102e183765e293` |

### Margin Trading

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_COLLATERAL_COEIFFICIENT` | List of Marginable Securities | `stock/p_COLLATERAL_COEIFFICIENT` | `2d4368b57a5146f8a8ba21e7dd941cdd` |
| `p_COLLATERAL_SEC_CHANGE` | Changes of Marginable Securities | `stock/p_COLLATERAL_SEC_CHANGE` | `556151f7ea4f423a985cb2ec8289111f` |
| `p_MARGIN_AGG_TRADEDATA` | Margin Trading Summary of Individual Stock | `stock/p_MARGIN_AGG_TRADEDATA` | `fb918b0ea49a4d8182061293c64603ec` |
| `p_MARGIN_DATADETAIL` | Margin Trading Breakdown of Individual Stock | `stock/p_MARGIN_DATADETAIL` | `ec340fc5ae7b4735ba6abed0b8bc8c43` |
| `p_MARGIN_FIAN_BAL_SEC_QTY_EX` | Trading Suspension of Eligible Securities for Margin Trading | `stock/p_MARGIN_FIAN_BAL_SEC_QTY_EX` | `1c57bed0ed334a8bb76f654191d282fd` |
| `p_MARGIN_SEC_CHANGE` | Changes of Eligible Securities for Margin Trading | `stock/p_MARGIN_SEC_CHANGE` | `fc06ee50aae3450a9db8375469193856` |
| `p_MARGIN_SEC_INFORMATION` | List of Eligible Securities for Margin Trading | `stock/p_MARGIN_SEC_INFORMATION` | `56b0931bf7e340e6ad95032f4e9e44bc` |
| `p_MARGIN_SEC_INFORMATION_INOUT` | Estimated List of Eligible Securities for Margin Trading | `en/p_MARGIN_SEC_INFORMATION_INOUT` | `3d5e4b583405477d9bcb0f0604319674` |
| `p_REFIANCING_MARGIN_TRANS` | Refinancing Trading Breakdown | `stock/p_REFIANCING_MARGIN_TRANS` | `fad55eae962f4a91a13f086924af70d5` |
| `p_REFIANCING_TRANS_AGG` | Refinancing Trading Summary | `stock/p_REFIANCING_TRANS_AGG` | `3419c68078d449aa86e531cc239127b7` |
| `p_securitycode` | Exchange-traded Securities Information | `stock/p_securitycode` | `28b5d71f1f49423c8f9c19e58f06e2aa` |

### Trade Info

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENT7401` | Margin Trading Breakdown | `en/p_ENT7401` | `3fdc2d648eb7428e80a4285913fe52ea` |
| `p_ENT7402` | Fund Discount Rate | `en/p_ENT7402` | `ac701c1694094569bd6dbc29b905da23` |
| `p_ENT7403` | Special Tips | `en/p_ENT7403` | `6587605deff140afa9d397871420b521` |
| `p_ENT7404` | Abnormal Stock Trading Fluctuations | `en/p_ENT7404` | `7c95d1bce85f4349b890e07076d44e5b` |
| `p_ENT7405` | Subscription List | `en/p_ENT7405` | `9e3749a165d24b558c145d5080ae22af` |
| `p_ENT7406` | Trading Calendar | `en/p_ENT7406` | `a99a8b31ce6d41809274fe7160522e1f` |
| `p_ENT7407` | Daily Reference | `en/p_ENT7407` | `af50fe4574eb455bbc7e607efed16d60` |

### Stock Connects Trading

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENNS7603` | Stock Connects Daily Market Statistics  | `en/p_ENNS7603` | `12117c6053654e5fa4d5973d492c8c9a` |
| `p_ENNS7604` | Stock Connects Daily Top 10 Most Actively Traded Securities | `en/p_ENNS7604` | `de35faebb34e49e993c0961d82a5f21f` |
| `p_ENNS7605` | Stock Connects Monthly Market Statistics | `en/p_ENNS7605` | `8c162c4b323043619626b20aba0e2ab4` |
| `p_ENNS7606` | Stock Connects Monthly Top 10 Most Actively Traded Securities | `en/p_ENNS7606` | `3fe7bccfb12f46aeb371fe0189a1210d` |
| `p_ENNS7607` | Northbound Trading Daily Short Selling Trading Statistics  | `en/p_ENNS7607` | `82f42505f3b8494aa52c2a2d65b17f18` |
| `p_ENNS7608` | Stock Connect Trading Shareholding Records | `en/p_ENNS7608` | `0f9e6042ceb246e38f8acc81d7b9b574` |
| `p_ENNS7611` | HKEX Daily Short Selling Turnover | `en/p_ENNS7611` | `c1422788b1c24cba8fbe693a05c19c91` |
| `p_ENNS7612` | Southbound Trading Daily Shareholding Movements | `en/p_ENNS7612` | `3086be0f271442bb86d9090c2ca2d67b` |
| `p_ENNS7613` | Southbound Trading Change in Market Value held by Industries | `en/p_ENNS7613` | `6c816d2100fe4cdd9f81ecd5c7e7b416` |
| `p_ENNS7614` | List of Eligible Securities of the Stock Connect | `en/p_ENNS7614` | `0f03cba782e8441c8315b7cd5f205c3b` |
| `p_ENNS7615` | Southbound Trading Settlement Exchange Rate | `en/p_ENNS7615` | `9128132ae59c45bea42d98a345693eaf` |
| `p_ENNS7616` | Southbound Trading Reference Exchange Rate | `en/p_ENNS7616` | `40c42a2fa5354ac6903e9cec08bc11d1` |
| `p_ENNS7620` | CCASS Shareholding of A Share | `en/p_ENNS7620` | `471517ec97fd4cc1b1d7b9892a19ebe2` |
| `p_ENNS7621` | CCASS Participants' Shareholding of A Share | `en/p_ENNS7621` | `a9caf12f32c8472fa7e69351d6fb4426` |
| `p_ENNS7623` | Change of List of Eligible Securities for Stock Connect | `en/p_ENNS7623` | `c2663765927b4685861c4a6e2cece8d8` |
| `p_ENNS7624` | Buy Suspended /Resumed Northbound Trading Securities  | `en/p_ENNS7624` | `10cd687969e6475b9539ee5919521247` |
| `p_ENS7047` | Foreign Investors' Shareholding Exceeds 24 PCT of Share Capital | `en/p_ENS7047` | `db04cf9c628a42438180b297b10949e0` |

### Stocks_BSE

#### Basic Information_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7001_BSE` | Basic Information | `en/p_ENS7001_BSE` | `feb95e483c1a44a586a8a2c8a1599911` |
| `p_ENS7005_BSE` | Industry of Company | `en/p_ENS7005_BSE` | `31c1bfe0f8fd44f48804817ae5f1e83f` |
| `p_ENS7045_BSE` | Registration-based IPO Listing Standards | `en/p_ENS7045_BSE` | `8a25d3b807124121b289f67d62f13937` |

#### Corporate Actions_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7002_BSE` | Company Name Change | `en/p_ENS7002_BSE` | `9d741600e95b4881a62279c5b7f399e4` |
| `p_ENS7003_BSE` | Stock Abbreviation Change | `en/p_ENS7003_BSE` | `608b874511584112b93bb40e24e2cf62` |
| `p_ENS7004_BSE` | Listing Status Change | `en/p_ENS7004_BSE` | `b8f04f57d57e47578617ee376b3bfd26` |
| `p_ENS7009_BSE` | IPO | `en/p_ENS7009_BSE` | `401473a884b94c50bd8d3f7614e5449b` |
| `p_ENS7010_BSE` | Public Additional Offering | `en/p_ENS7010_BSE` | `3530900046b640148788b3b297397e25` |
| `p_ENS7011_BSE` | Non-public Additional Offering | `en/p_ENS7011_BSE` | `c61dc0e900884bc593329f7b57bc215e` |
| `p_ENS7012_BSE` | Rights Issue  | `en/p_ENS7012_BSE` | `5dd2ae8122a14c0dac7aa028d205dab2` |
| `p_ENS7013_BSE` | Meeting Dates | `en/p_ENS7013_BSE` | `9bffa1cef9284d7b98fea324cb945a08` |
| `p_ENS7014_BSE` | Meeting Proposals | `en/p_ENS7014_BSE` | `de2e23eba11d4ffebd365a9be273002b` |
| `p_ENS7017_BSE` | Cash Dividends and Bonus Shares | `en/p_ENS7017_BSE` | `5173b07bde1e46fc8874bd428990ccb6` |
| `p_ENS7031_BSE` | Merger and Acquisition  | `en/p_ENS7031_BSE` | `524416add7304cbcba64f72968878c8b` |
| `p_ENS7032_BSE` | Tender Offer and Cash Option | `en/p_ENS7032_BSE` | `e710d4e14f994cb18a7d159a70f05b8e` |
| `p_ENS7034_BSE` | Restricted Share Listing | `en/p_ENS7034_BSE` | `bff19ad6668e4183badc5e863555dcdf` |
| `p_ENS7036_BSE` | Special Tips | `en/p_ENS7036_BSE` | `c3d04f320e21432082bfe891109dab16` |
| `p_ENS7046_BSE` | Meeting Change | `en/p_ENS7046_BSE` | `4241d98243c54070a898e83cc9db2136` |

#### Ownership_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7006_BSE` | Equity Structure | `en/p_ENS7006_BSE` | `60e57cddb0d54498af60f62d73e7c908` |
| `p_ENS7015_BSE` | Top 10 Shareholders | `en/p_ENS7015_BSE` | `1377c2b792eb40559bf70edb6c682d74` |
| `p_ENS7034_BSE` | Restricted Share Listing | `en/p_ENS7034_BSE` | `bff19ad6668e4183badc5e863555dcdf` |
| `p_ENS7043_BSE` | Top 10 Floating Shareholders | `en/p_ENS7043_BSE` | `a617e21d9a504479a7e9ccc7e5e3526b` |
| `p_ENS7056_BSE` | Movements in Shareholding | `en/p_ENS7056_BSE` | `244c3065b3114b828391fc9267879914` |

#### Corporate Finance (Point-in-Time)_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7018_BSE` | Major Financial Indicators | `en/p_ENS7018_BSE` | `77faf277810742ef93cc05da3f66fbde` |
| `p_ENS7033_BSE` | Periodic Report Disclosure Schedule | `en/p_ENS7033_BSE` | `c79d121bada74564996ac8b0c9810b85` |
| `p_ENS7035_BSE` | Performance Forecast | `en/p_ENS7035_BSE` | `7f8ac731a08a4d20ad087e2edcd9b951` |
| `p_ENS7048_BSE` | Audit Opinion on Annual Report | `en/p_ENS7048_BSE` | `bedaac88fa574dbd8d3fdfbc144c6c82` |
| `p_ENS7049_BSE` | Balance Sheet for Non-financial Co. (Point-in-Time) | `en/p_ENS7049_BSE` | `2d6bba0faec040f0b847f54f7a22196b` |
| `p_ENS7050_BSE` | Income Statement for Non-financial Co. (Point-in-Time) | `en/p_ENS7050_BSE` | `43e4c3596d4f4654ac875404cff7c0e2` |
| `p_ENS7051_BSE` | Cash Flow Statement for Non-financial Co. (Point-in-Time) | `en/p_ENS7051_BSE` | `b0b64a139fba4e2d8f1d5d28c6ffd1b3` |
| `p_ENS7052_BSE` | Balance Sheet for Financial Co. (Point-in-Time) | `en/p_ENS7052_BSE` | `a693f0fd95fb4e08a0526cf3801e721d` |
| `p_ENS7053_BSE` | Income Statement for Financial Co. (Point-in-Time) | `en/p_ENS7053_BSE` | `2f8cfda17f24442882518640ef8060f3` |
| `p_ENS7054_BSE` | Cash Flow Statement for Financial Co. (Point-in-Time) | `en/p_ENS7054_BSE` | `54beb6d83ad643ae9318639fe71c9999` |
| `p_ENS7055_BSE` | Preliminary Earnings Estimate | `en/p_ENS7055_BSE` | `3b9e132b3d2746e8afbc8a5f4a46201a` |

#### Quotes_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7038_BSE` | Daily Quotes | `en/p_ENS7038_BSE` | `eb4fe7ae2d1c4b92ad21c8f8cac005cb` |
| `p_ENS7039_BSE` | Weekly Quotes | `en/p_ENS7039_BSE` | `73d1613b2c69428e84ccb05c20de41dc` |
| `p_ENS7040_BSE` | Monthly Quotes | `en/p_ENS7040_BSE` | `009fe871216f4a27b0faf26747898e91` |

#### Corporate Finance_BSE

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENS7018_BSE` | Major Financial Indicators | `en/p_ENS7018_BSE` | `77faf277810742ef93cc05da3f66fbde` |
| `p_ENS7019_BSE` | Income Statement for Non-financial-type Companies | `en/p_ENS7019_BSE` | `9f0c2795d76c4eb298ec6b0181910664` |
| `p_ENS7020_BSE` | Balance Sheet for Non-financial-type Companies | `en/p_ENS7020_BSE` | `1e515119fb954077aee1678bc83facd6` |
| `p_ENS7021_BSE` | Cash Flow Statement for Non-financial-type Companies | `en/p_ENS7021_BSE` | `aac0a3c87e5d4da783dcf07b4801c2bf` |
| `p_ENS7022_BSE` | Income Statement for Banks | `en/p_ENS7022_BSE` | `6f295bfc8f7c417dbe45217577b83b51` |
| `p_ENS7023_BSE` | Balance Sheet for Banks | `en/p_ENS7023_BSE` | `3ad701903a01468395d1fe590e476b9d` |
| `p_ENS7024_BSE` | Cash Flow Statement for Banks | `en/p_ENS7024_BSE` | `e621e1c5a07445e2bd528e73b2df4339` |
| `p_ENS7025_BSE` | Income Statement for Securities Companies | `en/p_ENS7025_BSE` | `3cb324b9b3734661ad6e521902af1aad` |
| `p_ENS7026_BSE` | Balance Sheet for Securities Companies | `en/p_ENS7026_BSE` | `b733249f01fa40668eea523e41a97949` |
| `p_ENS7027_BSE` | Cash Flow Statement for Securities Companies | `en/p_ENS7027_BSE` | `ea11b56e77e647a599ee6bf4bc93f4b3` |
| `p_ENS7028_BSE` | Income Statement for Insurance Companies | `en/p_ENS7028_BSE` | `142141174e8b4a52b4c9ffe684f41f59` |
| `p_ENS7029_BSE` | Balance Sheet for Insurance Companies | `en/p_ENS7029_BSE` | `81f7c6b4768a46b68620593d6c636b01` |
| `p_ENS7030_BSE` | Cash Flow Statement for Insurance Companies | `en/p_ENS7030_BSE` | `663f413e4df04fb9875af86cb9b27483` |
| `p_ENS7033_BSE` | Periodic Report Disclosure Schedule | `en/p_ENS7033_BSE` | `c79d121bada74564996ac8b0c9810b85` |
| `p_ENS7035_BSE` | Performance Forecast | `en/p_ENS7035_BSE` | `7f8ac731a08a4d20ad087e2edcd9b951` |
| `p_ENS7048_BSE` | Audit Opinion on Annual Report | `en/p_ENS7048_BSE` | `bedaac88fa574dbd8d3fdfbc144c6c82` |
| `p_ENS7055_BSE` | Preliminary Earnings Estimate | `en/p_ENS7055_BSE` | `3b9e132b3d2746e8afbc8a5f4a46201a` |

### Ownership Structure Analysis

#### Ownership Structure

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENSH7708_1` | Ownership Structure Overview | `fund/p_ENSH7708_1` | `2a53974a127d4096a2dcfce5680e4b98` |
| `p_ENSH7708_2` | Ownership Structure Breakdown | `fund/p_ENSH7708_2` | `cbbb09e10b0f4bbcb034d0f3bad14628` |
| `p_ENSH7708_breakdown` | Ownership Structure Breakdown | `load/p_ENSH7708_breakdown` | `4a7ec6833cec4959976679ff1acc0966` |
| `p_ENSH7708_breakdown_c` | Ownership Structure Breakdown | `load/p_ENSH7708_breakdown_c` | `b5614a88961540e58d8242147234fb15` |
| `p_ENSH7708_overview` | Ownership Structure Overview | `load/p_ENSH7708_overview` | `d230ddf1833d4c9f89b091b829aaab7d` |
| `p_ENSH7708_overview_c` | Ownership Structure Overview | `load/p_ENSH7708_overview_c` | `94452391d0c84791b07fc00fcf84c0f2` |
| `p_ENSH7715` | Foreign Investors Shareholding | `en/p_ENSH7715` | `47b86219766749edb9f4d20d281c4d90` |

#### Fund Position

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ENSH7709` | Mutual Funds Position Details | `en/p_ENSH7709` | `c0faae1149d94fad82e5d5282bf43a7d` |
| `p_ENSH7710` | Aggregate Fund Position of Individual Stock | `en/p_ENSH7710` | `64bb99a8bfff4833b82237c55d7007f9` |
| `p_ENSH7711` | Aggregate Position of Individual Stocks by Fund Companies | `en/p_ENSH7711` | `e99975348f2b4e53b218fdc201ff8ba8` |
| `p_ENSH7712` | Ranking of Stocks by Aggregate Market Capitalization | `en/p_ENSH7712` | `813154d8fd1b426ba67115ca3e0774bf` |
| `p_ENSH7741` | The No. of Funds Holding Individual Stocks as Top 10 Stock Picks | `en/p_ENSH7741` | `ee791adc54ca47a09624de23ed3f7ab7` |
| `p_ENSH7742` | Proportion of Fund Top 10 Stock Picks to Fund Net Value | `en/p_ENSH7742` | `41f5dc5988c94fdab5a1ff76f8bcb2d8` |

## 深证信量化数据服务

### 全局性量化分析数据

#### 公共信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_public0001` | 交易日历数据 | `stock/p_public0001` | `0bf76273eb724e38bf32c30cfac5ddda` |
| `p_stock2428` | 量化分析证券信息表接口 | `info/p_stock2428` | `54647464b02347889aff3f1cd7d3db1d` |

### 股票类量化分析数据

#### 股票行情量化数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_public0004` | 板块成份股数据 | `stock/p_public0004` | `9ab168b31df84d8e98076bef67073537` |
| `p_stock2401` | 股票最新日行情 | `stock/p_stock2401` | `f16b697db4724bc69f972fa291d03d12` |
| `p_stock2402` | 股票历史日行情 | `stock/p_stock2402` | `c3c41c16bf0f420e863fdad34b0d6648` |
| `p_stock2427` | AB股证券状态表接口 | `info/p_stock2427` | `40b567dfc7894fc29c749c36c3a42ddc` |
| `p_stock2429` | AB股除复权因子表接口 | `info/p_stock2429` | `fddfdac69d694248ac4e91704c0cbf1f` |
| `p_stock2430` | 除权参考价 | `stock/p_stock2430` | `a3289a806c1745babf3ddc43cf9150db` |

#### 股票交易量化数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_rzrq3104` |  融资融券明细数据 | `stock/p_rzrq3104` | `6e9e5d07f7dc42e1a69dae2ce82da33f` |
| `p_rzrq3106` | 单一股票质押比例 | `stock/p_rzrq3106` | `fe029a72e7fc4b5da736a62e8b7de0ec` |
| `p_stock2202` | 证券交易特别提示 | `stock/p_stock2202` | `f968156887bd46319d98a31b93c25d4a` |
| `p_stock2203` | 证券交易停复牌信息 | `stock/p_stock2203` | `21a87d1689714dc380eb4df951ae7424` |
| `p_stock2204` | 沪深异动证券公开信息 | `stock/p_stock2204` | `7958c463073c4f8da684e43b8d1bc60c` |
| `p_stock2226` | 股东增（减）持情况 | `stock/p_stock2226` | `9000cd76f0d640b9ba8cb79eb90748a0` |
| `p_stock2416` | 大宗交易数据 | `stock/p_stock2416` | `4cb90e94909f489592f4ab9e201bac62` |
| `p_stock2426` | 多市场交易日报 | `stock/p_stock2426` | `b51f2add2fc140158d820a36c8ddabd6` |

#### 股票财务量化数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2373` | 通用资产负债表2022版表 | `stock/p_stock2373` | `a38e1fc2b18347a499376401addd2f36` |
| `p_stock2374` | 通用利润表2022版表 | `stock/p_stock2374` | `07919cd4ddee4d908c27bd26d1566f6e` |
| `p_stock2375` | 通用现金流量表及补充资料2022版表 | `stock/p_stock2375` | `1da81595f6e14e6cb9a5500cba47e94d` |
| `p_stock2376` | 金融资产负债表2022版表 | `stock/p_stock2376` | `b473a666acf5475f81a46bfcb60f010c` |
| `p_stock2377` | 金融类利润表2022版表 | `stock/p_stock2377` | `6a155ba51d3e47f2ab88329ff3344474` |
| `p_stock2378` | 金融现金流量表2022版表 | `stock/p_stock2378` | `ecc2ead06c2243bfb6df4a5aa0468fe5` |

### 指数类量化分析数据

#### 指数概况数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_index2903` | 国证指数基本信息 | `index/p_index2903` | `26afccd478734364ac28740cbb216c6b` |
| `p_index2911` | 交易所指数基本信息 | `index/p_index2911` | `78e68f259799412790353db0e2682898` |

#### 指数行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_index2904` | 国证指数行情表 | `index/p_index2904` | `50a6eb578a1344d09b1d55e800a2d105` |
| `p_index2905` | 交易所指数日行情 | `index/p_index2905` | `099b7af98af04ef9b37a118f82ce2356` |

## 新闻研报

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3097_inc` | 个股研报摘要 | `load/p_info3097_inc` | `63bd34c18e214772832425065a5ef13f` |
| `p_stock2205` | 投资评级 | `sysapi/p_stock2205` | `d7afdca660264fc28253479e627935b7` |

### 研报数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3029` | 研报摘要 | `info/p_info3029` | `be3f791d452048048061529b6a2ef77b` |
| `p_info3032` | 公司研报数据 | `info/p_info3032` | `dd45c07bdf2b46ddacfc4492744b1627` |
| `p_info3033` | 行业研报数据 | `info/p_info3033` | `c05ade3a35634513b688d22847973d9b` |
| `p_info3034` | 宏观研报数据 | `info/p_info3034` | `3c25a8126178463dab243ecc808e3675` |
| `p_info3097` | 个股研报摘要 | `info/p_info3097` | `c7095df0abc14cb7aa1c8c0732c3b1e5` |
| `p_stock2205` | 投资评级 | `sysapi/p_stock2205` | `d7afdca660264fc28253479e627935b7` |

### 新闻数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3030` | 新闻数据查询 | `info/p_info3030` | `7aba8a88d224499886309ab515d3fd0b` |

## 工商大数据

### 沪深北AB股工商大数据

#### 沪深北AB股工商信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_com_branch` | 沪深AB股分支机构 | `bigdata/p_com_branch` | `9f79cab4c55746c480a6132e2c32b788` |
| `p_com_info` | 沪深AB股公司详情 | `bigdata/p_com_info` | `60de4045a73349d2a4945de4eb17c7aa` |
| `p_com_invest` | 沪深AB股对外投资 | `bigdata/p_com_invest` | `91c1bcf4607c49b9b63b6108b96ab8dc` |
| `p_com_regchange` | 沪深AB股工商变更 | `bigdata/p_com_regchange` | `8b3ff79f6e744026b2f370bfbf317319` |
| `p_com_socialsecurity` | 沪深AB股工商社保 | `bigdata/p_com_socialsecurity` | `de81c793b2504edaa1b048607e5d90ac` |

#### 沪深北AB股法律诉讼

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_com_courtannc` | 沪深AB股法院公告列表 | `bigdata/p_com_courtannc` | `44fc73a5ac924668934043b0f963a3ff` |
| `p_com_courtanncinfo` | 沪深AB股法院公告详情 | `bigdata/p_com_courtanncinfo` | `f996bf4257dc49cea8b89d21c55abf77` |
| `p_com_courtruling` | 沪深AB股法律文书列表 | `bigdata/p_com_courtruling` | `8e6b02b4b32f49e3bdb397c887ca1b3d` |
| `p_com_hearinginfo` | 沪深AB股开庭公告详情 | `bigdata/p_com_hearinginfo` | `e768f350062c4079ac8d4eb379c959fd` |
| `p_com_hearingsch` | 沪深AB股开庭公告列表 | `bigdata/p_com_hearingsch` | `5305d83ac4eb4026adcfe1c163cf5b30` |
| `p_com_rulinginfo` | 沪深AB股法律文书详情 | `bigdata/p_com_rulinginfo` | `1c9b4e27774f4cd8a0dea26cca9ccfbf` |

#### 沪深北AB股知识产权

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_com_copyright` | 沪深AB股作品著作权 | `bigdata/p_com_copyright` | `ddbb3bdaaf1c40ce8d0589ce18d65bde` |
| `p_com_icprecord` | 沪深AB股网站备案 | `bigdata/p_com_icprecord` | `9bd324ddfd6c416786ccf294ef0ad0b0` |
| `p_com_patent` | 沪深AB股专利列表 | `bigdata/p_com_patent` | `5b4fef9900e340b0988fb3553a0096c0` |
| `p_com_patentinfo` | 沪深AB股专利详情 | `bigdata/p_com_patentinfo` | `c07972e1c6274e97af251113c0ecf697` |
| `p_com_swcopr` | 沪深AB股软件著作权 | `bigdata/p_com_swcopr` | `8180a3f94bed4568ad73c99e1adcac26` |
| `p_com_tendering` | 沪深AB股招投标 | `bigdata/p_com_tendering` | `cd33afa93e3945d6aed6717b4757b6a9` |
| `p_com_trademark` | 沪深AB股商标 | `bigdata/p_com_trademark` | `4564423bb8bc41c98c13005b433bcbfe` |

#### 沪深北AB股处罚与监管

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_com_adminlicense` | 沪深AB股行政许可 | `bigdata/p_com_adminlicense` | `883c4964827c4713bf28d97f7bfe0736` |
| `p_com_adminpenalty` | 沪深AB股行政处罚 | `bigdata/p_com_adminpenalty` | `49a69ebbb6bb4e9aad4da372c61e3d96` |
| `p_com_check` | 沪深AB股抽查检查 | `bigdata/p_com_check` | `76408000e80e4e1fbe6b36bcb126f34e` |
| `p_com_defaultinfo` | 沪深AB股失信信息 | `bigdata/p_com_defaultinfo` | `f67acbdf315c4b78a2def30d7e546ce0` |

#### 沪深北AB股舆情

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_com_news` | AB股舆情 | `bigdata/p_com_news` | `444dd9bda22844a380fd4a5e2801cfdd` |

### 新三板工商大数据

#### 新三板工商信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ntb_branch` | 新三板分支机构 | `bigdata/p_ntb_branch` | `dd274fdbdfb34d9fa4b6efd1db0eaf40` |
| `p_ntb_info` | 新三板公司信息 | `bigdata/p_ntb_info` | `d4be6a16c86b4bec9de3bd34871f6043` |
| `p_ntb_invest` | 新三板对外投资 | `bigdata/p_ntb_invest` | `0b9714e77381412bba4559831633a4a5` |
| `p_ntb_regchange` | 新三板工商变更 | `bigdata/p_ntb_regchange` | `946456c339a2460f99897bc6583f1e1e` |
| `p_ntb_socialsecurity` | 新三板工商社保 | `bigdata/p_ntb_socialsecurity` | `bcd1956bb7c646a286b79712c4a9ac4d` |

#### 新三板法律与诉讼

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ntb_courtannc` | 新三板法院公告列表 | `bigdata/p_ntb_courtannc` | `7ad713f971164521a790ed2fdd3935f1` |
| `p_ntb_courtanncinfo` | 新三板法院公告详情 | `bigdata/p_ntb_courtanncinfo` | `5d7fab592ed945a59d405628aaa0a984` |
| `p_ntb_courtruling` | 新三板法律文书列表 | `bigdata/p_ntb_courtruling` | `256aaba2dc0c4d0abb775687096cf6e6` |
| `p_ntb_hearinginfo` | 新三板开庭公告详情 | `bigdata/p_ntb_hearinginfo` | `9d639fbd8d2b4c5fa7c2565fe5c7878e` |
| `p_ntb_hearingsch` | 新三板开庭公告列表 | `bigdata/p_ntb_hearingsch` | `7c9ccbf3cb4e491f92bbb3c0ef085efd` |
| `p_ntb_rulinginfo` | 新三板法律文书详情 | `bigdata/p_ntb_rulinginfo` | `408f4de46bae47f5bfa0b427cebb3dde` |

#### 新三板知识产权

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ntb_copyright` | 新三板作品著作权 | `bigdata/p_ntb_copyright` | `af0414d2194e48aa90c7fe0c7ab11b20` |
| `p_ntb_icprecord` | 新三板网站备案 | `bigdata/p_ntb_icprecord` | `7a191a9f24a249e793922ea7ef387e69` |
| `p_ntb_patent` | 新三板专利列表 | `bigdata/p_ntb_patent` | `fcb4b48ca5fe4751838a982640446813` |
| `p_ntb_patentinfo` | 新三板专利详情 | `bigdata/p_ntb_patentinfo` | `1a74a00e433845bd97eb90fcd8474550` |
| `p_ntb_swcopr` | 新三板软件著作权 | `bigdata/p_ntb_swcopr` | `e9169e3c5272494cbf3c86f6d00d0a62` |
| `p_ntb_tendering` | 新三板招投标 | `bigdata/p_ntb_tendering` | `80c3758658764ffcaee323406732298b` |
| `p_ntb_trademark` | 新三板商标 | `bigdata/p_ntb_trademark` | `0425b064bc6649b9a6b89fe9672d0ac2` |

#### 新三板处罚与监管

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ntb_adminlicense` | 新三板行政许可 | `bigdata/p_ntb_adminlicense` | `cbf0fdb7e24341b0b5d6f15ca48f26bb` |
| `p_ntb_adminpenalty` | 新三板行政处罚 | `bigdata/p_ntb_adminpenalty` | `6af94f78a676409db786e5c16ea52e09` |
| `p_ntb_check` | 新三板抽查检查 | `bigdata/p_ntb_check` | `420b04d18d7b4c318d9600ad19b71d5f` |
| `p_ntb_defaultinfo` | 新三板失信信息 | `bigdata/p_ntb_defaultinfo` | `adef97cf1b98450cbcad64f239faf048` |

### 其他工商信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_gsinfo_batch` | p_gsinfo_batch | `bigdata/p_gsinfo_batch` | `af5bce024a0b42a9b234baeb4e1a4ba5` |

## 拟上市公司数据

### 首发或注册制申报企业

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ipocodelist` | 首发申报企业编码表 | `stock/p_ipocodelist` | `38aa898b9ebb422bbff1667d9f99cd59` |
| `p_ipoinfo` | 首发申报企业基本情况 | `stock/p_ipoinfo` | `4728a94e0fb24b35a43990a9e19c75fa` |
| `p_ipostateupdate` | 首发申报企业状态更新 | `stock/p_ipostateupdate` | `d9201acaadcf4a818fedb4809edc8d6f` |
| `p_regbalancesheet` | 注册制发行申报企业通用资产负债表 | `stock/p_regbalancesheet` | `8412dd46d5674c6a891293fb7ece6886` |
| `p_regcashflowstatement` | 注册制发行申报企业通用现金流量表 | `stock/p_regcashflowstatement` | `f8622d1a7d274f90b350182e1ad7eb59` |
| `p_regfinanciallndicators` | 注册制发行申报企业通用主要财务指标 | `stock/p_regfinanciallndicators` | `6caeccbb9f484341930182b0d80d9d6e` |
| `p_regincomestatement` | 注册制发行申报企业通用利润表 | `stock/p_regincomestatement` | `c5da8801d5194af9ba776a4fc33b3df1` |

### 证监会辅导企业

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_csrcguidancestateupdate` | 各地证监局辅导企业状态更新 | `stock/p_csrcguidancestateupdate` | `1c6c2214fcf8471997f2130acbafbf5f` |
| `p_info3076` | 辅导企业公告 | `info/p_info3076` | `f0f91648b59f4a2cb8db2ece57daa889` |
| `p_stock2271` | 新拟上市辅导企业信息表 | `stock/p_stock2271` | `9c662fa0568a49b19a891e78e6f504b2` |

### 新三板精选层企业

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_neeq6017` | 新三板公司通用主要财务指标 | `neeq/p_neeq6017` | `4042fe32eeff49d2a011eea7351f711e` |
| `p_neeq6018` | 新三板公司通用资产负债表 | `neeq/p_neeq6018` | `aea1337f05bd446e84af166a2197188d` |
| `p_neeq6019` | 新三板公司通用利润表 | `neeq/p_neeq6019` | `453eed44893c4ed7a94426f93b8cba88` |
| `p_neeq6020` | 新三板公司通用现金流量表及补充资料表 | `neeq/p_neeq6020` | `6f6ecbf51c2447e5b8b94c74d5b0f640` |
| `p_neeq6028` | 新三板股份报价日行情信息 | `neeq/p_neeq6028` | `98c49db2f12447dd99615883b562a2de` |
| `p_neeqannouncement` | 新三板创新层公司相关公告 | `neeq/p_neeqannouncement` | `e931d936420644ff984fcf9f16940c08` |
| `p_neeqselectsires` | 新三板创新层公司基本情况 | `neeq/p_neeqselectsires` | `b58ff3d724444860987f306f7644006f` |

## 深证信专题数据服务

### 资金流向

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_capitalflowsnapshot` | 最新资金流向实时快照数据 | `stock/p_capitalflowsnapshot` | `3ef3e07ac5c84c0a99aad8cec6860b64` |
| `p_cninfo5044` | 深沪股通资金流向 | `cninfo/p_cninfo5044` | `d9c1145692af435684fdc3ae25a4b7be` |
| `p_stock2529` | 最新资金流向分时数据 | `stock/p_stock2529` | `388d07c831da4799b29334f3bd7607b6` |

### 陆港通数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_MHKCONN4523` | 陆港通标的券变动 | `stock/p_MHKCONN4523` | `1540a4e1750f416fb1c8c74d1b8e3d82` |
| `p_MHKCONN4524` | 陆港通标的券暂停买入 | `stock/p_MHKCONN4524` | `01a710958dc443dda7e7e68db933fd5a` |
| `p_mhkconn0002` | 申万行业代码查询-陆股通专用 | `stock/p_mhkconn0002` | `aad9a0e0d51d45caa8008a8dcac401b8` |
| `p_mhkconn4500` | 陆港通证券标的证券表 | `stock/p_mhkconn4500` | `34e3e2f28c1040a7968cd7b2bc931170` |
| `p_mhkconn4501` | 陆股通实时卖空数据-按日期查询 | `stock/p_mhkconn4501` | `99a63ac1e2a64cec9838ba9d3a4d94b5` |
| `p_mhkconn4501_code` | 陆股通实时卖空数据-代码维度查询 | `stock/p_mhkconn4501_code` | `b20d5966a914438da41459efa7076cc7` |
| `p_mhkconn4502` | 陆港通每日市场统计数据 | `stock/p_mhkconn4502` | `3af9df1a16a6408190e352f90d5545ed` |
| `p_mhkconn4503` | 陆港通每日持股记录数据-按日期查询 | `stock/p_mhkconn4503` | `e458812717aa4fbdb9405e00016e0bf7` |
| `p_mhkconn4503_code` | 陆港通每日持股记录数据-代码维度查询 | `stock/p_mhkconn4503_code` | `ce23da0c0ef343deb409cace62d3cd26` |
| `p_mhkconn4504` | 陆港通每日市场十大成交-按日期查询 | `stock/p_mhkconn4504` | `08d4bfbe6ac4476e86912f9cac698c69` |
| `p_mhkconn4504_code` | 陆港通每日市场十大成交-代码维度查询 | `stock/p_mhkconn4504_code` | `8088c1a6702f4c939c54d35e206a1ace` |
| `p_mhkconn4505` | 陆港通每月市场数据统计 | `stock/p_mhkconn4505` | `becc3c3f2a1546c694fe5ac8491bd538` |
| `p_mhkconn4506` | 陆港通每月十大成交活跃股-按日期查询 | `stock/p_mhkconn4506` | `5cbc7d746e3d413db1308fa1b1dff11b` |
| `p_mhkconn4506_code` | 陆港通每月十大成交活跃股-代码维度查询 | `stock/p_mhkconn4506_code` | `bb640244cd834821becbcc29f6a12ce1` |
| `p_mhkconn4507` | 港股每日卖空成交统计-按日期查询 | `stock/p_mhkconn4507` | `02fd1dcdc94f43ba8a5f88b4649f097f` |
| `p_mhkconn4507_code` | 港股每日卖空成交统计-按代码查询 | `stock/p_mhkconn4507_code` | `c74781a47f0348f689db5e4b09f08658` |
| `p_mhkconn4508` | 陆港通结算汇兑比率 | `stock/p_mhkconn4508` | `ec4a5599f3e84ec18c435d33e5a2c674` |
| `p_mhkconn4509` | 央行汇率参考表 | `stock/p_mhkconn4509` | `f0ef6d80a78d4485b0b6b5688617ec28` |
| `p_mhkconn4511` | 陆股通每日持股变化统计-按日期查询 | `stock/p_mhkconn4511` | `824418d567344463971ace431c059f5c` |
| `p_mhkconn4511_code` | 陆股通每日持股变化统计-代码维度查询 | `stock/p_mhkconn4511_code` | `2acaa9882fb7479596901804124e64f5` |
| `p_mhkconn4512` | 港股通每日持股变化统计-按日期查询 | `stock/p_mhkconn4512` | `475284e0f16f426ca5062a253436b38a` |
| `p_mhkconn4512_code` | 港股通每日持股变化统计-代码维度查询 | `stock/p_mhkconn4512_code` | `8bf83ae6c67045b9a287d86d1b44d5f9` |
| `p_mhkconn4513` | 陆股通行业持股市值变化 | `stock/p_mhkconn4513` | `da2c3bc35f554452a7e2bd40f65481ab` |
| `p_mhkconn4514` | 港股通行业持股市值变化 | `stock/p_mhkconn4514` | `65d4caf79ad54047ab94f508d10edbe4` |
| `p_mhkconn4515` | 北向互联互通ETF份额及净资产规模变动情况  | `stock/p_mhkconn4515` | `0c88817809cf4580bd296b74917f4559` |
| `p_mhkconn4516` | 北向互联互通ETF融资融券明细表 | `en/p_mhkconn4516` | `f190e7cac72b4660be8dca4dffcebd47` |
| `p_mhkconn4525` | 陆港通参考及结算汇率 | `stock/p_mhkconn4525` | `cf5d1224a7a94e59bd86ebc502eb0f87` |
| `p_public0001` | 交易日历数据 | `stock/p_public0001` | `0bf76273eb724e38bf32c30cfac5ddda` |

### 绿债数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2804` | 债券行情 | `bond/p_bond2804` | `92fb2958fbda498c84d600c01b38e93d` |
| `p_greenbondbaseinfo` | 绿债基本信息表 | `bond/p_greenbondbaseinfo` | `6e4de4fe698e4a4b8f16ac257fddc462` |

### 并购重组专题

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2241` | 公司资产重组概况 | `stock/p_stock2241` | `d89f3205a5ae43d0a6336bb78f8f166c` |
| `p_stock2242` | 公司债务重组 | `stock/p_stock2242` | `ccd2390dce874d1caee6a9d4b988a4ce` |
| `p_stock2243` | 公司吸收合并 | `stock/p_stock2243` | `cb4204ed2f23492ca78b127a268037c7` |
| `p_stock2244` | 公司股权变更 | `stock/p_stock2244` | `28f583afd51d4bffa33213b58f8e0e3c` |
| `p_stock2251` | 公司产品出让表 | `stock/p_stock2251` | `833bbf6c41174b56992699faa364a482` |
| `p_stock2252` | 公司资产收购表 | `stock/p_stock2252` | `34fabf4df6a34e8aa84c6e9017c5bdc4` |
| `p_stock2253` | 公司资产置换表 | `stock/p_stock2253` | `7b55c33669e64592877c24e26eef506d` |
| `p_stock2254` | 并购重组基本信息表 | `stock/p_stock2254` | `44ba69c56a7d45398298f0640d728f8d` |
| `p_stock2255` | 并购重组标的表 | `stock/p_stock2255` | `4054e34f719343df8d5869db79c5b555` |
| `p_stock2256` | 并购重组标的公司财务指标表 | `stock/p_stock2256` | `ce7200a7f1134a85b8fe7f15c23b0a7d` |
| `p_stock2257` | 并购重组交易对手情况表 | `stock/p_stock2257` | `01b1aff7d87c404a8ec971fa33e0168e` |
| `p_stock2258` | 并购重组客户供应商情况表 | `stock/p_stock2258` | `04e947b9bf75480d81b32468b9d0a198` |

### 财务统计专题

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2501` | 财务指标行业排名 | `stock/p_stock2501` | `8b6a4cacff0a4b3d88a53755bcaa0136` |
| `p_stock2502` | A股按地区市场统计 | `stock/p_stock2502` | `5093a7b065954b16bbbc015541b2865e` |
| `p_stock2503` | 分红募资统计 | `stock/p_stock2503` | `cf11c1da3afe45d1b04c80fd9da77884` |

### 环球股票数据

#### 环球股票公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_GSCI8201` | 代码与简称对应数据 | `gsci/p_GSCI8201` | `e200d7ae9e624888bf1909c2cc0ed1da` |
| `p_GSCI8203` | 股票基本情况 | `gsci/p_GSCI8203` | `b1d32b5d72f54ab09c90f81671aa648a` |
| `p_GSCI8204` | 公司高管 | `gsci/p_GSCI8204` | `c7b424f907334862af6685176c44b415` |

#### 发行与分配

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_GSCI8205` | 发行 | `gsci/p_GSCI8205` | `cb050496648241149ad49fdac797f429` |
| `p_GSCI8206` | 分配 | `gsci/p_GSCI8206` | `42a499c77c6f4e66b06a39f0a1aa424b` |

#### 股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_GSCI8207` | 股本数据 | `gsci/p_GSCI8207` | `e1a39086614a4bdc966008662fd36fca` |
| `p_GSCI8208` | 股东股权变动表 | `gsci/p_GSCI8208` | `8153d476f78f4a73867f4b9e21ac0f80` |

#### 财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_GSCI8210` | 主要财务指标 | `gsci/p_GSCI8210` | `ef39269263d94db2851742d5b51cdc73` |
| `p_GSCI8211` | 通用资产负债表 | `gsci/p_GSCI8211` | `e55ab9caec37488fab8844d490f8e707` |
| `p_GSCI8212` | 通用利润表 | `gsci/p_GSCI8212` | `6cd20ed213f34f2c8a5ebc51a61cd16d` |
| `p_GSCI8213` | 通用现金流量表 | `gsci/p_GSCI8213` | `75a14b70ff484605a6b59869c9301377` |

#### 公告与新闻

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_GSCI8214` | 环球证券公告 | `gsci/p_GSCI8214` | `276357a00ab94d459bb298c2ece5ae5a` |

### 产业链数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_autokeydata_by_scode` | 智能行业透视 | `bigdata/p_autokeydata_by_scode` | `f1057ab2c62749218582e2c92201a2f4` |
| `p_chain_by_scode` | 公司所属产业链 | `bigdata/p_chain_by_scode` | `81be175244d748ea95a8239b1b0a7867` |
| `p_com_invest` | 沪深AB股对外投资 | `bigdata/p_com_invest` | `91c1bcf4607c49b9b63b6108b96ab8dc` |
| `p_graph_common` | 公司企业族谱 | `bigdata/p_graph_common` | `4b3d4eb54f4c452090a5606bfba20bf9` |
| `p_graph_managers` | 公司高管图谱 | `bigdata/p_graph_managers` | `9d09db010c3e403e801f3e768d4eb68b` |
| `p_graph_neighbor` | 公司搜索和人物搜索 | `bigdata/p_graph_neighbor` | `a58a9502e42a416494d714f82da30d99` |
| `p_intro_by_scode` | 产业链节点简介 | `bigdata/p_intro_by_scode` | `950bd66b54054060bf7af8c95289fa5c` |
| `p_news_by_scode` | 公司舆情数据 | `bigdata/p_news_by_scode` | `f321de1c05a74650bb72344800e7df41` |
| `p_ods3302` | 公司主要行业收入数据 | `stock/p_ods3302` | `73d88cc4b67a49d49e61454f63fa53e3` |
| `p_ods3303` | 行业上下游接口 | `bigdata/p_ods3303` | `4ecbac39a3654eb294a97a0227e03b0a` |
| `p_researchreport_by_scode` | 公司研报数据 | `bigdata/p_researchreport_by_scode` | `8e2a694a90bd48bc8be7bdf9039119f9` |
| `p_typical_by_scode` | 同行业典型公司 | `bigdata/p_typical_by_scode` | `d39620af381643e2a600e3ae67e8a0e5` |

### A股IPO网下配售

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2270` | A股IPO网下配售 | `stock/p_stock2270` | `2700efa58de84b079876769cb4624cfd` |
| `p_stock2270_inc` | A股IPO网下配售 | `load/p_stock2270_inc` | `8892cf3f42604a47abcd6d8cbbb9533d` |

### 股东结构分析

#### 股东结构

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_shareholder4208_1` | 股东结构总览 | `fund/p_shareholder4208_1` | `437de521bb944cc98db2a1e2911a1041` |
| `p_shareholder4208_2` | 股东结构明细 | `fund/p_shareholder4208_2` | `6f17ac69aa784b43ba507834e8c6a070` |
| `p_shareholder4215` | 境外投资者持股 | `stock/p_shareholder4215` | `4112b6c34a4d4bb4a107d96126c8cb4a` |

#### 基金持股

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_shareholder4209` | 基金类股东持股明细 | `fund/p_shareholder4209` | `dc241c75c37241939d4ec9f242260165` |
| `p_shareholder4210` | 基金类股东持股统计 | `fund/p_shareholder4210` | `b92bd4e770ba4bd99ea0c4e07d56f307` |
| `p_shareholder4211` | 基金公司持股统计 | `fund/p_shareholder4211` | `c99bc38fbcf64dc4a394fe49c9204c0f` |
| `p_shareholder4240` | 基金类股东持股市值排名 | `fund/p_shareholder4240` | `47b4f58d6d7a4e99bc0f4397af5fba3e` |
| `p_shareholder4241` | 基金重仓股分析-持股基金数 | `fund/p_shareholder4241` | `e94ec7db1d744a6780b51fd9d2e692f4` |
| `p_shareholder4242` | 基金重仓股分析-重仓股占基金净值比 | `fund/p_shareholder4242` | `ad3287389ccc4363b355f3bfccd9ea5f` |

## 深证信金融科技专区

### 金融分词

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_CwsNer` | 分词、NER | `NLP/p_CwsNer` | `30ca8731d75b47f081488225469f5828` |
| `p_industrys` | 行业树 | `bigdata/p_industrys` | `70b8db7b14364f469eb102129c7e2915` |

## ESG专题数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ESG2156` | ESG公司治理议题智能资讯 | `stock/p_ESG2156` | `fb21b02bf0f5419bbddcf0aa31360a5f` |
| `p_ESG2157` | ESG环境议题智能资讯 | `stock/p_ESG2157` | `f0a1df1715c34e71ab0561a907f9fac7` |
| `p_ESG2158` | ESG社会议题智能资讯接口 | `stock/p_ESG2158` | `47fbf1e18ea341bca095ad9f20eaa33d` |
| `p_ESG2159` | ESG因子库评分 | `stock/p_ESG2159` | `a9f88bc9d6bb41189ed10869c0ecb79b` |
| `p_info3094` | ESG动态数据 | `info/p_info3094` | `cc500afe5d6c4a2a952bceede0f0f572` |

## TTM

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3030` | 新闻数据查询 | `info/p_info3030` | `7aba8a88d224499886309ab515d3fd0b` |
| `p_stock2329` | 个股单季财务利润表 | `stock/p_stock2329` | `af00e0c3965d433998b133c8ae7e2c83` |
| `p_stock2329_inc` | 个股单季财务利润表 | `load/p_stock2329_inc` | `3bb355396aa147a48b0058d8983db753` |
| `p_stock2330` | 个股单季现金流量表 | `stock/p_stock2330` | `50e56707f95d40318cd6700d2ab2b540` |
| `p_stock2330_inc` | 个股单季现金流量表 | `load/p_stock2330_inc` | `4f1592bf5acf4cbf8b475829f116b356` |
| `p_stock2331` | 个股单季财务指标 | `stock/p_stock2331` | `bfed9ba2aa814a34bcdf382896fca762` |
| `p_stock2331_inc` | 个股单季财务指标 | `load/p_stock2331_inc` | `a7ccaaa55bd649bd96cf6bf303718a11` |
| `p_stock2332` | 个股TTM财务利润表 | `stock/p_stock2332` | `a463852dd6c74f27b92bf6419603e381` |
| `p_stock2333` | 个股TTM现金流量表 | `stock/p_stock2333` | `5ec0f9cccfcf44dcbd2e134fb9e4d82c` |
| `p_stock2334` | TTM主要财务指标 | `stock/p_stock2334` | `2380064aeb754424806a14c0708ddd92` |

## 指数样本

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_index2914_inc` | 指数样本股变动表 | `load/p_index2914_inc` | `19579988d4a44071b16325d889fa5a27` |

## 海外数据

### 编码与基础表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_exchangeinfo` | 海外交易所编码查询 | `oversea/p_exchangeinfo` | `6a293193b2184cf5a3cf0e595c332830` |
| `p_geninducls` | 海外通用行业分类查询 | `oversea/p_geninducls` | `40dfbd15023e4aa796a5866f09291c88` |
| `p_mkcode_list` | 海外交易所信息列表 | `oversea/p_mkcode_list` | `3487a7dd08d1478ba0f4000625e1f162` |
| `p_oversea8001` | 海外主要市场证券信息 | `oversea/p_oversea8001` | `2a0a6ee28baa4e5199e3e5e9ac66a15f` |
| `p_oversea8002` | 上市公司机构信息查询 | `oversea/p_oversea8002` | `a2708e91c85345399826e22b9631b23a` |
| `p_oversea8003` | 各货币兑美元汇率查询 | `oversea/p_oversea8003` | `3d54371ce5f7451c9d6046f4404373e1` |
| `p_overseacodelist` | 板块分类所属证券代码查询 | `oversea/p_overseacodelist` | `2892df72df144a488132113885f1e58f` |
| `p_sic` | 海外标准产业分类(SIC)查询 | `oversea/p_sic` | `d06fa54429e7457999a7bee3292d7b18` |
| `p_sysapi1006` | 海外标准产业分类与国证对应关系查询 | `oversea/p_sysapi1006` | `779f9ba43cfc4d3ba26e9be96d437a99` |

### 证券交易与权益变动

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_oversea8007` | 证券市场股票历年派息 | `oversea/p_oversea8007` | `7f43f9f3c3e34ae18a87370b85cd2e23` |
| `p_oversea8008` | 证券市场历史股票除权因子 | `oversea/p_oversea8008` | `ac83fb9e6d88476eab04fbf0acd5bfbb` |
| `p_oversea8009` | 海外行情数据表 | `oversea/p_oversea8009` | `d74604c52eaf4be688631a96f564cf55` |
| `p_oversea8012` | 证券市场股票最新收盘行情 | `oversea/p_oversea8012` | `cccd51113b504739b3d24b9b97696efe` |

### 上市公司股本股东与并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_oversea8005` | 证券市场股票的最新股本 | `oversea/p_oversea8005` | `41ca7fcf37b54f0f97f91699bddabdda` |
| `p_oversea8006` | 证券市场历史股票股本变化 | `oversea/p_oversea8006` | `9b34a583ffad4624aec3b4e891a764c7` |
| `p_oversea8013` | 公司股东持股变动表 | `oversea/p_oversea8013` | `30443a8fec074354b35818374c0de371` |
| `p_oversea8014` | 上市公司并购概况 | `oversea/p_oversea8014` | `12ac57c97a9f4444852a31d7f360824a` |

### 财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_oversea8016` | 最新交易指标表 | `oversea/p_oversea8016` | `8666d115be0d4e9aa03d931e422815d4` |
| `p_oversea8017` | 上市公司通用资产负债表 | `oversea/p_oversea8017` | `65134ec950eb40c38db0ad513b2773bf` |
| `p_oversea8018` | 上市公司通用损益表 | `oversea/p_oversea8018` | `6b162d352c644a9bb0f4a46f3792de62` |
| `p_oversea8018LTM` | 上市公司损益表(最近四季模拟报表) | `oversea/p_oversea8018LTM` | `eaf96f4d87cb47acbe21b89101ac7783` |
| `p_oversea8019` | 上市公司通用现金流量表 | `oversea/p_oversea8019` | `4156ad8fa21e48a58791ff088bf33fb4` |
| `p_oversea8019LTM` | 上市公司现金流量表(最近四季模拟报表) | `oversea/p_oversea8019LTM` | `91ca7b4abaf84a44a35d5c21d338f6f0` |
| `p_oversea8020` | 上市公司财务衍生报表 | `oversea/p_oversea8020` | `041ecedce3ca4b88b7fd9e97dcb23598` |
| `p_oversea8020LTM` | 上市公司财务衍生报告(最近四季模拟报表) | `oversea/p_oversea8020LTM` | `dd16b2fa33fe473b9ff2d4934f7680eb` |
| `p_oversea8021` | 上市公司分行业收入情况表 | `oversea/p_oversea8021` | `9552a6ccece642d280d1eb262fb89af1` |
| `p_oversea8022` | 上市公司分地区收入情况表 | `oversea/p_oversea8022` | `6921288af447422e9c933f522be1d09c` |

### 海外交易所证券代码

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_seccode_oversea` | 海外交易所证券代码表 | `oversea/p_seccode_oversea` | `8f45a12792c04da7b602504a3eed6ab7` |

### 上市公司股东、高管与其他

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_oversea8024` | 上市公司中文简介 | `oversea/p_oversea8024` | `7ced4b851caa49458577416ee0ee7b7d` |

### 美国证券交易所

#### 美国证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_ASE` | 美国证券交易所上市公司中文简介 | `oversea/p_cnintroduce_ASE` | `c8924c94cce645e4a9bfebd7dd783010` |
| `p_executives_ASE` | 美国证券交易所高管 | `oversea/p_executives_ASE` | `9483fcc636744433af509bf09a54a7a6` |
| `p_info_ASE` | 美国证券交易所公司基本情况 | `oversea/p_info_ASE` | `7c5943b349b04b5f86461087d97b7b1f` |

#### 美国证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_ASE` | 美国证券交易所派息 | `oversea/p_dividends_ASE` | `4d0b292641854da4847c4ba1d0967d1a` |

#### 美国证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_ASE` | 美国证券交易所并购 | `oversea/p_manda_ASE` | `0334da78024b44f1a44e21af746a9167` |

#### 美国证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_ASE` | 美国证券交易所股本变化表 | `oversea/p_cine_ASE` | `e194627a00b14a178d23a54e9f01edea` |
| `p_latestequity_ASE` | 美国证券交易所最新股本表 | `oversea/p_latestequity_ASE` | `e5cb0beea35b4c5880f07381c6d87dc8` |
| `p_shareholders_ASE` | 美国证券交易所主要股东表 | `oversea/p_shareholders_ASE` | `f7234d22b34644e7bba9d81dcbe58b12` |

#### 美国证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_ASE` | 美国证券交易所通用现金流量表 | `oversea/p_cashflow_ASE` | `fb56907d831746bbb0d9285fad152d20` |
| `p_finanderive_ASE` | 美国证券交易所财务衍生报表 | `oversea/p_finanderive_ASE` | `3e5d7af08bec47dba1556d39a9f107ba` |
| `p_income_ASE` | 美国证券交易所通用利润表 | `oversea/p_income_ASE` | `5131f76a34df4fcf91df8cfc9b152c31` |
| `p_liabilities_ASE` | 美国证券交易所通用资产负债表 | `oversea/p_liabilities_ASE` | `fed952d874ee409aa122a549ab3f08ed` |
| `p_mainfinance_ASE` | 美国交易所主要财务指标 | `oversea/p_mainfinance_ASE` | `c9462c83562f44bbbe1acfcc277ca168` |
| `p_plateincome_ASE` | 美国证券交易所板块收入情况表 | `oversea/p_plateincome_ASE` | `96214f27323c4b7e8281a1725de09e1b` |
| `p_regionalincome_ASE` | 美国证券交易所地域收入情况表 | `oversea/p_regionalincome_ASE` | `ef6fdb7f22214351a81a6e01651ee542` |
| `p_tranindex_ASE` | 美国证券交易所最新交易指标表 | `oversea/p_tranindex_ASE` | `71814f73d04141a88c7113aa93a81c85` |

#### 美国证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_ASE` | 美国证券交易所行情数据 | `oversea/p_quotadata_ASE` | `7831c15b41ef4678949b5fed37174a46` |
| `p_stockexefactor_ASE` | 美国证券交易所股票除权因子表 | `oversea/p_stockexefactor_ASE` | `5d194721cbd640eaaceb394c2ffd9986` |

### 纽约证券交易所

#### 纽约证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_NYS` | 纽约交易所上市公司中文简介 | `oversea/p_cnintroduce_NYS` | `51648523bc994df3bab1e673a6452d71` |
| `p_executives_NYS` | 纽约交易所高管 | `oversea/p_executives_NYS` | `a6fbd8edc3a5447d8838d62ec5c17126` |
| `p_info_NYS` | 纽约交易所公司基本情况 | `oversea/p_info_NYS` | `0b544b6299e744ed87c7acd37c6f23a6` |

#### 纽约证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_NYS` | 纽约证券交易所派息 | `oversea/p_dividends_NYS` | `eecf5325250c490b9ecd8c00d8baadc9` |

#### 纽约证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_NYS` | 纽约证券交易所并购 | `oversea/p_manda_NYS` | `c52c4982a054457c8d423369cfdc6ae6` |

#### 纽约证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_NYS` | 纽约证券交易所股本变化表 | `oversea/p_cine_NYS` | `bb868e468eb7418bb5bfc52b8f66925b` |
| `p_latestequity_NYS` | 纽约交易所最新股本表 | `oversea/p_latestequity_NYS` | `1bfe750f5496403a94b54910d6b8fd3c` |
| `p_shareholders_NYS` | 纽约证券交易所主要股东表 | `oversea/p_shareholders_NYS` | `4aa7323825414e4583009812983d397a` |

#### 纽约证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_NYS` | 纽约证券交易所通用现金流量表 | `oversea/p_cashflow_NYS` | `484db36c32da49b4bd61f784e1300944` |
| `p_finanderive_NYS` | 纽约证券交易所财务衍生报表 | `oversea/p_finanderive_NYS` | `bdd148f94c7f431fa748bad8e6640b33` |
| `p_income_NYS` | 纽约证券交易所通用利润表 | `oversea/p_income_NYS` | `f79004c38b314fb78dc464a1f623678a` |
| `p_liabilities_NYS` | 纽约证券交易所通用资产负债表 | `oversea/p_liabilities_NYS` | `f8cd6e327dfa48ef80fdaa7a58caf9ca` |
| `p_mainfinance_NYS` | 纽约交易所主要财务指标 | `oversea/p_mainfinance_NYS` | `7faf40799edb4b67a69a3ec3c7e58394` |
| `p_plateincome_NYS` | 纽约证券交易所板块收入情况表 | `oversea/p_plateincome_NYS` | `815d1853739a4349868b4db43cc81ad8` |
| `p_regionalincome_NYS` | 纽约证券交易所地域收入情况表 | `oversea/p_regionalincome_NYS` | `fbc930d89ae04e129196c74ea1825673` |
| `p_tranindex_NYS` | 纽约证券交易所最新交易指标表 | `oversea/p_tranindex_NYS` | `2a058697ae1043baa64ca24e25af7459` |

#### 纽约证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_NYS` | 纽约交易所行情数据 | `oversea/p_quotadata_NYS` | `e56ff3fada1045aa9a0a8e1e5e0fdae5` |
| `p_stockexefactor_NYS` | 纽约交易所股票除权因子表 | `oversea/p_stockexefactor_NYS` | `179f711b0e3c420c8b6b6d6cc2c25884` |

### 纳斯达克证券交易所

#### 纳斯达克证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_NAS` | 纳斯达克交易所上市公司中文简介 | `oversea/p_cnintroduce_NAS` | `1bc58ef0319d4dc597ef5a5453dfa140` |
| `p_executives_NAS` | 纳斯达克交易所高管 | `oversea/p_executives_NAS` | `49e0ef25180c4ba9acf4bc190cc225aa` |
| `p_info_NAS` | 纳斯达克交易所公司基本情况 | `oversea/p_info_NAS` | `608ab33b9bf64ac785c996062ff0fe59` |

#### 纳斯达克证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_NAS` | 纳斯达克交易所派息 | `oversea/p_dividends_NAS` | `7304b9057ad64979966e52c4a8bf9c0d` |

#### 纳斯达克证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_NAS` | 纳斯达克证券交易所并购 | `oversea/p_manda_NAS` | `ba3ac6eb037545deb80a92b071df38d8` |

#### 纳斯达克证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_NAS` | 纳斯达克证券交易所股本变化表 | `oversea/p_cine_NAS` | `eb752d33106d4d6f862b1808706a6a2f` |
| `p_latestequity_NAS` | 纳斯达克交易所最新股本表 | `oversea/p_latestequity_NAS` | `1c0f4c15715e4da1b3776bdf69430906` |
| `p_shareholders_NAS` | 纳斯达克证券交易所主要股东表 | `oversea/p_shareholders_NAS` | `db5fe338093044ccb8ccfecd5a21430a` |

#### 纳斯达克证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_NAS` | 纳斯达克证券交易所通用现金流量表 | `oversea/p_cashflow_NAS` | `066309712f9c45aa8b923a9f93dbf0e0` |
| `p_finanderive_NAS` | 纳斯达克证券交易所财务衍生报表 | `oversea/p_finanderive_NAS` | `85c481728bf94b80a605e476acc127ab` |
| `p_income_NAS` | 纳斯达克证券交易所通用利润表 | `oversea/p_income_NAS` | `736cf51aec6d4c35a9a141d44985e891` |
| `p_liabilities_NAS` | 纳斯达克证券交易所通用资产负债表 | `oversea/p_liabilities_NAS` | `97e2039c367d4ae39342e63fdc26fa70` |
| `p_mainfinance_NAS` | 纳斯达克交易所主要财务指标 | `oversea/p_mainfinance_NAS` | `ba0540173a274594a496d3a5dbc3650a` |
| `p_plateincome_NAS` | 纳斯达克证券交易所板块收入情况表 | `oversea/p_plateincome_NAS` | `5bba228181f046daac72f75ec8b3aade` |
| `p_regionalincome_NAS` | 纳斯达克证券交易所地域收入情况表 | `oversea/p_regionalincome_NAS` | `360745ec32c94cd5a2f1952b03814cc1` |
| `p_tranindex_NAS` | 纳斯达克证券交易所最新交易指标表 | `oversea/p_tranindex_NAS` | `71a4dbff6dc34a13857a0d801da5048d` |

#### 纳斯纳克证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_NAS` | 纳斯达克交易所行情数据 | `oversea/p_quotadata_NAS` | `b51594e458c0479ebcdcc382974094e3` |
| `p_stockexefactor_NAS` | 纳斯达克交易所股票除权因子表 | `oversea/p_stockexefactor_NAS` | `2bda45b3fb6c4cae943a88d9f51d4241` |

### 伦敦证券交易所

#### 伦敦证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_LON` | 伦敦交易所上市公司中文简介 | `oversea/p_cnintroduce_LON` | `b779f9a278924104b813108336539da7` |
| `p_executives_LON` | 伦敦交易所高管 | `oversea/p_executives_LON` | `5f847eae2f0a4e778d53434d9352b84a` |
| `p_info_LON` | 伦敦交易所公司基本情况 | `oversea/p_info_LON` | `af50ae86e6604d1897f7b41e7fa7d00f` |

#### 伦敦证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_LON` | 伦敦证券交易所派息 | `oversea/p_dividends_LON` | `f4517daf876f494e963ec10fd46fed95` |

#### 伦敦证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_LON` | 伦敦证券交易所并购 | `oversea/p_manda_LON` | `aeb2ddbdc21e4834aacfa63f53d9d0f1` |

#### 伦敦证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_LON` | 伦敦证券交易所股本变化表 | `oversea/p_cine_LON` | `5254ed9030c0490dae1aa898fa7ba431` |
| `p_latestequity_LON` | 伦敦交易所最新股本表 | `oversea/p_latestequity_LON` | `3c601e498c6e458cb74df3468279fda9` |
| `p_shareholders_LON` | 伦敦证券交易所主要股东表 | `oversea/p_shareholders_LON` | `5a7bb8dac824424e9aded9cf19d25070` |

#### 伦敦证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_LON` | 伦敦证券交易所通用现金流量表 | `oversea/p_cashflow_LON` | `0cb7ad952dab480aa47188efdc747a37` |
| `p_finanderive_LON` | 伦敦证券交易所财务衍生报表 | `oversea/p_finanderive_LON` | `41ffecee4668454dac9a5d530d71719e` |
| `p_income_LON` | 伦敦证券交易所通用利润表 | `oversea/p_income_LON` | `4e13fbcf148446baac95e14f7b8bd60b` |
| `p_liabilities_LON` | 伦敦证券交易所通用资产负债表 | `oversea/p_liabilities_LON` | `36e0ea40a2ca4ec0ac1bc2385dbeb38d` |
| `p_mainfinance_LON` | 伦敦交易所主要财务指标 | `oversea/p_mainfinance_LON` | `c61a04024562432a8d1f004526c3be74` |
| `p_plateincome_LON` | 伦敦证券交易所板块收入情况表 | `oversea/p_plateincome_LON` | `f8d42f7aa88841ae861f9510519bc261` |
| `p_regionalincome_LON` | 伦敦证券交易所地域收入情况表 | `oversea/p_regionalincome_LON` | `1c4ad005f53740cf99351dd90d578e56` |
| `p_tranindex_LON` | 伦敦证券交易所最新交易指标表 | `oversea/p_tranindex_LON` | `8236da2c6de047e18dd2a09c34d25851` |

#### 伦敦证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_LON` | 伦敦交易所行情数据 | `oversea/p_quotadata_LON` | `c57a9601bc7d4274a027a389e90ae21c` |
| `p_stockexefactor_LON` | 伦敦交易所股票除权因子表 | `oversea/p_stockexefactor_LON` | `40571ba64d2e49c29b05eb80087ac746` |

### 东京证券交易所

#### 东京证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_TKS` | 东京交易所上市公司中文简介 | `oversea/p_cnintroduce_TKS` | `cb2c1351a7a741cc884d06e2054b1edc` |
| `p_executives_TKS` | 东京交易所高管 | `oversea/p_executives_TKS` | `3b77305f8a82410d95047f2c064585f2` |
| `p_info_TKS` | 东京交易所公司基本情况 | `oversea/p_info_TKS` | `b819349d275c45f48fbef570381c3072` |

#### 东京证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_TKS` | 东京证券交易所派息 | `oversea/p_dividends_TKS` | `e4d260c6f52d468581c10e3e36d6f98d` |

#### 东京证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_TKS` | 东京证券交易所并购 | `oversea/p_manda_TKS` | `e819f4474d484b428fb5210950d34c59` |

#### 东京证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_TKS` | 东京证券交易所股本变化表 | `oversea/p_cine_TKS` | `22e5a1c725dd48da95a4b96a6ec85eb2` |
| `p_latestequity_TKS` | 东京交易所最新股本表 | `oversea/p_latestequity_TKS` | `17b057aa22f3482b8ae79c6e8b32824e` |
| `p_shareholders_TKS` | 东京证券交易所主要股东表 | `oversea/p_shareholders_TKS` | `0e90f2ce1b2548fbb5f68c063d3672fa` |

#### 东京证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_TKS` | 东京证券交易所通用现金流量表 | `oversea/p_cashflow_TKS` | `b0209cd82c7a4d16946905ea4eaef2fe` |
| `p_finanderive_TKS` | 东京证券交易所财务衍生报表 | `oversea/p_finanderive_TKS` | `debd80f4cc2340fe89a1ee2b9d39b18a` |
| `p_income_TKS` | 东京证券交易所通用利润表 | `oversea/p_income_TKS` | `ebfd20bd53e048bd84456027ea87ab2e` |
| `p_liabilities_TKS` | 东京证券交易所通用资产负债表 | `oversea/p_liabilities_TKS` | `b02f13d9062c445e9aca2b344c78cf37` |
| `p_mainfinance_TKS` | 东京交易所主要财务指标 | `oversea/p_mainfinance_TKS` | `e4e7397f1ba443c0a516324087e3f58a` |
| `p_plateincome_TKS` | 东京证券交易所板块收入情况表 | `oversea/p_plateincome_TKS` | `a8edc069f8774059b28c22885e99fd59` |
| `p_regionalincome_TKS` | 东京证券交易所地域收入情况表 | `oversea/p_regionalincome_TKS` | `7cd6e92d884f4980ab4a03706c546019` |
| `p_tranindex_TKS` | 东京证券交易所最新交易指标表 | `oversea/p_tranindex_TKS` | `e3289e1cdb0b429a9c8f7dbcf574781b` |

#### 东京证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_TKS` | 东京交易所行情数据 | `oversea/p_quotadata_TKS` | `a4656a79e598415f9a08a13e62388a25` |
| `p_stockexefactor_TKS` | 东京交易所股票除权因子表 | `oversea/p_stockexefactor_TKS` | `bd5fac68fc874d65a9af968e1bb12b79` |

### 巴黎泛欧证券交易所

#### 巴黎泛欧证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_PAR` | 巴黎泛欧交易所交易所上市公司中文简介 | `oversea/p_cnintroduce_PAR` | `27c488a9fd3546d9a64580ce20b267d0` |
| `p_executives_PAR` | 巴黎泛欧交易所交易所高管 | `oversea/p_executives_PAR` | `ee22caeeb528446ca59361d13bb52ae6` |
| `p_info_PAR` | 巴黎泛欧交易所交易所公司基本情况 | `oversea/p_info_PAR` | `c7e435e952a64d51be7445a29b64bbea` |

#### 巴黎泛欧证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_PAR` | 巴黎泛欧交易所派息 | `oversea/p_dividends_PAR` | `4c05f33c712c4fb69e58d953f3aad75e` |

#### 巴黎泛欧证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_PAR` | 巴黎泛欧交易所并购 | `oversea/p_manda_PAR` | `b67d6ce0821c4d5298af40a0dce43649` |

#### 巴黎泛欧证券证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_PAR` | 巴黎泛欧交易所股本变化表 | `oversea/p_cine_PAR` | `6f98a6b87ac043d5a2f5ffc6b7d22098` |
| `p_latestequity_PAR` | 巴黎泛欧交易所交易所最新股本表 | `oversea/p_latestequity_PAR` | `cdc3f5a18d354d138a8fb7495612d78a` |
| `p_shareholders_PAR` | 巴黎泛欧交易所主要股东表 | `oversea/p_shareholders_PAR` | `edb29de05be64065be206d7b98cea65a` |

#### 巴黎泛欧证券证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_PAR` | 巴黎泛欧交易所通用现金流量表 | `oversea/p_cashflow_PAR` | `b3fa818fe6b64d9dbabe4c5c439cc102` |
| `p_finanderive_PAR` | 巴黎泛欧交易所财务衍生报表 | `oversea/p_finanderive_PAR` | `ee3faa62564448bf9eb2ca1d386a5ebc` |
| `p_income_PAR` | 巴黎泛欧交易所通用利润表 | `oversea/p_income_PAR` | `365a5ada7f10413187385959634bef2f` |
| `p_liabilities_PAR` | 巴黎泛欧交易所通用资产负债表 | `oversea/p_liabilities_PAR` | `10c0a6967b844c91803908f15c3aba63` |
| `p_mainfinance_PAR` | 巴黎泛欧交易所主要财务指标 | `oversea/p_mainfinance_PAR` | `b18a68bfd2744bf38bff3069f9461350` |
| `p_plateincome_PAR` | 巴黎泛欧交易所板块收入情况表 | `oversea/p_plateincome_PAR` | `312dff5f21c240c69888d1c9526cc0a6` |
| `p_regionalincome_PAR` | 巴黎泛欧交易所地域收入情况表 | `oversea/p_regionalincome_PAR` | `3adf8b2aa5654faa999628462623d8fe` |
| `p_tranindex_PAR` | 巴黎泛欧交易所最新交易指标表 | `oversea/p_tranindex_PAR` | `842ae36087c74ebfb5389d9d2bd8a98f` |

#### 巴黎泛欧证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_PAR` | 巴黎泛欧交易所交易所行情数据 | `oversea/p_quotadata_PAR` | `79ad6fb2c3ed4dadb82cf63beb641512` |
| `p_stockexefactor_PAR` | 巴黎泛欧交易所交易所股票除权因子表 | `oversea/p_stockexefactor_PAR` | `e110b7ff1c6247ee967e432c4305713d` |

### 多伦多证券交易所

#### 多伦多证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_TSE` | 多伦多交易所上市公司中文简介 | `oversea/p_cnintroduce_TSE` | `3e54528064f2486f85f13cb5b6817be9` |
| `p_executives_TSE` | 多伦多交易所高管 | `oversea/p_executives_TSE` | `bab5129b2fc64d358ccb3bbf7b51416f` |
| `p_info_TSE` | 多伦多交易所公司基本情况 | `oversea/p_info_TSE` | `62047d92978046c4ba5cdb4366edb568` |

#### 多伦多证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_TSE` | 多伦多交易所派息 | `oversea/p_dividends_TSE` | `4b4bff86b3b24ae5820a5411000cf320` |

#### 多伦多证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_TSE` | 多伦多交易所并购 | `oversea/p_manda_TSE` | `68adc1974ce740bfab57783783766fd4` |

#### 多伦多证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_TSE` | 多伦多交易所股本变化表 | `oversea/p_cine_TSE` | `fdfd75d8c254415db322bc8877260d6a` |
| `p_latestequity_TSE` | 多伦多交易所最新股本表 | `oversea/p_latestequity_TSE` | `a71dc16b11974813b5ccff3cbfcf134c` |
| `p_shareholders_TSE` | 多伦多交易所主要股东表 | `oversea/p_shareholders_TSE` | `152a25eaef1d4fb8b566b31a17ff425b` |

#### 多伦多证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_TSE` | 多伦多交易所通用现金流量表 | `oversea/p_cashflow_TSE` | `c2c0f397ee724e86aab688259383f6cc` |
| `p_finanderive_TSE` | 多伦多交易所财务衍生报表 | `oversea/p_finanderive_TSE` | `a9d411863fc744f4ae84ffffa111aa80` |
| `p_income_TSE` | 多伦多交易所通用利润表 | `oversea/p_income_TSE` | `ed141b3d36c340beb37448e3deffef52` |
| `p_liabilities_TSE` | 多伦多交易所通用资产负债表 | `oversea/p_liabilities_TSE` | `fb32a7801bca4403b112f3878df8b663` |
| `p_mainfinance_TSE` | 多伦多交易所主要财务指标 | `oversea/p_mainfinance_TSE` | `4d2cd54a6b79438cab17cbbb201af4ac` |
| `p_plateincome_TSE` | 多伦多交易所板块收入情况表 | `oversea/p_plateincome_TSE` | `bd44fe6ebbdd4042b1e867a7cce0d3ae` |
| `p_regionalincome_TSE` | 多伦多交易所地域收入情况表 | `oversea/p_regionalincome_TSE` | `d1422d77edc64bcab2210595b97aa6d5` |
| `p_tranindex_TSE` | 多伦多交易所最新交易指标表 | `oversea/p_tranindex_TSE` | `95b0ecbb72a14306a994db494cf02265` |

#### 多伦多证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_TSE` | 多伦多交易所行情数据 | `oversea/p_quotadata_TSE` | `8961d22559f546a381b14275947b3901` |
| `p_stockexefactor_TSE` | 多伦多交易所股票除权因子表 | `oversea/p_stockexefactor_TSE` | `93a40cbb675b42faa57a1147efc08eaa` |

### 多伦多证券交易所创业板

#### 多伦多证券交易所创业板公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_TSX` | 多伦多创业板上市公司中文简介 | `oversea/p_cnintroduce_TSX` | `c6515eec518c4df6b53bdb0d635c9c29` |
| `p_executives_TSX` | 多伦多创业板高管 | `oversea/p_executives_TSX` | `577f1e4436f144d9b2e1922d9bfbfa1f` |
| `p_info_TSX` | 多伦多创业板公司基本情况 | `oversea/p_info_TSX` | `4e232b5e3cdf4c5d8a626f4278ec078f` |

#### 多伦多证券交易所创业板公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_TSX` | 多伦多创业板派息 | `oversea/p_dividends_TSX` | `81386b5b6e344a7590050065e13634f7` |

#### 多伦多证券交易所创业板公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_TSX` | 多伦多创业板并购 | `oversea/p_manda_TSX` | `2d8dde360ea242dd9e47f3b6fa6ab332` |

#### 多伦多证券交易所创业板股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_TSX` | 多伦多创业板股本变化表 | `oversea/p_cine_TSX` | `d4629d7936f0441393cfec9d6a1cb307` |
| `p_latestequity_TSX` | 多伦多创业板最新股本表 | `oversea/p_latestequity_TSX` | `00a79721fefb40438fb7ca3f3285e702` |
| `p_shareholders_TSX` | 多伦多创业板主要股东表 | `oversea/p_shareholders_TSX` | `f15003883a8a4d22aa4a93dd33c33258` |

#### 多伦多证券交易所创业板财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_TSX` | 多伦多创业板通用现金流量表 | `oversea/p_cashflow_TSX` | `af8da3da4b35410fac50dd61ef590cea` |
| `p_finanderive_TSX` | 多伦多创业板财务衍生报表 | `oversea/p_finanderive_TSX` | `bd7e601a44df4611afed4a19883a1b81` |
| `p_income_TSX` | 多伦多创业板通用利润表 | `oversea/p_income_TSX` | `fa2989c9531d41f9a16ef51ff3f06980` |
| `p_liabilities_TSX` | 多伦多创业板通用资产负债表 | `oversea/p_liabilities_TSX` | `54dfc748cb5849b0a42e3656a5bb880c` |
| `p_mainfinance_TSX` | 多伦多创业板主要财务指标 | `oversea/p_mainfinance_TSX` | `b43ea2fb7444486b8ee26d1e052c0623` |
| `p_plateincome_TSX` | 多伦多创业板板块收入情况表 | `oversea/p_plateincome_TSX` | `80b0b0a09ad54a2880a231eb4abdce7d` |
| `p_regionalincome_TSX` | 多伦多创业板地域收入情况表 | `oversea/p_regionalincome_TSX` | `f1536c1616ed43a0a4a3b2da0e6ff4a7` |
| `p_tranindex_TSX` | 多伦多创业板最新交易指标表 | `oversea/p_tranindex_TSX` | `8fca5707a67f451b8d5c3552cff8a947` |

#### 多伦多证券交易所创业板行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_TSX` | 多伦多创业板行情数据 | `oversea/p_quotadata_TSX` | `8eaef4edb2c047e2bf9278f503aea17a` |
| `p_stockexefactor_TSX` | 多伦多创业板股票除权因子表 | `oversea/p_stockexefactor_TSX` | `5e33874b3a784e67bd9bff611d482742` |

### 澳大利亚证券交易所

#### 澳大利亚证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_ASX` | 澳大利亚交易所上市公司中文简介 | `oversea/p_cnintroduce_ASX` | `c0f0ed609e894aeaaf76abdca27d1954` |
| `p_executives_ASX` | 澳大利亚交易所高管 | `oversea/p_executives_ASX` | `7ad07e8e363140e89b67681a678682f6` |
| `p_info_ASX` | 澳大利亚交易所公司基本情况 | `oversea/p_info_ASX` | `df13d4a0b8aa46c0b6e07d6b9de8c9f0` |

#### 澳大利亚证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_ASX` | 澳大利亚交易所派息 | `oversea/p_dividends_ASX` | `7d4cb8527d9b48ba878c6769507a2b4b` |

#### 澳大利亚证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_ASX` | 澳大利亚交易所并购 | `oversea/p_manda_ASX` | `73798078c1b24b0095c94d03de0d160e` |

#### 澳大利亚证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_ASX` | 澳大利亚交易所股本变化表 | `oversea/p_cine_ASX` | `369793b07d064a348a534ce3a0f1dc02` |
| `p_latestequity_ASX` | 澳大利亚交易所最新股本表 | `oversea/p_latestequity_ASX` | `ddfbf807b3d0490ba1f39d2f65365db2` |
| `p_shareholders_ASX` | 澳大利亚交易所主要股东表 | `oversea/p_shareholders_ASX` | `9ab9d679e7e544369d7d39606b4e5f4b` |

#### 澳大利亚证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_ASX` | 澳大利亚交易所通用现金流量表 | `oversea/p_cashflow_ASX` | `49afa4c9072141119106749f6dabd4a0` |
| `p_finanderive_ASX` | 澳大利亚交易所财务衍生报表 | `oversea/p_finanderive_ASX` | `e07c3dd45cd74fdd8f12ba6a4e234547` |
| `p_income_ASX` | 澳大利亚交易所通用利润表 | `oversea/p_income_ASX` | `cd152920ebf14c009f30de248038eb66` |
| `p_liabilities_ASX` | 澳大利亚交易所通用资产负债表 | `oversea/p_liabilities_ASX` | `1663de8e2adc4f7cb2bdb7b2944dec9a` |
| `p_mainfinance_ASX` | 澳大利亚交易所主要财务指标 | `oversea/p_mainfinance_ASX` | `db211939047d4ffd90d307abc87f3950` |
| `p_plateincome_ASX` | 澳大利亚交易所板块收入情况表 | `oversea/p_plateincome_ASX` | `3de51a6932684a6bad227d4a6cdd63c0` |
| `p_regionalincome_ASX` | 澳大利亚交易所地域收入情况表 | `oversea/p_regionalincome_ASX` | `f22f917cc11047c6882e811780a4e422` |
| `p_tranindex_ASX` | 澳大利亚交易所最新交易指标表 | `oversea/p_tranindex_ASX` | `49f194cae581466b8abfd5ded76e3d59` |

#### 澳大利亚证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_ASX` | 澳大利亚交易所行情数据 | `oversea/p_quotadata_ASX` | `2d27d62634fa4ceebda86f013f90f723` |
| `p_stockexefactor_ASX` | 澳大利亚交易所股票除权因子表 | `oversea/p_stockexefactor_ASX` | `4687c1dc96ff43f4944ada1ed6c1b087` |

### 西班牙证券交易所

#### 西班牙证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_MCE` | 西班牙交易所上市公司中文简介 | `oversea/p_cnintroduce_MCE` | `c4a1a219aa1848f9a17bf5bef29e4b83` |
| `p_executives_MCE` | 西班牙交易所高管 | `oversea/p_executives_MCE` | `db8123f974a8443da907650078d98c5c` |
| `p_info_MCE` | 西班牙交易所公司基本情况 | `oversea/p_info_MCE` | `cf21f0b4525244a8ae4a1848ce7fe6cf` |

#### 西班牙证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_MCE` | 西班牙交易所派息 | `oversea/p_dividends_MCE` | `0848a793f45f45bd9964cf1335826ad4` |

#### 西班牙证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_MCE` | 西班牙交易所并购 | `oversea/p_manda_MCE` | `71f23bc750864fd2a9852ef11f324dd6` |

#### 西班牙证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_MCE` | 西班牙交易所股本变化表 | `oversea/p_cine_MCE` | `f1a1bff82cdc4d8a93588c97a2510aa1` |
| `p_latestequity_MCE` | 西班牙交易所最新股本表 | `oversea/p_latestequity_MCE` | `ac968069394141acbbce7d89f41bcc92` |
| `p_shareholders_MCE` | 西班牙交易所主要股东表 | `oversea/p_shareholders_MCE` | `7ae0d5655e924a72975b675781e7e0a8` |

#### 西班牙证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_MCE` | 西班牙交易所通用现金流量表 | `oversea/p_cashflow_MCE` | `a85c6d205dbe4cdea3347a2f72b51d2f` |
| `p_finanderive_MCE` | 西班牙交易所财务衍生报表 | `oversea/p_finanderive_MCE` | `a07252ebe67b41fe970c36de3c17e5aa` |
| `p_income_MCE` | 西班牙交易所通用利润表 | `oversea/p_income_MCE` | `b4ebfbdbb86646d984f7d9b04701c73a` |
| `p_liabilities_MCE` | 西班牙交易所通用资产负债表 | `oversea/p_liabilities_MCE` | `cdd62e8ffd7a402fa338103ec0028c50` |
| `p_mainfinance_MCE` | 西班牙交易所主要财务指标 | `oversea/p_mainfinance_MCE` | `25a21b261ef043118df2c7f904b5b625` |
| `p_plateincome_MCE` | 西班牙交易所板块收入情况表 | `oversea/p_plateincome_MCE` | `e734134088bb45da9cf45888cf84e083` |
| `p_regionalincome_MCE` | 西班牙交易所地域收入情况表 | `oversea/p_regionalincome_MCE` | `11ca7abdf1d24940aa16ef2bedbc3167` |
| `p_tranindex_MCE` | 西班牙交易所最新交易指标表 | `oversea/p_tranindex_MCE` | `acfd4249759649909c10ab5bd45922b8` |

#### 西班牙证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_MCE` | 西班牙交易所行情数据 | `oversea/p_quotadata_MCE` | `144a3778844e4e08b842fae5be784978` |
| `p_stockexefactor_MCE` | 西班牙交易所股票除权因子表 | `oversea/p_stockexefactor_MCE` | `b137d39c83154d078efa909be3d24484` |

### 法兰克福证券交易所

#### 法兰克福证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_FRA` | 法兰克福交易所上市公司中文简介 | `oversea/p_cnintroduce_FRA` | `df677ca04e2a40b792d47bc2c606f84b` |
| `p_executives_FRA` | 法兰克福交易所高管 | `oversea/p_executives_FRA` | `3bba85d749a24d97833640a9e5313bd5` |
| `p_info_FRA` | 法兰克福交易所公司基本情况 | `oversea/p_info_FRA` | `6bc21d932f8e40c588d705b12baf5238` |

#### 法兰克福证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_FRA` | 法兰克福交易所派息 | `oversea/p_dividends_FRA` | `2dcaff3594a441e8b97eef9f65889715` |

#### 法兰克福证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_FRA` | 法兰克福交易所并购 | `oversea/p_manda_FRA` | `136dfd4f434c46a699da382749b2caa6` |

#### 法兰克福证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_FRA` | 法兰克福交易所股本变化表 | `oversea/p_cine_FRA` | `cac7c6f4ee2548e483c06ee38c1444a3` |
| `p_latestequity_FRA` | 法兰克福交易所最新股本表 | `oversea/p_latestequity_FRA` | `5adba13e24154be7899433fbc4e5608f` |
| `p_shareholders_FRA` | 法兰克福交易所主要股东表 | `oversea/p_shareholders_FRA` | `fa608017c8244d528b7d7e0dcb0da21b` |

#### 法兰克福证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_FRA` | 法兰克福交易所通用现金流量表 | `oversea/p_cashflow_FRA` | `31e2a70a5f164ce9961b84f6995269fc` |
| `p_finanderive_FRA` | 法兰克福交易所财务衍生报表 | `oversea/p_finanderive_FRA` | `16e22268c9be4c43a02a4eea7d8ccd69` |
| `p_income_FRA` | 法兰克福交易所通用利润表 | `oversea/p_income_FRA` | `d4d054a084c74a14ae47c446a7c3c4ba` |
| `p_liabilities_FRA` | 法兰克福交易所通用资产负债表 | `oversea/p_liabilities_FRA` | `0488826fa8e94ef7ac6786ff76aae261` |
| `p_mainfinance_FRA` | 法兰克福交易所主要财务指标 | `oversea/p_mainfinance_FRA` | `948f5ffc783b4fa892c7a5729a359c0a` |
| `p_plateincome_FRA` | 法兰克福交易所板块收入情况表 | `oversea/p_plateincome_FRA` | `2bfbd6b8821e40c4a20c1a547402cb70` |
| `p_regionalincome_FRA` | 法兰克福交易所地域收入情况表 | `oversea/p_regionalincome_FRA` | `d09e44c4bafa4d4b89e8f2ddda51f57c` |
| `p_tranindex_FRA` | 法兰克福交易所最新交易指标表 | `oversea/p_tranindex_FRA` | `9a6c6e01f7474c7e895def6276563849` |

#### 法兰克福证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_FRA` | 法兰克福交易所行情数据 | `oversea/p_quotadata_FRA` | `0cd8939587014a9782cced81415c1ed7` |
| `p_stockexefactor_FRA` | 法兰克福交易所股票除权因子表 | `oversea/p_stockexefactor_FRA` | `5186a21ce2294d05a697d40185bc1197` |

### 德国证券交易所

#### 德国证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_ETR` | 德国交易所上市公司中文简介 | `oversea/p_cnintroduce_ETR` | `cb831405525c430599126d960fa39b45` |
| `p_executives_ETR` | 德国交易所高管 | `oversea/p_executives_ETR` | `f11de4c4c1494ea993961728b7a95e5b` |
| `p_info_ETR` | 德国交易所公司基本情况 | `oversea/p_info_ETR` | `c69ac4e8a6c34bc7b275a2a54e6a01c6` |

#### 德国证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_ETR` | 德国交易所派息 | `oversea/p_dividends_ETR` | `b5fc85e365b44b22854411a5b36edc40` |

#### 德国证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_ETR` | 德国交易所并购 | `oversea/p_manda_ETR` | `30bc3f714bc14c62848ee5b279ee5546` |

#### 德国证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_ETR` | 德国交易所股本变化表 | `oversea/p_cine_ETR` | `2d5e89b762154a64b3596b0dbf09cb6e` |
| `p_latestequity_ETR` | 德国交易所最新股本表 | `oversea/p_latestequity_ETR` | `c548fa7e0c8b40b6ad8e7fcbd88f2650` |
| `p_shareholders_ETR` | 德国交易所主要股东表 | `oversea/p_shareholders_ETR` | `01f636a7fe9d4eb28adcc9cff276eb12` |

#### 德国证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_ETR` | 德国交易所通用现金流量表 | `oversea/p_cashflow_ETR` | `28c36ebd26de4b4199eea0034d1a808c` |
| `p_finanderive_ETR` | 德国交易所财务衍生报表 | `oversea/p_finanderive_ETR` | `290f21d6829545b580ace248f9b34c37` |
| `p_income_ETR` | 德国交易所通用利润表 | `oversea/p_income_ETR` | `5a7e2c69b09b4b92b425411d2e0b8222` |
| `p_liabilities_ETR` | 德国交易所通用资产负债表 | `oversea/p_liabilities_ETR` | `198d367d48454b418826750012b48a88` |
| `p_mainfinance_ETR` | 德国交易所主要财务指标 | `oversea/p_mainfinance_ETR` | `1909ebbeae47451c9cf24446efbbe285` |
| `p_plateincome_ETR` | 德国交易所板块收入情况表 | `oversea/p_plateincome_ETR` | `92a5e31badf84df0867dd07b66391422` |
| `p_regionalincome_ETR` | 德国交易所地域收入情况表 | `oversea/p_regionalincome_ETR` | `230527d578644805ac3c9c760554cde2` |
| `p_tranindex_ETR` | 德国交易所最新交易指标表 | `oversea/p_tranindex_ETR` | `6d7d6a44f03445a3b645ffac69e691a5` |

#### 德国证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_ETR` | 德国交易所行情数据 | `oversea/p_quotadata_ETR` | `762806f9a3cd4794a99c44331eafe87f` |
| `p_stockexefactor_ETR` | 德国交易所股票除权因子表 | `oversea/p_stockexefactor_ETR` | `054219d3c71e47ba905bbf6e5301c285` |

### 日本股市二板市场交易所

#### 日本股市二板市场交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_JAS` | 日本股市二板市场上市公司中文简介 | `oversea/p_cnintroduce_JAS` | `a4bed394f7d74c3b9a71c85c68f98ccc` |
| `p_executives_JAS` | 日本股市二板市场高管 | `oversea/p_executives_JAS` | `07dbbec5490d4ba7946ed43bb6e462d8` |
| `p_info_JAS` | 日本股市二板市场公司基本情况 | `oversea/p_info_JAS` | `a8255e81e45848848090dab199de8644` |

#### 日本股市二板市场交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_JAS` | 日本股市二板市场派息 | `oversea/p_dividends_JAS` | `33d9f64550d54237b7ad09cda633014d` |

#### 日本股市二板市场交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_JAS` | 日本股市二板市场并购 | `oversea/p_manda_JAS` | `12eaf9f21d59491baca90edb8a8e7c41` |

#### 日本股市二板市场交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_JAS` | 日本股市二板市场股本变化表 | `oversea/p_cine_JAS` | `88aaee7d54724a9996534eb340dd3158` |
| `p_latestequity_JAS` | 日本股市二板市场最新股本表 | `oversea/p_latestequity_JAS` | `4a3b1d5f7be94c12b594e0b5e1eb6656` |
| `p_shareholders_JAS` | 日本股市二板市场主要股东表 | `oversea/p_shareholders_JAS` | `4f766a8533ac4239ba821882084d0528` |

#### 日本股市二板市场交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_JAS` | 日本股市二板市场通用现金流量表 | `oversea/p_cashflow_JAS` | `a35d72cf274249d6a076c9f76cfa6642` |
| `p_finanderive_JAS` | 日本股市二板市场财务衍生报表 | `oversea/p_finanderive_JAS` | `a4b54e8a62914c91a313f469e68144e8` |
| `p_income_JAS` | 日本股市二板市场通用利润表 | `oversea/p_income_JAS` | `452055b13d9340c2ad6b6b1703ff1ff8` |
| `p_liabilities_JAS` | 日本股市二板市场通用资产负债表 | `oversea/p_liabilities_JAS` | `878d31f5564d4ab493c8bf07d818d119` |
| `p_mainfinance_JAS` | 日本股市二板市场主要财务指标 | `oversea/p_mainfinance_JAS` | `ccbfdf73c76e40618d20d0715ca1ebf9` |
| `p_plateincome_JAS` | 日本股市二板市场板块收入情况表 | `oversea/p_plateincome_JAS` | `e478b40075bc416fa3aeacc88c47eefb` |
| `p_regionalincome_JAS` | 日本股市二板市场地域收入情况表 | `oversea/p_regionalincome_JAS` | `aed16b774bcc4479a578f3ba9a1edbf5` |
| `p_tranindex_JAS` | 日本股市二板市场最新交易指标表 | `oversea/p_tranindex_JAS` | `d8bcf7188eca4c478ac8010f4bb51b40` |

#### 日本股市二板市场交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_JAS` | 日本股市二板市场行情数据 | `oversea/p_quotadata_JAS` | `d70f16bca565485e9fc47064d6832381` |
| `p_stockexefactor_JAS` | 日本股市二板市场股票除权因子表 | `oversea/p_stockexefactor_JAS` | `42dd77643d604036b0813513b6379eb9` |

### 孟买证券交易所

#### 孟买证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_BOM` | 孟买交易所上市公司中文简介 | `oversea/p_cnintroduce_BOM` | `c58ecc1e6950445abb39ad04adc0aad2` |
| `p_executives_BOM` | 孟买交易所高管 | `oversea/p_executives_BOM` | `8dc2626531cf44f48aa5d4444fa77fea` |
| `p_info_BOM` | 孟买交易所公司基本情况 | `oversea/p_info_BOM` | `138242f1c17a4315932297e052824f8f` |

#### 孟买证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_BOM` | 孟买证券交易所派息 | `oversea/p_dividends_BOM` | `d1855953b2c34d17a92a98fb71b2b68b` |

#### 孟买证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_BOM` | 孟买证券交易所并购 | `oversea/p_manda_BOM` | `8ee5ab50a9314fceaa2b21682eedef9e` |

#### 孟买证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_BOM` | 孟买证券交易所股本变化表 | `oversea/p_cine_BOM` | `390cc336d69143c99334f6296ac1509a` |
| `p_latestequity_BOM` | 孟买交易所最新股本表 | `oversea/p_latestequity_BOM` | `ff8e9d800abd472993deb14bdd97af4a` |
| `p_shareholders_BOM` | 孟买证券交易所主要股东表 | `oversea/p_shareholders_BOM` | `c3d34bd2a33f4be6bc6ddfa29ba80e1b` |

#### 孟买证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_BOM` | 孟买证券交易所通用现金流量表 | `oversea/p_cashflow_BOM` | `7421cea59bde4648ae19b2224d071e92` |
| `p_finanderive_BOM` | 孟买证券交易所财务衍生报表 | `oversea/p_finanderive_BOM` | `2dd8785665d74ec09374e7fb253b569c` |
| `p_income_BOM` | 孟买证券交易所通用利润表 | `oversea/p_income_BOM` | `132cb9fd6f2348abaacc8ea36d0e2a50` |
| `p_liabilities_BOM` | 孟买证券交易所通用资产负债表 | `oversea/p_liabilities_BOM` | `c40255278b93451a86053b34e843dc60` |
| `p_mainfinance_BOM` | 孟买交易所主要财务指标 | `oversea/p_mainfinance_BOM` | `9acf8bd252a14cfcac7faba5f012694b` |
| `p_plateincome_BOM` | 孟买证券交易所板块收入情况表 | `oversea/p_plateincome_BOM` | `1e230e6e6fdf4ea3bcf5c7debb647c74` |
| `p_regionalincome_BOM` | 孟买证券交易所地域收入情况表 | `oversea/p_regionalincome_BOM` | `5bcfa616af1a4dbba07b7a9c5603a7a6` |
| `p_tranindex_BOM` | 孟买证券交易所最新交易指标表 | `oversea/p_tranindex_BOM` | `c1cbaa0ce4ce41618c497923b805b7bc` |

#### 孟买证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_BOM` | 孟买交易所行情数据 | `oversea/p_quotadata_BOM` | `347d34ff08ec4d458a5d74b9670375ea` |
| `p_stockexefactor_BOM` | 孟买交易所股票除权因子表 | `oversea/p_stockexefactor_BOM` | `df1c68c7b08640f88735d41f55afc19b` |

### 马来西亚证券交易所

#### 马来西亚证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_KLS` | 马来西亚交易所上市公司中文简介 | `oversea/p_cnintroduce_KLS` | `d9eb750141ea4673bcbb945fc61cf923` |
| `p_executives_KLS` | 马来西亚交易所高管 | `oversea/p_executives_KLS` | `8a30a6d47d804180a952603edc4fdf63` |
| `p_info_KLS` | 马来西亚交易所公司基本情况 | `oversea/p_info_KLS` | `0a1e63ab606b46fd946a8d1effe78952` |

#### 马来西亚证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_KLS` | 马来西亚交易所派息 | `oversea/p_dividends_KLS` | `571fa12945df484b8cbfda773082451a` |

#### 马来西亚证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_KLS` | 马来西亚交易所并购 | `oversea/p_manda_KLS` | `90f5e808a5724cc98539426a89271afc` |

#### 马来西亚证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_KLS` | 马来西亚交易所股本变化表 | `oversea/p_cine_KLS` | `7d4bf55b3301405e951fdc889937c79c` |
| `p_latestequity_KLS` | 马来西亚交易所最新股本表 | `oversea/p_latestequity_KLS` | `fb038c91f5e64eae8bfefd60eb30492d` |
| `p_shareholders_KLS` | 马来西亚交易所主要股东表 | `oversea/p_shareholders_KLS` | `76ea7156792b40e6a24b937189cbcdd1` |

#### 马来西亚证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_KLS` | 马来西亚交易所通用现金流量表 | `oversea/p_cashflow_KLS` | `201ba648a25b4d729fd2121c218eaa40` |
| `p_finanderive_KLS` | 马来西亚交易所财务衍生报表 | `oversea/p_finanderive_KLS` | `6f85328732954ff5a417e124dd452dbd` |
| `p_income_KLS` | 马来西亚交易所通用利润表 | `oversea/p_income_KLS` | `3aedbe7ef4114810a9a28c10ef5425c2` |
| `p_liabilities_KLS` | 马来西亚交易所通用资产负债表 | `oversea/p_liabilities_KLS` | `c1cc447334044f0f9f517612f2ae954a` |
| `p_mainfinance_KLS` | 马来西亚交易所主要财务指标 | `oversea/p_mainfinance_KLS` | `0cd07e46ca58402ebb1b68b983d999d1` |
| `p_plateincome_KLS` | 马来西亚交易所板块收入情况表 | `oversea/p_plateincome_KLS` | `4453339350994236a326e66d244d9780` |
| `p_regionalincome_KLS` | 马来西亚交易所地域收入情况表 | `oversea/p_regionalincome_KLS` | `7440840f03fc45b0a69314585f2b997e` |
| `p_tranindex_KLS` | 马来西亚交易所最新交易指标表 | `oversea/p_tranindex_KLS` | `c5ea81c970274cd69ab3f5e739b6d60d` |

#### 马来西亚证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_KLS` | 马来西亚交易所行情数据 | `oversea/p_quotadata_KLS` | `18e4e4997ade4936af3e3df630d5d36d` |
| `p_stockexefactor_KLS` | 马来西亚交易所股票除权因子表 | `oversea/p_stockexefactor_KLS` | `96d92a2968354f76ba1412ccb76627a1` |

### 台北证券交易所

#### 台北证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_ROCO` | 台北交易所上市公司中文简介 | `oversea/p_cnintroduce_ROCO` | `0d0353445d4e47c0a6a8d69d33105e42` |
| `p_executives_ROCO` | 台北交易所高管 | `oversea/p_executives_ROCO` | `e217f29c275c4097ad325588d4a8c575` |
| `p_info_ROCO` | 台北交易所公司基本情况 | `oversea/p_info_ROCO` | `52e2d8152e93419da73c4773b3f0847d` |

#### 台北证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_ROCO` | 台北交易所派息 | `oversea/p_dividends_ROCO` | `dc47283e295747dbad044311048b86c3` |

#### 台北证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_ROCO` | 台北交易所并购 | `oversea/p_manda_ROCO` | `5342932b96134a4182bec3c4859db75f` |

#### 台北证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_ROCO` | 台北交易所股本变化表 | `oversea/p_cine_ROCO` | `e37344d71df14e35a7549443d6a2e7ee` |
| `p_latestequity_ROCO` | 台北交易所最新股本表 | `oversea/p_latestequity_ROCO` | `1bbffbc72b0c4609a48b931a4b5010a8` |
| `p_shareholders_ROCO` | 台北交易所主要股东表 | `oversea/p_shareholders_ROCO` | `f457d1b6520e4c60a1ebc1ec6ddd9b14` |

#### 台北证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_ROCO` | 台北交易所通用现金流量表 | `oversea/p_cashflow_ROCO` | `b941301f291b40219b88bfb7e6d0a5a4` |
| `p_finanderive_ROCO` | 台北交易所财务衍生报表 | `oversea/p_finanderive_ROCO` | `11087c6f8f9a40aab0cbe1271076cbe5` |
| `p_income_ROCO` | 台北交易所通用利润表 | `oversea/p_income_ROCO` | `635be9db18b640589daa47a07ca68389` |
| `p_liabilities_ROCO` | 台北交易所通用资产负债表 | `oversea/p_liabilities_ROCO` | `1ca0fd8bcc5946f5a4427f3e4ae72b69` |
| `p_mainfinance_ROCO` | 台北交易所主要财务指标 | `oversea/p_mainfinance_ROCO` | `040aa9fd121a40b39e6a1d837f145678` |
| `p_plateincome_ROCO` | 台北交易所板块收入情况表 | `oversea/p_plateincome_ROCO` | `5852a9532ce942ed8b9d54d46fe8f2a3` |
| `p_regionalincome_ROCO` | 台北交易所地域收入情况表 | `oversea/p_regionalincome_ROCO` | `c968ebf4ecc048c4b2b515f33a66d8f2` |
| `p_tranindex_ROCO` | 台北交易所最新交易指标表 | `oversea/p_tranindex_ROCO` | `7349430ec170483193af8243bb79ae82` |

#### 台北证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_ROCO` | 台北交易所行情数据 | `oversea/p_quotadata_ROCO` | `a596b86ddd4440f487dd2679afe3b980` |
| `p_stockexefactor_ROCO` | 台北交易所股票除权因子表 | `oversea/p_stockexefactor_ROCO` | `7524146816254d1cb512b271c8f87468` |

### 台湾证券交易所

#### 台湾证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_TAI` | 台湾交易所上市公司中文简介 | `oversea/p_cnintroduce_TAI` | `d7c57b3879814f0d94303e5f715eaeda` |
| `p_executives_TAI` | 台湾交易所高管 | `oversea/p_executives_TAI` | `0a5ea2ae13364c2cb5ac1ade818b8363` |
| `p_info_TAI` | 台湾交易所公司基本情况 | `oversea/p_info_TAI` | `ad7206057acb430595f3cdd4df6b9d8a` |

#### 台湾证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_TAI` | 台湾交易所派息 | `oversea/p_dividends_TAI` | `3bd991cd717540ee8d5c5513dae2b642` |

#### 台湾证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_TAI` | 台湾交易所并购 | `oversea/p_manda_TAI` | `3207520fb9414bf388131ca98189ddf9` |

#### 台湾证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_TAI` | 台湾交易所股本变化表 | `oversea/p_cine_TAI` | `640c9f1aef7142e8aa48b0d764f8966d` |
| `p_latestequity_TAI` | 台湾交易所最新股本表 | `oversea/p_latestequity_TAI` | `91eefa5a1e2543d9a9d115c11007ab46` |
| `p_shareholders_TAI` | 台湾交易所主要股东表 | `oversea/p_shareholders_TAI` | `11fa7e1f0c914322be3e064ca958fa06` |

#### 台湾证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_TAI` | 台湾交易所通用现金流量表 | `oversea/p_cashflow_TAI` | `2d2bf5623f9c47b1adec64c098470dd1` |
| `p_finanderive_TAI` | 台湾交易所财务衍生报表 | `oversea/p_finanderive_TAI` | `06d3ee1d2f0a42dab0d0c3c274ee3f7f` |
| `p_income_TAI` | 台湾交易所通用利润表 | `oversea/p_income_TAI` | `8cd8f22224714a68b6edb20906a375bc` |
| `p_liabilities_TAI` | 台湾交易所通用资产负债表 | `oversea/p_liabilities_TAI` | `809189b25808456f960b9c4f0d47fab6` |
| `p_mainfinance_TAI` | 台湾交易所主要财务指标 | `oversea/p_mainfinance_TAI` | `010ac1a5b1c4428fba18527e49e740ee` |
| `p_plateincome_TAI` | 台湾交易所板块收入情况表 | `oversea/p_plateincome_TAI` | `ece925d17d094e23b2f4dc260bbb6f3a` |
| `p_regionalincome_TAI` | 台湾交易所地域收入情况表 | `oversea/p_regionalincome_TAI` | `5ba9e51f09204839a330e8cc9ad54fc8` |
| `p_tranindex_TAI` | 台湾交易所最新交易指标表 | `oversea/p_tranindex_TAI` | `32b91bacafb84f22bf74fc216cade6cb` |

#### 台湾证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_TAI` | 台湾交易所行情数据 | `oversea/p_quotadata_TAI` | `66af6d46945e401ebdd34bc58530c9ff` |
| `p_stockexefactor_TAI` | 台湾交易所股票除权因子表 | `oversea/p_stockexefactor_TAI` | `0cede59dc56443b0a35c92bf654c4b60` |

### 新加坡证券交易所

#### 新加坡证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_SES` | 新加坡交易所上市公司中文简介 | `oversea/p_cnintroduce_SES` | `d9c36626a6384ed3af954ad7c68ebe46` |
| `p_executives_SES` | 新加坡交易所高管 | `oversea/p_executives_SES` | `91a77b706b76478892eb4fda5b9574df` |
| `p_info_SES` | 新加坡交易所公司基本情况 | `oversea/p_info_SES` | `60f0af3c1b7c46b992df4f5746be7544` |

#### 新加坡证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_SES` | 新加坡交易所派息 | `oversea/p_dividends_SES` | `33f47ab5ac254f3287753ddc7f76b450` |

#### 新加坡证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_SES` | 新加坡交易所并购 | `oversea/p_manda_SES` | `fa9c89d40f484d40addc2a19600fe527` |

#### 新加坡证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_SES` | 新加坡交易所股本变化表 | `oversea/p_cine_SES` | `247299a358d347e2939cea910d76410f` |
| `p_latestequity_SES` | 新加坡交易所最新股本表 | `oversea/p_latestequity_SES` | `84512c0f082e490096944f3598bdcfb1` |
| `p_shareholders_SES` | 新加坡交易所主要股东表 | `oversea/p_shareholders_SES` | `6b509e7e6ec84da491315619dfe8d8f3` |

#### 新加坡证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_SES` | 新加坡交易所通用现金流量表 | `oversea/p_cashflow_SES` | `187474216e684a9ab702de4f2e90931f` |
| `p_finanderive_SES` | 新加坡交易所财务衍生报表 | `oversea/p_finanderive_SES` | `dd4d9d4260824ae9b0b8290ac411657b` |
| `p_income_SES` | 新加坡交易所通用利润表 | `oversea/p_income_SES` | `c9b8e27de2634b0aa23cc72874732880` |
| `p_liabilities_SES` | 新加坡交易所通用资产负债表 | `oversea/p_liabilities_SES` | `3719c8b897154c0ca0ebcd9f7f182acc` |
| `p_mainfinance_SES` | 新加坡交易所主要财务指标 | `oversea/p_mainfinance_SES` | `a06caf8729794018a8ba7509c50118b8` |
| `p_plateincome_SES` | 新加坡交易所板块收入情况表 | `oversea/p_plateincome_SES` | `8b36339703894240bc2bc62a75431c4b` |
| `p_regionalincome_SES` | 新加坡交易所地域收入情况表 | `oversea/p_regionalincome_SES` | `640dbb1b83d34232861b12a6d7a85aa8` |
| `p_tranindex_SES` | 新加坡交易所最新交易指标表 | `oversea/p_tranindex_SES` | `a2ed10c351cb4ed89cab95d617fd7604` |

#### 新加坡证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_SES` | 新加坡交易所行情数据 | `oversea/p_quotadata_SES` | `8b1d21b342564e07939d006256b5afcc` |
| `p_stockexefactor_SES` | 新加坡交易所股票除权因子表 | `oversea/p_stockexefactor_SES` | `72910f294c644a81bd348ec673dab89d` |

### 莫斯科证券交易所

#### 莫斯科证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_RUS` | 莫斯科交易所上市公司中文简介 | `oversea/p_cnintroduce_RUS` | `7bbd7d9e0a7d45109a43940f287ee266` |
| `p_executives_RUS` | 莫斯科交易所高管 | `oversea/p_executives_RUS` | `9e1fd8b922dc40d28d0344ac7451a218` |
| `p_info_RUS` | 莫斯科交易所公司基本情况 | `oversea/p_info_RUS` | `e45f99b7e80e4c6b9a0b00dd157f29bf` |

#### 莫斯科证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_RUS` | 莫斯科交易所派息 | `oversea/p_dividends_RUS` | `9b42be57827048eab02deebe05acc915` |

#### 莫斯科证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_RUS` | 莫斯科交易所并购 | `oversea/p_manda_RUS` | `c82a559f66ff4795adef128c4fda0a19` |

#### 莫斯科证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_RUS` | 莫斯科交易所股本变化表 | `oversea/p_cine_RUS` | `2b5bc7fbb7304673bddd0521ab3d8be6` |
| `p_latestequity_RUS` | 莫斯科交易所最新股本表 | `oversea/p_latestequity_RUS` | `8116f172416848faacf2808d1a6f21db` |
| `p_shareholders_RUS` | 莫斯科交易所主要股东表 | `oversea/p_shareholders_RUS` | `03927c0c303a4280b78d3abf1560ac74` |

#### 莫斯科证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_RUS` | 莫斯科交易所通用现金流量表 | `oversea/p_cashflow_RUS` | `0e586704306e43758b0f3759f9b6af1b` |
| `p_finanderive_RUS` | 莫斯科交易所财务衍生报表 | `oversea/p_finanderive_RUS` | `95b243fcfb9a4860a3e72c95cb61cc92` |
| `p_income_RUS` | 莫斯科交易所通用利润表 | `oversea/p_income_RUS` | `ee759f4c0fc6443ba88f6ead5eb4acbd` |
| `p_liabilities_RUS` | 莫斯科交易所通用资产负债表 | `oversea/p_liabilities_RUS` | `5cd0defc849d47b785e9cf6b72fc17bb` |
| `p_mainfinance_RUS` | 莫斯科交易所主要财务指标 | `oversea/p_mainfinance_RUS` | `6bd17c85956344c6a1f6b7a7ab3f0738` |
| `p_plateincome_RUS` | 莫斯科交易所板块收入情况表 | `oversea/p_plateincome_RUS` | `c90dc21413704b06a75757bb4349746b` |
| `p_regionalincome_RUS` | 莫斯科交易所地域收入情况表 | `oversea/p_regionalincome_RUS` | `ef5160aa0f17419f94424a576c22b1aa` |
| `p_tranindex_RUS` | 莫斯科交易所最新交易指标表 | `oversea/p_tranindex_RUS` | `1059dfafb2d640ddbf14ac0d1aa29427` |

#### 莫斯科证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_RUS` | 莫斯科交易所行情数据 | `oversea/p_quotadata_RUS` | `50003c6ee77e436d94c5520fb9c5be67` |
| `p_stockexefactor_RUS` | 莫斯科交易所股票除权因子表 | `oversea/p_stockexefactor_RUS` | `a4501b90c8d045559f4a1517ee862996` |

### 米兰证券交易所

#### 米兰证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_MIL` | 米兰交易所上市公司中文简介 | `oversea/p_cnintroduce_MIL` | `3f752b190676404c9be4e5f1830595dc` |
| `p_executives_MIL` | 米兰交易所高管 | `oversea/p_executives_MIL` | `8950c2e1c5594e8790fed775792fd149` |
| `p_info_MIL` | 米兰交易所公司基本情况 | `oversea/p_info_MIL` | `87c95c2607a64a66b4f8aa1f9719590d` |

#### 米兰证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_MIL` | 米兰交易所派息 | `oversea/p_dividends_MIL` | `23d1c6d6eaae4eb5a6135ef3d2e8ab01` |

#### 米兰证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_MIL` | 米兰交易所并购 | `oversea/p_manda_MIL` | `6451a0bec1f74c3f9d4a677134ab0694` |

#### 米兰证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_MIL` | 米兰交易所股本变化表 | `oversea/p_cine_MIL` | `99aa8465ba264e1caad8a9401b9c5a13` |
| `p_latestequity_MIL` | 米兰交易所最新股本表 | `oversea/p_latestequity_MIL` | `0cadf53c99864b53b37da7b96142b01d` |
| `p_shareholders_MIL` | 米兰交易所主要股东表 | `oversea/p_shareholders_MIL` | `584632fd74eb4c8db2be293eb3f36416` |

#### 米兰证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_MIL` | 米兰交易所通用现金流量表 | `oversea/p_cashflow_MIL` | `0814191db8c0448d8228691ea03b5080` |
| `p_finanderive_MIL` | 米兰交易所财务衍生报表 | `oversea/p_finanderive_MIL` | `18aa4cb6dd444bb5a8f0379abf20197e` |
| `p_income_MIL` | 米兰交易所通用利润表 | `oversea/p_income_MIL` | `242e2af7248e4b228e02763d6c0579d5` |
| `p_liabilities_MIL` | 米兰交易所通用资产负债表 | `oversea/p_liabilities_MIL` | `e0162c30a4484eed9287ffc9096c2a71` |
| `p_mainfinance_MIL` | 米兰交易所主要财务指标 | `oversea/p_mainfinance_MIL` | `a33309a262ed49598d7f8a4fc748142e` |
| `p_plateincome_MIL` | 米兰交易所板块收入情况表 | `oversea/p_plateincome_MIL` | `a8b3290d53d34957829b0e7beeebeaa2` |
| `p_regionalincome_MIL` | 米兰交易所地域收入情况表 | `oversea/p_regionalincome_MIL` | `b2a98ddc79e34048ab0f46cfca1d6b10` |
| `p_tranindex_MIL` | 米兰交易所最新交易指标表 | `oversea/p_tranindex_MIL` | `aa16507eb7104d54a4278d1e7520b9a9` |

#### 米兰证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_MIL` | 米兰交易所行情数据 | `oversea/p_quotadata_MIL` | `739adbc89d5e42c487ecddc658f51cac` |
| `p_stockexefactor_MIL` | 米兰交易所股票除权因子表 | `oversea/p_stockexefactor_MIL` | `05da475a9320456cb7656091aeb61a29` |

### 泰国证券交易所

#### 泰国证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_BKK` | 泰国交易所上市公司中文简介 | `oversea/p_cnintroduce_BKK` | `4a0638a7127e4f58a6f404d56456be3f` |
| `p_executives_BKK` | 泰国交易所高管 | `oversea/p_executives_BKK` | `a4a41e62b28e4d20a190a0098cd5dc19` |
| `p_info_BKK` | 泰国交易所公司基本情况 | `oversea/p_info_BKK` | `9809afb065974b1eb7a507e8e06393bd` |

#### 泰国证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_BKK` | 泰国交易所派息 | `oversea/p_dividends_BKK` | `c28a434eae4a4dbaae7fd02b8d6032e5` |

#### 泰国证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_BKK` | 泰国交易所并购 | `oversea/p_manda_BKK` | `aba27c3b0d73463db405847af084dda4` |

#### 泰国证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_BKK` | 泰国交易所股本变化表 | `oversea/p_cine_BKK` | `d6b5bb1d900440bbba7f54a77821f560` |
| `p_latestequity_BKK` | 泰国交易所最新股本表 | `oversea/p_latestequity_BKK` | `4c61636e4b904e27ab92b1e8279691dc` |
| `p_shareholders_BKK` | 泰国交易所主要股东表 | `oversea/p_shareholders_BKK` | `9f3a4827ea1440e895b35a9a6634594e` |

#### 泰国证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_BKK` | 泰国交易所通用现金流量表 | `oversea/p_cashflow_BKK` | `9f85ec4d83c5469b8cff797d6f762694` |
| `p_finanderive_BKK` | 泰国交易所财务衍生报表 | `oversea/p_finanderive_BKK` | `5145902f3c18484a9345992c6a6f91f6` |
| `p_income_BKK` | 泰国交易所通用利润表 | `oversea/p_income_BKK` | `9dc765c70baf4161b3d046cfbdfb4d59` |
| `p_liabilities_BKK` | 泰国交易所通用资产负债表 | `oversea/p_liabilities_BKK` | `a8d3656f020e424383bd0fd2b92a97ce` |
| `p_mainfinance_BKK` | 泰国交易所主要财务指标 | `oversea/p_mainfinance_BKK` | `9d25f85eb232400aa2187b707f64de33` |
| `p_plateincome_BKK` | 泰国交易所板块收入情况表 | `oversea/p_plateincome_BKK` | `33939998c9f04735998e9bb0f56917f7` |
| `p_regionalincome_BKK` | 泰国交易所地域收入情况表 | `oversea/p_regionalincome_BKK` | `5bc3c645f21b4550bdcad299c3bbaac8` |
| `p_tranindex_BKK` | 泰国交易所最新交易指标表 | `oversea/p_tranindex_BKK` | `032a5bd1455a49f3ac6b5763ceccbf56` |

#### 泰国证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_BKK` | 泰国交易所行情数据 | `oversea/p_quotadata_BKK` | `a9ffbe5f91784f1ca7833df1952fabad` |
| `p_stockexefactor_BKK` | 泰国交易所股票除权因子表 | `oversea/p_stockexefactor_BKK` | `e65e2465cdb341dcb60d81fe5ac68548` |

### 华沙证券交易所

#### 华沙证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_WAR` | 华沙交易所上市公司中文简介 | `oversea/p_cnintroduce_WAR` | `6ea45a403a154f1dbc7fa25e85f44f4e` |
| `p_executives_WAR` | 华沙交易所高管 | `oversea/p_executives_WAR` | `73e083996ad74c718e7934d695363c32` |
| `p_info_WAR` | 华沙交易所公司基本情况 | `oversea/p_info_WAR` | `58cb67b86feb4587882a7e0cf3b961a5` |

#### 华沙证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_WAR` | 华沙交易所派息 | `oversea/p_dividends_WAR` | `b3e1748ab71b463aa81896a69d7d713d` |

#### 华沙证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_WAR` | 华沙交易所并购 | `oversea/p_manda_WAR` | `05f0e5aef0b949dbb7eabccd221b2c2e` |

#### 华沙证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_WAR` | 华沙交易所股本变化表 | `oversea/p_cine_WAR` | `d3422dfacb9545e689155f685a3148df` |
| `p_latestequity_WAR` | 华沙交易所最新股本表 | `oversea/p_latestequity_WAR` | `556bc116e0d94f608b1225e716f6c6be` |
| `p_shareholders_WAR` | 华沙交易所主要股东表 | `oversea/p_shareholders_WAR` | `9dc0ceeee5cd488ebe5ba3d45b2ed87d` |

#### 华沙证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_WAR` | 华沙交易所通用现金流量表 | `oversea/p_cashflow_WAR` | `6d4a6d0bf3fd4e0ca1dcbc239ba4ae2c` |
| `p_finanderive_WAR` | 华沙交易所财务衍生报表 | `oversea/p_finanderive_WAR` | `7e1dcc985fa044319f04268d3544ce82` |
| `p_income_WAR` | 华沙交易所通用利润表 | `oversea/p_income_WAR` | `a2ef8f7b500344919cd94339ab3ae563` |
| `p_liabilities_WAR` | 华沙交易所通用资产负债表 | `oversea/p_liabilities_WAR` | `dc114e56e7994bc58a372d42f4441781` |
| `p_mainfinance_WAR` | 华沙交易所主要财务指标 | `oversea/p_mainfinance_WAR` | `5abb527eb94142fea6999f14686e0ccd` |
| `p_plateincome_WAR` | 华沙交易所板块收入情况表 | `oversea/p_plateincome_WAR` | `ed94b9194e2a42e6b9a08d5fa5ecdc9f` |
| `p_regionalincome_WAR` | 华沙交易所地域收入情况表 | `oversea/p_regionalincome_WAR` | `e794376e3aa6408bac5f736bc4b777c0` |
| `p_tranindex_WAR` | 华沙交易所最新交易指标表 | `oversea/p_tranindex_WAR` | `c2890e4b24da48c8bc8d8ae4a5814abd` |

#### 华沙证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_WAR` | 华沙交易所行情数据 | `oversea/p_quotadata_WAR` | `a5983e2ba53e4f52a3e74886c21084df` |
| `p_stockexefactor_WAR` | 华沙交易所股票除权因子表 | `oversea/p_stockexefactor_WAR` | `6b86851d13ef4f10867c9acb08235cdf` |

### 斯德哥尔摩证券交易所

#### 斯德哥尔摩证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_OME` | 斯德哥尔摩上市公司中文简介 | `oversea/p_cnintroduce_OME` | `ea55eb52bb584be18c3867847592056e` |
| `p_executives_OME` | 斯德哥尔摩高管 | `oversea/p_executives_OME` | `0a40151e561d4d998a9b557e7518b996` |
| `p_info_OME` | 斯德哥尔摩公司基本情况 | `oversea/p_info_OME` | `7163462844a6446b8a6acf4060ce5422` |

#### 斯德哥尔摩证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_OME` | 斯德哥尔摩派息 | `oversea/p_dividends_OME` | `02f96c8d0ad94e7f9f5a2efc196b2acd` |

#### 斯德哥尔摩证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_OME` | 斯德哥尔摩并购 | `oversea/p_manda_OME` | `c39d58f449a74b18883798d234d84459` |

#### 斯德哥尔摩证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_OME` | 斯德哥尔摩股本变化表 | `oversea/p_cine_OME` | `fffbdbcd6bfa4eb5bc59542dc8b9d73d` |
| `p_latestequity_OME` | 斯德哥尔摩最新股本表 | `oversea/p_latestequity_OME` | `d9573d3c1d454d3ba510d51c13a201ba` |
| `p_shareholders_OME` | 斯德哥尔摩主要股东表 | `oversea/p_shareholders_OME` | `7a59b551faa2417db1f6c377855a163d` |

#### 斯德哥尔摩证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_OME` | 斯德哥尔摩通用现金流量表 | `oversea/p_cashflow_OME` | `79eef6bf0d6d4ad98072a167d85c2b2d` |
| `p_finanderive_OME` | 斯德哥尔摩财务衍生报表 | `oversea/p_finanderive_OME` | `08d17b3f146940c385fb4d71d4197b6f` |
| `p_income_OME` | 斯德哥尔摩通用利润表 | `oversea/p_income_OME` | `4184cc71404e418fbd7fd4c764fb858a` |
| `p_liabilities_OME` | 斯德哥尔摩通用资产负债表 | `oversea/p_liabilities_OME` | `00e3bdf0cb5e4d22a893c42fd36bd774` |
| `p_mainfinance_OME` | 斯德哥尔摩主要财务指标 | `oversea/p_mainfinance_OME` | `64f311954dd54173bc72cb3c9fc55c52` |
| `p_plateincome_OME` | 斯德哥尔摩板块收入情况表 | `oversea/p_plateincome_OME` | `2c7a74b5d62f4e7e9c1abd229535c282` |
| `p_regionalincome_OME` | 斯德哥尔摩地域收入情况表 | `oversea/p_regionalincome_OME` | `2ca6e614ef70416c80d524a073aa1c61` |
| `p_tranindex_OME` | 斯德哥尔摩最新交易指标表 | `oversea/p_tranindex_OME` | `23ff3a466e94480d9136dbe0bdb6851c` |

#### 斯德哥尔摩证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_OME` | 斯德哥尔摩行情数据 | `oversea/p_quotadata_OME` | `783f3db9229a4967aef6ad2c44d769a2` |
| `p_stockexefactor_OME` | 斯德哥尔摩股票除权因子表 | `oversea/p_stockexefactor_OME` | `57e168a31be34e46b864f68b0c720878` |

### 特拉维夫证券交易所

#### 特拉维夫证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_TAE` | 特拉维夫证交所上市公司中文简介 | `oversea/p_cnintroduce_TAE` | `60d32442d0d44857be80e62fb0740936` |
| `p_executives_TAE` | 特拉维夫证交所高管 | `oversea/p_executives_TAE` | `f29965d3b63a43ada2ab66f6887fde8f` |
| `p_info_TAE` | 特拉维夫证交所公司基本情况 | `oversea/p_info_TAE` | `315e38c45d184fe58e2f358d29659c4d` |

#### 特拉维夫证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_TAE` | 特拉维夫证交所派息 | `oversea/p_dividends_TAE` | `d5db2392798d4bc7b80c39e973f3381c` |

#### 特拉维夫证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_TAE` | 特拉维夫证交所并购 | `oversea/p_manda_TAE` | `ff700ecc10f140ac8a21437850a45a22` |

#### 特拉维夫证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_TAE` | 特拉维夫证交所股本变化表 | `oversea/p_cine_TAE` | `48c84320e4ae4833a6a4ebf3beb25341` |
| `p_latestequity_TAE` | 特拉维夫证交所最新股本表 | `oversea/p_latestequity_TAE` | `5adb16f1c37b4e8093459dd3c2fd9f88` |
| `p_shareholders_TAE` | 特拉维夫证交所主要股东表 | `oversea/p_shareholders_TAE` | `e48cee0c26de4b9280ec4dc81f580157` |

#### 特拉维夫证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_TAE` | 特拉维夫证交所通用现金流量表 | `oversea/p_cashflow_TAE` | `6c4487f4892545d0bc8e64234c97befe` |
| `p_finanderive_TAE` | 特拉维夫证交所财务衍生报表 | `oversea/p_finanderive_TAE` | `0678da4ce60b4d68b6fbdb227e385b85` |
| `p_income_TAE` | 特拉维夫证交所通用利润表 | `oversea/p_income_TAE` | `e3abf3cc516d42d680093cfa4165e504` |
| `p_liabilities_TAE` | 特拉维夫证交所通用资产负债表 | `oversea/p_liabilities_TAE` | `dbc1823c83c64ecbbd8f357e1ec1a024` |
| `p_mainfinance_TAE` | 特拉维夫证交所主要财务指标 | `oversea/p_mainfinance_TAE` | `00d14c2f1fdb42028d0faaf6736065a8` |
| `p_plateincome_TAE` | 特拉维夫证交所板块收入情况表 | `oversea/p_plateincome_TAE` | `3679a705b0cf4684a6ea394e213ba6cf` |
| `p_regionalincome_TAE` | 特拉维夫证交所地域收入情况表 | `oversea/p_regionalincome_TAE` | `85f4bd674ecc48b791b8b0ec40ef8154` |
| `p_tranindex_TAE` | 特拉维夫证交所最新交易指标表 | `oversea/p_tranindex_TAE` | `983f588cd4fe465f99d2af9bb9ba83f6` |

#### 特拉维夫证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_TAE` | 特拉维夫证交所行情数据 | `oversea/p_quotadata_TAE` | `735e21dc4ba041989680bffadd81375a` |
| `p_stockexefactor_TAE` | 特拉维夫证交所股票除权因子表 | `oversea/p_stockexefactor_TAE` | `5027b4cbebc941469300cc551a1a83c2` |

### 约翰内斯堡证券交易所

#### 约翰内斯堡证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_JSE` | 约翰内斯堡证券交易所上市公司中文简介 | `oversea/p_cnintroduce_JSE` | `c3b325ae64504a93bd8c4b0331124bc4` |
| `p_executives_JSE` | 约翰内斯堡证券交易所高管 | `oversea/p_executives_JSE` | `c1dc7bfb2d2245248729614a127cdc84` |
| `p_info_JSE` | 约翰内斯堡证券交易所公司基本情况 | `oversea/p_info_JSE` | `7794fd9544e345b7bdccb2b3a35c8f68` |

#### 约翰内斯堡证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_JSE` | 约翰内斯堡证券交易所派息 | `oversea/p_dividends_JSE` | `83db2526858a4846ac9c03464293a7d2` |

#### 约翰内斯堡证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_JSE` | 约翰内斯堡证券交易所并购 | `oversea/p_manda_JSE` | `45227369cf0746a6b326d6d59aa8f86c` |

#### 约翰内斯堡证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_JSE` | 约翰内斯堡证券交易所股本变化表 | `oversea/p_cine_JSE` | `a6c29f78835e42fd9a41479d233eefd6` |
| `p_latestequity_JSE` | 约翰内斯堡证券交易所最新股本表 | `oversea/p_latestequity_JSE` | `79f2d21724e043cda4ff0e62b6213444` |
| `p_shareholders_JSE` | 约翰内斯堡证券交易所主要股东表 | `oversea/p_shareholders_JSE` | `90b7432e35374fe28136043e8ad1ec22` |

#### 约翰内斯堡证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_JSE` | 约翰内斯堡证券交易所通用现金流量表 | `oversea/p_cashflow_JSE` | `74a580b2cf0647fc9417601a02a07914` |
| `p_finanderive_JSE` | 约翰内斯堡证券交易所财务衍生报表 | `oversea/p_finanderive_JSE` | `41820e1c1dd24431b1792446620437e8` |
| `p_income_JSE` | 约翰内斯堡证券交易所通用利润表 | `oversea/p_income_JSE` | `196763f882384068aa73c91207a7ea1f` |
| `p_liabilities_JSE` | 约翰内斯堡证券交易所通用资产负债表 | `oversea/p_liabilities_JSE` | `4e4fe093242c4ca88ab99a23be7a15dc` |
| `p_mainfinance_JSE` | 约翰内斯堡证券交易所主要财务指标 | `oversea/p_mainfinance_JSE` | `b25c3988439f4c279c1ce245cf674a8f` |
| `p_plateincome_JSE` | 约翰内斯堡证券交易所板块收入情况表 | `oversea/p_plateincome_JSE` | `b31df0bc92f74e10b5059b648b3cbbfe` |
| `p_regionalincome_JSE` | 约翰内斯堡证券交易所地域收入情况表 | `oversea/p_regionalincome_JSE` | `70b52118073c41c9bf84f589e244e150` |
| `p_tranindex_JSE` | 约翰内斯堡证券交易所最新交易指标表 | `oversea/p_tranindex_JSE` | `4f3ad45048f446169f2187b19285f365` |

#### 约翰内斯堡证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_JSE` | 约翰内斯堡证券交易所行情数据 | `oversea/p_quotadata_JSE` | `d43dab8fd1fc4076a7800390fd5ef601` |
| `p_stockexefactor_JSE` | 约翰内斯堡证券交易所股票除权因子表 | `oversea/p_stockexefactor_JSE` | `d19d43d9b9494083b7265de7051ae82a` |

### 印度尼西亚证券交易所

#### 印度尼西亚证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_JKT` | 印度尼西亚交易所上市公司中文简介 | `oversea/p_cnintroduce_JKT` | `d83642124854482ea84c3ce9f0fd0a9d` |
| `p_executives_JKT` | 印度尼西亚交易所高管 | `oversea/p_executives_JKT` | `539a1b590eb94a93b26b4350a8a07b79` |
| `p_info_JKT` | 印度尼西亚交易所公司基本情况 | `oversea/p_info_JKT` | `1288901c11d142d1bff88e0b7c8525ea` |

#### 印度尼西亚证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_JKT` | 印度尼西亚交易所派息 | `oversea/p_dividends_JKT` | `ba848be6ebf74c679bd2d91710f878ea` |

#### 印度尼西亚证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_JKT` | 印度尼西亚交易所并购 | `oversea/p_manda_JKT` | `6e79ec8661a345dc87911cfe1247fec8` |

#### 印度尼西亚证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_JKT` | 印度尼西亚交易所股本变化表 | `oversea/p_cine_JKT` | `0da8df628b77418cac71bca24b29ab66` |
| `p_latestequity_JKT` | 印度尼西亚交易所最新股本表 | `oversea/p_latestequity_JKT` | `d98f80c1f9a144e394af5180127d8704` |
| `p_shareholders_JKT` | 印度尼西亚交易所主要股东表 | `oversea/p_shareholders_JKT` | `cdb03012a3a84a839872019713a9ae7e` |

#### 印度尼西亚证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_JKT` | 印度尼西亚交易所通用现金流量表 | `oversea/p_cashflow_JKT` | `239a90b48ac847048640c15cea5e92a0` |
| `p_finanderive_JKT` | 印度尼西亚交易所财务衍生报表 | `oversea/p_finanderive_JKT` | `a0c49033912249c98d16609d213d9a4f` |
| `p_income_JKT` | 印度尼西亚交易所通用利润表 | `oversea/p_income_JKT` | `d6eb81632ddd45b2b1dfdbc7064302e7` |
| `p_liabilities_JKT` | 印度尼西亚交易所通用资产负债表 | `oversea/p_liabilities_JKT` | `05dfa6e227e249fca8d74c63d278dead` |
| `p_mainfinance_JKT` | 印度尼西亚交易所主要财务指标 | `oversea/p_mainfinance_JKT` | `1ceb6f18cc314d448bfdcbc409211c7b` |
| `p_plateincome_JKT` | 印度尼西亚交易所板块收入情况表 | `oversea/p_plateincome_JKT` | `127c00be453f4bb7b14888049ad90786` |
| `p_regionalincome_JKT` | 印度尼西亚交易所地域收入情况表 | `oversea/p_regionalincome_JKT` | `22d76de6f4a5407cb383153a8b00f92d` |
| `p_tranindex_JKT` | 印度尼西亚交易所最新交易指标表 | `oversea/p_tranindex_JKT` | `c7a349f65aaa425caa653e51f30aa876` |

#### 印度尼西亚证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_JKT` | 印度尼西亚交易所行情数据 | `oversea/p_quotadata_JKT` | `0c7c2ba85f6c4a728265c0b843bd9808` |
| `p_stockexefactor_JKT` | 印度尼西亚交易所股票除权因子表 | `oversea/p_stockexefactor_JKT` | `d83644b74b2c4f73a37ed2d7a4e7415b` |

### 巴基斯坦证券交易所

#### 巴基斯坦证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_KAR` | 巴基斯坦交易所上市公司中文简介 | `oversea/p_cnintroduce_KAR` | `f8a7d3b44ddc4d22ae0a49267f5672a3` |
| `p_executives_KAR` | 巴基斯坦交易所高管 | `oversea/p_executives_KAR` | `a7fd67a02d144422975599b9ef0ef52d` |
| `p_info_KAR` | 巴基斯坦交易所公司基本情况 | `oversea/p_info_KAR` | `f062b999389d47d188115cb8c2f0de0b` |

#### 巴基斯坦证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_KAR` | 巴基斯坦交易所派息 | `oversea/p_dividends_KAR` | `65ed7a37eea4428bb49fdbf6913c68a4` |

#### 巴基斯坦证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_KAR` | 巴基斯坦交易所并购 | `oversea/p_manda_KAR` | `849f9ff42ac446ce99f84140a4f31f75` |

#### 巴基斯坦证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_KAR` | 巴基斯坦交易所股本变化表 | `oversea/p_cine_KAR` | `13eaaf3bf0ca40a1b0fdc1cde304a50e` |
| `p_latestequity_KAR` | 巴基斯坦交易所最新股本表 | `oversea/p_latestequity_KAR` | `ffdb19f6b8d04819ac28fab9853c2667` |
| `p_shareholders_KAR` | 巴基斯坦交易所主要股东表 | `oversea/p_shareholders_KAR` | `7e4f64547dcc41debc191aedd7633a6c` |

#### 巴基斯坦证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_KAR` | 巴基斯坦交易所通用现金流量表 | `oversea/p_cashflow_KAR` | `337c74cf4bf94d569e1b1408af93029f` |
| `p_finanderive_KAR` | 巴基斯坦交易所财务衍生报表 | `oversea/p_finanderive_KAR` | `88e111e4fc0647a483bf74453bb1650e` |
| `p_income_KAR` | 巴基斯坦交易所通用利润表 | `oversea/p_income_KAR` | `6bf2e6f2d45843b2b870caa71382f46c` |
| `p_liabilities_KAR` | 巴基斯坦交易所通用资产负债表 | `oversea/p_liabilities_KAR` | `27580ac6e2cb429bbf81e2d11294fa49` |
| `p_mainfinance_KAR` | 巴基斯坦交易所主要财务指标 | `oversea/p_mainfinance_KAR` | `4ee15e65009149cba7aae0b9fab75423` |
| `p_plateincome_KAR` | 巴基斯坦交易所板块收入情况表 | `oversea/p_plateincome_KAR` | `130fe241c0a24c518fa8849fbfa7a396` |
| `p_regionalincome_KAR` | 巴基斯坦交易所地域收入情况表 | `oversea/p_regionalincome_KAR` | `3c00e1251e224d5ba3f1c6e848660042` |
| `p_tranindex_KAR` | 巴基斯坦交易所最新交易指标表 | `oversea/p_tranindex_KAR` | `7ea4aa9d721c4173be0785c89f5cf2c5` |

#### 巴基斯坦证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_KAR` | 巴基斯坦交易所行情数据 | `oversea/p_quotadata_KAR` | `8fcf635f74da4fd9b6dc11d131ddca5f` |
| `p_stockexefactor_KAR` | 巴基斯坦交易所股票除权因子表 | `oversea/p_stockexefactor_KAR` | `7857c419a6cf42788702d8ebdfed55ec` |

### 圣保罗证券交易所

#### 圣保罗证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_BSP` | 圣保罗交易所上市公司中文简介 | `oversea/p_cnintroduce_BSP` | `a320ec1458184735b6e8f9007eb44efe` |
| `p_executives_BSP` | 圣保罗交易所高管 | `oversea/p_executives_BSP` | `ebbb956a04144fc1b8a1c57194a6698d` |
| `p_info_BSP` | 圣保罗交易所公司基本情况 | `oversea/p_info_BSP` | `b1838148b99b4e5c84e06c71be5e5cee` |

#### 圣保罗证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_BSP` | 圣保罗交易所派息 | `oversea/p_dividends_BSP` | `d106fe6bda244a0c8d732a87e561d4cc` |

#### 圣保罗证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_BSP` | 圣保罗交易所并购 | `oversea/p_manda_BSP` | `12ef50fcbad9482c843de59d260160ab` |

#### 圣保罗证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_BSP` | 圣保罗交易所股本变化表 | `oversea/p_cine_BSP` | `471524524d714e17a4363318b8fd30a5` |
| `p_latestequity_BSP` | 圣保罗交易所最新股本表 | `oversea/p_latestequity_BSP` | `1c4749b55a944246b033aeb48090097d` |
| `p_shareholders_BSP` | 圣保罗交易所主要股东表 | `oversea/p_shareholders_BSP` | `ad8f01a8f6674742a26866433bcd02e9` |

#### 圣保罗证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_BSP` | 圣保罗交易所通用现金流量表 | `oversea/p_cashflow_BSP` | `f5a01425f7624c4eb002494032fb7ded` |
| `p_finanderive_BSP` | 圣保罗交易所财务衍生报表 | `oversea/p_finanderive_BSP` | `2abf4415037643a79d12eb1e2d1d03f4` |
| `p_income_BSP` | 圣保罗交易所通用利润表 | `oversea/p_income_BSP` | `255d8ef03a714cc0adca0a9af3bebde8` |
| `p_liabilities_BSP` | 圣保罗交易所通用资产负债表 | `oversea/p_liabilities_BSP` | `10c51e7e441141ff9b4bf0e986d34e9c` |
| `p_mainfinance_BSP` | 圣保罗交易所主要财务指标 | `oversea/p_mainfinance_BSP` | `e4720cd2d89a4c048282f8ef3592658e` |
| `p_plateincome_BSP` | 圣保罗交易所板块收入情况表 | `oversea/p_plateincome_BSP` | `418ae12d403640d4aa73a094ffe08b0d` |
| `p_regionalincome_BSP` | 圣保罗交易所地域收入情况表 | `oversea/p_regionalincome_BSP` | `4071771f4127455887f5c682931540c1` |
| `p_tranindex_BSP` | 圣保罗交易所最新交易指标表 | `oversea/p_tranindex_BSP` | `05e3d248346a49aebd97ba7d079103aa` |

#### 圣保罗证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_BSP` | 圣保罗交易所行情数据 | `oversea/p_quotadata_BSP` | `82d2305010a84f7f9eb384903b14c3a7` |
| `p_stockexefactor_BSP` | 圣保罗交易所股票除权因子表 | `oversea/p_stockexefactor_BSP` | `4d46ce706b9d4c76b51b8ccd812426ba` |

### 伊斯坦布尔证券交易所

#### 伊斯坦布尔证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_IST` | 伊斯坦布尔交易所上市公司中文简介 | `oversea/p_cnintroduce_IST` | `2816f631bc314aeaa4d0bca3d66efa4e` |
| `p_executives_IST` | 伊斯坦布尔交易所高管 | `oversea/p_executives_IST` | `3130c5aaa101477c8cca38f5d0e3910a` |
| `p_info_IST` | 伊斯坦布尔交易所公司基本情况 | `oversea/p_info_IST` | `e2971bf18b804fe9a74dc7f0eab15be7` |

#### 伊斯坦布尔证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_IST` | 伊斯坦布尔交易所派息 | `oversea/p_dividends_IST` | `7a241bc283c642db8ca04f0f021cc729` |

#### 伊斯坦布尔证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_IST` | 伊斯坦布尔交易所并购 | `oversea/p_manda_IST` | `762ab4547a31458180c2b08bc702399e` |

#### 伊斯坦布尔证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_IST` | 伊斯坦布尔交易所股本变化表 | `oversea/p_cine_IST` | `dfb95b3e20a24af5afa468c622065af2` |
| `p_latestequity_IST` | 伊斯坦布尔交易所最新股本表 | `oversea/p_latestequity_IST` | `c1790179f58f458fbb736390e5f25bd3` |
| `p_shareholders_IST` | 伊斯坦布尔交易所主要股东表 | `oversea/p_shareholders_IST` | `4728a28d7a454802a158b0ff3c1994a4` |

#### 伊斯坦布尔证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_IST` | 伊斯坦布尔交易所通用现金流量表 | `oversea/p_cashflow_IST` | `697830b3ceca412fa3c1a39530575ef6` |
| `p_finanderive_IST` | 伊斯坦布尔交易所财务衍生报表 | `oversea/p_finanderive_IST` | `a2ba92a3b4ef408cb83371fb13c91487` |
| `p_income_IST` | 伊斯坦布尔交易所通用利润表 | `oversea/p_income_IST` | `f361e0480a3c4ac3a48ddecba1cb2a07` |
| `p_liabilities_IST` | 伊斯坦布尔交易所通用资产负债表 | `oversea/p_liabilities_IST` | `2bda2999659c4943a14094e31c3512ab` |
| `p_mainfinance_IST` | 伊斯坦布尔交易所主要财务指标 | `oversea/p_mainfinance_IST` | `0efa9b5f2e0641feb30fd4bbc3c494b3` |
| `p_plateincome_IST` | 伊斯坦布尔交易所板块收入情况表 | `oversea/p_plateincome_IST` | `8673b736fb6f40bfad8b3908337f06e5` |
| `p_regionalincome_IST` | 伊斯坦布尔交易所地域收入情况表 | `oversea/p_regionalincome_IST` | `3bc52ade679043e8bf2816d94cb93232` |
| `p_tranindex_IST` | 伊斯坦布尔交易所最新交易指标表 | `oversea/p_tranindex_IST` | `e81a2b366e404c04a5a30cdf3add9510` |

#### 伊斯坦布尔证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_IST` | 伊斯坦布尔交易所行情数据 | `oversea/p_quotadata_IST` | `7bd183bc198e407d9eee9dfb62095d52` |
| `p_stockexefactor_IST` | 伊斯坦布尔交易所股票除权因子表 | `oversea/p_stockexefactor_IST` | `858560efbb2f4b2db283698e26b4377d` |

### 河内证券交易所

#### 河内证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_HSTC` | 河内交易所上市公司中文简介 | `oversea/p_cnintroduce_HSTC` | `4ebe09b226c4481fb9a1df1f9d0368ab` |
| `p_executives_HSTC` | 河内交易所高管 | `oversea/p_executives_HSTC` | `444ccc84c160454d81383d2b8cc5ed16` |
| `p_info_HSTC` | 河内交易所公司基本情况 | `oversea/p_info_HSTC` | `568311301ec249c68eb40790bbf578e3` |

#### 河内证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_HSTC` | 河内交易所派息 | `oversea/p_dividends_HSTC` | `f61ae24db9e441e18503a5c8769339c0` |

#### 河内证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_HSTC` | 河内交易所并购 | `oversea/p_manda_HSTC` | `8dc235aaeddb4de096b1e05a50333804` |

#### 河内证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_HSTC` | 河内交易所股本变化表 | `oversea/p_cine_HSTC` | `4162de99dce344ba94219d03c4e3a260` |
| `p_latestequity_HSTC` | 河内交易所最新股本表 | `oversea/p_latestequity_HSTC` | `8ff9c477cdc54bdca3d42a7811ed99c6` |
| `p_shareholders_HSTC` | 河内交易所主要股东表 | `oversea/p_shareholders_HSTC` | `b865ac9637cd459a8d76ab502e51a607` |

#### 河内证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_HSTC` | 河内交易所通用现金流量表 | `oversea/p_cashflow_HSTC` | `e91950ddbd1d4a6b9cd0d1b9fad56360` |
| `p_finanderive_HSTC` | 河内交易所财务衍生报表 | `oversea/p_finanderive_HSTC` | `e64f52c9bdf94de18bbc41fb38d1f7da` |
| `p_income_HSTC` | 河内交易所通用利润表 | `oversea/p_income_HSTC` | `408a81c35b04443fb556c6de22cc4084` |
| `p_liabilities_HSTC` | 河内交易所通用资产负债表 | `oversea/p_liabilities_HSTC` | `14cdd8758ad040b88b7e090fa12ffaae` |
| `p_mainfinance_HSTC` | 河内交易所主要财务指标 | `oversea/p_mainfinance_HSTC` | `d560077de6294a08acf508f5f3d7f925` |
| `p_plateincome_HSTC` | 河内交易所板块收入情况表 | `oversea/p_plateincome_HSTC` | `daf685f4b99c4275bc73d49cc6dd270b` |
| `p_regionalincome_HSTC` | 河内交易所地域收入情况表 | `oversea/p_regionalincome_HSTC` | `305998f682dd4936b83d49865447bf41` |
| `p_tranindex_HSTC` | 河内交易所最新交易指标表 | `oversea/p_tranindex_HSTC` | `552a661eaac04354a475d14da0703d6c` |

#### 河内证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_HSTC` | 河内交易所行情数据 | `oversea/p_quotadata_HSTC` | `e449621cc27247af98ff990e8af1ba6f` |
| `p_stockexefactor_HSTC` | 河内交易所股票除权因子表 | `oversea/p_stockexefactor_HSTC` | `b2512b485d0142a0a8f97de435052575` |

### 瑞士证券交易所

#### 瑞士证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_SWX` | 瑞士交易所上市公司中文简介 | `oversea/p_cnintroduce_SWX` | `efa6ea06a76e4e5a91b1528e06d44073` |
| `p_executives_SWX` | 瑞士交易所高管 | `oversea/p_executives_SWX` | `83abc50aebb6494ca0fdbad9534757f6` |
| `p_info_SWX` | 瑞士交易所公司基本情况 | `oversea/p_info_SWX` | `ac9e122647924907a0498bf972ad4776` |

#### 瑞士证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_SWX` | 瑞士交易所派息 | `oversea/p_dividends_SWX` | `e574c8f1aa63414299bc3e8895cba231` |

#### 瑞士证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_SWX` | 瑞士交易所并购 | `oversea/p_manda_SWX` | `46ddb431e4f34df9b309128939e9a57e` |

#### 瑞士证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_SWX` | 瑞士交易所股本变化表 | `oversea/p_cine_SWX` | `7ad15a700eaa40fe888aa857a8160251` |
| `p_latestequity_SWX` | 瑞士交易所最新股本表 | `oversea/p_latestequity_SWX` | `9fa84956e33946b1b852c1a85af82e1f` |
| `p_shareholders_SWX` | 瑞士交易所主要股东表 | `oversea/p_shareholders_SWX` | `9b5cd599bf144ade979589640a58685f` |

#### 瑞士证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_SWX` | 瑞士交易所通用现金流量表 | `oversea/p_cashflow_SWX` | `49cfa6e5546840b683a7d76b4b3b9941` |
| `p_finanderive_SWX` | 瑞士交易所财务衍生报表 | `oversea/p_finanderive_SWX` | `ab4ad021124f463f95b5523f8a295c69` |
| `p_income_SWX` | 瑞士交易所通用利润表 | `oversea/p_income_SWX` | `f43f39526a554e0f8a3da1b85471ff01` |
| `p_liabilities_SWX` | 瑞士交易所通用资产负债表 | `oversea/p_liabilities_SWX` | `86b6cee70f034f418591967f41a7eef4` |
| `p_mainfinance_SWX` | 瑞士交易所主要财务指标 | `oversea/p_mainfinance_SWX` | `2420e2534fe343a1a36524c8df5e8d02` |
| `p_plateincome_SWX` | 瑞士交易所板块收入情况表 | `oversea/p_plateincome_SWX` | `9966e4cee60442ffbefbd6a8890ab9c9` |
| `p_regionalincome_SWX` | 瑞士交易所地域收入情况表 | `oversea/p_regionalincome_SWX` | `67f80f8b29814b18a74a7fdb4a6e1d27` |
| `p_tranindex_SWX` | 瑞士交易所最新交易指标表 | `oversea/p_tranindex_SWX` | `67621eea84f14e9c9ed43310e1349061` |

#### 瑞士证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_SWX` | 瑞士交易所行情数据 | `oversea/p_quotadata_SWX` | `0d92c63bf9ce4a1a8cb9d0cfdfe371da` |
| `p_stockexefactor_SWX` | 瑞士交易所股票除权因子表 | `oversea/p_stockexefactor_SWX` | `953c02475e7f43cd863c9e965e1a69c0` |

### 越南证券交易所

#### 越南证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_STC` | 越南交易所上市公司中文简介 | `oversea/p_cnintroduce_STC` | `112a7f7a3e414c89be6486234c75c879` |
| `p_executives_STC` | 越南交易所高管 | `oversea/p_executives_STC` | `2f4006b471f3433db65446451d2ab65c` |
| `p_info_STC` | 越南交易所公司基本情况 | `oversea/p_info_STC` | `fdf78ae2f5ff4440981c8827c1f34bdc` |

#### 越南证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_STC` | 越南交易所派息 | `oversea/p_dividends_STC` | `e35d3775fd794942bdfb6772149129eb` |

#### 越南证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_STC` | 越南交易所并购 | `oversea/p_manda_STC` | `03d50cfb5f424154ad82a994463b7988` |

#### 越南证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_STC` | 越南交易所股本变化表 | `oversea/p_cine_STC` | `75958dff43ca4b6b92fecea4e1d265d0` |
| `p_latestequity_STC` | 越南交易所最新股本表 | `oversea/p_latestequity_STC` | `594d8cc1257a4f89bd19731955b6d976` |
| `p_shareholders_STC` | 越南交易所主要股东表 | `oversea/p_shareholders_STC` | `03041b5d57ce426d83339efefc1eeaf6` |

#### 越南证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_STC` | 越南交易所通用现金流量表 | `oversea/p_cashflow_STC` | `a452b3b5236b4082921de2eb8a855e73` |
| `p_finanderive_STC` | 越南交易所财务衍生报表 | `oversea/p_finanderive_STC` | `4cdd5e387cb24bd2b92163afc1789d7d` |
| `p_income_STC` | 越南交易所通用利润表 | `oversea/p_income_STC` | `0997d17d47384c90afa9c432778e5a64` |
| `p_liabilities_STC` | 越南交易所通用资产负债表 | `oversea/p_liabilities_STC` | `f90d5f39e6254385b7aede830fe3ebbe` |
| `p_mainfinance_STC` | 越南交易所主要财务指标 | `oversea/p_mainfinance_STC` | `0002cfb121fe4c0c8ad6243890e47d52` |
| `p_plateincome_STC` | 越南交易所板块收入情况表 | `oversea/p_plateincome_STC` | `b88715f08b3a41bb96d58d4211f124c4` |
| `p_regionalincome_STC` | 越南交易所地域收入情况表 | `oversea/p_regionalincome_STC` | `1e17e9dbb35d4610b4c73fa00c0f4ee9` |
| `p_tranindex_STC` | 越南交易所最新交易指标表 | `oversea/p_tranindex_STC` | `6ba6b881a47d4dba9bdbbe9264bc7c8a` |

#### 越南证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_STC` | 越南交易所行情数据 | `oversea/p_quotadata_STC` | `b9de235d736b4b598e91da093aa2dcf3` |
| `p_stockexefactor_STC` | 越南交易所股票除权因子表 | `oversea/p_stockexefactor_STC` | `4ac6227e8c0848c8add55f57a1804d06` |

### 墨西哥证券交易所

#### 墨西哥证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_MEX` | 墨西哥交易所上市公司中文简介 | `oversea/p_cnintroduce_MEX` | `312cc121565c4bccb4eb96ad7be635a0` |
| `p_executives_MEX` | 墨西哥交易所高管 | `oversea/p_executives_MEX` | `9f6109fd940a4cfc984ddee2db5a6608` |
| `p_info_MEX` | 墨西哥交易所公司基本情况 | `oversea/p_info_MEX` | `e0f731e1782d4b0f838dacfc9284b781` |

#### 墨西哥证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_MEX` | 墨西哥交易所派息 | `oversea/p_dividends_MEX` | `4db50399d6bf420c87c0c54a8a6fe370` |

#### 墨西哥证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_MEX` | 墨西哥交易所并购 | `oversea/p_manda_MEX` | `b46350e4c9674d939d98a11d825f902a` |

#### 墨西哥证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_MEX` | 墨西哥交易所股本变化表 | `oversea/p_cine_MEX` | `f41aee2c863546afbc35154b8e139955` |
| `p_latestequity_MEX` | 墨西哥交易所最新股本表 | `oversea/p_latestequity_MEX` | `144558bc641f437e8354e04410f9c175` |
| `p_shareholders_MEX` | 墨西哥交易所主要股东表 | `oversea/p_shareholders_MEX` | `a60815a2229c487683ab062f55488a9e` |

#### 墨西哥证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_MEX` | 墨西哥交易所通用现金流量表 | `oversea/p_cashflow_MEX` | `78ed4812611b47ae91247e0d3e08e905` |
| `p_finanderive_MEX` | 墨西哥交易所财务衍生报表 | `oversea/p_finanderive_MEX` | `35a5709459544c73a786183c01372100` |
| `p_income_MEX` | 墨西哥交易所通用利润表 | `oversea/p_income_MEX` | `63671c0717fe49e0a868efcbcfc477f3` |
| `p_liabilities_MEX` | 墨西哥交易所通用资产负债表 | `oversea/p_liabilities_MEX` | `6a0030294f1149a9b3bbc0d34325d25f` |
| `p_mainfinance_MEX` | 墨西哥交易所主要财务指标 | `oversea/p_mainfinance_MEX` | `82f4cc4e50cc4cad9590fd6fecbcdd88` |
| `p_plateincome_MEX` | 墨西哥交易所板块收入情况表 | `oversea/p_plateincome_MEX` | `afea73c03e3b46859f6d88eaa8186d1f` |
| `p_regionalincome_MEX` | 墨西哥交易所地域收入情况表 | `oversea/p_regionalincome_MEX` | `fc6216f7b85d47b6af53da3dd3383d40` |
| `p_tranindex_MEX` | 墨西哥交易所最新交易指标表 | `oversea/p_tranindex_MEX` | `111cbe8720ee4d6fb5fec1a226c1b02f` |

#### 墨西哥证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_MEX` | 墨西哥交易所行情数据 | `oversea/p_quotadata_MEX` | `e071d44cdc834874be577497955cac7f` |
| `p_stockexefactor_MEX` | 墨西哥交易所股票除权因子表 | `oversea/p_stockexefactor_MEX` | `93f334cd32ae49a9ab4379ad2118094c` |

### 雅典证券交易所

#### 雅典证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_ATH` | 雅典交易所上市公司中文简介 | `oversea/p_cnintroduce_ATH` | `66b6318e72c64ee88c74657d3ca57999` |
| `p_executives_ATH` | 雅典交易所高管 | `oversea/p_executives_ATH` | `119ca72a078c4281b8729d96508030f1` |
| `p_info_ATH` | 雅典交易所公司基本情况 | `oversea/p_info_ATH` | `261a753b632147159eddfa3ead9b5340` |

#### 雅典证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_ATH` | 雅典交易所派息 | `oversea/p_dividends_ATH` | `caaf7957628e4268b78f4ffb0cf85dfa` |

#### 雅典证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_ATH` | 雅典交易所并购 | `oversea/p_manda_ATH` | `8e745173f93a44d48b942736fb1a76fc` |

#### 雅典证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_ATH` | 雅典交易所股本变化表 | `oversea/p_cine_ATH` | `a8152e53c13e46709925bffa1c8d8438` |
| `p_latestequity_ATH` | 雅典交易所最新股本表 | `oversea/p_latestequity_ATH` | `c42c002f035f4a3da9538360c5565972` |
| `p_shareholders_ATH` | 雅典交易所主要股东表 | `oversea/p_shareholders_ATH` | `356d8b7a29274542b0238998ba79b0f4` |

#### 雅典证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_ATH` | 雅典交易所通用现金流量表 | `oversea/p_cashflow_ATH` | `62d497b085a54f689522a0dbb4282234` |
| `p_finanderive_ATH` | 雅典交易所财务衍生报表 | `oversea/p_finanderive_ATH` | `52c989285d844d9c96ca77b809b8aba5` |
| `p_income_ATH` | 雅典交易所通用利润表 | `oversea/p_income_ATH` | `c810182572974464b0ef2bd1bddb281d` |
| `p_liabilities_ATH` | 雅典交易所通用资产负债表 | `oversea/p_liabilities_ATH` | `8bba995389a74faaaaf242f8a39c9c4a` |
| `p_mainfinance_ATH` | 雅典交易所主要财务指标 | `oversea/p_mainfinance_ATH` | `d7dc2a6bd23347bc8c1027c3b18c07b1` |
| `p_plateincome_ATH` | 雅典交易所板块收入情况表 | `oversea/p_plateincome_ATH` | `7af842d66a624f469c8c770d037ddf59` |
| `p_regionalincome_ATH` | 雅典交易所地域收入情况表 | `oversea/p_regionalincome_ATH` | `73205d09c00b4755bbb6a2651ad9911f` |
| `p_tranindex_ATH` | 雅典交易所最新交易指标表 | `oversea/p_tranindex_ATH` | `0f62247c14ea4c618bd2cf28ff81011b` |

#### 雅典证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_ATH` | 雅典交易所行情数据 | `oversea/p_quotadata_ATH` | `676a7108921a46de99b8e8769fa5c061` |
| `p_stockexefactor_ATH` | 雅典交易所股票除权因子表 | `oversea/p_stockexefactor_ATH` | `6fd766df696642f4bf692be4d754adb6` |

### 菲律宾证券交易所

#### 菲律宾证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_PHS` | 菲律宾交易所上市公司中文简介 | `oversea/p_cnintroduce_PHS` | `584115b2f4e04853872c62382604462b` |
| `p_executives_PHS` | 菲律宾交易所高管 | `oversea/p_executives_PHS` | `b7b473b13d904dcdabaf44408546d1c9` |
| `p_info_PHS` | 菲律宾交易所公司基本情况 | `oversea/p_info_PHS` | `56aa3c045ce747a9b3f5ea0d247c50d2` |

#### 菲律宾证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_PHS` | 菲律宾交易所派息 | `oversea/p_dividends_PHS` | `501985a3342944b3942677e47c999789` |

#### 菲律宾证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_PHS` | 菲律宾交易所并购 | `oversea/p_manda_PHS` | `e3103cfabc544dcbbe0c0f6a5fe55f47` |

#### 菲律宾证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_PHS` | 菲律宾交易所股本变化表 | `oversea/p_cine_PHS` | `69fc260b0b8e4a9cb9d3a51c8076ce99` |
| `p_latestequity_PHS` | 菲律宾交易所最新股本表 | `oversea/p_latestequity_PHS` | `0674b215e0ab4bef81511844c23f0d07` |
| `p_shareholders_PHS` | 菲律宾交易所主要股东表 | `oversea/p_shareholders_PHS` | `83f005c831784e9a8ecfd91ba0bac00d` |

#### 菲律宾证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_PHS` | 菲律宾交易所通用现金流量表 | `oversea/p_cashflow_PHS` | `453dc9e0bef04249adb1ac34c83c8bdb` |
| `p_finanderive_PHS` | 菲律宾交易所财务衍生报表 | `oversea/p_finanderive_PHS` | `960a3499d3f244498b8692c852f24675` |
| `p_income_PHS` | 菲律宾交易所通用利润表 | `oversea/p_income_PHS` | `6b6df9b8beea4a25a9a6b4884ad65958` |
| `p_liabilities_PHS` | 菲律宾交易所通用资产负债表 | `oversea/p_liabilities_PHS` | `9f77454a10ae4a8796e9707a5db7371e` |
| `p_mainfinance_PHS` | 菲律宾交易所主要财务指标 | `oversea/p_mainfinance_PHS` | `7539d9df071542ec93959ecd8b50809f` |
| `p_plateincome_PHS` | 菲律宾交易所板块收入情况表 | `oversea/p_plateincome_PHS` | `9902d40bfc714a298229965aca3aa703` |
| `p_regionalincome_PHS` | 菲律宾交易所地域收入情况表 | `oversea/p_regionalincome_PHS` | `9da02a4376554620b79b8bf2f3e524d0` |
| `p_tranindex_PHS` | 菲律宾交易所最新交易指标表 | `oversea/p_tranindex_PHS` | `6c3bb6f1d2634dc4822922e3ec77de04` |

#### 菲律宾证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_PHS` | 菲律宾交易所行情数据 | `oversea/p_quotadata_PHS` | `816ab87df73a49c89084682c658d5984` |
| `p_stockexefactor_PHS` | 菲律宾交易所股票除权因子表 | `oversea/p_stockexefactor_PHS` | `382bf3d4b3804e84a686f8cfdc9c07b6` |

### 达卡证券交易所

#### 达卡证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_DHA` | 达卡交易所上市公司中文简介 | `oversea/p_cnintroduce_DHA` | `ca4e723bffe14326a4052e85d514909a` |
| `p_executives_DHA` | 达卡交易所高管 | `oversea/p_executives_DHA` | `7a362f6ee3754763bca68b9ab5e242c9` |
| `p_info_DHA` | 达卡交易所公司基本情况 | `oversea/p_info_DHA` | `e8c75701078546e7addb260454137cf3` |

#### 达卡证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_DHA` | 达卡交易所派息 | `oversea/p_dividends_DHA` | `11312f69ad334c36ab0e1bbd2f9e94d7` |

#### 达卡证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_DHA` | 达卡交易所并购 | `oversea/p_manda_DHA` | `adc514127f924906ae3a92f0d056742d` |

#### 达卡证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_DHA` | 达卡交易所股本变化表 | `oversea/p_cine_DHA` | `a7102a18233c4bb4b83ceb187309d3bb` |
| `p_latestequity_DHA` | 达卡交易所最新股本表 | `oversea/p_latestequity_DHA` | `575cd3d397bf46debfe32cb137986391` |
| `p_shareholders_DHA` | 达卡交易所主要股东表 | `oversea/p_shareholders_DHA` | `9ba7c528e3fb44699399be79d6f44ea1` |

#### 达卡证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_DHA` | 达卡交易所通用现金流量表 | `oversea/p_cashflow_DHA` | `784e3db5ccf142588750576d530e33cb` |
| `p_finanderive_DHA` | 达卡交易所财务衍生报表 | `oversea/p_finanderive_DHA` | `6171e1523b5b4e49a5cc68b146c62760` |
| `p_income_DHA` | 达卡交易所通用利润表 | `oversea/p_income_DHA` | `92e90b629f5a479bb5ed318fd3c0fcda` |
| `p_liabilities_DHA` | 达卡交易所通用资产负债表 | `oversea/p_liabilities_DHA` | `27ad16b8b9584a44afef1d6609d75a95` |
| `p_mainfinance_DHA` | 达卡交易所主要财务指标 | `oversea/p_mainfinance_DHA` | `c8ff9098ad044622a63abd10bd2897ec` |
| `p_plateincome_DHA` | 达卡交易所板块收入情况表 | `oversea/p_plateincome_DHA` | `db4e20802b734451b6fe2969e8c2c260` |
| `p_regionalincome_DHA` | 达卡交易所地域收入情况表 | `oversea/p_regionalincome_DHA` | `01282e47f4534f3eb48f7c3762129e8f` |
| `p_tranindex_DHA` | 达卡交易所最新交易指标表 | `oversea/p_tranindex_DHA` | `eb09a564c9304a52ba9488e06dd2104a` |

#### 达卡证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_DHA` | 达卡交易所行情数据 | `oversea/p_quotadata_DHA` | `793a099761564191be2ad71f659c0ed8` |
| `p_stockexefactor_DHA` | 达卡交易所股票除权因子表 | `oversea/p_stockexefactor_DHA` | `cc22a00c22d949e9abb6209f39e6b991` |

### 埃及证券交易所

#### 埃及证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_CAI` | 埃及交易所上市公司中文简介 | `oversea/p_cnintroduce_CAI` | `2dc504472bdb46e5ae34e26d691190b6` |
| `p_executives_CAI` | 埃及交易所高管 | `oversea/p_executives_CAI` | `9d4a61eeb3864330a22637414ed54a46` |
| `p_info_CAI` | 埃及交易所公司基本情况 | `oversea/p_info_CAI` | `9ca0d920d9fb4a5aad57fd90faf0e7fa` |

#### 埃及证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_CAI` | 埃及交易所派息 | `oversea/p_dividends_CAI` | `7fb97c64796249d6b3454e8ee0da2984` |

#### 埃及证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_CAI` | 埃及交易所并购 | `oversea/p_manda_CAI` | `72afcb32f6d94ec1801228f760b5adf1` |

#### 埃及证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_CAI` | 埃及交易所股本变化表 | `oversea/p_cine_CAI` | `b6ba532942904b5cbb6528413a120a44` |
| `p_latestequity_CAI` | 埃及交易所最新股本表 | `oversea/p_latestequity_CAI` | `72825cc73ba6446bad46192ba785508a` |
| `p_shareholders_CAI` | 埃及交易所主要股东表 | `oversea/p_shareholders_CAI` | `387fafe8514b4d6f905b2ad13a158600` |

#### 埃及证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_CAI` | 埃及交易所通用现金流量表 | `oversea/p_cashflow_CAI` | `cec88edec59e41cfbd68eaed1b0968c5` |
| `p_finanderive_CAI` | 埃及交易所财务衍生报表 | `oversea/p_finanderive_CAI` | `de0fba9e60534048b8c1c5a5090fee69` |
| `p_income_CAI` | 埃及交易所通用利润表 | `oversea/p_income_CAI` | `c5f0245aaac342f7a54c4cd90db58d91` |
| `p_liabilities_CAI` | 埃及交易所通用资产负债表 | `oversea/p_liabilities_CAI` | `69d0175f98df4cdea98cd0c4cf30a9cc` |
| `p_mainfinance_CAI` | 埃及交易所主要财务指标 | `oversea/p_mainfinance_CAI` | `9fea372b8eaf439eafcf72f5bcd142b6` |
| `p_plateincome_CAI` | 埃及交易所板块收入情况表 | `oversea/p_plateincome_CAI` | `7b1589b4bee74ce9a972ab5d0a41a75f` |
| `p_regionalincome_CAI` | 埃及交易所地域收入情况表 | `oversea/p_regionalincome_CAI` | `5b185b9bc68547c89965e38285ca5013` |
| `p_tranindex_CAI` | 埃及交易所最新交易指标表 | `oversea/p_tranindex_CAI` | `1658a9ccab0c4f43944df568311aec34` |

#### 埃及证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_CAI` | 埃及交易所行情数据 | `oversea/p_quotadata_CAI` | `89e1d23a4802408388d32743d66f7a17` |
| `p_stockexefactor_CAI` | 埃及交易所股票除权因子表 | `oversea/p_stockexefactor_CAI` | `9b97ffa703e640dfad03f25075c4256a` |

### 阿姆斯特丹证券交易所

#### 阿姆斯特丹证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_AMS` | 阿姆斯特丹交易所上市公司中文简介 | `oversea/p_cnintroduce_AMS` | `324f433a386640c9b18a7347842eb89b` |
| `p_executives_AMS` | 阿姆斯特丹交易所高管 | `oversea/p_executives_AMS` | `a11a43582eb74c798179b181ddbb8b10` |
| `p_info_AMS` | 阿姆斯特丹交易所公司基本情况 | `oversea/p_info_AMS` | `ec6f4ed1ec2b4e168098e840dc6e560c` |

#### 阿姆斯特丹证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_AMS` | 阿姆斯特丹交易所派息 | `oversea/p_dividends_AMS` | `d3d96c6279724c45970d61c826469a95` |

#### 阿姆斯特丹证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_AMS` | 阿姆斯特丹交易所并购 | `oversea/p_manda_AMS` | `c756c9c5cd724308948662f0ba04519d` |

#### 阿姆斯特丹证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_AMS` | 阿姆斯特丹交易所股本变化表 | `oversea/p_cine_AMS` | `5e3e71f804fc41f6872fd3d125bc252d` |
| `p_latestequity_AMS` | 阿姆斯特丹交易所最新股本表 | `oversea/p_latestequity_AMS` | `2567cf3f07c54fea9a6543ccb8b3fadd` |
| `p_shareholders_AMS` | 阿姆斯特丹交易所主要股东表 | `oversea/p_shareholders_AMS` | `a46d479deb894261b3635a8be67d7f12` |

#### 阿姆斯特丹证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_AMS` | 阿姆斯特丹交易所通用现金流量表 | `oversea/p_cashflow_AMS` | `2b2e2e6861854896b38e6bea5be13074` |
| `p_finanderive_AMS` | 阿姆斯特丹交易所财务衍生报表 | `oversea/p_finanderive_AMS` | `9ff3720d4f004dfa8770713e785e7adc` |
| `p_income_AMS` | 阿姆斯特丹交易所通用利润表 | `oversea/p_income_AMS` | `6e4eea29bbdf4a42bff405c36f3dedc4` |
| `p_liabilities_AMS` | 阿姆斯特丹交易所通用资产负债表 | `oversea/p_liabilities_AMS` | `0bb4ebf8509a405c937237be2aeb1dfd` |
| `p_mainfinance_AMS` | 阿姆斯特丹交易所主要财务指标 | `oversea/p_mainfinance_AMS` | `fbd43b4401b649dbb9c7378b11e1e467` |
| `p_plateincome_AMS` | 阿姆斯特丹交易所板块收入情况表 | `oversea/p_plateincome_AMS` | `6d19ec4a1cf54191838757e8c5552d7f` |
| `p_regionalincome_AMS` | 阿姆斯特丹交易所地域收入情况表 | `oversea/p_regionalincome_AMS` | `b9ec975385ad45fa89782ffcbf00e7c4` |
| `p_tranindex_AMS` | 阿姆斯特丹交易所最新交易指标表 | `oversea/p_tranindex_AMS` | `a9fd7079b048497f99bd622a55b2da5f` |

#### 阿姆斯特丹证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_AMS` | 阿姆斯特丹交易所行情数据 | `oversea/p_quotadata_AMS` | `e44394f66b364720b77add7b0224a8ec` |
| `p_stockexefactor_AMS` | 阿姆斯特丹交易所股票除权因子表 | `oversea/p_stockexefactor_AMS` | `ae070bcb56074303a39e08643524364b` |

### 韩国证券交易所

#### 韩国证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_KRX` | 韩国交易所上市公司中文简介 | `oversea/p_cnintroduce_KRX` | `dc4694f27cae4d73a054e73b76c934e5` |
| `p_executives_KRX` | 韩国交易所高管 | `oversea/p_executives_KRX` | `53b3a5dbf24c4982acde17f431d1f819` |
| `p_info_KRX` | 韩国交易所公司基本情况 | `oversea/p_info_KRX` | `f4500a167edc4a338ebf9bf7ce07f154` |

#### 韩国证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_KRX` | 韩国交易所派息 | `oversea/p_dividends_KRX` | `ce2b8b4dc9d248c0a6011e58bacdec65` |

#### 韩国证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_KRX` | 韩国交易所并购 | `oversea/p_manda_KRX` | `577d851cb64f4b1bbc4be70ea68a090f` |

#### 韩国证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_KRX` | 韩国交易所股本变化表 | `oversea/p_cine_KRX` | `6c475dcddac8488d9574f7538c79ddd6` |
| `p_latestequity_KRX` | 韩国交易所最新股本表 | `oversea/p_latestequity_KRX` | `f7fd39b2e3294ad88f1355f7a81e3708` |
| `p_shareholders_KRX` | 韩国交易所主要股东表 | `oversea/p_shareholders_KRX` | `91d143d7b42f404da77a4b9896c454db` |

#### 韩国证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_KRX` | 韩国交易所通用现金流量表 | `oversea/p_cashflow_KRX` | `02e6767a7110430f9d1998d6a38910d5` |
| `p_finanderive_KRX` | 韩国交易所财务衍生报表 | `oversea/p_finanderive_KRX` | `d82d56a1321449f9a604df1a64b6fa19` |
| `p_income_KRX` | 韩国交易所通用利润表 | `oversea/p_income_KRX` | `dea957820e084fc484ec9847a2650c45` |
| `p_liabilities_KRX` | 韩国交易所通用资产负债表 | `oversea/p_liabilities_KRX` | `a2b838ddc00d4f788a776fbf9600e54f` |
| `p_mainfinance_KRX` | 韩国交易所主要财务指标 | `oversea/p_mainfinance_KRX` | `e3f068dd3fe9474491dfed0b6eedec01` |
| `p_plateincome_KRX` | 韩国交易所板块收入情况表 | `oversea/p_plateincome_KRX` | `3a066e89361e479f8ee289c5d185ec6a` |
| `p_regionalincome_KRX` | 韩国交易所地域收入情况表 | `oversea/p_regionalincome_KRX` | `81dab56d8ed14ce59d25f55bef2730fa` |
| `p_tranindex_KRX` | 韩国交易所最新交易指标表 | `oversea/p_tranindex_KRX` | `516ad7ec603e44bbb5123ef62f84a8d4` |

#### 韩国证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_KRX` | 韩国交易所行情数据 | `oversea/p_quotadata_KRX` | `999ce1e43109455795d61d39355c7538` |
| `p_stockexefactor_KRX` | 韩国交易所股票除权因子表 | `oversea/p_stockexefactor_KRX` | `1123c7c2ccaa4e5fad37dd582e9b133d` |

### 新西兰证券交易所

#### 新西兰证券交易所公司概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cnintroduce_NZE` | 新西兰交易所上市公司中文简介 | `oversea/p_cnintroduce_NZE` | `ad93a7b9c3ce48ffb5d759b3833bfcbe` |
| `p_executives_NZE` | 新西兰交易所高管 | `oversea/p_executives_NZE` | `8a4b5d5f49eb4ce9addca4288b780688` |
| `p_info_NZE` | 新西兰交易所公司基本情况 | `oversea/p_info_NZE` | `bfbe970b41664817bd3ddd6f47e8f148` |

#### 新西兰证券交易所公司派息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_dividends_NZE` | 新西兰交易所派息 | `oversea/p_dividends_NZE` | `5306e68be77f4af1b2b69969b2ad83f6` |

#### 新西兰证券交易所公司并购

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_manda_NZE` | 新西兰交易所并购 | `oversea/p_manda_NZE` | `aeefd5f635924f12b3d9b8082f49b511` |

#### 新西兰证券交易所股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cine_NZE` | 新西兰交易所股本变化表 | `oversea/p_cine_NZE` | `ff91845460584f2a8da1645a5db79e64` |
| `p_latestequity_NZE` | 新西兰交易所最新股本表 | `oversea/p_latestequity_NZE` | `979a6bb6b7c14d08a722ee6769efccf6` |
| `p_shareholders_NZE` | 新西兰交易所主要股东表 | `oversea/p_shareholders_NZE` | `47733e5f3ea14f3c985cfe04b41c9c57` |

#### 新西兰证券交易所财务数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cashflow_NZE` | 新西兰交易所通用现金流量表 | `oversea/p_cashflow_NZE` | `1a622037cb97440db5a88ac17a282f5e` |
| `p_finanderive_NZE` | 新西兰交易所财务衍生报表 | `oversea/p_finanderive_NZE` | `63d3a32d92594a5c84f6a74ee1edec19` |
| `p_income_NZE` | 新西兰交易所通用利润表 | `oversea/p_income_NZE` | `cdd19a1d67f848dda920362889e4ce74` |
| `p_liabilities_NZE` | 新西兰交易所通用资产负债表 | `oversea/p_liabilities_NZE` | `0964464c0679408ea03b46df9925e99b` |
| `p_mainfinance_NZE` | 新西兰交易所主要财务指标 | `oversea/p_mainfinance_NZE` | `b54bf5cb241b4903b1e98e934dce2466` |
| `p_plateincome_NZE` | 新西兰交易所板块收入情况表 | `oversea/p_plateincome_NZE` | `e392e1e3b22341d39086c521e49d746c` |
| `p_regionalincome_NZE` | 新西兰交易所地域收入情况表 | `oversea/p_regionalincome_NZE` | `7dad1f56784f4586ac5c3694fd26723c` |
| `p_tranindex_NZE` | 新西兰交易所最新交易指标表 | `oversea/p_tranindex_NZE` | `0f0f63f5d1a84ef5b6bcf180e70097a0` |

#### 新西兰证券交易所行情数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_quotadata_NZE` | 新西兰交易所行情数据 | `oversea/p_quotadata_NZE` | `3442be16f302435383914f7cc1d9fb9c` |
| `p_stockexefactor_NZE` | 新西兰交易所股票除权因子表 | `oversea/p_stockexefactor_NZE` | `a7314fa4d0bb45549bd626e78c2ae11f` |

## 宏观数据

### 宏观-热点数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_CPI` | 全国居民消费价格指数 | `macro/p_CPI` | `6ce0003d35214568ac1311d52056cc0b` |
| `p_PMI` | 采购经理指数（月度） | `macro/p_PMI` | `7235239291a844008c24ff03a1e5d9d0` |
| `p_PPI` | 工业生产者出厂价格指数 | `macro/p_PPI` | `4dcc67c8b3e64cf3b15d77b024c108a7` |
| `p_macro9034` | 货币供应量月度统计表 | `macro/p_macro9034` | `640ce506df2d46658131189580ea2bb9` |

### 公共编码

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_BalanceSheetMenu` | 央行资产负债表科目查询 | `macro/p_BalanceSheetMenu` | `732c967ed3514200a1117936750c679f` |
| `p_MajorIndustrialProducts` | 工业主要产品列表 | `macro/p_MajorIndustrialProducts` | `d54d22cc8b5f4c2da6c84f1d2c72952c` |
| `p_SourcesandUsesofCreditFunds` | 信贷收支表科目列表 | `macro/p_SourcesandUsesofCreditFunds` | `85a9c54a4c2f4f54b424b34ccf010829` |
| `p_countryinfo` | 国家（地区）编码 | `macro/p_countryinfo` | `4cc4da37056c4d1a95791892cac7dac9` |
| `p_macro9002` | 重要宏观数据日历 | `macro/p_macro9002` | `73a3d17a3d1c45daaa07a00168ea2ff9` |
| `p_macrobaseinfo` | 宏观数据基本编码 | `macro/p_macrobaseinfo` | `01fc8ce3091f4e27b7165edb605c71de` |

### 价格指数

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_CPI` | 全国居民消费价格指数 | `macro/p_CPI` | `6ce0003d35214568ac1311d52056cc0b` |
| `p_CPIbyCategory` | 全国居民消费价格指数分类指数 | `macro/p_CPIbyCategory` | `75dd194cd9d74584b98a790df99923f2` |
| `p_CPIbyRegion` | 各省市居民消费价格指数 | `macro/p_CPIbyRegion` | `7813f57800cb412692a2f0e6392fb079` |
| `p_CPIbyRegionandCategory` | 各省市居民消费价格指数分类指数 | `macro/p_CPIbyRegionandCategory` | `3e2018c1a4f04057ab777b42beb8f31c` |
| `p_PPI` | 工业生产者出厂价格指数 | `macro/p_PPI` | `4dcc67c8b3e64cf3b15d77b024c108a7` |
| `p_PPIbyCategory` | 工业生产者出厂价格行业分类指数(月度) | `macro/p_PPIbyCategory` | `2833bc3e11814b659576333ebfc1b680` |
| `p_PurchasingPriceIndex` | 全国工业生产者购进价格指数(月度) | `macro/p_PurchasingPriceIndex` | `3ba2f51db3224dcea3d7bc649e4a81b9` |
| `p_PurchasingPriceIndexbyRegion` | 各省市工业生产者购进价格指数(月度) | `macro/p_PurchasingPriceIndexbyRegion` | `de16ed443d7646fabb4b8fb5cf90b2f4` |
| `p_PurchasingPriceIndexbyRegionandCategory` | 各省市工业生产者购进价格指数—分类指数(月度) | `macro/p_PurchasingPriceIndexbyRegionandCategory` | `efb722cd6e3846f1bb3449bd228738f1` |
| `p_RPI` | 全国商品零售价格指数(月度) | `macro/p_RPI` | `ccfccc2231c6408a888142353a9784eb` |
| `p_RPIbyCategory` | 全国商品零售价格指数-分类指数 | `macro/p_RPIbyCategory` | `d5f3a10ce81b4b108532221eb914098b` |
| `p_RPIbyRegion` | 各省市商品零售价格指数(月度) | `macro/p_RPIbyRegion` | `d02295e1d6524570a17cffd932d5f7d5` |
| `p_RPIbyRegionandCategory` | 各省市商品零售价格指数(月度)--分类指数 | `macro/p_RPIbyRegionandCategory` | `c4f548779548419a8ccab8247254b4b9` |
| `p_macro9015` | 生产资料类工业生产者出厂价格指数(月度) | `macro/p_macro9015` | `4fd7887cb34d406c89f7d67f9addfa58` |
| `p_macro9016` | 生活资料类工业生产者出厂价格指数(月度) | `macro/p_macro9016` | `bbd09bccc33640f18b7bbf49211eb3e9` |
| `p_macro9017` | 全国农业价格指数(月度) | `macro/p_macro9017` | `e158db7b7f6e4a3b94cf7a0274a2c5f1` |
| `p_macro9019` | 全国固定资产投资价格指数(季度) | `macro/p_macro9019` | `7b19f168f93a4399b6cdbfd6eb29e839` |
| `p_macro9024` | 各省市固定资产投资价格指数(季度) | `macro/p_macro9024` | `9015e371ac854301995a333cd53d8fae` |

### 金融运行指数

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_SourcesandUsesofCreditFunds` | 信贷收支表科目列表 | `macro/p_SourcesandUsesofCreditFunds` | `85a9c54a4c2f4f54b424b34ccf010829` |
| `p_macro9034` | 货币供应量月度统计表 | `macro/p_macro9034` | `640ce506df2d46658131189580ea2bb9` |
| `p_macro9035` | 中央银行（货币当局）资产负债表 | `macro/p_macro9035` | `8170278f64ef466c954d0fc88ec1cb84` |
| `p_macro9036` | 国际储备月度统计表 | `macro/p_macro9036` | `18b14683988a48459dda2e20035ac0e8` |
| `p_macro9037` | 金融机构人民币信贷收支表 （按类型） | `macro/p_macro9037` | `87f888fdb7dd49839212630f47992340` |
| `p_macro9038` | 金融机构人民币信贷收支表（按部门、用途） | `macro/p_macro9038` | `56161d8b7aca464587d51246ea8a20d8` |
| `p_macro9039` | 金融机构本外币信贷收支表（按类型） | `macro/p_macro9039` | `b9847640ecad4756979673120e0ce3e3` |
| `p_macro9040` | 金融机构本外币信贷收支表（按部门、用途） | `macro/p_macro9040` | `e6b8c92f6a694fbabda2d54393705333` |
| `p_macro9041` | 其他存款性公司资产负债表 | `macro/p_macro9041` | `d7756c905da9458e836c246fab776119` |

### 经济运行指数

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_CCI` | 消费者信心指数月度统计 | `macro/p_CCI` | `39f1aefa891e478c857c9222650feefe` |
| `p_CategoryforInduValAdded` | 工业增加值增长速度细分行业列表 | `macro/p_CategoryforInduValAdded` | `3a9aa033049848968ba7dc339a1a1be6` |
| `p_GrowthRateofInduValAdded` | 全国工业增加值增长速度（月度） | `macro/p_GrowthRateofInduValAdded` | `0faae096b4494ff89c70188952f62d3d` |
| `p_GrowthRateofInduValAddedbyCategory` | 全国细分行业工业增加值增长速度（月度） | `macro/p_GrowthRateofInduValAddedbyCategory` | `4c21c7c247ff42e29d92e06d0dc681af` |
| `p_GrowthRateofInduValAddedbyRegion` | 各省市工业增加值增长速度（月度） | `macro/p_GrowthRateofInduValAddedbyRegion` | `b0c1e988b30d44b7b77b0d66e69328a7` |
| `p_GrowthRateofInduValAddedbyRegionandCategory` | 各省市细分行业工业增加值增长速度（月度） | `macro/p_GrowthRateofInduValAddedbyRegionandCategory` | `515f7b0393c346fd9db9e61a14955dbf` |
| `p_MajorIndustrialProducts` | 工业主要产品列表 | `macro/p_MajorIndustrialProducts` | `d54d22cc8b5f4c2da6c84f1d2c72952c` |
| `p_PMI` | 采购经理指数（月度） | `macro/p_PMI` | `7235239291a844008c24ff03a1e5d9d0` |
| `p_macro9025` | 全国工业主要产品产量及增长速度 | `macro/p_macro9025` | `31f734f27d3d4558bd5189a200eb96dc` |
| `p_macro9028` | 全国工业企业经济效益综合数据(月度) | `macro/p_macro9028` | `186ccd74d13443cbb67106895444ce21` |
| `p_macro9029` | 全国各行业工业企业利润额(月度) | `macro/p_macro9029` | `be67513be54d4fb6ae3459c33ccd77c6` |
| `p_macro9031` | 银行业景气指数(季度) | `macro/p_macro9031` | `674df3531a964811a2836bc9503883db` |
| `p_macro9032` | 各省市工业主要产品产量及增长速度 | `macro/p_macro9032` | `fb72f984e2d3450284455ffbba0c9cf6` |
| `p_macro9047` | 全国消费品零售总额综合数据(月度) | `macro/p_macro9047` | `bd16d601f6e948f29c8c0c41116278ea` |

### 房地产与固定资产投资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_macro9019` | 全国固定资产投资价格指数(季度) | `macro/p_macro9019` | `7b19f168f93a4399b6cdbfd6eb29e839` |
| `p_macro9024` | 各省市固定资产投资价格指数(季度) | `macro/p_macro9024` | `9015e371ac854301995a333cd53d8fae` |
| `p_macro9042` | 全国房地产建设与销售 | `macro/p_macro9042` | `4aaeaa6c96394b159b6eabed3f15a769` |
| `p_macro9043` | 各省市房地产建设与销售 | `macro/p_macro9043` | `f05daf0815cd46b28e1f283c459d4fe9` |
| `p_macro9046` | 全国城镇固定资产投资情况(月度) | `macro/p_macro9046` | `abba8aadc75145ffb0da06f99f777c03` |
| `p_macro9050` | 各省市城镇固定资产投资情况(月度) | `macro/p_macro9050` | `44d91712b5584c73b733b323c100b83e` |

### 国民经济与政府财政

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_macro9049` | 各国对华直接投资月度统计 | `macro/p_macro9049` | `ad10b3455f774f33bb0db9c8a91e4d55` |
| `p_macro9054` | 全国政府财政收支情况(月度) | `macro/p_macro9054` | `28fa70bf23054ccf99780081d6f60d79` |
| `p_macro9055` | 全国家庭收入及支出统计（季度) | `macro/p_macro9055` | `f598015cf48749a9af92542224df95b5` |
| `p_macro9056` | 生产法国民生产总值表 | `macro/p_macro9056` | `e30b40802523491586bc0d160c257730` |
| `p_macro9057` | 生产法国内生产总值分季度统计表 | `macro/p_macro9057` | `b9e95a8763ab479c915005d8c8fc6363` |
| `p_macro9058` | 生产法国内生产总值各地区分季度统计表 | `macro/p_macro9058` | `276bdf78944547a8bf42240154decebe` |

### 贸易与投资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_macro9048` | 全国进出口贸易数据(月度) | `macro/p_macro9048` | `d415d026bc484a479a1f9e6b1d3a4f91` |
| `p_macro9049` | 各国对华直接投资月度统计 | `macro/p_macro9049` | `ad10b3455f774f33bb0db9c8a91e4d55` |
| `p_macro9052` | 各省市进出口贸易数据(月度) | `macro/p_macro9052` | `0a5b33779d4b401595369cbdc50a925d` |
| `p_macro9053` | 各行业实际使用外国直接投资表(月度) | `macro/p_macro9053` | `177b256ce3944673a44b8b74280558ed` |

## 证券提示库数据服务

### 股票类

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3039` | 股票类资讯内容全量记录 | `info/p_info3039` | `0891ada8a8f44118990f25e7c83efc9c` |
| `p_info3041` | 股票类提示内容全量记录 | `info/p_info3041` | `9ad1aac088c044de9d5081ad83c0bab3` |
| `p_info3091` | 上市公司互动信息智能摘要 | `info/p_info3091` | `68d977f1d3f14779b98b9012566d35b0` |

### 基金类

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3043` | 基金类资讯内容全量记录 | `info/p_info3043` | `bf20606042c34cc5a56c0abb25083c21` |
| `p_info3045` | 基金类提示内容全量记录 | `info/p_info3045` | `bc8e4d9b4a72404a87ce8963cf090a7d` |

### 债券类

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3047` | 债券类资讯内容全量记录 | `info/p_info3047` | `c48089fa745644f590308727d53af854` |
| `p_info3049` | 债券类提示内容全量记录 | `info/p_info3049` | `8abbffc7e8e04410849823ab22231aa9` |

### 新三板

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3057` | 新三板资讯内容全量记录 | `info/p_info3057` | `1611f2dc9f2447d9a0dda0b5f2bd5379` |
| `p_info3059` | 新三板提示内容全量记录 | `info/p_info3059` | `cb86f853ac2d4887ac8fc357402870f9` |

### 港股类

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3078` | 港股提示内容全量记录 | `info/p_info3078` | `bedeb7ef0a0249b7bf82ce6d762f2539` |
| `p_info3079_AI` | 港股智能资讯接口 | `info/p_info3079_AI` | `24e2f94faa544fe594ecce77166cc13b` |
| `p_info3080` | 港股资讯内容全量记录 | `info/p_info3080` | `ab39458230fc41f4937cf6db90098d3a` |

## 深证信VIP数据服务

### 上市公司实时落地数据

#### 上市公司基础数据

##### 公司基本信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2100_inc` | 公司基本信息 | `load/p_stock2100_inc` | `7e33330155c1477d80b9a10ccb9d3d6e` |

##### 股票基本信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2101_inc` | 股票基本信息 | `load/p_stock2101_inc` | `e5ed155b084b48f19995537f4c95bd89` |

##### 公司管理人员任职情况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2102_inc` | 公司管理人员任职情况 | `load/p_stock2102_inc` | `63c700e98cb84d8eb01461190229af64` |

##### 公司员工情况表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2107_inc` | 公司员工情况表 | `load/p_stock2107_inc` | `cc7d367dcf054e789512516f8519644e` |

##### 上市公司状态报表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2117_inc` | 公司上市状态变动情况表 | `load/p_stock2117_inc` | `b31b833b27b34bee84ec9fda59565cb2` |

#### 上市公司分红募资数据

##### 分红转增信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2201_inc` | 分红转增信息 | `load/p_stock2201_inc` | `60dd83d9aa264f658f05f806611c9aca` |

##### 公司增发股票预案

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2229_inc` | 公司增发股票预案 | `load/p_stock2229_inc` | `be3c9d3f13284c3aa5c5ac355a796406` |

##### 公司增发股票实施方案

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2230_inc` | 公司增发股票实施方案 | `load/p_stock2230_inc` | `360c8dddb24a4f1583588e9203cd5fb9` |

##### 公司配股预案

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2231_inc` | 公司配股预案 | `load/p_stock2231_inc` | `74c2e1ba04a84cf9a8e67b168dd05b9f` |

##### 公司配股实施方案

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2232_inc` | 公司配股实施方案 | `load/p_stock2232_inc` | `70c3e887fcc8412e97450a7609776346` |

##### 公司首发股票

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2233_inc` | 公司首发股票 | `load/p_stock2233_inc` | `4e7a68b3585f491f8a63dee2d0452db2` |

##### 募集资金来源

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2234_inc` | 募集资金来源 | `load/p_stock2234_inc` | `4e8d645bc7554753bccb0aeda0d9c61b` |

##### 股票发行中介机构及承销情况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2235_inc` | 股票发行中介机构及承销情况 | `load/p_stock2235_inc` | `9bb0788bcfd2456bbd89010951284d39` |

##### 募集资金投资项目计划

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2236_inc` | 募集资金投资项目计划 | `load/p_stock2236_inc` | `c5ca7f2ed832493eb1be74d9a08d8e80` |

##### 新股过会情况表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2262_inc` | 新股过会情况表 | `load/p_stock2262_inc` | `4e6c8abb60184fdf877e4445b43a1072` |

##### 优先股派息表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2263_inc` | 优先股派息表 | `load/p_stock2263_inc` | `837fa542e3224eec988c7ebbb07bc3ee` |

#### 上市公司并购重组数据

##### 公司资产重组概况

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2241_inc` | 公司资产重组概况 | `load/p_stock2241_inc` | `e9a06dacf36b4f4c8024447391c0aab1` |

##### 公司债务重组

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2242_inc` | 公司债务重组 | `load/p_stock2242_inc` | `fa5b6531393743acb7171540e2a5ab08` |

##### 公司吸收合并

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2243_inc` | 公司吸收合并 | `load/p_stock2243_inc` | `a295b39dc7b0487ea90752dc08631641` |

##### 公司股权变更表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2244_inc` | 上市公司股权被转让变更的情况 | `load/p_stock2244_inc` | `a77cd0358243488486fd961edea5f17f` |

##### 公司产品出让表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2251_inc` | 公司产品出让表 | `load/p_stock2251_inc` | `a39a6c75677c4baa9b83a876cf33f286` |

##### 公司资产收购表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2252_inc` | 公司资产收购表 | `load/p_stock2252_inc` | `430ab7699cca4ab1ada9d6daf1872f8b` |

##### 公司资产置换表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2253_inc` | 公司资产置换表 | `load/p_stock2253_inc` | `58edaa58332b414a985d4c90a6f42aa9` |

##### 并购重组基本信息表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2254_inc` | 并购重组基本信息表 | `load/p_stock2254_inc` | `6ca2a9ac2b02448ea7401661cee508aa` |

##### 并购重组标的表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2255_inc` | 并购重组标的表 | `load/p_stock2255_inc` | `bc6ae537d7354f679c4f870221db2dbf` |

##### 并购重组标的公司财务指标表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2256_inc` | 并购重组标的公司财务指标表 | `load/p_stock2256_inc` | `8052cd9d6d014154aec7f97443599dca` |

##### 并购重组交易对手情况表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2257_inc` | 并购重组交易对手情况表 | `load/p_stock2257_inc` | `965546bcca8e455a9309fb43e68e0e76` |

## 深证信专业订制数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_EquityStructure` | Equity Structure (for Bloomberg) | `stock/p_EquityStructure` | `aa1019589d24466193a67e8bd9c7003d` |
| `p_PeriodicReportsDisclosureSchedule` | Periodic Reports Disclosure Schedule  (for Bloomberg) | `stock/p_PeriodicReportsDisclosureSchedule` | `e16c9d449f19482f87aad3ea58396359` |

### 订制数据-众信电子

#### 科金定制数据接口

##### 科技金融产品定制接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_comnewslist` | 新闻列表 | `bigdata/p_comnewslist` | `d6c8c43cafad4c1aa17330f6fa41056f` |
| `p_neeq6021` | 新三版财务衍生指标数据 | `neeq/p_neeq6021` | `9622a5fe38b34832ad92204bd94fab7b` |
| `p_neeq6030` | 市值相关指标 | `neeq/p_neeq6030` | `3c15c6bd832b420ea9654f493cdde2a6` |
| `p_stock2240` | 上市公司股东变动汇总表 | `stock/p_stock2240` | `6879259fab2f46a297f793bb49d01054` |
| `p_stock2329` | 个股单季财务利润表 | `stock/p_stock2329` | `af00e0c3965d433998b133c8ae7e2c83` |
| `p_stock2330` | 个股单季现金流量表 | `stock/p_stock2330` | `50e56707f95d40318cd6700d2ab2b540` |
| `p_stock2331` | 个股单季财务指标 | `stock/p_stock2331` | `bfed9ba2aa814a34bcdf382896fca762` |
| `p_stock2332` | 个股TTM财务利润表 | `stock/p_stock2332` | `a463852dd6c74f27b92bf6419603e381` |
| `p_stock2333` | 个股TTM现金流量表 | `stock/p_stock2333` | `5ec0f9cccfcf44dcbd2e134fb9e4d82c` |
| `p_stock2334` | TTM主要财务指标 | `stock/p_stock2334` | `2380064aeb754424806a14c0708ddd92` |
| `p_stock2335` | 市值计算指标 | `stock/p_stock2335` | `f9cd3fe4d7024a25bb0ec3e9d3209a69` |
| `p_stock2407` | 股票前后复权日行情表 | `stock/p_stock2407` | `bbcee85fd60b4e719d2cf7ea897b0c06` |
| `p_stock2410` | 股票前后复权行情周报 | `stock/p_stock2410` | `59aa3a6c9aaa420f98a2c98f48b6dc40` |
| `p_stock2411` | 股票前后复权行情月报 | `stock/p_stock2411` | `4ccf837aa23f46ec8be0dd8b8498e206` |
| `p_stock2412` | 股票前后复权行情年报 | `stock/p_stock2412` | `dc25fadcaad44e3c8d27af218e820cc8` |
| `p_stock2503` | 分红募资统计 | `stock/p_stock2503` | `cf11c1da3afe45d1b04c80fd9da77884` |

#### 大数据包

##### BIGDATA

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_APP` | APP信息 | `bigdata/p_APP` | `2056f7d5113a418dbd63f79486b0bae2` |
| `p_AnnouncementPush` | 重点公告推送 | `bigdata/p_AnnouncementPush` | `4775947ee80f4153a8a5eb5944a955a0` |
| `p_announceinfo` | 法院公告详情 | `bigdata/p_announceinfo` | `73c2bfbe9e4846d0a63971b862a6d0be` |
| `p_announcement` | 法院公告列表 | `bigdata/p_announcement` | `b929dd96e68b4eacb3a2ae42793ff193` |
| `p_branchs` | 分支机构 | `bigdata/p_branchs` | `b8e2d9a38c984d6ea95382702203f056` |
| `p_changes` | 工商变更 | `bigdata/p_changes` | `098fdad5a3d74fd2b6d4955ba1be976e` |
| `p_comnewsinfo` | 新闻详情 | `bigdata/p_comnewsinfo` | `b9d9b23c2f384298986d122b54a6fa2f` |
| `p_comnewslist` | 新闻列表 | `bigdata/p_comnewslist` | `d6c8c43cafad4c1aa17330f6fa41056f` |
| `p_companalysis` | 竞争分析 | `bigdata/p_companalysis` | `5f57f0afef3c4b63be3d9155c1f2d8b1` |
| `p_copyright` | 作品著作权 | `bigdata/p_copyright` | `6e4f496e96644581a3fa241eb3e01fa7` |
| `p_dishonest` | 失信列表 | `bigdata/p_dishonest` | `6e9ab9491e8d45748a7e3c289cdc389b` |
| `p_dishonestinfo` | 失信详情 | `bigdata/p_dishonestinfo` | `f0c85a4d6b1244f5a5b738ecf04cd2c9` |
| `p_financinghistory` | 融资历史 | `bigdata/p_financinghistory` | `a8782d5050794b82b5b7d84838cf4d79` |
| `p_graph` | p_graph | `bigdata/p_graph` | `160c60a8ed864aff85912b57276f132a` |
| `p_holders` | 工商股东 | `bigdata/p_holders` | `93dba9d4db114d57ae79cbd917ad61ae` |
| `p_humaninfo` | 人物详情 | `bigdata/p_humaninfo` | `bbcbb2e67b0b45efa2601e8032849672` |
| `p_icprecord` | 网站备案 | `bigdata/p_icprecord` | `2724939b2f7946cea75a9551754d23eb` |
| `p_info` | 公司详情 | `bigdata/p_info` | `40f1d6ab5bf7423cb9d3763a0751933b` |
| `p_invests` | 对外投资 | `bigdata/p_invests` | `f1f89bb5a58f4e579b4250cd209127c0` |
| `p_job` | 招聘 | `bigdata/p_job` | `ffef6e3f4cbd4e44803252d03ee84daa` |
| `p_lawsuitinfo` | 法律文书详情 | `bigdata/p_lawsuitinfo` | `79e58a8afcd84022921a2b1b906e4acb` |
| `p_lawsuits` | 法律文书列表 | `bigdata/p_lawsuits` | `58940f97cc1d4762937cd9e7f989a4c8` |
| `p_managers` | 公司高管 | `bigdata/p_managers` | `ddf1a002afd242438fedb028ac220d2d` |
| `p_noticeinfo` | 开庭公告详情 | `bigdata/p_noticeinfo` | `1f3635197d1f41f9b22b3df9e7f13c65` |
| `p_notices` | 开庭公告列表 | `bigdata/p_notices` | `97fa63e934944b50be1f72366c0bbd1f` |
| `p_patent` | 专利列表 | `bigdata/p_patent` | `ae21030013f041868551f81be62cc641` |
| `p_patentinfo` | 专利详情 | `bigdata/p_patentinfo` | `2778538c7ded4cedbefc1607fcc70ce2` |
| `p_personcompanynum` | 人物相关公司数量 | `bigdata/p_personcompanynum` | `33e70fcbc9fd4bda8c3ea5b63f093132` |
| `p_prelistingTutor` | 上市前辅导 | `bigdata/p_prelistingTutor` | `74d856e3c8304ceeb85408c5b2f38ae4` |
| `p_projectinfo` | 意向项目详情 | `bigdata/p_projectinfo` | `c29cae7484f046758c1b921d759d079c` |
| `p_prompt` | 搜索提示 | `bigdata/p_prompt` | `ad46891157fb46ea9add84bf7d1f38d2` |
| `p_reference` | 参考资料列表 | `bigdata/p_reference` | `e2bb52a394074b0fa9cbacec1c34718f` |
| `p_referenceinfo` | 参考资料详情 | `bigdata/p_referenceinfo` | `463d866e632a4ff4aa6f2ce9ba0868dc` |
| `p_regcpinfo` | 软件著作权详情 | `bigdata/p_regcpinfo` | `68d37b066d264f64a65a2de03adda360` |
| `p_regcyright` | 软件著作权列表 | `bigdata/p_regcyright` | `036f8b61c01d46e8b332cd4827907b22` |
| `p_researchreport` | 研报 | `bigdata/p_researchreport` | `787382b2b5004f9ca0c83b53290e5398` |
| `p_tm` | 商标列表 | `bigdata/p_tm` | `5a43a09e2d0f43f3a6fa8c9258883aa2` |
| `p_tminfo` | 商标详情 | `bigdata/p_tminfo` | `90f1c054ed5541e5ac0f44fd526cf964` |
| `p_zhixinginfo` | 被执行人 | `bigdata/p_zhixinginfo` | `c5a8dad3bc3a455daa6b752671ebb536` |

### 订制数据-正前方

#### 债券募集说明书接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3017` | 债券募集说明书公告 | `info/p_info3017` | `283ad3d28d454d7ca13e8ad6c3647963` |

## 数据浏览器

### 基本资料

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1018` | 基本资料 | `sysapi/p_sysapi1018` | `613f2062eea24447b9df4cbc203bfb6d` |

### 股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2213` | 公司股东实际控制人 | `stock/p_stock2213` | `b2555f4def9447d28a60f61766935877` |
| `p_stock2215` | 公司股本变动 | `stock/p_stock2215` | `1a4ac5994044470a9759d3675f9ac372` |
| `p_stock2218` | 上市公司高管持股变动 | `stock/p_stock2218` | `fd626eec701c40fe90f79c63add6325f` |
| `p_stock2226` | 股东增（减）持情况 | `stock/p_stock2226` | `9000cd76f0d640b9ba8cb79eb90748a0` |
| `p_sysapi1020` | 持股集中度 | `sysapi/p_sysapi1020` | `399f3a274f404cddb0df3908125869c8` |

### 投资评级

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2205` | 投资评级 | `sysapi/p_stock2205` | `d7afdca660264fc28253479e627935b7` |

### 业绩预期

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2238` | 上市公司业绩预告 | `stock/p_stock2238` | `97c2b582835244c1bdafc704c8fc9408` |

### 分红指标

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1019` | 分红指标 | `sysapi/p_sysapi1019` | `66ac85d341c4484a9d287f31ba59cc80` |

### 筹资指标

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2223` | 股东大会议案 | `stock/p_stock2223` | `29d6a4172d274db69f4267b87931738c` |
| `p_stock2229` | 公司增发股票预案 | `stock/p_stock2229` | `f47f4d5304b34d77b10a843685282bcc` |
| `p_stock2230` | 公司增发股票实施方案 | `stock/p_stock2230` | `28e105950c7d4d8bb4ef9679a525c06a` |
| `p_stock2231` | 公司配股预案 | `stock/p_stock2231` | `ac6ecb8efb7b4101ac1f3a69cef50252` |
| `p_stock2232` | 公司配股实施方案 | `stock/p_stock2232` | `71a7162a7ebe434c81ef0c45c8c60240` |

### 财务指标

#### 报告期

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2300` | 个股报告期资产负债表 | `stock/p_stock2300` | `5474f0bfcc0a497197b3fe9cdf37befb` |
| `p_stock2301` | 个股报告期利润表 | `stock/p_stock2301` | `0838f71fe00e4d00bb4d9a8d45df8472` |
| `p_stock2302` | 个股报告期现金表 | `stock/p_stock2302` | `dff987d3d00e4c62afeb042bb3f6a84b` |
| `p_stock2325` | 金融类资产负债表2007版 | `stock/p_stock2325` | `e0ad51bd4c2743ce88ef0932503e51e9` |
| `p_stock2326` | 金融类利润表2007版 | `stock/p_stock2326` | `e8945e68ef5247f8ba51b58151407cef` |
| `p_stock2327` | 金融类现金流量表2007版 | `stock/p_stock2327` | `c77eaa699e2b42dcb2889c55dfdc554c` |

#### 财务指标

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2303` | 个股报告期指标表 | `stock/p_stock2303` | `87701f2530ae482ab2a999dae0dde022` |
| `p_stock2501` | 财务指标行业排名 | `stock/p_stock2501` | `8b6a4cacff0a4b3d88a53755bcaa0136` |

#### 单季度

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2329` | 个股单季财务利润表 | `stock/p_stock2329` | `af00e0c3965d433998b133c8ae7e2c83` |
| `p_stock2330` | 个股单季现金流量表 | `stock/p_stock2330` | `50e56707f95d40318cd6700d2ab2b540` |
| `p_stock2331` | 个股单季财务指标 | `stock/p_stock2331` | `bfed9ba2aa814a34bcdf382896fca762` |

#### TTM

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_stock2332` | 个股TTM财务利润表 | `stock/p_stock2332` | `a463852dd6c74f27b92bf6419603e381` |
| `p_stock2333` | 个股TTM现金流量表 | `stock/p_stock2333` | `5ec0f9cccfcf44dcbd2e134fb9e4d82c` |

## 专题统计

### 股本股东

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 业绩与分红

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1037` | 业绩预告 | `sysapi/p_sysapi1037` | `6f7156ad0a044170b15e70da1a5bb552` |
| `p_sysapi1038` | 预告业绩扭亏个股 | `sysapi/p_sysapi1038` | `b9ea31b969b74ead8639aa1dc163b8b7` |
| `p_sysapi1039` | 预告业绩大幅下降个股 | `sysapi/p_sysapi1039` | `1219ab371d3346a3b597156e137e92d9` |
| `p_sysapi1040` | 预告业绩大幅上升个股 | `sysapi/p_sysapi1040` | `16de11a7a37742a4bbe53060dd33630f` |
| `p_sysapi1045` | 地区分红明细 | `sysapi/p_sysapi1045` | `4939ba7be4a243ad82de96307d1e571f` |
| `p_sysapi1046` | 行业分红明细 | `sysapi/p_sysapi1046` | `032dc0fca63847e480cb66ac048b3c3f` |
| `p_sysapi1129` | 报告期分红明细 | `sysapi/p_sysapi1129` | `c01f01725662494db5e8e7b3987f61e9` |

### 发行筹资

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1056` | 首发审核 | `sysapi/p_sysapi1056` | `140900f6d30c48ed81df564663f71ea2` |
| `p_sysapi1057` | 首发筹资 | `sysapi/p_sysapi1057` | `1757ad36ad9544468a96623feb707c1e` |
| `p_sysapi1058` | 增发筹资 | `sysapi/p_sysapi1058` | `83cfd75000154ee8a78033dc7a6cc504` |
| `p_sysapi1059` | 配股筹资 | `sysapi/p_sysapi1059` | `f81e96468f044257873340c550c7bcab` |
| `p_sysapi1060` | 公司债或可转债 | `sysapi/p_sysapi1060` | `1fb119598802429e8d48e1cc6002b941` |
| `p_sysapi1096` | 新股申购 | `sysapi/p_sysapi1096` | `7daff00f76034071ac1f3e626c51006e` |
| `p_sysapi1097` | 新股发行 | `sysapi/p_sysapi1097` | `cbf469fc3f674a3c83680cb8034f76c1` |
| `p_sysapi1098` | 新股过会 | `sysapi/p_sysapi1098` | `c27434e6d4c048bbaf04acc421fafe5f` |

### 公司治理

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1050` | 资产重组 | `sysapi/p_sysapi1050` | `fa4940f2c1d24bf8978f0b83dee9298b` |
| `p_sysapi1051` | 债务重组 | `sysapi/p_sysapi1051` | `c80d41b6461c445d84e6fc00ef1f22ef` |
| `p_sysapi1052` | 吸收合并 | `sysapi/p_sysapi1052` | `cd26153220594c64a6084bed1cc0d915` |
| `p_sysapi1053` | 股权变更 | `sysapi/p_sysapi1053` | `a46fd7123089462f96bfdc81442bce25` |
| `p_sysapi1054` | 对外担保 | `sysapi/p_sysapi1054` | `19e31288c6644eaeb11476f504e09301` |
| `p_sysapi1055` | 公司诉讼 | `sysapi/p_sysapi1055` | `58578c60916444cbaafe351aa2d371ff` |
| `p_sysapi1093` | 并购重组 | `sysapi/p_sysapi1093` | `a0901f3df14a4f33a6e53df64ae671da` |
| `p_sysapi1094` | 股权质押 | `sysapi/p_sysapi1094` | `5f7a56f60df8475c8457cdddf623f19f` |

### 财务分析

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1041` | 个股主要指标 | `sysapi/p_sysapi1041` | `51e2ad1a3ed6446788f245c78d6e11e2` |
| `p_sysapi1042` | 分地区财务指标 | `sysapi/p_sysapi1042` | `3cecdf45234640ec9720e7aa139f39c9` |
| `p_sysapi1043` | 分行业财务指标 | `sysapi/p_sysapi1043` | `27da2508e0db40d0b9e2672c8a449457` |
| `p_sysapi1044` | 分市场财务指标 | `sysapi/p_sysapi1044` | `d9ba0a1015b04492b1f6b7740355ab87` |
| `p_sysapi1115` | 盈利能力 | `sysapi/p_sysapi1115` | `aa1a9f28c8324bb8b41048fd78e13cbc` |
| `p_sysapi1116` | 运营能力 | `sysapi/p_sysapi1116` | `53852b866dba468892e4ab95de11c88f` |
| `p_sysapi1117` | 成长能力 | `sysapi/p_sysapi1117` | `9219fe432eec442e86ebce1f9f42a4a4` |
| `p_sysapi1118` | 偿债能力 | `sysapi/p_sysapi1118` | `3ebb88b1c9e5494eb4c73bf14d382e2e` |

### 行业分析

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1087` | 行业市盈率 | `sysapi/p_sysapi1087` | `4d7f5b84cd9a498ebc5208f02b038cf6` |

### 评级预测

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1089` | 投资评级 | `sysapi/p_sysapi1089` | `054cb0d30c87435e8dd37c8e0e429abc` |

### 市场交易

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1022` | 大宗交易报表 | `sysapi/p_sysapi1022` | `2f27105bcfa7487ba6d70560dd6fbfd1` |
| `p_sysapi1023` | 融资融券明细 | `sysapi/p_sysapi1023` | `dec022e037f045c484a32347e8ed9f02` |

### 信息提示

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1047` | 股东大会召开情况 | `sysapi/p_sysapi1047` | `befc13dd5fa74dddaf68934c414b1cff` |
| `p_sysapi1048` | 股东大会相关事项变动 | `sysapi/p_sysapi1048` | `07ad2d226fec4365be7c8c3bae7b3829` |
| `p_sysapi1049` | 股东大会议案表 | `sysapi/p_sysapi1049` | `aaf5eae5932d498aa0cf3eff930770c2` |
| `p_sysapi1062` | 市场公开信息汇总 | `sysapi/p_sysapi1062` | `0155851e88514932b46500a30009f217` |
| `p_sysapi1063` | 拟上市公司清单 | `sysapi/p_sysapi1063` | `8247dd4d1ad34db3bf5c39a55873f014` |
| `p_sysapi1064` | 暂停上市公司清单 | `sysapi/p_sysapi1064` | `1365097f6dc84087ae1957edbd1cbd86` |
| `p_sysapi1065` | 终止上市公司清单 | `sysapi/p_sysapi1065` | `e2073480827a43ff8e291aa8e9c80b78` |
| `p_sysapi1119` | 定期报告披露预约时间表 | `sysapi/p_sysapi1119` | `a024077c6afe4d638abce288789ac363` |

### 基金报表

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1111` | 上市基金行情 | `sysapi/p_sysapi1111` | `a8aebc578f62481d8d35dbba66b92675` |
| `p_sysapi1112` | 基金重仓股 | `sysapi/p_sysapi1112` | `96ae45d78e47467d98c93cfed8f6bffb` |
| `p_sysapi1113` | 基金行业配置 | `sysapi/p_sysapi1113` | `a4ef89821c874e85968ec73294df87cf` |
| `p_sysapi1114` | 基金资产配置 | `sysapi/p_sysapi1114` | `36c55c4be8e74ca5b280b7aa13cf2161` |

### 债券报表

#### 债券发行

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1120` | 国债发行 | `sysapi/p_sysapi1120` | `07686917147b428891b7c82bb3bc9425` |
| `p_sysapi1121` | 地方债发行 | `sysapi/p_sysapi1121` | `abef9394a91c4d86bdbf07c60f00297e` |
| `p_sysapi1122` | 企业债发行 | `sysapi/p_sysapi1122` | `4e499a8785d140b8b31e650cc9121631` |
| `p_sysapi1123` | 可转债发行 | `sysapi/p_sysapi1123` | `6f6a7887e42248d69467d57f2228ef50` |
| `p_sysapi1124` | 可转债转股 | `sysapi/p_sysapi1124` | `908968cae4d6463dbc169579353d8316` |

#### 债券基本信息

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

### 证券市值

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_hk4052` | 港股个股市值数据 | `hk/p_hk4052` | `424d55f002854db3802df0170691afdf` |
| `p_oversea8026` | 美股中概股个股市值数据 | `stock/p_oversea8026` | `863f818646be43fe8b8c7b7883604832` |
| `p_stock2401_bse` | 北交所个股市值数据 | `stock/p_stock2401_bse` | `624c7d21ca634140b14e897326feaa9a` |
| `p_stock2541` | 沪深个股市值数据 | `stock/p_stock2541` | `c6b16e2f167f4d818437b5bfba1217ff` |

## 内部服务-服务平台接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_h5dqms` | DQMS沪深北上市公司H5公告 | `info/p_h5dqms` | `f99993cce40a43d9b226bec60def2994` |
| `p_info3068` | 中文摘要表 | `info/p_info3068` | `ca1e3175dcb2470c988aad42ae70cb45` |
| `p_info3090` | p_info3090 | `bigdata/p_info3090` | `ff774acd6eb942d0a78217d630832ad7` |
| `p_pdfdqms` | DQMS公告PDF及H5接口 | `info/p_pdfdqms` | `efaf862af8094222a2e9b1e7fead9e0a` |
| `p_server_topicstatus` | 公告推送数据统计情况 | `sysapi/p_server_topicstatus` | `b4aacfd02c8f484b822502da7599ba8a` |
| `p_stock2118` | AB股代码对应表 | `stock/p_stock2118` | `07d5c459a82a4f8faae2ef4d00a1e803` |

### 公告订制

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3020` | 上市公司智能资讯 | `info/p_info3020` | `5df07791f0fe4411bad81ab37b87b79e` |
| `p_info3021` | 公告摘要分类编码 | `info/p_info3021` | `1f664454f35b4768b6c73343d4575fdc` |
| `p_info3085_client` | 上市公司公告(DataCloud) | `info/p_info3085_client` | `4b4ebc4052274398bbd43840e1f6f77b` |
| `p_sysapi1012` | 港股行业板块成份股 | `sysapi/p_sysapi1012` | `22ae1b2eb382466289c214a8f89a1755` |
| `p_sysapi1016` | 证券标的股查询 | `sysapi/p_sysapi1016` | `294a791c7b794d36bfbcdb3a2a8052da` |
| `p_sysapi1085` | 公告分类信息 | `sysapi/p_sysapi1085` | `b60d8edf350346f0935e05b7175110ea` |
| `p_sysapi1086` | 新三板行业分类成份股 | `sysapi/p_sysapi1086` | `8dbf6891032c465ebad606fa45f5bd6f` |
| `p_sysapi1091` | 公告信息数据 | `sysapi/p_sysapi1091` | `bc18adc0fce4447aab22423302ab38c4` |

### 首页内容

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1022` | 大宗交易报表 | `sysapi/p_sysapi1022` | `2f27105bcfa7487ba6d70560dd6fbfd1` |
| `p_sysapi1023` | 融资融券明细 | `sysapi/p_sysapi1023` | `dec022e037f045c484a32347e8ed9f02` |
| `p_sysapi1025` | 减持明细 | `sysapi/p_sysapi1025` | `6c58758094c94c60848ad8932455e398` |
| `p_sysapi1026` | 增持明细 | `sysapi/p_sysapi1026` | `eff062877e544b7bb7f4932f3d52860b` |
| `p_sysapi1078` | 股票智能摘要 | `sysapi/p_sysapi1078` | `af27590f813d4a4ea67cc5eb62efcdf9` |
| `p_sysapi1079` | 行业市盈率 | `sysapi/p_sysapi1079` | `06f27c9c98ad48a88cd77ed537b23e15` |
| `p_sysapi1080` | 投资评级 | `sysapi/p_sysapi1080` | `93ee6ebd27c34a75bbd47f9ab00cf3cd` |
| `p_sysapi1081` | 预告业绩大幅上升个股 | `sysapi/p_sysapi1081` | `a4c96ccbe7d14e218dfa33e6211ea632` |
| `p_sysapi1082` | 预告业绩大幅下降个股 | `sysapi/p_sysapi1082` | `d4fc1618f19a4c318604fb2ae527131e` |
| `p_sysapi1083` | LOF基金净值增长率 | `sysapi/p_sysapi1083` | `505da5a4406148f096ef3c0e8c055340` |
| `p_sysapi1084` | ETF基金净值增长率 | `sysapi/p_sysapi1084` | `0e0b519e77ac4091ba1a1e8531e8f5fc` |
| `p_sysapi1126` | 基金智能资讯 | `sysapi/p_sysapi1126` | `5efd7a9d7bb345ab88805cab7b3ad8ee` |
| `p_sysapi1127` | 数据智能资讯 | `sysapi/p_sysapi1127` | `8cd2885fdd0d406c8de3ecf999b4b835` |
| `p_sysapi1128` | 最新智能资讯 | `sysapi/p_sysapi1128` | `28ec7a373a8b4242a90fa5b8238a6ccb` |

### 公告定制用户包

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `user_noticemod_ins` | 公告定制插入 | `sysapi/user_noticemod_ins` | `0888ef9a013f419ba038ccd92f79b676` |
| `user_noticemod_sel` | 公告定制查询 | `sysapi/user_noticemod_sel` | `f7842ee41bc947f08d440842cb8c9d78` |

### 小程序接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_sysapi1022` | 大宗交易报表 | `sysapi/p_sysapi1022` | `2f27105bcfa7487ba6d70560dd6fbfd1` |
| `p_sysapi1025` | 减持明细 | `sysapi/p_sysapi1025` | `6c58758094c94c60848ad8932455e398` |
| `p_sysapi1026` | 增持明细 | `sysapi/p_sysapi1026` | `eff062877e544b7bb7f4932f3d52860b` |
| `p_sysapi1039` | 预告业绩大幅下降个股 | `sysapi/p_sysapi1039` | `1219ab371d3346a3b597156e137e92d9` |
| `p_sysapi1040` | 预告业绩大幅上升个股 | `sysapi/p_sysapi1040` | `16de11a7a37742a4bbe53060dd33630f` |
| `p_sysapi1062` | 市场公开信息汇总 | `sysapi/p_sysapi1062` | `0155851e88514932b46500a30009f217` |
| `p_sysapi1079` | 行业市盈率 | `sysapi/p_sysapi1079` | `06f27c9c98ad48a88cd77ed537b23e15` |
| `p_sysapi1089` | 投资评级 | `sysapi/p_sysapi1089` | `054cb0d30c87435e8dd37c8e0e429abc` |
| `p_sysapi1090` | 小程序栏目数据接口 | `sysapi/p_sysapi1090` | `0ef9f6bc59bf475c957371de5919b899` |
| `p_sysapi1093` | 并购重组 | `sysapi/p_sysapi1093` | `a0901f3df14a4f33a6e53df64ae671da` |
| `p_sysapi1094` | 股权质押 | `sysapi/p_sysapi1094` | `5f7a56f60df8475c8457cdddf623f19f` |

### 内部平台使用接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_capitalflow_redis` | p_capitalflow_redis | `stock/p_capitalflow_redis` | `bb89b4e63414431998b90e51c41b3d0e` |
| `p_financinghistory_new` | 融资历史（新） | `bigdata/p_financinghistory_new` | `a891bc8304064fab83f08ae418bfe60d` |
| `p_info3070` | 英文采编-银行间公告 | `info/p_info3070` | `8c46f1ece7824a6d965ba06bee8819c5` |
| `p_sorttable` | DQMS分类维护表 | `info/p_sorttable` | `21a5cdc85d3f458e9d3fc20c3ee8cf3a` |
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
| `p_sysapi1133` | 新f10基本资料 | `sysapi/p_sysapi1133` | `902f9066f79c4d869719dfeeea0bd75a` |
| `p_sysapi1134` | 新F10上市相关 | `sysapi/p_sysapi1134` | `5f17d7689d4c4c38860db90dc30cc4ff` |
| `p_sysapi1135` | 新F10公司高管  | `sysapi/p_sysapi1135` | `545163177d8049cf8257f677f14c2a13` |
| `p_sysapi1137` | 新F10大宗交易 | `sysapi/p_sysapi1137` | `c6dd9ebbbf95420380e1b0c96071be0a` |
| `p_sysapi1138` | 新F10融资融券 | `sysapi/p_sysapi1138` | `41207f07b2214e1fa5677c64c96158d1` |
| `p_sysapi1140` | 新F10-主要财务指标 | `sysapi/p_sysapi1140` | `1849c5edbbde4a08952ccf32b060b111` |
| `p_sysapi1142` | 新F10现金流表表 | `sysapi/p_sysapi1142` | `25fb4b60a9d046a7b6990dc553239719` |
| `p_sysapi1143` | 新F10资产负债表 | `sysapi/p_sysapi1143` | `9e89aa83323c479983408573492a47fe` |
| `p_sysapi1144` | 公司透视-最近五个报告期 | `sysapi/p_sysapi1144` | `3722e6860d8c42a0b50d45bee69d7dec` |

### 上市公司要览-英文黄页

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_snapshot5014` | 每股数据 | `snapshot/p_snapshot5014` | `432eef7d646049b991e0e9399feebcaf` |
| `p_snapshot5015` | 公司基本信息 | `snapshot/p_snapshot5015` | `2972d955276b420ab3b4be57323ba70d` |
| `p_snapshot5016` | 净利润 | `snapshot/p_snapshot5016` | `36c7b57c8db74d61be14e9329ee13082` |
| `p_snapshot5017` | 资产负责表 | `snapshot/p_snapshot5017` | `9073cec42139424c9ef8f062b5f44972` |
| `p_snapshot5018` | 现金流量表 | `snapshot/p_snapshot5018` | `412eb57b01f84d0ba9e6b74d99bc2c88` |
| `p_snapshot5019` | 分红数据 | `snapshot/p_snapshot5019` | `dba47c6403634d278dd5cddaacec34f7` |
| `p_snapshot5020` | 前五大股东 | `snapshot/p_snapshot5020` | `3ca6f68be280464bbf7b2aaaa17ff658` |
| `p_snapshot5022` | 营业收入 | `snapshot/p_snapshot5022` | `ad5724c84cbc4588aac9121477e3f530` |
| `p_snapshot5023` | 亮点风险 | `snapshot/p_snapshot5023` | `b487e2100dc743a0ab0ffe18b91b663e` |
| `p_snapshot5025` | 公司高管 | `snapshot/p_snapshot5025` | `91103812b0b7462f82dcfb529ae57c95` |
| `p_snapshot5026` | 上市公司要览-基本信息确认接口 | `snapshot/p_snapshot5026` | `91fe06aea23d4db395bc1cfe8842770e` |
| `p_snapshot5026_ins` | 上市公司要览-基本信息 | `snapshot/p_snapshot5026_ins` | `5ffa70fa88a14e48ba9d1184846bab7f` |
| `p_snapshot5027` | 上市公司要览-董事及高管接口 | `snapshot/p_snapshot5027` | `f972059d82ec410c9bd7673f052e8682` |
| `p_snapshot5027_ins` | 上市公司要览-董事及高 | `snapshot/p_snapshot5027_ins` | `6990d8e8b93443efb18a67214a5b9167` |
| `p_snapshot5028` | 上市公司要览-前五大股东接口 | `snapshot/p_snapshot5028` | `128c89bb8d0e4f25a8bea495286aceca` |
| `p_snapshot5028_ins` | 上市公司要览-前五大股东 | `snapshot/p_snapshot5028_ins` | `5a5f363d27184e00b4b090b86350224e` |
| `p_snapshot5030` | 上市公司要览-业务概况接口 | `snapshot/p_snapshot5030` | `0fde62e0bf8b401caea01d3b9c7a8aba` |
| `p_snapshot5030_ins` | 上市公司要览-业务概况 | `snapshot/p_snapshot5030_ins` | `59639d55e16140049d9dbbad64d46c6d` |
| `p_snapshot5033` | 上市公司要览-业务亮点接口 | `snapshot/p_snapshot5033` | `bd111ab0a54c4a5798383ee9702adc83` |
| `p_snapshot5033_ins` | 上市公司要览-业务亮点 | `snapshot/p_snapshot5033_ins` | `4a2809f37db64316a6489f7b6b81d5bb` |
| `p_snapshot5034` | 上市公司要览-业务风险接口 | `snapshot/p_snapshot5034` | `bcbd421669a743079ff15d8400c2351b` |
| `p_snapshot5034_ins` | 上市公司要览-业务风险 | `snapshot/p_snapshot5034_ins` | `a9b56c47074f45a79dc9244242d62f8b` |
| `p_snapshot5036` | 上市公司要览-短信提示接口 | `snapshot/p_snapshot5036` | `ff4f9bcef034461491c44791750a7fc8` |
| `p_snapshot5037_ins` | 上市公司要览-提交确认接口 | `snapshot/p_snapshot5037_ins` | `e280fa0f1f2a47ec939b6a0269ac34d0` |
| `p_snapshot5038` | 上市公司要览-邮件提醒接口 | `snapshot/p_snapshot5038` | `dc27fe8d7ae44cfb9d7b43244483560a` |
| `p_snapshot5040` | 上市公司要览-每股数据接口 | `snapshot/p_snapshot5040` | `e9904727181e448bb30485d990ff2607` |
| `p_snapshot5041` | 上市公司要览-净利润接口 | `snapshot/p_snapshot5041` | `94f25c2f2b1645ef8f0c59e907b1c551` |
| `p_snapshot5042` | 上市公司要览-资产负债接口 | `snapshot/p_snapshot5042` | `0e3ba5449a47449fa8e98c7a39379532` |
| `p_snapshot5043` | 上市公司要览-现金流量接口 | `snapshot/p_snapshot5043` | `622b5babed574987be8d1f10648c5a65` |
| `p_snapshot5044` | 上市公司要览-分红数据接口 | `snapshot/p_snapshot5044` | `9e6ed132f3754ecd804f10675ca48b11` |
| `p_snapshot5045` | 上市公司要览-营业收入接口 | `snapshot/p_snapshot5045` | `818a2691777a4b4dbdda81f8d707f546` |
| `p_snapshot5046` | 上市公司要览-通用财务营业成本营业收入修改接口 | `snapshot/p_snapshot5046` | `fd6e97c2c2cc47708c8476f6383e134c` |
| `p_snapshot5047` | 上市公司要览-营业收入修改接口 | `snapshot/p_snapshot5047` | `83dc4745aee04932931405a9bd7928a0` |

### 大数据接口

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_abnormal_enterprises` | p_abnormal_enterprises | `bigdata/p_abnormal_enterprises` | `fd0bfa6e6bc9460ca6a25dc6981460a9` |
| `p_auctions_relations` | p_auctions_relations | `bigdata/p_auctions_relations` | `0010660f38ef4d29ab7d2b98b3407bf3` |
| `p_biddings_all` | p_biddings_all | `bigdata/p_biddings_all` | `1be99a9bd6df463685371659a1fa8f91` |
| `p_bond_info` | p_bond_info | `bigdata/p_bond_info` | `c7a0702e23b84f4b8ec8d9c313377934` |
| `p_creditimportexport_data` | p_creditimportexport_data | `bigdata/p_creditimportexport_data` | `bc1bf90b1dbb4400bddbda7da5dd09b3` |
| `p_engineer_abnormal` | p_engineer_abnormal | `bigdata/p_engineer_abnormal` | `2263bc4bc5054242883329d96ddc6590` |
| `p_general_taxpayer` | p_general_taxpayer | `bigdata/p_general_taxpayer` | `00cdca8f583f4b609f69920c061e0da5` |
| `p_goudi_information` | p_goudi_information | `bigdata/p_goudi_information` | `b98b4dca20664986b3698fb6374ee0e6` |
| `p_graph_actualcontrollers` | 疑似实际控制人 | `bigdata/p_graph_actualcontrollers` | `4b4dfef11acf4058900d735646c48501` |
| `p_graph_neighbor` | 公司搜索和人物搜索 | `bigdata/p_graph_neighbor` | `a58a9502e42a416494d714f82da30d99` |
| `p_graph_penetration` | 股权穿透 | `bigdata/p_graph_penetration` | `10091bb464984c76ad3b97a834d87179` |
| `p_graph_relatedparty` | 法定关联方 | `bigdata/p_graph_relatedparty` | `afd5b2515b154a0080b986388ccbeb08` |
| `p_graph_relatedrelations` | 关联关系 | `bigdata/p_graph_relatedrelations` | `b60cf8a920e043f481f9bd9c4f1e9f79` |
| `p_graph_v2` | 图谱接口（使用url传参） | `bigdata/p_graph_v2` | `8f3618b2c6d0498aadccb897281843e8` |
| `p_huanbaochufas` | p_huanbaochufas | `bigdata/p_huanbaochufas` | `5ba6d82444ce400399089a6c802b6a2b` |
| `p_managers` | 公司高管 | `bigdata/p_managers` | `ddf1a002afd242438fedb028ac220d2d` |
| `p_pay_taxes` | p_pay_taxes | `bigdata/p_pay_taxes` | `df9ddad5152241d4b11c3482401826f1` |
| `p_prompt` | 搜索提示 | `bigdata/p_prompt` | `ad46891157fb46ea9add84bf7d1f38d2` |
| `p_search_other` | id获取 | `bigdata/p_search_other` | `da1b3b84a84e4c95a3e10ada5b05fe08` |

### 科金内容

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_financinghistory_new` | 融资历史（新） | `bigdata/p_financinghistory_new` | `a891bc8304064fab83f08ae418bfe60d` |
| `p_holders` | 工商股东 | `bigdata/p_holders` | `93dba9d4db114d57ae79cbd917ad61ae` |
| `p_info` | 公司详情 | `bigdata/p_info` | `40f1d6ab5bf7423cb9d3763a0751933b` |
| `p_prompt_kejin` | p_prompt_kejin | `bigdata/p_prompt_kejin` | `dcda8707fa7c4518a947262b76210bcf` |
| `p_search` | 搜索 | `bigdata/p_search` | `98f8a12a88f24a65a3043cf1babc701f` |
| `p_stock2119` | 人民币汇率中间价表 | `stock/p_stock2119` | `35f74930d3b1481790a467a8e7a8f2ca` |
| `p_youqicha_score` | 优企查评分查询 | `bigdata/p_youqicha_score` | `e4256ae68a3542d191a5b804558a505b` |

### 科技一部

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_bond2916` | 发行人基本信息 | `bond/p_bond2916` | `932b31d4f8c7475eb6699c4fa665d604` |
| `p_bond2917` | 债券基本信息 | `bond/p_bond2917` | `0e7b3096645e4446bd11fb75a15b1661` |

### 上交所数据互换

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3830` | 深证公告互换数据 | `info/p_info3830` | `6bf8a49785af4d62a6925cde035ac2c4` |
| `p_info3831` | 深证公告更新信息 | `info/p_info3831` | `0abeac50ebf14f07b1c43e1f1b8a13b8` |
| `p_stock2201_sz` | 分红转增信息 | `stock/p_stock2201_sz` | `7c135481ae734f6f8022397641ce0bb1` |
| `p_trade2715` | 停复牌互换数据 | `stock/p_trade2715` | `6edc0873e54f49dd875232b069e03bef` |

## 巨潮网使用接口

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

### IPO可视化

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_cninfo5048` | IPO公司情况列表 | `cninfo/p_cninfo5048` | `4b5455c928484b0d9a8d2ae6c025e926` |
| `p_cninfo5049` | IPO创业板上市进展 | `cninfo/p_cninfo5049` | `05f1bceb4a5b4910ab90d1261b8c7e84` |
| `p_cninfo5050` | IPO主要股东 | `cninfo/p_cninfo5050` | `729adc67cc034257bd6385e635cabbfd` |
| `p_cninfo5051` | IPO实际控制人 | `cninfo/p_cninfo5051` | `a16f986aa58d45c690790ddb2aab4582` |
| `p_cninfo5052` | IPO核心技术及研发技术人员 | `cninfo/p_cninfo5052` | `9496acba3f81464c9ac3b489f758f6f1` |
| `p_cninfo5053` | IPO主要竞争对手 | `cninfo/p_cninfo5053` | `63e07f6b45ef4bb4923e9dafc4b21678` |
| `p_cninfo5054` | IPO前5大供应商占比情况 | `cninfo/p_cninfo5054` | `da1607e35f694c11a214005e78f3d24a` |
| `p_cninfo5055` | IPO前5大客户占比情况 | `cninfo/p_cninfo5055` | `35ba3907674d493080e82bd27a665a78` |

### 成长通

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ESG8701` | 二级行业评级分布 | `stock/p_ESG8701` | `0c0aabcf75264978b87120cc0511ac17` |
| `p_ESG8702` | 深沪市场评级分布 | `stock/p_ESG8702` | `a65369742ba546f9972f7620f43b68fb` |
| `p_ESG8703` | ESG细项评分 | `stock/p_ESG8703` | `e96ed46b0432426482ba04e206a8614f` |
| `p_ESG8704` | 上市公司ESG综合评分 | `stock/p_ESG8704` | `6cd7ec5a07c24807af4dc5efa8e4ee2b` |
| `p_ESGCODE` | ESG键盘精灵订制接口 | `stock/p_ESGCODE` | `6df5084746f1430c9f0dd00dfc344818` |
| `p_cninfo5067` | ESG指数信息视图 | `cninfo/p_cninfo5067` | `0143bfbde7ca4a6a95b40dca4ebbd0aa` |

### 巨潮专用

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
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

## 第三方数据

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `company_info` | 按机构ID查询合规数据 | `/simuwang/company_info` | `2a73d195e89a4eff8306d6c8fbe34cfc` |
| `fund_base_info` | 查询基金的基本信息 | `/simuwang/fund_base_info` | `cd52589c3741472e838277e1b74f00a8` |
| `fund_nav` | 获取指定基金的净值等信息 | `/simuwang/fund_nav` | `e6aee513bcd94ec2a80d4f8858b62091` |
| `query_dictionary_item` | 查询字典树中指定itemCode的意义 | `/simuwang/query_dictionary_item` | `0edb10dc22b54e30a35f5a55dd5033f0` |
| `request_count` | 查询最近N天内的请求调用量 | `/simuwang/request_count` | `e0f809a471294cab99d531dfda6db721` |
| `seach_fund` | 按关键字搜索基金信息 | `/simuwang/seach_fund` | `5b74447009a64cb2a85974a47cb60ac0` |
| `search_company` | 根据输入的name模糊查询所有匹配的机构ID | `/simuwang/search_company` | `16be1908df994b1081b21493096675f3` |

## 小巨人

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_listed_zjtx` | 深沪北上市公司是否专精特新 | `bigdata/p_listed_zjtx` | `9fa880707fcf45368265b2253450eb53` |
| `p_listed_zjtx_customer_supplier` | 上市公司和专精特新公司的客户供应商关系 | `bigdata/p_listed_zjtx_customer_supplier` | `954c1026c20d48d28ff334479902a3cc` |
| `p_listed_zjtx_holder` | 专精特新与上市公司股东关系 | `bigdata/p_listed_zjtx_holder` | `060349bcbb1c42eaaaa8a610638976dd` |

## 产业链数据服务

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_ods3303` | 行业上下游接口 | `bigdata/p_ods3303` | `4ecbac39a3654eb294a97a0227e03b0a` |
| `p_ods3304` | 上市公司主营行业数据 | `bigdata/p_ods3304` | `c8d2047806a64b0a85784e54ae8d8d0f` |
| `p_ods3305` | 行业码表 | `bigdata/p_ods3305` | `33e18c350fe94623b47610cd0f9de26b` |
| `p_ods3306` | 典型公司和可比公司 | `bigdata/p_ods3306` | `6b4a0d8e636e435c8310510444b23c2e` |

## 上市公司官网嵌入服务

### 300450

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3024_0470` | 港股中英文公告 | `info/p_info3024_0470` | `cbc4244a42344b4281ba2b20e01fd930` |
| `p_info3085_300450` | 先导智能公司公告 | `info/p_info3085_300450` | `9ee8963c7efb4101912e8b7922c1ad84` |
| `p_info3139_300450` | 先导智能公司互动信息 | `info/p_info3139_300450` | `4d0f48f63d63456c8e0766af420673d0` |

### 300015

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3015_300015` | 公告基本信息 | `info/p_info3015_300015` | `926acf0c53a74725805926cac0ba72cf` |
| `p_info3085_300015` | 爱尔眼科公司公告 | `info/p_info3085_300015` | `ed2c1da0c3af475da4ad320f477431e4` |
| `p_info3097_300015` | 爱尔眼科个股研报摘要 | `info/p_info3097_300015` | `c71bcd966e954f79a622d0b27ac2d9b4` |
| `p_info3139_300015` | 爱尔眼科互动信息明细 | `info/p_info3139_300015` | `bb70c7d7a3b34f33af53956b537ec6c1` |
| `p_stock2100_300015` | 爱尔眼科公司基本信息 | `stock/p_stock2100_300015` | `57c73dbfa1ce42beaebe0571f80c504e` |
| `p_stock2201_300015` | 爱尔眼科分红转增信息 | `stock/p_stock2201_300015` | `15e036661c144970a4fa4f019176ae69` |
| `p_stock2300_300015` | 爱尔眼科资产负债表 | `stock/p_stock2300_300015` | `2c76b529764a4b23aa39bc76fc7aec24` |
| `p_stock2301_300015` | 爱尔眼科个股报告期利润表 | `stock/p_stock2301_300015` | `be0a5852806b4c938f1fa5a6b909b1f7` |
| `p_stock2302_300015` | 爱尔眼科个股报告期现金表 | `stock/p_stock2302_300015` | `c2a1413f865d43d6b3cf243181155ea2` |
| `p_stock2303_300015` | 个股报告期指标表 | `stock/p_stock2303_300015` | `2233cf0b9ff54f049c617e7a7679c2f3` |
| `p_stock2402_300015` | 爱尔眼科历史日行情 | `stock/p_stock2402_300015` | `4e1df10a12fb4fcaa47a24c2195236d0` |

### 000600

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3085_000600` | 建投能源公司公告 | `info/p_info3085_000600` | `2a2b03ed283f4c08939807d94f87648b` |

### 03200

| 接口名 | 中文名 | 请求路径 | gatewayCode |
|--------|--------|----------|-------------|
| `p_info3024_3200` | 港股中英文公告 | `info/p_info3024_3200` | `df4e37c1d107482db75c9ad7e8ec8cd6` |
| `p_info3085_301200` | 大族数控公司公告 | `info/p_info3085_301200` | `ad3511546ba241fcaf99fd7f937ae49f` |

