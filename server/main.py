from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
