from fastapi import FastAPI
from dotenv import load_dotenv
import os

from .routes.user_routes import router as user_router
from .routes.auth_routes import router as auth_router

load_dotenv()

database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")


app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(auth_router, prefix="/api", tags=["authentication"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
