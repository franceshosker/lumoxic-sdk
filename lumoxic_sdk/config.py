"""Configuration management for the Lumoxic SDK."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


DEFAULT_BASE_URL = "https://api.lumoxic.ai/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

ENV_API_KEY = "LUMOXIC_API_KEY"
ENV_BASE_URL = "LUMOXIC_BASE_URL"
ENV_TIMEOUT = "LUMOXIC_TIMEOUT"


@dataclass
class LumoxicConfig:
    """Configuration for the Lumoxic API client.

    Attributes:
        api_key: Your Lumoxic API key. Falls back to the LUMOXIC_API_KEY
            environment variable if not provided.
        base_url: Base URL for the Lumoxic API. Defaults to
            ``https://api.lumoxic.ai/v1``.
        timeout: Request timeout in seconds. Defaults to 30.
        max_retries: Maximum number of retries for transient failures.
            Defaults to 3.
        headers: Additional HTTP headers to include in every request.
    """

    api_key: str | None = None
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Resolve from environment if not explicitly provided.
        if self.api_key is None:
            self.api_key = os.environ.get(ENV_API_KEY)

        env_base = os.environ.get(ENV_BASE_URL)
        if env_base and self.base_url == DEFAULT_BASE_URL:
            self.base_url = env_base

        env_timeout = os.environ.get(ENV_TIMEOUT)
        if env_timeout:
            try:
                self.timeout = float(env_timeout)
            except ValueError:
                pass

        # Strip trailing slashes for consistency.
        self.base_url = self.base_url.rstrip("/")

    def validate(self) -> None:
        """Raise if the configuration is incomplete."""
        from .exceptions import AuthenticationError

        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key to the client or set the "
                f"{ENV_API_KEY} environment variable."
            )

    @property
    def auth_headers(self) -> dict[str, str]:
        """Return headers that include the Authorization bearer token."""
        base = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "lumoxic-sdk-python/0.1.0",
        }
        base.update(self.headers)
        return base
