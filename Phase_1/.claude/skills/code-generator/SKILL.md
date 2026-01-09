---
name: code-generator
description: Generates clean, modular Python code for the in-memory todo CLI app. Use when implementing features, writing functions, or building the main loop.
---
# Code Generator for Todo App

When generating code, always follow these rules:

1. Use an in-memory list of dictionaries for storage:
   tasks = [
       {"id": 1, "title": "Buy milk", "description": "From store", "complete": False}
   ]

2. Auto-generate unique IDs (use max(id) + 1 or len(tasks) + 1).

3. Write small, reusable functions:
   - add_task(title, description)
   - delete_task(task_id)
   - update_task(task_id, title=None, description=None)
   - list_tasks()
   - mark_complete(task_id, complete=True)

4. Main loop: Use a simple while True loop with input() and clear menu options (add, list, update, delete, complete, quit).

5. Handle errors gracefully (e.g., invalid ID, empty title).

6. Follow PEP8: clean variable names, docstrings, comments.

7. No external libraries except built-ins.

Keep code simple, readable, and ready to run.