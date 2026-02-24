import pytest
import app as app_module


def test_signup_new_student_sync(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@example.com"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module.activities[activity]["participants"]


def test_signup_existing_student_sync(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]
    before = list(app_module.activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing})

    # Assert
    assert response.status_code == 400
    assert app_module.activities[activity]["participants"] == before


def test_signup_missing_activity_sync(client, activities_snapshot):
    # Arrange
    activity = "Nonexistent Activity"
    email = "someone@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_signup_new_student_async(async_client, activities_snapshot):
    # Arrange
    activity = "Programming Class"
    email = "asyncstudent@example.com"
    assert email not in __import__("app").activities[activity]["participants"]

    # Act
    response = await async_client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in __import__("app").activities[activity]["participants"]
