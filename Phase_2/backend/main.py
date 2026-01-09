"""
FastAPI Application Entry Point
Task CRUD Operations with Authentication (JWT Version)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router
from auth_endpoint import router as auth_router

# Initialize FastAPI application
app = FastAPI(
    title="Task CRUD API with Authentication",
    description="API for Task CRUD Operations with JWT-based Authentication",
    version="0.1.0",
)

# CORS middleware configuration (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3005",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3005"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancer probes.
    Returns a simple status indicating the service is running.
    """
    return {"status": "ok", "service": "task-crud-api"}

# Root endpoint
@app.get("/")
def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "name": "Task CRUD API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }

# Include routers
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])