"""
Database Connection Setup
Task CRUD Operations with Proper Connection Pooling
"""

import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from typing import Generator

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Configure connection arguments based on database type
connect_args = {}

# For PostgreSQL/NeonDB, add connection pooling and keepalive settings
if "postgresql" in DATABASE_URL or "neon" in DATABASE_URL:
    connect_args = {
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
    
    # Ensure SSL is enabled for NeonDB
    if "neon" in DATABASE_URL or "amazonaws" in DATABASE_URL:
        connect_args["sslmode"] = "require"

# Create database engine with proper connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args,
    pool_pre_ping=True,      # Test connections before using them (fixes SSL errors)
    pool_size=10,             # Number of connections to keep open
    max_overflow=20,          # Maximum number of connections that can be created beyond pool_size
    pool_recycle=3600,        # Recycle connections after 1 hour (3600 seconds)
)


def create_db_and_tables():
    """
    Create all database tables defined in the models
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Generator for database sessions.
    
    This function is designed to work as a FastAPI dependency.
    Ensures proper session lifecycle management and handles connection errors.
    """
    with Session(engine) as session:
        yield session