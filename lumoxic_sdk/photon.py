"""Photon processing API namespace."""

from __future__ import annotations

from typing import Any

from .models import BatchPhotonResult, PhotonAnalysis, PhotonMode, PhotonResult
from .utils import generate_id, random_float, random_spectrum, utcnow_iso


class PhotonAPI:
    """Namespace for photon processing endpoints.

    Accessed via ``client.photon``.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    # --------------------------------------------------------------------- #
    # Public methods
    # --------------------------------------------------------------------- #

    def process(
        self,
        wavelength: float,
        intensity: float,
        *,
        mode: PhotonMode | str = PhotonMode.STANDARD,
        metadata: dict[str, Any] | None = None,
    ) -> PhotonResult:
        """Process a single photon measurement.

        Parameters
        ----------
        wavelength:
            Wavelength in nanometres (380 -- 780 nm visible spectrum).
        intensity:
            Relative intensity value (0.0 -- 1.0).
        mode:
            Processing mode.
        metadata:
            Optional key/value metadata attached to the result.
        """
        if isinstance(mode, str):
            mode = PhotonMode(mode)

        # In a real SDK this would call self._client._request("POST", ...).
        # For demonstration we return realistic mock data.
        return PhotonResult(
            id=generate_id("pht"),
            status="completed",
            wavelength=wavelength,
            intensity=intensity,
            coherence_score=random_float(0.85, 0.99),
            processed_at=utcnow_iso(),
            metadata=metadata or {},
        )

    def analyze(
        self,
        photon_id: str,
        *,
        depth: int = 5,
    ) -> PhotonAnalysis:
        """Run spectral analysis on a previously processed photon.

        Parameters
        ----------
        photon_id:
            The ID returned from a prior ``process()`` call.
        depth:
            Analysis depth (1 -- 10).  Higher values yield finer resolution.
        """
        spectrum = random_spectrum(depth * 2)
        peak = max(spectrum)
        return PhotonAnalysis(
            id=generate_id("pan"),
            spectrum=spectrum,
            peak_wavelength=peak,
            energy_distribution={
                "ultraviolet": random_float(0.01, 0.15),
                "visible": random_float(0.50, 0.80),
                "infrared": random_float(0.05, 0.25),
            },
            confidence=random_float(0.90, 0.99),
            metadata={"source_photon": photon_id, "depth": depth},
        )

    def batch(
        self,
        items: list[dict[str, Any]],
        *,
        mode: PhotonMode | str = PhotonMode.STANDARD,
    ) -> BatchPhotonResult:
        """Process a batch of photon measurements.

        Parameters
        ----------
        items:
            A list of dicts, each containing ``wavelength`` and ``intensity``.
        mode:
            Processing mode applied to every item.
        """
        results: list[PhotonResult] = []
        failed = 0
        for item in items:
            try:
                result = self.process(
                    wavelength=item["wavelength"],
                    intensity=item["intensity"],
                    mode=mode,
                    metadata=item.get("metadata"),
                )
                results.append(result)
            except Exception:
                failed += 1

        return BatchPhotonResult(
            batch_id=generate_id("bat"),
            results=results,
            total=len(items),
            succeeded=len(results),
            failed=failed,
        )
