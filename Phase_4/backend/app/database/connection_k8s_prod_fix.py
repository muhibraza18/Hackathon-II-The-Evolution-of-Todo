from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import asynccontextmanager
from ..config import settings
import logging
import re

# Set up logging
logger = logging.getLogger(__name__)

# Synchronous engine for FastAPI (existing)
database_url_sync = settings.database_url.replace("+asyncpg", "").replace("asyncpg", "psycopg2")

engine = create_engine(
    database_url_sync,
    echo=settings.log_level == "DEBUG",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)


def get_db_session() -> Generator[Session, None, None]:
    """
    Synchronous dependency generator for database sessions.

    Used in FastAPI endpoints.
    Yields a database session for use in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session


# ============================================
# ASYNC DATABASE SESSION (for MCP server in Kubernetes)
# ============================================

def build_clean_asyncpg_url(original_url: str) -> str:
    """
    Build a clean asyncpg URL from the original database URL.

    PRODUCTION FIX FOR KUBERNETES:
    - Always forces sslmode=disable for local PostgreSQL service
    - This is deterministic and safe for Kubernetes PostgreSQL services
    - Override any existing SSL settings to prevent conflicts
    """
    logger.info(f"🔧 MCP SERVER: Original URL received: {original_url}")

    # Parse the original URL to extract components
    if '?' in original_url:
        base_url = original_url.split('?')[0]
        query_part = original_url.split('?')[1]

        # Parse existing query parameters
        params = {}
        for param in query_part.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key.lower()] = value

        # Check if sslmode is already set - force override to 'disable' for Kubernetes
        if 'sslmode' in params:
            logger.info(f"🔒 MCP SERVER: sslmode already set to '{params['sslmode']}' - FORCING to 'disable' for Kubernetes")
            # Replace sslmode parameter with 'disable'
            updated_query = re.sub(r'sslmode=[^&]*', 'sslmode=disable', query_part, flags=re.IGNORECASE)
            clean_url = f"{base_url}?{updated_query}"
        else:
            # Add sslmode=disable to existing parameters
            clean_url = f"{base_url}?{query_part}&sslmode=disable"
    else:
        # No query parameters - add sslmode=disable
        clean_url = f"{original_url}?sslmode=disable"

    logger.info(f"✅ MCP SERVER: Final clean URL with sslmode=disable: {clean_url}")
    return clean_url


# Debug the database URL to see what it is
logger.info(f"🔧 MCP SERVER: Database URL in settings: {settings.database_url}")

# Only create async engine for PostgreSQL databases, not SQLite
is_postgres = settings.database_url.startswith((
    "postgresql://", "postgres://",
    "postgresql+asyncpg://", "postgres+asyncpg://",
    "postgresql+psycopg2://", "postgres+psycopg2://"
))

logger.info(f"🔍 MCP SERVER: Is PostgreSQL URL? {is_postgres}")

# Initialize async components
async_engine = None
async_session_maker = None
database_url_async = None

if is_postgres:
    logger.info("=" * 80)
    logger.info("🚀 MCP SERVER: Building async database URL with forced SSL disabled...")
    database_url_async = build_clean_asyncpg_url(settings.database_url)
    logger.info("=" * 80)

    async_engine = create_async_engine(
        database_url_async,
        echo=settings.log_level == "DEBUG",
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        future=True
    )

    # Create async session maker
    async_session_maker = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    logger.info("✅ MCP SERVER: Async engine and session maker initialized with sslmode=disable")
else:
    logger.warning("⚠️  MCP SERVER: Async engine skipped for non-PostgreSQL database")


@asynccontextmanager
async def get_db_session_async():
    """
    Async context manager for database sessions.

    Used in MCP server and other async contexts.
    Usage: async with get_db_session_async() as session:
    """
    if async_session_maker is None:
        raise RuntimeError("MCP SERVER: Async session maker not initialized - database not available")

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            logger.error("MCP SERVER: Database transaction rolled back due to error")
            raise
        finally:
            await session.close()


# Export for use in other modules
__all__ = [
    "engine",
    "get_db_session",
    "get_db_session_async",
    "build_clean_asyncpg_url",
    "async_engine",
    "async_session_maker"
]