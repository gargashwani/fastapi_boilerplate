# Security Guide

This guide covers security best practices and features in the FastAPI boilerplate.

## Table of Contents

1. [Security Features](#security-features)
2. [Authentication & Authorization](#authentication--authorization)
3. [Input Validation](#input-validation)
4. [File Security](#file-security)
5. [Configuration Security](#configuration-security)
6. [Production Deployment](#production-deployment)
7. [Security Testing](#security-testing)

## Security Features

The boilerplate includes comprehensive security features:

### Authentication & Authorization
- JWT-based authentication with timezone-aware tokens
- Password strength requirements (8+ chars, uppercase, lowercase, digit)
- Policy and Gate-based authorization
- Secure password hashing with bcrypt

### Input Validation
- Pydantic schema validation for all requests
- File upload validation (type, size, content)
- Path traversal prevention
- Command injection prevention

### Security Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy
- Strict-Transport-Security (HSTS) in production
- Referrer-Policy
- Permissions-Policy

### Rate Limiting
- Redis-based distributed rate limiting
- In-memory fallback for single-server deployments
- Configurable limits per endpoint

### Error Handling
- Secure error messages (no information disclosure)
- Request ID tracking
- Proper logging without sensitive data

## Authentication & Authorization

### Password Requirements

Passwords must meet the following requirements:
- Minimum 8 characters
- Maximum 128 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

```python
# Example: Creating a user with password validation
from app.schemas.user import UserCreate

user_data = UserCreate(
    email="user@example.com",
    password="SecurePass123"  # Must meet requirements
)
```

### JWT Tokens

JWT tokens are timezone-aware and include:
- Expiration time
- User ID (subject)
- Secure signing with HS256

```python
from app.core.security import create_access_token

# Create token
token = create_access_token(user_id, expires_delta=timedelta(hours=1))
```

## Input Validation

### Request Validation

Always use Pydantic schemas for request validation:

```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password too short')
        return v
```

### File Upload Validation

File uploads are automatically validated:

```python
from app.api.v1.endpoints.files import upload_file

# Automatic validation includes:
# - File type (extension and MIME type)
# - File size (max 10MB)
# - Filename sanitization
# - Path traversal prevention
```

## File Security

### Path Traversal Prevention

All file operations use path validation:

```python
from app.core.file_security import validate_file_path

# Safe file path validation
safe_path = validate_file_path(user_path, base_directory)
```

### File Upload Security

File uploads are secured with:
- Type validation (extension and MIME type)
- Size limits (10MB default)
- Filename sanitization
- Content validation (magic bytes)

```python
# Allowed file types
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf', ...}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

## Configuration Security

### Environment Variables

**Critical**: Never commit `.env` files to version control.

Required secrets for production:
```env
APP_KEY=<generate-secure-32-char-key>
JWT_SECRET=<generate-secure-32-char-key>
```

Generate secure keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Production Configuration

```env
APP_ENV=production
APP_DEBUG=false
APP_URL=https://yourdomain.com

# CORS - Never use wildcard in production
BACKEND_CORS_ORIGINS=["https://yourdomain.com","https://app.yourdomain.com"]

# Cache - Use JSON only (no pickle)
CACHE_SERIALIZER=json
```

## Production Deployment

### Pre-Deployment Checklist

1. **Generate Secure Secrets**
   ```bash
   python -c "import secrets; print('APP_KEY=' + secrets.token_urlsafe(32))"
   python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))"
   ```

2. **Update Environment Variables**
   - Set `APP_ENV=production`
   - Set `APP_DEBUG=false`
   - Configure secure `APP_KEY` and `JWT_SECRET`
   - Set proper CORS origins
   - Use strong database passwords

3. **Configure HTTPS**
   - Set up SSL/TLS certificates
   - Configure reverse proxy (nginx/Apache)
   - Enable HSTS header

4. **Set Up Redis**
   - Configure Redis password
   - Set up firewall rules
   - Use for distributed rate limiting

5. **Security Headers**
   - Verify all security headers are present
   - Configure CSP for your application
   - Enable HSTS

6. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

7. **File Storage**
   - Set appropriate permissions
   - Use secure storage (S3 with encryption)
   - Validate all file operations

### Deployment Security

```bash
# 1. Generate secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. Update .env
APP_ENV=production
APP_DEBUG=false
APP_KEY=<generated-key>
JWT_SECRET=<generated-key>

# 3. Check for vulnerabilities
pip install safety
safety check

# 4. Run security linter
pip install bandit
bandit -r app/

# 5. Test application
pytest
```

## Security Testing

### Dependency Scanning

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

### Code Security Scanning

```bash
# Run Bandit security linter
pip install bandit
bandit -r app/

# Check for common issues
bandit -r app/ -f json -o security-report.json
```

### Manual Security Testing

1. **Test Path Traversal**
   ```bash
   curl http://localhost:8000/api/v1/files/download/../../../etc/passwd
   # Should return 403 Forbidden
   ```

2. **Test File Upload**
   ```bash
   # Try uploading large file (>10MB) - should fail
   # Try uploading wrong file type - should fail
   ```

3. **Test Authentication**
   ```bash
   # Try accessing protected endpoint without token - should fail
   # Try WebSocket without token - should be rejected
   ```

4. **Test Rate Limiting**
   ```bash
   # Make many requests quickly - should be rate limited
   ```

5. **Check Security Headers**
   ```bash
   curl -I http://localhost:8000/
   # Should see security headers
   ```

## Common Security Issues

### 1. Hardcoded Secrets

**Problem**: Secrets in code or default values
**Solution**: Always use environment variables

### 2. SQL Injection

**Problem**: Raw SQL queries with user input
**Solution**: Use SQLAlchemy ORM (already implemented)

### 3. XSS Attacks

**Problem**: Unescaped user input in responses
**Solution**: FastAPI automatically escapes JSON responses

### 4. CSRF Attacks

**Problem**: No CSRF protection
**Solution**: Consider implementing CSRF tokens for state-changing operations

### 5. Information Disclosure

**Problem**: Detailed error messages in production
**Solution**: Use secure error handler (already implemented)

## Security Best Practices

1. **Never trust user input** - Always validate
2. **Use parameterized queries** - SQLAlchemy does this
3. **Implement defense in depth** - Multiple security layers
4. **Keep dependencies updated** - Regular security updates
5. **Use HTTPS everywhere** - Especially in production
6. **Implement proper logging** - But don't log sensitive data
7. **Regular security audits** - Review code regularly
8. **Use security headers** - Protect against common attacks
9. **Monitor for vulnerabilities** - Use automated tools
10. **Regular penetration testing** - Test your security measures

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)
- [Security Audit Report](SECURITY_AUDIT.md)
- [Security Fixes Summary](SECURITY_FIXES.md)

