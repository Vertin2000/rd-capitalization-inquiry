"""Convert cninfo_official_api_catalog.json to a hierarchical Markdown catalog.

The JSON catalog stores each API's category path as a list of headings. This
script maps that path directly to Markdown heading levels and lists the APIs
under their leaf category as a table.
"""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(r'c:\Users\Vertin2000\上经贸大\数据挖掘与机器学习\project2')
CATALOG_PATH = PROJECT_ROOT / 'docs' / 'cninfo_official_api_catalog.json'
MD_PATH = PROJECT_ROOT / 'docs' / 'cninfo_official_api_catalog.md'


def _escape_pipe(text: str) -> str:
    """Escape pipe characters so they do not break Markdown tables."""
    return text.replace('|', '\\|')


def _insert_api(tree: dict, api: dict) -> None:
    """Insert an API into the category tree based on its categoryPath."""
    path = api.get('categoryPath') or []
    node = tree
    current_node = None
    for segment in path:
        if segment not in node:
            node[segment] = {'_apis': [], '_children': {}}
        current_node = node[segment]
        node = current_node['_children']
    if current_node is not None:
        current_node['_apis'].append(api)


def _build_tree(apis: list[dict]) -> dict:
    """Build a nested tree from the flat API list."""
    tree: dict = {}
    for api in apis:
        _insert_api(tree, api)
    return tree


def _render_category(
    name: str,
    node: dict,
    depth: int,
    lines: list[str],
    path: tuple[str, ...],
    cat_meta: dict[tuple[str, ...], dict],
) -> None:
    """Render one category node and its children recursively."""
    heading = '#' * depth
    lines.append(f'{heading} {_escape_pipe(name)}')
    lines.append('')

    apis = sorted(node.get('_apis', []), key=lambda a: a.get('name', ''))
    if apis:
        lines.append('| 接口名 | 中文名 | 请求路径 | gatewayCode |')
        lines.append('|--------|--------|----------|-------------|')
        for api in apis:
            lines.append(
                f"| `{api.get('name', '')}` | "
                f"{_escape_pipe(api.get('alias') or '')} | "
                f"`{api.get('requestPath', '')}` | "
                f"`{api.get('code', '')}` |"
            )
        lines.append('')

    children = node.get('_children', {})

    def _child_sort_key(child_name: str) -> tuple:
        meta = cat_meta.get(path + (child_name,), {})
        return (
            meta.get('sort') if meta.get('sort') is not None else 10**9,
            child_name,
        )

    for child_name in sorted(children.keys(), key=_child_sort_key):
        _render_category(
            child_name,
            children[child_name],
            depth + 1,
            lines,
            path + (child_name,),
            cat_meta,
        )


def generate_markdown(catalog: dict) -> str:
    """Generate the full Markdown catalog from the parsed catalog dict."""
    meta = catalog['metadata']
    categories = catalog.get('categories', [])

    # Build a lookup from category path -> metadata (display / sort).
    cat_meta: dict[tuple[str, ...], dict] = {
        tuple(node.get('path', [])): {
            'display': node.get('display'),
            'sort': node.get('sort'),
        }
        for node in catalog.get('categoryNodes', [])
    }

    def _top_sort_key(cat: dict) -> tuple:
        meta_info = cat_meta.get((cat['name'],), {})
        return (
            -(meta_info.get('display') or 0),
            meta_info.get('sort') if meta_info.get('sort') is not None else 10**9,
            cat['name'],
        )

    # Visible categories (display == 1) first, then hidden ones.
    # Within each group, follow the website's original sort order.
    sorted_categories = sorted(categories, key=_top_sort_key)
    top_order = [cat['name'] for cat in sorted_categories]
    tree = _build_tree(catalog.get('apis', []))

    lines = [
        '# 深证信（巨潮）官方 API 目录（全量）',
        '',
        f"> 来源：[{meta['source']}]({meta['source']})",
        f"> 提取时间：{meta['extractedAt']}",
        f"> 全量接口数：{meta['totalApis']}",
        f"> 一级类目数：{meta['totalCategories']}",
        f"> 与研究相关接口数：{meta.get('relevantApis', 'N/A')}",
        '>',
        '> 注：本目录包含网页左侧未显示的隐藏类目（`display: 0`）。'
        '类目顺序与网页左侧目录树一致：可见类目在前，隐藏类目在后。',
        '',
        '## 一级类目概览',
        '',
        '| 一级类目 | 接口数 | 可见性 |',
        '|----------|--------|--------|',
    ]

    for cat in sorted_categories:
        visibility = '可见' if cat.get('display') else '隐藏'
        lines.append(f"| {cat['name']} | {cat['apiCount']} | {visibility} |")
    lines.append('')

    # Render top-level categories in website order.
    for top_name in top_order:
        if top_name in tree:
            _render_category(
                top_name, tree[top_name], depth=2,
                lines=lines, path=(top_name,), cat_meta=cat_meta,
            )

    return '\n'.join(lines) + '\n'


def main() -> None:
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    markdown = generate_markdown(catalog)

    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MD_PATH, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f'Wrote {MD_PATH} ({len(markdown):,} characters, '
          f'{len(catalog.get("apis", []))} APIs)')


if __name__ == '__main__':
    main()
