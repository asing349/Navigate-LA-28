# server/tests/test_user_routes.py

from httpx import AsyncClient  # For making asynchronous HTTP requests
import pytest  # For defining and running tests
import bcrypt  # For hashing passwords

from main import app  # The FastAPI application instance
from models.user import User as UserModel  # Model for the `users` table


@pytest.mark.asyncio
async def test_create_user(async_db):
    """
    Test the creation of a new user.

    Workflow:
        1. Send a POST request to the user creation endpoint with user data.
        2. Verify that the response status code is 201 (Created).
        3. Assert that the returned user data matches the input data.
        4. Ensure the response contains a unique user ID.

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # User data for the test
        user_data = {
            "username": "newuser",
            "password": "newpassword",
            "dob": "2000-01-01",
            "country": "Nowhere",
        }
        # Send POST request to create a user
        response = await ac.post("/api/users/", json=user_data)
        # Assert response status is 201
        assert response.status_code == 201
        json_response = response.json()
        # Assert returned username matches the input
        assert json_response["username"] == user_data["username"]
        # Assert the response contains a unique ID
        assert "id" in json_response


@pytest.mark.asyncio
async def test_read_user(async_db):
    """
    Test retrieving a user by ID.

    Workflow:
        1. Create a mock user in the test database.
        2. Send a GET request to retrieve the user by ID.
        3. Verify that the response status code is 200 (OK).
        4. Assert that the returned user data matches the expected data.

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    # Create a mock user in the database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="testuser", password=hashed_password,
                         dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()  # Ensure the user is added to the database
        user_id = user.id  # Retrieve the user's ID

    # Send a GET request to retrieve the user by ID
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id}")
        # Assert response status is 200
        assert response.status_code == 200
        json_response = response.json()
        # Assert returned data matches the mock user's data
        assert json_response["id"] == user_id
        assert json_response["username"] == "testuser"


@pytest.mark.asyncio
async def test_update_user(async_db):
    """
    Test updating an existing user.

    Workflow:
        1. Create a mock user in the test database.
        2. Send a PUT request to update the user's details.
        3. Verify that the response status code is 200 (OK).
        4. Assert that the returned user data reflects the updates.

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    # Create a mock user in the database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="olduser", password=hashed_password,
                         dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()  # Ensure the user is added to the database
        user_id = user.id  # Retrieve the user's ID

    # Send a PUT request to update the user's details
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_data = {
            "username": "updateduser",
            "password": "updatedpassword",
            "dob": "2001-01-01",
            "country": "Somewhere",
        }
        response = await ac.put(f"/api/users/{user_id}", json=user_data)
        # Assert response status is 200
        assert response.status_code == 200
        json_response = response.json()
        # Assert the updated username matches the input
        assert json_response["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_delete_user(async_db):
    """
    Test deleting an existing user.

    Workflow:
        1. Create a mock user in the test database.
        2. Send a DELETE request to delete the user by ID.
        3. Verify that the response status code is 204 (No Content).
        4. Attempt to retrieve the deleted user and verify that the response status code is 404 (Not Found).

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    # Create a mock user in the database
    async with async_db.begin():
        hashed_password = bcrypt.hashpw("testpassword".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username="deletableuser",
                         password=hashed_password, dob="1990-01-01", country="Nowhere")
        async_db.add(user)
        await async_db.flush()  # Ensure the user is added to the database
        user_id = user.id  # Retrieve the user's ID

    # Send a DELETE request to delete the user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/users/{user_id}")
        # Assert response status is 204
        assert response.status_code == 204

        # Verify the user has been deleted
        response = await ac.get(f"/api/users/{user_id}")
        # Assert response status is 404
        assert response.status_code == 404
