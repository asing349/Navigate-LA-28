import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy import select, Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from config.database import AsyncSessionFactory, engine
from models.base import Base
from models.bus_route_usage import BusRouteUsage
from models.user import User
from models.bus_stops import BusStop


async def populate_random_bus_route_usages(db: AsyncSession, num_records: int = 1000):
    """
    Populate the customer_usage table with random usage data.

    Args:
        db (AsyncSession): Database session.
        num_records (int): Number of random records to generate.
    """
    try:
        # Get all existing users and bus stops
        users = (await db.execute(select(User))).scalars().all()
        bus_stops = (await db.execute(select(BusStop))).scalars().all()

        if not users or not bus_stops:
            print("Error: No existing users or bus stops found in the database")
            return

        # Generate random usage records
        for _ in range(num_records):
            user = random.choice(users)
            # Select two different bus stops for origin and destination
            origin_stop = random.choice(bus_stops)
            destination_stops = [
                stop for stop in bus_stops if stop.id != origin_stop.id
            ]
            destination_stop = random.choice(destination_stops)

            usage = BusRouteUsage(
                user_id=user.id,
                origin_stop_id=origin_stop.id,
                destination_stop_id=destination_stop.id,
            )
            db.add(usage)

        await db.commit()
        print(f"Successfully generated {num_records} random bus route usages.")
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        print(f"Error generating random data: {str(e)}")


async def main():
    """
    Main script entry point to populate random bus route usages.
    """
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Created database tables")

    # Populate data
    async with AsyncSessionFactory() as db:
        await populate_random_bus_route_usages(db)


if __name__ == "__main__":
    asyncio.run(main())

# To run:
# docker exec -it navigate_la_backend bash
# python tests/populate_bus_route_usages.py

# To verify:
# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT COUNT(*) FROM customer_usage;
# SELECT * FROM customer_usage LIMIT 5;
