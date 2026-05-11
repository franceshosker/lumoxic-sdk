"""Asynchronous Lumoxic API client."""

from __future__ import annotations

import asyncio
from typing import Any, AsyncGenerator

from .config import LumoxicConfig
from .models import (
    BatchPhotonResult,
    BinaryStream,
    BounceResult,
    BounceStrategy,
    Model,
    PhotonAnalysis,
    PhotonMode,
    PhotonResult,
    TrainingJob,
)
from .utils import generate_id, random_binary_state, random_float, random_spectrum, utcnow_iso


class AsyncLumoxicClient:
    """Async version of the Lumoxic AI client.

    Usage::

        import asyncio
        from lumoxic_sdk import AsyncLumoxicClient

        async def main():
            client = AsyncLumoxicClient(api_key="lmx-...")
            result = await client.photon.process(wavelength=550.0, intensity=0.8)
            print(result)

        asyncio.run(main())

    Parameters
    ----------
    api_key:
        Your Lumoxic API key.
    base_url:
        Override the default API base URL.
    timeout:
        Request timeout in seconds.
    max_retries:
        Maximum automatic retries for transient errors.
    headers:
        Additional HTTP headers.
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
        self._config.validate()

        self.photon = _AsyncPhotonAPI(self)
        self.bounce = _AsyncBounceAPI(self)
        self.training = _AsyncTrainingAPI(self)
        self.models = _AsyncModelsAPI(self)

    @property
    def config(self) -> LumoxicConfig:
        return self._config

    async def close(self) -> None:
        """Close the underlying HTTP session (no-op in demo mode)."""
        pass

    async def __aenter__(self) -> AsyncLumoxicClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return (
            f"AsyncLumoxicClient(base_url={self._config.base_url!r}, "
            f"timeout={self._config.timeout})"
        )


# ====================================================================== #
# Async API namespaces
# ====================================================================== #


class _AsyncPhotonAPI:
    def __init__(self, client: AsyncLumoxicClient) -> None:
        self._client = client

    async def process(
        self,
        wavelength: float,
        intensity: float,
        *,
        mode: PhotonMode | str = PhotonMode.STANDARD,
        metadata: dict[str, Any] | None = None,
    ) -> PhotonResult:
        """Process a single photon measurement (async)."""
        await asyncio.sleep(0)  # Yield to event loop (simulates I/O).
        return PhotonResult(
            id=generate_id("pht"),
            status="completed",
            wavelength=wavelength,
            intensity=intensity,
            coherence_score=random_float(0.85, 0.99),
            processed_at=utcnow_iso(),
            metadata=metadata or {},
        )

    async def analyze(self, photon_id: str, *, depth: int = 5) -> PhotonAnalysis:
        """Analyze a photon result (async)."""
        await asyncio.sleep(0)
        spectrum = random_spectrum(depth * 2)
        return PhotonAnalysis(
            id=generate_id("pan"),
            spectrum=spectrum,
            peak_wavelength=max(spectrum),
            energy_distribution={
                "ultraviolet": random_float(0.01, 0.15),
                "visible": random_float(0.50, 0.80),
                "infrared": random_float(0.05, 0.25),
            },
            confidence=random_float(0.90, 0.99),
            metadata={"source_photon": photon_id, "depth": depth},
        )

    async def batch(
        self,
        items: list[dict[str, Any]],
        *,
        mode: PhotonMode | str = PhotonMode.STANDARD,
    ) -> BatchPhotonResult:
        """Batch process photon measurements (async)."""
        results = []
        for item in items:
            r = await self.process(
                wavelength=item["wavelength"],
                intensity=item["intensity"],
                mode=mode,
                metadata=item.get("metadata"),
            )
            results.append(r)
        return BatchPhotonResult(
            batch_id=generate_id("bat"),
            results=results,
            total=len(items),
            succeeded=len(results),
            failed=0,
        )


class _AsyncBounceAPI:
    def __init__(self, client: AsyncLumoxicClient) -> None:
        self._client = client

    async def simulate(
        self,
        initial_state: list[int] | None = None,
        *,
        iterations: int = 100,
        strategy: BounceStrategy | str = BounceStrategy.DETERMINISTIC,
        energy_threshold: float = 0.01,
        metadata: dict[str, Any] | None = None,
    ) -> BounceResult:
        """Run a bounce simulation (async)."""
        await asyncio.sleep(0)
        if initial_state is None:
            initial_state = random_binary_state(8)
        return BounceResult(
            id=generate_id("bnc"),
            status="completed",
            iterations=iterations,
            convergence=random_float(0.92, 0.999),
            binary_state=random_binary_state(len(initial_state)),
            energy_delta=random_float(-0.05, 0.05),
            elapsed_ms=random_float(12.0, 350.0, decimals=2),
            metadata={
                **(metadata or {}),
                "strategy": strategy if isinstance(strategy, str) else strategy.value,
                "initial_state": initial_state,
            },
        )

    async def stream(
        self,
        initial_state: list[int] | None = None,
        *,
        iterations: int = 20,
        strategy: BounceStrategy | str = BounceStrategy.STOCHASTIC,
    ) -> AsyncGenerator[BinaryStream, None]:
        """Stream bounce frames (async generator)."""
        import random as _random
        import time

        if initial_state is None:
            initial_state = random_binary_state(8)
        state = list(initial_state)
        start = time.monotonic()

        for i in range(iterations):
            await asyncio.sleep(0)
            idx = _random.randrange(len(state))
            state[idx] ^= 1
            energy = random_float(0.0, 1.0)
            converged = energy < 0.05 and i > iterations // 2

            yield BinaryStream(
                frame_index=i,
                timestamp=round(time.monotonic() - start, 6),
                binary_state=list(state),
                energy=energy,
                converged=converged,
            )
            if converged:
                break


class _AsyncTrainingAPI:
    def __init__(self, client: AsyncLumoxicClient) -> None:
        self._client = client

    async def create(
        self,
        name: str,
        model_id: str,
        *,
        config: dict[str, Any] | None = None,
    ) -> TrainingJob:
        """Create a training job (async)."""
        await asyncio.sleep(0)
        from .models import JobStatus
        return TrainingJob(
            id=generate_id("trn"),
            name=name,
            status=JobStatus.PENDING,
            model_id=model_id,
            created_at=utcnow_iso(),
            progress=0.0,
            config=config or {"learning_rate": 1e-4, "epochs": 10, "batch_size": 32},
        )

    async def status(self, job_id: str) -> TrainingJob:
        """Get training job status (async)."""
        await asyncio.sleep(0)
        from .models import JobStatus
        return TrainingJob(
            id=job_id,
            name="mock-training-run",
            status=JobStatus.RUNNING,
            model_id="lmx-photon-base-v2",
            created_at=utcnow_iso(),
            started_at=utcnow_iso(),
            progress=random_float(0.10, 0.85),
            metrics={"loss": random_float(0.01, 0.5), "accuracy": random_float(0.75, 0.98)},
            config={"learning_rate": 1e-4, "epochs": 10},
        )

    async def cancel(self, job_id: str) -> TrainingJob:
        """Cancel a training job (async)."""
        await asyncio.sleep(0)
        from .models import JobStatus
        return TrainingJob(
            id=job_id,
            name="mock-training-run",
            status=JobStatus.CANCELLED,
            model_id="lmx-photon-base-v2",
            created_at=utcnow_iso(),
            completed_at=utcnow_iso(),
            progress=0.0,
        )


class _AsyncModelsAPI:
    def __init__(self, client: AsyncLumoxicClient) -> None:
        self._client = client

    async def list(self, *, limit: int = 20, offset: int = 0) -> list[Model]:
        """List available models (async)."""
        await asyncio.sleep(0)
        from .models_api import ModelsAPI
        api = ModelsAPI(None)
        return api.list(limit=limit, offset=offset)

    async def get(self, model_id: str) -> Model:
        """Get a model by ID (async)."""
        await asyncio.sleep(0)
        from .models_api import ModelsAPI
        api = ModelsAPI(None)
        return api.get(model_id)

    async def deploy(
        self,
        model_id: str,
        *,
        replicas: int = 1,
        accelerator: str = "gpu-a100",
    ) -> dict[str, Any]:
        """Deploy a model (async)."""
        await asyncio.sleep(0)
        from .models_api import ModelsAPI
        api = ModelsAPI(None)
        return api.deploy(model_id, replicas=replicas, accelerator=accelerator)
