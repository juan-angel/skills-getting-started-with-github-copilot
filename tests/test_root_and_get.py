import app as app_module


def test_root_redirect(client, activities_snapshot):
    # Arrange: nothing special

    # Act
    response = client.get("/", allow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_sync(client, activities_snapshot):
    # Arrange
    expected_keys = set(app_module.activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == expected_keys


import pytest


@pytest.mark.asyncio
async def test_get_activities_async(async_client):
    # Arrange: none

    # Act
    response = await async_client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
