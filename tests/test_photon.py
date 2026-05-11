"""Tests for the PhotonAPI namespace."""

import pytest

from lumoxic_sdk import LumoxicClient, PhotonResult, PhotonAnalysis, BatchPhotonResult


@pytest.fixture
def client():
    return LumoxicClient(api_key="lmx-test-key")


class TestPhotonProcess:
    def test_process_returns_photon_result(self, client):
        result = client.photon.process(wavelength=550.0, intensity=0.8)
        assert isinstance(result, PhotonResult)

    def test_process_preserves_wavelength(self, client):
        result = client.photon.process(wavelength=632.8, intensity=0.5)
        assert result.wavelength == 632.8

    def test_process_preserves_intensity(self, client):
        result = client.photon.process(wavelength=500.0, intensity=0.42)
        assert result.intensity == 0.42

    def test_process_status_is_completed(self, client):
        result = client.photon.process(wavelength=500.0, intensity=0.5)
        assert result.status == "completed"

    def test_process_id_has_prefix(self, client):
        result = client.photon.process(wavelength=500.0, intensity=0.5)
        assert result.id.startswith("pht_")

    def test_process_coherence_in_range(self, client):
        result = client.photon.process(wavelength=500.0, intensity=0.5)
        assert 0.0 <= result.coherence_score <= 1.0

    def test_process_with_metadata(self, client):
        meta = {"experiment": "lab-3", "operator": "jdoe"}
        result = client.photon.process(wavelength=500.0, intensity=0.5, metadata=meta)
        assert result.metadata["experiment"] == "lab-3"

    def test_process_with_string_mode(self, client):
        result = client.photon.process(wavelength=500.0, intensity=0.5, mode="high_fidelity")
        assert isinstance(result, PhotonResult)


class TestPhotonAnalyze:
    def test_analyze_returns_analysis(self, client):
        analysis = client.photon.analyze("pht_abc123")
        assert isinstance(analysis, PhotonAnalysis)

    def test_analyze_spectrum_length(self, client):
        analysis = client.photon.analyze("pht_abc123", depth=3)
        assert len(analysis.spectrum) == 6  # depth * 2

    def test_analyze_has_energy_distribution(self, client):
        analysis = client.photon.analyze("pht_abc123")
        assert "visible" in analysis.energy_distribution

    def test_analyze_confidence_in_range(self, client):
        analysis = client.photon.analyze("pht_abc123")
        assert 0.0 <= analysis.confidence <= 1.0


class TestPhotonBatch:
    def test_batch_returns_batch_result(self, client):
        items = [
            {"wavelength": 500.0, "intensity": 0.5},
            {"wavelength": 600.0, "intensity": 0.7},
        ]
        result = client.photon.batch(items)
        assert isinstance(result, BatchPhotonResult)

    def test_batch_correct_count(self, client):
        items = [
            {"wavelength": 500.0, "intensity": 0.5},
            {"wavelength": 600.0, "intensity": 0.7},
            {"wavelength": 700.0, "intensity": 0.9},
        ]
        result = client.photon.batch(items)
        assert result.total == 3
        assert result.succeeded == 3
        assert result.failed == 0

    def test_batch_results_are_photon_results(self, client):
        items = [{"wavelength": 550.0, "intensity": 0.6}]
        result = client.photon.batch(items)
        assert all(isinstance(r, PhotonResult) for r in result.results)
