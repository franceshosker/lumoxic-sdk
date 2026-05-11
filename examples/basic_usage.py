#!/usr/bin/env python3
"""Basic usage of the Lumoxic AI SDK.

Run::

    pip install lumoxic-sdk
    export LUMOXIC_API_KEY="lmx-your-key-here"
    python basic_usage.py
"""

from lumoxic_sdk import LumoxicClient

# Initialize the client (uses LUMOXIC_API_KEY env var or pass directly).
client = LumoxicClient(api_key="lmx-demo-key-12345")


def photon_demo():
    """Demonstrate photon processing."""
    print("=== Photon Processing ===\n")

    # Process a single photon measurement.
    result = client.photon.process(wavelength=550.0, intensity=0.85)
    print(f"Photon ID:        {result.id}")
    print(f"Status:           {result.status}")
    print(f"Wavelength:       {result.wavelength} nm")
    print(f"Intensity:        {result.intensity}")
    print(f"Coherence Score:  {result.coherence_score}")
    print(f"Processed At:     {result.processed_at}")
    print()

    # Analyze the result.
    analysis = client.photon.analyze(result.id, depth=4)
    print(f"Analysis ID:      {analysis.id}")
    print(f"Peak Wavelength:  {analysis.peak_wavelength:.2f} nm")
    print(f"Confidence:       {analysis.confidence:.4f}")
    print(f"Energy Dist:      {analysis.energy_distribution}")
    print()


def bounce_demo():
    """Demonstrate binary bounce simulation."""
    print("=== Binary Bounce Simulation ===\n")

    result = client.bounce.simulate(
        initial_state=[1, 0, 1, 1, 0, 0, 1, 0],
        iterations=200,
        strategy="stochastic",
    )
    print(f"Bounce ID:     {result.id}")
    print(f"Iterations:    {result.iterations}")
    print(f"Convergence:   {result.convergence:.6f}")
    print(f"Final State:   {result.binary_state}")
    print(f"Energy Delta:  {result.energy_delta}")
    print(f"Elapsed:       {result.elapsed_ms:.2f} ms")
    print()


def models_demo():
    """Demonstrate model listing."""
    print("=== Available Models ===\n")

    models = client.models.list()
    for m in models:
        print(f"  {m.id:25s}  {m.name:20s}  v{m.version}  ({m.status})")
    print()

    # Get details for a specific model.
    model = client.models.get("lmx-photon-base-v2")
    print(f"Model:         {model.name}")
    print(f"Parameters:    {model.parameters:,}")
    print(f"Capabilities:  {', '.join(model.capabilities)}")
    print()


def training_demo():
    """Demonstrate training job creation."""
    print("=== Training ===\n")

    job = client.training.create(
        name="photon-finetune-exp1",
        model_id="lmx-photon-base-v2",
        config={"learning_rate": 3e-5, "epochs": 5, "batch_size": 16},
    )
    print(f"Job ID:   {job.id}")
    print(f"Name:     {job.name}")
    print(f"Status:   {job.status.value}")
    print(f"Config:   {job.config}")
    print()

    # Check status.
    status = client.training.status(job.id)
    print(f"Progress: {status.progress:.1%}")
    print(f"Metrics:  {status.metrics}")
    print()


if __name__ == "__main__":
    photon_demo()
    bounce_demo()
    models_demo()
    training_demo()
    print("Done!")
