"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original activities
    from src.app import activities
    original = {
        "Basketball": {
            "description": "Learn basketball skills and compete in friendly matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis": {
            "description": "Develop tennis techniques and participate in tournaments",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and experiments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": []
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and acting workshops",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Visual Arts": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original)
