---
id: 0003
title: Foundation Plan
stage: plan
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-foundation-setup
branch: 001-foundation-setup
user: user
command: /sp.plan
labels: [plan,foundation,research]
links:
  spec: specs/001-foundation-setup/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-foundation-setup/plan.md
 - specs/001-foundation-setup/research.md
 - specs/001-foundation-setup/data-model.md
 - specs/001-foundation-setup/quickstart.md
tests:
 - none
---

## Prompt

/sp.plan

Create:
- Monorepo folder structure blueprint (exact hierarchy)
- Spec-Kit Plus configuration file template
- CLAUDE.md content structure for root, frontend, and backend
- Initial spec files outline (overview, architecture, database schema)
- Development environment setup steps (Next.js + FastAPI initialization)
- Docker compose service definitions

Decisions needing documentation:
1. **Monorepo vs separate repos**:
   - Option A: Monorepo (single context for Claude Code) ✅ CHOSEN
   - Option B: Separate repos (independent deployments)
   - Tradeoff: Monorepo is simpler for hackathon, easier cross-cutting changes
2. **Spec organization**:
   - Option A: Flat /specs folder
   - Option B: Organized /specs with subfolders (features/, api/, database/, ui/) ✅ CHOSEN
   - Tradeoff: Subfolder structure scales better, matches Spec-Kit Plus conventions

3. **Frontend framework**:
   - Option A: Next.js Pages Router
   - Option B: Next.js App Router ✅ CHOSEN
   - Tradeoff: App Router is latest pattern, better server component support

4. **Backend ORM**:
   - Option A: Raw SQLAlchemy
   - Option B: SQLModel ✅ CHOSEN
   - Tradeoff: SQLModel provides Pydantic integration, simpler for FastAPI

5. **Database choice**:
   - Option A: Local PostgreSQL via Docker
   - Option B: Neon Serverless PostgreSQL ✅ CHOSEN
   - Tradeoff: Neon requires internet but no local management

6. **Development setup**:
   - Option A: Manual startup (separate terminal commands)
   - Option B: docker-compose.yml ✅ CHOSEN
   - Tradeoff: docker-compose simplifies multi-service orchestration

Testing strategy:
- Validation check 1: Verify all required folders exist (use tree command or ls -R)
- Validation check 2: Confirm .spec-kit/config.yaml is valid YAML and has phases defined
- Validation check 3: Check each CLAUDE.md contains spec reference instructions
- Validation check 4: Verify specs/overview.md mentions Phase II and lists tech stack
- Validation check 5: Confirm specs/architecture.md shows monorepo structure
- Validation check 6: Validate specs/database/schema.md has users + tasks tables
- Validation check 7: Run `cd frontend && npm install` succeeds
- Validation check 8: Run `cd backend && pip install -r requirements.txt` succeeds
- Validation check 9: Verify docker-compose.yml has frontend and backend services
- Validation check 10: Check .gitignore excludes node_modules, __pycache__, .env

Technical details:
- Use **scaffold-first approach** (create structure, then populate specs, then test setup)
- Follow **Spec-Kit Plus conventions** from Constitution
- Organize implementation phases:
  1. **Scaffold Phase**: Create all folders and empty files
  2. **Configuration Phase**: Write .spec-kit/config.yaml, package.json, requirements.txt
  3. **Documentation Phase**: Write all CLAUDE.md files with navigation guidance
  4. **Specification Phase**: Write overview.md, architecture.md, schema.md
  5. **Initialization Phase**: Run `npx create-next-app`, setup FastAPI project structure
  6. **Validation Phase**: Run all 10 validation checks listed above

Dependencies and order:
- .spec-kit/config.yaml must exist before writing specs (specs reference config)
- Root CLAUDE.md must exist before subfolder CLAUDE.md files (they reference root)
- Specs must be written before Next.js/FastAPI init (they guide implementation)
- package.json and requirements.txt needed before docker-compose.yml (for build context)

File generation priorities:
Priority 1 (Foundation):
- .spec-kit/config.yaml
- Root CLAUDE.md
- .gitignore
Priority 2 (Specifications):
- specs/overview.md
- specs/architecture.md
- specs/database/schema.md

Priority 3 (Layer Guidance):
- frontend/CLAUDE.md
- backend/CLAUDE.md

Priority 4 (Project Setup):
- frontend/ (Next.js initialization)
- backend/ (FastAPI structure)
- docker-compose.yml
Priority 5 (Documentation):
- README.md (setup instructions)

## Response snapshot

Successfully executed `/sp.plan` workflow for 001-foundation-setup feature:

1. **Plan Generation**:
   - Updated `specs/001-foundation-setup/plan.md` with comprehensive technical context
   - Completed Constitution Check: ALL GATES PASSED (6/6 principles)
   - Defined project structure (monorepo with frontend/backend)
   - No violations detected

2. **Phase 0 - Research**:
   - Updated `specs/001-foundation-setup/research.md` with:
     - 6 architectural decisions documented with rationale and alternatives
     - Best practices for Next.js 16+ App Router setup
     - FastAPI + SQLModel setup guidelines
     - Docker Compose configuration patterns
     - 10 validation checks defined
   - Resolved all NEEDS CLARIFICATION items

3. **Phase 1 - Artifacts**:
   - `data-model.md`: Verified existing (users table + tasks table schema)
   - `quickstart.md`: Verified existing (setup instructions, verification checklist)
   - Contracts: Not applicable (foundation phase only)

4. **Constitution Compliance**:
   - Spec-Driven Foundation: ✅
   - Monorepo Integrity: ✅
   - Layered Guidance: ✅
   - Automation-First Scaffolding: ✅
   - Stack Alignment: ✅
   - Blueprint-Only Delivery: ✅

## Outcome

- ✅ Impact: Implementation plan ready with complete technical context and architectural decisions
- 🧪 Tests: 10 validation checks defined for implementation phase
- 📁 Files: plan.md, research.md updated; data-model.md, quickstart.md verified
- 🔁 Next prompts: Proceed with `/sp.implement` to execute tasks from tasks.md
- 🧠 Reflection: All decisions align with constitution; blueprint-only scope maintained

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check passed (6/6 gates)
- Prompt variant (if applicable): N/A
- Next experiment: N/A (plan phase complete)
