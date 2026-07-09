from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Software Engineer",
            "status": "Applied",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Google"
    assert data["position"] == "Software Engineer"
    assert data["status"] == "Applied"
    assert "id" in data


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_one_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Amazon",
            "position": "SDE",
            "status": "Applied",
        },
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id


def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Meta",
            "position": "Backend Engineer",
            "status": "Applied",
        },
    )

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "company": "Meta",
            "position": "Backend Engineer",
            "status": "Interview",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Netflix",
            "position": "Software Engineer",
            "status": "Applied",
        },
    )

    application_id = create_response.json()["id"]

    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 204

    get_response = client.get(f"/applications/{application_id}")

    assert get_response.status_code == 404