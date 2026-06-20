# Tool Setup Check

- 使用工具：Codex / Claude Code
- 操作系统：Windows 11
- Python 版本：项目 `.venv` 由 uv 管理，MinerU 工具环境使用 uv-managed Python 3.12
- 是否能打开项目目录：是
- 是否能运行 `uv run python src/main.py --help`：是
- 是否已创建 `.env.example`：是
- 是否确认 `.env` 不提交：是（已在 `.gitignore` 中排除）

## MinerU 安装与 GPU 配置检查

- [ ] MinerU 命令可用：`mineru --version`
- [ ] MinerU 使用新版命令：`mineru`，不是旧版 `magic-pdf`
- [ ] MinerU 安装形态：用户级 `uv tool`，包规格为 `mineru[all]`
- [ ] PyTorch 可导入：

  ```powershell
  $toolPython = Join-Path (uv tool dir) "mineru\Scripts\python.exe"
  & $toolPython -B -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
  ```

- [ ] CUDA 可用：`torch.cuda.is_available()` 输出 `True`
- [ ] 国内网络模型源：运行解析前设置 `$env:MINERU_MODEL_SOURCE = "modelscope"`
- [ ] 示例解析成功：

  ```powershell
  $env:MINERU_DEVICE_MODE = "cuda"
  $env:MINERU_MODEL_SOURCE = "modelscope"
  uv run python src/main.py --stage parse --limit 1
  ```

## LLM API 检查

- [x] `.env` 文件已创建并填入 API Key
  - 备注：`.env.example` 已提供，`.env` 不提交
- [ ] 运行 extract 阶段前验证 API 响应正常

## 已知环境问题

| 问题 | 处理方式 |
| --- | --- |
| 用户级 uv cache 报 `.git` 拒绝访问 | 临时设置 `$env:UV_CACHE_DIR = "$PWD\.uv-cache"`；长期清理/重建用户级 uv cache |
| 用户级 uv tool 报 `tools\.lock` 拒绝访问 | 临时指定 `-ToolDir "$PWD\.uv-tools" -ToolBinDir "$PWD\.uv-tool-bin"`；长期修复用户级 uv tool 目录权限 |
| 旧 `.mineru` 环境中 `torch==2.4.0+cu121` 报 `fbgemm.dll` | 不手补 DLL；重跑 `scripts/setup_mineru.ps1`，让 uv 解析 `torch>=2.6,<3` |
