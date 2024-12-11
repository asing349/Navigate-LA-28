import asyncio
from config.database import engine
from models.base import Base

# Import populate scripts
from scripts.populate_places import main as populate_places
from scripts.populate_users import main as populate_users
from scripts.populate_reviews import main as populate_reviews
from scripts.populate_bus_stops import main as populate_bus_stops
from scripts.populate_bus_route_usages import main as populate_bus_route_usages


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def populate_database():
    # Run populate scripts in sequence
    await populate_places()
    await populate_users()
    await populate_reviews()
    await populate_bus_stops()
    await populate_bus_route_usages()


if __name__ == "__main__":
    asyncio.run(create_tables())
    asyncio.run(populate_database())
