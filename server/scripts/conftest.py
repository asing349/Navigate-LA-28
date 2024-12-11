# server/tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from models.base import Base
from config.database import get_db

# Define an asynchronous fixture for the database


@pytest.fixture(scope="session")
async def async_engine():
    # Create an asynchronous engine for the test database
    engine = create_async_engine(
        "postgresql+asyncpg://la28_user:bigdata_la28@navigate_la_postgres:5432/navigate_la28_test_db",
        echo=True,
    )
    async with engine.begin() as conn:
        # Create all tables asynchronously
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        # Drop all tables asynchronously after tests
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="session")
async def async_db(async_engine):
    """Creates a new database session for testing."""
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
def client(async_db):
    """Creates a FastAPI test client with an overridden dependency."""
    def override_get_db():
        try:
            yield async_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Use FastAPI TestClient for synchronous testing
    with TestClient(app) as test_client:
        yield test_client
