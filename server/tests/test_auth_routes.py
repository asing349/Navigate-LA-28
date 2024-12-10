# server/tests/test_auth_routes.py
from httpx import AsyncClient
import pytest

from main import app


@pytest.mark.asyncio
async def test_login_for_access_token(async_db):
    """Test valid login for access token retrieval."""
    # Mock user creation in the database
    async with async_db.begin():
        from models.user import User as UserModel
        import bcrypt
        hashed_password = bcrypt.hashpw("password123".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(
            username="testuser", password=hashed_password, dob="2000-01-01", country="US")
        async_db.add(user)

    # Perform the login request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/token", data={"username": "testuser", "password": "password123"})
        assert response.status_code == 200
        json_response = response.json()
        assert "access_token" in json_response
        assert json_response["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_bad_credentials(async_db):
    """Test login with incorrect credentials."""
    # Mock user creation in the database
    async with async_db.begin():
        from models.user import User as UserModel
        import bcrypt
        hashed_password = bcrypt.hashpw("password123".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(
            username="testuser", password=hashed_password, dob="2000-01-01", country="US")
        async_db.add(user)

    # Attempt login with incorrect credentials
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/token", data={"username": "baduser", "password": "badpass"})
        assert response.status_code == 401
        json_response = response.json()
        assert "detail" in json_response
        assert json_response["detail"] == "Incorrect username or password"
