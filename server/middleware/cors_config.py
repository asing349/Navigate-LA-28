# server/middleware/cors_config.py

# FastAPI's built-in middleware for handling CORS
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app):
    """
    Add CORS (Cross-Origin Resource Sharing) middleware to the FastAPI application.

    CORS allows a server to specify which origins are permitted to access resources,
    enabling secure cross-origin requests in web applications.

    Args:
        app (FastAPI): The FastAPI application instance to which the middleware will be added.
    """
    # List of allowed origins
    origins = [
        # React frontend running locally (default development setup)
        "http://localhost:3000",
        "http://localhost:3030",  # Alternate local port for React frontend
        # Production domain (replace with actual domain)
        "https://your-production-domain.com",
    ]

    # Add the CORS middleware to the FastAPI application
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Specify the allowed origins
        # Enable credentials (e.g., cookies, authorization headers)
        allow_credentials=True,
        # Allow all HTTP methods (e.g., GET, POST, PUT, DELETE)
        allow_methods=["*"],
        allow_headers=["*"],  # Allow all headers in the requests
    )
