"""Basic functionality test for Todo Evolution Phase I.

This test verifies that the application module can be imported
and core functions work correctly.

Note: Unicode characters (checkmark, ballot box) may not display
correctly on Windows console due to encoding limitations.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import application
import main as todo_app

print("=" * 50)
print("Testing Todo Evolution - Phase I")
print("=" * 50)

# Test 1: Add task
print("\n[Test 1] Add Task")
try:
    task_id_1 = todo_app.add_task("Buy groceries", "Purchase milk, eggs, and bread")
    print("[PASS] Added task with ID: {}".format(task_id_1))
    assert task_id_1 == 1, "First task ID should be 1"
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 2: Add another task
print("\n[Test 2] Add Second Task")
try:
    task_id_2 = todo_app.add_task("Write report", "Complete quarterly sales analysis")
    print("[PASS] Added task with ID: {}".format(task_id_2))
    assert task_id_2 == 2, "Second task ID should be 2"
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 3: List tasks
print("\n[Test 3] List Tasks")
try:
    todo_app.list_tasks()
    assert len(todo_app.tasks) == 2, "Should have 2 tasks"
    print("[PASS] List tasks works correctly")
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 4: Toggle task status to complete
print("\n[Test 4] Mark Task Complete")
try:
    todo_app.toggle_task_status(1, True)
    assert todo_app.tasks[0]["complete"] == True, "Task 1 should be complete"
    print("[PASS] Task 1 marked as complete")
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 5: Update task
print("\n[Test 5] Update Task")
try:
    todo_app.update_task(1, "Buy groceries (updated)", None)
    assert todo_app.tasks[0]["title"] == "Buy groceries (updated)", "Title should be updated"
    print("[PASS] Task 1 title updated")
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 6: Delete task
print("\n[Test 6] Delete Task")
try:
    todo_app.delete_task(2)
    assert len(todo_app.tasks) == 1, "Should have 1 task after deletion"
    assert todo_app.tasks[0]["id"] == 1, "Remaining task should be ID 1"
    print("[PASS] Task 2 deleted successfully")
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

# Test 7: Validation - Empty title
print("\n[Test 7] Validation - Empty Title")
try:
    todo_app.add_task("", "Valid description")
    print("[FAIL] Should have raised ValueError for empty title")
    sys.exit(1)
except ValueError as e:
    if "empty" in str(e).lower():
        print("[PASS] Empty title rejected correctly: {}".format(e))
    else:
        print("[FAIL] Wrong error: {}".format(e))
        sys.exit(1)

# Test 8: Validation - Empty description
print("\n[Test 8] Validation - Empty Description")
try:
    todo_app.add_task("Valid title", "")
    print("[FAIL] Should have raised ValueError for empty description")
    sys.exit(1)
except ValueError as e:
    if "empty" in str(e).lower():
        print("[PASS] Empty description rejected correctly: {}".format(e))
    else:
        print("[FAIL] Wrong error: {}".format(e))
        sys.exit(1)

# Test 9: Task not found
print("\n[Test 9] Task Not Found")
try:
    todo_app.delete_task(999)
    print("[FAIL] Should have raised ValueError for non-existent task")
    sys.exit(1)
except ValueError as e:
    if "not found" in str(e).lower():
        print("[PASS] Non-existent task ID rejected correctly: {}".format(e))
    else:
        print("[FAIL] Wrong error: {}".format(e))
        sys.exit(1)

# Test 10: Final list
print("\n[Test 10] Final List")
try:
    todo_app.list_tasks()
    print("[PASS] Final list displays correctly")
except Exception as e:
    print("[FAIL] {}".format(e))
    sys.exit(1)

print("\n" + "=" * 50)
print("All tests passed!")
print("=" * 50)
print("\nFinal state: {} task(s)".format(len(todo_app.tasks)))
for task in todo_app.tasks:
    status = "X" if task["complete"] else "O"
    print("  [{}] ID {}: {}".format(status, task['id'], task['title']))
