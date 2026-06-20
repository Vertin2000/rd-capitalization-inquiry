param(
    [string]$Python = "3.12",

    [string]$TorchBackend = "cu126",

    [string]$ToolDir = "",

    [string]$ToolBinDir = "",

    [switch]$NoPathUpdate
)

# MinerU global installer (uv tool + GPU mode)
# Usage:
#   .\scripts\setup_mineru.ps1
#
# MinerU is treated as a user-level CLI application, not as a dependency of
# this project's .venv. The tool environment installs mineru[all]; this project
# still invokes the conservative pipeline backend at runtime.

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $true)]
        [scriptblock]$ScriptBlock
    )

    Write-Host "`n$Title" -ForegroundColor Yellow
    & $ScriptBlock
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $Title"
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MinerU global setup (uv tool + CUDA)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv was not found. Install uv first, then rerun this script."
}

$package = "mineru[all]"

Write-Host "Package: $package"
Write-Host "Python: $Python"
Write-Host "PyTorch backend: $TorchBackend"

if (-not $env:MINERU_MODEL_SOURCE) {
    $env:MINERU_MODEL_SOURCE = "modelscope"
}
Write-Host "Model source: $env:MINERU_MODEL_SOURCE"

if ($ToolDir) {
    $env:UV_TOOL_DIR = $ToolDir
    Write-Host "UV_TOOL_DIR: $ToolDir"
}

if ($ToolBinDir) {
    $env:UV_TOOL_BIN_DIR = $ToolBinDir
    Write-Host "UV_TOOL_BIN_DIR: $ToolBinDir"
}

Invoke-Checked "[1/5] uv version" {
    & uv --version
}

Invoke-Checked "[2/5] Install MinerU tool environment" {
    & uv tool install $package `
        --python $Python `
        --managed-python `
        --torch-backend $TorchBackend `
        --default-index https://mirrors.aliyun.com/pypi/simple `
        --force
}

if ($NoPathUpdate) {
    Write-Host "`n[3/5] Skip PATH update" -ForegroundColor Yellow
} else {
    Invoke-Checked "[3/5] Ensure uv tool executable directory is on PATH" {
        & uv tool update-shell
    }
}

$toolDir = (& uv tool dir).Trim()
$toolPython = Join-Path $toolDir "mineru\Scripts\python.exe"
$shimRoot = if ($env:UV_TOOL_BIN_DIR) {
    $env:UV_TOOL_BIN_DIR
} else {
    Join-Path $env:APPDATA "uv\tools\bin"
}
$uvShim = Join-Path $shimRoot "mineru.exe"
$pathMineru = (Get-Command mineru -ErrorAction SilentlyContinue).Source

if ($pathMineru) {
    $mineruExe = $pathMineru
} elseif (Test-Path -LiteralPath $uvShim) {
    $mineruExe = $uvShim
} else {
    $candidate = Join-Path $toolDir "mineru\Scripts\mineru.exe"
    if (Test-Path -LiteralPath $candidate) {
        $mineruExe = $candidate
    } else {
        throw "mineru.exe was not found. uv tool dir: $toolDir"
    }
}

if (-not (Test-Path -LiteralPath $toolPython)) {
    throw "MinerU tool Python was not found: $toolPython"
}

Invoke-Checked "[4/5] Verify PyTorch and CUDA" {
    & $toolPython -B -c "import importlib.metadata as m; import torch; print('mineru', m.version('mineru')); print('torch', torch.__version__); print('cuda runtime', torch.version.cuda); print('cuda available', torch.cuda.is_available()); print('device', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"
}

Invoke-Checked "[5/5] Verify MinerU CLI" {
    & $mineruExe --version
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "MinerU setup finished." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nCurrent mineru executable:" -ForegroundColor White
Write-Host "  $mineruExe" -ForegroundColor Gray
Write-Host "`nOpen a new PowerShell and run:" -ForegroundColor White
Write-Host "  mineru --version" -ForegroundColor Gray
Write-Host '  $env:MINERU_MODEL_SOURCE = "modelscope"' -ForegroundColor Gray
Write-Host '  uv run python src/main.py --stage parse --limit 1' -ForegroundColor Gray
