from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.middlewares import LoggingMiddleware, RateLimitMiddleware
import os

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url="/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI Boilerplate API",
        "version": "1.0.0",
        "docs": "/docs",
        "api_docs": "/redoc"
    }

# Mount static files (public directory)
# Similar to Laravel's public directory
public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
if os.path.exists(public_dir):
    app.mount("/public", StaticFiles(directory=public_dir), name="public")

# Mount storage files for public access
# Files in public/storage will be accessible via /storage/ URL
storage_public_dir = os.path.join(public_dir, "storage")
if os.path.exists(storage_public_dir):
    app.mount("/storage", StaticFiles(directory=storage_public_dir), name="storage")

# Include API router
app.include_router(api_router, prefix="/api/v1") 