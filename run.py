#!/usr/bin/env python3
"""项目运行入口

Usage:
    uv run python run.py --help
    uv run python run.py --stage all
    uv run python run.py --stage crawl --limit 10
"""

import sys
from pathlib import Path

# 确保 src 可被导入
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())
