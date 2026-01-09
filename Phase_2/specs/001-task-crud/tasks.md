---

description: "Task list for Task CRUD Operations feature implementation"
---

# Tasks: Task CRUD Operations (Unauthenticated Version)

**Input**: Design documents from `/specs/001-task-crud/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api-endpoints.md, contracts/frontend-types.md

**Tests**: Manual testing only - tests are NOT explicitly requested in specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `frontend/` at repository root
- Tasks assume the monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, environment setup, and basic structure

- [ ] T001 Verify backend directory structure exists with backend/models.py, backend/db.py, backend/main.py, backend/routes/tasks.py
- [ ] T002 Verify frontend directory structure exists with frontend/lib/, frontend/components/, frontend/app/page.tsx
- [ ] T003 Create backend/.env file with DATABASE_URL placeholder (use neon-db-steward subagent for Neon database setup assistance)
- [ ] T004 [P] Create frontend/.env.local with NEXT_PUBLIC_API_URL=http://localhost:8000/api
- [ ] T005 Create backend/requirements.txt with fastapi, uvicorn, sqlmodel, psycopg2-binary, python-dotenv dependencies
- [ ] T006 Verify frontend/package.json exists with Next.js 16+, React, Tailwind CSS dependencies

**Checkpoint**: Environment and project structure verified - ready for foundational work

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T007 Create database connection in backend/db.py using SQLModel create_engine with DATABASE_URL from environment (use neon-db-steward subagent for Neon-specific connection pooling setup)
- [ ] T008 Implement get_session() dependency injection function in backend/db.py for FastAPI session management
- [ ] T009 Create Task model in backend/models.py with SQLModel table=True, fields: id, user_id, title, description, completed, created_at, updated_at (use stack-validation-sentry subagent to validate model aligns with TypeScript types)
- [ ] T010 Create TaskCreate schema in backend/models.py extending TaskBase with title validation (min_length=1, max_length=200)
- [ ] T011 Create TaskUpdate schema in backend/models.py with optional title and description fields
- [ ] T012 Create TaskResponse schema in backend/models.py extending TaskBase with id, user_id, completed, created_at, updated_at
- [ ] T013 [P] Create database table creation script in backend/init_db.py to create tasks and users tables with indexes (use neon-db-steward subagent for Neon-specific migration approach)

### Frontend Foundation

- [ ] T014 Create TypeScript types in frontend/lib/types.ts: Task, TaskCreate, TaskUpdate, ApiResponse interfaces (use stack-validation-sentry subagent to generate types matching backend Pydantic models)
- [ ] T015 Create API client fetchApi function in frontend/lib/api.ts with { data, error } return pattern
- [ ] T016 Create fetchTasks function in frontend/lib/api.ts calling GET /api/test-user-1/tasks
- [ ] T017 Create createTask function in frontend/lib/api.ts calling POST /api/test-user-1/tasks
- [ ] T018 Create updateTask function in frontend/lib/api.ts calling PUT /api/test-user-1/tasks/{id}
- [ ] T019 Create deleteTask function in frontend/lib/api.ts calling DELETE /api/test-user-1/tasks/{id}
- [ ] T020 Create toggleComplete function in frontend/lib/api.ts calling PATCH /api/test-user-1/tasks/{id}/complete
- [ ] T021 [P] Create frontend/lib/api.ts error handling with try/catch and user-friendly error messages

### Backend Routes Foundation

- [ ] T022 Create FastAPI router in backend/routes/tasks.py for task endpoints
- [ ] T023 [P] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py creating tasks with TaskCreate schema validation
- [ ] T024 [P] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py returning all tasks ordered by created_at DESC
- [ ] T025 [P] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py returning single task or 404
- [ ] T026 [P] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py updating task with TaskUpdate schema
- [ ] T027 [P] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py deleting task
- [ ] T028 [P] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/routes/tasks.py toggling completed status
- [ ] T029 Add error handling with HTTPException(404) and HTTPException(422) in all backend/routes/tasks.py endpoints
- [ ] T030 Register tasks router in backend/main.py with /api prefix
- [ ] T031 [P] Add CORS middleware to backend/main.py allowing http://localhost:3000 origin (use fastapi-security-shield subagent for CORS configuration)
- [ ] T032 Test all 6 backend endpoints with curl commands from contracts/api-endpoints.md

**Checkpoint**: Foundation ready - backend API fully functional, frontend API client ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks and view all tasks in a list

**Independent Test**: Create a task with title and description → verify it appears in the task list with correct information displayed

### Frontend Components for US1

- [ ] T033 [P] [US1] Create TaskForm component in frontend/components/TaskForm.tsx as Client Component with title and description form fields
- [ ] T034 [P] [US1] Add form validation in frontend/components/TaskForm.tsx preventing empty title submission (1-200 chars, 0-1000 chars for description)
- [ ] T035 [P] [US1] Add submit handler in frontend/components/TaskForm.tsx calling createTask API function with loading state
- [ ] T036 [P] [US1] Add error message display in frontend/components/TaskForm.tsx showing API errors
- [ ] T037 [P] [US1] Add cancel button in frontend/components/TaskForm.tsx with onCancel callback support
- [ ] T038 [P] [US1] Create TaskItem component in frontend/components/TaskItem.tsx displaying task title, description, and completed status
- [ ] T039 [P] [US1] Add completed visual styling in frontend/components/TaskItem.tsx (strikethrough, opacity) using Tailwind CSS classes
- [ ] T040 [P] [US1] Create TaskList component in frontend/components/TaskList.tsx as Client Component with tasks state
- [ ] T041 [P] [US1] Add loadTasks call in frontend/components/TaskList.tsx useEffect on component mount
- [ ] T042 [P] [US1] Add loading state display in frontend/components/TaskList.tsx showing "Loading tasks..." while fetching
- [ ] T043 [P] [US1] Add error state display in frontend/components/TaskList.tsx showing API errors
- [ ] T044 [P] [US1] Render TaskForm in frontend/components/TaskList.tsx when showForm state is true
- [ ] T045 [P] [US1] Render TaskItem components in frontend/components/TaskList.tsx for each task in tasks array
- [ ] T046 [P] [US1] Add empty state display in frontend/components/TaskList.tsx showing "No tasks yet" when tasks array is empty
- [ ] T047 [P] [US1] Add "New Task" toggle button in frontend/components/TaskList.tsx to show/hide TaskForm

### Main Page Integration for US1

- [ ] T048 [US1] Update frontend/app/page.tsx to import and render TaskList component
- [ ] T049 [US1] Add responsive Tailwind CSS styling to frontend/app/page.tsx with max-width container and padding
- [ ] T050 [US1] Test complete create workflow: page load → click New Task → enter title and description → submit → verify task appears in list

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - MVP is ready

---

## Phase 4: User Story 2 - Edit and Complete Tasks (Priority: P2)

**Goal**: Enable users to edit task details and mark tasks as completed

**Independent Test**: Create a task → click edit → modify title → save → verify task is updated; click checkbox → verify completed status toggles

### Frontend Enhancements for US2

- [ ] T051 [P] [US2] Add mode prop (create | edit) to TaskForm component in frontend/components/TaskForm.tsx
- [ ] T052 [P] [US2] Add task prop to TaskForm component in frontend/components/TaskForm.tsx for edit mode prepopulation
- [ ] T053 [P] [US2] Populate form fields in TaskForm.tsx with task.title and task.description when in edit mode
- [ ] T054 [P] [US2] Call updateTask API function in TaskForm.tsx when mode is 'edit' instead of createTask
- [ ] T055 [P] [US2] Add Edit button in TaskItem component in frontend/components/TaskItem.tsx
- [ ] T056 [P] [US2] Add onEdit callback prop to TaskItem component in frontend/components/TaskItem.tsx passing task object
- [ ] T057 [P] [US2] Add checkbox input in TaskItem component in frontend/components/TaskItem.tsx for toggling completed status
- [ ] T058 [P] [US2] Add onChange handler in TaskItem.tsx calling toggleComplete API function
- [ ] T059 [P] [US2] Add onToggle callback prop to TaskItem component in frontend/components/TaskItem.tsx for parent refresh
- [ ] T060 [P] [US2] Add editingTask state to TaskList component in frontend/components/TaskList.tsx
- [ ] T061 [P] [US2] Add handleEdit function in TaskList.tsx setting editingTask and showForm to true
- [ ] T062 [P] [US2] Pass editingTask and handleEdit to TaskItem in TaskList.tsx
- [ ] T063 [P] [US2] Pass editingTask to TaskForm in TaskList.tsx for edit mode
- [ ] T064 [US2] Add reloadTasks call in TaskList.tsx after successful edit
- [ ] T065 [US2] Add reloadTasks call in TaskList.tsx after successful complete toggle

### Backend Verification for US2

- [ ] T066 [US2] Test PUT endpoint with curl updating task title and description (use api-integration-bridge subagent to verify frontend-backend type alignment)
- [ ] T067 [US2] Test PATCH /complete endpoint with curl toggling completed status
- [ ] T068 [US2] Verify updated_at timestamp updates on PUT and PATCH operations
- [ ] T069 [US2] Test edit workflow in frontend: create task → edit title → save → verify update
- [ ] T070 [US2] Test complete toggle workflow in frontend: create task → click checkbox → verify status change

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - tasks can be created, viewed, edited, and marked complete

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks from the list

**Independent Test**: Create a task → click delete → confirm → verify task is removed from list

### Frontend Enhancements for US3

- [ ] T071 [P] [US3] Add Delete button in TaskItem component in frontend/components/TaskItem.tsx
- [ ] T072 [P] [US3] Add onDelete callback prop to TaskItem component in frontend/components/TaskItem.tsx
- [ ] T073 [P] [US3] Add confirmation prompt in TaskItem.tsx before calling deleteTask API function
- [ ] T074 [P] [US3] Add handleDelete function in TaskList component in frontend/components/TaskList.tsx
- [ ] T075 [P] [US3] Pass handleDelete to TaskItem in TaskList.tsx
- [ ] T076 [US3] Add reloadTasks call in TaskList.tsx after successful delete

### Backend Verification for US3

- [ ] T077 [US3] Test DELETE endpoint with curl removing a task
- [ ] T078 [US3] Verify 204 No Content response on successful delete
- [ ] T079 [US3] Verify 404 response when deleting non-existent task
- [ ] T080 [US3] Test delete workflow in frontend: create task → delete → confirm → verify removal
- [ ] T081 [US3] Test multiple tasks: create 3 tasks → delete 1 → verify only specified task removed

**Checkpoint**: All user stories should now be independently functional - full CRUD workflow complete

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure production readiness

### Responsive Design

- [ ] T082 [P] Add mobile-responsive styling to frontend/components/TaskList.tsx using Tailwind breakpoints (sm, md, lg)
- [ ] T083 [P] Add mobile-responsive styling to frontend/components/TaskForm.tsx with proper input sizing on small screens
- [ ] T084 [P] Add mobile-responsive styling to frontend/components/TaskItem.tsx with proper spacing on small screens
- [ ] T085 Test responsive design on viewport width 375px (minimum supported size)
- [ ] T086 Test responsive design on viewport widths 768px, 1024px, 1440px

### Loading & Error States

- [ ] T087 [P] Add loading spinner component or Tailwind animation to frontend/components/TaskList.tsx
- [ ] T088 [P] Add loading state to TaskForm submit button in frontend/components/TaskForm.tsx showing "Saving..."
- [ ] T089 [P] Add loading state to TaskItem checkbox in frontend/components/TaskItem.tsx during toggle operation
- [ ] T090 [P] Add loading state to TaskItem delete button in frontend/components/TaskItem.tsx during delete operation
- [ ] T091 Add error boundary to frontend/app/page.tsx catching component errors

### Validation Enhancements

- [ ] T092 [P] Add character count display to TaskForm title input in frontend/components/TaskForm.tsx (x/200)
- [ ] T093 [P] Add character count display to TaskForm description textarea in frontend/components/TaskForm.tsx (x/1000)
- [ ] T094 [P] Add inline validation error in TaskForm.tsx showing real-time title validation
- [ ] T095 [P] Add inline validation error in TaskForm.tsx showing real-time description validation

### Edge Case Handling

- [ ] T096 Test creating task with 200-character title (boundary validation)
- [ ] T097 Test creating task with 1000-character description (boundary validation)
- [ ] T098 Test creating task with empty title → verify validation error (use testing-quality-ops subagent for validation testing)
- [ ] T099 Test creating task with special characters in title and description → verify proper display
- [ ] T100 Test creating task with only whitespace in title → verify validation error
- [ ] T101 Test network failure scenario → verify error message displays in UI
- [ ] T102 Test simultaneous edits from multiple users → verify last update wins
- [ ] T103 Test task list with 100+ tasks → verify scrollable interface and performance

### Success Criteria Verification

- [ ] T104 Verify create task completes in under 5 seconds from page load (use stack-perf-optimizer subagent for performance measurement)
- [ ] T105 Verify 100% task persistence after page refresh (create task → refresh → verify task exists)
- [ ] T106 Verify loading indicators appear within 500ms for slow operations
- [ ] T107 Verify error messages clearly explain validation failures (empty title, length exceeded)
- [ ] T108 Verify mobile UI functionality on 375px viewport
- [ ] T109 Verify task list updates reflect within 2 seconds of user action
- [ ] T110 Verify full CRUD workflow without page refresh needed

### Database & API Polish

- [ ] T111 Run database table creation script in backend/init_db.py to verify tasks table structure (use neon-db-steward subagent for Neon deployment)
- [ ] T112 Verify database indexes exist: idx_tasks_user_id, idx_tasks_created_at, idx_tasks_completed, idx_tasks_user_date
- [ ] T113 Verify user_id foreign key constraint in tasks table references users.id
- [ ] T114 Open Swagger UI at http://localhost:8000/docs and verify all 6 endpoints documented
- [ ] T115 Test all 6 API endpoints through Swagger UI interface

### Documentation & Quickstart Validation

- [ ] T116 Run quickstart.md setup instructions for new developer onboarding
- [ ] T117 Verify backend server starts with `uvicorn backend.main:app --reload` on port 8000
- [ ] T118 Verify frontend server starts with `npm run dev` on port 3000
- [ ] T119 Verify complete manual test workflow from quickstart.md: create → view → edit → complete → delete
- [ ] T120 [P] Update CLAUDE.md files in root, frontend, backend if implementation revealed new patterns
- [ ] T121 [P] Create or update feature-specific documentation in README.md

### Code Quality (Optional - if needed)

- [ ] T122 [P] Run Python linter (pylint or flake8) on backend code if configured
- [ ] T123 [P] Run TypeScript compiler with strict mode on frontend code
- [ ] T124 [P] Run ESLint on frontend code if configured
- [ ] T125 [P] Run Prettier formatter on frontend code if configured

**Checkpoint**: Feature production-ready with all success criteria met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - provides MVP
  - User Story 2 (P2): Can start after Foundational - builds on US1
  - User Story 3 (P3): Can start after Foundational - completes CRUD
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Extends TaskForm and TaskItem from US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational - Extends TaskItem from US1/US2 but should be independently testable

### Within Each User Story

- Foundation tasks must complete before any user story
- Components built in order: Form → Item → List → Page
- API client functions before component implementations
- Backend endpoints before frontend integration
- All tasks must follow checklist format with [P] marker for parallelizable tasks

### Parallel Opportunities

**Setup Phase (Phase 1)**:
```bash
# Can run in parallel:
Task: T001 - Verify backend directory structure
Task: T002 - Verify frontend directory structure
Task: T004 - Create frontend/.env.local
```

**Foundational Phase - Backend (Phase 2)**:
```bash
# Can run in parallel:
Task: T013 - Create database table creation script
Task: T021 - Create API client error handling
Task: T031 - Add CORS middleware
```

**Foundational Phase - Backend Routes (Phase 2)**:
```bash
# Can run in parallel:
Task: T023 - Implement POST endpoint
Task: T024 - Implement GET tasks endpoint
Task: T025 - Implement GET single task endpoint
Task: T026 - Implement PUT endpoint
Task: T027 - Implement DELETE endpoint
Task: T028 - Implement PATCH complete endpoint
```

**Foundational Phase - Frontend (Phase 2)**:
```bash
# Can run in parallel:
Task: T016 - Create fetchTasks function
Task: T017 - Create createTask function
Task: T018 - Create updateTask function
Task: T019 - Create deleteTask function
Task: T020 - Create toggleComplete function
```

**User Story 1 - Frontend Components (Phase 3)**:
```bash
# Can run in parallel:
Task: T033 - Create TaskForm component
Task: T038 - Create TaskItem component
Task: T039 - Add completed visual styling
Task: T040 - Create TaskList component
```

**User Story 2 - Frontend Enhancements (Phase 4)**:
```bash
# Can run in parallel:
Task: T051 - Add mode prop to TaskForm
Task: T052 - Add task prop to TaskForm
Task: T053 - Populate form fields
Task: T054 - Call updateTask API function
```

**User Story 3 - Frontend Enhancements (Phase 5)**:
```bash
# Can run in parallel:
Task: T071 - Add Delete button to TaskItem
Task: T072 - Add onDelete callback
Task: T073 - Add confirmation prompt
```

**Polish Phase - Responsive Design (Phase 6)**:
```bash
# Can run in parallel:
Task: T082 - Add mobile styling to TaskList
Task: T083 - Add mobile styling to TaskForm
Task: T084 - Add mobile styling to TaskItem
```

**Polish Phase - Loading States (Phase 6)**:
```bash
# Can run in parallel:
Task: T088 - Add loading to submit button
Task: T089 - Add loading to checkbox
Task: T090 - Add loading to delete button
```

**Polish Phase - Validation (Phase 6)**:
```bash
# Can run in parallel:
Task: T092 - Add title character count
Task: T093 - Add description character count
Task: T094 - Add inline title validation
Task: T095 - Add inline description validation
```

**Parallel Team Strategy**:

With multiple developers:

1. **Foundation Phase** (All developers):
   - All work on Setup and Foundational tasks together
   - T001-T032 complete foundation

2. **User Story Phase** (After foundation):
   - **Developer A**: User Story 1 (T033-T050) - MVP delivery
   - **Developer B**: User Story 2 (T051-T070) - Edit and complete
   - **Developer C**: User Story 3 (T071-T081) - Delete functionality
   - All work independently on their components

3. **Integration Phase**:
   - Merge all user story implementations
   - Run polish tasks together (T082-T125)

---

## Parallel Example: User Story 1 Implementation

```bash
# Launch all TaskForm tasks together:
Task: T033 - Create TaskForm component
Task: T034 - Add form validation
Task: T035 - Add submit handler
Task: T036 - Add error message display
Task: T037 - Add cancel button

# Launch all TaskItem tasks together:
Task: T038 - Create TaskItem component
Task: T039 - Add completed visual styling

# Launch all TaskList tasks together:
Task: T040 - Create TaskList component
Task: T041 - Add loadTasks call
Task: T042 - Add loading state display
Task: T043 - Add error state display
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T032) - **CRITICAL**
3. Complete Phase 3: User Story 1 (T033-T050)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Polish and cross-cutting concerns → Production ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With 3 developers:

1. **Week 1**: All complete Setup (T001-T006) + Foundational (T007-T032) together
2. **Week 2**: After foundation complete:
   - Developer A: User Story 1 (T033-T050) - MVP
   - Developer B: User Story 2 (T051-T070) - Edit/Complete
   - Developer C: User Story 3 (T071-T081) - Delete
3. **Week 3**: Merge and polish together (T082-T125)

---

## Sub-Agent and Skill Utilization Guide

Tasks marked with sub-agent recommendations:

### neon-db-steward (Use for Neon PostgreSQL tasks)
- T003: Neon database setup
- T007: Database connection pooling
- T013: Table creation and migration
- T111: Verify database deployment

### stack-validation-sentry (Use for type alignment tasks)
- T009: Task model to TypeScript alignment
- T014: TypeScript type generation
- T066: Frontend-backend type verification

### fastapi-security-shield (Use for security/middleware tasks)
- T031: CORS configuration

### api-integration-bridge (Use for type synchronization)
- T066: API type alignment verification

### stack-perf-optimizer (Use for performance tasks)
- T104: Create task performance measurement

### testing-quality-ops (Use for validation testing)
- T099: Validation error testing

---

## Success Criteria Checklist

Per specification success criteria (SC-001 to SC-010):

- [ ] SC-001: Create task in under 5 seconds (T104)
- [ ] SC-002: 100% task persistence (T105)
- [ ] SC-003: Loading indicators within 500ms (T106)
- [ ] SC-004: 95% first-attempt success (T099, T100, T102)
- [ ] SC-005: Valid input accepted 100% (T096, T097, T099)
- [ ] SC-006: Clear error messages (T106)
- [ ] SC-007: Mobile functional (T085)
- [ ] SC-008: Updates within 2 seconds (T109)
- [ ] SC-009: Full CRUD without refresh (T110)
- [ ] SC-010: User ID persisted (T099, T114)

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = User Story 1 only (Create and View Tasks)
- Full feature = User Stories 1 + 2 + 3 + Polish
- Use sub-agents and skills as noted in task descriptions for specialized assistance
- All validation checks from backend plan should pass before frontend integration

## Task Count Summary

- **Total Tasks**: 125
- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 26 tasks
- **Phase 3 (User Story 1 - MVP)**: 18 tasks
- **Phase 4 (User Story 2)**: 20 tasks
- **Phase 5 (User Story 3)**: 11 tasks
- **Phase 6 (Polish)**: 44 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel with appropriate grouping

**Suggested MVP Scope**: Phase 1 (6) + Phase 2 (26) + Phase 3 (18) = 50 tasks for functional MVP
