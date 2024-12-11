# server/populate_places.py
import asyncio
import csv
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config.database import AsyncSessionFactory
from models.place import Place


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


def extract_coordinates(geometry_str):
    """
    Extract latitude and longitude from a geometry string.

    Args:
        geometry_str (str): Geometry string in POINT format, e.g., "POINT (1234567.89 9876543.21)".

    Returns:
        Tuple[float, float]: Latitude and longitude as floats.
    """
    match = re.search(r"POINT \(([-\d.]+) ([-\d.]+)\)", geometry_str)
    if match:
        longitude, latitude = map(float, match.groups())
        return latitude, longitude
    raise ValueError(f"Invalid geometry string: {geometry_str}")


async def populate_places_from_file(
    db: AsyncSession, file_path: str, columns: dict, default_type: str = None
):
    """
    Populate the places table from a CSV file.

    Args:
        db (AsyncSession): Database session.
        file_path (str): Path to the CSV file.
        columns (dict): Mapping of CSV columns to Place model fields.
        default_type (str): Default value for the "types" field.
    """
    try:
        rows = await read_csv(file_path)
        for row in rows:
            place_data = {}

            # Map fields
            for csv_column, db_column in columns.items():
                if db_column in ["latitude", "longitude"]:
                    # Explicitly convert latitude and longitude to float
                    place_data[db_column] = float(row[csv_column])
                elif (
                    db_column in ["latitude", "longitude"] and csv_column == "geometry"
                ):
                    latitude, longitude = extract_coordinates(row[csv_column])
                    place_data["latitude"] = latitude
                    place_data["longitude"] = longitude
                else:
                    place_data[db_column] = row.get(csv_column)

            # Set the `types` field explicitly if a `default_type` is provided
            if default_type:
                place_data["types"] = default_type

            # Create a Place model instance
            place = Place(**place_data)
            db.add(place)

        # Commit the transaction
        await db.commit()
        print(f"Successfully populated places from {file_path}.")
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {str(e)}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


async def main():
    """
    Main script entry point to populate places from CSV files.
    """
    # File paths and column mappings
    files = [
        # Commented out `all_parks.csv` for now
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
            "path": "all_places.csv",
            "columns": {
                "name": "name",
                "latitude": "latitude",
                "longitude": "longitude",
                "address": "address",
            },
            "type": "tourist attraction",
        },
        {
            "path": "all_restrooms.csv",
            "columns": {
                "name": "name",
                "latitude": "latitude",
                "longitude": "longitude",
                "address": "address",
            },
            "type": "restroom",
        },
    ]

    # Database session
    async with AsyncSessionFactory() as db:
        for file in files:
            await populate_places_from_file(
                db, file["path"], file["columns"], file.get("type")
            )


if __name__ == "__main__":
    asyncio.run(main())

# docker exec -it navigate_la_backend bash
# python tests/populate_places.py

# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT COUNT(*) FROM places;
# SELECT types, COUNT(*) FROM places GROUP BY types;
# SELECT * FROM places LIMIT 10;
