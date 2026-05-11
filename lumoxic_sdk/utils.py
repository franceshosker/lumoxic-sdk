"""Utility helpers for the Lumoxic SDK."""

from __future__ import annotations

import random
import string
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from .exceptions import RateLimitError, ServerError, TimeoutError

T = TypeVar("T")


def generate_id(prefix: str = "lmx") -> str:
    """Generate a unique Lumoxic-style identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def utcnow() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def utcnow_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return utcnow().isoformat()


def random_float(low: float = 0.0, high: float = 1.0, decimals: int = 6) -> float:
    """Return a random float rounded to *decimals* places."""
    return round(random.uniform(low, high), decimals)


def random_binary_state(length: int = 8) -> list[int]:
    """Return a random binary state vector."""
    return [random.randint(0, 1) for _ in range(length)]


def random_spectrum(length: int = 10) -> list[float]:
    """Return a random spectrum array."""
    return [random_float(380.0, 780.0) for _ in range(length)]


def retry_with_backoff(
    fn: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    retryable: tuple[type[Exception], ...] = (RateLimitError, ServerError, TimeoutError),
) -> T:
    """Execute *fn* with exponential back-off on transient errors.

    Parameters
    ----------
    fn:
        A zero-argument callable to execute.
    max_retries:
        Number of retries after the initial attempt.
    base_delay:
        Initial delay in seconds (doubled each retry).
    max_delay:
        Maximum delay cap in seconds.
    retryable:
        Exception types that trigger a retry.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except retryable as exc:
            last_exc = exc
            if attempt == max_retries:
                raise
            delay = min(base_delay * (2 ** attempt) + random.random(), max_delay)
            time.sleep(delay)
    # Should not reach here, but satisfy the type checker.
    raise last_exc  # type: ignore[misc]


def build_url(base: str, *segments: str) -> str:
    """Join URL path segments onto a base URL."""
    parts = [base.rstrip("/")]
    for seg in segments:
        parts.append(seg.strip("/"))
    return "/".join(parts)


def build_headers(
    api_key: str,
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Construct standard request headers."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "lumoxic-sdk-python/0.1.0",
    }
    if extra:
        headers.update(extra)
    return headers
