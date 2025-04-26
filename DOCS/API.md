# API Documentation

## Authentication

### Register a new user
```http
POST /api/v1/auth/register
```

Request body:
```json
{
    "email": "user@example.com",
    "password": "string",
    "full_name": "string",
    "is_superuser": false
}
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

### Login
```http
POST /api/v1/auth/login
```

Request body (form data):
```
username: user@example.com
password: string
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

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
```json
{
    "detail": "Incorrect email or password",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
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