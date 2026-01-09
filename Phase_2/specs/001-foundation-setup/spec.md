# Feature Specification: Setup Monorepo Structure & Initial Specs

**Feature Branch**: `001-foundation-setup`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description covering monorepo scaffolding, Spec-Kit Plus integration, CLAUDE.md guidance, initial specs, and baseline frontend/backend setups with docker orchestration.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Spec-Kit Monorepo Blueprint (Priority: P1)
A Claude Code operator initializes the repository so `/specs`, `/frontend`, `/backend`, and `/.spec-kit/config.yaml` exist with mandated subdirectories and templates. Specs reference each other using `@specs/...` paths, and CLAUDE.md files outline layered guidance.

**Why this priority**: Without an aligned blueprint, subsequent automation and scaffolding cannot proceed consistently.

**Independent Test**: Run `ls specs` and confirm `features/`, `api/`, `database/`, `ui/`, plus `overview.md`, `architecture.md`, and `database/schema.md` exist with required content.

**Acceptance Scenarios**:
1. **Given** a fresh clone, **when** the operator runs the setup commands, **then** the `specs/` tree contains mandated folders and seed documents with cross-links.
2. **Given** CLAUDE.md files, **when** reviewers open root, frontend, and backend guides, **then** each references `@specs/...` files without overlap.

---

### User Story 2 - Framework Scaffolding Readiness (Priority: P1)
A developer bootstraps the frontend (Next.js 16+, TS, Tailwind) and backend (FastAPI + SQLModel) projects, ensuring `.env.example` files, package manifests, and health endpoints exist before features are added.

**Why this priority**: Framework scaffolding is required before any future CRUD, auth, or UI tasks can start.

**Independent Test**: Run `npm run dev` inside `/frontend` and `uvicorn backend.main:app --reload` to verify servers boot with placeholder pages and health route.

**Acceptance Scenarios**:
1. **Given** the frontend folder, **when** `npm install && npm run dev` executes, **then** the App Router serves a baseline page at `http://localhost:3000` without errors.
2. **Given** the backend folder, **when** dependencies are installed from `requirements.txt` and `uvicorn` runs, **then** FastAPI responds at `/docs` and `/health`.

---

### User Story 3 - Local Orchestration & Documentation (Priority: P2)
The team documents startup steps in README.md and docker-compose.yml so both services can run together with matching environment expectations.

**Why this priority**: Combined orchestration ensures onboarding and QA can validate the foundation quickly.

**Independent Test**: Run `docker-compose up` and confirm frontend (port 3000) and backend (port 8000) become healthy while README instructions remain accurate.

**Acceptance Scenarios**:
1. **Given** docker-compose.yml, **when** `docker-compose up` runs, **then** both containers report healthy status and expose documented ports.
2. **Given** README instructions, **when** a new contributor follows them, **then** they can start both dev servers and locate all CLAUDE.md files without seeking extra help.

### Edge Cases
- What happens when required runtimes (Node 20+, Python 3.11+) are missing on a contributor’s machine?
- How does the system handle docker conflicts (ports already in use or Docker Desktop not running)?
- What if `.env` secrets are missing—do commands fail loudly with guidance?
- How are mismatched package managers (npm vs. pnpm) handled during bootstrap?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST provide `/.spec-kit/config.yaml` describing project metadata, enforced directories, and phases (at least `phase1-console`, `phase2-web`).
- **FR-002**: Repository MUST include `/specs/overview.md`, `/specs/architecture.md`, and `/specs/database/schema.md` detailing Better Auth-managed `users` and `tasks` tables (with `user_id` FK).
- **FR-003**: `/frontend` MUST host a Next.js 16+ App Router project with TypeScript, Tailwind, `package.json`, `app/page.tsx`, and `.env.example` declaring required variables.
- **FR-004**: `/backend` MUST host a FastAPI project using SQLModel, containing `main.py`, `models.py`, `db.py`, `requirements.txt`, and `.env.example` for future Neon credentials.
- **FR-005**: Root, frontend, and backend MUST each include CLAUDE.md files outlining workflows, referencing specs, and preventing overlapping guidance.
- **FR-006**: Repository MUST provide docker-compose.yml that builds/runs both services with shared network and documented ports (frontend 3000, backend 8000).
- **FR-007**: README.md MUST explain setup, environment expectations, and validation steps (dev servers, docker-compose, lint checks) without requiring undocumented commands.
- **FR-008**: No business logic, CRUD endpoints, authentication, or database migrations may be included; health checks only.

### Key Entities
- **Monorepo Workspace**: Root directory containing specs, frontend, backend, config, docker, and documentation artifacts required for foundation work.
- **Reference Specifications**: Documents under `/specs` (overview, architecture, database) that codify requirements for future phases using `@specs/...` references.
- **Environment Templates**: `.env.example` files and `.spec-kit/config.yaml` acting as the single source of truth for runtime/config expectations.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: A new contributor can clone the repo, install prerequisites, and start both dev servers in under 15 minutes by following README instructions.
- **SC-002**: `docker-compose up` brings both services to a healthy state within 60 seconds, exposing frontend on port 3000 and backend on port 8000 consistently.
- **SC-003**: All CLAUDE.md files and specs reference required documents via `@specs/...` with zero broken links during review.
- **SC-004**: `database/schema.md` documents at least the Better Auth `users` table and the `tasks` table with `user_id` foreign key, enabling downstream planning without further context.

## Assumptions
- Contributors have Node.js 20+ and Python 3.11+ installed; README will point to official installers when missing.
- Better Auth integration and Neon database provisioning will occur in later phases; current work only documents schema expectations.
- Docker Desktop (or compatible runtime) is available for local orchestration tests.
