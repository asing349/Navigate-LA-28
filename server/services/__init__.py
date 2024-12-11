# server/services/__init__.py

# Importing all necessary functions from the user services
from services.user_service import (
    create_user,  # Function to create a new user
    get_user,     # Function to retrieve a user by ID
    delete_user,  # Function to delete a user by ID
    update_user   # Function to update user details
)

# Importing all necessary functions from the review services
from services.review_service import (
    create_review,  # Function to create a new review
    get_review,     # Function to retrieve a review by ID
    update_review,  # Function to update an existing review
    delete_review   # Function to delete a review by ID
)

# Importing all necessary functions from the auth services
from services.auth_service import (
    authenticate_user,  # Function to authenticate a user with credentials
    create_access_token,  # Function to generate an access token for authentication
    get_password_hash,    # Function to hash a plain text password
    verify_password       # Function to verify a plain text password against a hashed one
)
