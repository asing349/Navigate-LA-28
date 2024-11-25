import asyncio
from config.database import engine
from models.base import Base

# Import all your models here
# from models.user import User
# from models.other_model import OtherModel


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
