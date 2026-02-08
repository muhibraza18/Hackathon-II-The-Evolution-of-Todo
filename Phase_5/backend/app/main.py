from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database.connection import engine, async_engine
from sqlmodel import SQLModel
from .routes import chat, tasks, reminders
from .auth.routes import router as auth_router
from .auth.middleware import AuthMiddleware

# Import all models to ensure they're registered
from .database.models import User, SessionModel, Task, Conversation, Message, Reminder

# Create the FastAPI app
app = FastAPI(
    title="AI Chat API for Todo AI Chatbot (Google Gemini)",
    description="API for interacting with AI assistant that manages tasks via MCP tools",
    version="1.0.0"
)

# CORS Middleware (MUST be added FIRST)
# NOTE: When allow_credentials=True, we cannot use "*" wildcard. Must specify exact origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004",
        "http://127.0.0.1:3005",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://frontend-service:3000",
        "http://frontend-service.default:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://backend-service:8000",
        "http://backend-service.default:8000",
        # Cloud deployment URLs
        "http://24.199.72.246:3000",
        "http://134.199.184.47:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
    allow_origin_regex=None,
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization", "Content-Type", "X-Requested-With"],
    max_age=600
)

# Add authentication middleware (AFTER CORS)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router, tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(reminders.router, prefix="/api", tags=["reminders"])


@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    print("Starting up...")

    try:
        print("Creating database tables...")
        # Use async engine for table creation (since we're using asyncpg)
        if async_engine:
            async with async_engine.begin() as conn:
                await conn.run_sync(lambda connection: SQLModel.metadata.create_all(connection, checkfirst=True))
        else:
            # Fallback to sync engine
            SQLModel.metadata.create_all(bind=engine, checkfirst=True)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("Application will continue anyway...")

    print("Database tables created successfully!")


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Chat API (Google Gemini)"}


@app.get("/health")
def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Chat API (Google Gemini)",
        "version": "1.0.0",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )