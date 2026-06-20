# MinerU 配置指南（本地 CLI fallback + API batch 主路线）

> 本文件说明如何把 MinerU 配置成全局可复用的外部 CLI 工具，并记录当前项目的 API batch 主路线。
>
> 对应讲义：`../00-课程讲义/Week13-MinerU解析与Schema抽取/讲义.md`

---

## 1. 定位

MinerU 在本项目中有两条路线：

- **主路线**：MinerU 精准解析 API batch，命令为 `uv run python src/main.py --stage parse --parse-backend api-batch`。当前已完成 150/150 年报全量解析。
- **fallback**：本地 `mineru` CLI。它是系统级外部工具，类似 Git、Node 或 pandoc；项目通过 CLI 调用它，不把 `mineru[all]` 放进本项目 `.venv`。

推荐安装方式：

| 层面 | 做法 |
|------|------|
| 依赖声明 | README 写明需要全局 `mineru>=3.2.0` |
| 安装管理 | 使用 `uv tool install "mineru[all]"` 创建独立工具环境 |
| 项目代码 | `src/parse/mineru_parser.py` 只调用 CLI |
| 模型缓存 | 复用用户目录下的 HuggingFace 或 ModelScope 缓存 |

这样做可以避免每个项目重复安装数 GB 的 PyTorch、OCR、VLM 依赖，也能让多个项目共享同一套 MinerU。

课程 Week13 Lab 提到正式项目可使用 MinerU API。当前项目已经新增 `src/parse/mineru_api_parser.py`，通过 MinerU 官方精准解析 API 的 URL batch endpoint 批量解析长年报；本地 CLI backend 继续保留，用于无 API Key、网络异常或需要本地复核时 fallback。

---

## 2. 环境要求

| 项目 | 要求 |
|------|------|
| Python | 3.10-3.12（Windows 下 `ray` 不支持 3.13） |
| uv | 已安装并可执行 `uv --version` |
| GPU | NVIDIA Volta 及以后架构；本机 RTX 4060 Laptop 8GB 符合要求 |
| PyTorch | MinerU 3.2.3 要求 `torch>=2.6,<3`；Windows `mineru[all]` 中 `lmdeploy` 要求 `torch<=2.8` |
| 磁盘 | 建议预留 20GB 以上给依赖和模型缓存 |

当前项目默认使用 Python 3.12 和 CUDA 12.6 后端。

---

## 3. 安装

### 3.1 一键安装（推荐）

在 `project2/` 目录执行：

```powershell
.\scripts\setup_mineru.ps1
```

脚本会执行：

1. 检查 `uv`
2. 设置默认模型源 `MINERU_MODEL_SOURCE=modelscope`
3. 运行 `uv tool install "mineru[all]" --python 3.12 --torch-backend cu126 --force`
4. 运行 `uv tool update-shell`
5. 验证 MinerU、PyTorch 和 CUDA

### 3.2 手动安装

如果你希望自己观察安装耗时，直接运行：

```powershell
$env:MINERU_MODEL_SOURCE = "modelscope"

uv tool install "mineru[all]" `
  --python 3.12 `
  --torch-backend cu126 `
  --default-index https://mirrors.aliyun.com/pypi/simple `
  --force
```

安装后验证：

```powershell
uv tool update-shell

$mineruPy = Join-Path (uv tool dir) "mineru\Scripts\python.exe"
& $mineruPy -B -c "import torch, importlib.metadata as m; print('mineru', m.version('mineru')); print('torch', torch.__version__); print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"

mineru --version
```

如果当前终端还找不到 `mineru`，重新打开一个 PowerShell。

---

## 4. 解析烟测与复跑

推荐复跑或补跑年报 parse：

```powershell
uv run python src/main.py --stage parse --parse-backend api-batch
```

需要先在 `.env` 设置 `MINERU_API_KEY`。API batch 会按 200 页拆分，记录 `data/parsed/mineru_api_tasks.jsonl`，原始结果保留在 `data/parsed/mineru_api_raw/{doc_id}/part_*/`。

本地 CLI 首次解析会下载模型，耗时较长。需要本地 fallback 时，建议在终端手动执行，方便观察进度：

```powershell
$env:MINERU_MODEL_SOURCE = "modelscope"
mineru -p "data/pdf/600276_恒瑞医药_2021年报.pdf" -o "data/parsed/_smoke_mineru"
```

本地烟测成功后，再通过项目 Pipeline 解析：

```powershell
uv run python src/main.py --stage parse --limit 1
```

项目会把稳定入口写到：

- `data/parsed/{doc_id}.md`
- `data/parsed/{doc_id}_content_list.json`（如果 MinerU 输出）
- `data/parsed/mineru_raw/{doc_id}/`（保留 MinerU 原始输出结构）

---

## 5. 配置方式

MinerU 3.x 主要通过 CLI 参数和环境变量控制。

| 变量 | 推荐值 | 用途 |
|------|--------|------|
| `MINERU_MODEL_SOURCE` | `modelscope` | 国内网络优先使用 ModelScope 下载模型 |
| `MINERU_DEVICE_MODE` | `cuda` | 强制使用 CUDA；项目代码默认设置 |
| `MINERU_BACKEND` | 默认 `pipeline` | 可设为 `hybrid-auto-engine` 试高精度后端 |
| `MINERU_API_KEY` | 写入 `.env` | MinerU 精准解析 API / batch backend 认证 |
| `MINERU_API_BATCH_SIZE` | `50` | URL batch 每批 page segment 数，贴近官方 50 files/min 限流 |
| `MINERU_API_DOWNLOAD_WORKERS` | `8` | 结果 zip 并发下载 worker 数 |
| `MINERU_API_EXTRACT_WORKERS` | `4` | 结果 zip 并发解压 worker 数 |
| `MINERU_EXE` / `MINERU_CLI` | 可选 | 指向自定义 `mineru.exe`，优先级最高 |
| `UV_TOOL_DIR` | 可选 | 用户级 uv tool 目录权限异常时，指定替代工具目录 |
| `UV_TOOL_BIN_DIR` | 可选 | 指定 uv tool shim 目录 |

旧文件 `configs/mineru_config_legacy.json` 和 `~/.cache/magic-pdf/magic-pdf.json` 属于旧版 `magic-pdf` 配置思路。当前项目不再依赖它们，只保留作历史参考。

---

## 6. 故障排查

| 问题 | 排查方式 | 处理 |
|------|----------|------|
| `mineru` 找不到 | `uv tool dir`，检查 `mineru\Scripts\mineru.exe` 是否存在 | 运行 `uv tool update-shell`，或设置 `MINERU_EXE` |
| `uv tool` 报 `tools\.lock` 拒绝访问 | 用户级 uv tool 目录权限异常 | 临时用 `.\scripts\setup_mineru.ps1 -ToolDir "$PWD\.uv-tools" -ToolBinDir "$PWD\.uv-tool-bin" -NoPathUpdate` 验证；长期修复用户目录权限 |
| `import torch` 失败 | 用上文验证命令查看 `torch.__version__` | 确认不是旧的 `torch==2.4.0+cu121`；重新运行 uv tool 安装 |
| CUDA 为 `False` | 验证 `torch.cuda.is_available()` | 确认安装时使用 `--torch-backend cu126` |
| 模型下载慢或失败 | 查看是否使用 HuggingFace | 设置 `$env:MINERU_MODEL_SOURCE = "modelscope"` |
| 解析结果未生成 Markdown | 查看 `data/parsed/parsed_docs.jsonl` 中的错误摘要 | 根据 stderr 修复；不要只看“返回非零” |
| 显存不足 | 解析时出现 CUDA OOM | 先用 `--limit 1`；必要时临时改用 CPU 后端验证流程 |

不要通过下载 libtorch 并手动复制 DLL 的方式修复 PyTorch。那会绕过依赖解析，容易得到不满足 MinerU 版本约束的环境。

---

## 7. 版本记录

| 日期 | 变更 |
|------|------|
| 2026-06-10 | 从旧版 `magic-pdf` 迁移到新版 `mineru` CLI |
| 2026-06-10 | 确认旧环境 `mineru==3.2.3` + `torch==2.4.0+cu121` 不满足 MinerU 依赖约束 |
| 2026-06-10 | 改为 `uv tool` 全局工具化安装，默认 Python 3.12 + CUDA 12.6 |
| 2026-06-15 | 新增 MinerU API batch 主路线，完成 150/150 年报 Markdown 解析；本地 CLI 改为 fallback |
