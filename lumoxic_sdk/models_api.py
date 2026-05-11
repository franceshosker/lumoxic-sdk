"""Models registry API namespace."""

from __future__ import annotations

from typing import Any

from .models import Model
from .utils import generate_id, utcnow_iso


class ModelsAPI:
    """Namespace for model registry endpoints.

    Accessed via ``client.models``.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    # -- Mock model catalogue ------------------------------------------------

    _MOCK_MODELS = [
        {
            "id": "lmx-photon-base-v2",
            "name": "Photon Base v2",
            "version": "2.1.0",
            "description": "General-purpose photon processing model with broad spectrum support.",
            "status": "ready",
            "parameters": 125_000_000,
            "capabilities": ["process", "analyze", "batch"],
        },
        {
            "id": "lmx-bounce-turbo",
            "name": "Bounce Turbo",
            "version": "1.4.0",
            "description": "High-speed binary bounce simulation optimised for low latency.",
            "status": "ready",
            "parameters": 68_000_000,
            "capabilities": ["simulate", "stream"],
        },
        {
            "id": "lmx-unified-7b",
            "name": "Unified 7B",
            "version": "0.9.0",
            "description": "Experimental unified model for photon + bounce workloads.",
            "status": "beta",
            "parameters": 7_000_000_000,
            "capabilities": ["process", "analyze", "simulate", "stream", "batch"],
        },
    ]

    # --------------------------------------------------------------------- #
    # Public methods
    # --------------------------------------------------------------------- #

    def list(self, *, limit: int = 20, offset: int = 0) -> list[Model]:
        """List available models.

        Parameters
        ----------
        limit:
            Maximum number of models to return.
        offset:
            Pagination offset.
        """
        raw = self._MOCK_MODELS[offset : offset + limit]
        return [
            Model.from_dict({**m, "created_at": utcnow_iso()})
            for m in raw
        ]

    def get(self, model_id: str) -> Model:
        """Retrieve details for a single model.

        Parameters
        ----------
        model_id:
            The model identifier (e.g. ``lmx-photon-base-v2``).
        """
        for m in self._MOCK_MODELS:
            if m["id"] == model_id:
                return Model.from_dict({**m, "created_at": utcnow_iso()})

        # If not found, return a placeholder.
        from .exceptions import NotFoundError
        raise NotFoundError(f"Model '{model_id}' not found.")

    def deploy(
        self,
        model_id: str,
        *,
        replicas: int = 1,
        accelerator: str = "gpu-a100",
    ) -> dict[str, Any]:
        """Deploy a model to a serving endpoint.

        Parameters
        ----------
        model_id:
            The model to deploy.
        replicas:
            Number of serving replicas.
        accelerator:
            Hardware accelerator type.

        Returns
        -------
        dict
            Deployment metadata including endpoint URL.
        """
        return {
            "deployment_id": generate_id("dpl"),
            "model_id": model_id,
            "status": "deploying",
            "replicas": replicas,
            "accelerator": accelerator,
            "endpoint": f"https://serve.lumoxic.ai/v1/models/{model_id}",
            "created_at": utcnow_iso(),
        }
