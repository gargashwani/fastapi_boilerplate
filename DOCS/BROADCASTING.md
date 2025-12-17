# Broadcasting Guide

This guide explains how to use the Laravel-like broadcasting system for real-time events in this FastAPI boilerplate.

## Table of Contents

1. [Introduction](#introduction)
2. [Server Side Installation](#server-side-installation)
3. [Configuration](#configuration)
4. [Defining Broadcast Events](#defining-broadcast-events)
5. [Authorizing Channels](#authorizing-channels)
6. [Broadcasting Events](#broadcasting-events)
7. [Client Side Installation](#client-side-installation)
8. [Receiving Broadcasts](#receiving-broadcasts)
9. [Examples](#examples)

## Introduction

The broadcasting system allows you to broadcast server-side events to connected clients in real-time using WebSockets. It's similar to Laravel's broadcasting system and supports multiple drivers.

### Key Features

- **Real-time Broadcasting**: WebSocket-based real-time communication
- **Multiple Drivers**: Redis, Pusher, Ably, Log, Null
- **Channel Types**: Public, Private, Presence channels
- **Channel Authorization**: Secure access control for private/presence channels
- **Event Broadcasting**: Broadcast model events and custom events
- **Laravel-like API**: Familiar broadcasting syntax

## Server Side Installation

### Dependencies

The required packages are already included in `requirements.txt`:

- `redis[hiredis]` - For Redis pub/sub broadcasting
- `python-socketio` - WebSocket support
- `websockets` - WebSocket protocol support

### Configuration

Configure broadcasting in your `.env` file:

```env
# Broadcasting Configuration
BROADCAST_DRIVER=redis  # Options: redis, pusher, ably, log, null
BROADCAST_CONNECTION=default
```

## Configuration

### Broadcasting Drivers

**Redis (Default):**
```env
BROADCAST_DRIVER=redis
# Uses Redis pub/sub for broadcasting
```

**Pusher Channels:**
```env
BROADCAST_DRIVER=pusher
PUSHER_APP_ID=your-app-id
PUSHER_APP_KEY=your-app-key
PUSHER_APP_SECRET=your-app-secret
PUSHER_APP_CLUSTER=mt1
```

**Ably:**
```env
BROADCAST_DRIVER=ably
ABLY_KEY=your-ably-key
```

**Log (Development):**
```env
BROADCAST_DRIVER=log
# Logs broadcasts instead of sending them
```

**Null (Testing):**
```env
BROADCAST_DRIVER=null
# No-op driver for testing
```

## Defining Broadcast Events

### Creating Broadcast Events

Create event classes that implement `ShouldBroadcast`:

```python
from app.events.base import ShouldBroadcast
from typing import Dict, Any

class OrderShipped(ShouldBroadcast):
    """Event broadcast when an order is shipped."""
    
    def __init__(self, order):
        self.order = order
    
    def broadcast_on(self) -> str:
        """Channel to broadcast on."""
        return f"private-order.{self.order.id}"
    
    def broadcast_as(self) -> str:
        """Event name."""
        return "OrderShipped"
    
    def broadcast_with(self) -> Dict[str, Any]:
        """Data to broadcast."""
        return {
            "order_id": self.order.id,
            "status": "shipped",
            "tracking_number": self.order.tracking_number,
        }
```

### Broadcast Name

By default, the event name is the class name. Override `broadcast_as()` to customize:

```python
def broadcast_as(self) -> str:
    return "order.shipped"  # Custom event name
```

### Broadcast Data

Override `broadcast_with()` to customize the data:

```python
def broadcast_with(self) -> Dict[str, Any]:
    return {
        "order": {
            "id": self.order.id,
            "total": str(self.order.total),
        }
    }
```

### Broadcast Queue

Queue broadcasts for async processing:

```python
def broadcast_queue(self) -> Optional[str]:
    return "broadcasts"  # Queue name
```

### Broadcast Conditions

Broadcast only when conditions are met:

```python
class OrderShipped(ShouldBroadcast):
    def should_broadcast(self) -> bool:
        """Only broadcast if order is actually shipped."""
        return self.order.status == "shipped"
```

## Authorizing Channels

### Defining Authorization Callbacks

Define channel authorization in `app/routes/channels.py`:

```python
from app.core.channels import channel
from app.models.user import User

def register_channels():
    """Register channel authorization callbacks."""
    
    # Private user channel - only user can access their own channel
    channel().channel('private-user.{id}', lambda user, id: user.id == id)
    
    # Private order channel - user can access if they own the order
    channel().channel('private-order.{id}', lambda user, id: user_owns_order(user, id))
    
    # Presence channel - all authenticated users can join
    channel().channel('presence-users', lambda user: True)
```

### Channel Classes

For complex authorization logic, use channel classes:

```python
from app.core.channels import channel

class OrderChannel:
    """Channel authorization for orders."""
    
    @staticmethod
    def join(user: User, order_id: int) -> bool:
        """User can join if they own the order or are admin."""
        from app.models.order import Order
        order = Order.get(db, id=order_id)
        return order and (order.user_id == user.id or user.is_superuser)

def register_channels():
    channel().channel('private-order.{id}', OrderChannel.join)
```

## Broadcasting Events

### Broadcasting from Code

```python
from app.core.broadcasting import broadcast
from app.events.user_events import UserCreated

# Broadcast an event
user = User.create(db, obj_in=user_data)
event = UserCreated(user)
broadcast().event(event)
```

### Broadcasting to Specific Channels

```python
# Broadcast to public channel
broadcast().channel('orders').broadcast('OrderCreated', {'order_id': 123})

# Broadcast to private channel
broadcast().private('user.123').broadcast('UserUpdated', {'user_id': 123})

# Broadcast to presence channel
broadcast().presence('chat.room1').broadcast('MessageSent', {'message': 'Hello'})
```

### Broadcasting to Others Only

Exclude the current user from receiving the broadcast:

```python
# In your endpoint
event = UserUpdated(current_user)
broadcast().to_others().event(event)
```

### Customizing the Connection

Use a different broadcasting driver:

```python
broadcast().driver('pusher').channel('orders').broadcast('OrderCreated', data)
```

## Client Side Installation

### JavaScript Client

Install a WebSocket client library:

```bash
npm install laravel-echo pusher-js
# or
npm install socket.io-client
```

### Connecting to WebSocket

```javascript
// Using native WebSocket
const socket = new WebSocket('ws://localhost:8000/api/v1/broadcasting/ws?token=YOUR_TOKEN');

socket.onopen = () => {
    console.log('Connected');
    
    // Subscribe to channel
    socket.send(JSON.stringify({
        event: 'subscribe',
        channel: 'users'
    }));
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    if (data.event === 'UserCreated') {
        console.log('New user:', data.data);
    }
};
```

### Using Laravel Echo (Compatible)

```javascript
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: 'your-app-key',
    cluster: 'mt1',
    encrypted: true,
    wsHost: 'localhost',
    wsPort: 8000,
    wssPort: 8000,
    authEndpoint: 'http://localhost:8000/api/v1/broadcasting/auth',
    auth: {
        headers: {
            Authorization: 'Bearer ' + token
        }
    }
});
```

## Receiving Broadcasts

### Listening for Events

```javascript
// Listen to public channel
Echo.channel('users')
    .listen('UserCreated', (e) => {
        console.log('User created:', e);
    });

// Listen to private channel
Echo.private('user.123')
    .listen('UserUpdated', (e) => {
        console.log('User updated:', e);
    });

// Listen to presence channel
Echo.join('presence-users')
    .here((users) => {
        console.log('Users here:', users);
    })
    .joining((user) => {
        console.log('User joined:', user);
    })
    .leaving((user) => {
        console.log('User left:', user);
    });
```

### Leaving a Channel

```javascript
// Leave a channel
Echo.leave('users');

// Leave private channel
Echo.leaveChannel('private-user.123');
```

### Namespaces

Use namespaces to organize events:

```python
class OrderShipped(ShouldBroadcast):
    def broadcast_as(self) -> str:
        return "App\\Events\\OrderShipped"  # Namespaced event name
```

## Examples

### Example 1: Broadcasting User Events

```python
from app.events.user_events import UserCreated, UserUpdated
from app.core.broadcasting import broadcast

# When user is created
user = User.create(db, obj_in=user_data)
broadcast().event(UserCreated(user))

# When user is updated
user = User.update(db, db_obj=user, obj_in=user_data)
broadcast().event(UserUpdated(user))
```

### Example 2: Broadcasting Order Events

```python
from app.events.base import ShouldBroadcast

class OrderShipped(ShouldBroadcast):
    def __init__(self, order):
        self.order = order
    
    def broadcast_on(self) -> str:
        return f"private-order.{self.order.id}"
    
    def broadcast_as(self) -> str:
        return "OrderShipped"
    
    def broadcast_with(self) -> Dict[str, Any]:
        return {
            "order_id": self.order.id,
            "status": "shipped",
        }

# Broadcast when order is shipped
order.status = "shipped"
db.commit()
broadcast().event(OrderShipped(order))
```

### Example 3: Presence Channel

```python
class UserJoined(ShouldBroadcast):
    def __init__(self, user):
        self.user = user
    
    def broadcast_on(self) -> str:
        return "presence-chat.room1"
    
    def broadcast_as(self) -> str:
        return "UserJoined"
    
    def broadcast_with(self) -> Dict[str, Any]:
        return {
            "user": {
                "id": self.user.id,
                "name": self.user.full_name,
            }
        }
```

### Example 4: Model Broadcasting

Automatically broadcast when models are created/updated/deleted:

```python
from app.events.base import ShouldBroadcast
from app.models.user import User

class User(ShouldBroadcast):
    # Model implementation...
    
    def broadcast_on(self) -> str:
        return "users"
    
    def broadcast_as(self) -> str:
        return "UserCreated"  # or UserUpdated, UserDeleted
    
    def broadcast_with(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
        }
```

## Best Practices

1. **Use Private Channels**: For user-specific data, use private channels
2. **Authorize Properly**: Always implement proper channel authorization
3. **Queue Heavy Broadcasts**: Use queues for broadcasts that might be slow
4. **Handle Errors**: Always handle WebSocket connection errors
5. **Reconnect Logic**: Implement reconnection logic on client side
6. **Rate Limiting**: Consider rate limiting for client events

## Troubleshooting

### WebSocket Connection Failed

1. Check if WebSocket endpoint is accessible
2. Verify authentication token
3. Check CORS settings
4. Verify Redis is running (for Redis driver)

### Channel Authorization Failed

1. Check channel authorization callback
2. Verify user authentication
3. Check channel name format

### Events Not Received

1. Verify event is being broadcast
2. Check if client is subscribed to correct channel
3. Verify broadcasting driver is configured correctly
4. Check Redis pub/sub connection

## Additional Resources

- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
- [Laravel Broadcasting](https://laravel.com/docs/broadcasting)

