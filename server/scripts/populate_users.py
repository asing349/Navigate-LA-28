import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

from config.database import AsyncSessionFactory
from models.user import User as UserModel

# Create a Faker instance
faker = Faker()

# Add this list of 20 countries after the faker instance
COUNTRIES = [
    "United States",
    "Canada",
    "Mexico",
    "United Kingdom",
    "France",
    "Germany",
    "Spain",
    "Italy",
    "Japan",
    "China",
    "Australia",
    "Brazil",
    "India",
    "Russia",
    "South Korea",
    "Netherlands",
    "Sweden",
    "Singapore",
    "New Zealand",
    "Ireland",
]


async def fetch_existing_usernames(db: AsyncSession):
    """
    Fetch all existing usernames from the database.

    Args:
        db (AsyncSession): Database session.

    Returns:
        set: Set of existing usernames in the database.
    """
    try:
        result = await db.execute(select(UserModel.username))
        return {row[0] for row in result}
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching existing usernames: {str(e)}")


async def create_random_users(db: AsyncSession, num_users: int = 200):
    """
    Populate the database with random user data, ensuring unique usernames.
    """
    try:
        print("Fetching existing usernames...")
        existing_usernames = await fetch_existing_usernames(db)
        print(f"Found {len(existing_usernames)} existing usernames")

        for i in range(num_users):
            if i % 100 == 0:
                print(f"Creating users {i}-{min(i+99, num_users)}/{num_users}")

            # Generate unique username
            while True:
                username = faker.unique.user_name()
                if username not in existing_usernames:
                    break

            # Generate random user data
            dob = faker.date_of_birth(minimum_age=18, maximum_age=70)
            country = faker.random_element(COUNTRIES)
            password = "password123"  # Simple password for test users
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Create a User model instance
            user = UserModel(
                username=username,
                password=hashed_password.decode("utf-8"),
                dob=dob,
                country=country,
            )
            db.add(user)

            # Add to existing usernames to prevent duplicates
            existing_usernames.add(username)

            # Commit every 100 users to avoid large transactions
            if (i + 1) % 100 == 0:
                await db.commit()
                print(f"Committed batch of 100 users")

        # Commit any remaining users
        await db.commit()
        print(f"Successfully created {num_users} users.")
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")


async def main():
    """
    Main entry point for the script.
    """
    try:
        async with AsyncSessionFactory() as db:
            print("Starting user creation process...")
            await create_random_users(db, num_users=200)
    except Exception as e:
        print(f"Main function error: {str(e)}")


# Run the script
if __name__ == "__main__":
    asyncio.run(main())


# docker exec -it navigate_la_backend bash
# python scripts/populate_users.py

# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT id, username, dob, country FROM users LIMIT 10;
