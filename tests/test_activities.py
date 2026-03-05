"""Tests for activities endpoint"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    """Test that GET /activities returns all activities"""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Debate Society", "Math Olympiad", "Drama Club", "Art Studio"
    ]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == 9
    assert list(data.keys()) == expected_activities


def test_get_activities_contains_activity_details():
    """Test that activities contain required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_info in data.items():
        assert set(activity_info.keys()) == required_fields


def test_get_activities_participants_are_lists():
    """Test that participants field is always a list"""
    # Arrange
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_info in data.values():
        assert isinstance(activity_info["participants"], list)
