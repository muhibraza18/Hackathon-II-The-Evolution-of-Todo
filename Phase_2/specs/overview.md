# Todo Full-Stack Web Application - Project Overview

## Project Purpose

A full-stack todo application built as a monorepo with Next.js 16+ (frontend) and FastAPI (backend), backed by Neon PostgreSQL. This project follows Spec-Kit Plus conventions for spec-driven development, ensuring all features are properly specified, architected, and implemented through structured workflows.

## Current Phase

**Active Phase**: Foundation Setup (`001-foundation-setup` branch)

This initial phase establishes:
- Monorepo directory structure
- Spec-Kit Plus configuration
- Framework scaffolding (Next.js 16+ and FastAPI)
- Layered development guidance via CLAUDE.md files
- Docker Compose orchestration
- Baseline documentation

**No business logic is implemented in this phase** - we only create the scaffolding to enable rapid feature development in subsequent phases.

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **UI Library**: TBD (likely shadcn/ui for future phases)

### Backend
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.18+
- **Database**: Neon Serverless PostgreSQL

### Authentication
- **Provider**: Better Auth
- **Managed Tables**: `users` table (managed externally by Better Auth)

### Development Tools
- **Version Control**: Git
- **Package Managers**: npm (frontend), pip/uv (backend)
- **Containerization**: Docker & Docker Compose
- **Documentation**: Spec-Kit Plus workflow

## Project Scope

The application will support:
- User authentication (via Better Auth)
- Task CRUD operations (create, read, update, delete)
- Task status management (pending, in_progress, completed)
- Task priority levels (low, medium, high)
- Personal task lists per authenticated user

### Out of Scope (Foundation Phase)
- Business logic implementation
- Database migrations
- Authentication integration
- API endpoints beyond health checks
- UI components beyond placeholders

## Directory Structure

```
.
├── .spec-kit/              # Spec-Kit Plus configuration
├── specs/                  # Feature specifications
│   ├── overview.md         # This file
│   ├── architecture.md     # System architecture
│   ├── database/           # Database specifications
│   ├── features/           # Feature-specific specs (future)
│   ├── api/                # API specifications (future)
│   └── ui/                 # UI specifications (future)
├── frontend/               # Next.js 16+ App Router
├── backend/                # FastAPI + SQLModel
├── history/                # Prompt history records and ADRs
├── CLAUDE.md               # Root development guidance
├── README.md               # Project README
└── docker-compose.yml      # Service orchestration
```

## Key Specifications

### Foundation Phase Specs
- **Feature Spec**: `@specs/001-foundation-setup/spec.md` - Feature requirements and user stories
- **Implementation Plan**: `@specs/001-foundation-setup/plan.md` - Architecture decisions and technical context
- **Task List**: `@specs/001-foundation-setup/tasks.md` - Detailed implementation tasks
- **Data Model**: `@specs/001-foundation-setup/data-model.md` - Entity definitions and relationships
- **Quickstart**: `@specs/001-foundation-setup/quickstart.md` - Developer onboarding guide

### Database Schema
- **Schema Documentation**: `@specs/database/schema.md` - Complete database structure including Better Auth's `users` table and local `tasks` table

## Development Workflow

1. **Specification**: Use `/sp.specify` to create feature specs
2. **Planning**: Use `/sp.plan` to generate architecture decisions
3. **Task Breakdown**: Use `/sp.tasks` to create actionable tasks
4. **Implementation**: Use `/sp.implement` to execute tasks
5. **Quality**: Create PHRs for all development work
6. **Architecture**: Document significant decisions with ADRs

## Success Criteria

A new contributor can:
- Clone the repository and complete setup in under 15 minutes
- Run `npm run dev` (frontend) and `uvicorn` (backend) successfully
- Start both services with `docker-compose up` within 60 seconds
- Navigate all CLAUDE.md files and understand development workflows
- Find all relevant specifications using `@specs/...` references

## Constitution Alignment

This project follows the principles in `.specify/memory/constitution.md`:
- **Spec-Driven Foundation**: All features start as specifications
- **Monorepo Integrity**: Single workspace with clear boundaries
- **Layered Guidance**: Non-overlapping CLAUDE.md files per directory
- **Automation-First**: Scaffolding via Spec-Kit Plus workflows
- **Stack Alignment**: Consistent tech stack across the monorepo
- **Blueprint-Only Delivery**: Foundation phase creates scaffolding, not features

## Related Documents

- **Architecture**: `@specs/architecture.md` - System design and component responsibilities
- **Database**: `@specs/database/schema.md` - Data model and relationships
- **Root Guide**: `CLAUDE.md` - Overall development guidance
- **Frontend Guide**: `frontend/CLAUDE.md` - Frontend-specific conventions
- **Backend Guide**: `backend/CLAUDE.md` - Backend-specific conventions

## Next Steps

After foundation setup:
1. Review architecture documentation
2. Study database schema
3. Begin feature implementation using Spec-Kit Plus workflows
4. Create PHRs for all development work
5. Document architectural decisions as they emerge
