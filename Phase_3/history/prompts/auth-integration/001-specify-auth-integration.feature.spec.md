---
id: 001
title: "Specify Auth Integration"
stage: "spec"
date: "2026-01-14"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "auth-integration"
branch: "001-auth-integration"
user: "MuhibRaza"
command: "sp.specify"
labels: ["auth", "authentication", "better-auth", "session-management", "security", "registration", "login"]
links:
  spec: "specs/001-auth-integration/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-auth-integration/spec.md"
  - "specs/001-auth-integration/checklists/requirements.md"
tests:
  - "Specification completeness"
  - "Requirements validation"
  - "User scenarios coverage"
---

## Prompt

Better Auth integration for user authentication and session management in Todo AI Chatbot
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
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```
Response (success):
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "token": "session_token_here"
}
```
Response (error):
```json
{
  "error": "Email already registered"
}
```

**POST /api/auth/login**
Request:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
Response (success):
```json
{
  "user_id": "user_abc123",
  "token": "session_token_here",
  "expires_at": "2026-01-15T10:30:00Z"
}
```
Response (error):
```json
{
  "error": "Invalid credentials"
}
```

**POST /api/auth/logout**
Request headers:
Authorization: Bearer session_token_here
Response:
```json
{
  "message": "Logged out successfully"
}
```

**GET /api/auth/me**
Request headers:Authorization: Bearer session_token_here
Response:
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe"
}
```

Protected route integration:

**Chat endpoint protection:**
- Current: POST /api/{user_id}/chat (from Step 4)
- Change to: POST /api/chat (user_id extracted from session)
- Authorization header required: `Authorization: Bearer <token>`
- Middleware extracts user_id from valid session
- Request body no longer includes user_id (security improvement)

**Modified chat request:**
```json
{
  "conversation_id": 5,
  "message": "Add buy groceries"
}
``Note: user_id automatically extracted from authenticated session

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
- Refresh tokens (using long-lived sessions for simplicity)

## Response snapshot

Created a comprehensive specification for the Better Auth integration feature for the Todo AI Chatbot, defining:

- User Story 1 (P1): User Registration and Authentication - enabling users to create accounts and securely access the Todo AI Chatbot
- User Story 2 (P2): Protected Route Access - ensuring that users can only access their own data and that all requests are properly authenticated
- User Story 3 (P3): Session Management and Logout - providing important security functionality that allows users to properly terminate their sessions

The specification includes 15 functional requirements covering registration, login, session management, token validation, and security aspects. It defines 6 measurable success criteria focused on registration success rates, login performance, authentication accuracy, and session persistence. The spec also captures important edge cases around validation, rate limiting, and error handling.

## Outcome

- ✅ Impact: Complete specification for Better Auth integration with clear user stories and requirements
- 🧪 Tests: All requirements validated with testable acceptance scenarios
- 📁 Files: Created spec and requirements checklist in proper directory structure
- 🔁 Next prompts: Ready for planning phase (`/sp.plan`)
- 🧠 Reflection: Specification provides clear roadmap for implementing secure authentication