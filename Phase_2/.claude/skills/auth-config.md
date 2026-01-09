# Skill: Auth Config

## Description
Configures Better Auth with JWT on frontend and backend verification.

## Usage
/auth-config <part>

## Instructions

### For `frontend`:
- Install and configure Better Auth client
- Enable JWT plugin with proper configuration
- Set up `BETTER_AUTH_SECRET` environment variable
- Configure auth routes and session management
- Add token attachment to API calls (Authorization header)
- Implement login/logout flows

### For `backend`:
- Install and configure JWT verification middleware
- Extract and validate JWT tokens from Authorization header
- Parse `user_id` from verified token payload
- Add authentication dependency to protected routes
- Handle token expiration and refresh
- Return proper 401/403 status codes

### Security checklist:
- Use HTTPS in production
- Secure cookie settings (httpOnly, sameSite, secure)
- Proper CORS configuration
- Token expiration handling

## Examples
- `/auth-config frontend`
- `/auth-config backend`