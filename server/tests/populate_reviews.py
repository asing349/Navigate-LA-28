import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from config.database import AsyncSessionFactory
from models.review import Review
from models.user import User
from models.place import Place
from comments import comments  # Import comments from the external file


async def fetch_user_ids(db: AsyncSession):
    """
    Fetch all user IDs from the users table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[int]: List of user IDs.
    """
    try:
        result = await db.execute(select(User.id))
        return [row[0] for row in result]
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error fetching user IDs: {str(e)}")


async def fetch_place_ids(db: AsyncSession):
    """
    Fetch all place IDs from the places table.

    Args:
        db (AsyncSession): Database session.

    Returns:
        List[int]: List of place IDs.
    """
    try:
        result = await db.execute(select(Place.id))
        return [row[0] for row in result]
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error fetching place IDs: {str(e)}")


def generate_review():
    """
    Generate a random review with a rating and optional comment.

    Returns:
        dict: Dictionary containing review details (rating and comment).
    """
    rating = random.randint(1, 5)  # Ratings between 1 and 5
    comment = random.choice(comments) if random.random(
    ) < 0.8 else None  # 80% chance of a comment
    return {"rating": rating, "comment": comment}


async def populate_reviews(db: AsyncSession, user_ids: list, place_ids: list):
    """
    Populate the reviews table with random reviews.

    Args:
        db (AsyncSession): Database session.
        user_ids (List[int]): List of user IDs.
        place_ids (List[int]): List of place IDs.
    """
    try:
        for user_id in user_ids:
            # Select 30 random place IDs for the user
            selected_places = random.sample(place_ids, min(30, len(place_ids)))

            for place_id in selected_places:
                review_data = generate_review()

                # Create a Review instance
                review = Review(
                    user_id=user_id,
                    place_id=place_id,
                    rating=review_data["rating"],
                    comment=review_data["comment"]
                )
                db.add(review)

        # Commit the transaction
        await db.commit()
        print("Successfully populated the reviews table.")
    except SQLAlchemyError as e:
        await db.rollback()
        raise RuntimeError(f"Error populating reviews: {str(e)}")


async def main():
    """
    Main script entry point to populate reviews table.
    """
    async with AsyncSessionFactory() as db:
        # Fetch all user IDs and place IDs
        user_ids = await fetch_user_ids(db)
        place_ids = await fetch_place_ids(db)

        if not user_ids or not place_ids:
            print("No users or places found in the database.")
            return

        # Populate reviews
        await populate_reviews(db, user_ids, place_ids)

if __name__ == "__main__":
    asyncio.run(main())

# docker exec -it navigate_la_backend bash
# python tests/populate_reviews.py

# docker exec -it navigate_la_postgres psql -U la28_user -d navigate_la28_db
# SELECT * FROM reviews LIMIT 10;
# SELECT COUNT(*) FROM reviews;