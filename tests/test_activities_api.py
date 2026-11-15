"""
Comprehensive API tests for Mergington High School Activities API.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status code 200."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_expected_activities(self, client):
        """Test that all expected activities are returned."""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Track and Field",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_response_structure(self, client):
        """Test that each activity has the correct structure."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=new_student@mergington.edu"
        )
        
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "new_student@mergington.edu" in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup adds the participant to the activity."""
        email = "test_student@mergington.edu"
        
        client.post(f"/activities/Basketball%20Team/signup?email={email}")
        
        response = client.get("/activities")
        activities = response.json()
        
        assert email in activities["Basketball Team"]["participants"]

    def test_signup_duplicate_email_fails(self, client):
        """Test that signing up with duplicate email returns 400 error."""
        email = "michael@mergington.edu"
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found(self, client):
        """Test that signup for non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent%20Club/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_multiple_participants_same_activity(self, client):
        """Test that multiple different students can sign up for same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        client.post(f"/activities/Art%20Club/signup?email={email1}")
        client.post(f"/activities/Art%20Club/signup?email={email2}")
        
        response = client.get("/activities")
        participants = response.json()["Art Club"]["participants"]
        
        assert email1 in participants
        assert email2 in participants
        assert len(participants) == 2

    def test_signup_same_student_different_activities(self, client):
        """Test that same student can sign up for different activities."""
        email = "student@mergington.edu"
        
        client.post(f"/activities/Art%20Club/signup?email={email}")
        client.post(f"/activities/Debate%20Club/signup?email={email}")
        
        response = client.get("/activities")
        activities = response.json()
        
        assert email in activities["Art Club"]["participants"]
        assert email in activities["Debate Club"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity."""
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister removes the participant from activity."""
        email = "michael@mergington.edu"
        
        client.delete(f"/activities/Chess%20Club/signup?email={email}")
        
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        
        assert email not in participants

    def test_unregister_participant_not_found(self, client):
        """Test that unregistering non-existent participant returns 400."""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=notregistered@mergington.edu"
        )
        
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_activity_not_found(self, client):
        """Test that unregistering from non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent%20Club/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_unregister_updates_availability(self, client):
        """Test that unregistering updates the availability count."""
        email = "michael@mergington.edu"
        
        response_before = client.get("/activities")
        spots_before = (
            response_before.json()["Chess Club"]["max_participants"]
            - len(response_before.json()["Chess Club"]["participants"])
        )
        
        client.delete(f"/activities/Chess%20Club/signup?email={email}")
        
        response_after = client.get("/activities")
        spots_after = (
            response_after.json()["Chess Club"]["max_participants"]
            - len(response_after.json()["Chess Club"]["participants"])
        )
        
        assert spots_after == spots_before + 1

    def test_unregister_multiple_times_fails(self, client):
        """Test that unregistering same student twice fails on second attempt."""
        email = "michael@mergington.edu"
        
        response1 = client.delete(f"/activities/Chess%20Club/signup?email={email}")
        assert response1.status_code == 200
        
        response2 = client.delete(f"/activities/Chess%20Club/signup?email={email}")
        assert response2.status_code == 400
