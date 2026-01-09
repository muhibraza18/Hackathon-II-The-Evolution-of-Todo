# Todo Full-Stack Web Application

A full-stack todo application built with Next.js 16+ (frontend), FastAPI (backend), and Neon PostgreSQL (database). This monorepo follows Spec-Kit Plus conventions with spec-driven development.

## Prerequisites

Before setting up the development environment, ensure you have the following installed:

### Required Tools

- **Node.js** v20+ - [Download](https://nodejs.org/)
  - Check version: `node --version`

- **npm** v10+ (comes with Node.js)
  - Check version: `npm --version`

- **Python** v3.11+ - [Download](https://www.python.org/downloads/)
  - Check version: `python --version` or `python3 --version`

- **pip** (Python package manager) or **uv** (recommended for faster dependency management)
  - Check pip: `pip --version`
  - Install uv (optional): `pip install uv`

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
  - Check version: `docker --version`
  - Ensure Docker Desktop is running before using docker-compose

- **Git** - [Download](https://git-scm.com/downloads)
  - Check version: `git --version`

### Platform-Specific Notes

**Windows:**
- Install Windows Subsystem for Linux (WSL 2) for optimal Docker performance
- Use Git Bash or PowerShell for command-line operations

**macOS:**
- Use Homebrew for package management: `brew install node python docker git`

**Linux:**
- Use your distribution's package manager (apt, yum, pacman, etc.)

## Project Structure

```
.
├── .spec-kit/           # Spec-Kit Plus configuration
├── specs/               # Feature specifications and documentation
│   ├── overview.md
│   ├── architecture.md
│   └── database/
├── frontend/            # Next.js 16+ App Router
├── backend/             # FastAPI + SQLModel
├── history/             # Prompt history records and ADRs
├── CLAUDE.md            # Root development guidance
├── README.md            # This file
└── docker-compose.yml   # Service orchestration
```

## Quick Start

### Option 1: Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Phase_2
   ```

2. Start both services:
   ```bash
   docker-compose up
   ```

3. Access the applications:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

### Option 2: Manual Setup

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your values
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

5. Open http://localhost:3000

#### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or if using uv:
   uv pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

5. Start development server:
   ```bash
   uvicorn backend.main:app --reload
   ```

6. Access API documentation: http://localhost:8000/docs

## Development Workflow

1. Read `@specs/001-foundation-setup/spec.md` for feature requirements
2. Review `@specs/001-foundation-setup/plan.md` for architecture decisions
3. Execute tasks from `@specs/001-foundation-setup/tasks.md`
4. Run `@specs/001-foundation-setup/quickstart.md` validation steps

## Validation Checklist

- [ ] Frontend dev server starts without errors: `npm run dev`
- [ ] Backend dev server starts without errors: `uvicorn backend.main:app --reload`
- [ ] Health check endpoints respond:
  - Frontend: http://localhost:3000
  - Backend: http://localhost:8000/health
  - Backend API docs: http://localhost:8000/docs
- [ ] All `@specs/...` links resolve correctly
- [ ] Docker Compose starts both services within 60 seconds: `docker-compose up`
- [ ] Placeholder page displays foundation phase status correctly

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:
```bash
# Find process using port 3000 (macOS/Linux)
lsof -i :3000
# Kill the process
kill -9 <PID>

# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Docker Desktop Not Running

Ensure Docker Desktop is started before running docker-compose:
```bash
# Check Docker status
docker ps
# If error, start Docker Desktop from Applications
```

### Python Version Issues

If you encounter Python version errors:
```bash
# Check which Python is active
python --version
python3 --version

# Use pyenv (macOS/Linux) to manage versions
pyenv install 3.11.0
pyenv global 3.11.0
```

### Node Module Issues

If frontend has dependency conflicts:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Documentation

- **Spec-Kit Rules**: See `.specify/memory/constitution.md`
- **Project Overview**: `@specs/overview.md`
- **Architecture**: `@specs/architecture.md`
- **Database Schema**: `@specs/database/schema.md`
- **Development Guides**:
  - Root: `CLAUDE.md`
  - Frontend: `frontend/CLAUDE.md`
  - Backend: `backend/CLAUDE.md`

## Contributing

1. Follow the constitution in `.specify/memory/constitution.md`
2. Create feature specs under `specs/`
3. Use Spec-Kit Plus workflows (`/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement`)
4. Create PHRs for all significant development work
5. Document architectural decisions with ADRs

## License

[Add license information here]

## Support

For issues or questions:
1. Check `@specs/001-foundation-setup/quickstart.md` for common setup issues
2. Review relevant CLAUDE.md files for guidance
3. Check existing ADRs in `history/adr/`
