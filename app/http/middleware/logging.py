"""Logging Middleware"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import json
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request details (don't log sensitive information)
        # Remove query parameters that might contain sensitive data
        url = str(request.url)
        if '?' in url:
            base_url = url.split('?')[0]
            # Only log base URL, not query params
            url = base_url
        
        log_data = {
            "method": request.method,
            "url": url,  # Sanitized URL
            "status_code": response.status_code,
            "process_time": process_time,
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }
        
        # Use proper logging instead of print
        logger.info(json.dumps(log_data))
        
        return response

