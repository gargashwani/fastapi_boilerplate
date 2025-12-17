"""
Error Handling Utilities
Provides secure error handling that doesn't expose sensitive information.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
import logging
import traceback

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that prevents information disclosure.
    """
    # Log full error for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Return generic error in production
    if settings.APP_ENV == "production":
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An internal error occurred",
                "request_id": getattr(request.state, "request_id", None)
            }
        )
    else:
        # In development, show more details
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__,
                "traceback": traceback.format_exc() if settings.APP_DEBUG else None,
                "request_id": getattr(request.state, "request_id", None)
            }
        )

def secure_error_message(error: Exception, default_message: str = "An error occurred") -> str:
    """
    Get secure error message that doesn't expose sensitive information.
    
    Args:
        error: Exception object
        default_message: Default message to return
        
    Returns:
        Safe error message
    """
    if settings.APP_DEBUG:
        return str(error)
    else:
        # In production, return generic message
        return default_message

