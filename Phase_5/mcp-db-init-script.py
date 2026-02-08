"""
Database initialization script for Todo AI Chatbot.

This script creates all required tables in the database using SQLModel.metadata.create_all.
"""

import asyncio
from sqlmodel import SQLModel
from app.database.connection import async_engine  # Use the async engine from the correct location
from app.database.models import Task, Conversation, Message


async def create_tables():
    """
    Create all tables in the database.
    """
    async with async_engine.begin() as conn:
        # This will create all tables defined in the models
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())