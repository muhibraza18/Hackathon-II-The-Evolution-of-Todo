"""
Migration script for existing tasks to assign to default user
Used during the transition from unauthenticated to authenticated task system
"""

from sqlmodel import Session, select
from models import Task
from db import engine
import uuid

def migrate_existing_tasks():
    """
    Migrate existing tasks to be associated with a default user.
    In a real migration, you might create a proper user account,
    but for this demo we'll use a consistent user ID.
    """
    print("Starting task migration...")

    with Session(engine) as session:
        # Find all tasks without a proper user_id (or with the old test-user-1)
        # Note: We'll update any tasks that don't have a proper user_id
        statement = select(Task).where(Task.user_id == "test-user-1")
        tasks = session.exec(statement).all()

        if not tasks:
            # If no tasks with test-user-1, try to find any tasks at all
            statement = select(Task)
            tasks = session.exec(statement).all()

            if not tasks:
                print("No existing tasks found to migrate.")
                return

        print(f"Found {len(tasks)} tasks to migrate")

        # For this migration, we'll create a default user ID for existing tasks
        # In a real system, this would be a proper user account
        default_user_id = str(uuid.uuid4())  # Generate a unique ID
        print(f"Migrating tasks to user ID: {default_user_id}")

        for task in tasks:
            task.user_id = default_user_id
            session.add(task)

        session.commit()
        print(f"Successfully migrated {len(tasks)} tasks to user {default_user_id}")

if __name__ == "__main__":
    migrate_existing_tasks()