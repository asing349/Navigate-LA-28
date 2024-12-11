# server/scripts/populate_bus_stops.py

import asyncio  # For asynchronous programming
import csv  # For reading CSV files
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError  # For handling database exceptions

# Import application-specific modules
# Database session factory and engine
from config.database import AsyncSessionFactory, engine
from models.base import Base  # Base class for SQLAlchemy models
from models.bus_stops import BusStop  # Model for bus stops


async def read_csv(file_path):
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[dict]: List of rows as dictionaries, where each dictionary represents a row.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Read CSV as a dictionary
        # Convert the reader object to a list of rows
        return [row for row in reader]


async def populate_bus_stops_from_file(db: AsyncSession, file_path: str):
    """
    Populate the bus_stops table from a CSV file.

    Args:
        db (AsyncSession): Database session used for inserting records.
        file_path (str): Path to the CSV file containing bus stop data.

    Workflow:
        1. Read the CSV file to extract bus stop data.
        2. Iterate through the rows and create `BusStop` objects.
        3. Add each `BusStop` object to the database session.
        4. Commit the transaction or handle errors if any occur.

    Raises:
        SQLAlchemyError: If a database error occurs, the transaction is rolled back.
        Exception: For any other unexpected errors.
    """
    try:
        # Read bus stop data from the CSV file
        rows = await read_csv(file_path)
        for row in rows:
            # Create a `BusStop` object for each row
            bus_stop = BusStop(
                stop_number=int(row["STOPNUM"]),  # Bus stop number
                line=row["LINE"],  # Bus line
                direction=row["DIR"],  # Direction of the bus line
                stop_name=row["STOPNAME"],  # Name of the bus stop
                latitude=float(row["LAT"]),  # Latitude of the bus stop
                longitude=float(row["LONG"]),  # Longitude of the bus stop
                geometry=row["geometry"],  # Geometry string for spatial data
            )
            db.add(bus_stop)  # Add the `BusStop` object to the database session

        # Commit the transaction to save changes
        await db.commit()
        print(f"Successfully populated bus stops from {file_path}.")
    except SQLAlchemyError as e:
        # Rollback the transaction in case of database errors
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        # Handle unexpected errors
        print(f"Error processing {file_path}: {str(e)}")


async def main():
    """
    Main script entry point to populate bus stops from a CSV file.

    Workflow:
        1. Create database tables if they do not already exist.
        2. Open a database session.
        3. Call the function to populate the bus_stops table with data from the CSV file.
    """
    # Create tables if they do not already exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create database tables
        print("Created database tables")

    # Path to the CSV file containing bus stop data
    file_path = "bus_stops.csv"

    # Populate bus stops data
    async with AsyncSessionFactory() as db:
        await populate_bus_stops_from_file(db, file_path)

if __name__ == "__main__":
    """
    Script execution entry point.

    Calls the main function to set up the database and populate it with data from the CSV file.
    """
    asyncio.run(main())  # Run the script using asyncio

# Instructions for running the script:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python scripts/populate_bus_stops.py

# Instructions for verifying the data:
# 1. Open a bash terminal inside the Postgres container:
#    docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# 2. Execute SQL queries to check the records:
#    SELECT COUNT(*) FROM bus_stops;
#    SELECT * FROM bus_stops LIMIT 5;
