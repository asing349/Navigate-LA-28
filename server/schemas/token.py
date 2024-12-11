# server/schemas/token.py

from pydantic import BaseModel  # Base class for defining Pydantic schemas


class Token(BaseModel):
    """
    Schema representing an authentication token.

    Attributes:
        access_token (str): The actual token string used for authentication.
        token_type (str): The type of token, typically "bearer".
    """
    access_token: str  # The token string used for user authentication
    token_type: str  # The type of token, e.g., "bearer"
