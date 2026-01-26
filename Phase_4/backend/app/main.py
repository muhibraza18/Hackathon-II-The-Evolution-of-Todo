from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database.connection import engine
from sqlmodel import SQLModel
from .routes import chat
from .auth.routes import router as auth_router
from .auth.middleware import AuthMiddleware

# Import all models to ensure they're registered
from .database.models import User, SessionModel, Task, Conversation, Message

# Create the FastAPI app
app = FastAPI(
    title="AI Chat API for Todo AI Chatbot (Google Gemini)",
    description="API for interacting with AI assistant that manages tasks via MCP tools",
    version="1.0.0"
)

# CORS Middleware (MUST be added FIRST)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3002",
        "http://localhost:3004",
        "http://localhost:3003",
        "http://localhost:3001",
        "http://localhost:3005",
        "http://127.0.0.1:3005",
        "http://localhost:5173",
        "http://frontend-service:3000",
        "http://backend-service:8000",
        "http://127.0.0.1:58587",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://backend-service.default:8000",
        "http://frontend-service.default:3000",
        "*"  # Allow all origins during development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    allow_origin_regex=None,  # Remove regex to simplify
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization", "Content-Type", "X-Requested-With"],
    # Additional settings for development
    max_age=600  # Cache preflight requests for 10 minutes
)

# Add authentication middleware (AFTER CORS)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router, tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
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