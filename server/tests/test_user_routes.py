async def test_create_user(client):
    user_data = {"username": "newuser", "password": "newpassword", "dob": "2000-01-01", "country": "Nowhere"}
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']

async def test_read_user(client):
    # Assume user_id 1 exists; adjust accordingly based on your test setup
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1

async def test_update_user(client):
    user_data = {"username": "updateduser", "password": "updatedpassword", "dob": "2001-01-01", "country": "Somewhere"}
    response = client.put("/api/users/1", json=user_data)
    assert response.status_code == 200
    assert response.json()['username'] == user_data['username']

async def test_delete_user(client):
    response = client.delete("/api/users/1")
    assert response.status_code == 204
