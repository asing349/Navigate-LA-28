import asyncio
import random
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from config.database import AsyncSessionFactory
from models.review import Review
from models.user import User
from models.place import Place
from scripts.comments import comments

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def fetch_user_ids(db: AsyncSession) -> list[int]:
    """
    Fetch all user IDs from the users table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        list[int]: List of user IDs.

    Raises:
        SQLAlchemyError: If there's an error fetching user IDs.
    """
    try:
        result = await db.execute(select(User.id))
        user_ids = [row[0] for row in result]
        logger.info(f"Retrieved {len(user_ids)} user IDs")
        return user_ids
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user IDs: {e}")
        raise


async def fetch_place_ids(db: AsyncSession) -> list[int]:
    """
    Fetch all place IDs from the places table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        list[int]: List of place IDs.

    Raises:
        SQLAlchemyError: If there's an error fetching place IDs.
    """
    try:
        result = await db.execute(select(Place.id))
        place_ids = [row[0] for row in result]
        logger.info(f"Retrieved {len(place_ids)} place IDs")
        return place_ids
    except SQLAlchemyError as e:
        logger.error(f"Error fetching place IDs: {e}")
        raise


def generate_review() -> dict:
    """
    Generate a random review with a rating and optional comment.

    Returns:
        dict: Dictionary containing review details (rating and comment).
    """
    rating = random.randint(1, 5)
    comment = random.choice(comments) if random.random() < 0.8 else None
    return {"rating": rating, "comment": comment}


async def populate_reviews(
    db: AsyncSession,
    user_ids: list[int],
    place_ids: list[int],
    reviews_per_user: int = 30,
) -> None:
    """
    Populate the reviews table with random reviews.

    Args:
        db (AsyncSession): Database session.
        user_ids (list[int]): List of user IDs.
        place_ids (list[int]): List of place IDs.
        reviews_per_user (int): Number of reviews to generate per user.

    Raises:
        SQLAlchemyError: If there's an error during review creation.
    """
    try:
        total_reviews = 0
        for user_id in user_ids:
            selected_places = random.sample(
                place_ids, min(reviews_per_user, len(place_ids))
            )

            reviews = [
                Review(user_id=user_id, place_id=place_id, **generate_review())
                for place_id in selected_places
            ]

            db.add_all(reviews)
            total_reviews += len(reviews)

        await db.commit()
        logger.info(f"Successfully created {total_reviews} reviews")
    except SQLAlchemyError as e:
        logger.error(f"Error populating reviews: {e}")
        await db.rollback()
        raise


async def main() -> None:
    """
    Main script entry point to populate reviews table.
    """
    try:
        async with AsyncSessionFactory() as db:
            user_ids = await fetch_user_ids(db)
            place_ids = await fetch_place_ids(db)

            if not user_ids or not place_ids:
                logger.error("No users or places found in the database")
                return

            await populate_reviews(db, user_ids, place_ids)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

# Usage instructions:
# docker exec -it navigate_la_backend bash
# python scripts/populate_reviews.py

# To verify:
# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT * FROM reviews LIMIT 10;
# SELECT COUNT(*) FROM reviews;
