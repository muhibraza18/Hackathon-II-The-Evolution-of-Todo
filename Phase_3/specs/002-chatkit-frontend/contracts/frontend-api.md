# Frontend API Contract: OpenAI ChatKit Frontend for Todo AI Chatbot

## Authentication API Integration

### Registration Request
**Method**: POST
**Endpoint**: `/api/auth/register`
**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}
```

**Validation**:
- `email`: Required, valid email format, maximum 255 characters
- `password`: Required, minimum 8 characters, must include uppercase, lowercase, number, and special character
- `name`: Optional, maximum 100 characters

**Success Response (200)**:
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:
- **400 Bad Request**: Invalid email format, weak password, missing required fields
- **409 Conflict**: Email already registered
- **500 Internal Server Error**: Database connection failure, unexpected error

### Login Request
**Method**: POST
**Endpoint**: `/api/auth/login`
**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Validation**:
- `email`: Required, valid email format
- `password`: Required, minimum 8 characters

**Success Response (200)**:
```json
{
  "user_id": "user_abc123",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-01-15T10:30:00Z"
}
```

**Error Responses**:
- **400 Bad Request**: Missing email or password
- **401 Unauthorized**: Invalid credentials
- **500 Internal Server Error**: Database connection failure, unexpected error

### Logout Request
**Method**: POST
**Endpoint**: `/api/auth/logout`
**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses**:
- **401 Unauthorized**: Missing, invalid, or expired token
- **500 Internal Server Error**: Database connection failure, unexpected error

### Get Current User Request
**Method**: GET
**Endpoint**: `/api/auth/me`
**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200)**:
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Error Responses**:
- **401 Unauthorized**: Missing, invalid, or expired token
- **500 Internal Server Error**: Database connection failure, unexpected error

## Chat API Integration

### Send Chat Message
**Method**: POST
**Endpoint**: `/api/chat`
**Headers**:
```
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**:
```json
{
  "message": "Add buy groceries",
  "conversation_id": 123
}
```

**Validation**:
- `message`: Required, maximum 1000 characters
- `conversation_id`: Optional, positive integer

**Success Response (200)**:
```json
{
  "conversation_id": 123,
  "response": "✓ Added 'buy groceries' to your list!",
  "tool_calls": []
}
```

**Error Responses**:
- **401 Unauthorized**: Missing, invalid, or expired token
- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Backend service failure

## Frontend State Management

### Local Storage Keys
- `auth_token`: Stores authentication token (string)
- `user_id`: Stores user identifier (string)
- `conversation_id`: Stores current conversation identifier (string, optional)

### Event Handling

#### Authentication Events
- `AUTH_LOGIN_SUCCESS`: Triggered when login succeeds
- `AUTH_LOGIN_ERROR`: Triggered when login fails
- `AUTH_REGISTER_SUCCESS`: Triggered when registration succeeds
- `AUTH_LOGOUT`: Triggered when user logs out

#### Chat Events
- `CHAT_MESSAGE_SEND`: Triggered when user sends message
- `CHAT_MESSAGE_RECEIVED`: Triggered when assistant responds
- `CHAT_ERROR`: Triggered when chat operation fails

## Error Handling Contract

### Error Response Format
All error responses follow this format:
```json
{
  "error": "Descriptive error message",
  "status_code": 401,
  "timestamp": "2026-01-14T10:30:00Z"
}
```

### Expected Error Scenarios
- Network connectivity issues
- API timeout errors
- Invalid authentication tokens
- Server-side processing errors
- Malformed request data

## Security Requirements
- All authentication tokens must be stored securely
- All API requests must include valid authentication tokens
- Sensitive data must not be logged
- Input validation must be performed before API calls
- Cross-site scripting (XSS) prevention for message display