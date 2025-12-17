from fastapi import APIRouter
from app.api.v1.controllers import auth, users, files, broadcasting

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(broadcasting.router, prefix="/broadcasting", tags=["broadcasting"]) 