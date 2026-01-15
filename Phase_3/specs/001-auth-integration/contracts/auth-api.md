# API Contract: Authentication Endpoints for Todo AI Chatbot

## Base URL
`/api/auth`

## Authentication Registration
### `POST /register`

#### Request
**Content-Type**: `application/json`

**Body**:
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

#### Success Response (200)
**Content-Type**: `application/json`

```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Error Responses
- **400 Bad Request**: Invalid email format, weak password, missing required fields
- **409 Conflict**: Email already registered
- **500 Internal Server Error**: Database connection failure, unexpected error

## Authentication Login
### `POST /login`

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Validation**:
- `email`: Required, valid email format
- `password`: Required, minimum 8 characters

#### Success Response (200)
**Content-Type**: `application/json`

```json
{
  "user_id": "user_abc123",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-01-15T10:30:00Z"
}
```

#### Error Responses
- **400 Bad Request**: Missing email or password
- **401 Unauthorized**: Invalid credentials
- **500 Internal Server Error**: Database connection failure, unexpected error

## Authentication Logout
### `POST /logout`

#### Request
**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Success Response (200)
**Content-Type**: `application/json`

```json
{
  "message": "Logged out successfully"
}
```

#### Error Responses
- **401 Unauthorized**: Missing, invalid, or expired token
- **500 Internal Server Error**: Database connection failure, unexpected error

## Get Current User
### `GET /me`

#### Request
**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Success Response (200)
**Content-Type**: `application/json`

```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe"
}
```

#### Error Responses
- **401 Unauthorized**: Missing, invalid, or expired token
- **500 Internal Server Error**: Database connection failure, unexpected error

## Updated Chat Endpoint
### `POST /chat` (Previously `POST /api/{user_id}/chat`)

#### Request
**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Content-Type**: `application/json`

**Body**:
```json
{
  "conversation_id": 123,
  "message": "Add buy groceries"
}
```

**Validation**:
- `conversation_id`: Optional, positive integer
- `message`: Required, maximum 1000 characters

#### Success Response (200)
**Content-Type**: `application/json`

```json
{
  "conversation_id": 123,
  "response": "✓ Added 'buy groceries' to your list!",
  "tool_calls": []
}
```

#### Error Responses
- **401 Unauthorized**: Missing, invalid, or expired token
- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Backend service failure

## Rate Limiting
All authentication endpoints are subject to rate limiting:
- Maximum 10 requests per minute per IP address
- Returns 429 Too Many Requests when exceeded

## Security Headers
All responses include appropriate security headers:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy