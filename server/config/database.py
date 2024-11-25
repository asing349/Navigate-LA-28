from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from yarl import URL as MultiHostUrl
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "la28_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bigdata_la28")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "navigate_la28_db")

    @property
    def database_url(self) -> str:
        logger.info(
            f"Attempting to connect to: {self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
        )
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=int(self.POSTGRES_PORT),
                path=f"/{self.POSTGRES_DB}",
            )
        )


db_config = DatabaseConfig()
engine = create_async_engine(
    db_config.database_url, echo=True, future=True, pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
