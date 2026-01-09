# Research Log: Setup Monorepo Structure & Initial Specs

**Branch**: `001-foundation-setup`
**Date**: 2026-01-07

## Objectives
1. Validate Spec-Kit Plus requirements for blueprint-only delivery.
2. Confirm stack versions and tooling (Next.js 16+, FastAPI + SQLModel, Docker Desktop).
3. Identify onboarding needs for contributors (runtimes, env templates, verification commands).
4. Collect guidance for layered CLAUDE documentation and `@specs/...` linking.
5. Document architectural decisions with rationale and alternatives.

## Findings

### Spec-Kit & Constitution Requirements
- Phase 2 must only deliver scaffolding, specs, and configs (constitution Principle VI).
- `/specs` must include `overview.md`, `architecture.md`, `database/schema.md` referencing other docs via `@specs/...`.
- CLAUDE guidance is layered: root (global workflow), `/frontend` (Next.js patterns), `/backend` (FastAPI conventions).
- `.spec-kit/config.yaml` stores enforced directories and phase definitions (at least `phase1-console`, `phase2-web`).

### Stack & Tooling
- **Frontend**: Next.js 16+ App Router with TypeScript and Tailwind CSS. Node.js 20 recommended for compatibility.
- **Backend**: FastAPI + SQLModel with Pydantic v2, Uvicorn for ASGI server. Python 3.11 baseline.
- **Infrastructure**: Docker Desktop for Windows/macOS; Compose to run frontend/backend in tandem.
- **Schema**: Better Auth manages `users` table; only `tasks` table is defined locally (with `user_id` FK).

### Architectural Decisions

#### Decision 1: Monorepo vs Separate Repositories
**Decision**: Monorepo (single repository)

**Rationale**:
- Simplifies context for Claude Code (single workspace navigation)
- Enables cross-cutting changes across frontend and backend without repo coordination
- Reduces setup overhead for hackathon timeframe
- Shared CI/CD, documentation, and configuration
- Easier dependency management between services

**Alternatives Considered**:
- Separate repos: Independent deployments but requires repo coordination, duplicate CI/CD, and version alignment

**Tradeoff**: Monorepo is simpler for hackathon, easier cross-cutting changes

#### Decision 2: Spec Organization Structure
**Decision**: Organized `/specs` with subfolders (`features/`, `api/`, `database/`, `ui/`)

**Rationale**:
- Scales better as project grows
- Matches Spec-Kit Plus conventions
- Clear separation of concerns (features vs architecture vs data)
- Easier navigation and maintenance
- Prevents flat directory clutter

**Alternatives Considered**:
- Flat `/specs` folder: Simpler initially but becomes unwieldy with many specs

**Tradeoff**: Subfolder structure scales better, matches Spec-Kit Plus conventions

#### Decision 3: Frontend Router Choice
**Decision**: Next.js App Router (not Pages Router)

**Rationale**:
- Latest Next.js pattern (future-proof)
- Better server component support
- Improved performance with streaming
- Co-located routing and layouts
- Recommended by Next.js team for new projects

**Alternatives Considered**:
- Pages Router: Legacy pattern, less efficient for server-side rendering

**Tradeoff**: App Router is latest pattern, better server component support

#### Decision 4: Backend ORM Choice
**Decision**: SQLModel (not raw SQLAlchemy)

**Rationale**:
- Built on SQLAlchemy + Pydantic (best of both worlds)
- Native Pydantic models for FastAPI request/response validation
- Type-safe database models with IDE autocomplete
- Automatic schema generation for FastAPI docs
- Simpler API than raw SQLAlchemy

**Alternatives Considered**:
- Raw SQLAlchemy: More verbose, manual Pydantic conversion needed

**Tradeoff**: SQLModel provides Pydantic integration, simpler for FastAPI

#### Decision 5: Database Choice
**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- No local database management required
- Auto-scaling for hackathon load
- Serverless pricing (pay-as-you-go)
- PostgreSQL-compatible (standard SQL)
- Better Auth integration support
- Fast connection setup (connection string only)

**Alternatives Considered**:
- Local PostgreSQL via Docker: Requires local management, resource overhead

**Tradeoff**: Neon requires internet but no local management

#### Decision 6: Development Setup Approach
**Decision**: docker-compose.yml for orchestrated service startup

**Rationale**:
- Single command brings up both frontend and backend
- Consistent environment across team members
- Simplifies onboarding (no manual terminal management)
- Matches production-like orchestration
- Easy to add services (e.g., Redis) later

**Alternatives Considered**:
- Manual startup (separate terminals): Flexible but error-prone, requires documentation

**Tradeoff**: docker-compose simplifies multi-service orchestration

### Onboarding Considerations
- Contributors need instructions for Node.js, npm, Python, pip, and Docker installations.
- CLI commands should be documented both for manual runs (`npm run dev`, `uvicorn`) and docker (`docker-compose up`).
- `.env.example` files must clearly indicate placeholder values and secrets withheld per constitution.

### Best Practices Research

#### Next.js 16+ App Router Setup
**Key Patterns**:
- Use Server Components by default (default in App Router)
- Client Components marked with `"use client"` directive
- Layouts for shared UI (navigation, footer)
- Route groups for logical organization
- TypeScript strict mode enabled
- Tailwind CSS for styling (no custom CSS files)

**Dependencies**:
```json
{
  "dependencies": {
    "next": "16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

**Scripts**:
- `npm run dev`: Development server with hot reload
- `npm run build`: Production build
- `npm start`: Start production server
- `npm run lint`: ESLint checks

#### FastAPI + SQLModel Setup
**Key Patterns**:
- SQLModel inherits from SQLAlchemy + Pydantic
- Define models with type hints
- Use `engine` for DB connection
- `Session` for database operations
- FastAPI automatic OpenAPI docs at `/docs`
- Pydantic v2 for request/response validation

**Dependencies**:
```txt
fastapi>=0.109.0
sqlmodel>=0.0.18
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
```

**Scripts**:
- `uvicorn main:app --reload`: Development server
- `uvicorn main:app`: Production server
- `pytest`: Run tests

#### Docker Compose Configuration
**Best Practices**:
- Use named volumes for persistence (not needed here - Neon is cloud DB)
- Health checks for service readiness
- Expose ports only on localhost (security)
- Environment variables from `.env` file
- Shared network for service communication
- Volume mounts for live code reload

**Service Definitions**:
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      backend:
        condition: service_healthy

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

### Constraints & Exclusions
- No CRUD endpoints, auth flows, Neon connections, or migrations.
- No UI components beyond placeholder page.
- Health checks only (`/health`, Next.js default page).

## Validation Strategy

### Testing Strategy (from user input)

1. **Folder Structure Validation**:
   - Command: `tree /F` (Windows) or `ls -R` (Unix)
   - Check: All required directories exist

2. **Spec-Kit Config Validation**:
   - Command: `yamllint .spec-kit/config.yaml` or manual review
   - Check: Valid YAML with phases defined

3. **CLAUDE.md Reference Validation**:
   - Check: Each CLAUDE.md contains `@specs/...` references
   - Verify: No overlapping guidance between files

4. **Spec Content Validation**:
   - Check: `specs/overview.md` mentions Phase II and tech stack
   - Check: `specs/architecture.md` shows monorepo structure
   - Check: `specs/database/schema.md` has users + tasks tables

5. **Frontend Setup Validation**:
   - Command: `cd frontend && npm install`
   - Expected: Success without errors

6. **Backend Setup Validation**:
   - Command: `cd backend && pip install -r requirements.txt`
   - Expected: Success without errors

7. **Docker Compose Validation**:
   - Check: `docker-compose.yml` has frontend and backend services
   - Command: `docker-compose config` (validates syntax)

8. **Gitignore Validation**:
   - Check: `.gitignore` excludes `node_modules`, `__pycache__`, `.env`
   - Verify: No sensitive files tracked

9. **Dev Server Validation**:
   - Command: `cd frontend && npm run dev`
   - Expected: Server starts on port 3000

10. **Backend Server Validation**:
    - Command: `cd backend && uvicorn main:app --reload`
    - Expected: Server starts on port 8000, `/docs` accessible

## References
- `@specs/001-foundation-setup/spec.md`
- `.specify/memory/constitution.md`
- `.specify/templates/plan-template.md`
- `.specify/templates/tasks-template.md`

## Open Questions
- None at this stage; specification was explicit and checklist-confirmed.

## Next Steps
- Proceed with Phase 1: Generate data-model.md, contracts, and quickstart.md
- Use this research log to inform README quickstart and CLAUDE documentation sections.
