import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SentinelCore API is running."}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 404  # Not implemented yet