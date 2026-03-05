"""Tests for signup endpoint"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert email in data["message"]


def test_signup_for_nonexistent_activity():
    """Test signup fails for activity that doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email_rejected():
    """Test that duplicate signups are rejected"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_adds_participant_to_activity():
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"
    
    # Act - get initial participants count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act - signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - get updated participants count
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    
    # Assert
    assert signup_response.status_code == 200
    assert updated_count == initial_count + 1
    assert email in updated_response.json()[activity_name]["participants"]
