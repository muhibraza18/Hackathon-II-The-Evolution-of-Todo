---
id: 0001
title: Foundation Specification
stage: spec
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-foundation-setup
branch: 001-foundation-setup
user: user
command: /sp.specify
labels: [specification,foundation]
links:
  spec: specs/001-foundation-setup/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-foundation-setup/spec.md
 - specs/001-foundation-setup/checklists/requirements.md
tests:
 - none
---

## Prompt

Setup Monorepo Structure & Initial Specs (Foundation Phase)

Target audience: Claude Code agent establishing project foundation for full-stack todo application

Focus: Create monorepo structure, Spec-Kit Plus integration, CLAUDE.md files, initial specs, and basic scaffolding (no features)

Success criteria:
- Monorepo created: /frontend, /backend, /specs (with subfolders: features/, api/, database/, ui/)
- .spec-kit/config.yaml configured with phase definitions
- Three CLAUDE.md files (root, frontend, backend) with navigation and patterns
- Specs written: overview.md, architecture.md, database/schema.md (users + tasks tables)
- Next.js 16+ initialized in /frontend (TypeScript, Tailwind, App Router)
- FastAPI initialized in /backend (SQLModel, main.py)
- docker-compose.yml for both services
- .env.example files for frontend and backend
- README.md with setup instructions

Constraints:
- Must use monorepo (single Claude Code context)
- Spec-Kit Plus structure with organized /specs subfolders
- Technology stack: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- Database schema: users table (Better Auth managed), tasks table (user_id FK)
- No feature implementation - only scaffolding

Required structure:
hackathon-todo/
├── .spec-kit/config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── database/schema.md
│   └── features/, api/, ui/ (empty folders)
├── CLAUDE.md
├── frontend/
│   ├── CLAUDE.md
│   ├── package.json
│   ├── .env.example
│   └── app/page.tsx
├── backend/
│   ├── CLAUDE.md
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py
├── docker-compose.yml
└── README.md

Not building:
- CRUD functionality or business logic
- Authentication (comes in Step 4)
- API endpoints (beyond health check)
- UI components for tasks
- JWT middleware
- Database migrations
- Production deployment config

Validation:
- [ ] `docker-compose up` starts both services
- [ ] Next.js accessible at localhost:3000
- [ ] FastAPI docs at localhost:8000/docs
- [ ] All CLAUDE.md files exist with content
- [ ] database/schema.md shows users + tasks tables

## Response snapshot

- Authored spec `specs/001-foundation-setup/spec.md` describing user stories for monorepo blueprint, framework scaffolding, and orchestration/documentation with edge cases and assumptions.
- Defined eight functional requirements, key entities, success criteria, and assumptions aligned with Spec-Kit Plus foundations.
- Created checklist `specs/001-foundation-setup/checklists/requirements.md` verifying no clarifications needed and spec readiness for `/sp.plan`.

## Outcome

- ✅ Impact: Repository now has a complete foundation specification for planning.
- 🧪 Tests: Documentation change only; no automated tests executed.
- 📁 Files: Spec and checklist added under `specs/001-foundation-setup/`.
- 🔁 Next prompts: Proceed with `/sp.clarify` if new questions arise, otherwise `/sp.plan`.
- 🧠 Reflection: Keep references in CLAUDE.md and README synchronized with spec during implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): Not run.
- Prompt variant (if applicable): N/A.
- Next experiment (smallest change to try): N/A.
