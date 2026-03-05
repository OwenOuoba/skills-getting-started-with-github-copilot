"""Tests for unregister endpoint"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_unregister_from_activity_success():
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already a participant
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "message" in data


def test_unregister_removes_participant():
    """Test that unregister actually removes the participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    
    # Act - verify participant exists
    initial_response = client.get("/activities")
    assert email in initial_response.json()[activity_name]["participants"]
    
    # Act - unregister
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Act - verify participant removed
    updated_response = client.get("/activities")
    
    # Assert
    assert unregister_response.status_code == 200
    assert email not in updated_response.json()[activity_name]["participants"]


def test_unregister_from_nonexistent_activity():
    """Test unregister fails for activity that doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up():
    """Test unregister fails when student is not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
