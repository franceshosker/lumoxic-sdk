"""Response models for the Lumoxic SDK.

Uses :mod:`dataclasses` with a lightweight ``from_dict`` helper so the SDK
works with zero required dependencies beyond the standard library.
Pydantic is available as an optional extra.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PhotonMode(str, Enum):
    """Processing mode for photon operations."""
    STANDARD = "standard"
    HIGH_FIDELITY = "high_fidelity"
    LOW_LATENCY = "low_latency"


class BounceStrategy(str, Enum):
    """Strategy for binary bounce simulations."""
    DETERMINISTIC = "deterministic"
    STOCHASTIC = "stochastic"
    HYBRID = "hybrid"


class JobStatus(str, Enum):
    """Status of an asynchronous training job."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _parse_datetime(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


# ---------------------------------------------------------------------------
# Photon models
# ---------------------------------------------------------------------------

@dataclass
class PhotonResult:
    """Result of a photon processing request."""
    id: str
    status: str
    wavelength: float
    intensity: float
    coherence_score: float
    processed_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PhotonResult:
        return cls(
            id=data["id"],
            status=data["status"],
            wavelength=data["wavelength"],
            intensity=data["intensity"],
            coherence_score=data["coherence_score"],
            processed_at=_parse_datetime(data.get("processed_at")),
            metadata=data.get("metadata", {}),
        )


@dataclass
class PhotonAnalysis:
    """Result of a photon analysis request."""
    id: str
    spectrum: list[float]
    peak_wavelength: float
    energy_distribution: dict[str, float]
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PhotonAnalysis:
        return cls(
            id=data["id"],
            spectrum=data["spectrum"],
            peak_wavelength=data["peak_wavelength"],
            energy_distribution=data["energy_distribution"],
            confidence=data["confidence"],
            metadata=data.get("metadata", {}),
        )


@dataclass
class BatchPhotonResult:
    """Result of a batch photon processing request."""
    batch_id: str
    results: list[PhotonResult]
    total: int
    succeeded: int
    failed: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatchPhotonResult:
        return cls(
            batch_id=data["batch_id"],
            results=[PhotonResult.from_dict(r) for r in data.get("results", [])],
            total=data["total"],
            succeeded=data["succeeded"],
            failed=data["failed"],
        )


# ---------------------------------------------------------------------------
# Bounce models
# ---------------------------------------------------------------------------

@dataclass
class BounceResult:
    """Result of a binary bounce simulation."""
    id: str
    status: str
    iterations: int
    convergence: float
    binary_state: list[int]
    energy_delta: float
    elapsed_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BounceResult:
        return cls(
            id=data["id"],
            status=data["status"],
            iterations=data["iterations"],
            convergence=data["convergence"],
            binary_state=data["binary_state"],
            energy_delta=data["energy_delta"],
            elapsed_ms=data["elapsed_ms"],
            metadata=data.get("metadata", {}),
        )


@dataclass
class BinaryStream:
    """A single frame in a streamed bounce simulation."""
    frame_index: int
    timestamp: float
    binary_state: list[int]
    energy: float
    converged: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BinaryStream:
        return cls(
            frame_index=data["frame_index"],
            timestamp=data["timestamp"],
            binary_state=data["binary_state"],
            energy=data["energy"],
            converged=data["converged"],
        )


# ---------------------------------------------------------------------------
# Training models
# ---------------------------------------------------------------------------

@dataclass
class TrainingJob:
    """Represents a model training job."""
    id: str
    name: str
    status: JobStatus
    model_id: str
    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    progress: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TrainingJob:
        return cls(
            id=data["id"],
            name=data["name"],
            status=JobStatus(data["status"]),
            model_id=data["model_id"],
            created_at=_parse_datetime(data.get("created_at")),
            started_at=_parse_datetime(data.get("started_at")),
            completed_at=_parse_datetime(data.get("completed_at")),
            progress=data.get("progress", 0.0),
            metrics=data.get("metrics", {}),
            config=data.get("config", {}),
        )


# ---------------------------------------------------------------------------
# Model registry models
# ---------------------------------------------------------------------------

@dataclass
class Model:
    """A registered model in the Lumoxic platform."""
    id: str
    name: str
    version: str
    description: str
    status: str
    created_at: datetime | None = None
    parameters: int = 0
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Model:
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            description=data.get("description", ""),
            status=data.get("status", "ready"),
            created_at=_parse_datetime(data.get("created_at")),
            parameters=data.get("parameters", 0),
            capabilities=data.get("capabilities", []),
            metadata=data.get("metadata", {}),
        )
