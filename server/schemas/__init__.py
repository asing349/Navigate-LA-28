# server/schemas/__init__.py

# Import user-related schemas
from schemas.user import (
    User,  # Schema for retrieving user data
    UserCreate,  # Schema for creating new users
    UserBase,  # Base schema shared across user-related operations
)

# Import review-related schemas
from schemas.review import (
    Review,  # Schema for retrieving review data
    ReviewCreate,  # Schema for creating new reviews
    ReviewBase,  # Base schema shared across review-related operations
)

# Import customer usage-related schemas
from schemas.customer_usage import (
    CustomerUsage,  # Schema for retrieving customer usage data
    CustomerUsageCreate,  # Schema for creating new customer usage records
    CustomerUsageBase,  # Base schema shared across customer usage-related operations
)

# Import place-related schemas
from schemas.place import (
    Place,  # Schema for retrieving place data
    PlaceCreate,  # Schema for creating new places
    PlaceBase,  # Base schema shared across place-related operations
)
