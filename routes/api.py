"""
API Routes
Define API routes here, similar to Laravel's routes/api.php
"""
from fastapi import APIRouter
from app.api.v1.controllers import auth, users, files, broadcasting

def register_api_routes() -> APIRouter:
    """
    Register all API routes.
    Similar to Laravel's routes/api.php
    Returns the API router with all routes included.
    """
    api_router = APIRouter()
    
    # Authentication routes
    api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
    
    # User routes
    api_router.include_router(users.router, prefix="/users", tags=["users"])
    
    # File routes
    api_router.include_router(files.router, prefix="/files", tags=["files"])
    
    # Broadcasting routes
    api_router.include_router(broadcasting.router, prefix="/broadcasting", tags=["broadcasting"])
    
    return api_router

