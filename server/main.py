# server/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes import api_router  # Import the API router
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Fetch environment variables with defaults
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname"
)
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecretkey")

# Initialize the FastAPI app
app = FastAPI(
    title="Your API Title",
    description="Description of your API functionality.",
    version="1.0.0",
    docs_url="/docs",  # URL for Swagger UI
    redoc_url="/redoc",  # URL for ReDoc
    openapi_url="/openapi.json",  # URL for OpenAPI schema
)

# Add CORS middleware BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=False,  # Changed to False since we're using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api", tags=["API"])


@app.get("/")
async def read_root():
    """
    Root endpoint to verify the server is running.
    """
    return {"message": "Welcome to the API!"}
