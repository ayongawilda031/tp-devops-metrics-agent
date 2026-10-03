"""Tests de l'API FastAPI (app.api)."""
from fastapi.testclient import TestClient

from app.api import app, received_metrics

client = TestClient(app)


def setup_function():
    """Réinitialise l'état partagé avant chaque test pour les isoler les uns des autres."""
    received_metrics.clear()


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_metrics_empty_initially():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json() == {"total": 0, "metrics": []}


def test_post_then_get_latest_metrics():
    payload = {
        "agent": "test-agent",
        "event_type": "system_metrics",
        "data": {"cpu": {"percent": 10.0}},
    }

    post_response = client.post("/metrics", json=payload)
    assert post_response.status_code == 201
    assert post_response.json()["total_received"] == 1

    latest_response = client.get("/metrics/latest")
    assert latest_response.status_code == 200
    assert latest_response.json()["agent"] == "test-agent"


def test_latest_metrics_404_when_empty():
    response = client.get("/metrics/latest")

    assert response.status_code == 404