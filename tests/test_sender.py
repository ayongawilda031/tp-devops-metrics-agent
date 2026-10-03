"""Tests du module app.sender (les appels réseau réels sont simulés)."""
import pytest
import requests

from app.sender import MetricsDeliveryError, send_metrics


class _FakeResponse:
    def __init__(self, status_code=201, json_body=None):
        self.status_code = status_code
        self._json_body = json_body or {"status": "received"}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._json_body


def test_send_metrics_success(monkeypatch):
    """Un envoi réussi doit retourner le code HTTP et la réponse de l'API."""

    def fake_post(url, json, timeout):
        assert url == "http://api:8000/metrics"
        return _FakeResponse(status_code=201, json_body={"status": "received"})

    monkeypatch.setattr(requests, "post", fake_post)

    result = send_metrics(endpoint="http://api:8000/metrics", payload={"agent": "x"}, timeout=3)

    assert result["status_code"] == 201
    assert result["response"] == {"status": "received"}


def test_send_metrics_failure_raises(monkeypatch):
    """Si l'API est injoignable, une MetricsDeliveryError explicite doit être levée."""

    def fake_post(url, json, timeout):
        raise requests.ConnectionError("Connexion refusée")

    monkeypatch.setattr(requests, "post", fake_post)

    with pytest.raises(MetricsDeliveryError):
        send_metrics(endpoint="http://api:8000/metrics", payload={"agent": "x"}, timeout=3)