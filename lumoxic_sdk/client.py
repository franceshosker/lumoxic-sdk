"""Synchronous Lumoxic API client."""

from __future__ import annotations

from typing import Any

from .bounce import BounceAPI
from .config import LumoxicConfig
from .models_api import ModelsAPI
from .photon import PhotonAPI
from .training import TrainingAPI


class LumoxicClient:
    """Main entry-point for the Lumoxic AI SDK.

    Usage::

        from lumoxic_sdk import LumoxicClient

        client = LumoxicClient(api_key="lmx-...")

        # Photon processing
        result = client.photon.process(wavelength=550.0, intensity=0.8)

        # Binary bounce simulation
        bounce = client.bounce.simulate(iterations=200)

        # Model management
        models = client.models.list()

    Parameters
    ----------
    api_key:
        Your Lumoxic API key.  If omitted, the ``LUMOXIC_API_KEY``
        environment variable is used.
    base_url:
        Override the default API base URL.
    timeout:
        Request timeout in seconds.
    max_retries:
        Maximum automatic retries for transient errors.
    headers:
        Additional HTTP headers sent with every request.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        kwargs: dict[str, Any] = {}
        if api_key is not None:
            kwargs["api_key"] = api_key
        if base_url is not None:
            kwargs["base_url"] = base_url
        if timeout is not None:
            kwargs["timeout"] = timeout
        if max_retries is not None:
            kwargs["max_retries"] = max_retries
        if headers is not None:
            kwargs["headers"] = headers

        self._config = LumoxicConfig(**kwargs)

        # Eagerly validate so callers get a clear error at init time.
        self._config.validate()

        # API namespaces
        self.photon = PhotonAPI(self)
        self.bounce = BounceAPI(self)
        self.training = TrainingAPI(self)
        self.models = ModelsAPI(self)

    # ------------------------------------------------------------------ #
    # Internal helpers (used by namespace classes for real HTTP calls)
    # ------------------------------------------------------------------ #

    @property
    def config(self) -> LumoxicConfig:
        """Return the active configuration."""
        return self._config

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send an HTTP request to the Lumoxic API.

        This is a stub that would use ``httpx`` in a production SDK.
        For now it raises ``NotImplementedError`` because all public
        methods return mock data directly.
        """
        raise NotImplementedError(
            "HTTP transport is not implemented in this demo SDK. "
            "All public methods return mock data."
        )

    def __repr__(self) -> str:
        return (
            f"LumoxicClient(base_url={self._config.base_url!r}, "
            f"timeout={self._config.timeout})"
        )
