"""Binary bounce simulation API namespace."""

from __future__ import annotations

import time
from typing import Any, Generator

from .models import BinaryStream, BounceResult, BounceStrategy
from .utils import generate_id, random_binary_state, random_float, utcnow_iso


class BounceAPI:
    """Namespace for binary bounce simulation endpoints.

    Accessed via ``client.bounce``.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    # --------------------------------------------------------------------- #
    # Public methods
    # --------------------------------------------------------------------- #

    def simulate(
        self,
        initial_state: list[int] | None = None,
        *,
        iterations: int = 100,
        strategy: BounceStrategy | str = BounceStrategy.DETERMINISTIC,
        energy_threshold: float = 0.01,
        metadata: dict[str, Any] | None = None,
    ) -> BounceResult:
        """Run a binary bounce simulation.

        Parameters
        ----------
        initial_state:
            Starting binary state vector.  If *None* a random 8-bit state is
            generated.
        iterations:
            Maximum number of bounce iterations.
        strategy:
            Simulation strategy to use.
        energy_threshold:
            Energy convergence threshold.
        metadata:
            Optional key/value metadata attached to the result.
        """
        if isinstance(strategy, str):
            strategy = BounceStrategy(strategy)

        if initial_state is None:
            initial_state = random_binary_state(8)

        # Simulate convergence with mock data.
        final_state = random_binary_state(len(initial_state))
        convergence = random_float(0.92, 0.999)
        elapsed = random_float(12.0, 350.0, decimals=2)

        return BounceResult(
            id=generate_id("bnc"),
            status="completed",
            iterations=iterations,
            convergence=convergence,
            binary_state=final_state,
            energy_delta=random_float(-0.05, 0.05),
            elapsed_ms=elapsed,
            metadata={
                **(metadata or {}),
                "strategy": strategy.value,
                "energy_threshold": energy_threshold,
                "initial_state": initial_state,
            },
        )

    def stream(
        self,
        initial_state: list[int] | None = None,
        *,
        iterations: int = 20,
        strategy: BounceStrategy | str = BounceStrategy.STOCHASTIC,
    ) -> Generator[BinaryStream, None, None]:
        """Stream bounce simulation frames as they are computed.

        Yields :class:`BinaryStream` objects one per iteration.

        Parameters
        ----------
        initial_state:
            Starting binary state vector.
        iterations:
            Number of frames to produce.
        strategy:
            Simulation strategy.
        """
        if isinstance(strategy, str):
            strategy = BounceStrategy(strategy)

        if initial_state is None:
            initial_state = random_binary_state(8)

        state = list(initial_state)
        start = time.monotonic()

        for i in range(iterations):
            # Mutate one random bit to simulate a bounce step.
            import random
            idx = random.randrange(len(state))
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
