"""Tests for the LumoxicClient."""

import os
import pytest

from lumoxic_sdk import LumoxicClient, AsyncLumoxicClient
from lumoxic_sdk.exceptions import AuthenticationError
from lumoxic_sdk.config import LumoxicConfig


class TestLumoxicClient:
    """Test the synchronous client."""

    def test_init_with_api_key(self):
        client = LumoxicClient(api_key="lmx-test-key-123")
        assert client.config.api_key == "lmx-test-key-123"

    def test_init_without_api_key_raises(self):
        # Ensure env var is not set.
        os.environ.pop("LUMOXIC_API_KEY", None)
        with pytest.raises(AuthenticationError, match="No API key"):
            LumoxicClient()

    def test_init_with_env_var(self, monkeypatch):
        monkeypatch.setenv("LUMOXIC_API_KEY", "lmx-env-key")
        client = LumoxicClient()
        assert client.config.api_key == "lmx-env-key"

    def test_custom_base_url(self):
        client = LumoxicClient(api_key="lmx-k", base_url="https://custom.api.test/v2")
        assert client.config.base_url == "https://custom.api.test/v2"

    def test_trailing_slash_stripped(self):
        client = LumoxicClient(api_key="lmx-k", base_url="https://api.test/v1/")
        assert not client.config.base_url.endswith("/")

    def test_namespaces_exist(self):
        client = LumoxicClient(api_key="lmx-k")
        assert hasattr(client, "photon")
        assert hasattr(client, "bounce")
        assert hasattr(client, "training")
        assert hasattr(client, "models")

    def test_repr(self):
        client = LumoxicClient(api_key="lmx-k")
        r = repr(client)
        assert "LumoxicClient" in r
        assert "lumoxic.ai" in r

    def test_custom_timeout(self):
        client = LumoxicClient(api_key="lmx-k", timeout=60.0)
        assert client.config.timeout == 60.0

    def test_custom_max_retries(self):
        client = LumoxicClient(api_key="lmx-k", max_retries=5)
        assert client.config.max_retries == 5


class TestLumoxicConfig:
    """Test configuration dataclass."""

    def test_defaults(self):
        cfg = LumoxicConfig(api_key="k")
        assert cfg.timeout == 30.0
        assert cfg.max_retries == 3

    def test_auth_headers(self):
        cfg = LumoxicConfig(api_key="lmx-abc")
        headers = cfg.auth_headers
        assert headers["Authorization"] == "Bearer lmx-abc"
        assert "User-Agent" in headers

    def test_validate_missing_key(self):
        os.environ.pop("LUMOXIC_API_KEY", None)
        cfg = LumoxicConfig()
        with pytest.raises(AuthenticationError):
            cfg.validate()
