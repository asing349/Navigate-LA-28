# server/tests/test_user_routes.py
from httpx import AsyncClient
import pytest
import bcrypt

from main import app
from models.user import User as UserModel


@pytest.mark.asyncio
async def test_create_user(async_db):
    """Test the creation of a new user."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {"username": "newuser", "password": "newpassword",
                     "dob": "2000-01-01", "country": "Nowhere"}
        response = await ac.post("/api/users/", json=user_data)
        assert response.status_code == 201
        json_response = response.json()
        assert json_response['username'] == user_data['username']
        assert "id" in json_response  # Ensure the response contains an ID


@pytest.mark.asyncio
async def test_read_user(async_db):
    """Test retrieving a user by ID."""
    # Create a mock user in the test database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="testuser", password=hashed_password,
                         dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()  # Ensure the user is added before proceeding
        user_id = user.id

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        json_response = response.json()
        assert json_response['id'] == user_id
        assert json_response['username'] == "testuser"


@pytest.mark.asyncio
async def test_update_user(async_db):
    """Test updating an existing user."""
    # Create a mock user in the test database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="olduser", password=hashed_password,
                         dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()
        user_id = user.id

    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {"username": "updateduser", "password": "updatedpassword",
                     "dob": "2001-01-01", "country": "Somewhere"}
        response = await ac.put(f"/api/users/{user_id}", json=user_data)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response['username'] == user_data['username']


@pytest.mark.asyncio
async def test_delete_user(async_db):
    """Test deleting an existing user."""
    # Create a mock user in the test database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="deletableuser",
                         password=hashed_password, dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()
        user_id = user.id

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/users/{user_id}")
        assert response.status_code == 204

        # Verify the user has been deleted
        response = await ac.get(f"/api/users/{user_id}")
        assert response.status_code == 404
