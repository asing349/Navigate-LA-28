# server/scripts/populate_bus_route_usages.py

import asyncio  # For asynchronous programming
import random  # For generating random selections
from datetime import datetime, timedelta  # For working with timestamps
# SQLAlchemy utilities
from sqlalchemy import select, Column, Integer, ForeignKey, DateTime, func
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError  # For handling database errors
from sqlalchemy.orm import relationship  # For defining relationships in models

# Import application-specific modules
# Database session factory and engine
from config.database import AsyncSessionFactory, engine
from models.base import Base  # Base class for SQLAlchemy models
from models.bus_route_usage import BusRouteUsage  # Model for bus route usages
from models.user import User  # Model for users
from models.bus_stops import BusStop  # Model for bus stops


async def populate_random_bus_route_usages(db: AsyncSession, num_records: int = 1000):
    """
    Populate the bus_route_usage table with random usage data.

    Args:
        db (AsyncSession): The database session used for inserting data.
        num_records (int): The number of random records to generate (default: 1000).

    Workflow:
        1. Retrieve all users and bus stops from the database.
        2. Randomly select a user, an origin stop, and a destination stop for each record.
        3. Ensure the origin and destination stops are not the same.
        4. Insert the generated records into the database.
        5. Commit the changes or handle errors if any occur.

    Raises:
        SQLAlchemyError: If a database error occurs, the transaction is rolled back.
        Exception: For all other unexpected errors.
    """
    try:
        # Retrieve all users and bus stops from the database
        users = (await db.execute(select(User))).scalars().all()
        bus_stops = (await db.execute(select(BusStop))).scalars().all()

        if not users or not bus_stops:
            print("Error: No existing users or bus stops found in the database")
            return

        # Generate random usage records
        for _ in range(num_records):
            user = random.choice(users)  # Randomly select a user
            # Randomly select an origin stop
            origin_stop = random.choice(bus_stops)

            # Ensure destination stop is different from origin stop
            destination_stops = [
                stop for stop in bus_stops if stop.id != origin_stop.id
            ]
            destination_stop = random.choice(destination_stops)

            # Create a new BusRouteUsage record
            usage = BusRouteUsage(
                user_id=user.id,
                origin_stop_id=origin_stop.id,
                destination_stop_id=destination_stop.id,
            )
            db.add(usage)  # Add the record to the session

        # Commit the transaction
        await db.commit()
        print(f"Successfully generated {num_records} random bus route usages.")
    except SQLAlchemyError as e:
        # Rollback the transaction in case of database errors
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        # Handle unexpected errors
        print(f"Error generating random data: {str(e)}")


async def main():
    """
    Main script entry point to populate random bus route usages.

    Workflow:
        1. Create database tables if they do not already exist.
        2. Open a database session.
        3. Call the function to populate the bus_route_usage table with random data.
    """
    # Create tables if they do not already exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Created database tables")

    # Populate random bus route usage data
    async with AsyncSessionFactory() as db:
        await populate_random_bus_route_usages(db)

if __name__ == "__main__":
    """
    Script execution entry point.

    Calls the main function to set up the database and populate it with random data.
    """
    asyncio.run(main())  # Run the script using asyncio

# Instructions for running the script:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python scripts/populate_bus_route_usages.py

# Instructions for verifying the data:
# 1. Open a bash terminal inside the Postgres container:
#    docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# 2. Execute SQL queries to check the records:
#    SELECT COUNT(*) FROM bus_route_usage;
#    SELECT * FROM bus_route_usage LIMIT 5;
