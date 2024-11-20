async def test_login_for_access_token(client):
    # Create a user first or load it if your test database prepopulates data
    response = client.post("/api/auth/token", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

async def test_login_bad_credentials(client):
    response = client.post("/api/auth/token", data={"username": "baduser", "password": "badpass"})
    assert response.status_code == 401
