# Quickstart Guide: Setup Monorepo Structure & Initial Specs

**Branch**: `001-foundation-setup`
**Audience**: Contributors bootstrapping the Hackathon Phase 2 monorepo

## Prerequisites
- Node.js 20+ (https://nodejs.org)
- npm 10+ (bundled with Node)
- Python 3.11+ (https://www.python.org/downloads/)
- pip or uv (Python package manager)
- Docker Desktop (latest stable)
- Git CLI

## Repository Setup
```bash
# Clone repository
 git clone <repo-url> hackathon-todo
 cd hackathon-todo

# Install frontend dependencies
 cd frontend
 npm install
 cd ..

# Create Python virtual environment (optional but recommended)
 cd backend
 python -m venv .venv
 source .venv/bin/activate   # Windows: .venv\Scripts\activate
 pip install -r requirements.txt
 cd ..
```

## Environment Configuration
```bash
# Copy example env files and fill in values
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env
```
Required values (placeholders only during blueprint phase):
- `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
- `BETTER_AUTH_PUBLIC_KEY=placeholder`
- `DATABASE_URL=postgresql://placeholder`
- `BETTER_AUTH_SECRET=placeholder`

## Running Services Independently
```bash
# Frontend
cd frontend
npm run dev

# Backend
cd backend
uvicorn backend.main:app --reload
```
Validation:
- Visit `http://localhost:3000` → see placeholder Next.js page displaying "Foundation Setup Complete"
- Visit `http://localhost:8000/docs` → FastAPI Swagger UI with health check endpoint
- Visit `http://localhost:8000/health` → returns `{ "status": "ok", "service": "todo-api" }`
- Visit `http://localhost:8000/` → returns API information with version 0.1.0

## Running with Docker Compose
```bash
cd hackathon-todo
docker-compose up --build
```
Validation:
- Frontend container logs show `ready - started server on 0.0.0.0:3000`.
- Backend container logs show `Application startup complete.`
- Ports: frontend → `http://localhost:3000`, backend → `http://localhost:8000`.
- Stop with `Ctrl+C` then `docker-compose down`.

## Verification Checklist
- [ ] `npm run dev` serves placeholder page at port 3000.
- [ ] `uvicorn backend.main:app --reload` exposes `/docs` and `/health`.
- [ ] `docker-compose up` starts both services without errors in under 60 seconds.
- [ ] Root, frontend, backend CLAUDE.md files exist and reference `@specs/...`.
- [ ] `specs/database/schema.md` documents `users` (Better Auth) and `tasks` tables.
- [ ] README instructions mirror these steps and prerequisites.

## Troubleshooting
- **Ports already in use**: Stop existing services (`lsof -i :3000`, `lsof -i :8000`) or adjust docker-compose.
- **Missing runtimes**: Re-run installers; verify versions (`node -v`, `python --version`).
- **Docker not running**: Start Docker Desktop; ensure resources (CPU/RAM) are sufficient.
- **Env values missing**: CLI commands fail with descriptive errors; copy `.env.example` again and fill placeholders.

## Next Steps
- Follow `/sp.tasks` outputs to implement scaffolding tasks per user story.
- Keep CLAUDE.md, README, and specs synchronized whenever structure changes.
