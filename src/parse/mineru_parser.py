"""MinerU PDF 解析器

将 PDF 解析为 Markdown，默认使用稳定的 `mineru -b pipeline` 与
`MINERU_DEVICE_MODE=cuda`，可通过 `MINERU_BACKEND` 切换 MinerU 后端。

Usage:
    from src.parse.mineru_parser import MinerUParser
    parser = MinerUParser()
    stats = parser.run()

讲义依据: Week 13 — MinerU 解析
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# MinerU 解析超时（单份 PDF，秒）。首次运行可能需要加载/下载模型。
PARSE_TIMEOUT = int(os.getenv("MINERU_PARSE_TIMEOUT", "1800"))
DEFAULT_BACKEND = "pipeline"
MISSING_MINERU_MESSAGE = (
    "mineru 命令不可用。请执行 scripts/setup_mineru.ps1，"
    '或手动运行 uv tool install "mineru[all]" --python 3.12 '
    "--torch-backend cu126 --force；也可设置 MINERU_EXE 指向 mineru.exe"
)


def _mineru_cmd_from_exe(mineru_exe: Path) -> list[str]:
    """Return a MinerU command, bypassing broken Windows exe launchers."""
    sibling_python = mineru_exe.with_name("python.exe")
    if sibling_python.exists():
        return [str(sibling_python), "-B", "-m", "mineru.cli.client"]
    return [str(mineru_exe)]


def _kill_process_tree(process: subprocess.Popen) -> None:
    """Terminate a process and its descendants."""
    if process.poll() is not None:
        return

    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    process.kill()


def _read_log_tail(path: Path, limit_chars: int = 2000) -> str:
    if not path.exists():
        return ""

    data = path.read_bytes()
    for encoding in ("utf-8", "gb18030"):
        try:
            text = data.decode(encoding)
            return text.strip()[-limit_chars:]
        except UnicodeDecodeError:
            continue
    return f"{path.name} 无法按 UTF-8 或 GB18030 解码"


class MinerUParser:
    """MinerU PDF 解析器

    调用 `mineru` CLI 将 PDF 转换为 Markdown。
    输出格式: data/parsed/{doc_id}.md
    Resume: 通过 parsed_docs.jsonl 跟踪已解析的 doc_id
    """

    def __init__(
        self,
        pdf_dir: str = "data/pdf",
        output_dir: str = "data/parsed",
        resume_file: str = "data/parsed/parsed_docs.jsonl",
    ) -> None:
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.pdf_dir = self.project_root / pdf_dir
        self.output_dir = self.project_root / output_dir
        self.resume_file = self.project_root / resume_file

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resume_file.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # 内部方法
    # ------------------------------------------------------------------ #

    def _load_parsed_set(self) -> set[str]:
        """加载已解析的 doc_id 集合"""
        if not self.resume_file.exists():
            return set()
        parsed: set[str] = set()
        with open(self.resume_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record.get("status") != "success":
                        continue
                    doc_id = record["doc_id"]
                    parsed_md = self.output_dir / f"{doc_id}.md"
                    if parsed_md.exists() and parsed_md.stat().st_size > 0:
                        parsed.add(doc_id)
                except json.JSONDecodeError:
                    continue
        return parsed

    def _save_parse_record(
        self, doc_id: str, status: str, error: str = ""
    ) -> None:
        """保存解析记录到 resume 文件"""
        record = {
            "doc_id": doc_id,
            "status": status,
            "error": error,
        }
        with open(self.resume_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _get_mineru_cmd(self) -> list[str]:
        """获取 mineru 命令路径

        优先使用显式环境变量，其次查找 PATH，再回退到 uv tool 的
        独立工具环境，最后兼容旧的 ~/.mineru venv。这里只做路径发现，
        不执行 mineru，以免 torch 尚未配置好时把“命令存在”误判为
        “命令不存在”。
        """
        for env_name in ("MINERU_EXE", "MINERU_CLI"):
            env_mineru = os.getenv(env_name)
            if env_mineru:
                env_path = Path(env_mineru)
                if env_path.exists():
                    return _mineru_cmd_from_exe(env_path)
                return [env_mineru]

        uv_tool_bin_dir = os.getenv("UV_TOOL_BIN_DIR")
        if uv_tool_bin_dir:
            uv_tool_bin_exe = Path(uv_tool_bin_dir) / "mineru.exe"
            if uv_tool_bin_exe.exists():
                return _mineru_cmd_from_exe(uv_tool_bin_exe)

        uv_tool_dir_env = os.getenv("UV_TOOL_DIR")
        if uv_tool_dir_env:
            uv_tool_env = (
                Path(uv_tool_dir_env) / "mineru" / "Scripts" / "mineru.exe"
            )
            if uv_tool_env.exists():
                return _mineru_cmd_from_exe(uv_tool_env)

        appdata = os.getenv("APPDATA")
        if appdata:
            uv_tool_dir = Path(appdata) / "uv" / "tools"
            uv_tool_env = uv_tool_dir / "mineru" / "Scripts" / "mineru.exe"
            if uv_tool_env.exists():
                return _mineru_cmd_from_exe(uv_tool_env)
            uv_tool_shim = uv_tool_dir / "bin" / "mineru.exe"
            if uv_tool_shim.exists():
                return _mineru_cmd_from_exe(uv_tool_shim)

        path_mineru = shutil.which("mineru")
        if path_mineru:
            return _mineru_cmd_from_exe(Path(path_mineru))

        userprofile = os.getenv("USERPROFILE")
        if userprofile:
            uv_local_bin = Path(userprofile) / ".local" / "bin" / "mineru.exe"
            if uv_local_bin.exists():
                return _mineru_cmd_from_exe(uv_local_bin)

            managed_venv = Path(userprofile) / ".mineru" / "Scripts" / "mineru.exe"
            if managed_venv.exists():
                return _mineru_cmd_from_exe(managed_venv)

        return []

    def _check_mineru_available(self) -> bool:
        """检查 mineru 命令是否可用"""
        return len(self._get_mineru_cmd()) > 0

    @staticmethod
    def _summarize_mineru_failure(
        returncode: int,
        stdout_log: Path,
        stderr_log: Path,
    ) -> str:
        """Return a compact diagnostic message for a failed MinerU process."""
        stdout = _read_log_tail(stdout_log)
        stderr = _read_log_tail(stderr_log)
        parts = [f"exit={returncode}"]
        if stderr:
            parts.append(f"stderr: {stderr[-2000:]}")
        if stdout:
            parts.append(f"stdout: {stdout[-2000:]}")
        return " | ".join(parts)

    def _run_mineru(self, pdf_path: Path, temp_output: Path) -> tuple[bool, str]:
        """调用 MinerU CLI 解析单个 PDF"""
        mineru = self._get_mineru_cmd()
        if not mineru:
            logger.error("mineru 命令不可用")
            return False, "mineru 命令不可用"

        backend = os.getenv("MINERU_BACKEND", DEFAULT_BACKEND)
        cmd = mineru + [
            "-p", str(pdf_path),
            "-o", str(temp_output),
            "-b", backend,
        ]

        env = os.environ.copy()
        for python_env in (
            "PYTHONHOME",
            "PYTHONPATH",
            "PYTHONEXECUTABLE",
            "__PYVENV_LAUNCHER__",
            "VIRTUAL_ENV",
        ):
            env.pop(python_env, None)
        env.setdefault("MINERU_DEVICE_MODE", "cuda")
        env.setdefault("MINERU_MODEL_SOURCE", "modelscope")

        log_dir = self.output_dir / "mineru_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_log = log_dir / f"{pdf_path.stem}.stdout.log"
        stderr_log = log_dir / f"{pdf_path.stem}.stderr.log"

        with open(stdout_log, "wb") as stdout_file, open(stderr_log, "wb") as stderr_file:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=stdout_file,
                stderr=stderr_file,
                env=env,
            )
            try:
                returncode = process.wait(timeout=PARSE_TIMEOUT)
            except subprocess.TimeoutExpired:
                _kill_process_tree(process)
                try:
                    process.wait(timeout=10)
                except Exception:
                    pass
                raise

        if returncode != 0:
            error = self._summarize_mineru_failure(
                returncode,
                stdout_log,
                stderr_log,
            )
            logger.error(
                "MinerU 命令失败（%s）\nstdout log: %s\nstderr log: %s",
                error,
                stdout_log,
                stderr_log,
            )
            return False, error
        return True, ""

    def _move_output(self, temp_output: Path, doc_id: str) -> Path | None:
        """将 MinerU 输出移动到标准位置"""
        doc_output = temp_output / doc_id
        if not doc_output.exists():
            return None

        raw_output = self.output_dir / "mineru_raw" / doc_id
        if raw_output.exists():
            shutil.rmtree(raw_output)
        raw_output.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(doc_output), str(raw_output))

        # MinerU 3.x 通常输出到 {doc_id}/{backend}_auto/，旧版本可能直接
        # 输出到 {doc_id}/。用精确文件名递归查找，兼容两种结构。
        md_candidates = sorted(raw_output.rglob(f"{doc_id}.md"))
        if not md_candidates:
            return None

        mineru_md = md_candidates[0]
        target_md = self.output_dir / f"{doc_id}.md"

        # 保留完整 MinerU 原始输出，同时在 data/parsed/ 提供稳定入口。
        shutil.copy2(str(mineru_md), str(target_md))

        mineru_json = next(
            iter(sorted(raw_output.rglob(f"{doc_id}_content_list.json"))),
            None,
        )
        if mineru_json is not None:
            target_json = self.output_dir / f"{doc_id}_content_list.json"
            shutil.copy2(str(mineru_json), str(target_json))

        if temp_output.exists() and not any(temp_output.iterdir()):
            temp_output.rmdir()

        return target_md

    # ------------------------------------------------------------------ #
    # 公共方法
    # ------------------------------------------------------------------ #

    def parse(self, pdf_path: Path, doc_id: str) -> Path | None:
        """解析单个 PDF

        Returns:
            解析后的 Markdown 路径，或 None（解析失败）
        """
        # Resume 检查
        parsed = self._load_parsed_set()
        if doc_id in parsed:
            logger.info("[%s] 已解析，跳过", doc_id)
            return self.output_dir / f"{doc_id}.md"

        # 检查 mineru 是否可用
        if not self._check_mineru_available():
            logger.error(MISSING_MINERU_MESSAGE)
            self._save_parse_record(doc_id, "failed", MISSING_MINERU_MESSAGE)
            return None

        # MinerU 输出到临时子目录
        temp_output = self.output_dir / f"_tmp_{doc_id}"
        temp_output.mkdir(parents=True, exist_ok=True)

        try:
            success, mineru_error = self._run_mineru(pdf_path, temp_output)
            if not success:
                logger.error("[%s] MinerU 解析失败", doc_id)
                self._save_parse_record(
                    doc_id,
                    "failed",
                    mineru_error or "MinerU 返回非零",
                )
                return None

            target_md = self._move_output(temp_output, doc_id)
            if target_md is None:
                logger.error("[%s] MinerU 未生成 Markdown 文件", doc_id)
                self._save_parse_record(doc_id, "failed", "未生成 Markdown")
                return None

            self._save_parse_record(doc_id, "success")
            logger.info("[%s] 解析完成: %s", doc_id, target_md)
            return target_md

        except subprocess.TimeoutExpired:
            logger.error("[%s] MinerU 解析超时（%ds）", doc_id, PARSE_TIMEOUT)
            self._save_parse_record(doc_id, "failed", f"超时 {PARSE_TIMEOUT}s")
            return None
        except Exception as e:
            logger.error("[%s] 解析异常: %s", doc_id, e)
            self._save_parse_record(doc_id, "failed", str(e))
            return None
        finally:
            # 清理可能残留的临时目录
            if temp_output.exists():
                shutil.rmtree(temp_output, ignore_errors=True)

    def run(self, limit: int | None = None) -> dict[str, int]:
        """运行解析

        Args:
            limit: 限制处理的 PDF 数量（用于测试）

        Returns:
            统计信息: {"total": 总数, "success": 成功数, "failed": 失败数}
        """
        pdf_files = sorted(self.pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning("未找到 PDF 文件: %s", self.pdf_dir)
            return {"total": 0, "success": 0, "failed": 0}

        if limit:
            pdf_files = pdf_files[:limit]

        total = len(pdf_files)
        success = 0
        failed = 0

        logger.info("开始解析 %d 份 PDF...", total)

        for index, pdf_path in enumerate(pdf_files, start=1):
            doc_id = pdf_path.stem
            start = time.monotonic()
            logger.info("[%d/%d] parse 开始: %s", index, total, doc_id)
            result = self.parse(pdf_path, doc_id)
            elapsed = time.monotonic() - start
            if result:
                success += 1
                status = "success"
            else:
                failed += 1
                status = "failed"
            logger.info(
                "[%d/%d] parse %s: %s (耗时 %.1fs)",
                index,
                total,
                status,
                doc_id,
                elapsed,
            )

        logger.info(
            "解析完成: total=%d, success=%d, failed=%d",
            total, success, failed,
        )
        return {"total": total, "success": success, "failed": failed}


# ---------------------------------------------------------------------- #
# CLI 入口
# ---------------------------------------------------------------------- #

def main() -> int:
    """独立运行入口"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    parser = MinerUParser()
    stats = parser.run()
    print(f"\n{'✅' if stats['failed'] == 0 else '⚠️'} 解析完成: {stats}")
    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
