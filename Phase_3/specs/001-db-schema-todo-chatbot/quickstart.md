# Quickstart Guide: Database Schema for Todo AI Chatbot

**Feature**: Database Schema for Todo AI Chatbot
**Date**: 2026-01-13
**Status**: Draft

## Overview

This guide provides quick instructions for setting up and using the database schema for the Todo AI Chatbot. The schema consists of three main entities: Task, Conversation, and Message, all designed to work with PostgreSQL and SQLModel.

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)
- SQLModel installed
- Environment variables configured

## Installation

### 1. Install Dependencies

```bash
pip install sqlmodel asyncpg python-dotenv
```

### 2. Environment Configuration

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
POOL_MIN_SIZE=1
POOL_MAX_SIZE=16
```

## Database Setup

### 1. Initialize Database Models

Create your `models.py` file with the following structure:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Conversation

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # Only "user" or "assistant"
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

### 2. Create Database Engine and Session

Create your `database.py` file:

```python
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine
engine = create_async_engine(DATABASE_URL)

# Create async session maker
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### 3. Initialize Database Tables

To create the tables in your database:

```python
from sqlmodel import SQLModel
from database import engine
from models import Task, Conversation, Message  # Import your models

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

## Basic Usage Examples

### 1. Create a Task

```python
from models import Task
from database import get_db_session

async def create_task(user_id: str, title: str, description: str = None):
    async with get_db_session() as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
```

### 2. Create a Conversation

```python
from models import Conversation

async def create_conversation(user_id: str):
    async with get_db_session() as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation
```

### 3. Create a Message

```python
from models import Message

async def create_message(user_id: str, conversation_id: int, role: str, content: str):
    async with get_db_session() as session:
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
```

### 4. Query Tasks for a User

```python
from sqlmodel import select
from models import Task

async def get_user_tasks(user_id: str, completed: bool = None):
    async with get_db_session() as session:
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        result = await session.execute(query)
        return result.scalars().all()
```

### 5. Get Conversation with Messages

```python
from sqlmodel import select
from models import Conversation

async def get_conversation_with_messages(conversation_id: int, user_id: str):
    async with get_db_session() as session:
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
```

## Testing Your Setup

### 1. Basic Connection Test

```python
import asyncio
from database import engine

async def test_connection():
    try:
        async with engine.connect() as conn:
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Run the test
asyncio.run(test_connection())
```

### 2. Create Sample Data

```python
import asyncio

async def create_sample_data():
    # Create a user
    user_id = "user_123"

    # Create a conversation
    conversation = await create_conversation(user_id)
    print(f"Created conversation: {conversation.id}")

    # Create some messages
    msg1 = await create_message(user_id, conversation.id, "user", "I need to buy groceries")
    msg2 = await create_message(user_id, conversation.id, "assistant", "Sure, I can add that as a task for you")
    print(f"Created messages: {msg1.id}, {msg2.id}")

    # Create a task
    task = await create_task(user_id, "Buy groceries", "Milk, eggs, bread")
    print(f"Created task: {task.id}")

# Run the sample
asyncio.run(create_sample_data())
```

## Running Migrations

For the initial setup, use the create_tables function above. As your application grows, consider implementing Alembic for more sophisticated migration management:

```bash
pip install alembic
alembic init alembic
```

Then configure alembic.ini to work with your async database setup.

## Error Handling

Always wrap database operations in try-catch blocks:

```python
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager

async def safe_create_task(user_id: str, title: str):
    try:
        return await create_task(user_id, title)
    except IntegrityError as e:
        print(f"Database integrity error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Next Steps

1. Implement the CRUD operations for each entity
2. Add proper validation and error handling
3. Create API endpoints that use these models
4. Implement the MCP tools that interact with these models
5. Add comprehensive tests for all operations