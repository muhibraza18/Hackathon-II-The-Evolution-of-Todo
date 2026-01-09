"""Todo Evolution - Phase I: In-Memory CLI Todo Application.

A command-line interface todo application demonstrating agentic development
workflows through spec-driven development using Claude Code agents.
"""

from __future__ import annotations

# In-memory task storage
tasks: list[dict] = []

# ID counter for unique IDs
_next_id: int = 1


def _get_next_id() -> int:
    """Get the next available task ID.

    Returns:
        int: The next unique ID.
    """
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


def _find_task_by_id(task_id: int) -> dict | None:
    """Find a task by its ID.

    Args:
        task_id: The ID of the task to find.

    Returns:
        The task dictionary if found, None otherwise.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def _validate_title(title: str) -> None:
    """Validate task title.

    Args:
        title: The title to validate.

    Raises:
        ValueError: If title is invalid.
    """
    if not title or title.strip() == "":
        raise ValueError("Error: Title cannot be empty")
    if len(title) > 100:
        raise ValueError("Error: Title must be 100 characters or less")


def _validate_description(description: str) -> None:
    """Validate task description.

    Args:
        description: The description to validate.

    Raises:
        ValueError: If description is invalid.
    """
    if not description or description.strip() == "":
        raise ValueError("Error: Description cannot be empty")
    if len(description) > 500:
        raise ValueError("Error: Description must be 500 characters or less")


def add_task(title: str, description: str) -> int:
    """Add a new task.

    Args:
        title: Task title (non-empty, max 100 chars).
        description: Task description (non-empty, max 500 chars).

    Returns:
        int: ID of created task.

    Raises:
        ValueError: If title or description is invalid.
    """
    _validate_title(title)
    _validate_description(description)

    task_id = _get_next_id()
    task = {
        "id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "complete": False,
    }
    tasks.append(task)
    return task_id


def list_tasks() -> None:
    """Display all tasks with their status."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
    print("=" * 70)

    for task in tasks:
        status_icon = "✓" if task["complete"] else "☐"
        title = task["title"][:27] + "..." if len(task["title"]) > 30 else task["title"]
        desc = task["description"][:20] + "..." if len(task["description"]) > 23 else task["description"]
        print(f"{task['id']:<4} {status_icon:<8} {title:<30} {desc}")

    print("=" * 70)
    print(f"\nTotal: {len(tasks)} task{'s' if len(tasks) != 1 else ''}")


def update_task(task_id: int, title: str = None, description: str = None) -> None:
    """Update a task's title and/or description.

    Args:
        task_id: ID of task to update.
        title: New title (optional).
        description: New description (optional).

    Raises:
        ValueError: If task_id not found or no fields provided.
    """
    if title is None and description is None:
        raise ValueError("Error: At least one field must be provided")

    task = _find_task_by_id(task_id)
    if task is None:
        raise ValueError(f"Error: Task {task_id} not found")

    if title is not None:
        _validate_title(title)
        task["title"] = title.strip()

    if description is not None:
        _validate_description(description)
        task["description"] = description.strip()


def delete_task(task_id: int) -> None:
    """Delete a task by ID.

    Args:
        task_id: ID of task to delete.

    Raises:
        ValueError: If task_id not found.
    """
    task = _find_task_by_id(task_id)
    if task is None:
        raise ValueError(f"Error: Task {task_id} not found")

    tasks.remove(task)


def toggle_task_status(task_id: int, complete: bool) -> None:
    """Mark a task as complete or incomplete.

    Args:
        task_id: ID of task to update.
        complete: True to mark complete, False for incomplete.

    Raises:
        ValueError: If task_id not found.
    """
    task = _find_task_by_id(task_id)
    if task is None:
        raise ValueError(f"Error: Task {task_id} not found")

    task["complete"] = complete


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("    Todo Evolution - Phase I")
    print("=" * 50)
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Help")
    print("7. Exit")
    print("=" * 50)


def show_help() -> None:
    """Display help information."""
    print("\n" + "=" * 50)
    print("    Help - Todo Evolution")
    print("=" * 50)
    print("1. Add Task       - Create a new task")
    print("2. List Tasks     - View all tasks")
    print("3. Update Task    - Modify task title/description")
    print("4. Delete Task    - Remove a task")
    print("5. Mark Status    - Mark complete/incomplete")
    print("6. Help           - Show this help text")
    print("7. Exit           - Exit the application")
    print("=" * 50)
    print("\nTask IDs are unique and never reused.")
    print("Data is stored in memory only (lost on exit).")
    print("=" * 50 + "\n")


def _get_menu_choice() -> int:
    """Get and validate menu choice from user.

    Returns:
        int: Valid menu choice (1-7).
    """
    while True:
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            if choice == "":
                raise ValueError("Error: Please enter a number between 1 and 7")

            choice_num = int(choice)
            if 1 <= choice_num <= 7:
                return choice_num
            raise ValueError("Error: Please enter a number between 1 and 7")
        except ValueError as e:
            if str(e).startswith("Error:"):
                print(e)
            else:
                print("Error: Please enter a valid number (1-7)")


def _get_task_id(prompt: str = "Enter task ID: ") -> int:
    """Get task ID from user with validation.

    Args:
        prompt: The prompt to display.

    Returns:
        int: Valid task ID.
    """
    while True:
        try:
            task_id = input(prompt).strip()
            return int(task_id)
        except ValueError:
            print("Error: Please enter a valid number")


def _confirm_action(action: str, details: str) -> bool:
    """Get user confirmation for an action.

    Args:
        action: The action being confirmed.
        details: Details of what will happen.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    while True:
        choice = input(f"\n{details}\nConfirm? (y/n): ").strip().lower()
        if choice == "y":
            return True
        if choice == "n":
            return False
        print("Error: Please enter 'y' or 'n'")


def route_to_function(choice: int) -> None:
    """Route menu choice to appropriate function.

    Args:
        choice: The user's menu choice.
    """
    try:
        if choice == 1:
            # Add Task
            print("\n--- Add Task ---")
            title = input("Enter task title: ").strip()
            description = input("Enter task description: ").strip()

            task_id = add_task(title, description)
            print(f"\n✓ Task added successfully (ID: {task_id})")

        elif choice == 2:
            # List Tasks
            print("\n--- List Tasks ---")
            list_tasks()

        elif choice == 3:
            # Update Task
            print("\n--- Update Task ---")
            list_tasks()
            task_id = _get_task_id("Enter task ID to update: ")

            print("\nLeave blank to keep current value")
            title = input("Enter new title: ").strip() or None
            description = input("Enter new description: ").strip() or None

            update_task(task_id, title, description)
            print(f"\n✓ Task {task_id} updated")

        elif choice == 4:
            # Delete Task
            print("\n--- Delete Task ---")
            list_tasks()
            task_id = _get_task_id("Enter task ID to delete: ")

            task = _find_task_by_id(task_id)
            if task:
                details = f"Delete task: {task['title']}"
                if _confirm_action("Delete", details):
                    delete_task(task_id)
                    print(f"\n✓ Task {task_id} deleted")
                else:
                    print("\nDelete cancelled")

        elif choice == 5:
            # Mark Complete/Incomplete
            print("\n--- Mark Complete/Incomplete ---")
            list_tasks()
            task_id = _get_task_id("Enter task ID: ")

            while True:
                choice = input("Mark as (c)omplete or (i)ncomplete: ").strip().lower()
                if choice == "c":
                    toggle_task_status(task_id, True)
                    print(f"\n✓ Task {task_id} marked as complete")
                    break
                if choice == "i":
                    toggle_task_status(task_id, False)
                    print(f"\n✓ Task {task_id} marked as incomplete")
                    break
                print("Error: Please enter 'c' or 'i'")

        elif choice == 6:
            # Help
            show_help()

        elif choice == 7:
            # Exit
            print("\nThank you for using Todo Evolution!")
            exit()

    except ValueError as e:
        print(f"\n{e}")


def main() -> None:
    """Main entry point for the application."""
    print("\n" + "=" * 50)
    print("    Todo Evolution - Phase I")
    print("    In-Memory CLI Todo Application")
    print("=" * 50)

    while True:
        display_menu()
        choice = _get_menu_choice()
        route_to_function(choice)


if __name__ == "__main__":
    main()
