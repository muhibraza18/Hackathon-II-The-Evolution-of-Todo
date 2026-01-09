<!--
Sync Impact Report
Version change: 1.2.0 → 1.3.0
Modified principles:
 - None
Added principles:
 - XIV. Authentication Phase Security Standards
 - XV. JWT Token Management
 - XVI. User Isolation and Data Privacy
Added sections:
 - Phase II Step 4: Authentication Implementation with Better Auth + JWT
Removed sections:
 - None
Templates requiring updates:
 - ⚠ .specify/templates/plan-template.md — No change required (existing principles remain valid)
 - ⚠ .specify/templates/spec-template.md — No change required (remains aligned)
 - ⚠ .specify/templates/tasks-template.md — No change required (remains aligned)
Follow-up TODOs:
 - None
-->

# Hackathon Phase 2 Constitution

## Core Principles

### I. Spec-Driven Foundation
Every deliverable begins as a Spec-Kit Plus artifact. Features MUST be introduced through specs located under `/specs` (referenced as `@specs/...` in documentation), followed by plans and task lists before any implementation occurs. Specs MUST remain the source of truth for requirements, constraints, and measurable outcomes.

### II. Monorepo Integrity
The repository MUST remain a single workspace that houses `/specs` (with `features/`, `api/`, `database/`, `ui/`), `/frontend`, `/backend`, and `/.spec-kit/config.yaml`. All tooling, CI, and developer workflows operate from the monorepo root so Claude Code can navigate and edit any surface without context switching.

### III. Layered Guidance
CLAUDE.md files provide non-overlapping guidance: the root file defines global workflow, `/frontend/CLAUDE.md` documents Next.js conventions, and `/backend/CLAUDE.md` covers FastAPI patterns. Each CLAUDE file MUST reference relevant specs via `@specs/...` links and stay synchronized when principles change.

### IV. Automation-First Scaffolding
All scaffolding, code generation, and structural updates are executed through Claude Code commands or approved scripts. Manual coding for setup is prohibited. When new directories, configs, or boilerplate are required, invoke the appropriate `/sp.*` command or Spec-Kit script so changes stay reproducible and reviewable.

### V. Stack Alignment
The frontend is standardized on Next.js 16+ (App Router, TypeScript, Tailwind CSS). The backend is FastAPI with SQLModel, ready for future Better Auth integration. Specs under `@specs/database/schema.md` MUST describe at minimum the Better Auth-managed `users` table and a `tasks` table with a `user_id` foreign key. Optional `docker-compose.yml` files orchestrate both services but cannot diverge from this stack.

### VI. Blueprint-Only Delivery
Phase 2 work establishes foundation only. No feature logic, CRUD flows, auth wiring, or external database connections may be implemented yet. Deliverables are limited to scaffolding, specs, and configuration that prove `npm run dev` (frontend) and `uvicorn backend.main:app --reload` (backend) succeed locally.

## Structural Standards
- `/specs/features`, `/specs/api`, `/specs/database`, and `/specs/ui` each include `overview.md`, `architecture.md`, and `database/schema.md` (where applicable), referencing other documents with `@specs/...` links for traceability.
- `/.spec-kit/config.yaml` defines the project name, version, enforced directory structure, and phases (`phase1-console`, `phase2-web` minimum). Updates to structure or phases must first appear in this config.
- `/frontend` contains a Next.js App Router project with TypeScript, Tailwind, linting, and the basic run script `npm run dev`. `/backend` contains FastAPI entry points (`main.py`, `models.py`, `db.py`) and a corresponding CLAUDE guide.
- Optional orchestration artifacts (e.g., `docker-compose.yml`) must only start approved services and expose environment variables needed for local parity.

## Delivery Workflow
1. Capture new requests via spec files under `@specs/features/.../spec.md`, ensuring user stories are independently testable.
2. Run `/sp.plan` to produce architecture, data, and contract artifacts that explicitly reference the constitution gates.
3. Use `/sp.tasks` to generate dependency-ordered tasks grouped by user story; all tasks cite exact file paths within `/frontend` or `/backend`.
4. Scaffold or update code exclusively through Claude Code-driven automation, verifying `npm run dev` and `uvicorn backend.main:app --reload` before handing off.
5. Record Prompt History Records (PHRs) for every user prompt, and suggest ADRs when architectural decisions impact stack, schemas, or tooling.

## Governance
- This constitution supersedes other guidance; deviations require explicit approval recorded via `/sp.constitution` and an associated PHR.
- Amendments require: (a) documented rationale in the pull request, (b) synced updates to affected templates, and (c) semantic version bump per change impact.
- Compliance reviews occur at every `/sp.plan` Constitution Check gate and during code review. Violations block merges until resolved or waived with written justification.
- Versioning follows MAJOR.MINOR.PATCH semantics; MAJOR for principle removals or incompatible governance changes, MINOR for new principles/sections, PATCH for clarifications.

## Phase II Step 2: Task CRUD Implementation

### VII. API-First Development Pattern
All features MUST follow the API-first approach: backend endpoints are fully implemented and tested before any frontend integration begins. This ensures:
- Backend contracts are stable before frontend work starts
- API responses are validated independently
- Frontend can rely on known data structures and error codes

### VIII. Unauthenticated Development Stage
During Step 2, authentication is explicitly excluded to focus on core CRUD functionality:
- All API endpoints use hardcoded `user_id = "test-user-1"`
- No JWT tokens or Bearer auth headers in requests
- All users see the same tasks (shared global state)
- Database schema MUST include `user_id` field for future auth integration
- Frontend works without login/signup pages

### IX. Simplified Feature Scope
Step 2 implements basic task management only:
- Create, Read, Update, Delete, and Toggle completion
- No advanced features (priority, due dates, categories, search)
- No user isolation or filtering
- No authentication flows
- Error handling focuses on basic HTTP status codes (200, 201, 404, 500)

### X. Incremental Testing Protocol
Each layer must be verified independently before proceeding:
1. Database layer: Verify SQLModel queries work
2. API layer: Test endpoints with curl/Postman
3. Integration layer: Test API client (`/frontend/lib/api.ts`)
4. Frontend layer: Verify UI components render correctly
5. End-to-end: Manual testing of full CRUD workflow

### XI. API Client Centralization
All backend communication MUST flow through `/frontend/lib/api.ts`:
- Single source of truth for API endpoints
- Centralized error handling and type definitions
- No direct fetch calls in components
- Consistent request/response formatting

### XI. API Client Centralization
All backend communication MUST flow through `/frontend/lib/api.ts`:
- Single source of truth for API endpoints
- Centralized error handling and type definitions
- No direct fetch calls in components
- Consistent request/response formatting

### XII. Success Criteria Definition
Step 2 implementation is successful only when ALL criteria are met:
- Backend API endpoints return proper JSON responses
- Frontend can create, read, update, delete, and toggle tasks
- Tasks persist in Neon PostgreSQL database
- All CRUD operations work end-to-end (frontend → API → database)
- Responsive UI with loading states and error handling
- API returns appropriate HTTP status codes (200, 201, 404, 500)
- Database queries use SQLModel ORM (no raw SQL)
- Frontend uses React Server Components where possible
- Manual testing passes: Create task → View in list → Edit → Mark complete → Delete

### XIII. Implementation Sequencing
Step 2 MUST follow this exact order:
1. Update all specs with detailed requirements
   - `specs/features/task-crud.md` (user stories, acceptance criteria, test cases)
   - `specs/api/rest-endpoints.md` (request/response formats, error codes)
   - `specs/database/schema.md` (verify tasks table structure)
   - `specs/ui/components.md` (task list, task form, task item components)
   - `specs/ui/pages.md` (main tasks page layout and behavior)
2. Backend: Create Task model in models.py
3. Backend: Implement all 6 API endpoints in routes/tasks.py
4. Backend: Test endpoints with curl/Postman
5. Frontend: Create API client lib/api.ts
6. Frontend: Build TaskList, TaskForm, TaskItem components
7. Frontend: Create main tasks page
8. Integration test: Full CRUD workflow

### Exclusions (Not Building in Step 2)
The following are explicitly deferred to later steps:
- User authentication (Step 4)
- JWT token verification (Step 5)
- User signup/signin pages (Step 4)
- User-specific task filtering (Step 5)
- Advanced features (priority, due dates, categories)
- Search or advanced filtering

## Phase II Step 4: Authentication Implementation with Better Auth + JWT

### XIV. Authentication Phase Security Standards
All authentication implementations MUST adhere to security-first principles:
- Use Better Auth library exclusively (no NextAuth, Auth.js, or custom solutions)
- JWT tokens only (HS256 algorithm, no session cookies or OAuth in this phase)
- Strong secret key: BETTER_AUTH_SECRET must be 32+ random characters
- Store secrets in .env files only (never commit to git)
- Token expiry: 7 days (configurable)
- All API endpoints require valid JWT (except /health)
- Frontend stores JWT in httpOnly cookie OR localStorage (choose one)

### XV. JWT Token Management
JWT token structure and lifecycle MUST follow these standards:
```json
{
  "sub": "user_id_here",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

Frontend responsibilities:
- Signup → Login → Receive JWT → Store securely → Attach to all API requests
- Auto-attach JWT to Authorization: Bearer <token> header
- Persist JWT across page refreshes
- Clear JWT on logout

Backend responsibilities:
- Extract JWT from Authorization header
- Verify signature using BETTER_AUTH_SECRET (shared secret)
- Check token expiration (exp claim)
- Extract user_id from token payload
- Return 401 Unauthorized for missing/invalid/expired tokens
- Never call frontend to verify tokens (stateless JWT verification)

### XVI. User Isolation and Data Privacy
All data operations MUST enforce user isolation:
- Every task query MUST filter by authenticated user's ID
- Backend extracts user_id from JWT token payload
- User A cannot access User B's tasks (return 404, don't leak existence)
- All existing tasks must be migrated to a test user OR deleted
- Database: tasks.user_id foreign key references users.id

Error handling standards:
- 401 Unauthorized: Missing, invalid, or expired JWT token
- 403 Forbidden: Valid token but insufficient permissions (future use)
- 404 Not Found: Resource doesn't exist OR user doesn't own it (don't leak info)
- 422 Validation Error: Invalid signup/login data
- 500 Internal Server Error: Unexpected server issues

### Implementation Order (Step 4)
1. Update all specs with authentication requirements
   - `specs/features/authentication.md` (signup/login flows, JWT lifecycle, security requirements)
   - `specs/api/rest-endpoints.md` (add Authentication section, update all endpoints to require JWT)
   - `specs/database/schema.md` (verify users table structure, add indexes)
   - `specs/ui/pages.md` (add /login, /signup, /logout pages)
   - `specs/ui/components.md` (add AuthForm, ProtectedRoute components)

2. Frontend: Install and configure Better Auth with JWT plugin
   - npm install better-auth
   - Configure Better Auth in next.config or auth.ts
   - Enable JWT plugin with 7-day expiry
   - Configure database adapter for Neon PostgreSQL

3. Frontend: Create users table migration (Better Auth schema)
   - Better Auth handles table creation automatically
   - Verify users table has id, email, password, emailVerified fields

4. Frontend: Build signup page (/signup)
   - Form with email and password fields
   - Validation (email format, password strength)
   - Error handling for duplicate email
   - Redirect to /login after successful signup

5. Frontend: Build login page (/login)
   - Form with email and password fields
   - Error handling for invalid credentials
   - Store JWT token securely on success
   - Redirect to /tasks after login

6. Frontend: Test signup/login flow
   - Verify JWT token is issued on login
   - Verify token structure and claims
   - Test invalid credentials handling

7. Frontend: Update API client to attach JWT to requests
   - Modify `lib/api.ts` to include Authorization header
   - Extract token from storage
   - Handle 401 responses (redirect to login)

8. Frontend: Implement ProtectedRoute wrapper
   - Check for valid JWT token
   - Redirect to /login if not authenticated
   - Wrap /tasks page and future protected pages

9. Backend: Install JWT library
   - pip install python-jose[cryptography]
   - Configure BETTER_AUTH_SECRET environment variable

10. Backend: Create JWT verification middleware
    - Extract JWT from Authorization: Bearer <token> header
    - Verify signature with BETTER_AUTH_SECRET
    - Check token expiration
    - Return user_id from token payload
    - Return 401 for invalid/missing/expired tokens

11. Backend: Update all route handlers
    - Add JWT verification dependency to each endpoint
    - Extract user_id from token
    - Remove hardcoded "test-user-1"
    - Use authenticated user_id in all operations

12. Backend: Update database queries
    - Filter all task queries by user_id from JWT
    - Ensure user isolation in GET, PUT, DELETE, PATCH
    - Return 404 for tasks not owned by user

13. Backend: Test endpoints with tokens
    - Test with valid JWT (should work)
    - Test without JWT (should return 401)
    - Test with invalid JWT (should return 401)
    - Test with expired JWT (should return 401)
    - Test user isolation (User A cannot access User B's tasks)

14. Integration testing: Full authentication flow
    - Signup new user → Verify JWT issued
    - Login with credentials → Verify JWT issued
    - Create task with JWT → Verify task belongs to user
    - Logout → Verify JWT cleared
    - Login as different user → Verify cannot access previous user's tasks

15. Migration: Handle existing tasks
    - Assign existing tasks to a test user OR delete all tasks
    - Verify no orphaned tasks remain

### Exclusions (Not Building in Step 4)
The following are explicitly deferred to later steps:
- OAuth providers (Google, GitHub, etc.)
- Two-factor authentication (2FA)
- Password reset flow
- Email verification
- Role-based access control (RBAC)
- Refresh tokens (use long-lived access tokens for now)
- Session management UI (active sessions list)
- Account settings page

**Version**: 1.3.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-08
