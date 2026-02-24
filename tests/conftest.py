import sys
import copy
from pathlib import Path

import pytest
import httpx
from fastapi.testclient import TestClient
import importlib

# Ensure src/ is importable so tests can import the app module as `app`
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

app_module = importlib.import_module("app")


@pytest.fixture
def client():
    """Sync TestClient for FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture
async def async_client():
    """Async httpx AsyncClient for FastAPI app."""
    async with httpx.AsyncClient(app=app_module.app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def activities_snapshot():
    """
    Deep-copy `src.app.activities` before a test and restore it after the test.
    Use this fixture in tests that mutate `app.activities`.
    """
    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)
