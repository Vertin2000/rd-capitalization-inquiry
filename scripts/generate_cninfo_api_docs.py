"""Generate official CNINFO API catalog and reference docs from apiDocTree."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(r'c:\Users\Vertin2000\上经贸大\数据挖掘与机器学习\project2')
TREE_PATH = PROJECT_ROOT / 'cninfo_api_doc_tree.json'
CATALOG_PATH = PROJECT_ROOT / 'docs' / 'cninfo_official_api_catalog.json'
REF_PATH = PROJECT_ROOT / 'docs' / 'cninfo_official_api_reference.md'

# Categories most relevant to R&D capitalization / annual report / announcement / inquiry research
RELEVANT_CATEGORIES = {
    '公告资讯',
    '巨潮网使用接口',
    '证券提示库数据服务',
    '公司数据',
    '公共信息',
    '新闻研报',
}


def walk(n: dict, path_names: list[str] | None = None):
    if path_names is None:
        path_names = []
    children = n.get('children') or []
    apis = n.get('apiList') or []
    name = n.get('name') or n.get('alias') or '(unnamed)'
    full_path = path_names + [name]
    node_type = n.get('type')
    if node_type == 1:
        # Category node
        yield {
            'kind': 'category',
            'name': n.get('name'),
            'alias': n.get('alias'),
            'code': n.get('code'),
            'display': n.get('display'),
            'sort': n.get('sort'),
            'categoryPath': full_path[1:],
            'topCategory': full_path[1] if len(full_path) > 1 else '',
        }
    elif node_type == 0 or (not children and not apis):
        # API node (or stray leaf)
        yield {
            'kind': 'api',
            'name': n.get('name'),
            'alias': n.get('alias'),
            'code': n.get('code'),
            'requestPath': n.get('requestPath'),
            'categoryPath': full_path[1:-1],
            'topCategory': full_path[1] if len(full_path) > 1 else '',
        }
    for c in children + apis:
        yield from walk(c, full_path)


def generate_catalog(tree: dict) -> dict:
    entries = list(walk(tree))
    apis = [e for e in entries if e.get('kind') == 'api']
    categories_entries = [e for e in entries if e.get('kind') == 'category']

    # Map category path -> metadata (display / sort)
    category_meta = {
        tuple(cat['categoryPath']): {
            'display': cat.get('display'),
            'sort': cat.get('sort'),
        }
        for cat in categories_entries
    }

    by_top = defaultdict(list)
    for api in apis:
        by_top[api['topCategory']].append(api)

    def _cat_sort_key(cat_name: str) -> tuple:
        meta = category_meta.get((cat_name,), {})
        # Visible first, then by website sort order, then by name.
        return (-(meta.get('display') or 0), meta.get('sort') or 10**9, cat_name)

    categories = [
        {
            'name': cat,
            'apiCount': len(items),
            'display': category_meta.get((cat,), {}).get('display'),
            'sort': category_meta.get((cat,), {}).get('sort'),
            'subPaths': sorted({tuple(api['categoryPath']) for api in items}),
        }
        for cat, items in sorted(by_top.items(), key=lambda x: _cat_sort_key(x[0]))
    ]

    relevant_apis = [api for api in apis if api['topCategory'] in RELEVANT_CATEGORIES]

    return {
        'metadata': {
            'source': 'https://webapi.cninfo.com.cn/#/apiDoc',
            'extractedAt': datetime.now(timezone.utc).isoformat(),
            'totalApis': len(apis),
            'totalCategories': len(categories),
            'relevantCategories': sorted(RELEVANT_CATEGORIES),
            'relevantApis': len(relevant_apis),
        },
        'categories': categories,
        'categoryNodes': [
            {
                'path': cat['categoryPath'],
                'display': cat.get('display'),
                'sort': cat.get('sort'),
            }
            for cat in categories_entries
        ],
        'apis': apis,
        'relevantApis': relevant_apis,
    }


def generate_reference(catalog: dict) -> str:
    meta = catalog['metadata']
    lines = [
        '# 深证信（巨潮）官方 API 文档本地参考',
        '',
        '> 来源：[https://webapi.cninfo.com.cn/#/apiDoc](https://webapi.cninfo.com.cn/#/apiDoc)',
        f'> 提取时间：{meta["extractedAt"]}',
        f'> 全量接口数：{meta["totalApis"]}',
        f'> 与研究相关接口数：{meta["relevantApis"]}',
        '',
        '## 1. 关键结论',
        '',
        '- 官方 API 文档树通过前端脚本 `/js/apiDocTree.js` 暴露，整棵树已导出为 `cninfo_api_doc_tree.json`。',
        '- 每个接口的元数据可通过公开接口 `GET /api-cloud-gateway-manage/apiDoc/info?gatewayCode=<uuid>` 获取，无需登录。',
        '- **接口文档是公开的，但实际数据接口需要授权**。直接请求数据端点（如 `http://webapi.cninfo.com.cn/api/cninfo/p_cninfo5001`）会返回 `401 未经授权的访问`。',
        '- 因此 crawler 重构建议采用 **Plan A**：数据仍走公开前端接口 `www.cninfo.com.cn/new/hisAnnouncement/query`，本官方文档仅用于校准参数、字段语义和输出结构。',
        '',
        '## 2. 目录结构',
        '',
        '| 一级类目 | 接口数 | 说明 |',
        '|----------|--------|------|',
    ]
    for cat in catalog['categories']:
        note = ''
        if cat['name'] in RELEVANT_CATEGORIES:
            note = '（与研究相关）'
        lines.append(f"| {cat['name']} | {cat['apiCount']} | {note} |")

    lines.extend([
        '',
        '## 3. 与研究相关的重点类目',
        '',
    ])

    relevant_by_top: dict[str, list[dict]] = defaultdict(list)
    for api in catalog['relevantApis']:
        relevant_by_top[api['topCategory']].append(api)

    for idx, cat in enumerate(sorted(relevant_by_top.keys(), key=lambda c: -len(relevant_by_top[c])), start=1):
        apis = relevant_by_top[cat]
        lines.extend([
            f"### 3.{idx} {cat}（{len(apis)} 个接口）",
            '',
            '| 接口名 | 中文名 | 请求路径 | gatewayCode |',
            '|--------|--------|----------|-------------|',
        ])
        for api in apis:
            lines.append(
                f"| `{api['name']}` | {api['alias']} | `{api['requestPath']}` | `{api['code']}` |"
            )
        lines.append('')

    lines.extend([
        '## 4. 典型接口元数据示例',
        '',
        '### 4.1 p_cninfo5001 — 定期报告披露事件',
        '',
        '```json',
        json.dumps(fetch_info('a2eac0ef2ed14b0bb71dccf4f630f8da'), ensure_ascii=False, indent=2),
        '```',
        '',
        '### 4.2 p_public0001 — 交易日历数据',
        '',
        '```json',
        json.dumps(fetch_info('0bf76273eb724e38bf32c30cfac5ddda'), ensure_ascii=False, indent=2),
        '```',
        '',
        '## 5. crawler 重构建议',
        '',
        '1. **保留现有公开接口**：`hisAnnouncement/query` 仍是获取公告列表和 PDF 链接的主力接口。',
        '2. **用官方文档校准字段**：本参考文档中的 `p_cninfo5001`/`p_cninfo5002` 等接口参数可与现有 crawler 参数互相对照，避免传错字段名或日期格式。',
        '3. **不尝试绕过官方认证**：官方数据端点 401 说明存在 token/授权机制，项目规则不允许绕过登录，因此不纳入爬取方案。',
        '',
        '## 6. 文件索引',
        '',
        '- `cninfo_api_doc_tree.json`：原始完整文档树（raw，已加入 `.gitignore`）。',
        '- `cninfo_api_gateway_codes.json`：全部 2465 个接口的 `gatewayCode` 索引（raw，已加入 `.gitignore`）。',
        '- `docs/cninfo_official_api_catalog.json`：机器可读的全量目录与相关接口子集。',
        '- `docs/cninfo_official_api_reference.md`：本 human-readable 参考文档。',
    ])

    return '\n'.join(lines) + '\n'


def fetch_info(gateway_code: str) -> dict:
    """Return a trimmed info payload for examples."""
    import requests
    url = 'https://webapi.cninfo.com.cn/api-cloud-gateway-manage/apiDoc/info'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://webapi.cninfo.com.cn/',
    }
    resp = requests.get(url, params={'gatewayCode': gateway_code}, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()['data']
    # Trim verbose examples but keep structure
    for param in data.get('requestConfig', {}).get('inputParameter', []):
        if isinstance(param, dict):
            param.pop('example', None)
    for param in data.get('resultContent', {}).get('outputParameter', []):
        if isinstance(param, dict):
            param.pop('example', None)
    return data


def main() -> None:
    with open(TREE_PATH, 'r', encoding='utf-8') as f:
        tree = json.load(f)

    catalog = generate_catalog(tree)
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f'Wrote {CATALOG_PATH}')

    reference = generate_reference(catalog)
    with open(REF_PATH, 'w', encoding='utf-8') as f:
        f.write(reference)
    print(f'Wrote {REF_PATH}')


if __name__ == '__main__':
    main()
