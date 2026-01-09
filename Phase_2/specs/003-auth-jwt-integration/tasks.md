---
description: "Task list for authentication with Better Auth + JWT Integration"
---

# Tasks: Authentication with Better Auth + JWT Integration

**Input**: Design documents from `/specs/003-auth-jwt-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/`, `frontend/`
- **Mobile**: `api/`, `ios/` or `android/`
- Paths shown below assume web app - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Update backend requirements.txt to include PyJWT dependency
- [X] T002 [P] Update frontend package.json to include Better Auth dependencies
- [X] T003 [P] Create BETTER_AUTH_SECRET environment variable in .env and .env.local
- [X] T004 [P] Update CORS configuration in backend/main.py to allow credentials

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create auth.py backend module for JWT utilities in backend/auth.py
- [X] T006 [P] Update Task model in backend/models.py to include user_id foreign key
- [X] T007 [P] Create AuthContext in frontend/contexts/AuthContext.tsx for frontend auth state management
- [X] T008 [P] Create auth utilities in frontend/lib/auth.ts for Better Auth integration
- [X] T009 Update database schema to add user_id column to tasks table with foreign key reference
- [X] T010 Create ProtectedRoute component in frontend/components/ProtectedRoute.tsx
- [X] T011 Update API client in frontend/lib/api.ts to include JWT tokens in requests

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Account Creation (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account with email and password using Better Auth

**Independent Test**: Can be fully tested by registering a new user with email and password, then verifying the account is created in the database and can be used to log in.

### Implementation for User Story 1

- [X] T012 [P] Create signup page in frontend/app/signup/page.tsx with form and validation
- [X] T013 [P] Implement signup functionality using Better Auth in frontend/app/signup/page.tsx
- [X] T014 [P] Add email format validation to signup form in frontend/app/signup/page.tsx
- [X] T015 [P] Add password strength validation (min 8 chars) to signup form in frontend/app/signup/page.tsx
- [X] T016 [P] Handle signup errors and display appropriate messages in frontend/app/signup/page.tsx
- [X] T017 [P] Redirect to login page after successful signup in frontend/app/signup/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login and Authentication (Priority: P1)

**Goal**: Enable registered users to log in to their account and receive a JWT token for session management

**Independent Test**: Can be fully tested by logging in with valid credentials and verifying a JWT token is issued and stored properly.

### Implementation for User Story 2

- [X] T018 [P] Create login page in frontend/app/login/page.tsx with form and validation
- [X] T019 [P] Implement login functionality using Better Auth in frontend/app/login/page.tsx
- [X] T020 [P] Handle login errors and display appropriate messages in frontend/app/login/page.tsx
- [X] T021 [P] Store JWT token securely (httpOnly cookie) after successful login
- [X] T022 [P] Redirect to tasks page after successful login in frontend/app/login/page.tsx
- [X] T023 [P] Update AuthContext to handle login/logout operations
- [X] T024 [P] Test page refresh maintains authenticated state

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Task Access and User Isolation (Priority: P2)

**Goal**: Ensure authenticated users can only access their own tasks, with proper user isolation enforced

**Independent Test**: Can be fully tested by creating tasks as one user, logging in as another user, and verifying the second user cannot see the first user's tasks.

### Implementation for User Story 3

- [X] T025 [P] Create JWT verification dependency in backend/auth.py for FastAPI
- [X] T026 [P] Update all task endpoints in backend/routers/tasks.py to require authentication
- [X] T027 [P] Modify task queries to filter by authenticated user_id from JWT token
- [X] T028 [P] Return 404 for tasks not owned by authenticated user (don't leak existence)
- [X] T029 [P] Update frontend API calls to include JWT tokens automatically
- [X] T030 [P] Test that users cannot access each other's tasks via direct API calls

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - User Logout and Session Management (Priority: P2)

**Goal**: Allow logged-in users to securely log out and clear their JWT tokens

**Independent Test**: Can be fully tested by logging in, then logging out, and verifying the JWT token is cleared and protected routes are no longer accessible.

### Implementation for User Story 4

- [X] T031 [P] Create logout functionality in frontend/components/ProtectedRoute.tsx
- [X] T032 [P] Implement logout API call to clear session in Better Auth
- [X] T033 [P] Clear JWT token from frontend storage after logout
- [X] T034 [P] Redirect to login page after successful logout
- [X] T035 [P] Test that protected routes are inaccessible after logout
- [X] T036 [P] Update AuthContext to handle logout operations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T037 [P] Update Next.js configuration to support Better Auth in next.config.js
- [X] T038 [P] Add error handling for expired JWT tokens with appropriate user notifications
- [X] T039 [P] Add 401 handling to API client for automatic redirect to login
- [X] T040 [P] Create migration script for existing tasks to assign to default user
- [X] T041 [P] Update health check endpoint to remain public while protecting other endpoints
- [X] T042 [P] Add comprehensive error messages for authentication failures
- [X] T043 [P] Run quickstart.md validation to ensure complete flow works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Depends on US2 (login functionality) - requires authentication to be implemented first
- **User Story 4 (P2)**: Depends on US2 (login functionality) - requires authentication to be implemented first

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 2, 3, and 4 can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all signup page components together:
Task: "Create signup page in frontend/app/signup/page.tsx with form and validation"
Task: "Implement signup functionality using Better Auth in frontend/app/signup/page.tsx"
Task: "Add email format validation to signup form in frontend/app/signup/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Login)
5. **STOP and VALIDATE**: Test registration and login independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo (MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Stories 3 & 4 (since they depend on login)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence