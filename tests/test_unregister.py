import pytest
import app as app_module


def test_unregister_existing_participant_sync(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    participant = app_module.activities[activity]["participants"][0]
    assert participant in app_module.activities[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": participant})

    # Assert
    assert response.status_code == 200
    assert participant not in app_module.activities[activity]["participants"]
    assert response.json() == {"message": f"Removed {participant} from {activity}"}


def test_unregister_nonexistent_participant_sync(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    email = "not-signed-up@example.com"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_missing_activity_sync(client, activities_snapshot):
    # Arrange
    activity = "No Such Activity"
    email = "someone@example.com"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unregister_existing_participant_async(async_client, activities_snapshot):
    # Arrange
    activity = "Programming Class"
    participant = __import__("app").activities[activity]["participants"][0]
    assert participant in __import__("app").activities[activity]["participants"]

    # Act
    response = await async_client.delete(f"/activities/{activity}/participants", params={"email": participant})

    # Assert
    assert response.status_code == 200
    assert participant not in __import__("app").activities[activity]["participants"]
