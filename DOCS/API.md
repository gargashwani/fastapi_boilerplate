# API Documentation

## 🔐 Authentication Overview

**All API endpoints require authentication EXCEPT:**
- `POST /api/v1/auth/register` - Public (for user registration)
- `POST /api/v1/auth/login` - Public (for user login)

**All other endpoints require the `Authorization` header:**
```
Authorization: Bearer <access_token>
```

**Protected Endpoint Groups:**
- ✅ `/api/v1/users/*` - All user management endpoints
- ✅ `/api/v1/files/*` - All file operations
- ✅ `/api/v1/broadcasting/*` - All broadcasting endpoints (including WebSocket)

## Authentication

### Register a new user
```http
POST /api/v1/auth/register
```

Request body:
```json
{
    "email": "user@example.com",
    "password": "Test@12345",
    "full_name": "string",
    "is_superuser": false
}
```

**Note:** Password requirements:
- Minimum 8 characters
- Maximum 512 characters (bcrypt limitation handled automatically)
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

Response:
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "string",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-12-18T07:40:47.076834",
    "updated_at": "2025-12-18T07:40:47.076838"
}
```

**Note:** After registration, use the `/api/v1/auth/login` endpoint to get an authorization token.

### Login
```http
POST /api/v1/auth/login
```

Request body (form data):
```
username: user@example.com
password: Test@12345
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "string",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2025-12-18T07:40:47.076834",
        "updated_at": "2025-12-18T07:40:47.076838"
    }
}
```

**Note:** The login response includes both the authorization token and complete user information for immediate use in your application.

## Authentication Required

**⚠️ IMPORTANT: All API endpoints except `/api/v1/auth/login` and `/api/v1/auth/register` require authentication.**

To authenticate, include the `Authorization` header in your requests:

```
Authorization: Bearer <access_token>
```

Where `<access_token>` is the token received from the login endpoint.

**Example:**
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Unauthenticated requests will return:**
```json
{
  "detail": "Not authenticated"
}
```

**Protected Endpoints:**
- ✅ All `/api/v1/users/*` endpoints
- ✅ All `/api/v1/files/*` endpoints  
- ✅ All `/api/v1/broadcasting/*` endpoints (including WebSocket)

**Public Endpoints:**
- ❌ `/api/v1/auth/login` - Public (no authentication)
- ❌ `/api/v1/auth/register` - Public (no authentication)

## Users

### Get current user
```http
GET /api/v1/users/me
```

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```json
{
    "email": "user@example.com",
    "full_name": "string",
    "is_active": true,
    "is_superuser": false,
    "id": 1,
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```

### Update current user
```http
PUT /api/v1/users/me
```

Headers:
```
Authorization: Bearer <access_token>
```

Request body:
```json
{
    "email": "newemail@example.com",
    "full_name": "New Name",
    "password": "newpassword"
}
```

Response:
```json
{
    "email": "newemail@example.com",
    "full_name": "New Name",
    "is_active": true,
    "is_superuser": false,
    "id": 1,
    "created_at": "2024-03-19T00:00:00",
    "updated_at": "2024-03-19T00:00:00"
}
```

### Get all users
```http
GET /api/v1/users?skip=0&limit=100
```

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```json
[
    {
        "email": "user1@example.com",
        "full_name": "User One",
        "is_active": true,
        "is_superuser": false,
        "id": 1,
        "created_at": "2024-03-19T00:00:00",
        "updated_at": "2024-03-19T00:00:00"
    },
    {
        "email": "user2@example.com",
        "full_name": "User Two",
        "is_active": true,
        "is_superuser": false,
        "id": 2,
        "created_at": "2024-03-19T00:00:00",
        "updated_at": "2024-03-19T00:00:00"
    }
]
```

## Error Responses

### 400 Bad Request
```json
{
    "detail": "The user with this email already exists in the system."
}
```

### 401 Unauthorized

**Missing or Invalid Token:**
```json
{
    "detail": "Not authenticated"
}
```

**Invalid Credentials (Login):**
```json
{
    "detail": "Incorrect email or password",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

**Invalid Token:**
```json
{
    "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
    "detail": "User not found"
}
``` 