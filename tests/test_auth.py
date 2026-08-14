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


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "haslo"})
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "haslo"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "haslo"})
    response = client.post(
        "/auth/login",
        data={"username": "wrong@example.com", "password": "zlehaslo"},
    )
    assert response.status_code == 401