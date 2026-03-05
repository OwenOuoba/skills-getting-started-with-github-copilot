"""Tests for root endpoint"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static():
    """Test that GET / redirects to /static/index.html"""
    # Arrange
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
