# server/scripts/populate_places.py

import asyncio  # For asynchronous programming
import csv  # For reading CSV files
import re  # For parsing geometry strings
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError  # For handling database exceptions

# Import application-specific modules
from config.database import AsyncSessionFactory  # Database session factory
from models.place import Place  # Model for the `places` table


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


def extract_coordinates(geometry_str):
    """
    Extract latitude and longitude from a geometry string.

    Args:
        geometry_str (str): Geometry string in POINT format, e.g., "POINT (1234567.89 9876543.21)".

    Returns:
        Tuple[float, float]: Latitude and longitude as floats.

    Raises:
        ValueError: If the geometry string format is invalid.
    """
    match = re.search(r"POINT \(([-\d.]+) ([-\d.]+)\)", geometry_str)
    if match:
        # Extract and convert values
        longitude, latitude = map(float, match.groups())
        return latitude, longitude
    # Raise error for invalid format
    raise ValueError(f"Invalid geometry string: {geometry_str}")


async def populate_places_from_file(
    db: AsyncSession, file_path: str, columns: dict, default_type: str = None
):
    """
    Populate the `places` table from a CSV file.

    Args:
        db (AsyncSession): Database session used for inserting records.
        file_path (str): Path to the CSV file containing place data.
        columns (dict): Mapping of CSV columns to Place model fields.
        default_type (str): Default value for the "types" field, if applicable.

    Workflow:
        1. Read the CSV file to extract place data.
        2. Map CSV columns to `Place` model fields based on the provided column mapping.
        3. Extract latitude and longitude explicitly or from a geometry string.
        4. Add records to the database session and commit the transaction.
        5. Handle and log errors during the process.
    """
    try:
        rows = await read_csv(file_path)  # Read the CSV file
        for row in rows:
            place_data = {}

            # Map fields from CSV to Place model
            for csv_column, db_column in columns.items():
                if db_column in ["latitude", "longitude"]:
                    # Explicitly convert latitude and longitude to float
                    place_data[db_column] = float(row[csv_column])
                elif db_column in ["latitude", "longitude"] and csv_column == "geometry":
                    # Extract latitude and longitude from geometry
                    latitude, longitude = extract_coordinates(row[csv_column])
                    place_data["latitude"] = latitude
                    place_data["longitude"] = longitude
                else:
                    # Map other fields directly
                    place_data[db_column] = row.get(csv_column)

            # Set the `types` field if a default type is provided
            if default_type:
                place_data["types"] = default_type

            # Create a Place model instance
            place = Place(**place_data)
            db.add(place)  # Add the record to the session

        # Commit the transaction
        await db.commit()
        print(f"Successfully populated places from {file_path}.")
    except SQLAlchemyError as e:
        # Rollback the transaction in case of database errors
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        # Handle unexpected errors
        print(f"Error processing {file_path}: {str(e)}")


async def main():
    """
    Main script entry point to populate places from CSV files.

    Workflow:
        1. Define file paths and column mappings for the CSV files.
        2. Open a database session.
        3. Call the function to populate the `places` table with data from each file.
    """
    # File paths and column mappings for CSV files
    files = [
        # Uncomment and modify this block to include other datasets
        # {
        #     "path": "/app/datasets/all_parks.csv",
        #     "columns": {
        #         "Name": "name",
        #         "Address": "address",
        #         "geometry": "geometry",  # Extract latitude and longitude from geometry
        #     },
        #     "type": "park",
        # },
        {
            "path": "all_places.csv",  # File path for places
            "columns": {
                "name": "name",
                "latitude": "latitude",
                "longitude": "longitude",
                "address": "address",
            },
            "type": "tourist attraction",  # Default type for this dataset
        },
        {
            "path": "all_restrooms.csv",  # File path for restrooms
            "columns": {
                "name": "name",
                "latitude": "latitude",
                "longitude": "longitude",
                "address": "address",
            },
            "type": "restroom",  # Default type for this dataset
        },
    ]

    # Database session
    async with AsyncSessionFactory() as db:
        for file in files:
            # Populate places for each file
            await populate_places_from_file(
                db, file["path"], file["columns"], file.get("type")
            )

if __name__ == "__main__":
    """
    Script execution entry point.

    Calls the main function to populate the `places` table with data from multiple CSV files.
    """
    asyncio.run(main())  # Run the script using asyncio

# Instructions for running the script:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python scripts/populate_places.py

# Instructions for verifying the data:
# 1. Open a bash terminal inside the Postgres container:
#    docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# 2. Execute SQL queries to check the records:
#    SELECT COUNT(*) FROM places;
#    SELECT types, COUNT(*) FROM places GROUP BY types;
#    SELECT * FROM places LIMIT 10;
