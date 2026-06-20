"""公共工具模块

提供配置加载、环境变量读取、JSONL 读写等基础功能。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(config_path: str) -> dict[str, Any]:
    """加载 YAML 配置文件"""
    full_path = PROJECT_ROOT / config_path
    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_env() -> None:
    """加载环境变量

    从项目根目录的 .env 文件读取环境变量。
    该文件包含敏感信息（API Key），已配置在 .gitignore 中，不得提交到 Git。
    模板见 .env.example。
    """
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print(f"警告: .env 文件不存在，请先复制 .env.example 为 .env 并配置 API Key")


def read_jsonl(file_path: str | Path) -> list[dict]:
    """读取 JSONL 文件"""
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def write_jsonl(data: list[dict], file_path: str | Path) -> None:
    """写入 JSONL 文件"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def log_step(
    step: str,
    *,
    doc_id: str = "*",
    status: str = "success",
    elapsed: float = 0.0,
    error: str = "",
    log_path: str | Path | None = None,
) -> None:
    """追加一行统一阶段日志到 outputs/logs/run_log.jsonl（Week 14 讲义要求）。

    字段：time / step / doc_id / status / elapsed / error
    doc_id 对批量 stage 填 "*"，明细仍由各模块自己的 jsonl 记录。
    """
    from datetime import datetime, timezone

    path = Path(log_path) if log_path else PROJECT_ROOT / "outputs" / "logs" / "run_log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "step": step,
        "doc_id": doc_id,
        "status": status,
        "elapsed": round(float(elapsed), 3),
        "error": error,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
