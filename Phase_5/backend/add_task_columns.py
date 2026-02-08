#!/usr/bin/env python3
"""
Add missing columns to the task table in Neon PostgreSQL
"""
import asyncio
from app.database.connection import async_session_maker
from sqlalchemy import text

async def add_missing_columns():
    """Add missing columns to the task table"""
    print("Adding missing columns to task table...")

    async with async_session_maker() as session:
        async with session.begin() as conn:
            # Check current columns
            result = await conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'task'
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"Existing columns: {existing_columns}")

            # Add missing columns
            columns_to_add = [
                ("due_date", "TIMESTAMP"),
                ("priority", "VARCHAR(20)"),
                ("tags", "VARCHAR(1000)"),
                ("recurring_config", "VARCHAR(1000)"),
                ("next_occurrence_id", "VARCHAR(100)"),
                ("parent_task_id", "INTEGER"),
                ("original_task_id", "INTEGER"),
            ]

            for column_name, column_type in columns_to_add:
                if column_name not in existing_columns:
                    print(f"Adding column: {column_name}")
                    if column_name in ["parent_task_id", "original_task_id"]:
                        # Add foreign key columns
                        await conn.execute(text(f"""
                            ALTER TABLE task
                            ADD COLUMN {column_name} {column_type} REFERENCES task(id)
                        """))
                        # Add index
                        await conn.execute(text(f"""
                            CREATE INDEX IF NOT EXISTS ix_task_{column_name}
                            ON task({column_name})
                        """))
                    else:
                        # Add regular columns
                        await conn.execute(text(f"""
                            ALTER TABLE task
                            ADD COLUMN {column_name} {column_type}
                        """))
                        # Add index for some columns
                        if column_name in ["due_date", "priority", "next_occurrence_id"]:
                            await conn.execute(text(f"""
                                CREATE INDEX IF NOT EXISTS ix_task_{column_name}
                                ON task({column_name})
                            """))
                    print(f"  ✓ Added {column_name}")
                else:
                    print(f"  ⊙ {column_name} already exists, skipping")

            # Verify columns were added
            result = await conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'task'
            """))
            new_columns = [row[0] for row in result.fetchall()]
            print(f"\nUpdated columns: {new_columns}")

    print("\n✅ Database columns added successfully!")

if __name__ == "__main__":
    asyncio.run(add_missing_columns())
