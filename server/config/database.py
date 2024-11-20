from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the database URL from environment variables or default to a placeholder
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Create the SQLAlchemy asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory using the asynchronous engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    """
    Dependency that provides a database session for request handling.
    Ensures proper closure of the session in an asynchronous context.
    """
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            # The context manager ensures the session is closed after use
            await db.close()
