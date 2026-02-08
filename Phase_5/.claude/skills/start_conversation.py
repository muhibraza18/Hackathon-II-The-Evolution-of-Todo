"""
Skill: Add Task
Purpose: Create a new task for a given user
Reusable: Yes - core CRUD operation
"""

from typing import Dict, Any
from datetime import datetime

class AddTask:
    """Handles creation of new tasks"""

    @staticmethod
    def create_task(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
        """
        Creates a new task entry
        """
        # Normally this would insert into Neon DB
        return {
            "task_id": 1,  # placeholder
            "user_id": user_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }
