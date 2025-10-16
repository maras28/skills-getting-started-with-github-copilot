"""
Test cases for the FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_redirect(self, client, reset_activities):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "static/index.html" in response.headers["location"]


class TestActivitiesEndpoint:
    """Test the activities endpoint"""
    
    def test_get_activities(self, client, reset_activities):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # We have 9 activities in the initial data
        
        # Check that we have the expected activities
        expected_activities = [
            "Basketball Team", "Soccer Club", "Drama Club", "Art Workshop",
            "Debate Team", "Science Club", "Chess Club", "Programming Class", "Gym Class"
        ]
        for activity in expected_activities:
            assert activity in data
            
    def test_activity_structure(self, client, reset_activities):
        """Test that each activity has the correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignupEndpoint:
    """Test the signup endpoint"""
    
    def test_successful_signup(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post("/activities/Basketball Team/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Basketball Team" in data["message"]
        
        # Verify the student was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newstudent@mergington.edu" in activities_data["Basketball Team"]["participants"]
        
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signup for an activity that doesn't exist"""
        response = client.post("/activities/Nonexistent Activity/signup?email=student@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
        
    def test_signup_already_registered(self, client, reset_activities):
        """Test signup when student is already registered for an activity"""
        # First signup
        response1 = client.post("/activities/Basketball Team/signup?email=test@mergington.edu")
        assert response1.status_code == 200
        
        # Try to signup for another activity (should fail)
        response2 = client.post("/activities/Soccer Club/signup?email=test@mergington.edu")
        assert response2.status_code == 400
        
        data = response2.json()
        assert "already signed up" in data["detail"]
        
    def test_signup_with_url_encoded_activity_name(self, client, reset_activities):
        """Test signup with URL-encoded activity name"""
        response = client.post("/activities/Art%20Workshop/signup?email=artist@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "Art Workshop" in data["message"]
        
    def test_signup_with_url_encoded_email(self, client, reset_activities):
        """Test signup with URL-encoded email"""
        response = client.post("/activities/Basketball Team/signup?email=test%2Buser@mergington.edu")
        assert response.status_code == 200
        
        # Verify the email was properly decoded
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "test+user@mergington.edu" in activities_data["Basketball Team"]["participants"]


class TestUnregisterEndpoint:
    """Test the unregister endpoint"""
    
    def test_successful_unregister(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # First, sign up a student
        client.post("/activities/Basketball Team/signup?email=test@mergington.edu")
        
        # Then unregister them
        response = client.delete("/activities/Basketball Team/unregister?email=test@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "test@mergington.edu" in data["message"]
        assert "Basketball Team" in data["message"]
        
        # Verify the student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "test@mergington.edu" not in activities_data["Basketball Team"]["participants"]
        
    def test_unregister_from_nonexistent_activity(self, client, reset_activities):
        """Test unregistration from an activity that doesn't exist"""
        response = client.delete("/activities/Nonexistent Activity/unregister?email=student@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
        
    def test_unregister_student_not_found(self, client, reset_activities):
        """Test unregistration when student is not registered for the activity"""
        response = client.delete("/activities/Basketball Team/unregister?email=notregistered@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Student not found in this activity"
        
    def test_unregister_existing_participant(self, client, reset_activities):
        """Test unregistering an existing participant"""
        # Alex is already registered for Basketball Team in the initial data
        response = client.delete("/activities/Basketball Team/unregister?email=alex@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "Removed alex@mergington.edu from Basketball Team" in data["message"]
        
        # Verify alex was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "alex@mergington.edu" not in activities_data["Basketball Team"]["participants"]
        
    def test_unregister_with_url_encoded_params(self, client, reset_activities):
        """Test unregistration with URL-encoded parameters"""
        # Sign up with special characters
        client.post("/activities/Art Workshop/signup?email=test%2Buser@mergington.edu")
        
        # Unregister with URL encoding
        response = client.delete("/activities/Art%20Workshop/unregister?email=test%2Buser@mergington.edu")
        assert response.status_code == 200


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_missing_email_parameter(self, client, reset_activities):
        """Test endpoints with missing email parameter"""
        # Test signup without email
        response1 = client.post("/activities/Basketball Team/signup")
        assert response1.status_code == 422  # Validation error
        
        # Test unregister without email
        response2 = client.delete("/activities/Basketball Team/unregister")
        assert response2.status_code == 422  # Validation error
        
    def test_empty_email_parameter(self, client, reset_activities):
        """Test endpoints with empty email parameter"""
        # The API currently accepts empty emails, so we test the actual behavior
        response1 = client.post("/activities/Basketball Team/signup?email=")
        assert response1.status_code == 200  # Empty email is currently accepted
        
        response2 = client.delete("/activities/Basketball Team/unregister?email=")
        assert response2.status_code == 200  # Empty email removal is accepted
        
    def test_invalid_activity_names(self, client, reset_activities):
        """Test with various invalid activity names"""
        invalid_names = ["", "   ", "NonExistent", "basketball team"]  # Case sensitive
        
        for name in invalid_names:
            response1 = client.post(f"/activities/{name}/signup?email=test@mergington.edu")
            assert response1.status_code == 404
            
            response2 = client.delete(f"/activities/{name}/unregister?email=test@mergington.edu")
            assert response2.status_code == 404


class TestDataPersistence:
    """Test that data persists correctly across requests"""
    
    def test_multiple_signups_and_unregistrations(self, client, reset_activities):
        """Test complex scenario with multiple operations"""
        # Sign up multiple students for different activities
        students = [
            ("student1@mergington.edu", "Basketball Team"),
            ("student2@mergington.edu", "Soccer Club"),
            ("student3@mergington.edu", "Drama Club")
        ]
        
        for email, activity in students:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
            
        # Verify all students were added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for email, activity in students:
            assert email in activities_data[activity]["participants"]
            
        # Unregister one student
        response = client.delete("/activities/Basketball Team/unregister?email=student1@mergington.edu")
        assert response.status_code == 200
        
        # Verify only that student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        assert "student1@mergington.edu" not in activities_data["Basketball Team"]["participants"]
        assert "student2@mergington.edu" in activities_data["Soccer Club"]["participants"]
        assert "student3@mergington.edu" in activities_data["Drama Club"]["participants"]