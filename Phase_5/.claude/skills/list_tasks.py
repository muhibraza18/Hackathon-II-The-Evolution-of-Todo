"""
Skill: List Tasks
Purpose: Retrieve tasks for a user
Reusable: Yes - used across chatbot and API
"""

from typing import List, Dict

class ListTasks:
    """Lists tasks for a given user"""

    @staticmethod
    def get_tasks(user_id: str, status: str = "all") -> List[Dict]:
        """
        Returns tasks filtered by status
        """
        # Placeholder data
        tasks = [
            {"id": 1, "title": "Buy groceries", "completed": False},
            {"id": 2, "title": "Call mom", "completed": True}
        ]
        if status == "pending":
            return [t for t in tasks if not t["completed"]]
        elif status == "completed":
            return [t for t in tasks if t["completed"]]
        return tasks
