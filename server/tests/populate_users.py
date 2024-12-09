import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config.database import AsyncSessionFactory
from models.user import User as UserModel
import bcrypt

# Create a Faker instance
faker = Faker()

async def create_random_users(db: AsyncSession, num_users: int = 50):
    """
    Populate the database with random user data.

    Args:
        db (AsyncSession): Database session.
        num_users (int): Number of users to create.
    """
    try:
        for _ in range(num_users):
            # Generate random user data
            username = faker.unique.user_name()
            dob = faker.date_of_birth(minimum_age=18, maximum_age=70)
            country = faker.country()
            password = faker.password(length=10)
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Create a User model instance
            user = UserModel(
                username=username,
                password=hashed_password.decode("utf-8"),
                dob=dob,
                country=country,
            )
            db.add(user)

        # Commit the transaction
        await db.commit()
        print(f"Successfully created {num_users} users.")
    except SQLAlchemyError as e:
        # Rollback in case of an error
        await db.rollback()
        print(f"Error occurred: {str(e)}")
    finally:
        await db.close()

async def main():
    """
    Main entry point for the script.
    """
    # Create a database session
    async with AsyncSessionFactory() as db:
        await create_random_users(db, num_users=1000)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())

# docker exec -it navigate_la_backend bash
# python populate_users.py

# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT id, username, dob, country FROM users LIMIT 10;