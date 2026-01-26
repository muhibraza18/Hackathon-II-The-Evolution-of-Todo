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

    This preserves existing SSL parameters and only adds them for cloud providers.
    For local development, avoid forcing SSL.
    """
    print(f"🔍 Original URL received: {original_url}")

    # Check if the original URL already has SSL-related parameters
    has_ssl_param = any(param in original_url.lower() for param in ['ssl=', 'sslmode='])

    if has_ssl_param:
        # If SSL parameters already exist in the URL, preserve them
        clean_url = original_url
        print("🔓 SSL parameters already in URL - preserving original settings")
    else:
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

        # Check if this is a Neon database (has "neon" in the URL) or other cloud providers
        # Only add SSL parameters for cloud providers, not for local development
        is_cloud_db = ("neon" in original_url.lower() or
                       "aws" in original_url.lower() or
                       "azure" in original_url.lower() or
                       "gcp" in original_url.lower() or
                       "supabase" in original_url.lower() or
                       "heroku" in original_url.lower() or
                       "digitalocean" in original_url.lower())

        if is_cloud_db:
            # Add ssl=require for cloud databases
            clean_url = f"{base_url}?ssl=require"
            print("🔒 Cloud database detected - forcing SSL requirement")
        else:
            # For local development, don't force SSL
            clean_url = base_url
            print("🔓 Local development database detected - not forcing SSL")

    print(f"✅ Final clean URL: {clean_url}")

    return clean_url


# Debug the database URL to see what it is
print(f"🔍 Database URL in settings: {settings.database_url}")

# Only create async engine for PostgreSQL databases, not SQLite
# Check the original settings.database_url to determine if it's PostgreSQL
is_postgres = settings.database_url.startswith(("postgresql://", "postgres://", "postgresql+asyncpg://", "postgres+asyncpg://"))
print(f"🔍 Is PostgreSQL URL? {is_postgres}")

if is_postgres:
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