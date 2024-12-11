# server/scripts/populate_users.py

import asyncio  # For asynchronous programming
from faker import Faker  # For generating random user data
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
# For constructing and executing SQLAlchemy queries
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError  # For handling database exceptions
import bcrypt  # For hashing passwords

# Import application-specific modules
from config.database import AsyncSessionFactory  # Database session factory
from models.user import User as UserModel  # Model for the `users` table

# Create a Faker instance for generating fake data
faker = Faker()

# List of countries for assigning random user locations
COUNTRIES = [
    "United States", "Canada", "Mexico", "United Kingdom", "France", "Germany",
    "Spain", "Italy", "Japan", "China", "Australia", "Brazil", "India", "Russia",
    "South Korea", "Netherlands", "Sweden", "Singapore", "New Zealand", "Ireland",
]


async def fetch_existing_usernames(db: AsyncSession):
    """
    Fetch all existing usernames from the database.

    Args:
        db (AsyncSession): Database session.

    Returns:
        set: Set of existing usernames in the database.

    Raises:
        Exception: If an error occurs during database query execution.
    """
    try:
        # Query the database for existing usernames
        result = await db.execute(select(UserModel.username))
        # Return usernames as a set for fast lookup
        return {row[0] for row in result}
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching existing usernames: {str(e)}")


async def create_random_users(db: AsyncSession, num_users: int = 200):
    """
    Populate the database with random user data, ensuring unique usernames.

    Args:
        db (AsyncSession): Database session.
        num_users (int): Number of users to create (default: 200).

    Workflow:
        1. Fetch existing usernames from the database.
        2. Generate random user data with unique usernames.
        3. Hash passwords before saving.
        4. Insert user data into the database in batches to improve performance.

    Raises:
        SQLAlchemyError: If an error occurs during database transactions.
    """
    try:
        print("Fetching existing usernames...")
        # Fetch usernames already in the database to avoid duplicates
        existing_usernames = await fetch_existing_usernames(db)
        print(f"Found {len(existing_usernames)} existing usernames")

        for i in range(num_users):
            if i % 100 == 0:
                print(f"Creating users {i}-{min(i+99, num_users)}/{num_users}")

            # Generate a unique username
            while True:
                username = faker.unique.user_name()
                if username not in existing_usernames:
                    break

            # Generate random user details
            dob = faker.date_of_birth(
                minimum_age=18, maximum_age=70)  # Random date of birth
            # Random country from the list
            country = faker.random_element(COUNTRIES)
            password = "password123"  # Default password for testing
            hashed_password = bcrypt.hashpw(password.encode(
                "utf-8"), bcrypt.gensalt())  # Hash the password

            # Create a new user instance
            user = UserModel(
                username=username,
                password=hashed_password.decode("utf-8"),
                dob=dob,
                country=country,
            )
            db.add(user)  # Add the user instance to the session

            # Add the username to the existing usernames set to prevent duplicates
            existing_usernames.add(username)

            # Commit every 100 users to improve performance and avoid large transactions
            if (i + 1) % 100 == 0:
                await db.commit()
                print(f"Committed batch of 100 users")

        # Commit any remaining users that were not part of the last batch
        await db.commit()
        print(f"Successfully created {num_users} users.")
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback the transaction in case of errors
        print(f"Error occurred: {str(e)}")


async def main():
    """
    Main entry point for the script.

    Workflow:
        1. Open a database session.
        2. Call the function to populate the `users` table with random data.
    """
    try:
        async with AsyncSessionFactory() as db:
            print("Starting user creation process...")
            await create_random_users(db, num_users=200)  # Create 200 users
    except Exception as e:
        print(f"Main function error: {str(e)}")

# Run the script
if __name__ == "__main__":
    """
    Script execution entry point.

    Calls the main function to populate the `users` table with random data.
    """
    asyncio.run(main())

# Usage instructions:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python scripts/populate_users.py

# Instructions for verifying the data:
# 1. Open a bash terminal inside the Postgres container:
#    docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# 2. Execute SQL queries to check the records:
#    SELECT id, username, dob, country FROM users LIMIT 10;
