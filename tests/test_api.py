from fastapi.testclient import TestClient

from pdf_api.app import app

client = TestClient(app)


def test_status():
    response = client.get("/")
    assert response.status_code
