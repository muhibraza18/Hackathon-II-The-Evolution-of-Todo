# Feature Specification: Better Auth Integration for Todo AI Chatbot

**Feature Branch**: `001-auth-integration`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "Better Auth integration for user authentication and session management in Todo AI Chatbot
Target audience: Backend developers implementing authentication layer with Better Auth
Focus: User registration, login, session management, and route protection
Success criteria:
- Users can register with email/password
- Users can login and receive session tokens
- Protected routes verify user identity before processing requests
- user_id correctly extracted from session and passed to all operations
- Sessions persist across browser refreshes
- Logout invalidates sessions properly

Constraints:
- Authentication library: Better Auth (https://www.better-auth.com/)
- Backend: Python FastAPI (from Step 4)
- Database: Neon PostgreSQL (shared with tasks/conversations)
- Frontend: Integration with ChatKit UI (Step 7)
- Session storage: Database-backed (stateless server architecture)
- Password security: Bcrypt hashing minimum
- No third-party OAuth providers for Phase III (email/password only)

Technology requirements:
- Better Auth Python SDK
- FastAPI middleware for auth verification
- Database models for users and sessions
- Secure password hashing (bcrypt/argon2)
- JWT or session token mechanism

Database models needed:

**User model:**
- id (primary key, auto-increment)
- email (unique, required)
- password_hash (required)
- name (optional)
- created_at (timestamp)
- updated_at (timestamp)

**Session model:**
- id (primary key)
- user_id (foreign key to User)
- token (unique, required)
- expires_at (timestamp)
- created_at (timestamp)

Authentication endpoints:

**POST /api/auth/register**
Request:
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}

Response (success):
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "token": "session_token_here"
}

Response (error):
{
  "error": "Email already registered"
}

**POST /api/auth/login**
Request:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (success):
{
  "user_id": "user_abc123",
  "token": "session_token_here",
  "expires_at": "2026-01-15T10:30:00Z"
}

Response (error):
{
  "error": "Invalid credentials"
}

**POST /api/auth/logout**
Request headers:
Authorization: Bearer session_token_here
Response:
{
  "message": "Logged out successfully"
}

**GET /api/auth/me**
Request headers:Authorization: Bearer session_token_here
Response:
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe"
}

Protected route integration:

**Chat endpoint protection:**
- Current: POST /api/{user_id}/chat (from Step 4)
- Change to: POST /api/chat (user_id extracted from session)
- Authorization header required: `Authorization: Bearer <token>`
- Middleware extracts user_id from valid session
- Request body no longer includes user_id (security improvement)

**Modified chat request:**
{
  "conversation_id": 5,
  "message": "Add buy groceries"
}
Note: user_id automatically extracted from authenticated session

Authentication middleware requirements:
- Intercept all /api/* requests (except /api/auth/*)
- Extract Bearer token from Authorization header
- Validate token against database sessions table
- Check session expiration
- Extract user_id from valid session
- Inject user_id into request context for route handlers
- Return 401 Unauthorized for invalid/missing/expired tokens

Security requirements:
- Passwords hashed with bcrypt (minimum 10 rounds) or argon2
- Session tokens cryptographically random (UUID v4 or better)
- HTTPS enforced in production (HTTP allowed for local dev)
- Session expiration: 7 days default
- No passwords logged or returned in responses
- Rate limiting on auth endpoints (10 requests/minute per IP)
- Email validation (basic format check)
- Password minimum length: 8 characters

Error handling:
- 400 Bad Request: Invalid email format, weak password, missing fields
- 401 Unauthorized: Invalid credentials, expired session, missing token
- 409 Conflict: Email already registered
- 500 Internal Server Error: Database failures, unexpected errors

User flow:

**Registration flow:**
1. User submits email/password via frontend
2. Backend validates email format and password strength
3. Check if email already exists
4. Hash password with bcrypt
5. Create user record in database
6. Create session record with token
7. Return user_id and token to frontend
8. Frontend stores token in localStorage/cookie

**Login flow:**
1. User submits email/password
2. Backend finds user by email
3. Verify password hash matches
4. Create new session record with token
5. Return user_id and token
6. Frontend stores token

**Authenticated request flow:**
1. Frontend includes token in Authorization header
2. Middleware validates token and extracts user_id
3. Route handler receives user_id from context
4. Process request with authenticated user_id
5. Return response

**Logout flow:**
1. Frontend sends logout request with token
2. Backend deletes session record from database
3. Frontend clears stored token
4. User redirected to login

Integration with existing components:

**Step 4 backend changes:**
- Remove user_id from URL path: `/api/{user_id}/chat` → `/api/chat`
- Add auth middleware before chat route
- Extract user_id from request context (not URL parameter)
- Pass user_id to agent and MCP tools as before

**Step 5 agent changes:**
- No changes needed (still receives user_id from backend)
- user_id still passed to all MCP tool calls

**Step 3 MCP tools changes:**
- No changes needed (still receive user_id parameter)

Better Auth configuration:
```python
# In backend/app/config.py
BETTER_AUTH_CONFIG = {
    "secret": os.getenv("BETTER_AUTH_SECRET"),
    "database_url": os.getenv("DATABASE_URL"),
    "session_expiry_days": 7,
    "password_hash_rounds": 12,
    "trusted_origins": ["http://localhost:3000", "https://yourdomain.com"]
}
```
Environment variables:
- BETTER_AUTH_SECRET (cryptographic secret for token signing)
- DATABASE_URL (already defined in Step 4)
- ALLOWED_ORIGINS (CORS configuration for frontend)

Validation requirements:
- ✓ Users can register with valid email/password
- ✓ Registration rejects duplicate emails
- ✓ Login succeeds with correct credentials
- ✓ Login fails with incorrect credentials
- ✓ Protected routes reject requests without tokens
- ✓ Protected routes reject expired tokens
- ✓ Logout invalidates session tokens
- ✓ user_id correctly extracted and passed to chat endpoint
- ✓ Passwords never logged or returned in responses
- ✓ Sessions persist across server restarts (database-backed)

Not building:
- OAuth providers (Google, GitHub, etc.) - future phase
- Password reset/forgot password functionality - future phase
- Email verification - future phase
- Multi-factor authentication (MFA) - future phase
- Role-based access control (RBAC) - single role for Phase III
- Account deletion - future phase
- Password change endpoint - future phase
- Refresh tokens (using long-lived sessions for simplicity)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

A user wants to create an account with email and password to securely access the Todo AI Chatbot. The system allows them to register, validates their credentials, creates a secure session, and provides them with a session token for subsequent authenticated requests.

**Why this priority**: This is the foundational functionality that enables all other protected features of the Todo AI Chatbot, allowing users to have personalized experiences with their tasks.

**Independent Test**: Can be fully tested by sending registration requests with valid/invalid credentials and verifying that successful registrations return session tokens while invalid ones return appropriate error messages.

**Acceptance Scenarios**:

1. **Given** a user visits the Todo AI Chatbot for the first time, **When** they submit a registration request with a valid email, strong password, and name, **Then** the system creates their account, generates a session token, and returns their user ID and token.
2. **Given** a user attempts to register with an email that already exists, **When** they submit the registration request, **Then** the system returns an error indicating the email is already registered.
3. **Given** a user has registered successfully, **When** they submit a login request with correct credentials, **Then** the system validates the password, creates a new session, and returns a session token.

---

### User Story 2 - Protected Route Access (Priority: P2)

An authenticated user wants to interact with protected features of the Todo AI Chatbot, such as managing their tasks. The system verifies their session token before processing requests and provides access to personalized features.

**Why this priority**: Enables the core functionality of the Todo AI Chatbot by ensuring that users can only access their own data and that all requests are properly authenticated.

**Independent Test**: Can be tested by making authenticated requests to protected endpoints and verifying that the system correctly extracts user ID from the session and processes requests appropriately.

**Acceptance Scenarios**:

1. **Given** a user has a valid session token, **When** they make a request to a protected endpoint with proper authorization header, **Then** the system validates the token and processes the request using the associated user ID.
2. **Given** a user sends a request without an authorization token, **When** they access a protected endpoint, **Then** the system returns a 401 Unauthorized response.
3. **Given** a user has an expired session token, **When** they make a request to a protected endpoint, **Then** the system returns a 401 Unauthorized response.

---

### User Story 3 - Session Management and Logout (Priority: P3)

An authenticated user wants to securely end their session when they're done using the Todo AI Chatbot. The system allows them to invalidate their session token, ensuring that their account remains secure.

**Why this priority**: Provides important security functionality that allows users to properly terminate their sessions and prevents unauthorized access to their accounts.

**Independent Test**: Can be tested by making logout requests and verifying that subsequent requests with the same token are rejected.

**Acceptance Scenarios**:

1. **Given** a user has an active session, **When** they send a logout request with their valid token, **Then** the system invalidates the session and returns a success message.
2. **Given** a user has logged out, **When** they attempt to make requests with their previous token, **Then** the system rejects these requests with a 401 Unauthorized response.

---

### Edge Cases

- What happens when a user attempts to register with an invalid email format?
- How does system handle password validation when the password is too weak?
- What occurs when session tokens expire during a conversation?
- How does the system handle concurrent requests with the same session?
- What happens when the database is temporarily unavailable during authentication?
- How does the system respond to repeated failed login attempts (potential brute force)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email, password, and optional name
- **FR-002**: System MUST validate email format and password strength before creating accounts
- **FR-003**: System MUST hash passwords using bcrypt (minimum 10 rounds) before storing
- **FR-004**: System MUST prevent duplicate email registrations
- **FR-005**: System MUST allow users to login with their registered email and password
- **FR-006**: System MUST generate cryptographically random session tokens upon successful authentication
- **FR-007**: System MUST store sessions in the database with expiration timestamps
- **FR-008**: System MUST validate session tokens for all protected endpoints
- **FR-009**: System MUST extract user_id from valid sessions and pass to downstream operations
- **FR-010**: System MUST allow users to invalidate their sessions via logout functionality
- **FR-011**: System MUST protect the chat endpoint by requiring valid session tokens
- **FR-012**: System MUST automatically extract user_id from session instead of requiring it in URL path
- **FR-013**: System MUST enforce session expiration after 7 days of inactivity
- **FR-014**: System MUST implement rate limiting on auth endpoints (10 requests/minute per IP)
- **FR-015**: System MUST return appropriate error codes (400, 401, 409, 500) for different failure scenarios

### Key Entities

- **User**: Represents a registered user with credentials and profile information, including id, email, password_hash, name, and timestamps
- **Session**: Represents an active user session with token validation and expiration, including id, user_id reference, token, and expiration timestamp
- **Authentication Token**: Cryptographically secure identifier that verifies user identity without exposing credentials

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can register with email/password successfully with 95% success rate under normal conditions
- **SC-002**: User login succeeds with correct credentials within 2 seconds 98% of the time
- **SC-003**: Protected routes correctly authenticate users and reject unauthorized access 100% of the time
- **SC-004**: Session tokens persist across browser refreshes and remain valid for the full 7-day duration
- **SC-005**: User_id is correctly extracted from sessions and passed to all downstream operations 100% of the time
- **SC-006**: Logout functionality successfully invalidates sessions and prevents further access with the same token