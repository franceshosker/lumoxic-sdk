# Lumoxic SDK

Official Python SDK for the [Lumoxic AI](https://lumoxicai.me) model optimization API.

## Installation

```bash
pip install lumoxic
```

## Quick Start

```python
import lumoxic

client = lumoxic.Client("lmx_your_api_key")

# Optimize a model
result = client.optimize(
    model="./my_model.onnx",
    target="mobile",
    strategy="auto"
)

print(result.delta)
# {'size_reduction': '8.1x', 'speedup': '7.6x', ...}

# Download optimized model
result.download("./optimized_model.onnx")
```

## API Reference

### `Client(api_key)`
Initialize the Lumoxic client.

### `client.optimize(model, target, strategy)`
Submit a model for optimization.

- `model` — Path to .onnx file
- `target` — Deployment target: `"server"`, `"mobile"`, `"edge"`, `"browser"`
- `strategy` — `"auto"`, `"int8"`, `"int4"`, `"prune"`, `"distill"`

### `client.benchmark(model)`
Benchmark a model without optimizing.

### `result.download(path)`
Download the optimized model.

### `client.usage()`
Check account usage and quota.

## License

MIT License. © 2026 Lumoxic AI.