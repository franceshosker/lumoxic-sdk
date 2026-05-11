# Lumoxic AI Python SDK

The official Python client library for the [Lumoxic AI](https://lumoxic.ai) photon computing and binary bounce simulation API.

## Installation

```bash
pip install lumoxic-sdk
```

For async support with `aiohttp`:

```bash
pip install "lumoxic-sdk[async]"
```

## Authentication

Set your API key as an environment variable:

```bash
export LUMOXIC_API_KEY="lmx-your-api-key"
```

Or pass it directly when creating a client:

```python
from lumoxic_sdk import LumoxicClient

client = LumoxicClient(api_key="lmx-your-api-key")
```

## Quick Start

```python
from lumoxic_sdk import LumoxicClient

client = LumoxicClient(api_key="lmx-your-api-key")

# Process a photon measurement
result = client.photon.process(wavelength=550.0, intensity=0.85)
print(result.coherence_score)

# Run a binary bounce simulation
bounce = client.bounce.simulate(iterations=200, strategy="stochastic")
print(bounce.convergence)

# List available models
models = client.models.list()
for model in models:
    print(f"{model.name} (v{model.version})")
```

## API Reference

### Client

```python
LumoxicClient(
    api_key: str | None = None,      # Falls back to LUMOXIC_API_KEY env var
    base_url: str | None = None,      # Default: https://api.lumoxic.ai/v1
    timeout: float = 30.0,            # Request timeout in seconds
    max_retries: int = 3,             # Retries for transient errors
)
```

### Photon Processing (`client.photon`)

| Method | Description |
|---|---|
| `process(wavelength, intensity, *, mode, metadata)` | Process a single photon measurement |
| `analyze(photon_id, *, depth)` | Run spectral analysis on a processed photon |
| `batch(items, *, mode)` | Process multiple measurements in one request |

**Processing modes:** `"standard"`, `"high_fidelity"`, `"low_latency"`

```python
# Process
result = client.photon.process(wavelength=632.8, intensity=0.9, mode="high_fidelity")

# Analyze
analysis = client.photon.analyze(result.id, depth=8)
print(analysis.peak_wavelength, analysis.confidence)

# Batch
batch = client.photon.batch([
    {"wavelength": 450.0, "intensity": 0.6},
    {"wavelength": 550.0, "intensity": 0.8},
])
print(f"Succeeded: {batch.succeeded}/{batch.total}")
```

### Binary Bounce Simulation (`client.bounce`)

| Method | Description |
|---|---|
| `simulate(initial_state, *, iterations, strategy, energy_threshold)` | Run a bounce simulation |
| `stream(initial_state, *, iterations, strategy)` | Stream simulation frames as a generator |

**Strategies:** `"deterministic"`, `"stochastic"`, `"hybrid"`

```python
# Simulate
result = client.bounce.simulate(
    initial_state=[1, 0, 1, 1, 0, 0, 1, 0],
    iterations=500,
    strategy="hybrid",
)
print(result.convergence, result.energy_delta)

# Stream frames
for frame in client.bounce.stream(iterations=20):
    print(f"Frame {frame.frame_index}: energy={frame.energy:.4f}")
    if frame.converged:
        break
```

### Training (`client.training`)

| Method | Description |
|---|---|
| `create(name, model_id, *, config)` | Start a new training job |
| `status(job_id)` | Check training job status |
| `cancel(job_id)` | Cancel a running job |
| `list(*, limit, offset)` | List training jobs |

```python
job = client.training.create(
    name="photon-finetune",
    model_id="lmx-photon-base-v2",
    config={"learning_rate": 3e-5, "epochs": 5},
)

status = client.training.status(job.id)
print(f"Progress: {status.progress:.0%}")
```

### Models (`client.models`)

| Method | Description |
|---|---|
| `list(*, limit, offset)` | List available models |
| `get(model_id)` | Get model details |
| `deploy(model_id, *, replicas, accelerator)` | Deploy a model to an endpoint |

```python
models = client.models.list()
model = client.models.get("lmx-photon-base-v2")

deployment = client.models.deploy("lmx-photon-base-v2", replicas=2)
print(deployment["endpoint"])
```

## Async Usage

The SDK provides a fully async client for use with `asyncio`:

```python
import asyncio
from lumoxic_sdk import AsyncLumoxicClient

async def main():
    async with AsyncLumoxicClient(api_key="lmx-your-api-key") as client:
        # Concurrent photon processing
        results = await asyncio.gather(
            client.photon.process(wavelength=450.0, intensity=0.6),
            client.photon.process(wavelength=550.0, intensity=0.8),
            client.photon.process(wavelength=650.0, intensity=0.7),
        )

        for r in results:
            print(f"{r.wavelength} nm -> coherence {r.coherence_score:.4f}")

        # Async streaming
        async for frame in client.bounce.stream(iterations=15):
            print(f"Frame {frame.frame_index}: {frame.binary_state}")
            if frame.converged:
                break

asyncio.run(main())
```

## Error Handling

The SDK raises typed exceptions for different error scenarios:

```python
from lumoxic_sdk import LumoxicClient
from lumoxic_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ServerError,
    NotFoundError,
)

client = LumoxicClient(api_key="lmx-your-key")

try:
    model = client.models.get("nonexistent-model")
except NotFoundError as e:
    print(f"Model not found: {e}")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except ServerError:
    print("Server error, try again later")
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `LUMOXIC_API_KEY` | API key for authentication | (required) |
| `LUMOXIC_BASE_URL` | Override API base URL | `https://api.lumoxic.ai/v1` |
| `LUMOXIC_TIMEOUT` | Request timeout in seconds | `30` |

## License

MIT License. Copyright (c) 2026 Lumoxic AI. See [LICENSE](LICENSE) for details.
