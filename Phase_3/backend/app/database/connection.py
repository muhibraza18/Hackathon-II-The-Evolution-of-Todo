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
    
    This removes ALL query parameters and rebuilds with only what asyncpg needs.
    """
    print(f"🔍 Original URL received: {original_url}")
    
    # Extract the base URL without query parameters
    if '?' in original_url:
        base_url = original_url.split('?')[0]
        print(f"🔍 Base URL (before ?): {base_url}")
    else:
        base_url = original_url
    
    # Convert scheme to postgresql+asyncpg
    if base_url.startswith('postgres://'):
        base_url = base_url.replace('postgres://', 'postgresql+asyncpg://', 1)
    elif base_url.startswith('postgresql://'):
        base_url = base_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    elif base_url.startswith('postgresql+psycopg2://'):
        base_url = base_url.replace('postgresql+psycopg2://', 'postgresql+asyncpg://', 1)
    
    print(f"🔍 Base URL (after driver change): {base_url}")
    
    # Add only ssl=require (Neon requires SSL)
    clean_url = f"{base_url}?ssl=require"
    
    print(f"✅ Final clean URL: {clean_url}")
    
    return clean_url


# Build clean async URL
print("=" * 80)
print("🚀 Building async database URL...")
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