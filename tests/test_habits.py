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