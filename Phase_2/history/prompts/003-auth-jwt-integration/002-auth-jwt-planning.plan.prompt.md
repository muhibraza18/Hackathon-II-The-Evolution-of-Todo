---
id: 002
title: auth-jwt-planning
stage: plan
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-auth-jwt-integration
branch: 003-auth-jwt-integration
user: Claude Sonnet 4.5
command: /sp.plan
labels: ["authentication", "jwt", "better-auth", "planning", "architecture"]
links:
  spec: ../specs/003-auth-jwt-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/003-auth-jwt-integration/plan.md
 - ../specs/003-auth-jwt-integration/research.md
 - ../specs/003-auth-jwt-integration/data-model.md
 - ../specs/003-auth-jwt-integration/quickstart.md
 - ../specs/003-auth-jwt-integration/contracts/api-contracts.md
tests:
 - ../specs/003-auth-jwt-integration/contracts/api-contracts.md
---

## Prompt

Create:
- Better Auth architecture diagram (frontend config → JWT issuance → token storage → API requests)
- JWT token flow diagram (signup/login → token generation → frontend storage → API attachment → backend verification)
- Database schema updates (users table structure, tasks.user_id foreign key verification)
- Frontend auth flow (signup page → login page → protected routes → logout)
- Backend middleware architecture (JWT extraction → signature verification → user_id extraction → dependency injection)
- API security layer (which endpoints require auth, error handling strategy)
- Token lifecycle management (issuance, storage, expiry, renewal strategy)
- User isolation enforcement pattern (query filtering by authenticated user_id)
- Testing matrix (auth scenarios × API endpoints × expected outcomes)

Decisions needing documentation:

1. **JWT Token Storage Strategy**:
   - Option A: httpOnly cookie (more secure, prevents XSS) ✅ CHOSEN
   - Option B: localStorage (simpler, works with API-only backends)
   - Option C: sessionStorage (clears on tab close)
   - Tradeoff: httpOnly cookies are more secure but require cookie handling in API client

2. **Better Auth Database Adapter**:
   - Option A: Better Auth manages users table automatically ✅ CHOSEN
   - Option B: Custom user management with Better Auth for auth only
   - Tradeoff: Automatic management is simpler but less customizable

3. **JWT Verification Library (Backend)**:
   - Option A: python-jose (more features, heavier)
   - Option B: PyJWT ✅ CHOSEN (lightweight, sufficient for our needs)
   - Tradeoff: PyJWT is simpler and faster for basic JWT operations

4. **Protected Route Strategy (Frontend)**:
   - Option A: Wrapper component (ProtectedRoute) ✅ CHOSEN
   - Option B: Middleware in Next.js App Router
   - Option C: Manual checks in each page
   - Tradeoff: Wrapper is reusable but adds component nesting

5. **User ID Source in Backend**:
   - Option A: Extract from path parameter (/api/{user_id}/tasks)
   - Option B: Extract from JWT token only ✅ CHOSEN
   - Option C: Hybrid (verify path matches token)
   - Tradeoff: JWT-only is more secure (user can't spoof user_id in URL)

6. **API URL Structure Change**:
   - Option A: Keep /api/{user_id}/tasks, validate user_id matches JWT
   - Option B: Change to /api/tasks, user_id implicit from JWT ✅ CHOSEN
   - Tradeoff: Simpler URLs, enforces security at middleware level

7. **Existing Tasks Migration**:
   - Option A: Delete all tasks with user_id = "test-user-1"
   - Option B: Create test user and reassign tasks ✅ CHOSEN
   - Tradeoff: Reassigning preserves data for testing

8. **Auth Error Handling**:
   - Option A: Generic "Unauthorized" message
   - Option B: Specific error messages (expired, invalid, missing) ✅ CHOSEN
   - Tradeoff: Specific messages help debugging but might leak info

9. **Password Requirements**:
   - Option A: Minimal (6+ characters)
   - Option B: Moderate (8+ characters, no complexity) ✅ CHOSEN
   - Tradeoff: Moderate balances security and user experience

10. **Frontend Auth State Management**:
    - Option A: React Context API ✅ CHOSEN
    - Option B: Zustand/Redux
    - Option C: Local component state only
    - Tradeoff: Context is sufficient for auth without adding dependencies

Testing strategy:

**Authentication Flow Tests**:
- Test 1: Signup with valid email/password creates user in database
- Test 2: Signup with duplicate email returns error
- Test 3: Signup with invalid email format returns validation error
- Test 4: Signup with weak password returns validation error
- Test 5: Login with correct credentials returns JWT token
- Test 6: Login with incorrect password returns 401
- Test 7: Login with non-existent email returns 401
- Test 8: JWT token stored in cookie/localStorage after login
- Test 9: Logout clears stored JWT token
- Test 10: Logout redirects to /login page

**Frontend Protection Tests**:
- Test 11: Accessing / without auth redirects to /login
- Test 12: Accessing / with valid token shows tasks page
- Test 13: Page refresh maintains authenticated state
- Test 14: Expired token triggers re-login
- Test 15: Invalid token clears auth state and redirects

**Backend JWT Verification Tests**:
- Test 16: GET /api/tasks without token returns 401
- Test 17: GET /api/tasks with valid token returns 200
- Test 18: GET /api/tasks with invalid signature returns 401
- Test 19: GET /api/tasks with expired token returns 401
- Test 20: POST /api/tasks with valid token creates task with authenticated user_id

**User Isolation Tests**:
- Test 21: User A creates task → User B cannot see it
- Test 22: User A cannot update User B's task (returns 404)
- Test 23: User A cannot delete User B's task (returns 404)
- Test 24: User A's task list only contains their own tasks
- Test 25: Direct API call with User A's token + User B's task ID returns 404

**Integration Tests**:
- Test 26: Full flow: Signup → Login → Create task → Logout → Login → See task
- Test 27: Two users: User A creates tasks → User B creates tasks → both see only own
- Test 28: Token in Authorization header correctly extracted by backend
- Test 29: CORS allows frontend origin, rejects others
- Test 30: Database foreign key constraint enforced (tasks.user_id → users.id)

Technical details:
- Use **auth-first approach**: Setup auth before protecting routes
- Follow **security-by-default**: All routes protected unless explicitly public
- Organize by phases:
  1. Specs Update (features, api, database, ui specs)
  2. Frontend Setup (Better Auth install + config)
  3. Frontend UI (signup/login pages + forms)
  4. Frontend Context (AuthProvider + useAuth hook)
  5. Frontend Protection (ProtectedRoute wrapper)
  6. Frontend API Update (JWT attachment + 401 handling)
  7. Backend Setup (PyJWT install + auth.py)
  8. Backend Middleware (get_current_user dependency)
  9. Backend Routes (add auth to all endpoints)  10. CORS Config (allow frontend + Authorization header)
  11. Environment (BETTER_AUTH_SECRET in both services)
  12. Migration (users table + orphaned tasks cleanup)
  13. Integration Testing (end-to-end auth flows)
  14. Security Validation (verify protection works)
  15. Documentation (README + CLAUDE.md updates)

Dependencies and order:
- Specs → Frontend auth config → Auth pages → Protected routes
- Specs → Backend JWT library → Middleware → Route protection
- Both frontend and backend ready → Integration testing
- BETTER_AUTH_SECRET must be same in both services

File priorities:
Priority 1: Specs (features/authentication.md, api/rest-endpoints.md updates)
Priority 2: Environment (.env files with BETTER_AUTH_SECRET)
Priority 3: Frontend auth core (lib/auth.ts, contexts/AuthContext.tsx)
Priority 4: Frontend auth UI (signup/login pages, ProtectedRoute)
Priority 5: Frontend API (update lib/api.ts with JWT)
Priority 6: Backend auth (auth.py with JWT verification)
Priority 7: Backend routes (add get_current_user dependency)
Priority 8: CORS + testing + docs

Implementation patterns:
- Better Auth: JWT plugin with 7-day expiry
- Backend: FastAPI Depends(get_current_user) for all protected routes
- Frontend: AuthContext provides user state + login/logout methods
- API client: Auto-attach Authorization: Bearer <token> header
- User isolation: Filter all queries by authenticated user_id from JWT

Risk mitigation:
- BETTER_AUTH_SECRET mismatch → Document clearly + test early
- CORS blocks → Configure before integration testing
- Token not persisting → Test storage early
- Orphaned tasks → Decide migration strategy upfront

## Response snapshot

Successfully completed the planning phase for authentication with Better Auth + JWT Integration. Created comprehensive documentation including:

1. Implementation Plan (plan.md): Architecture overview, technical context, and project structure
2. Research (research.md): Technical research on Better Auth, JWT, cross-stack integration, security, and testing
3. Data Model (data-model.md): Updated entity relationships, database schema changes, JWT structure, and migration strategy
4. Quickstart Guide (quickstart.md): Step-by-step implementation guide with code examples for frontend and backend
5. API Contracts (contracts/api-contracts.md): Detailed API specifications for authentication and protected endpoints

Key decisions documented:
- JWT token storage using httpOnly cookies for security
- Better Auth managing users table automatically
- PyJWT for backend token verification
- React Context API for frontend auth state management
- User ID extraction from JWT token only for security
- All endpoints protected by default with proper error handling

The plan includes detailed technical specifications, implementation patterns, security requirements, and testing strategies to guide the development process.

## Outcome

- ✅ Impact: Completed comprehensive planning with detailed technical specifications for authentication implementation
- 🧪 Tests: Created detailed testing matrix with 30+ test scenarios across auth flows, frontend protection, backend verification, user isolation, and integration
- 📁 Files: Created 5 comprehensive documentation files covering all aspects of the authentication implementation
- 🔁 Next prompts: Ready to proceed with task generation using /sp.tasks
- 🧠 Reflection: Plan addresses all constitutional requirements for Phase II Step 4 authentication implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate implementation tasks using /sp.tasks based on the completed plan