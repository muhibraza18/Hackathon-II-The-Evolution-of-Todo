# Implementation Plan: Task CRUD Operations (Unauthenticated Version)

**Branch**: `001-task-crud` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-task-crud/spec.md`

## Summary

This plan implements basic task CRUD operations (Create, Read, Update, Delete, Toggle completion) with persistent storage using an unauthenticated approach. The system provides a web interface for task management without requiring user login, using a fixed user identifier for all operations. Backend endpoints are implemented first (API-first pattern), followed by frontend integration, with incremental testing at each layer.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5.0+
**Primary Dependencies**: FastAPI, SQLModel, Next.js 16+, React, Tailwind CSS, PostgreSQL (Neon)
**Storage**: Neon PostgreSQL (cloud-hosted)
**Testing**: pytest (backend), manual testing (frontend)
**Target Platform**: Web (desktop and mobile browsers)
**Project Type**: web (frontend + backend monorepo)
**Performance Goals**: <2s task list update response, <500ms loading indicator display
**Constraints**: No authentication, fixed user_id = "test-user-1", all tasks visible globally
**Scale/Scope**: Dozens to hundreds of tasks, single-user testing scenario

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Status: ✅ PASSED

| Constitution Principle | Compliance | Evidence |
|------------------------|------------|----------|
| I. Spec-Driven Foundation | ✅ PASS | Feature spec exists at `/specs/001-task-crud/spec.md` with user stories, requirements, and success criteria |
| II. Monorepo Integrity | ✅ PASS | Repository structure includes `/specs`, `/frontend`, `/backend` with proper organization |
| III. Layered Guidance | ✅ PASS | CLAUDE.md files in root, frontend, and backend provide non-overlapping guidance |
| IV. Automation-First Scaffolding | ✅ PASS | Implementation will use Claude Code commands, no manual setup required |
| V. Stack Alignment | ✅ PASS | Uses Next.js 16+, FastAPI, SQLModel as specified; database schema includes users table and tasks table with user_id |
| VI. Blueprint-Only Delivery | ⚠️ N/A | Step 2 exceeds blueprint scope by implementing full CRUD (documented in Phase II Step 2) |
| VII. API-First Development | ✅ PASS | Backend endpoints implemented and tested before frontend integration |
| VIII. Unauthenticated Stage | ✅ PASS | Uses hardcoded `user_id = "test-user-1"`, no JWT/Bearer auth |
| IX. Simplified Feature Scope | ✅ PASS | Implements only basic CRUD (no categories, priorities, search, etc.) |
| X. Incremental Testing | ✅ PASS | Testing protocol includes 5 layers: database, API, integration, frontend, E2E |
| XI. API Client Centralization | ✅ PASS | All frontend communication through `/frontend/lib/api.ts` |
| XII. Success Criteria | ✅ PASS | 10 measurable criteria defined (create time, persistence, loading, etc.) |
| XIII. Implementation Sequencing | ✅ PASS | Follows exact 8-step sequence from constitution |

### Notes:

- **VI. Blueprint-Only Delivery**: This feature intentionally exceeds Phase 1 blueprint scope as part of Phase II Step 2 implementation. The constitution explicitly permits full CRUD implementation in Step 2.

## Project Structure

### Documentation (this feature)

```text
specs/001-task-crud/
├── plan.md                    # This file (/sp.plan command output)
├── spec.md                    # Feature specification (/sp.specify command output)
├── research.md                # Phase 0 output (/sp.plan command)
├── data-model.md              # Phase 1 output (/sp.plan command)
├── quickstart.md              # Phase 1 output (/sp.plan command)
├── contracts/                 # Phase 1 output (/sp.plan command)
│   ├── api-endpoints.md       # API contract documentation
│   └── frontend-types.md      # TypeScript type definitions
├── tasks.md                   # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
└── checklists/
    └── requirements.md        # Spec quality checklist
```

### Source Code (repository root)

```text
backend/
├── main.py                    # FastAPI app with CORS and route registration
├── models.py                  # Task SQLModel with validations
├── db.py                      # Database connection and session management
└── routes/
    └── tasks.py               # All 6 API endpoint handlers

frontend/
├── lib/
│   ├── api.ts                 # Typed API client with error handling
│   └── types.ts               # TypeScript type definitions
├── components/
│   ├── TaskList.tsx           # Displays all tasks
│   ├── TaskForm.tsx           # Create/edit form
│   └── TaskItem.tsx           # Individual task with actions
└── app/
    └── page.tsx               # Main tasks page
```

**Structure Decision**: Standard web application structure with backend API server and frontend SPA. Backend uses FastAPI with SQLModel for database operations. Frontend uses Next.js App Router with TypeScript and Tailwind CSS. This structure follows the monorepo pattern specified in Constitution Principle II.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification. The plan fully complies with all constitution principles for Phase II Step 2.

## Implementation Phases

### Phase 0: Research & Analysis (Current Phase)

**Goal**: Document architectural decisions, technology choices, and implementation approach.

**Deliverables**:
- `research.md` - Technology stack analysis, architectural patterns, decision rationale
- `data-model.md` - Task entity definition, field specifications, relationships
- `quickstart.md` - Developer onboarding guide for implementing this feature

### Phase 1: Design & Contracts

**Goal**: Define API contracts, database schema, and frontend architecture.

**Deliverables**:
- `contracts/api-endpoints.md` - Complete API documentation for all 6 endpoints
- `contracts/frontend-types.md` - TypeScript interfaces matching API contracts

### Phase 2: Task Generation

**Goal**: Create dependency-ordered implementation tasks grouped by user story.

**Deliverables**:
- `tasks.md` - Generated by `/sp.tasks` command (not part of this plan)

## Architectural Decisions

### 1. Task Model Structure

**Decision**: Extended fields (id, user_id, title, description, completed, created_at, updated_at)

**Rationale**:
- Prepares for future authentication by including user_id field
- Timestamps enable audit trails and sorting
- Description field provides context beyond title

**Tradeoffs**:
- Pros: Future-proof, data-rich, enables sorting/filtering
- Cons: More complex than minimal model, slightly larger database footprint

### 2. API Endpoint Organization

**Decision**: User-scoped routes `/api/{user_id}/tasks`

**Rationale**:
- Aligns with future authentication pattern
- Enables smooth transition to user-specific filtering
- RESTful representation of user-task relationship

**Tradeoffs**:
- Pros: Auth-ready, follows REST conventions, clear ownership
- Cons: Requires dummy user_id now, slightly longer URLs

**Endpoints**:
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks` - List all tasks
- `GET /api/{user_id}/tasks/{id}` - Get single task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### 3. Frontend State Management

**Decision**: Local component state with props drilling

**Rationale**:
- Simplest approach for MVP feature
- No external dependencies required
- Clear data flow (parent → child)

**Tradeoffs**:
- Pros: Zero learning curve, minimal code, predictable behavior
- Cons: Prop drilling can become verbose with deep component trees

**Data Flow**:
- `page.tsx` (parent) → `TaskList.tsx` → `TaskItem.tsx` (children)
- `page.tsx` manages tasks state and passes as prop to TaskList
- TaskList passes each task to TaskItem for rendering

### 4. API Client Error Handling

**Decision**: Return `{ data, error }` objects

**Rationale**:
- Gives components explicit control over error display
- Type-safe error handling
- Consistent pattern across all API calls

**Tradeoffs**:
- Pros: Flexible, explicit, type-safe, easy to test
- Cons: Slightly more verbose than throw/catch pattern

**API Client Pattern**:
```typescript
async function fetchTasks(): Promise<{ data: Task[] | null, error: string | null }> {
  try {
    const response = await fetch('/api/test-user-1/tasks')
    if (!response.ok) throw new Error(response.statusText)
    const data = await response.json()
    return { data, error: null }
  } catch (err) {
    return { data: null, error: err.message }
  }
}
```

### 5. Database Connection Strategy

**Decision**: Connection pooling with FastAPI dependency injection

**Rationale**:
- Efficient resource utilization
- Automatic cleanup via FastAPI lifespan
- Thread-safe session handling

**Tradeoffs**:
- Pros: Production-ready, scalable, automatic cleanup
- Cons: Requires understanding of FastAPI dependency system

**Implementation**:
```python
from sqlmodel import Session, create_engine
from fastapi import Depends

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

### 6. Frontend Component Structure

**Decision**: Separate TaskList, TaskForm, TaskItem components

**Rationale**:
- Separation of concerns
- Reusability (TaskItem can be used elsewhere)
- Easier testing

**Tradeoffs**:
- Pros: Maintainable, testable, reusable, clear responsibilities
- Cons: More files, requires prop passing between components

**Component Hierarchy**:
```
page.tsx (Server Component)
├── TaskList (Client Component)
│   ├── TaskForm (Client Component) - for create/edit
│   └── TaskItem (Client Component) - repeated for each task
│       └── Action buttons (edit, complete, delete)
```

## Testing Strategy

### Backend Validation Checks (10 checks)

1. **Task Model Validation**: Task model creates valid SQLModel instance with all required fields
2. **Database Connection**: Database connection establishes successfully
3. **POST Endpoint**: `POST /api/test-user-1/tasks` returns 201 with created task
4. **GET All Endpoint**: `GET /api/test-user-1/tasks` returns 200 with array
5. **GET Single Endpoint**: `GET /api/test-user-1/tasks/{id}` returns 200 with single task
6. **PUT Endpoint**: `PUT /api/test-user-1/tasks/{id}` returns 200 with updated task
7. **PATCH Complete**: `PATCH /api/test-user-1/tasks/{id}/complete` toggles completed status
8. **DELETE Endpoint**: `DELETE /api/test-user-1/tasks/{id}` returns 204
9. **Not Found Error**: Invalid task ID returns 404
10. **Validation Error**: Missing required fields return 422 validation error

### Frontend Validation Checks (10 checks)

1. **API Client**: API client successfully calls backend
2. **Task List Display**: Task list displays on page load
3. **Create Form**: Create form submits and adds task to list
4. **Edit Button**: Edit button populates form with task data
5. **Update Save**: Update saves changes and refreshes list
6. **Complete Toggle**: Complete button toggles task status
7. **Delete Action**: Delete button removes task from list
8. **Loading Indicators**: Loading indicators show during API calls
9. **Error Messages**: Error messages display on API failures
10. **Form Validation**: Form validation prevents empty title submission

### Integration Validation Checks (5 checks)

1. **Create Persistence**: Create task in frontend → verify in database
2. **Update Persistence**: Update task → changes persist after page refresh
3. **Delete Persistence**: Delete task → no longer appears after refresh
4. **Complete Persistence**: Complete toggle → status persists in database
5. **Order Consistency**: Multiple tasks display in correct order (newest first)

## Implementation Sequencing

Following Constitution Principle XIII (Implementation Sequencing):

1. **Update Specs Phase**: Update all 5 spec files with detailed requirements
   - `specs/features/task-crud.md` (user stories, acceptance criteria, test cases)
   - `specs/api/rest-endpoints.md` (request/response formats, error codes)
   - `specs/database/schema.md` (verify tasks table structure)
   - `specs/ui/components.md` (task list, task form, task item components)
   - `specs/ui/pages.md` (main tasks page layout and behavior)

2. **Backend Model Phase**: Create Task model in models.py
   - Define SQLModel Task class with fields: id, user_id, title, description, completed, created_at, updated_at
   - Add Pydantic validators for title length (1-200) and description length (0-1000)
   - Test model instantiation and validation

3. **Backend Routes Phase**: Implement all 6 API endpoints in routes/tasks.py
   - POST /api/{user_id}/tasks - Create task
   - GET /api/{user_id}/tasks - List tasks
   - GET /api/{user_id}/tasks/{id} - Get task
   - PUT /api/{user_id}/tasks/{id} - Update task
   - DELETE /api/{user_id}/tasks/{id} - Delete task
   - PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

4. **Backend Testing Phase**: Test endpoints with curl/Postman
   - Verify all endpoints return correct status codes
   - Validate request/response formats
   - Test error handling (404, 422, 500)
   - Confirm task persistence in database

5. **Frontend API Client Phase**: Build typed API client with error handling
   - Create /frontend/lib/api.ts with all CRUD functions
   - Implement error handling with `{ data, error }` returns
   - Add TypeScript types for requests/responses
   - Test API client against backend endpoints

6. **Frontend Components Phase**: Build TaskList, TaskForm, TaskItem
   - Create TaskItem.tsx with edit, complete, delete actions
   - Create TaskForm.tsx with validation and submit handling
   - Create TaskList.tsx with list display and form integration
   - Apply Tailwind CSS for responsive design

7. **Frontend Page Phase**: Assemble components into main tasks page
   - Create /frontend/app/page.tsx (Server Component)
   - Integrate TaskList with data fetching
   - Handle loading and error states
   - Test full page functionality

8. **Integration Testing Phase**: Full CRUD workflow end-to-end
   - Test create → view → edit → complete → delete flow
   - Verify persistence after page refresh
   - Test responsive design on mobile
   - Confirm all success criteria met

## File Creation Priorities

### Priority 1: Specifications (update existing files)
- `specs/features/task-crud.md`
- `specs/api/rest-endpoints.md`
- `specs/database/schema.md`
- `specs/ui/components.md`
- `specs/ui/pages.md`

### Priority 2: Backend Core
- `backend/models.py` (Task model)
- `backend/db.py` (database session management)

### Priority 3: Backend API
- `backend/routes/tasks.py` (all 6 endpoints)
- `backend/main.py` (update to register routes)

### Priority 4: Frontend API Client
- `frontend/lib/api.ts` (typed fetch wrapper)
- `frontend/lib/types.ts` (TypeScript interfaces)

### Priority 5: Frontend Components
- `frontend/components/TaskItem.tsx`
- `frontend/components/TaskForm.tsx`
- `frontend/components/TaskList.tsx`

### Priority 6: Frontend Page
- `frontend/app/page.tsx` (main tasks page)

### Priority 7: Styling
- Apply Tailwind CSS classes throughout
- Add loading spinners and error states

## Implementation Patterns

### Backend Patterns
- **Pydantic Models**: Separate request/response schemas from SQLModel for validation
- **Database Queries**: Use `select(Task).where()` for queries, avoid raw SQL
- **API Responses**: Always return JSON with consistent structure
- **Session Management**: Use FastAPI dependency injection for database sessions

### Frontend Patterns
- **Async/Await**: Use async/await for all API calls
- **Error Handling**: Try/catch in API client, display user-friendly messages
- **TypeScript**: Define interfaces for all data shapes
- **React**: Use Server Components for initial data fetch, Client Components for interactivity
- **State**: useState for form inputs, re-fetch after mutations

## Dummy User Handling

All operations use hardcoded `user_id = "test-user-1"`:
- Backend route handlers extract from path parameter
- Frontend API client injects into URLs
- Database queries filter by this user_id

**Note**: This will be replaced with real authentication in Steps 4-5.

## Dependencies

### Implementation Dependencies (must be completed in order)

1. Specs must be updated before any implementation (they guide development)
2. Database schema verification before model creation
3. Task model must exist before routes can reference it
4. All backend endpoints must work before frontend integration
5. API client must be created before components can call backend
6. TaskItem and TaskForm must exist before TaskList can use them
7. Components must exist before page can import them

### External Dependencies

- Neon PostgreSQL database (must be accessible)
- Network connectivity for API calls
- Modern web browser for frontend testing

## Next Steps

After plan completion:

1. Run `/sp.tasks` to generate dependency-ordered implementation tasks
2. Review `tasks.md` for complete task breakdown
3. Begin implementation following the task order
4. Create PHR for this planning phase

## Architectural Decision Records (ADRs)

The following architectural decisions should be documented as ADRs:

- **ADR-001**: Task model with extended fields (vs. minimal model)
- **ADR-002**: User-scoped API routes (vs. flat routes)
- **ADR-003**: Local component state management (vs. Context/Zustand)
- **ADR-004**: API client error handling with `{ data, error }` returns
- **ADR-005**: Database connection pooling with FastAPI DI
- **ADR-006**: Multi-component architecture (vs. single component)

**Note**: Run `/sp.adr <title>` to create each ADR if these decisions warrant formal documentation.
