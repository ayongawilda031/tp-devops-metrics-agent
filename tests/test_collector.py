"""Tests du module app.collector."""
from app.collector import collect_system_metrics


def test_collect_system_metrics_structure():
    """La collecte doit retourner toutes les clés attendues, avec les bons types."""
    metrics = collect_system_metrics()

    assert "timestamp" in metrics
    assert "hostname" in metrics

    assert "percent" in metrics["cpu"]
    assert "logical_cores" in metrics["cpu"]
    assert isinstance(metrics["cpu"]["percent"], (int, float))

    assert "total_bytes" in metrics["memory"]
    assert "percent" in metrics["memory"]
    assert metrics["memory"]["total_bytes"] > 0

    assert "load_1m" in metrics["system"]