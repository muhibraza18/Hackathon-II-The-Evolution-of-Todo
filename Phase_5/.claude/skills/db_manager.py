"""
Skill: Database Connection Manager
Purpose: Handle PostgreSQL connection and session management
Reusable: Yes - used by MCP tools and API endpoints
"""

from sqlmodel import create_engine, Session
from typing import Generator

class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
    
    def get_session(self) -> Generator[Session, None, None]:
        """Provides database session with automatic cleanup"""
        with Session(self.engine) as session:
            yield session