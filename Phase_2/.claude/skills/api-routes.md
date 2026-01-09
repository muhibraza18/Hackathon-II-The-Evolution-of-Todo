# Skill: API Routes

## Description
Creates or updates FastAPI route handlers with proper authentication and error handling.

## Usage
/api-routes <endpoint-group>

## Instructions
- Read `@specs/api/rest-endpoints.md` for endpoint specifications
- Create/update route files in `backend/routes/`
- Implement all CRUD operations for the resource
- Add JWT authentication dependency to all protected routes
- Extract `user_id` from verified token
- Filter all queries by authenticated user's ID
- Use proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Add request/response Pydantic models
- Include error handling with HTTPException
- Follow patterns in `@backend/CLAUDE.md`

## Route Structure
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    current_user: User = Depends(verify_jwt),
    status: Optional[str] = "all"
):
    # Verify user_id matches authenticated user
    # Filter by user_id and status
    # Return tasks
```

## Examples
- `/api-routes "tasks endpoints"`
- `/api-routes "user profile"`