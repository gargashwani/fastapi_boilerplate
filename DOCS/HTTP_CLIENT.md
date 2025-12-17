# HTTP Client Guide

This guide explains how to use the Laravel-like HTTP client for making HTTP requests in this FastAPI boilerplate.

## Table of Contents

1. [Introduction](#introduction)
2. [Making Requests](#making-requests)
3. [Request Data](#request-data)
4. [Headers](#headers)
5. [Authentication](#authentication)
6. [Timeout](#timeout)
7. [Retries](#retries)
8. [Error Handling](#error-handling)
9. [Middleware](#middleware)
10. [Client Options](#client-options)
11. [Concurrent Requests](#concurrent-requests)
12. [Request Pooling](#request-pooling)
13. [Request Batching](#request-batching)
14. [Macros](#macros)
15. [Testing](#testing)

## Introduction

The HTTP client provides a fluent, Laravel-like interface for making HTTP requests. It's built on top of `httpx` and supports both synchronous and asynchronous requests.

### Key Features

- **Fluent API**: Chain methods for easy configuration
- **Authentication**: Basic auth, Bearer tokens
- **Retry Logic**: Automatic retries on failure
- **Middleware**: Custom request/response processing
- **Concurrent Requests**: Pool and batch multiple requests
- **Testing Support**: Fake responses and request recording
- **Error Handling**: Built-in error handling helpers

## Making Requests

### Basic GET Request

```python
from app.core.http import http

# Simple GET request
response = http().get('https://api.example.com/users')
data = response.json()
```

### POST Request

```python
# POST with JSON data
response = http().post('https://api.example.com/posts', json={
    'title': 'My Post',
    'content': 'Post content'
})

if response.successful():
    print(response.json())
```

### PUT and PATCH Requests

```python
# PUT request
response = http().put('https://api.example.com/posts/1', json={
    'title': 'Updated Title'
})

# PATCH request
response = http().patch('https://api.example.com/posts/1', json={
    'title': 'Patched Title'
})
```

### DELETE Request

```python
response = http().delete('https://api.example.com/posts/1')
if response.ok():
    print("Post deleted")
```

## Request Data

### JSON Data

```python
response = http().post('https://api.example.com/posts', json={
    'title': 'My Post',
    'content': 'Content here'
})
```

### Form Data

```python
response = http().post('https://api.example.com/posts', data={
    'title': 'My Post',
    'content': 'Content here'
})
```

### Query Parameters

```python
response = http().get('https://api.example.com/posts', params={
    'page': 1,
    'per_page': 10
})
```

### Files

```python
with open('image.jpg', 'rb') as f:
    response = http().post('https://api.example.com/upload', files={
        'file': ('image.jpg', f, 'image/jpeg')
    })
```

## Headers

### Setting Headers

```python
# Single header
response = http().with_header('X-Custom-Header', 'value').get('https://api.example.com')

# Multiple headers
response = http().with_headers({
    'X-Custom-Header': 'value',
    'X-Another-Header': 'another-value'
}).get('https://api.example.com')
```

### Default Headers

```python
# Set headers that apply to all requests
http_instance = http().with_headers({
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json'
})

response = http_instance.get('https://api.example.com/users')
```

## Authentication

### Bearer Token

```python
response = http().with_token('your-token-here').get('https://api.example.com/users')
```

### Basic Authentication

```python
response = http().with_basic_auth('username', 'password').get('https://api.example.com/users')
```

### Custom Authentication Header

```python
response = http().with_header('Authorization', 'Custom token-here').get('https://api.example.com')
```

## Timeout

### Setting Timeout

```python
# 5 second timeout
response = http().timeout(5.0).get('https://api.example.com/users')

# 30 second timeout
response = http().timeout(30.0).post('https://api.example.com/posts', json=data)
```

## Retries

### Automatic Retries

```python
# Retry 3 times on failure
response = http().retry(3).get('https://api.example.com/users')

# Retry on specific status codes
response = http().retry(3, retry_on=[500, 502, 503, 504]).get('https://api.example.com/users')
```

### Retry Logic

By default, retries occur on:
- Network errors
- HTTP 500, 502, 503, 504 status codes

## Error Handling

### Check Response Status

```python
response = http().get('https://api.example.com/users')

if response.successful():
    data = response.json()
elif response.client_error():
    print(f"Client error: {response.status()}")
elif response.server_error():
    print(f"Server error: {response.status()}")
```

### Throw on Error

```python
try:
    response = http().get('https://api.example.com/users').throw()
    data = response.json()
except Exception as e:
    print(f"Request failed: {e}")
```

### Error Callback

```python
response = http().get('https://api.example.com/users').on_error(
    lambda r: print(f"Error: {r.status_code}")
)
```

### Response Helpers

```python
response = http().get('https://api.example.com/users')

# Check status
response.ok()           # True if 200
response.successful()  # True if 2xx
response.failed()       # True if 4xx or 5xx
response.client_error() # True if 4xx
response.server_error() # True if 5xx

# Get data
data = response.json()  # Parse JSON
text = response.text()  # Get text
body = response.body()  # Get raw bytes

# Get headers
headers = response.headers()
header = response.header('Content-Type')
```

## Middleware

### Creating Middleware

```python
def logging_middleware(request):
    """Log all requests."""
    print(f"Making request: {request.method} {request.url}")
    return request

def auth_middleware(request):
    """Add authentication header."""
    request.headers['Authorization'] = 'Bearer token'
    return request

# Use middleware
response = http().with_middleware(logging_middleware).get('https://api.example.com')
```

### Multiple Middleware

```python
response = http()\
    .with_middleware(logging_middleware)\
    .with_middleware(auth_middleware)\
    .get('https://api.example.com')
```

## Client Options

### SSL Verification

```python
# Disable SSL verification (not recommended for production)
response = http().without_verifying().get('https://api.example.com')
```

### Redirects

```python
# Don't follow redirects
response = http().without_redirecting().get('https://api.example.com')
```

### Custom Options

```python
response = http().with_options(
    verify=False,
    follow_redirects=False,
    timeout=30.0
).get('https://api.example.com')
```

## Concurrent Requests

### Async Requests

```python
import asyncio

async def fetch_users():
    response = await http().async_get('https://api.example.com/users')
    return response.json()

async def fetch_posts():
    response = await http().async_get('https://api.example.com/posts')
    return response.json()

# Run concurrently
async def main():
    users, posts = await asyncio.gather(
        fetch_users(),
        fetch_posts()
    )
    return users, posts
```

## Request Pooling

### Connection Pool

```python
# Execute multiple requests concurrently
requests = [
    lambda: http().get('https://api.example.com/users'),
    lambda: http().get('https://api.example.com/posts'),
    lambda: http().get('https://api.example.com/comments'),
]

responses = http().pool(requests)
for response in responses:
    print(response.json())
```

### Async Pool

```python
async def fetch_data():
    requests = [
        lambda: http().async_get('https://api.example.com/users'),
        lambda: http().async_get('https://api.example.com/posts'),
    ]
    
    responses = await http().async_pool(requests)
    return [r.json() for r in responses]
```

## Request Batching

### Batch Requests

```python
requests = [
    {'method': 'GET', 'url': 'https://api.example.com/users'},
    {'method': 'GET', 'url': 'https://api.example.com/posts'},
    {'method': 'POST', 'url': 'https://api.example.com/posts', 'json': {'title': 'New Post'}},
]

responses = http().batch(requests)
for response in responses:
    print(response.json())
```

### Async Batch

```python
async def batch_requests():
    requests = [
        {'method': 'GET', 'url': 'https://api.example.com/users'},
        {'method': 'GET', 'url': 'https://api.example.com/posts'},
    ]
    
    responses = await http().async_batch(requests)
    return [r.json() for r in responses]
```

## Macros

### Defining Macros

```python
from app.core.http import macro

def github_api():
    """GitHub API macro."""
    return http().base_url('https://api.github.com').with_header('Accept', 'application/vnd.github.v3+json')

macro('github', github_api)

# Use macro
response = http().github().get('/users/octocat')
```

### Using Macros

```python
# After defining macro
response = http().github().with_token('token').get('/user')
```

## Testing

### Faking Responses

```python
# Fake responses for testing
http().fake([
    {
        'url': 'https://api.example.com/users',
        'method': 'GET',
        'status': 200,
        'json': {'id': 1, 'name': 'John'}
    },
    {
        'url': 'https://api.example.com/posts',
        'method': 'GET',
        'status': 200,
        'json': [{'id': 1, 'title': 'Post 1'}]
    }
])

# Now requests return fake responses
response = http().get('https://api.example.com/users')
assert response.json() == {'id': 1, 'name': 'John'}
```

### Recording Requests

```python
# Record all requests
http().record()

response = http().get('https://api.example.com/users')
response = http().post('https://api.example.com/posts', json={'title': 'Test'})

# Get recorded requests
recorded = http().recorded()
assert len(recorded) == 2
```

### Inspecting Requests

```python
http().record()

http().get('https://api.example.com/users')

# Check if request was sent
assert http().assert_sent()

# Check with callback
assert http().assert_sent(
    lambda req: req.url == 'https://api.example.com/users'
)
```

### Preventing Stray Requests

```python
# Prevent unexpected requests during testing
http().prevent_stray_requests()

# Only faked requests are allowed
http().fake([
    {'url': 'https://api.example.com/users', 'method': 'GET', 'status': 200}
])

# This will work
response = http().get('https://api.example.com/users')

# This will raise exception
# response = http().get('https://api.example.com/other')  # Exception!
```

## Base URL

### Setting Base URL

```python
# Set base URL for all requests
api = http().base_url('https://api.example.com')

# Now use relative URLs
response = api.get('/users')
response = api.post('/posts', json={'title': 'New Post'})
```

## Context Manager

### Using Context Manager

```python
# Automatic cleanup
with http().base_url('https://api.example.com') as client:
    response = client.get('/users')
    data = response.json()
```

### Async Context Manager

```python
async with http().base_url('https://api.example.com') as client:
    response = await client.async_get('/users')
    data = response.json()
```

## Examples

### Example 1: API Client

```python
class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.client = http().base_url(base_url).with_token(token)
    
    def get_users(self):
        return self.client.get('/users').json()
    
    def create_user(self, data: dict):
        return self.client.post('/users', json=data).json()
    
    def update_user(self, user_id: int, data: dict):
        return self.client.put(f'/users/{user_id}', json=data).json()
    
    def delete_user(self, user_id: int):
        return self.client.delete(f'/users/{user_id}').ok()

# Usage
client = ApiClient('https://api.example.com', 'token')
users = client.get_users()
```

### Example 2: Retry with Exponential Backoff

```python
import time
import random

def retry_middleware(request):
    """Custom retry with exponential backoff."""
    # Implementation would go here
    return request

response = http()\
    .retry(3)\
    .with_middleware(retry_middleware)\
    .get('https://api.example.com/users')
```

### Example 3: Batch Processing

```python
# Fetch multiple resources concurrently
user_ids = [1, 2, 3, 4, 5]

requests = [
    {'method': 'GET', 'url': f'https://api.example.com/users/{uid}'}
    for uid in user_ids
]

responses = http().batch(requests)
users = [r.json() for r in responses if r.successful()]
```

### Example 4: Testing

```python
def test_user_api():
    # Fake API responses
    http().fake([
        {
            'url': 'https://api.example.com/users',
            'method': 'GET',
            'status': 200,
            'json': [{'id': 1, 'name': 'John'}]
        },
        {
            'url': 'https://api.example.com/users',
            'method': 'POST',
            'status': 201,
            'json': {'id': 2, 'name': 'Jane'}
        }
    ])
    
    # Test GET
    response = http().get('https://api.example.com/users')
    assert response.successful()
    assert len(response.json()) == 1
    
    # Test POST
    response = http().post('https://api.example.com/users', json={'name': 'Jane'})
    assert response.status() == 201
```

## Best Practices

1. **Use Base URLs**: Set base URL for API clients
2. **Handle Errors**: Always check response status
3. **Use Retries**: Enable retries for unreliable APIs
4. **Set Timeouts**: Always set appropriate timeouts
5. **Use Async**: Use async methods for concurrent requests
6. **Test with Fakes**: Use fake responses in tests
7. **Record Requests**: Use recording to verify API calls in tests

## Additional Resources

- [httpx Documentation](https://www.python-httpx.org/)
- [Laravel HTTP Client](https://laravel.com/docs/http-client)

