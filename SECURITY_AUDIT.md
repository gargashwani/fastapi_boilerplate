# Security Audit Report

This document identifies security vulnerabilities and recommendations for the FastAPI boilerplate.

## Critical Vulnerabilities

### 1. Hardcoded Default Secrets
**Location:** `app/core/config.py`
**Issue:** Default values like `"your-secret-key-here"` and `"your-jwt-secret-key-here"` are insecure.
**Risk:** If these defaults are used in production, tokens can be easily forged.
**Fix:**
```python
# Require secrets to be set, no defaults
APP_KEY: str  # Remove default
JWT_SECRET: str  # Remove default
```

### 2. Path Traversal Vulnerability in File Download
**Location:** `app/api/v1/endpoints/files.py:52-81`
**Issue:** The `file_path:path` parameter allows accessing files outside intended directories.
**Risk:** Attackers can access arbitrary files on the server (e.g., `../../../etc/passwd`).
**Fix:**
```python
import os
from pathlib import Path

def validate_file_path(file_path: str, base_dir: str) -> str:
    """Validate and sanitize file path."""
    # Resolve path and ensure it's within base directory
    resolved = Path(base_dir) / file_path
    resolved = resolved.resolve()
    base = Path(base_dir).resolve()
    
    try:
        resolved.relative_to(base)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid file path")
    
    return str(resolved)
```

### 3. Command Injection in Scheduler
**Location:** `app/core/scheduler.py:76-93`
**Issue:** The `exec()` method executes shell commands without proper sanitization.
**Risk:** If user input reaches this method, command injection is possible.
**Fix:**
```python
import shlex

def exec(self, command: str) -> 'Schedule':
    """Schedule a shell command with proper sanitization."""
    # Validate command is from whitelist or sanitize
    if not self._is_allowed_command(command):
        raise ValueError("Command not allowed")
    
    # Use shlex to properly escape command
    sanitized = shlex.quote(command)
    # Or better: use subprocess with list of args instead of shell=True
```

### 4. Unsafe Pickle Serialization in Cache
**Location:** `app/core/cache.py`
**Issue:** Using pickle for cache serialization allows arbitrary code execution if cache is compromised.
**Risk:** If an attacker can inject data into cache, they can execute arbitrary code.
**Fix:**
- Remove pickle support or make it opt-in with warning
- Use JSON by default (already default, but ensure pickle is disabled in production)
- Add validation for cached data

### 5. CORS Misconfiguration
**Location:** `app/core/middlewares.py:67-78` and `app/__init__.py:14-21`
**Issue:** Custom CORS middleware allows all origins with `"*"`, and FastAPI CORS also configured.
**Risk:** Allows any origin to make requests, potentially exposing sensitive data.
**Fix:**
- Remove custom CORS middleware (FastAPI's is sufficient)
- Ensure `BACKEND_CORS_ORIGINS` is properly configured
- Never use `"*"` in production

### 6. File Upload Security Issues
**Location:** `app/api/v1/endpoints/files.py:17-50`
**Issues:**
- No file type validation
- No file size limits
- No content validation
- Filename can contain path traversal characters
**Risk:** 
- Malicious file uploads
- DoS via large files
- Path traversal in filenames
**Fix:**
```python
import magic
from pathlib import Path

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    # Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Validate MIME type
    mime_type = magic.from_buffer(content, mime=True)
    if not mime_type.startswith(('image/', 'application/pdf')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Sanitize filename
    safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._-")
    # ... rest of code
```

### 7. Missing Security Headers
**Location:** `app/__init__.py`
**Issue:** No security headers like X-Frame-Options, X-Content-Type-Options, CSP, etc.
**Risk:** Vulnerable to clickjacking, MIME sniffing, XSS attacks.
**Fix:**
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### 8. In-Memory Rate Limiting
**Location:** `app/core/middlewares.py:36-65`
**Issue:** Rate limiting uses in-memory dictionary, won't work across multiple servers.
**Risk:** Rate limiting can be bypassed in distributed deployments.
**Fix:**
- Use Redis for distributed rate limiting
- Implement proper sliding window algorithm

### 9. Weak WebSocket Authentication
**Location:** `app/api/v1/endpoints/broadcasting.py:144-224`
**Issue:** WebSocket authentication is optional and not properly validated.
**Risk:** Unauthorized access to WebSocket channels.
**Fix:**
```python
from app.core.security import get_current_user_from_token

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    if not token:
        await websocket.close(code=1008, reason="Authentication required")
        return
    
    try:
        # Properly validate token
        user = await get_current_user_from_token(token)
        user_id = user.id
    except Exception:
        await websocket.close(code=1008, reason="Invalid token")
        return
    # ... rest of code
```

### 10. Deprecated datetime.utcnow()
**Location:** `app/core/security.py:19,21` and `app/models/user.py:18`
**Issue:** Using deprecated `datetime.utcnow()` instead of timezone-aware datetime.
**Risk:** Timezone-related bugs, potential security issues with token expiration.
**Fix:**
```python
from datetime import datetime, timezone

# Replace
expire = datetime.utcnow() + expires_delta
# With
expire = datetime.now(timezone.utc) + expires_delta
```

## Medium Severity Issues

### 11. Information Disclosure in Error Messages
**Location:** Multiple endpoints
**Issue:** Error messages may expose sensitive information (stack traces, database errors).
**Risk:** Information leakage helps attackers understand system architecture.
**Fix:**
```python
# In production, don't expose detailed errors
if settings.APP_ENV == "production":
    # Return generic error messages
    raise HTTPException(status_code=500, detail="An error occurred")
else:
    # Development: show detailed errors
    raise HTTPException(status_code=500, detail=str(e))
```

### 12. No CSRF Protection
**Issue:** No CSRF tokens for state-changing operations.
**Risk:** Cross-site request forgery attacks.
**Fix:**
- Implement CSRF token validation for POST/PUT/DELETE requests
- Use SameSite cookies
- Add CSRF middleware

### 13. No Input Validation on File Paths
**Location:** `app/api/v1/endpoints/files.py`
**Issue:** File paths from user input are used without validation.
**Risk:** Path traversal, accessing unauthorized files.
**Fix:** Implement path validation (see #2 above)

### 14. Debug Mode Enabled by Default
**Location:** `app/core/config.py:26`
**Issue:** `APP_DEBUG: bool = True` by default.
**Risk:** Exposes detailed error information in production.
**Fix:**
```python
APP_DEBUG: bool = False  # Default to False
```

### 15. Missing Request ID Tracking
**Issue:** No request ID for tracking and logging.
**Risk:** Difficult to trace security incidents.
**Fix:**
```python
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

## Low Severity Issues

### 16. No Rate Limiting on Specific Endpoints
**Issue:** Global rate limiting only, no per-endpoint limits.
**Risk:** Some endpoints (login, registration) should have stricter limits.
**Fix:** Implement endpoint-specific rate limiting

### 17. Password Strength Not Enforced
**Location:** `app/schemas/user.py`
**Issue:** No password complexity requirements.
**Risk:** Weak passwords are vulnerable to brute force.
**Fix:**
```python
import re
from pydantic import validator

@validator('password')
def validate_password(cls, v):
    if len(v) < 8:
        raise ValueError('Password must be at least 8 characters')
    if not re.search(r'[A-Z]', v):
        raise ValueError('Password must contain uppercase letter')
    if not re.search(r'[a-z]', v):
        raise ValueError('Password must contain lowercase letter')
    if not re.search(r'\d', v):
        raise ValueError('Password must contain a digit')
    return v
```

### 18. JWT Token Not Revocable
**Issue:** No token blacklist or revocation mechanism.
**Risk:** Compromised tokens remain valid until expiration.
**Fix:** Implement token blacklist using Redis

### 19. No Account Lockout
**Issue:** No protection against brute force login attempts.
**Risk:** Attackers can try unlimited password combinations.
**Fix:** Implement account lockout after N failed attempts

### 20. Missing HTTPS Enforcement
**Issue:** No enforcement of HTTPS in production.
**Risk:** Data transmitted in plaintext.
**Fix:**
```python
if settings.APP_ENV == "production":
    @app.middleware("http")
    async def enforce_https(request: Request, call_next):
        if request.url.scheme != "https":
            return Response(status_code=301, headers={"Location": request.url.replace(scheme="https")})
        return await call_next(request)
```

## Recommendations

### Immediate Actions (Critical)
1. Remove hardcoded secrets - require environment variables
2. Fix path traversal in file endpoints
3. Remove or secure command execution in scheduler
4. Disable pickle in cache (use JSON only)
5. Fix CORS configuration
6. Add file upload validation
7. Add security headers

### Short-term Actions (Medium)
1. Implement proper error handling
2. Add CSRF protection
3. Fix WebSocket authentication
4. Use timezone-aware datetime
5. Implement distributed rate limiting

### Long-term Actions (Low)
1. Add password strength requirements
2. Implement token revocation
3. Add account lockout
4. Add request ID tracking
5. Implement endpoint-specific rate limiting

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Validate all input** - Never trust user input
3. **Use parameterized queries** - SQLAlchemy does this, but be careful with raw SQL
4. **Implement defense in depth** - Multiple layers of security
5. **Regular security audits** - Review code regularly
6. **Keep dependencies updated** - Use `pip-audit` or `safety`
7. **Use HTTPS everywhere** - Especially in production
8. **Implement proper logging** - But don't log sensitive data
9. **Use security headers** - Protect against common attacks
10. **Regular penetration testing** - Test your security measures

## Tools for Security Testing

- `bandit` - Python security linter
- `safety` - Check for known vulnerabilities in dependencies
- `pip-audit` - Audit Python packages for known vulnerabilities
- `semgrep` - Static analysis for security issues
- OWASP ZAP - Dynamic security testing

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

