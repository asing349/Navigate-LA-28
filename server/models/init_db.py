# server/models/init_db.py

import asyncio  # Library for running asynchronous code
# Asynchronous database engine from the configuration
from config.database import engine
from models.base import Base  # Base class for all SQLAlchemy models

# Import population scripts for populating initial data into tables
# Populates the Places table
from scripts.populate_places import main as populate_places
from scripts.populate_users import main as populate_users  # Populates the Users table
# Populates the Reviews table
from scripts.populate_reviews import main as populate_reviews
# Populates the BusStops table
from scripts.populate_bus_stops import main as populate_bus_stops
# Populates the BusRouteUsages table
from scripts.populate_bus_route_usages import main as populate_bus_route_usages


async def create_tables():
    """
    Create or reset database tables.

    This function drops all existing tables and recreates them using the metadata
    defined in the Base class. This ensures the database schema is always in sync
    with the application models.
    """
    async with engine.begin() as conn:  # Open a connection to the database
        await conn.run_sync(Base.metadata.drop_all)  # Drop all existing tables
        await conn.run_sync(Base.metadata.create_all)  # Recreate all tables


async def populate_database():
    """
    Populate the database with initial data.

    This function runs a series of scripts that insert sample or necessary
    initial data into the database tables. The scripts must be imported and
    called in sequence to ensure dependencies are satisfied.
    """
    # Run population scripts in the defined order
    await populate_places()  # Populate the Places table
    await populate_users()  # Populate the Users table
    await populate_reviews()  # Populate the Reviews table
    await populate_bus_stops()  # Populate the BusStops table
    await populate_bus_route_usages()  # Populate the BusRouteUsages table

if __name__ == "__main__":
    """
    Main entry point for the script.

    This script initializes the database by:
    1. Dropping and recreating all tables.
    2. Populating the database with initial data.
    """
    asyncio.run(create_tables())  # Run the table creation process
    asyncio.run(populate_database())  # Run the database population process
