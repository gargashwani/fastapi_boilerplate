import os
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from app.core.error_handler import global_exception_handler
from app.http.middleware import LoggingMiddleware, RateLimitMiddleware
from config import settings
from routes.api import register_api_routes

app = FastAPI(
    title=settings.APP_NAME, openapi_url="/openapi.json", debug=settings.APP_DEBUG
)


# Add global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    return await global_exception_handler(request, exc)


# Set up CORS - never allow all origins in production
cors_origins = settings.BACKEND_CORS_ORIGINS
if settings.APP_ENV == "production" and "*" in cors_origins:
    # In production, don't allow wildcard
    cors_origins = [origin for origin in cors_origins if origin != "*"]
    if not cors_origins:
        raise ValueError(
            "CORS origins must be specified in production. Cannot use '*' wildcard."
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)


# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # HSTS - only in production with HTTPS
    if settings.APP_ENV == "production" and settings.APP_URL.startswith("https://"):
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    # Content Security Policy
    # Allow Swagger UI CDN resources for /docs and /redoc endpoints
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        # More permissive CSP for API docs
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self';"
        )
    else:
        # Strict CSP for other endpoints
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        )

    # Permissions Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID for tracking."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Add custom middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI Boilerplate API",
        "version": "1.0.0",
        "docs": "/docs",
        "api_docs": "/redoc",
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

# Include API routes (Laravel-like routes/api.php)
api_router = register_api_routes()
app.include_router(api_router, prefix="/api/v1")
