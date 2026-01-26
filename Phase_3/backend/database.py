from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost:5432/todo_chatbot")

# Convert to sync URL for compatibility with sqlmodel
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "+psycopg2").replace("asyncpg", "psycopg2")

# Create synchronous engine (to match main app approach)
engine = create_engine(
    SYNC_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Create session maker
SessionLocal = sessionmaker(engine, class_=Session)

def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency generator for database sessions.

    Yields a database session for use in FastAPI endpoints.
    """
    with SessionLocal() as session:
        yield session