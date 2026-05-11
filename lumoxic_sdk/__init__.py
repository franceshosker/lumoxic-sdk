"""Lumoxic AI Python SDK.

A client library for interacting with the Lumoxic AI API for photon
processing, binary bounce simulation, model training, and deployment.

Quick start::

    from lumoxic_sdk import LumoxicClient

    client = LumoxicClient(api_key="lmx-...")
    result = client.photon.process(wavelength=550.0, intensity=0.8)
    print(result)
"""

from ._version import __version__
from .async_client import AsyncLumoxicClient
from .client import LumoxicClient
from .config import LumoxicConfig
from .exceptions import (
    AuthenticationError,
    LumoxicError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from .models import (
    BatchPhotonResult,
    BinaryStream,
    BounceResult,
    BounceStrategy,
    JobStatus,
    Model,
    PhotonAnalysis,
    PhotonMode,
    PhotonResult,
    TrainingJob,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "LumoxicClient",
    "AsyncLumoxicClient",
    # Config
    "LumoxicConfig",
    # Exceptions
    "LumoxicError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    "TimeoutError",
    "NotFoundError",
    # Models
    "PhotonResult",
    "PhotonAnalysis",
    "BatchPhotonResult",
    "BounceResult",
    "BinaryStream",
    "TrainingJob",
    "Model",
    # Enums
    "PhotonMode",
    "BounceStrategy",
    "JobStatus",
]
