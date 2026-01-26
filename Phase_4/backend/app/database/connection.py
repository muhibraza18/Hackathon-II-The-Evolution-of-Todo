from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import asynccontextmanager
from ..config import settings

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
# ASYNC DATABASE SESSION (for MCP server)
# ============================================

def build_clean_asyncpg_url(original_url: str) -> str:
    """
    Build a clean asyncpg URL from the original database URL.

    FOR ASYNCPG IN KUBERNETES:
    - Removes any existing SSL parameters that are psycopg2-specific (sslmode, etc.)
    - asyncpg does NOT support sslmode parameter - only accepts ssl parameter
    - For local Kubernetes PostgreSQL, use no SSL parameters
    """
    print(f"[DEBUG] Original asyncpg URL received: {original_url}")

    # Parse the original URL to extract components
    base_url = original_url
    if '?' in original_url:
        base_url = original_url.split('?')[0]
        query_part = original_url.split('?')[1]

        # Parse existing query parameters and filter out psycopg2-specific ones
        params = []
        for param in query_part.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # Skip psycopg2-specific SSL parameters that asyncpg doesn't support
                if key.lower() not in ['sslmode', 'sslcert', 'sslkey', 'sslrootcert', 'sslfactory', 'sslcompression']:
                    params.append(f"{key}={value}")
            else:
                params.append(param)

        # Reconstruct the URL without unsupported asyncpg parameters
        if params:
            clean_url = f"{base_url}?{'&'.join(params)}"
        else:
            clean_url = base_url
    else:
        clean_url = original_url

    print(f"[SUCCESS] Clean asyncpg URL (without unsupported SSL params): {clean_url}")
    return clean_url


# Debug the database URL to see what it is
print(f"[DEBUG] Database URL in settings: {settings.database_url}")

# Only create async engine for PostgreSQL databases, not SQLite
# Check the original settings.database_url to determine if it's PostgreSQL
is_postgres = settings.database_url.startswith(("postgresql://", "postgres://", "postgresql+asyncpg://", "postgres+asyncpg://"))
print(f"[DEBUG] Is PostgreSQL URL? {is_postgres}")

if is_postgres:
    print("=" * 80)
    print("[INFO] Building async database URL...")
    database_url_async = build_clean_asyncpg_url(settings.database_url)
    print("=" * 80)

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
else:
    print("⚠️ Async engine skipped for non-PostgreSQL database")
    database_url_async = None
    async_engine = None
    async_session_maker = None


@asynccontextmanager
async def get_db_session_async():
    """
    Async context manager for database sessions.
    
    Used in MCP server and other async contexts.
    Usage: async with get_db_session_async() as session:
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()