#!/usr/bin/env python3
"""Async usage example for the Lumoxic AI SDK.

Demonstrates how to use the ``AsyncLumoxicClient`` with ``asyncio`` for
concurrent photon processing and bounce simulation.

Run::

    python async_example.py
"""

import asyncio

from lumoxic_sdk import AsyncLumoxicClient


async def main():
    async with AsyncLumoxicClient(api_key="lmx-demo-key-12345") as client:
        # ----------------------------------------------------------
        # Concurrent photon processing
        # ----------------------------------------------------------
        print("=== Async Photon Processing ===\n")

        tasks = [
            client.photon.process(wavelength=450.0, intensity=0.6),
            client.photon.process(wavelength=550.0, intensity=0.8),
            client.photon.process(wavelength=650.0, intensity=0.7),
        ]
        results = await asyncio.gather(*tasks)

        for r in results:
            print(f"  {r.id}  {r.wavelength} nm  coherence={r.coherence_score:.4f}")
        print()

        # ----------------------------------------------------------
        # Async analysis
        # ----------------------------------------------------------
        print("=== Async Photon Analysis ===\n")

        analysis = await client.photon.analyze(results[0].id, depth=3)
        print(f"  Analysis ID:     {analysis.id}")
        print(f"  Peak Wavelength: {analysis.peak_wavelength:.2f} nm")
        print(f"  Confidence:      {analysis.confidence:.4f}")
        print()

        # ----------------------------------------------------------
        # Async batch
        # ----------------------------------------------------------
        print("=== Async Batch Processing ===\n")

        items = [
            {"wavelength": 500.0, "intensity": 0.5},
            {"wavelength": 600.0, "intensity": 0.7},
        ]
        batch = await client.photon.batch(items)
        print(f"  Batch ID:  {batch.batch_id}")
        print(f"  Total:     {batch.total}  Succeeded: {batch.succeeded}")
        print()

        # ----------------------------------------------------------
        # Async bounce simulation
        # ----------------------------------------------------------
        print("=== Async Bounce Simulation ===\n")

        bounce = await client.bounce.simulate(iterations=150, strategy="hybrid")
        print(f"  Bounce ID:    {bounce.id}")
        print(f"  Convergence:  {bounce.convergence:.6f}")
        print(f"  Final State:  {bounce.binary_state}")
        print()

        # ----------------------------------------------------------
        # Async streaming
        # ----------------------------------------------------------
        print("=== Async Bounce Streaming ===\n")

        async for frame in client.bounce.stream(iterations=8):
            status = "CONVERGED" if frame.converged else "running"
            print(
                f"  Frame {frame.frame_index:3d}  "
                f"state={frame.binary_state}  "
                f"energy={frame.energy:.4f}  [{status}]"
            )
            if frame.converged:
                break
        print()

        # ----------------------------------------------------------
        # Async model listing
        # ----------------------------------------------------------
        print("=== Async Models ===\n")

        models = await client.models.list()
        for m in models:
            print(f"  {m.id:25s}  {m.name}")
        print()

        # ----------------------------------------------------------
        # Async training
        # ----------------------------------------------------------
        print("=== Async Training ===\n")

        job = await client.training.create(
            name="async-finetune",
            model_id="lmx-photon-base-v2",
        )
        print(f"  Job ID:  {job.id}")
        print(f"  Status:  {job.status.value}")
        print()

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
