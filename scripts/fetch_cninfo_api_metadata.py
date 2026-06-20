"""Fetch per-interface metadata for all CNINFO APIs via the public apiDoc/info endpoint.

This script is independent of the production crawler. It only enriches the local
official-API documentation archive. The actual announcement data still flows through
the public frontend endpoint `www.cninfo.com.cn/new/hisAnnouncement/query`.

Usage:
    uv run python scripts/fetch_cninfo_api_metadata.py
    uv run python scripts/fetch_cninfo_api_metadata.py --limit 5 --no-checkpoint
    uv run python scripts/fetch_cninfo_api_metadata.py --concurrency 20
    uv run python scripts/fetch_cninfo_api_metadata.py --retry-failed
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger
from tqdm import tqdm

# Project paths. Keep consistent with scripts/generate_cninfo_api_docs.py.
PROJECT_ROOT = Path(r'c:\Users\Vertin2000\上经贸大\数据挖掘与机器学习\project2')
GATEWAY_CODES_PATH = PROJECT_ROOT / 'cninfo_api_gateway_codes.json'
OUTPUT_PATH = PROJECT_ROOT / 'cninfo_api_metadata.json'
CHECKPOINT_DIR = PROJECT_ROOT / '.tmp'
CHECKPOINT_PATH = CHECKPOINT_DIR / 'cninfo_api_metadata_checkpoint.jsonl'

API_URL = 'https://webapi.cninfo.com.cn/api-cloud-gateway-manage/apiDoc/info'
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/125.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://webapi.cninfo.com.cn/',
}

DEFAULT_CONCURRENCY = 10
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_BATCH_SIZE = 100
DEFAULT_REQUEST_DELAY = 0.05


def load_checkpoint(path: Path) -> tuple[set[str], dict[str, str]]:
    """Return (successful_codes, failed_code_to_error) from a JSONL checkpoint."""
    success: set[str] = set()
    failures: dict[str, str] = {}
    if not path.exists():
        return success, failures
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                logger.warning('Checkpoint line malformed: %s', line[:80])
                continue
            code = record.get('gateway_code')
            if not code:
                continue
            status = record.get('status')
            if status == 'success':
                success.add(code)
                failures.pop(code, None)
            elif status == 'failed':
                failures[code] = record.get('error', 'unknown')
    return success, failures


def append_checkpoint(path: Path, code: str, status: str, error: str | None = None) -> None:
    """Append a single checkpoint record to the JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        'gateway_code': code,
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'status': status,
    }
    if error:
        record['error'] = error
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def _jittered_backoff(attempt: int) -> float:
    """Exponential backoff with small jitter."""
    return (2 ** attempt) + random.uniform(0, 1)


async def fetch_one(
    gateway_code: str,
    client: httpx.AsyncClient,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> dict | None:
    """Fetch metadata for a single gateway code with retries.

    Returns the raw ``data`` payload from the API response, or ``None`` on
    permanent failure. The payload is kept intact, including ``example`` fields.
    """
    for attempt in range(max_retries):
        try:
            resp = await client.get(
                API_URL,
                params={'gatewayCode': gateway_code},
                headers=HEADERS,
                timeout=DEFAULT_TIMEOUT,
            )
            if resp.status_code == 429:
                wait = _jittered_backoff(attempt)
                logger.warning('Rate limited for {}, waiting {:.1f}s', gateway_code, wait)
                await asyncio.sleep(wait)
                continue
            if 400 <= resp.status_code < 500:
                logger.error('Client error {} for {}, skipping', resp.status_code, gateway_code)
                return None
            resp.raise_for_status()
            payload = resp.json()
            if payload.get('code') not in (200, '000000') or 'data' not in payload:
                logger.warning('Unexpected response for {}: {}', gateway_code, payload.get('msg'))
                return None
            return payload['data']
        except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as exc:
            wait = _jittered_backoff(attempt)
            logger.warning(
                'Network error for {} (attempt {}/{}): {}, retrying in {:.1f}s',
                gateway_code, attempt + 1, max_retries, exc, wait,
            )
            await asyncio.sleep(wait)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code >= 500:
                wait = _jittered_backoff(attempt)
                logger.warning(
                    'Server error {} for {}, retrying in {:.1f}s',
                    exc.response.status_code, gateway_code, wait,
                )
                await asyncio.sleep(wait)
            else:
                logger.error('HTTP error for {}: {}', gateway_code, exc)
                return None
        except json.JSONDecodeError as exc:
            logger.error('JSON decode error for {}: {}', gateway_code, exc)
            return None
        except Exception as exc:  # pragma: no cover - defensive
            logger.error('Unexpected error for {}: {}', gateway_code, exc)
            return None
    logger.error('Max retries exceeded for {}', gateway_code)
    return None


async def fetch_batch(
    codes: Sequence[str],
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    checkpoint_path: Path,
    pbar: tqdm,
) -> tuple[dict[str, dict], dict[str, str]]:
    """Fetch a batch of codes with bounded concurrency and write checkpoints."""
    results: dict[str, dict] = {}
    failures: dict[str, str] = {}

    async def _fetch(code: str) -> None:
        async with semaphore:
            data = await fetch_one(code, client)
            if data is not None:
                results[code] = data
                append_checkpoint(checkpoint_path, code, 'success')
            else:
                failures[code] = 'permanent failure'
                append_checkpoint(checkpoint_path, code, 'failed', 'permanent failure')
            pbar.update(1)
            await asyncio.sleep(DEFAULT_REQUEST_DELAY)

    await asyncio.gather(*[_fetch(code) for code in codes])
    return results, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fetch CNINFO API per-interface metadata archive.',
    )
    parser.add_argument(
        '--concurrency',
        type=int,
        default=DEFAULT_CONCURRENCY,
        help=f'Max concurrent requests (default: {DEFAULT_CONCURRENCY})',
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f'Request timeout in seconds (default: {DEFAULT_TIMEOUT})',
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f'Max retries per code (default: {DEFAULT_MAX_RETRIES})',
    )
    parser.add_argument(
        '--retry-failed',
        action='store_true',
        help='Only retry codes that previously failed',
    )
    parser.add_argument(
        '--no-checkpoint',
        action='store_true',
        help='Ignore existing checkpoint and start fresh',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Fetch only the first N codes (useful for testing)',
    )
    return parser.parse_args()


def load_unique_gateway_codes(path: Path) -> list[str]:
    """Load the gateway code index and return unique codes in stable order."""
    with open(path, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    # Preserve first-seen order while deduplicating.
    seen: set[str] = set()
    codes: list[str] = []
    for entry in entries:
        code = entry.get('code')
        if code and code not in seen:
            seen.add(code)
            codes.append(code)
    return codes


def load_existing_results(path: Path) -> dict[str, dict]:
    """Load results from a previous output file if it exists."""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('results', {})


async def main() -> int:
    args = parse_args()

    if not GATEWAY_CODES_PATH.exists():
        logger.error('Gateway code index not found: {}', GATEWAY_CODES_PATH)
        return 1

    all_codes = load_unique_gateway_codes(GATEWAY_CODES_PATH)
    logger.info('Total unique gateway codes: {}', len(all_codes))

    success_codes: set[str] = set()
    failed_codes: dict[str, str] = {}
    existing_results: dict[str, dict] = {}

    if not args.no_checkpoint:
        success_codes, failed_codes = load_checkpoint(CHECKPOINT_PATH)
        logger.info('Checkpoint: {} success, {} failed', len(success_codes), len(failed_codes))
        existing_results = load_existing_results(OUTPUT_PATH)

    if args.retry_failed:
        codes_to_fetch = [c for c in all_codes if c in failed_codes]
    else:
        codes_to_fetch = [c for c in all_codes if c not in success_codes]

    if args.limit is not None:
        codes_to_fetch = codes_to_fetch[: args.limit]
        logger.info('Test mode: limited to {} codes', len(codes_to_fetch))

    if not codes_to_fetch:
        logger.info('Nothing to fetch.')
        return 0

    logger.info('Codes to fetch: {}', len(codes_to_fetch))

    all_results: dict[str, dict] = dict(existing_results)
    all_failures: dict[str, str] = {}

    semaphore = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        with tqdm(total=len(codes_to_fetch), desc='Fetching metadata') as pbar:
            for i in range(0, len(codes_to_fetch), DEFAULT_BATCH_SIZE):
                batch = codes_to_fetch[i : i + DEFAULT_BATCH_SIZE]
                results, failures = await fetch_batch(
                    batch, client, semaphore, CHECKPOINT_PATH, pbar
                )
                all_results.update(results)
                all_failures.update(failures)

    output = {
        'metadata': {
            'source': API_URL,
            'fetchedAt': datetime.now(timezone.utc).isoformat(),
            'totalApis': len(all_codes),
            'successful': len(all_results),
            'failed': len(all_failures),
            'concurrency': args.concurrency,
            'timeoutSeconds': args.timeout,
            'maxRetries': args.max_retries,
        },
        'results': all_results,
        'failures': {
            code: {
                'error': error,
                'lastAttempt': datetime.now(timezone.utc).isoformat(),
            }
            for code, error in all_failures.items()
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    logger.info('Wrote {}', OUTPUT_PATH)
    logger.info('Successful: {}/{}', len(all_results), len(all_codes))
    if all_failures:
        logger.warning('Failed codes ({}): {}...', len(all_failures), list(all_failures.keys())[:5])

    return 0 if len(all_failures) == 0 else 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
