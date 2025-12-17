from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import json
from typing import Callable
from app.core.config import settings

class LoggingMiddleware(BaseHTTPMiddleware):
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
        import logging
        logger = logging.getLogger(__name__)
        logger.info(json.dumps(log_data))
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware.
    NOTE: This uses in-memory storage and won't work across multiple servers.
    For production, use Redis-based rate limiting.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.rate_limit = settings.RATE_LIMIT
        self.rate_limit_window = settings.RATE_LIMIT_WINDOW
        self.requests = {}
        
        # Try to use Redis for distributed rate limiting if available
        try:
            from redis import Redis
            from app.core.config import settings
            self.redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            # Test connection
            self.redis.ping()
            self.use_redis = True
        except Exception:
            self.redis = None
            self.use_redis = False
            if settings.APP_ENV == "production":
                import logging
                logger = logging.getLogger(__name__)
                logger.warning("Rate limiting using in-memory storage. For production, configure Redis.")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Use Redis if available for distributed rate limiting
        if self.use_redis and self.redis:
            try:
                key = f"rate_limit:{client_ip}"
                count = self.redis.incr(key)
                if count == 1:
                    self.redis.expire(key, self.rate_limit_window)
                
                if count > self.rate_limit:
                    return Response(
                        content=json.dumps({"detail": "Too many requests"}),
                        status_code=429,
                        media_type="application/json"
                    )
            except Exception:
                # Fallback to in-memory if Redis fails
                pass
        
        # In-memory rate limiting (fallback or if Redis not available)
        self.requests = {
            ip: [t for t in times if current_time - t < self.rate_limit_window]
            for ip, times in self.requests.items()
        }
        
        # Check rate limit
        if client_ip in self.requests:
            if len(self.requests[client_ip]) >= self.rate_limit:
                return Response(
                    content=json.dumps({"detail": "Too many requests"}),
                    status_code=429,
                    media_type="application/json"
                )
            self.requests[client_ip].append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        return await call_next(request)

# Removed custom CORS middleware - using FastAPI's built-in CORSMiddleware instead
# This prevents duplicate CORS headers and misconfiguration 