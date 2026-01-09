# Skill: JWT Middleware

## Description
Creates FastAPI middleware for JWT token verification and user extraction.

## Usage
/jwt-middleware

## Instructions
- Create `backend/middleware/auth.py`
- Implement JWT verification using `python-jose` library
- Extract and validate token from Authorization header
- Decode token to get `user_id` and other claims
- Create dependency function for protected routes
- Handle token expiration and invalid tokens
- Return proper HTTP errors (401, 403)
- Use same `BETTER_AUTH_SECRET` as frontend
- Follow patterns in `@backend/CLAUDE.md`

## Middleware Structure
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os

security = HTTPBearer()

def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    secret = os.getenv("BETTER_AUTH_SECRET")
    
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload  # Contains user_id, email, etc.
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Usage in routes
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(verify_jwt)
):
    # Verify user_id matches token
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # ... rest of logic
```

## Examples
- `/jwt-middleware`