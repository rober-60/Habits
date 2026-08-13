def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "yo@example.com", "password": "haaslo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "yo@example.com"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "yo@example.com", "password": "haslo"})
    response = client.post("/auth/register", json={"email": "yo@example.com", "password": "haslo"})
    assert response.status_code == 400