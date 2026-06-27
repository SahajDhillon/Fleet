from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_returns_service_info():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "FleetIQ"


def test_register_and_list_cluster():
    payload = {"name": "ci-test-cluster", "environment": "dev", "provider": "kind"}
    response = client.post("/clusters", json=payload)
    # 201 on first run, 409 if it already exists from a previous run
    assert response.status_code in (201, 409)

    listing = client.get("/clusters")
    assert listing.status_code == 200
    assert any(c["name"] == "ci-test-cluster" for c in listing.json())


def test_health_report_for_missing_cluster_returns_404():
    response = client.post(
        "/clusters/999999/health",
        json={"status": "healthy", "cpu_usage": 10.0, "memory_usage": 20.0},
    )
    assert response.status_code == 404
