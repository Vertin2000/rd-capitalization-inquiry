"""Tests for CNINFO API metadata fetcher."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from scripts.fetch_cninfo_api_metadata import (
    API_URL,
    append_checkpoint,
    fetch_one,
    load_checkpoint,
    load_unique_gateway_codes,
)


class FakeResponse:
    """Minimal httpx.Response stand-in for tests."""

    def __init__(
        self,
        status_code: int,
        json_data: dict | None = None,
        text: str = '',
    ) -> None:
        self.status_code = status_code
        self._json = json_data
        self.text = text or json.dumps(json_data)

    def json(self) -> dict:
        if self._json is None:
            raise json.JSONDecodeError('Expecting value', self.text, 0)
        return self._json

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f'{self.status_code} error',
                request=MagicMock(),
                response=MagicMock(status_code=self.status_code),
            )


@pytest.mark.anyio
async def test_fetch_one_success() -> None:
    client = AsyncMock()
    client.get = AsyncMock(
        return_value=FakeResponse(
            200,
            {
                'code': 200,
                'msg': 'success',
                'data': {'baseInfo': {'name': 'test_api'}},
            },
        ),
    )
    result = await fetch_one('abc123', client, max_retries=1)
    assert result == {'baseInfo': {'name': 'test_api'}}
    client.get.assert_awaited_once()
    call = client.get.await_args
    assert call.args[0] == API_URL
    assert call.kwargs['params'] == {'gatewayCode': 'abc123'}
    assert 'headers' in call.kwargs
    assert call.kwargs['timeout'] == 30


@pytest.mark.anyio
async def test_fetch_one_url_and_params() -> None:
    client = AsyncMock()
    client.get = AsyncMock(
        return_value=FakeResponse(
            200,
            {'code': 200, 'msg': 'success', 'data': {'requestConfig': {}}},
        ),
    )
    await fetch_one('uuid-001', client, max_retries=1)
    call = client.get.await_args
    assert call.kwargs['params'] == {'gatewayCode': 'uuid-001'}
    assert call.args[0] == API_URL


@pytest.mark.anyio
async def test_fetch_one_retry_then_success() -> None:
    client = AsyncMock()
    client.get = AsyncMock(
        side_effect=[
            httpx.TimeoutException('timeout'),
            FakeResponse(
                200,
                {
                    'code': 200,
                    'msg': 'success',
                    'data': {'baseInfo': {'name': 'test_api'}},
                },
            ),
        ],
    )
    result = await fetch_one('abc123', client, max_retries=2)
    assert result == {'baseInfo': {'name': 'test_api'}}
    assert client.get.await_count == 2


@pytest.mark.anyio
async def test_fetch_one_permanent_failure_404() -> None:
    client = AsyncMock()
    client.get = AsyncMock(return_value=FakeResponse(404, {}))
    result = await fetch_one('abc123', client, max_retries=3)
    assert result is None
    assert client.get.await_count == 1  # No retries for 4xx


@pytest.mark.anyio
async def test_fetch_one_api_error_response() -> None:
    client = AsyncMock()
    client.get = AsyncMock(
        return_value=FakeResponse(
            200,
            {'code': 500, 'msg': 'internal error', 'data': None},
        ),
    )
    result = await fetch_one('abc123', client, max_retries=1)
    assert result is None


@pytest.mark.anyio
async def test_fetch_one_json_decode_error() -> None:
    client = AsyncMock()
    client.get = AsyncMock(return_value=FakeResponse(200, text='not json'))
    result = await fetch_one('abc123', client, max_retries=1)
    assert result is None


def test_checkpoint_roundtrip(tmp_path: Path) -> None:
    checkpoint = tmp_path / 'checkpoint.jsonl'
    append_checkpoint(checkpoint, 'code1', 'success')
    append_checkpoint(checkpoint, 'code2', 'failed', 'timeout')
    success, failed = load_checkpoint(checkpoint)
    assert success == {'code1'}
    assert failed == {'code2': 'timeout'}


def test_checkpoint_ignores_malformed_lines(tmp_path: Path) -> None:
    checkpoint = tmp_path / 'checkpoint.jsonl'
    checkpoint.write_text(
        '{"gateway_code": "good", "status": "success"}\n'
        'this is not json\n'
        '{"gateway_code": "bad", "status": "failed", "error": "boom"}\n',
        encoding='utf-8',
    )
    success, failed = load_checkpoint(checkpoint)
    assert success == {'good'}
    assert failed == {'bad': 'boom'}


def test_checkpoint_overwrites_failed_with_success(tmp_path: Path) -> None:
    checkpoint = tmp_path / 'checkpoint.jsonl'
    append_checkpoint(checkpoint, 'code1', 'failed', 'timeout')
    append_checkpoint(checkpoint, 'code1', 'success')
    success, failed = load_checkpoint(checkpoint)
    assert success == {'code1'}
    assert 'code1' not in failed


def test_load_unique_gateway_codes(tmp_path: Path) -> None:
    path = tmp_path / 'codes.json'
    path.write_text(
        json.dumps(
            [
                {'name': 'a1', 'code': 'c1'},
                {'name': 'a2', 'code': 'c2'},
                {'name': 'a3', 'code': 'c1'},  # duplicate
                {'name': 'a4', 'code': 'c3'},
            ],
            ensure_ascii=False,
        ),
        encoding='utf-8',
    )
    codes = load_unique_gateway_codes(path)
    assert codes == ['c1', 'c2', 'c3']
