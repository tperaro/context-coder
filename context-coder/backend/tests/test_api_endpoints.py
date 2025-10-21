"""
API Endpoint Tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Context2Task API" in response.json()["message"]


def test_api_info():
    """Test API info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "features" in data
    assert "models" in data
    assert "mcp" in data


