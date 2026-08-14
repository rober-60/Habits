def register_and_login(client, email="habituser@example.com", password="haslo"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_habit(client):
    headers = register_and_login(client)
    response = client.post(
        "/habits/",
        json={"name": "Bieganie", "frequency": "daily"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bieganie"
    assert "id" in data


def test_two_users(client):
    headers_a = register_and_login(client, "usera@example.com", "pass1234")
    headers_b = register_and_login(client, "userb@example.com", "pass1234")

    client.post("/habits/", json={"name": "A's habit", "frequency": "daily"}, headers=headers_a)
    client.post("/habits/", json={"name": "B's habit", "frequency": "daily"}, headers=headers_b)

    response = client.get("/habits/", headers=headers_a)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "A's habit"


def test_check_streak(client):
    headers = register_and_login(client)
    habit = client.post(
        "/habits/", json={"name": "Czytanie", "frequency": "daily"}, headers=headers
    ).json()

    log_response = client.post(f"/habits/{habit['id']}/log", headers=headers)
    assert log_response.status_code == 200

    stats_response = client.get(f"/habits/{habit['id']}/stats", headers=headers)
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats["current_streak"] == 1


def test_delete_habit(client):
    headers = register_and_login(client)
    habit = client.post(
        "/habits/", json={"name": "Do usunięcia", "frequency": "daily"}, headers=headers
    ).json()

    delete_response = client.delete(f"/habits/{habit['id']}", headers=headers)
    assert delete_response.status_code == 200

    list_response = client.get("/habits/", headers=headers)
    assert list_response.json() == []

