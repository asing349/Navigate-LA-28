# server/scripts/populate_reviews.py

import asyncio  # For asynchronous programming
import random  # For generating random data
import logging  # For logging information and errors
# For asynchronous database sessions
from sqlalchemy.ext.asyncio import AsyncSession
# For constructing and executing SQLAlchemy queries
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError  # For handling database exceptions

# Import application-specific modules
from config.database import AsyncSessionFactory  # Database session factory
from models.review import Review  # Model for the `reviews` table
from models.user import User  # Model for the `users` table
from models.place import Place  # Model for the `places` table
from scripts.comments import comments  # Predefined list of comments for reviews

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    # Define the log message format
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)  # Create a logger for this script


async def fetch_user_ids(db: AsyncSession) -> list[int]:
    """
    Fetch all user IDs from the `users` table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        list[int]: List of user IDs.

    Raises:
        SQLAlchemyError: If there's an error fetching user IDs.
    """
    try:
        # Execute a query to fetch user IDs
        result = await db.execute(select(User.id))
        # Extract user IDs from the result
        user_ids = [row[0] for row in result]
        # Log the count of user IDs
        logger.info(f"Retrieved {len(user_ids)} user IDs")
        return user_ids
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user IDs: {e}")  # Log the error
        raise


async def fetch_place_ids(db: AsyncSession) -> list[int]:
    """
    Fetch all place IDs from the `places` table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        list[int]: List of place IDs.

    Raises:
        SQLAlchemyError: If there's an error fetching place IDs.
    """
    try:
        # Execute a query to fetch place IDs
        result = await db.execute(select(Place.id))
        # Extract place IDs from the result
        place_ids = [row[0] for row in result]
        # Log the count of place IDs
        logger.info(f"Retrieved {len(place_ids)} place IDs")
        return place_ids
    except SQLAlchemyError as e:
        logger.error(f"Error fetching place IDs: {e}")  # Log the error
        raise


def generate_review() -> dict:
    """
    Generate a random review with a rating and optional comment.

    Returns:
        dict: Dictionary containing review details (rating and comment).
    """
    rating = random.randint(1, 5)  # Generate a random rating between 1 and 5
    comment = random.choice(comments) if random.random(
    ) < 0.8 else None  # 80% chance to include a comment
    return {"rating": rating, "comment": comment}


async def populate_reviews(
    db: AsyncSession,
    user_ids: list[int],
    place_ids: list[int],
    reviews_per_user: int = 30,
) -> None:
    """
    Populate the `reviews` table with random reviews.

    Args:
        db (AsyncSession): Database session.
        user_ids (list[int]): List of user IDs.
        place_ids (list[int]): List of place IDs.
        reviews_per_user (int): Number of reviews to generate per user (default: 30).

    Workflow:
        1. Randomly select places for each user.
        2. Generate random reviews for the selected places.
        3. Add reviews to the database session and commit the transaction.

    Raises:
        SQLAlchemyError: If there's an error during review creation.
    """
    try:
        total_reviews = 0  # Initialize a counter for total reviews
        for user_id in user_ids:
            selected_places = random.sample(
                place_ids, min(reviews_per_user, len(place_ids))
            )  # Select a subset of places for the user

            # Generate reviews for the selected places
            reviews = [
                Review(user_id=user_id, place_id=place_id, **generate_review())
                for place_id in selected_places
            ]

            db.add_all(reviews)  # Add all reviews to the session
            total_reviews += len(reviews)

        await db.commit()  # Commit the transaction
        # Log the total number of reviews
        logger.info(f"Successfully created {total_reviews} reviews")
    except SQLAlchemyError as e:
        logger.error(f"Error populating reviews: {e}")  # Log the error
        await db.rollback()  # Rollback the transaction
        raise


async def main() -> None:
    """
    Main script entry point to populate the `reviews` table.

    Workflow:
        1. Fetch user and place IDs from the database.
        2. Populate the `reviews` table with random data.
    """
    try:
        async with AsyncSessionFactory() as db:
            user_ids = await fetch_user_ids(db)  # Fetch all user IDs
            place_ids = await fetch_place_ids(db)  # Fetch all place IDs

            if not user_ids or not place_ids:
                # Log an error if no data is found
                logger.error("No users or places found in the database")
                return

            await populate_reviews(db, user_ids, place_ids)  # Populate reviews
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log any unexpected errors
        raise

if __name__ == "__main__":
    """
    Script execution entry point.

    Calls the main function to populate the `reviews` table with random data.
    """
    try:
        asyncio.run(main())  # Run the script using asyncio
    except KeyboardInterrupt:
        # Log if the script is interrupted
        logger.info("Script interrupted by user")
    except Exception as e:
        # Log if the script fails unexpectedly
        logger.error(f"Script failed: {e}")
        raise

# Usage instructions:
# 1. Open a bash terminal inside the backend container:
#    docker exec -it navigate_la_backend bash
# 2. Run the script:
#    python scripts/populate_reviews.py

# Instructions for verifying the data:
# 1. Open a bash terminal inside the Postgres container:
#    docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# 2. Execute SQL queries to check the records:
#    SELECT * FROM reviews LIMIT 10;
#    SELECT COUNT(*) FROM reviews;
