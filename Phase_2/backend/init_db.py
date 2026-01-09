"""
Database Initialization Script
Task CRUD Operations with Authentication (JWT Version)
"""

from sqlmodel import SQLModel
from models import Task
from db import engine


def create_db_and_tables():
    """
    Create database tables.

    This function creates all tables defined in the SQLModel metadata.
    In this phase, it creates the tasks table with user_id for authentication.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()