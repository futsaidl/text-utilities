import pytest
from fastapi.testclient import TestClient
from app_final import app


@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version_check(client):
    response = client.get("/api/version")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert "version" in data

def test_api_slugify_success(client):
    response = client.get("/api/slugify", params={"text": "Hello World!"})
    assert response.status_code == 200
    data = response.json()
    assert data["original"] == "Hello World!"
    assert data["slug"] == "hello-world"

def test_api_slugify_invalid_input(client):
    response = client.get("/api/slugify", params={"text": "!!!---???"})
    assert response.status_code == 400
    assert "detail" in response.json()

def test_api_analyzer_success(client):
    response = client.get("/api/analyzer", params={"text": "Hello World, Hello!"})
    assert response.status_code == 200
    data = response.json()
    assert data is not None

def test_api_analyzer_empty_input(client):
    response = client.get("/api/analyzer", params={"text": "   "})
    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/analyzer",
        "/slugify",
        "/case",
    ],
)
def test_ui_pages(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]