from httpx import AsyncClient
import pytest
from main import app  # Ensure to import your FastAPI app correctly

@pytest.mark.asyncio
async def test_login_for_access_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/token", data={"username": "testuser", "password": "password123"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_bad_credentials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/token", data={"username": "baduser", "password": "badpass"})
        assert response.status_code == 401
