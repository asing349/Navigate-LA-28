# server/middleware/cors_config.py
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """
    Add CORS middleware to the FastAPI application.
    """
    origins = [
        "http://localhost:3000",  # React frontend running locally
        "http://localhost:3030",  # Another local port if used
        "https://your-production-domain.com",  # Add your production domain here
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allow only specified origins
        allow_credentials=True,  # Allow cookies to be sent in cross-origin requests
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
