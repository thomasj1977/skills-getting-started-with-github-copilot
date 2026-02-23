import urllib.parse

import src.app as app_module


def test_get_activities_returns_all(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    # each activity should have the expected keys
    for v in data.values():
        assert "description" in v
        assert "schedule" in v
        assert "max_participants" in v
        assert "participants" in v


def test_signup_success(client):
    activity = "Chess Club"
    email = "testuser@example.com"
    assert email not in app_module.activities[activity]["participants"]

    resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )

    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]
    assert email in resp.json().get("message", "")


def test_signup_duplicate_returns_400(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already present in sample data
    before = list(app_module.activities[activity]["participants"])

    resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )

    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up for this activity"
    assert app_module.activities[activity]["participants"] == before


def test_signup_activity_not_found_returns_404(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=test@example.com")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"


def test_unregister_success(client):
    activity = "Basketball Team"
    email = "james@mergington.edu"
    assert email in app_module.activities[activity]["participants"]

    resp = client.delete(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )

    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
    assert email in resp.json().get("message", "")


def test_unregister_not_signed_up_returns_404(client):
    activity = "Chess Club"
    email = "nobody@example.com"
    assert email not in app_module.activities[activity]["participants"]

    resp = client.delete(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )

    assert resp.status_code == 404
    assert resp.json().get("detail") == "Student not signed up for this activity"


def test_unregister_activity_not_found_returns_404(client):
    resp = client.delete("/activities/NoSuchActivity/signup?email=test@example.com")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"
