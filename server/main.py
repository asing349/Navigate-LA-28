from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Import the api_router from routes module
from routes import api_router

load_dotenv()

database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")

app = FastAPI()

# Include the API router that registers all routes
app.include_router(api_router, prefix="/api", tags=["API"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
