from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Update the DATABASE_URL to use asyncpg instead of psycopg2
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Update with your actual credentials
    "postgresql+asyncpg://postgres:postgres@localhost:5432/navigate_la",
)

# Make sure it's using asyncpg
if "postgresql://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)
