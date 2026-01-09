# Skill: CORS Config

## Description
Configures CORS (Cross-Origin Resource Sharing) for FastAPI backend.

## Usage
/cors-config

## Instructions
- Update `backend/main.py` with CORS middleware
- Allow frontend origin (http://localhost:3000 for development)
- Configure allowed methods: GET, POST, PUT, DELETE, PATCH
- Configure allowed headers: Authorization, Content-Type
- Allow credentials for cookie-based auth
- Use environment variable for production origins
- Follow patterns in `@backend/CLAUDE.md`

## CORS Configuration
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Examples
- `/cors-config`