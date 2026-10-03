"""Tests du module app.formatter."""
import pytest

from app.formatter import format_metrics


def test_format_metrics_success():
    """Un dict de métriques complet doit être correctement enveloppé."""
    raw_metrics = {
        "timestamp": "2026-01-01T00:00:00+00:00",
        "hostname": "test-host",
        "cpu": {"percent": 12.5, "logical_cores": 4},
        "memory": {"total_bytes": 1000, "available_bytes": 500, "used_bytes": 500, "percent": 50.0},
        "system": {"load_1m": 0.1, "load_5m": 0.2, "load_15m": 0.3},
    }

    payload = format_metrics(raw_metrics)

    assert payload["agent"] == "system-metrics-agent"
    assert payload["event_type"] == "system_metrics"
    assert payload["data"] == raw_metrics


def test_format_metrics_custom_agent_name():
    """Le nom de l'agent doit être personnalisable."""
    raw_metrics = {
        "timestamp": "t",
        "hostname": "h",
        "cpu": {},
        "memory": {},
        "system": {},
    }

    payload = format_metrics(raw_metrics, agent_name="mon-agent")

    assert payload["agent"] == "mon-agent"


def test_format_metrics_missing_keys_raises():
    """Des métriques incomplètes doivent lever une ValueError explicite."""
    incomplete_metrics = {"timestamp": "t", "hostname": "h"}

    with pytest.raises(ValueError, match="incomplètes"):
        format_metrics(incomplete_metrics)