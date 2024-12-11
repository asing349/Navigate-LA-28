import asyncio
import csv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config.database import AsyncSessionFactory, engine
from models.base import Base
from models.bus_stops import BusStop


async def read_csv(file_path):
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[dict]: List of rows as dictionaries.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


async def populate_bus_stops_from_file(db: AsyncSession, file_path: str):
    """
    Populate the bus_stops table from a CSV file.

    Args:
        db (AsyncSession): Database session.
        file_path (str): Path to the CSV file.
    """
    try:
        rows = await read_csv(file_path)
        for row in rows:
            bus_stop = BusStop(
                stop_number=int(row["STOPNUM"]),
                line=row["LINE"],
                direction=row["DIR"],
                stop_name=row["STOPNAME"],
                latitude=float(row["LAT"]),
                longitude=float(row["LONG"]),
                geometry=row["geometry"],
            )
            db.add(bus_stop)

        # Commit the transaction
        await db.commit()
        print(f"Successfully populated bus stops from {file_path}.")
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


async def main():
    """
    Main script entry point to populate bus stops from CSV file.
    """
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Created database tables")

    # Populate data
    file_path = "bus_stops.csv"

    async with AsyncSessionFactory() as db:
        await populate_bus_stops_from_file(db, file_path)


if __name__ == "__main__":
    asyncio.run(main())

# To run:
# docker exec -it navigate_la_backend bash
# python tests/populate_bus_stops.py

# To verify:
# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT COUNT(*) FROM bus_stops;
# SELECT * FROM bus_stops LIMIT 5;
