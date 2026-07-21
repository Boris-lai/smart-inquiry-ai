from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_application_title_comes_from_settings() -> None:
    settings = get_settings()

    assert app.title == settings.app_name
