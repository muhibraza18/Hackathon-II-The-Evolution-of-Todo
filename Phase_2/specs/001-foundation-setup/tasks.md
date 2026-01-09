---
description: "Task list for foundation scaffolding"
---

# Tasks: Setup Monorepo Structure & Initial Specs

**Input**: Design documents from `/specs/001-foundation-setup/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Only run validation steps explicitly listed under each story; no automated test suite required yet.

**Organization**: Tasks are grouped by user story so each story remains independently testable and deliverable.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Task can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)
- Include concrete file paths in every description

## Phase 1: Setup (Shared Infrastructure)
**Purpose**: Establish baseline repository structure and version control hygiene.**

- [X] T001 Create base directories `/.spec-kit`, `/specs`, `/frontend`, `/backend`, `/history/prompts` per implementation plan (repository root)
- [X] T002 Add `.gitkeep` files under `specs/features/`, `specs/api/`, `specs/database/`, `specs/ui/` to ensure empty subfolders remain tracked
- [X] T003 Create root `/.gitignore` covering `node_modules`, `.next/`, `.env*`, `__pycache__/`, `.venv/`, and docker artifacts

## Phase 2: Foundational (Blocking Prerequisites)
**Purpose**: Configure Spec-Kit metadata and document baseline prerequisites before story work begins. All later phases depend on these tasks.**

- [X] T004 Author `/.spec-kit/config.yaml` with project metadata, enforced directories, and phase definitions (`phase1-console`, `phase2-web`)
- [X] T005 Add prerequisites section to root `README.md` documenting required Node.js 20+, npm 10+, Python 3.11+, pip/uv, Docker Desktop, and Git

**Checkpoint**: Spec-Kit configuration ready—user story implementation may begin.

## Phase 3: User Story 1 – Spec-Kit Monorepo Blueprint (Priority: P1)
**Goal**: Deliver enforced specs foldering plus layered CLAUDE guidance referencing `@specs/...`.**

**Independent Test**: `ls specs` shows `features/`, `api/`, `database/`, `ui/`, `overview.md`, `architecture.md`, `database/schema.md`; opening CLAUDE.md files reveals correct cross-links without overlap.

### Implementation
- [X] T006 [US1] Draft `specs/overview.md` summarizing monorepo scope, referencing `@specs/001-foundation-setup/spec.md`, and outlining success criteria
- [X] T007 [US1] Author `specs/architecture.md` describing component responsibilities, stack alignment, and constitution references
- [X] T008 [US1] Write `specs/database/schema.md` documenting Better Auth-managed `users` table and local `tasks` table (fields, FK, indexes)
- [X] T009 [P] [US1] Update root `CLAUDE.md` navigation to link the new specs plus frontend/back-end guides using `@specs/...` syntax
- [X] T010 [P] [US1] Create `frontend/CLAUDE.md` detailing Next.js App Router conventions, Server/Client component rules, and links to specs
- [X] T011 [P] [US1] Create `backend/CLAUDE.md` outlining FastAPI module layout, SQLModel usage, and schema references

**Checkpoint**: Blueprint complete—specs and CLAUDE documentation allow new contributors to navigate requirements.

## Phase 4: User Story 2 – Framework Scaffolding Readiness (Priority: P1)
**Goal**: Bootstrap frontend and backend projects with health checks and env templates so dev servers run independently.**

**Independent Test**: `npm run dev` (frontend) and `uvicorn backend.main:app --reload` (backend) start successfully with placeholder output.

### Implementation
- [X] T012 [US2] Scaffold Next.js 16+ App Router project with TypeScript + Tailwind under `/frontend` (e.g., `npx create-next-app`) ensuring `package.json` scripts exist
- [X] T013 [P] [US2] Configure `frontend/tsconfig.json`, `frontend/tailwind.config.ts`, `frontend/postcss.config.js`, and `frontend/styles/globals.css` for Tailwind integration
- [X] T014 [P] [US2] Implement placeholder page in `frontend/app/page.tsx` describing blueprint-only state and linking README instructions
- [X] T015 [P] [US2] Create `frontend/.env.example` with `NEXT_PUBLIC_API_BASE_URL` and `BETTER_AUTH_PUBLIC_KEY` placeholders plus usage notes
- [X] T016 [US2] Initialize FastAPI entrypoint `backend/main.py` with `FastAPI()` instance, `/health` route, and router placeholder imports
- [X] T017 [P] [US2] Define SQLModel `Task` entity in `backend/models.py` reflecting fields from `data-model.md` (id, user_id FK, status, priority, timestamps)
- [X] T018 [P] [US2] Stub `backend/db.py` with SQLModel engine/session helpers referencing `DATABASE_URL` from environment
- [X] T019 [P] [US2] Capture backend dependencies in `backend/requirements.txt` and add `backend/.env.example` with `DATABASE_URL` + `BETTER_AUTH_SECRET` placeholders
- [X] T020 [US2] Document developer run commands (`npm run dev`, `uvicorn backend.main:app --reload`) inside `specs/001-foundation-setup/quickstart.md` to satisfy independent test criteria

**Checkpoint**: Both services run locally with health checks and documented env variables.

## Phase 5: User Story 3 – Local Orchestration & Documentation (Priority: P2)
**Goal**: Provide docker-compose orchestration plus comprehensive README/quickstart instructions for combined workflows.**

**Independent Test**: `docker-compose up` starts frontend (port 3000) and backend (port 8000) with healthy logs; README instructions allow a new contributor to finish setup in <15 minutes.

### Implementation
- [X] T021 [US3] Create `docker-compose.yml` orchestrating frontend (Node 20 image) and backend (Python 3.11 image) with shared network and exposed ports 3000/8000
- [X] T022 [P] [US3] Expand `README.md` with manual setup steps, docker usage, troubleshooting, and validation checklist referencing success criteria
- [X] T023 [P] [US3] Update `specs/001-foundation-setup/quickstart.md` with end-to-end instructions and verification checklist for npm, uvicorn, and docker-compose flows
- [X] T024 [US3] Run `docker-compose up`, `npm run dev`, and `uvicorn backend.main:app --reload`, recording outcomes in README "Validation" section per success criteria

**Checkpoint**: Documentation + orchestration validated—team onboarding can rely on README/quickstart alone.

## Phase N: Polish & Cross-Cutting Concerns
**Purpose**: Final verification ensuring documentation and references remain consistent.**

- [X] T025 Verify `CLAUDE.md`, `frontend/CLAUDE.md`, and `backend/CLAUDE.md` contain correct `@specs/...` links with no stale references
- [X] T026 Update `specs/001-foundation-setup/checklists/requirements.md` with final validation results and mark checklist items complete

---

## Dependencies & Execution Order
- **Setup (Phase 1)**: No dependencies—must finish before configuration.
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational; creates blueprint used by later phases.
- **User Story 2 (Phase 4)**: Depends on story 1 (needs CLAUDE/spec references) but can run in parallel with story 3 once blueprint stable.
- **User Story 3 (Phase 5)**: Depends on stories 1 & 2 (needs running apps and documentation sources).
- **Polish (Phase N)**: Depends on all prior phases.

## Parallel Opportunities
- **US1**: T009, T010, T011 can run concurrently while prose files (T006–T008) are written.
- **US2**: Frontend tasks T012–T015 can run in parallel with backend tasks T016–T019; documentation task T020 follows both.
- **US3**: T022 and T023 can proceed simultaneously once docker-compose (T021) is defined.

## Implementation Strategy
1. **MVP First**: Complete Setup + Foundational + User Story 1 to ensure Spec-Kit blueprint exists. This is the minimal increment enabling planning for downstream teams.
2. **Incremental Delivery**:
   - Deliver US1 → pause for review
   - Deliver US2 → verify dev servers
   - Deliver US3 → finalize documentation & docker workflows
3. **Parallel Execution**: After Foundational phase, split frontend vs backend tasks (US2) across contributors while documentation (US3) ramps once docker file exists.

## Notes
- Maintain blueprint-only scope; no CRUD/auth logic is allowed.
- Every file referencing other specs must use `@specs/...` syntax to stay consistent with constitution.
- Capture validation evidence (screenshots or log snippets) when completing T024 to ease future audits.
