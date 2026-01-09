# Implementation Plan: Authentication with Better Auth + JWT Integration

**Branch**: `003-auth-jwt-integration` | **Date**: 2026-01-08 | **Spec**: ../003-auth-jwt-integration/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement authentication with Better Auth for user management and JWT-based API protection with user-scoped task access. The solution will provide secure user registration/login, JWT token issuance and verification, and enforce user isolation through database-level filtering. This follows the constitutional requirements for Phase II Step 4 authentication implementation with Better Auth + JWT.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**: Better Auth, FastAPI, Next.js 16+, SQLModel, PyJWT
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/Vitest (frontend - future)
**Target Platform**: Web application (Next.js frontend + FastAPI backend)
**Project Type**: Web (frontend/backend architecture)
**Performance Goals**: <200ms auth operations, sub-millisecond JWT verification
**Constraints**: All API endpoints must require valid JWT tokens except health checks, user data must be isolated by user_id
**Scale/Scope**: Individual user accounts with secure authentication and authorization

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Authentication Phase Security Standards (Principle XIV): Will use Better Auth exclusively with JWT tokens and proper secret management
- ✅ JWT Token Management (Principle XV): Will implement JWT with HS256 algorithm and proper token structure
- ✅ User Isolation and Data Privacy (Principle XVI): Will filter all task queries by authenticated user_id from JWT payload
- ✅ API-First Development Pattern: Will implement backend authentication before frontend integration
- ✅ Incremental Testing Protocol: Will verify each layer independently before integration
- ✅ Success Criteria Definition: Will meet all specified success criteria (SC-001 through SC-007)

## Project Structure

### Documentation (this feature)

```text
specs/003-auth-jwt-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel models
├── db.py                # Database connection setup
├── auth.py              # Authentication middleware and dependencies
├── routers/
│   ├── tasks.py         # Task endpoints (to be updated with auth)
│   └── auth.py          # Auth endpoints (future)
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables

frontend/
├── app/
│   ├── login/page.tsx       # Login page
│   ├── signup/page.tsx      # Signup page
│   ├── logout/page.tsx      # Logout page (or route handler)
│   └── page.tsx             # Protected tasks page
├── components/
│   └── ProtectedRoute.tsx   # Protected route wrapper
├── lib/
│   ├── api.ts               # API client (to be updated with JWT)
│   └── auth.ts              # Authentication utilities
├── contexts/
│   └── AuthContext.tsx      # Authentication state management
├── next.config.js           # Next.js configuration (for Better Auth)
├── package.json             # Node.js dependencies
└── .env.local               # Frontend environment variables
```

**Structure Decision**: Selected Option 2: Web application structure with separate backend and frontend directories. This follows the constitutional requirement for Next.js frontend with FastAPI backend and allows for proper separation of concerns while maintaining the ability to implement the required authentication flow.

## Architecture Design

### Better Auth Architecture
- Frontend: Better Auth configured in Next.js app with JWT plugin
- Token issuance: Better Auth generates JWT on successful login/signup
- Token storage: httpOnly cookies for enhanced security (prevents XSS attacks)
- API requests: JWT automatically attached to requests via cookie

### JWT Token Flow
1. User registers/logs in via Better Auth endpoints
2. Better Auth generates JWT with user_id, email, exp, iat claims
3. JWT stored in httpOnly cookie by frontend
4. API requests automatically include JWT via cookie
5. Backend verifies JWT signature and extracts user_id
6. User-specific operations use extracted user_id for data isolation

### Backend Middleware Architecture
- JWT verification middleware using PyJWT
- FastAPI dependency injection (Depends(get_current_user))
- Extract user_id from JWT payload for database queries
- Return 401 for invalid/missing/expired tokens

### User Isolation Enforcement
- All task queries filtered by user_id from authenticated user
- Prevent cross-user data access through database-level filtering
- Return 404 for tasks not owned by authenticated user (don't leak existence)

## Decisions Made

1. **JWT Token Storage Strategy**: httpOnly cookies (more secure, prevents XSS)
2. **Better Auth Database Adapter**: Better Auth manages users table automatically (simpler)
3. **JWT Verification Library (Backend)**: PyJWT (lightweight, sufficient for our needs)
4. **Protected Route Strategy (Frontend)**: Wrapper component (ProtectedRoute) (reusable)
5. **User ID Source in Backend**: Extract from JWT token only (more secure)
6. **API URL Structure**: Change to /api/tasks, user_id implicit from JWT (simpler URLs)
7. **Existing Tasks Migration**: Create test user and reassign tasks (preserves data for testing)
8. **Auth Error Handling**: Specific error messages (helps debugging)
9. **Password Requirements**: Moderate (8+ characters, no complexity) (balances security and UX)
10. **Frontend Auth State Management**: React Context API (sufficient without adding dependencies)

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Cross-stack coordination | Authentication spans both frontend and backend | Would create security gaps if only one side implemented |
| Multiple dependency updates | Better Auth requires updates to both frontend and backend | Would create inconsistent authentication flow |