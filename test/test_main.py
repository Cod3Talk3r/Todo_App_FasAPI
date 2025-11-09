from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


def test_healthy_check():
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status:": "Healthy"}