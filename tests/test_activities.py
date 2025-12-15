"""Tests for activities endpoints."""
import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to static/index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Basketball" in activities
    assert "Tennis" in activities
    assert "Chess Club" in activities
    
    # Check structure of an activity
    basketball = activities["Basketball"]
    assert "description" in basketball
    assert "schedule" in basketball
    assert "max_participants" in basketball
    assert "participants" in basketball


def test_get_activities_has_participants(client):
    """Test that activities include existing participants."""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_signup_for_activity(client):
    """Test signing up for an activity."""
    response = client.post(
        "/activities/Basketball/signup?email=student@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "student@mergington.edu" in data["message"]
    assert "Basketball" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "student@mergington.edu" in activities["Basketball"]["participants"]


def test_signup_duplicate_email(client):
    """Test that signing up with the same email twice fails."""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/Basketball/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        f"/activities/Basketball/signup?email={email}"
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity."""
    response = client.post(
        "/activities/NonExistent/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_from_activity(client):
    """Test unregistering a participant from an activity."""
    email = "participant@mergington.edu"
    
    # First sign up
    signup_response = client.post(
        f"/activities/Basketball/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Then unregister
    response = client.post(
        f"/activities/Basketball/unregister?email={email}"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Basketball" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Basketball"]["participants"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a participant who is not signed up."""
    response = client.post(
        "/activities/Basketball/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from a non-existent activity."""
    response = client.post(
        "/activities/NonExistent/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_existing_participant(client):
    """Test unregistering an existing participant from Chess Club."""
    response = client.post(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_multiple_signups_and_unregisters(client):
    """Test multiple signup and unregister operations."""
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Sign up all students
    for email in emails:
        response = client.post(
            f"/activities/Tennis/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Verify all are registered
    activities_response = client.get("/activities")
    tennis_participants = activities_response.json()["Tennis"]["participants"]
    assert len(tennis_participants) == 3
    
    # Unregister one student
    response = client.post(
        "/activities/Tennis/unregister?email=student2@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify only 2 remain
    activities_response = client.get("/activities")
    tennis_participants = activities_response.json()["Tennis"]["participants"]
    assert len(tennis_participants) == 2
    assert "student1@mergington.edu" in tennis_participants
    assert "student3@mergington.edu" in tennis_participants
    assert "student2@mergington.edu" not in tennis_participants


def test_activity_max_participants_info(client):
    """Test that max_participants info is returned correctly."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity in activities.items():
        assert "max_participants" in activity
        assert isinstance(activity["max_participants"], int)
        assert activity["max_participants"] > 0
        assert len(activity["participants"]) <= activity["max_participants"]
