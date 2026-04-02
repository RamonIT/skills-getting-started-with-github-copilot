def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert "Signed up" in signup_response.json()["message"]
    participants = activities_response.json()[activity_name]["participants"]
    assert new_email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "notfound@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_then_unregister_flow(client):
    # Arrange
    activity_name = "Programming Class"
    email = "flowtest@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    after_signup = client.get("/activities")

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )
    after_unregister = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert email in after_signup.json()[activity_name]["participants"]

    assert unregister_response.status_code == 200
    assert email not in after_unregister.json()[activity_name]["participants"]
