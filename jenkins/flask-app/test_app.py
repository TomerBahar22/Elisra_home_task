"""Unit tests for the Flask app.
"""
import pytest

import app as app_module   # your app.py


# Fake container list, used instead of asking Docker
FAKE_CONTAINERS = [
    {"name": "flask-app", "short_id": "abc123",
     "image": "tomerbahar2/flask-containers:1.0.0", "status": "running"},
]


@pytest.fixture
def client(monkeypatch):
    """A fake browser for the app. Runs before each test."""
    # replace the real get_containers() with one that returns the fake list
    monkeypatch.setattr(app_module, "get_containers", lambda: FAKE_CONTAINERS)
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_health(client):
    """/health answers 200"""
    assert client.get("/health").status_code == 200


def test_api_lists_containers(client):
    """/api/containers returns the container list"""
    response = client.get("/api/containers")
    assert response.status_code == 200
    assert "flask-app" in response.get_data(as_text=True)


def test_home_shows_containers_and_client_ip(client):
    """the home page shows the containers and the IP that Nginx injects"""
    response = client.get("/", headers={"X-Real-IP": "203.0.113.7"})
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "flask-app" in body
    assert "203.0.113.7" in body