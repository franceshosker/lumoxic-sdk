"""Training job API namespace."""

from __future__ import annotations

from typing import Any

from .models import JobStatus, TrainingJob
from .utils import generate_id, random_float, utcnow_iso


class TrainingAPI:
    """Namespace for model training endpoints.

    Accessed via ``client.training``.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    # --------------------------------------------------------------------- #
    # Public methods
    # --------------------------------------------------------------------- #

    def create(
        self,
        name: str,
        model_id: str,
        *,
        config: dict[str, Any] | None = None,
    ) -> TrainingJob:
        """Create a new training job.

        Parameters
        ----------
        name:
            Human-readable name for the training run.
        model_id:
            Base model identifier to fine-tune.
        config:
            Training hyperparameters (learning_rate, epochs, batch_size, etc.).
        """
        job_id = generate_id("trn")
        return TrainingJob(
            id=job_id,
            name=name,
            status=JobStatus.PENDING,
            model_id=model_id,
            created_at=utcnow_iso(),
            started_at=None,
            completed_at=None,
            progress=0.0,
            metrics={},
            config=config or {
                "learning_rate": 1e-4,
                "epochs": 10,
                "batch_size": 32,
            },
        )

    def status(self, job_id: str) -> TrainingJob:
        """Retrieve the current status of a training job.

        Parameters
        ----------
        job_id:
            The training job identifier.
        """
        # Mock a running job with partial progress.
        return TrainingJob(
            id=job_id,
            name="mock-training-run",
            status=JobStatus.RUNNING,
            model_id="lmx-photon-base-v2",
            created_at=utcnow_iso(),
            started_at=utcnow_iso(),
            completed_at=None,
            progress=random_float(0.10, 0.85),
            metrics={
                "loss": random_float(0.01, 0.5),
                "accuracy": random_float(0.75, 0.98),
                "learning_rate": 1e-4,
            },
            config={"learning_rate": 1e-4, "epochs": 10, "batch_size": 32},
        )

    def cancel(self, job_id: str) -> TrainingJob:
        """Cancel a running training job.

        Parameters
        ----------
        job_id:
            The training job identifier.
        """
        return TrainingJob(
            id=job_id,
            name="mock-training-run",
            status=JobStatus.CANCELLED,
            model_id="lmx-photon-base-v2",
            created_at=utcnow_iso(),
            started_at=utcnow_iso(),
            completed_at=utcnow_iso(),
            progress=0.0,
            metrics={},
            config={},
        )

    def list(self, *, limit: int = 20, offset: int = 0) -> list[TrainingJob]:
        """List training jobs.

        Parameters
        ----------
        limit:
            Maximum number of jobs to return.
        offset:
            Pagination offset.
        """
        # Return a small mock list.
        jobs = []
        for i in range(min(limit, 3)):
            jobs.append(
                TrainingJob(
                    id=generate_id("trn"),
                    name=f"training-run-{i + 1}",
                    status=JobStatus.COMPLETED if i < 2 else JobStatus.RUNNING,
                    model_id="lmx-photon-base-v2",
                    created_at=utcnow_iso(),
                    started_at=utcnow_iso(),
                    completed_at=utcnow_iso() if i < 2 else None,
                    progress=1.0 if i < 2 else random_float(0.3, 0.7),
                    metrics={"loss": random_float(0.01, 0.1), "accuracy": random_float(0.90, 0.99)},
                    config={"learning_rate": 1e-4, "epochs": 10},
                )
            )
        return jobs
