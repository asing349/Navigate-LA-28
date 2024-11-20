from httpx import AsyncClient
import pytest
from main import app  # Make sure to import your FastAPI app correctly

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {"username": "newuser", "password": "newpassword", "dob": "2000-01-01", "country": "Nowhere"}
        response = await ac.post("/api/users/", json=user_data)
        assert response.status_code == 201
        assert response.json()['username'] == user_data['username']

@pytest.mark.asyncio
async def test_read_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Assume user_id 1 exists; adjust accordingly based on your test setup
        response = await ac.get("/api/users/1")
        assert response.status_code == 200
        assert response.json()['id'] == 1

@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {"username": "updateduser", "password": "updatedpassword", "dob": "2001-01-01", "country": "Somewhere"}
        response = await ac.put("/api/users/1", json=user_data)
        assert response.status_code == 200
        assert response.json()['username'] == user_data['username']

@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/api/users/1")
        assert response.status_code == 204
