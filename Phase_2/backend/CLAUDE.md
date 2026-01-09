# Backend Development Guide - FastAPI + SQLModel

## Framework Conventions

This guide outlines the conventions and patterns for backend development in the Todo Full-Stack Web Application.

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.18+
- **Database**: Neon Serverless PostgreSQL
- **Validation**: Pydantic 2.5+

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel models
├── db.py                # Database connection setup
├── routers/             # API routers (future)
│   ├── tasks.py         # Task endpoints
│   └── auth.py          # Auth endpoints (future)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── CLAUDE.md            # This file
```

## FastAPI Conventions

### Application Structure
- Single main application instance in `main.py`
- Modular routers in `routers/` directory
- Async/await for all I/O operations
- Type hints for all functions

### Entry Point
```python
from fastapi import FastAPI
from routers import tasks, auth

app = FastAPI(title="Todo API")

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
```

## SQLModel Guidelines

### Model Definitions
- Use SQLModel for all database entities
- Define fields with proper types and constraints
- Use `Field()` for column configurations
- Include all indexes in model definitions

### Example Model
```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", index=True)
    priority: str = Field(default="medium")
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Important Notes
- **DO NOT define the `users` table** - it's managed exclusively by Better Auth
- Reference `users.id` as a foreign key in local tables
- All database operations should use the session from `db.py`

## Database Connection

### Session Management
```python
from sqlmodel import create_engine, Session
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
```

### Usage Pattern
```python
def create_task(task_data: TaskCreate, user_id: UUID):
    with get_session() as session:
        task = Task(**task_data.dict(), user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

## Environment Variables

### Required Variables
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret for Better Auth integration

### Example `.env`
```env
DATABASE_URL=postgresql://user:password@host:port/database
BETTER_AUTH_SECRET=your-secret-here
```

## Development Workflow

### Running the Development Server
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Access API docs at http://localhost:8000/docs

### Database Operations
- Use SQLAlchemy session from `db.py`
- Always commit transactions
- Use context managers for automatic cleanup
- Handle database errors gracefully

## API Endpoints

### Health Check (Foundation Phase)
```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### CRUD Patterns (Future)
```python
# Create
@app.post("/api/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    return task_service.create(task, current_user.id)

# Read (List)
@app.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(user_id: UUID = Depends(get_current_user_id)):
    return task_service.list(user_id)

# Read (Single)
@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    return task_service.get(task_id, user_id)

# Update
@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, task_update: TaskUpdate, user_id: UUID = Depends(get_current_user_id)):
    return task_service.update(task_id, task_update, user_id)

# Delete
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    task_service.delete(task_id, user_id)
    return {"status": "deleted"}
```

## Authentication (Future)

### Better Auth Integration
- Validate JWT tokens on protected endpoints
- Extract `user_id` from JWT claims
- Use FastAPI dependency injection for auth

### Example Dependency
```python
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except JWTError:
        raise HTTPException(status_code=401)
```

## Related Documentation

- **Project Overview**: `@specs/overview.md` - Tech stack and scope
- **Architecture**: `@specs/architecture.md` - Backend responsibilities
- **Database Schema**: `@specs/database/schema.md` - Entity definitions
- **Data Model**: `@specs/001-foundation-setup/data-model.md` - Detailed schema
- **Quickstart**: `@specs/001-foundation-setup/quickstart.md` - Setup instructions

## Best Practices

1. **Type Safety**: Use type hints for all function parameters and return values
2. **Validation**: Leverage Pydantic for request/response validation
3. **Error Handling**: Provide clear error messages with appropriate HTTP status codes
4. **Async Operations**: Use async/await for all database and I/O operations
5. **Security**: Never commit secrets, use environment variables

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000 (macOS/Linux)
lsof -i :8000
kill -9 <PID>

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Connection Issues
- Verify `DATABASE_URL` in `.env` file
- Check if Neon database is accessible
- Ensure SSL certificates are configured correctly

### Import Errors
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.11+)

## Testing (Future)

### Unit Tests
- Use pytest framework
- Mock database operations
- Test business logic independently

### Integration Tests
- Test API endpoints with test database
- Verify CRUD operations
- Test authentication flow

### Test Commands
```bash
pytest                   # Run all tests
pytest -v                # Verbose output
pytest --cov=app         # Coverage report
```
