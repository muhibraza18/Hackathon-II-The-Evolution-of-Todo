---
id: 0002
title: Task CRUD Principles
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4.5
feature: none
branch: 001-foundation-setup
user: Wajahat traders
command: /sp.constitution
labels: [constitution,phase-ii,task-crud,success-criteria,implementation-sequencing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/0002-task-crud-principles.constitution.prompt.md
tests:
 - None
---

## Prompt

/sp.constitution
Project: Todo App - Basic Task CRUD Implementation (Phase II, Step 2)

Core principles:
- Spec-driven development (update specs → implement backend → implement frontend)
- API-first approach (backend endpoints functional before frontend integration)
- Test incrementally (verify each layer before moving to next)
- Simplicity first (unauthenticated version, dummy user_id for now)

Key standards:
- All features must have updated specs before implementation
- Backend: FastAPI + SQLModel + Neon PostgreSQL
- Frontend: Next.js 16+ (App Router) + TypeScript + Tailwind CSS
- API: RESTful conventions (GET, POST, PUT, DELETE, PATCH)
- Database: SQLModel models with proper relationships and indexes
- Code organization: /backend/models.py, /backend/routes/, /frontend/app/, /frontend/components/
- API client pattern: Centralized /frontend/lib/api.ts for all backend calls

Constraints:
- NO authentication yet (use hardcoded dummy user_id = "test-user-1")
- All users see same tasks for now (user isolation comes in Step 4)
- No JWT tokens or Bearer auth headers yet
- Frontend must work without login/signup
- Database must have user_id field (preparation for auth), but accept any value
- Use environment variables: DATABASE_URL (backend), NEXT_PUBLIC_API_URL (frontend)

Success criteria:
- Backend API endpoints return proper JSON responses
- Frontend can create, read, update, delete, and toggle tasks
- Tasks persist in Neon PostgreSQL database
- All CRUD operations work end-to-end (frontend → API → database)
- Responsive UI with loading states and error handling
- API returns appropriate HTTP status codes (200, 201, 404, 500)
- Database queries use SQLModel ORM (no raw SQL)
- Frontend uses React Server Components where possible
- Manual testing: Create task → View in list → Edit → Mark complete → Delete

Specifications to update:
- specs/features/task-crud.md (user stories, acceptance criteria, test cases)
- specs/api/rest-endpoints.md (request/response formats, error codes)
- specs/database/schema.md (verify tasks table structure)
- specs/ui/components.md (task list, task form, task item components)
- specs/ui/pages.md (main tasks page layout and behavior)

Implementation order:
1. Update all specs with detailed requirements
2. Backend: Create Task model in models.py
3. Backend: Implement all 6 API endpoints in routes/tasks.py
4. Backend: Test endpoints with curl/Postman
5. Frontend: Create API client lib/api.ts
6. Frontend: Build TaskList, TaskForm, TaskItem components
7. Frontend: Create main tasks page
8. Integration test: Full CRUD workflow

Not building in this step:
- User authentication (Step 4)
- JWT token verification (Step 5)
- User signup/signin pages (Step 4)
- User-specific task filtering (Step 5)
- Advanced features (priority, due dates, categories)
- Search or advanced filtering

## Response snapshot

Updated constitution to version 1.2.0 with two new principles:

**Principle XII - Success Criteria Definition:**
- Added 9 comprehensive success criteria for Step 2 implementation
- Includes backend API requirements, frontend functionality, database persistence, end-to-end workflows, responsive UI, proper HTTP status codes, ORM usage, React Server Components, and manual testing checklist

**Principle XIII - Implementation Sequencing:**
- Added 8-step implementation order that must be followed exactly
- Starts with spec updates across 5 spec files
- Continues through backend model creation, API endpoint implementation, and testing
- Proceeds to frontend API client, component building, and page creation
- Ends with integration testing of full CRUD workflow

**Exclusions Section:**
- Documented 6 items explicitly deferred to later steps
- Clarifies that auth, JWT, signup pages, user filtering, and advanced features are out of scope

The update maintained all existing principles (I-XI) and built upon them with concrete implementation guidance.

## Outcome

- ✅ Impact: Constitution now provides complete guidance for Phase II Step 2 task CRUD implementation with explicit success criteria and implementation sequencing
- 🧪 Tests: None required for constitution update
- 📁 Files: Modified .specify/memory/constitution.md, created PHR
- 🔁 Next prompts: Consider running /sp.specify to create task-crud.md specification based on these principles
- 🧠 Reflection: Existing constitution (1.1.0) already covered most principles; added missing success criteria, implementation order, and exclusions to make implementation guidance complete and actionable

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
