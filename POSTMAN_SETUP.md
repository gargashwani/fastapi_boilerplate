# Postman Collection Setup Guide

This guide explains how to import and use the Postman collection and environment for the FastAPI Boilerplate API.

## Files Included

1. **FastAPI_Boilerplate.postman_collection.json** - Complete API collection with all endpoints
2. **FastAPI_Boilerplate.postman_environment.json** - Environment variables for local development

## Import Instructions

### Step 1: Import the Collection

1. Open Postman
2. Click **Import** button (top left)
3. Select **File** tab
4. Choose `FastAPI_Boilerplate.postman_collection.json`
5. Click **Import**

### Step 2: Import the Environment

1. Click **Import** button again
2. Select **File** tab
3. Choose `FastAPI_Boilerplate.postman_environment.json`
4. Click **Import**

### Step 3: Select the Environment

1. In the top right corner, click the environment dropdown
2. Select **FastAPI Boilerplate - Local**

## Collection Structure

The collection is organized into the following folders:

### 🔐 Authentication
- **Register User** - Create a new user account
- **Login** - Get access token (automatically saves token to environment)

### 👤 Users (Authentication Required)
- **Get Current User** - Get authenticated user info
- **Update Current User** - Update your own profile
- **Get All Users** - List all users (admin only)
- **Get User by ID** - Get specific user details
- **Delete User** - Delete a user (admin only)

### 📁 Files (Authentication Required)
- **Upload File** - Upload a file to storage
- **Download File** - Download a file
- **Get File Info** - Get file metadata
- **Delete File** - Delete a file
- **List Files** - List files in a directory
- **Copy File** - Copy a file to another location
- **Move File** - Move a file to another location

### 📡 Broadcasting (Authentication Required)
- **Authorize Channel** - Authorize private/presence channel access
- **WebSocket** - Connect via WebSocket at `/api/v1/broadcasting/ws?token={{access_token}}`

### 🏠 Root
- **API Welcome** - Get API information

## Environment Variables

The environment includes the following variables:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://localhost:8000` | API base URL |
| `access_token` | (auto-filled) | JWT access token (auto-saved after login) |
| `user_id` | (auto-filled) | Current user ID (auto-saved after login/register) |
| `user_email` | (auto-filled) | Current user email (auto-saved after login/register) |
| `test_email` | `test@example.com` | Test user email |
| `test_password` | `Test@12345` | Test user password |
| `file_path` | (auto-filled) | File path (auto-saved after upload) |
| `socket_id` | (empty) | WebSocket socket ID |

## Quick Start

1. **Start the API server** (if not already running):
   ```bash
   docker compose up
   ```

2. **Register a new user**:
   - Go to **Authentication** → **Register User**
   - Click **Send**
   - The user ID and email will be automatically saved

3. **Login**:
   - Go to **Authentication** → **Login**
   - Click **Send**
   - The access token will be automatically saved to `access_token` variable
   - All authenticated endpoints will now work automatically

4. **Test authenticated endpoints**:
   - Try **Users** → **Get Current User**
   - Try **Files** → **Upload File** (select a file first)
   - Try **Files** → **List Files**

## Auto-Save Features

The collection includes test scripts that automatically save:
- **Access token** after login
- **User ID** after login/register
- **User email** after login/register
- **File path** after file upload

## Customization

### Change Base URL

To use a different server (e.g., production):

1. Click the environment dropdown (top right)
2. Select **FastAPI Boilerplate - Local**
3. Click the eye icon to edit
4. Change `base_url` value
5. Click **Save**

### Create Additional Environments

You can create additional environments for:
- **Development**: `http://localhost:8000`
- **Staging**: `https://staging-api.example.com`
- **Production**: `https://api.example.com`

## Password Requirements

When registering users, passwords must meet these requirements:
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)

## Authentication

Most endpoints require authentication. The collection automatically includes the Bearer token in the Authorization header using the `{{access_token}}` variable.

**Public Endpoints** (no authentication required):
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /`

**All other endpoints require authentication.**

## Troubleshooting

### Token Expired
If you get a 401 Unauthorized error:
1. Go to **Authentication** → **Login**
2. Click **Send** to get a new token
3. The token will be automatically updated

### Connection Refused
- Make sure the API server is running: `docker compose up`
- Check that `base_url` is correct in the environment

### File Upload Issues
- Make sure you select a file in the **Upload File** request
- Check file size limits (default: 10MB)
- Ensure file extension is allowed

## Additional Resources

- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- ReDoc Documentation: `http://localhost:8000/redoc`
- API Welcome: `http://localhost:8000/`

## Notes

- The WebSocket endpoint (`/api/v1/broadcasting/ws`) cannot be tested directly in Postman. Use a WebSocket client or browser console.
- Some endpoints require admin privileges (`is_superuser: true`).
- File paths are automatically sanitized for security.

