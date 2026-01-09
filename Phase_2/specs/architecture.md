# System Architecture - Todo Full-Stack Web Application

**Branch**: `001-foundation-setup`
**Updated**: 2026-01-06

## Overview

This architecture document describes the system design, component responsibilities, and technical decisions for the Todo Full-Stack Web Application. The system is designed as a monorepo with separate frontend (Next.js 16+) and backend (FastAPI) services, backed by Neon PostgreSQL with Better Auth for authentication.

## System Components

### 1. Frontend Service (Next.js 16+)

**Location**: `/frontend`

**Responsibilities**:
- User interface rendering and interaction
- Client-side routing via App Router
- State management for task operations
- Form handling and validation
- Authentication integration (Better Auth)
- Responsive design with Tailwind CSS

**Key Conventions**:
- App Router (not Pages Router)
- Server Components by default
- Client Components only when needed (interactivity)
- TypeScript for type safety
- Tailwind CSS for styling

**Technology Stack**:
- Next.js 16+ with React 19+
- TypeScript 5.3+
- Tailwind CSS 3.4+
- Better Auth SDK (future)

**Entry Point**: `frontend/app/page.tsx`

### 2. Backend Service (FastAPI)

**Location**: `/backend`

**Responsibilities**:
- RESTful API endpoints for task operations
- Authentication and authorization middleware
- Business logic validation
- Database operations via SQLModel
- Request/response validation with Pydantic

**Key Conventions**:
- SQLModel for ORM (not raw SQLAlchemy)
- Pydantic models for validation
- Modular router structure
- Async/await for I/O operations
- Type hints throughout

**Technology Stack**:
- FastAPI 0.109+
- Python 3.11+
- SQLModel 0.0.18+
- Pydantic 2.5+

**Entry Point**: `backend/main.py`

### 3. Database Layer (Neon PostgreSQL)

**Provider**: Neon Serverless PostgreSQL

**Tables**:
- `users` - Managed by Better Auth (external)
- `tasks` - Local table managed by our application

**Access Pattern**:
- Backend connects to Neon via SQLModel/SQLAlchemy
- Better Auth manages `users` table externally
- Application manages `tasks` table with `user_id` foreign key

**Schema Documentation**: `@specs/database/schema.md`

### 4. Authentication Layer (Better Auth)

**Provider**: Better Auth

**Responsibilities**:
- User registration and login
- Session management
- JWT token generation and validation
- `users` table management (external)

**Integration**:
- Frontend: Better Auth SDK for authentication UI
- Backend: Middleware validates JWT tokens from requests
- Database: `users` table managed exclusively by Better Auth

**Future Implementation**: Not included in foundation phase

## Data Flow

### Task Creation Flow

```
User → Frontend (form) → Backend API → Database
                              ↓
                        Better Auth JWT validation
```

### Authentication Flow

```
User → Better Auth → Frontend (JWT)
                          ↓
                    Backend (JWT validation)
```

### Data Access Pattern

```
Frontend → Backend API (FastAPI)
               ↓
         SQLModel (ORM)
               ↓
         Neon PostgreSQL
```

## API Structure

### Planned Endpoints (Future Phases)

**Health Check** (Foundation Phase):
- `GET /health` - Service health status

**Authentication** (Future):
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

**Tasks** (Future):
- `GET /api/tasks` - List tasks for authenticated user
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

**Note**: Only `/health` endpoint exists in foundation phase

## Component Boundaries

### Frontend Responsibilities
- UI rendering and user interaction
- Client-side state management
- Form validation
- Routing (App Router)
- Authentication state (via Better Auth SDK)

### Backend Responsibilities
- API endpoint implementation
- Business logic validation
- Database operations
- Authentication middleware
- Request/response transformation

### Shared Concerns
- Type definitions (shared between frontend/backend in future phases)
- Environment configuration
- API contract (OpenAPI/Swagger)

## Security Considerations

### Current Foundation Phase
- No authentication implemented yet
- No database connections established
- Health check endpoint only (no sensitive data)

### Future Phases
- JWT-based authentication via Better Auth
- Input validation with Pydantic
- SQL injection prevention via SQLModel
- CORS configuration for API access
- Rate limiting (if needed)

## Deployment Architecture

### Development Environment
```
Docker Compose
    ├─ Frontend (Node 20) → Port 3000
    └─ Backend (Python 3.11) → Port 8000
```

### Production (Future)
```
- Frontend: Deployed to Vercel or similar platform
- Backend: Deployed to container platform (AWS ECS, Railway, etc.)
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth service
```

## Constitution Alignment

This architecture aligns with `.specify/memory/constitution.md`:

### Spec-Driven Foundation
- ✅ Architecture documented before implementation
- ✅ Component boundaries clearly defined
- ✅ Technology stack consistent across layers

### Monorepo Integrity
- ✅ Clear separation between `/frontend` and `/backend`
- ✅ Shared root for configuration and documentation
- ✅ Minimal context switching

### Layered Guidance
- ✅ CLAUDE.md files provide per-directory guidance
- ✅ `@specs/...` references link to specifications
- ✅ No overlapping responsibilities

### Stack Alignment
- ✅ Next.js 16+ with App Router
- ✅ FastAPI + SQLModel
- ✅ Neon PostgreSQL
- ✅ Better Auth for authentication

## Scaling Considerations

### Current Design
- Single backend instance
- Neon serverless database (scales automatically)
- Frontend static assets served from CDN

### Future Improvements
- Horizontal scaling for backend (load balancer)
- Redis caching for session management
- CDN for frontend assets
- Database connection pooling

## Related Documents

- **Database Schema**: `@specs/database/schema.md` - Entity definitions
- **Feature Spec**: `@specs/001-foundation-setup/spec.md` - User requirements
- **Implementation Plan**: `@specs/001-foundation-setup/plan.md` - Technical decisions
- **Data Model**: `@specs/001-foundation-setup/data-model.md` - Detailed entity definitions
- **Constitution**: `.specify/memory/constitution.md` - Project principles
