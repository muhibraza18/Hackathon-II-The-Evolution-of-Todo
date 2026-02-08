#!/usr/bin/env python3
"""
Create database tables in Neon PostgreSQL
"""
import asyncio
from app.database.connection import async_session_maker
from sqlmodel import SQLModel
from app.database.models import User, SessionModel, Task, Conversation, Message


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")

    # Import all models to ensure they're registered
    from app.database.models import User, SessionModel, Task, Conversation, Message

    # Create all tables
    async with async_session_maker() as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(lambda connection: SQLModel.metadata.create_all(connection, checkfirst=True))

    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
