def test_get_activities_returns_expected_shape(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) > 0

    for activity_name, details in payload.items():
        assert isinstance(activity_name, str)
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)
