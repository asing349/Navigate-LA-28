import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app 
from models.base import Base

# Define an asynchronous fixture for the database
@pytest.fixture(scope="session")
async def async_engine():
    # Use the async engine here
    engine = create_async_engine(
        "postgresql+asyncpg://la28_user:bigdata_la28@navigate_la_postgres:5432/navigate_la28_test_db",
        echo=True,
    )
    async with engine.begin() as conn:
        # Create all tables asynchronously
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    async with engine.begin() as conn:
        # Drop all tables asynchronously
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture(scope="session")
async def async_db(async_engine):
    """Creates a new database session for a test."""
    connection = await async_engine.connect()
    transaction = await connection.begin()
    session = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False
    )()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest.fixture
def client(async_db):
    def override_get_db():
        try:
            yield async_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
