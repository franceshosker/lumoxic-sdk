#!/usr/bin/env python3
"""Batch processing example for the Lumoxic AI SDK.

Demonstrates how to process multiple photon measurements in a single
batch request and stream bounce simulation frames.

Run::

    python batch_processing.py
"""

from lumoxic_sdk import LumoxicClient

client = LumoxicClient(api_key="lmx-demo-key-12345")


def batch_photon_example():
    """Process a batch of photon measurements."""
    print("=== Batch Photon Processing ===\n")

    # Prepare a batch of measurements.
    measurements = [
        {"wavelength": 450.0, "intensity": 0.6, "metadata": {"label": "blue"}},
        {"wavelength": 520.0, "intensity": 0.75, "metadata": {"label": "green"}},
        {"wavelength": 590.0, "intensity": 0.82, "metadata": {"label": "yellow"}},
        {"wavelength": 635.0, "intensity": 0.91, "metadata": {"label": "red"}},
        {"wavelength": 700.0, "intensity": 0.55, "metadata": {"label": "deep-red"}},
    ]

    result = client.photon.batch(measurements, mode="high_fidelity")

    print(f"Batch ID:   {result.batch_id}")
    print(f"Total:      {result.total}")
    print(f"Succeeded:  {result.succeeded}")
    print(f"Failed:     {result.failed}")
    print()

    for r in result.results:
        label = r.metadata.get("label", "unknown")
        print(f"  [{label:10s}] {r.wavelength:6.1f} nm  coherence={r.coherence_score:.4f}")
    print()


def stream_bounce_example():
    """Stream bounce simulation frames in real time."""
    print("=== Streaming Bounce Simulation ===\n")

    initial = [1, 0, 0, 1, 1, 0, 1, 1]
    print(f"Initial state: {initial}\n")

    for frame in client.bounce.stream(initial_state=initial, iterations=10):
        status = "CONVERGED" if frame.converged else "running"
        print(
            f"  Frame {frame.frame_index:3d}  "
            f"state={frame.binary_state}  "
            f"energy={frame.energy:.4f}  "
            f"[{status}]"
        )
        if frame.converged:
            print("\n  Simulation converged early!")
            break

    print()


if __name__ == "__main__":
    batch_photon_example()
    stream_bounce_example()
    print("Done!")
