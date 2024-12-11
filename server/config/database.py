# For asynchronous database engine and session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# Factory for creating database sessions
from sqlalchemy.orm import sessionmaker
# Base model class for SQLAlchemy, imports and initializes all models
from models import Base
from yarl import URL as MultiHostUrl  # Utility for building database URLs
import os  # For environment variable access
from dotenv import load_dotenv  # For loading environment variables from a .env file
import logging  # For logging configuration

# Load environment variables from a .env file
load_dotenv()

# Configure logging
# Set logging level to INFO for detailed logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Create a logger for this module


# Database configuration class to encapsulate database connection settings
class DatabaseConfig:
    # Read database credentials and connection details from environment variables
    POSTGRES_USER = os.getenv("POSTGRES_USER", "la28_user")  # Default username
    POSTGRES_PASSWORD = os.getenv(
        "POSTGRES_PASSWORD", "bigdata_la28")  # Default password
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # Default hostname
    # Default PostgreSQL port
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    # Default database name
    POSTGRES_DB = os.getenv("POSTGRES_DB", "navigate_la28_db")

    @property
    def database_url(self) -> str:
        """
        Constructs the PostgreSQL database URL using the provided credentials.

        Returns:
            str: A properly formatted database URL.
        """
        logger.info(
            f"Attempting to connect to: {self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
        )  # Log connection details for debugging
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",  # Use the asyncpg driver for asynchronous operations
                user=self.POSTGRES_USER,  # Username for the database
                password=self.POSTGRES_PASSWORD,  # Password for the database
                host=self.POSTGRES_HOST,  # Hostname of the database server
                # Port number (converted to integer)
                port=int(self.POSTGRES_PORT),
                path=f"/{self.POSTGRES_DB}",  # Database name
            )
        )


# Instantiate the database configuration class
db_config = DatabaseConfig()

# Create an asynchronous database engine
engine = create_async_engine(
    db_config.database_url,  # Use the generated database URL
    echo=True,  # Enable SQL query logging for debugging
    future=True,  # Use the SQLAlchemy 2.0 future API
    pool_pre_ping=True,  # Test connections for liveness before using them
)

# Define a factory for creating asynchronous database sessions
AsyncSessionFactory = sessionmaker(
    engine,  # Bind the session to the database engine
    class_=AsyncSession,  # Use asynchronous sessions
    expire_on_commit=False,  # Prevent attributes from expiring after a commit
)


# Dependency function for FastAPI to get a database session
async def get_db():
    """
    Provides a database session to API routes.

    Yields:
        AsyncSession: An active database session.
    """
    async with AsyncSessionFactory() as session:  # Create a new session
        try:
            yield session  # Yield the session to the caller
        finally:
            await session.close()  # Ensure the session is properly closed
