from fastapi.testclient import TestClient

from lodestar_veritas.api.main import app


client = TestClient(app)


def test_api_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Lodestar Veritas API is running."


def test_api_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_api_ask_endpoint():
    response = client.post(
        "/ask",
        json={
            "query": "What increased in 2024?",
            "file_paths": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "What increased in 2024?"
    assert "answer" in data
    assert "confidence" in data
    assert "workflow_events" in data