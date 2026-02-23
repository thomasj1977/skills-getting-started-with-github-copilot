"""
Pytest fixtures for FastAPI tests.

Fixtures provided:
- `client`: FastAPI TestClient for the app at `src.app:app`.
- `activities_snapshot` (autouse): snapshots `src.app.activities` before each test and restores it after,
  ensuring tests are isolated and can modify the in-memory data safely.

Run tests:
    pytest -q

Tests follow Arrange-Act-Assert (AAA) pattern.
"""

import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def activities_snapshot():
    """Snapshot and restore the in-memory activities dict for each test."""
    snapshot = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(snapshot)
