# server/tests/test_auth_routes.py

from httpx import AsyncClient  # For making asynchronous HTTP requests
import pytest  # For defining and running tests

from main import app  # The FastAPI application instance


@pytest.mark.asyncio
async def test_login_for_access_token(async_db):
    """
    Test valid login for access token retrieval.

    Workflow:
        1. Mock the creation of a user in the database.
        2. Perform a POST request to the login endpoint with valid credentials.
        3. Assert the response status code is 200.
        4. Verify that the response contains an access token and the correct token type.

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    # Mock user creation in the database
    async with async_db.begin():  # Begin a database transaction
        from models.user import User as UserModel  # Import the User model
        import bcrypt  # For hashing passwords
        # Hash the password
        hashed_password = bcrypt.hashpw("password123".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        # Create a user instance
        user = UserModel(
            username="testuser",
            password=hashed_password,
            dob="2000-01-01",
            country="US"
        )
        async_db.add(user)  # Add the user to the database

    # Perform the login request
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send POST request with valid credentials
        response = await ac.post("/api/auth/token", data={"username": "testuser", "password": "password123"})
        # Assert the response status code is 200 (success)
        assert response.status_code == 200
        json_response = response.json()  # Parse the JSON response
        # Assert the presence of an access token
        assert "access_token" in json_response
        # Assert the token type is "bearer"
        assert json_response["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_bad_credentials(async_db):
    """
    Test login with incorrect credentials.

    Workflow:
        1. Mock the creation of a user in the database.
        2. Perform a POST request to the login endpoint with incorrect credentials.
        3. Assert the response status code is 401 (Unauthorized).
        4. Verify that the response contains the appropriate error message.

    Args:
        async_db (AsyncSession): The asynchronous test database session.
    """
    # Mock user creation in the database
    async with async_db.begin():  # Begin a database transaction
        from models.user import User as UserModel  # Import the User model
        import bcrypt  # For hashing passwords
        # Hash the password
        hashed_password = bcrypt.hashpw("password123".encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        # Create a user instance
        user = UserModel(
            username="testuser",
            password=hashed_password,
            dob="2000-01-01",
            country="US"
        )
        async_db.add(user)  # Add the user to the database

    # Attempt login with incorrect credentials
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send POST request with invalid credentials
        response = await ac.post("/api/auth/token", data={"username": "baduser", "password": "badpass"})
        # Assert the response status code is 401 (Unauthorized)
        assert response.status_code == 401
        json_response = response.json()  # Parse the JSON response
        # Assert the response contains an error message
        assert "detail" in json_response
        assert json_response["detail"] == "Incorrect username or password"
