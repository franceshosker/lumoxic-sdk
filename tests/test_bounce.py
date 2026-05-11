"""Tests for the BounceAPI namespace."""

import pytest

from lumoxic_sdk import LumoxicClient, BounceResult, BinaryStream


@pytest.fixture
def client():
    return LumoxicClient(api_key="lmx-test-key")


class TestBounceSimulate:
    def test_simulate_returns_bounce_result(self, client):
        result = client.bounce.simulate()
        assert isinstance(result, BounceResult)

    def test_simulate_status_completed(self, client):
        result = client.bounce.simulate()
        assert result.status == "completed"

    def test_simulate_id_prefix(self, client):
        result = client.bounce.simulate()
        assert result.id.startswith("bnc_")

    def test_simulate_custom_iterations(self, client):
        result = client.bounce.simulate(iterations=500)
        assert result.iterations == 500

    def test_simulate_with_initial_state(self, client):
        state = [1, 0, 1, 1, 0, 0, 1, 0]
        result = client.bounce.simulate(initial_state=state)
        assert len(result.binary_state) == len(state)

    def test_simulate_convergence_in_range(self, client):
        result = client.bounce.simulate()
        assert 0.0 <= result.convergence <= 1.0

    def test_simulate_with_string_strategy(self, client):
        result = client.bounce.simulate(strategy="stochastic")
        assert isinstance(result, BounceResult)

    def test_simulate_metadata_includes_strategy(self, client):
        result = client.bounce.simulate(strategy="hybrid")
        assert result.metadata["strategy"] == "hybrid"


class TestBounceStream:
    def test_stream_yields_binary_stream(self, client):
        frames = list(client.bounce.stream(iterations=5))
        assert len(frames) > 0
        assert all(isinstance(f, BinaryStream) for f in frames)

    def test_stream_frame_indices_sequential(self, client):
        frames = list(client.bounce.stream(iterations=5))
        indices = [f.frame_index for f in frames]
        # Indices should start at 0 and be sequential (may stop early on convergence).
        assert indices[0] == 0
        for i in range(1, len(indices)):
            assert indices[i] == indices[i - 1] + 1

    def test_stream_has_binary_state(self, client):
        frames = list(client.bounce.stream(iterations=3))
        for f in frames:
            assert all(b in (0, 1) for b in f.binary_state)

    def test_stream_respects_initial_state_length(self, client):
        state = [0, 1, 0, 1]
        frames = list(client.bounce.stream(initial_state=state, iterations=3))
        for f in frames:
            assert len(f.binary_state) == 4
