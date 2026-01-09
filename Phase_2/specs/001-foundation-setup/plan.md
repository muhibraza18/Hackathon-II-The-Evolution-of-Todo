# Implementation Plan: Foundation Setup

**Branch**: `001-foundation-setup` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-foundation-setup/spec.md`

## Summary

Establish the foundational monorepo structure for a Todo Full-Stack Web Application following Spec-Kit Plus conventions. This scaffolding phase creates the directory hierarchy, configuration files, initial specifications, and project boilerplate (Next.js 16+ App Router frontend, FastAPI + SQLModel backend) without implementing any business logic or authentication. All work is governed by the constitution and ensures `npm run dev` and `uvicorn backend.main:app --reload` succeed locally before proceeding to feature implementation.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.3+ (via Next.js 16+)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 19+, Tailwind CSS 3.4+
- Backend: FastAPI 0.109+, SQLModel 0.0.18+, Pydantic 2.5+

**Storage**: Neon Serverless PostgreSQL (Better Auth-managed `users` table + `tasks` table with `user_id` foreign key)

**Testing**: pytest (backend), Jest/Vitest (frontend - TBD in later phases)

**Target Platform**: Web browser (frontend) + Linux server (backend deployment)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**: Foundation phase has no performance requirements; baseline health checks only

**Constraints**:
- No business logic, CRUD endpoints, authentication, or database connections may be implemented in this phase
- Health check endpoints only (no feature code)
- Frontend must use App Router (not Pages Router)
- Backend must use SQLModel (not raw SQLAlchemy)
- All scaffolding via Claude Code automation (no manual coding)

**Scale/Scope**: Single workspace with `/specs`, `/frontend`, `/backend` directories; baseline structure for hackathon demo

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-Driven Foundation
- ✅ PASS: Deliverables begin as Spec-Kit Plus artifacts (spec.md → plan.md → tasks.md)
- ✅ PASS: No implementation without preceding spec
- ✅ PASS: Specs remain source of truth

### II. Monorepo Integrity
- ✅ PASS: Single workspace with `/specs`, `/frontend`, `/backend`, `/.spec-kit/config.yaml`
- ✅ PASS: All tooling operates from monorepo root
- ✅ PASS: No context switching required

### III. Layered Guidance
- ✅ PASS: CLAUDE.md files provide non-overlapping guidance (root, frontend, backend)
- ✅ PASS: Each CLAUDE.md references `@specs/...` links
- ✅ PASS: No duplicate or conflicting guidance

### IV. Automation-First Scaffolding
- ✅ PASS: All scaffolding via Claude Code commands or approved scripts
- ✅ PASS: Manual coding prohibited for setup
- ✅ PASS: Changes reproducible and reviewable

### V. Stack Alignment
- ✅ PASS: Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
- ✅ PASS: Backend: FastAPI + SQLModel
- ✅ PASS: Database schema includes Better Auth `users` table and `tasks` table with `user_id` FK
- ✅ PASS: docker-compose.yml orchestrates both services without divergence

### VI. Blueprint-Only Delivery
- ✅ PASS: Foundation phase only (scaffolding, specs, configuration)
- ✅ PASS: No feature logic, CRUD flows, auth wiring, or external DB connections
- ✅ PASS: Deliverables limited to proving `npm run dev` and `uvicorn` succeed locally

**Overall Status**: ✅ ALL GATES PASSED - No violations detected

## Project Structure

### Documentation (this feature)

```text
specs/001-foundation-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend monorepo)
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel models (users, tasks)
├── db.py                # Database connection setup
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── CLAUDE.md            # Backend development guidance

frontend/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page (placeholder)
│   └── globals.css      # Global styles
├── package.json         # Node dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tailwind.config.ts   # Tailwind CSS configuration
├── .env.example         # Environment variable template
└── CLAUDE.md            # Frontend development guidance

# Root configuration
.spec-kit/
├── config.yaml          # Spec-Kit Plus project configuration
└── templates/           # Spec-Kit templates

specs/
├── overview.md          # Project purpose, phase, tech stack
├── architecture.md      # System design, auth flow, API structure
├── database/
│   └── schema.md        # users + tasks tables with relationships
├── features/            # Feature-specific specs (future)
├── api/                 # API specifications (future)
└── ui/                  # UI specifications (future)

CLAUDE.md                # Root navigation and workflow guidance
docker-compose.yml       # Service orchestration
README.md                # Setup and development guide
.gitignore               # Ignored files (node_modules, __pycache__, .env)
```

**Structure Decision**: Web application monorepo with separate `/frontend` (Next.js 16+ App Router) and `/backend` (FastAPI + SQLModel) directories. Root contains Spec-Kit configuration, shared documentation, and docker-compose for orchestrated local development. This aligns with Constitution Principle II (Monorepo Integrity) and Principle V (Stack Alignment).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. Complexity tracking not applicable.
