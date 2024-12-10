# server/routes/__init__.py
from fastapi import APIRouter

# Import routers from individual route files
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from routes.review_routes import router as review_router
from routes.customer_usage_routes import router as customer_usage_router
from routes.geo_routes import router as geo_router

# Create a main router that includes all the other routers
api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(review_router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(
    customer_usage_router, prefix="/customer-usage", tags=["Customer Usage"]
)
api_router.include_router(geo_router, prefix="/geo", tags=["Geo"])
api_router.include_router(
    customer_usage_router, prefix="/customer-usage", tags=["Customer Usage"]
)
