# server/routes/__init__.py

# FastAPI's router class for grouping and managing routes
from fastapi import APIRouter

# Import routers from individual route files
# Routes related to user operations
from routes.user_routes import router as user_router
# Routes related to authentication
from routes.auth_routes import router as auth_router
from routes.review_routes import router as review_router  # Routes related to reviews
# Routes related to customer usage logs
from routes.customer_usage_routes import router as customer_usage_router
# Routes related to geographical data
from routes.geo_routes import router as geo_router
# Routes related to analytics and insights
from routes.analytics_routes import router as analytics_router

# Create a main router instance to include all other routers
api_router = APIRouter()

# Include the user routes
api_router.include_router(
    user_router,  # Router instance from user_routes
    prefix="/users",  # Prefix for all user-related endpoints
    tags=["Users"],  # Tag for categorizing user endpoints in the API docs
)

# Include the authentication routes
api_router.include_router(
    auth_router,  # Router instance from auth_routes
    prefix="/auth",  # Prefix for all authentication-related endpoints
    # Tag for categorizing authentication endpoints in the API docs
    tags=["Authentication"],
)

# Include the review routes
api_router.include_router(
    review_router,  # Router instance from review_routes
    prefix="/reviews",  # Prefix for all review-related endpoints
    tags=["Reviews"],  # Tag for categorizing review endpoints in the API docs
)

# Include the customer usage routes
api_router.include_router(
    customer_usage_router,  # Router instance from customer_usage_routes
    prefix="/customer-usage",  # Prefix for all customer usage-related endpoints
    # Tag for categorizing customer usage endpoints in the API docs
    tags=["Customer Usage"],
)

# Include the geographical routes
api_router.include_router(
    geo_router,  # Router instance from geo_routes
    prefix="/geo",  # Prefix for all geographical data-related endpoints
    tags=["Geo"],  # Tag for categorizing geo endpoints in the API docs
)

# Include the analytics routes
api_router.include_router(
    analytics_router,  # Router instance from analytics_routes
    prefix="/analytics",  # Prefix for all analytics-related endpoints
    # Tag for categorizing analytics endpoints in the API docs
    tags=["Analytics"],
)
