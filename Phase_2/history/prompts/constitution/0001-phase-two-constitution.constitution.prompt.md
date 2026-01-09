---
id: 0001
title: Phase Two Constitution
stage: constitution
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,scaffolding]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Core principles:

Spec-driven foundation: All setup must align with Spec-Kit Plus conventions for organized, referenceable specifications.
Monorepo integrity: Ensure a single, cohesive repository structure that allows Claude Code to navigate and edit frontend, backend, and specs in one context.
Clarity and modularity: Use layered CLAUDE.md files to provide clear, level-specific guidance without overlap or redundancy.
Automation-first: Rely on Claude Code for scaffolding; no manual coding.

Key standards:

Folder structure must match: /specs (with subfolders: features, api, database, ui), /frontend, /backend, /.spec-kit/config.yaml.
CLAUDE.md files: Root for overview and workflow; frontend-specific for Next.js patterns; backend-specific for FastAPI patterns.
Initial specs: Include overview.md, architecture.md, and database/schema.md (covering users table managed by Better Auth and tasks table with user_id foreign key).
Config.yaml: Define project name, version, structure (dirs), and phases (at least phase1-console and phase2-web).
Scaffolding: Basic Next.js setup in /frontend (App Router, TypeScript, Tailwind); basic FastAPI in /backend (main.py, models.py, db.py); optional docker-compose.yml for running both.

Constraints:

No feature implementation: Focus only on foundation; exclude task CRUD, auth, or UI components.
No database connections yet: Schema spec only; defer actual Neon setup to later steps.
File references: Use @specs/[path] format for all spec linking in CLAUDE.md.
Tech versions: Next.js 16+ (App Router), FastAPI with SQLModel.

Success criteria:

Monorepo navigable by Claude Code with all folders and files in place.
Specs referenceable and organized per config.yaml.
CLAUDE.md files provide complete guidance for future steps without implementing them.
Basic run commands work (e.g., npm run dev in frontend, uvicorn in backend).

You MUST consider the user input before proceeding (if not empty).

## Response snapshot

- Replaced constitution template placeholders with Hackathon Phase 2 principles covering specs-first flow, monorepo structure, layered CLAUDE guidance, automation-first scaffolding, mandated Next.js/FastAPI stack, and blueprint-only delivery limits.
- Added Structural Standards and Delivery Workflow sections to encode folder/layout expectations, config governance, and required /sp.* workflow.
- Set version 1.0.0 with ratified/amended dates 2026-01-05 and prepended Sync Impact Report summarizing changes and template alignment status.

## Outcome

- ✅ Impact: Constitution fully authored for Hackathon Phase 2 foundation.
- 🧪 Tests: Not applicable for documentation update.
- 📁 Files: .specify/memory/constitution.md updated with new content and report.
- 🔁 Next prompts: None required; future template adjustments only if principles change again.
- 🧠 Reflection: Maintain strict automation-first approach and keep CLAUDE guides synchronized as new specs arrive.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): Not run.
- Prompt variant (if applicable): N/A.
- Next experiment (smallest change to try): N/A.
