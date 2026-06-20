"""LLM 客户端模块

用于调用大语言模型 API 进行字段抽取、文本评估等任务。
支持硅基流动 API 及其他 OpenAI 兼容接口。
"""

from __future__ import annotations

import os
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class LLMClient:
    """LLM API 客户端"""

    DEFAULT_BASE_URL = "https://api.siliconflow.cn"
    DEFAULT_MODEL = "Qwen/Qwen2.5-72B-Instruct"

    def __init__(
        self,
        provider: str = "siliconflow",
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        temperature: float = 0,
        max_tokens: int = 2048,
        timeout: int = 300,
        user_agent: str | None = None,
        backend: str | None = None,
    ):
        load_dotenv(PROJECT_ROOT / ".env")
        self.provider = provider
        self.backend = (
            backend or os.environ.get("LLM_BACKEND", "http")
        ).strip().lower()
        self.model = model or os.environ.get("LLM_MODEL", self.DEFAULT_MODEL)
        self.base_url = base_url or os.environ.get(
            "LLM_BASE_URL", self.DEFAULT_BASE_URL
        )
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.user_agent = user_agent or os.environ.get("LLM_USER_AGENT", "")
        self.kimi_code_cli_command = os.environ.get(
            "KIMI_CODE_CLI_COMMAND",
            os.environ.get("KIMI_CLI_COMMAND", "kimi"),
        )
        self.kimi_code_cli_model = os.environ.get(
            "KIMI_CODE_CLI_MODEL",
            os.environ.get("KIMI_CLI_MODEL", ""),
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.kimi_code_cli_retries = max(
            0,
            int(os.environ.get("KIMI_CODE_CLI_RETRIES", "2")),
        )
        self.kimi_code_cli_retry_delay = float(
            os.environ.get("KIMI_CODE_CLI_RETRY_DELAY", "6")
        )
        # HTTP backend 重试：高并发下服务端可能返回空 body / 429 / 瞬断
        self.http_retries = max(0, int(os.environ.get("LLM_HTTP_RETRIES", "4")))
        self.http_retry_delay = float(
            os.environ.get("LLM_HTTP_RETRY_DELAY", "2")
        )
        self._active_processes: set[subprocess.Popen[str]] = set()
        self._active_processes_lock = threading.Lock()

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "LLMClient":
        """从配置字典创建客户端"""
        return cls(
            provider=config.get("provider", "siliconflow"),
            model=config.get("model"),
            base_url=os.environ.get(
                config.get("base_url_env", "LLM_BASE_URL"), ""
            ) or None,
            api_key=os.environ.get(
                config.get("api_key_env", "LLM_API_KEY"), ""
            ) or None,
            temperature=config.get("temperature", 0),
            max_tokens=config.get("max_tokens", 2048),
            timeout=config.get("timeout_seconds", 60),
            user_agent=os.environ.get(
                config.get("user_agent_env", "LLM_USER_AGENT"), ""
            ) or None,
            backend=os.environ.get(config.get("backend_env", "LLM_BACKEND"), "")
            or None,
        )

    def call(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """调用 LLM API

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 覆盖默认温度（可选）

        Returns:
            LLM 生成的文本内容

        Raises:
            ValueError: API Key 未配置
            httpx.HTTPStatusError: API 请求失败
        """
        if self.backend in {"kimi_code_cli", "kimi_cli", "kimi-code-cli", "kimi"}:
            return self._call_kimi_code_cli(prompt, system_prompt)

        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置，请先在 .env 中设置")

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.user_agent:
            headers["User-Agent"] = self.user_agent

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": self.max_tokens,
        }

        # 兼容 base_url 已带版本号路径（如 /v1、/v4）和不带版本号两种情况
        base = self.base_url.rstrip('/')
        if re.search(r'/v\d+$', base):
            api_url = f"{base}/chat/completions"
        else:
            api_url = f"{base}/v1/chat/completions"

        last_error: Exception | None = None
        for attempt in range(self.http_retries + 1):
            try:
                response = httpx.post(
                    api_url, json=payload, headers=headers, timeout=self.timeout
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                if content and content.strip():
                    return content
                # 空 body：高并发过载特征，退避重试
                last_error = RuntimeError("LLM 返回空内容")
            except (httpx.HTTPStatusError, httpx.TransportError, KeyError) as e:
                last_error = e
            if attempt < self.http_retries:
                time.sleep(self.http_retry_delay * (attempt + 1))

        raise RuntimeError(
            f"LLM HTTP 调用失败（重试 {self.http_retries} 次后）: "
            f"{self._truncate_error(str(last_error))}"
        )

    def _call_kimi_code_cli(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """通过本机已登录的 Kimi Code CLI 调用模型。"""
        cli_prompt = prompt
        if system_prompt:
            cli_prompt = f"系统指令：\n{system_prompt}\n\n用户任务：\n{prompt}"

        args = [self.kimi_code_cli_command]
        if self.kimi_code_cli_model:
            args.extend(["-m", self.kimi_code_cli_model])
        args.extend(["-p", cli_prompt, "--output-format", "text"])

        completed: subprocess.CompletedProcess[str] | None = None
        for attempt in range(self.kimi_code_cli_retries + 1):
            try:
                completed = self._run_kimi_process(args)
            except Exception as e:
                message = str(e)
                if (
                    attempt >= self.kimi_code_cli_retries
                    or not self._is_retryable_kimi_cli_error(message)
                ):
                    raise RuntimeError(
                        "Kimi CLI 调用失败: "
                        f"{self._truncate_error(message)}"
                    ) from e
                time.sleep(self.kimi_code_cli_retry_delay * (attempt + 1))
                continue

            if completed.returncode == 0:
                break
            message = completed.stderr.strip() or completed.stdout.strip()
            if (
                attempt >= self.kimi_code_cli_retries
                or not self._is_retryable_kimi_cli_error(message)
            ):
                break
            time.sleep(self.kimi_code_cli_retry_delay * (attempt + 1))

        if completed is None or completed.returncode != 0:
            message = ""
            if completed is not None:
                message = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(
                "Kimi CLI 调用失败: " f"{self._truncate_error(message)}"
            )

        return self._clean_kimi_cli_output(completed.stdout)

    def _run_kimi_process(
        self,
        args: list[str],
    ) -> subprocess.CompletedProcess[str]:
        """Run one Kimi CLI process while tracking it for fail-fast cleanup."""
        process = subprocess.Popen(
            args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        with self._active_processes_lock:
            self._active_processes.add(process)
        try:
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
            except subprocess.TimeoutExpired as exc:
                self._terminate_process_tree(process)
                try:
                    stdout, stderr = process.communicate(timeout=5)
                except Exception:
                    stdout, stderr = "", ""
                raise RuntimeError(
                    f"Kimi CLI 调用超时: {self.timeout}s"
                ) from exc
            return subprocess.CompletedProcess(
                args=args,
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr,
            )
        finally:
            with self._active_processes_lock:
                self._active_processes.discard(process)

    def terminate_active_processes(self) -> None:
        """Terminate active Kimi CLI processes started by this client."""
        with self._active_processes_lock:
            processes = list(self._active_processes)
        for process in processes:
            self._terminate_process_tree(process)

    @staticmethod
    def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
        """Terminate a Kimi CLI process and its child process tree when possible."""
        try:
            if process.poll() is not None:
                return
        except Exception:
            pass

        if os.name == "nt":
            try:
                subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                )
                return
            except Exception:
                pass

        try:
            process.terminate()
        except Exception:
            pass
        try:
            process.wait(timeout=5)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass

    @staticmethod
    def _is_retryable_kimi_cli_error(message: str) -> bool:
        """判断 Kimi CLI 失败是否适合短退避重试。"""
        retryable_markers = [
            "provider.rate_limit",
            "429",
            "provider.connection_error",
            "Connection error",
            "high risk",
        ]
        return any(marker in message for marker in retryable_markers)

    @staticmethod
    def _truncate_error(message: str, limit: int = 800) -> str:
        """避免模型长输出污染日志。"""
        if len(message) <= limit:
            return message
        return message[:limit] + "...[truncated]"

    @staticmethod
    def _clean_kimi_cli_output(raw: str) -> str:
        """清理 Kimi CLI prompt mode 的项目符号和 session 提示。"""
        cleaned_lines: list[str] = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("To resume this session:"):
                continue
            if stripped.startswith("• "):
                stripped = stripped[2:].strip()
            cleaned_lines.append(stripped)
        return "\n".join(cleaned_lines).strip()

    @staticmethod
    def _extract_json_text(raw: str) -> str:
        """从模型输出中提取第一个 JSON 对象或数组。"""
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw = "\n".join(lines).strip()

        import json

        decoder = json.JSONDecoder()
        for idx, char in enumerate(raw):
            if char not in "{[":
                continue
            try:
                _, end = decoder.raw_decode(raw[idx:])
            except json.JSONDecodeError:
                continue
            return raw[idx : idx + end]
        return raw

    def call_json(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> dict[str, Any]:
        """调用 LLM API 并解析 JSON 响应

        在 system_prompt 中自动追加 JSON 输出要求。
        """
        json_system = (
            "你必须以有效的 JSON 格式输出，不要包含任何其他文本。"
        )
        if system_prompt:
            system_prompt = f"{system_prompt}\n\n{json_system}"
        else:
            system_prompt = json_system

        raw = self.call(prompt, system_prompt)
        import json

        return json.loads(self._extract_json_text(raw))
