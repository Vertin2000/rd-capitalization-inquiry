"""Build clean MD reference from defuddle-extracted content.

Reads docs/mineru_api_docs_extracted.md (defuddle output) and builds a
polished, project-context-aware API reference at docs/mineru_api_reference.md.

Usage:
    python scripts/build_mineru_md.py
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def clean_content(text: str) -> str:
    """Clean up defuddle-extracted text."""
    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def build_final_md(body: str) -> str:
    """Build the final structured MD document."""

    archive_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    frontmatter = f"""# MinerU API 参考文档

> **来源**: [https://mineru.net/apiManage/docs](https://mineru.net/apiManage/docs)
> **存档时间**: {archive_date}
> **抓取工具**: [defuddle](https://github.com/kepano/defuddle)（干净提取，去除导航与广告）
> **原始 HTML**: `docs/mineru_api_docs.html`（2.2 MB，完整保留供比对）
> **补充参考**: [MinerU GitHub — 输出文件说明](https://github.com/opendatalab/MinerU/blob/master/docs/zh/reference/output_files.md)
>
> ⚠️ 本文档为离线存档，方便 AI 与开发者查阅。如官网有更新，以官网为准。

---

## 目录

- [1. 快速概览](#1-快速概览)
  - [1.1 两种 API 模式对比](#11-两种-api-模式对比)
  - [1.2 本项目使用场景](#12-本项目使用场景)
- [2. 认证与通用规范](#2-认证与通用规范)
- [3. 精准解析 API](#3-精准解析-api)
  - [3.1 文件限制](#31-文件限制)
  - [3.2 创建解析任务（POST /api/v4/extract/task）](#32-创建解析任务post-apiv4extracttask)
  - [3.3 获取任务结果（GET /api/v4/extract/task/{{task_id}}）](#33-获取任务结果get-apiv4extracttasktask_id)
  - [3.4 批量文件解析](#34-批量文件解析)
    - [3.4.1 本地文件批量上传（POST /api/v4/file-urls/batch）](#341-本地文件批量上传post-apiv4file-urlsbatch)
    - [3.4.2 URL 批量上传（POST /api/v4/file-urls/batch）](#342-url-批量上传post-apiv4file-urlsbatch)
    - [3.4.3 批量获取任务结果（GET /api/v4/extract-results/batch/{{batch_id}}）](#343-批量获取任务结果get-apiv4extract-resultsbatchbatch_id)
  - [3.5 常见错误码](#35-常见错误码)
- [4. Agent 轻量解析 API](#4-agent-轻量解析-api)
  - [4.1 文件限制](#41-文件限制)
  - [4.2 URL 解析接口（POST /api/v1/agent/parse/url）](#42-url-解析接口post-apiv1agentparseurl)
  - [4.3 本地文件上传接口（签名上传）（POST /api/v1/agent/parse/file）](#43-本地文件上传接口签名上传post-apiv1agentparsefile)
  - [4.4 查询解析结果（GET /api/v1/agent/parse/{{task_id}}）](#44-查询解析结果get-apiv1agentparsetask_id)
  - [4.5 完整使用示例（Python）](#45-完整使用示例python)
  - [4.6 Agent 专属错误码](#46-agent-专属错误码)
- [5. language 取值参考](#5-language-取值参考)
- [附录 A：解析输出文件说明](#附录-a解析输出文件说明)
- [附录 B：与项目代码的对应关系](#附录-b与项目代码的对应关系)

---

"""

    context_section = """
## 1. 快速概览

MinerU 提供两种文档解析 API，满足不同场景需求：

- 🎯 **精准解析 API** — 需填写 Token（API 管理页面自定创建），支持单文件/批量、表格/公式/多格式输出
- ⚡ **Agent 轻量解析 API** — 免登录，IP 限频防滥用，专为 AI Agent 工作流设计

### 1.1 两种 API 模式对比

| 对比维度 | 🎯 精准解析 API | ⚡ Agent 轻量解析 API |
| --- | --- | --- |
| 是否需要 Token | ✅ 需要 | ❌ 无需（IP 限频） |
| 接口地址 | `/api/v4/extract/task` 或 `/api/v4/file-urls/batch` | `/api/v1/agent/parse/url` 或 `/api/v1/agent/parse/file` |
| 模型版本 | `pipeline`（默认）/ `vlm`（推荐）/ `MinerU-HTML` | 固定 pipeline 轻量模型 |
| 文件大小限制 | ≤ 200 MB | ≤ 10 MB |
| 页数限制 | ≤ 200 页 | ≤ 20 页 |
| 批量支持 | ✅ 支持（≤ 200 个） | ❌ 单文件 |
| 输出格式 | Zip 包（含 Markdown、JSON），可额外导出 docx/html/latex | 仅 Markdown（CDN 链接） |
| 调用方式 | 异步（提交 → 轮询） | 异步（提交 → 轮询） |

### 1.2 本项目使用场景

本项目（巨潮资讯网公告 PDF 结构化抽取）的场景参数：

| 参数 | 实际情况 | 推荐 API |
|------|---------|---------|
| 文件数量 | 约 150 份年报 PDF | 批量上传或本地 CLI |
| 单文件大小 | 4–10 MB | ✅ 在 200 MB 限制内 |
| 单文件页数 | 100–300 页 | ⚠️ 部分可能超出 200 页限制，需拆分或分页处理 |
| 输出需求 | Markdown 正文 + 表格数据 | 精准解析 API（vlm 模型） |
| 网络环境 | 国内 | ✅ 国内 URL 优先，避免 GitHub/AWS 等国外源 |

> 💡 **当前实现**: 项目使用 **本地 MinerU CLI 模式**（`mineru -p <pdf> -o <output> -b pipeline`），无需 API Key，直接调用本地 GPU。如需切换到云端 API 模式，请参阅 [附录 B](#附录-b与项目代码的对应关系)。

---

## 2. 认证与通用规范

所有需要 Token 的接口，Header 中携带：

```http
Authorization: Bearer {{MINERU_API_KEY}}
Content-Type: application/json
```

Token 在 [API 管理页面](https://mineru.net/apiManage/token) 自定创建。存储于 `.env` 文件的 `MINERU_API_KEY`。

通用响应格式：

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 接口状态码，成功：0 |
| `msg` | string | 接口处理信息，成功："ok" |
| `trace_id` | string | 请求 ID，用于问题排查 |
| `data` | object | 业务数据，结构因接口而异 |

任务状态说明：

| 状态 | 说明 |
|------|------|
| `done` | 解析完成 |
| `pending` | 排队中 |
| `running` | 正在解析 |
| `failed` | 解析失败 |
| `waiting-file` | 等待文件上传（仅文件上传模式） |
| `converting` | 格式转换中 |

---

"""

    # ------------------------------------------------------------------
    # Process body: restructure headings to match our numbering scheme
    # ------------------------------------------------------------------

    lines = body.split("\n")

    # Cut away everything before the first "## 概述" (our context_section already
    # provides the quick overview and comparison table).
    cut_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "## 概述":
            cut_idx = i
            break
    body = "\n".join(lines[cut_idx:])

    # 1. Precise API section ------------------------------------------------
    body = body.replace(
        "## 概述\n\nMinerU 的精准解析 API",
        "## 3. 精准解析 API\n\nMinerU 的精准解析 API",
        1,  # only the first occurrence
    )
    body = body.replace("## 1.单个文件解析", "### 3.1 单个文件解析")
    body = body.replace("### 创建解析任务", "#### 创建解析任务")
    body = body.replace("### 获取任务结果", "#### 获取任务结果")
    body = body.replace("## 2.批量文件解析", "### 3.2 批量文件解析")
    body = body.replace("### 本地文件批量上传解析", "#### 本地文件批量上传解析")
    body = body.replace("### url 批量上传解析", "#### URL 批量上传解析")
    body = body.replace("### 批量获取任务结果", "#### 批量获取任务结果")
    body = body.replace("### 常见错误码", "### 3.3 常见错误码")

    # 2. Strip the Agent emoji heading + its callout box
    body = re.sub(
        r"## ⚡ Agent 轻量解析 API\n\n> [^\n]+\n\n",
        "",
        body,
    )

    # 3. Agent API section --------------------------------------------------
    body = body.replace(
        "## 概述\n\nAgent 轻量解析接口",
        "## 4. Agent 轻量解析 API\n\n### 4.1 概述\n\nAgent 轻量解析接口",
        1,
    )
    # Note: the source uses escaped dots (\.) in some headings
    body = body.replace("## 1\\. URL 解析接口", "### 4.2 URL 解析接口")
    body = body.replace(
        "## 2\\. 本地文件上传接口（签名上传）", "### 4.3 本地文件上传接口（签名上传）"
    )
    body = body.replace("## 3\\. 查询解析结果", "### 4.4 查询解析结果")
    body = body.replace("## 完整使用示例（Python）", "### 4.5 完整使用示例（Python）")
    body = body.replace("## Agent 专属错误码", "### 4.6 Agent 专属错误码")
    body = body.replace("## language 取值参考", "## 5. language 取值参考")

    # ------------------------------------------------------------------
    # Appendices
    # ------------------------------------------------------------------

    appendix_a = """

---

## 附录 A：解析输出文件说明

> 详细说明请参阅 MinerU 官方文档：[输出文件说明](https://github.com/opendatalab/MinerU/blob/master/docs/zh/reference/output_files.md)

### A.1 Zip 包内容（精准解析 API）

解析完成后，从 `full_zip_url` 下载的 Zip 包包含以下文件：

| 文件 | 说明 |
|------|------|
| `full.md` | **主产物**：Markdown 格式的解析结果，含文本、表格、公式、图片引用 |
| `middle.json` | 中间处理结果，包含每页的解析详情、布局信息、块结构 |
| `*_model.json` | 模型推理结果，包含每个内容块的类型、坐标、置信度 |
| `content_list.json` | 简化版结构化数据，按阅读顺序平铺存储所有可读内容块 |
| `content_list_v2.json` | 3.0+ 新增，统一 `type + content` 结构，便于程序化处理 |

**非 HTML 文件解析结果**：`full.md` + `middle.json` + `*_model.json` + `content_list.json`

**HTML 文件解析结果**（略有不同）：`full.md` + `main.html`

### A.2 内容块类型（content_list.json）

| 类型 | 说明 |
|------|------|
| `text` | 正文文本 |
| `title` | 标题块，含 `text_level` 标识层级（1=一级标题，以此类推） |
| `image` / `table` / `chart` | 视觉类块，含图片路径、说明文字、脚注等 |
| `equation` | 行间公式，含 LaTeX 文本 |
| `code` / `algorithm` | 代码块 / 算法块，含 `code_language` |
| `list` / `index` | 列表与索引，含 `list_items` |
| `header` / `footer` / `page_number` / `aside_text` / `page_footnote` | 页面辅助块 |

### A.3 后端差异

| 后端 | 特点 | 适用场景 |
|------|------|---------|
| `pipeline` | 传统深度学习后端，速度快 | 常规文档 |
| `vlm` | 视觉大模型后端，精度更高 | 复杂版式、扫描件 |
| `office` | Office 原生 API 解析 | Word/PPT/Excel |

---

## 附录 B：与项目代码的对应关系

### B.1 本地 CLI 模式（当前默认）

当前项目 [`src/parse/mineru_parser.py`](src/parse/mineru_parser.py) 使用**本地 MinerU CLI** 模式：

```bash
mineru -p <pdf_path> -o <output_dir> -b pipeline
```

- **无需 API Key**，直接调用本地 GPU
- **输出目录**中包含 `full.md`、`middle.json`、`content_list.json` 等文件
- **后续 Pipeline**（`route` → `extract`）以 `full.md` 为输入

### B.2 切换到云端 API 模式

如需切换到**云端 API** 模式：

1. **配置环境变量**：在 `.env` 中配置 `MINERU_API_KEY`
   ```bash
   MINERU_API_KEY=your_mineru_api_key_here
   MINERU_API_URL=https://mineru.net/api/v4/extract/task
   ```

2. **修改解析模块**：替换 `src/parse/mineru_parser.py` 中的 CLI 调用为 HTTP API 调用：
   ```python
   # POST 创建任务 → 轮询 GET 查询状态 → 下载 full_zip_url → 解压取 full.md
   ```

3. **流程对比**：

   | 步骤 | 本地 CLI | 云端 API |
   |------|---------|---------|
   | 1 | `mineru -p pdf -o dir` | `POST /api/v4/extract/task` |
   | 2 | 等待本地 GPU 处理 | 轮询 `GET /api/v4/extract/task/{id}` |
   | 3 | 读取 `dir/full.md` | 下载 Zip → 解压 → 取 `full.md` |

4. **注意事项**：
   - 每日 1000 页最高优先级额度，超出后排队
   - 国内 URL 优先，国外 URL（GitHub、AWS 等）可能超时
   - 建议设置合理的轮询间隔（3–5 秒）
   - callback 方式可减少轮询开销，但需要搭建接收端

### B.3 模式选择建议

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 有 NVIDIA GPU | 本地 CLI | 更快、更稳定、无网络依赖 |
| 无 GPU / 远程服务器 | 云端 API | 无需配置 CUDA 环境 |
| 批量处理 > 200 文件 | 云端 API | 本地 GPU 可能内存不足 |
| 需要最高精度 | 本地 CLI（vlm 后端） | 可控制模型版本和参数 |
"""

    return frontmatter + context_section + body + appendix_a


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    source = project_root / "docs" / "mineru_api_docs_extracted.md"
    output = project_root / "docs" / "mineru_api_reference.md"

    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    text = source.read_text(encoding="utf-8")
    cleaned = clean_content(text)
    final = build_final_md(cleaned)

    output.write_text(final, encoding="utf-8")

    chars = len(final)
    lines = final.count("\n")
    print(f"✅ Written {chars:,} chars ({lines:,} lines) to {output.relative_to(project_root)}")


if __name__ == "__main__":
    main()
