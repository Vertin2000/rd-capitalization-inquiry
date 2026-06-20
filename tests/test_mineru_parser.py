"""MinerU parser tests."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import src.parse.mineru_parser as mineru_parser
from src.parse.mineru_parser import MinerUParser


def make_parser(tmp_path: Path) -> MinerUParser:
    return MinerUParser(
        pdf_dir=str(tmp_path / "pdf"),
        output_dir=str(tmp_path / "parsed"),
        resume_file=str(tmp_path / "parsed" / "parsed_docs.jsonl"),
    )


def test_get_mineru_cmd_uses_mineru_exe_env_first(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    mineru_exe = tmp_path / "custom" / "mineru.exe"
    mineru_exe.parent.mkdir(parents=True)
    mineru_exe.write_text("", encoding="utf-8")

    monkeypatch.setenv("MINERU_EXE", str(mineru_exe))
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [str(mineru_exe)]


def test_get_mineru_cmd_uses_uv_tool_environment_when_not_on_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    scripts_dir = tmp_path / "Roaming" / "uv" / "tools" / "mineru" / "Scripts"
    uv_tool_exe = scripts_dir / "mineru.exe"
    uv_tool_python = scripts_dir / "python.exe"
    scripts_dir.mkdir(parents=True)
    uv_tool_exe.write_text("", encoding="utf-8")
    uv_tool_python.write_text("", encoding="utf-8")

    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [
        str(uv_tool_python),
        "-B",
        "-m",
        "mineru.cli.client",
    ]


def test_get_mineru_cmd_uses_custom_uv_tool_dir_when_not_on_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    scripts_dir = tmp_path / "uv-tools" / "mineru" / "Scripts"
    uv_tool_exe = scripts_dir / "mineru.exe"
    uv_tool_python = scripts_dir / "python.exe"
    scripts_dir.mkdir(parents=True)
    uv_tool_exe.write_text("", encoding="utf-8")
    uv_tool_python.write_text("", encoding="utf-8")

    monkeypatch.setenv("UV_TOOL_DIR", str(tmp_path / "uv-tools"))
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [
        str(uv_tool_python),
        "-B",
        "-m",
        "mineru.cli.client",
    ]


def test_get_mineru_cmd_prefers_uv_tool_environment_over_path_shim(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    scripts_dir = tmp_path / "Roaming" / "uv" / "tools" / "mineru" / "Scripts"
    uv_tool_exe = scripts_dir / "mineru.exe"
    uv_tool_python = scripts_dir / "python.exe"
    scripts_dir.mkdir(parents=True)
    uv_tool_exe.write_text("", encoding="utf-8")
    uv_tool_python.write_text("", encoding="utf-8")
    path_shim = tmp_path / ".local" / "bin" / "mineru.exe"
    path_shim.parent.mkdir(parents=True)
    path_shim.write_text("", encoding="utf-8")

    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))
    monkeypatch.setattr("shutil.which", lambda _name: str(path_shim))

    assert parser._get_mineru_cmd() == [
        str(uv_tool_python),
        "-B",
        "-m",
        "mineru.cli.client",
    ]


def test_get_mineru_cmd_falls_back_to_uv_tool_exe_without_python(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    uv_tool_exe = (
        tmp_path / "Roaming" / "uv" / "tools" / "mineru" / "Scripts" / "mineru.exe"
    )
    uv_tool_exe.parent.mkdir(parents=True)
    uv_tool_exe.write_text("", encoding="utf-8")

    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [str(uv_tool_exe)]


def test_get_mineru_cmd_uses_uv_local_bin_when_not_on_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    uv_local_exe = tmp_path / ".local" / "bin" / "mineru.exe"
    uv_local_exe.parent.mkdir(parents=True)
    uv_local_exe.write_text("", encoding="utf-8")

    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [str(uv_local_exe)]


def test_get_mineru_cmd_uses_home_managed_venv_when_not_on_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    mineru_exe = tmp_path / ".mineru" / "Scripts" / "mineru.exe"
    mineru_exe.parent.mkdir(parents=True)
    mineru_exe.write_text("", encoding="utf-8")

    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.delenv("UV_TOOL_DIR", raising=False)
    monkeypatch.delenv("UV_TOOL_BIN_DIR", raising=False)
    monkeypatch.setattr("shutil.which", lambda _name: None)

    assert parser._get_mineru_cmd() == [str(mineru_exe)]


def test_move_output_accepts_mineru_3_backend_directory(
    tmp_path: Path,
) -> None:
    parser = make_parser(tmp_path)
    doc_id = "000001_2024-03-01_abcd1234"
    backend_dir = tmp_path / "tmp_out" / doc_id / "pipeline_auto"
    backend_dir.mkdir(parents=True)
    (backend_dir / f"{doc_id}.md").write_text("# parsed\n", encoding="utf-8")
    (backend_dir / f"{doc_id}_content_list.json").write_text(
        "[]\n",
        encoding="utf-8",
    )

    target = parser._move_output(tmp_path / "tmp_out", doc_id)

    assert target == parser.output_dir / f"{doc_id}.md"
    assert target.read_text(encoding="utf-8") == "# parsed\n"
    assert (parser.output_dir / f"{doc_id}_content_list.json").read_text(
        encoding="utf-8"
    ) == "[]\n"
    assert (parser.output_dir / "mineru_raw" / doc_id / "pipeline_auto").exists()


def test_move_output_accepts_legacy_flat_directory(tmp_path: Path) -> None:
    parser = make_parser(tmp_path)
    doc_id = "000001_2024-03-01_abcd1234"
    doc_dir = tmp_path / "tmp_out" / doc_id
    doc_dir.mkdir(parents=True)
    (doc_dir / f"{doc_id}.md").write_text("# parsed\n", encoding="utf-8")

    target = parser._move_output(tmp_path / "tmp_out", doc_id)

    assert target == parser.output_dir / f"{doc_id}.md"
    assert target.read_text(encoding="utf-8") == "# parsed\n"


def test_parse_records_mineru_stderr_on_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    pdf_path = tmp_path / "input.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")

    monkeypatch.setattr(parser, "_get_mineru_cmd", lambda: ["mineru"])

    class FakeProcess:
        pid = 12345
        returncode = 1

        def __init__(self, *_args, **kwargs):
            kwargs["stdout"].write(b"stdout detail")
            kwargs["stderr"].write(b"torch import failed")

        def wait(self, timeout):
            self.timeout = timeout
            return self.returncode

    monkeypatch.setattr(subprocess, "Popen", FakeProcess)

    assert parser.parse(pdf_path, "input") is None
    record = json.loads(parser.resume_file.read_text(encoding="utf-8").strip())
    assert record["status"] == "failed"
    assert "exit=1" in record["error"]
    assert "torch import failed" in record["error"]


def test_run_mineru_removes_project_python_env_for_external_tool(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    pdf_path = tmp_path / "input.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")
    output_path = tmp_path / "out"
    captured_env = {}

    monkeypatch.setenv("PYTHONHOME", "C:/bad/python")
    monkeypatch.setenv("PYTHONPATH", "C:/bad/path")
    monkeypatch.setenv("VIRTUAL_ENV", "C:/project/.venv")
    monkeypatch.setenv("__PYVENV_LAUNCHER__", "C:/bad/python.exe")
    monkeypatch.setattr(parser, "_get_mineru_cmd", lambda: ["mineru"])

    class FakeProcess:
        pid = 12345
        returncode = 0

        def __init__(self, *_args, **kwargs):
            captured_env.update(kwargs["env"])
            assert kwargs["stdout"] is not subprocess.PIPE
            assert kwargs["stderr"] is not subprocess.PIPE

        def wait(self, timeout):
            self.timeout = timeout
            return self.returncode

    monkeypatch.setattr(subprocess, "Popen", FakeProcess)

    success, error = parser._run_mineru(pdf_path, output_path)

    assert success is True
    assert error == ""
    assert "PYTHONHOME" not in captured_env
    assert "PYTHONPATH" not in captured_env
    assert "VIRTUAL_ENV" not in captured_env
    assert "__PYVENV_LAUNCHER__" not in captured_env
    assert captured_env["MINERU_DEVICE_MODE"] == "cuda"
    assert captured_env["MINERU_MODEL_SOURCE"] == "modelscope"


def test_run_mineru_uses_backend_from_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    pdf_path = tmp_path / "input.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")
    output_path = tmp_path / "out"
    captured_cmd = []

    monkeypatch.setenv("MINERU_BACKEND", "hybrid-auto-engine")
    monkeypatch.setattr(parser, "_get_mineru_cmd", lambda: ["mineru"])

    class FakeProcess:
        pid = 12345
        returncode = 0

        def __init__(self, cmd, **_kwargs):
            captured_cmd.extend(cmd)

        def wait(self, timeout):
            self.timeout = timeout
            return self.returncode

    monkeypatch.setattr(subprocess, "Popen", FakeProcess)

    success, error = parser._run_mineru(pdf_path, output_path)

    assert success is True
    assert error == ""
    assert captured_cmd[-2:] == ["-b", "hybrid-auto-engine"]


def test_run_mineru_timeout_kills_process_tree(
    tmp_path: Path,
    monkeypatch,
) -> None:
    parser = make_parser(tmp_path)
    pdf_path = tmp_path / "input.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")
    output_path = tmp_path / "out"
    killed_pids = []

    monkeypatch.setattr(parser, "_get_mineru_cmd", lambda: ["mineru"])

    class FakeProcess:
        pid = 45678

        def __init__(self, *_args, **_kwargs):
            pass

        def wait(self, timeout):
            raise subprocess.TimeoutExpired(cmd=["mineru"], timeout=timeout)

        def kill(self):
            pass

    def fake_kill_process_tree(process):
        killed_pids.append(process.pid)

    monkeypatch.setattr(subprocess, "Popen", FakeProcess)
    monkeypatch.setattr(mineru_parser, "_kill_process_tree", fake_kill_process_tree)

    try:
        parser._run_mineru(pdf_path, output_path)
    except subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("Expected MinerU timeout")

    assert killed_pids == [45678]


def test_parse_records_missing_mineru_command(tmp_path: Path, monkeypatch) -> None:
    parser = make_parser(tmp_path)
    pdf_path = tmp_path / "input.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")

    monkeypatch.setattr(parser, "_get_mineru_cmd", lambda: [])

    assert parser.parse(pdf_path, "input") is None
    record = json.loads(parser.resume_file.read_text(encoding="utf-8").strip())
    assert record["status"] == "failed"
    assert "uv tool install" in record["error"]


def test_load_parsed_set_requires_existing_non_empty_markdown(tmp_path: Path) -> None:
    parser = make_parser(tmp_path)
    parser.resume_file.parent.mkdir(parents=True, exist_ok=True)
    records = [
        {"doc_id": "ready", "status": "success", "error": ""},
        {"doc_id": "missing", "status": "success", "error": ""},
        {"doc_id": "empty", "status": "success", "error": ""},
        {"doc_id": "failed", "status": "failed", "error": "boom"},
    ]
    parser.resume_file.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )
    (parser.output_dir / "ready.md").write_text("# parsed\n", encoding="utf-8")
    (parser.output_dir / "empty.md").write_text("", encoding="utf-8")

    assert parser._load_parsed_set() == {"ready"}


def test_run_logs_each_pdf_progress(
    tmp_path: Path,
    monkeypatch,
    caplog,
) -> None:
    parser = make_parser(tmp_path)
    parser.pdf_dir.mkdir(parents=True)
    (parser.pdf_dir / "a.pdf").write_bytes(b"%PDF-1.7")
    (parser.pdf_dir / "b.pdf").write_bytes(b"%PDF-1.7")

    def fake_parse(_pdf_path: Path, doc_id: str) -> Path:
        target = parser.output_dir / f"{doc_id}.md"
        target.write_text("# parsed\n", encoding="utf-8")
        return target

    monkeypatch.setattr(parser, "parse", fake_parse)
    caplog.set_level("INFO", logger=mineru_parser.logger.name)

    assert parser.run() == {"total": 2, "success": 2, "failed": 0}
    messages = "\n".join(record.getMessage() for record in caplog.records)

    assert "[1/2]" in messages
    assert "[2/2]" in messages
    assert "a" in messages
    assert "b" in messages
    assert "耗时" in messages
