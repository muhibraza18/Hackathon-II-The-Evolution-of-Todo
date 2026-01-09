# Implementation Plan: Todo Evolution - Phase I

## 1. Architecture Sketch

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Console Input)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    main() - Entry Point                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  while True:                                          │  │
│  │    display_menu()                                    │  │
│  │    choice = get_user_input()                         │  │
│  │    route_to_function(choice)                          │  │
│  └──────────────────────────────────────────────────────┘  │
└───┬─────────────────┬───────────────┬───────────────────┬────┘
    │                 │               │                   │
    ▼                 ▼               ▼                   ▼
┌───────────┐  ┌───────────┐  ┌───────────┐      ┌───────────┐
│ add_task  │  │ update_   │  │ delete_   │      │ display_  │
│   ()      │  │ task()    │  │  task()   │      │  tasks()  │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘      └─────┬─────┘
      │              │              │                  │
      └──────────────┼──────────────┼──────────────────┘
                     │              │
                     ▼              ▼
              ┌─────────────────────────────┐
              │      tasks = []              │
              │  (Global in-memory list)     │
              │  [{"id": 1, "title": "...",  │
              │    "description": "...",    │
              │    "complete": False}]       │
              └─────────────────────────────┘
```

### Data Flow

1. User inputs command choice via console
2. `main()` validates and routes to appropriate function
3. Function reads from/writes to global `tasks` list
4. Function returns result to `main()` for display
5. Loop continues until user exits

---

## 2. Project Structure

```
phase_1/
├── constitution.md              # Project constitution (EXISTS)
├── CLAUDE.md                     # Global Claude Code instructions
├── README.md                     # Setup and usage documentation
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Python project configuration
├── uv.lock                      # UV lock file (auto-generated)
│
├── specs/
│   ├── initial-spec.md          # Original specification (EXISTS)
│   ├── implementation-plan.md   # This file
│   └── history/                 # Specification iterations
│       ├── v1.0-spec.md         # Archive of initial-spec.md
│       └── v1.1-spec.md         # Future iterations (as needed)
│
└── src/
    ├── __init__.py              # Package marker
    └── main.py                  # Application entry point (ALL CODE)
```

---

## 3. Phased Task List

### Phase 1: Data Model and Core Functions

| Priority | Task | Description | Deliverable | Verification |
|----------|------|-------------|-------------|--------------|
| HIGH | 1.1 | Create project structure | Directory tree, empty files | All directories and files exist |
| HIGH | 1.2 | Initialize UV environment | `pyproject.toml`, `uv init` | `uv run python --version` works |
| HIGH | 1.3 | Define task data structure | Task dictionary template | Matches spec exactly |
| HIGH | 1.4 | Implement `add_task()` function | Adds task to global list | Can add task, ID auto-increments |
| HIGH | 1.5 | Implement `display_tasks()` function | Lists all tasks with status | Shows all fields, correct status icon |
| HIGH | 1.6 | Implement `toggle_task_status()` function | Marks complete/incomplete | Status toggles correctly |

**Dependencies**: 1.1 → 1.2 → 1.3 → 1.4, 1.5, 1.6 (parallel)

---

### Phase 2: Update and Delete Operations

| Priority | Task | Description | Deliverable | Verification |
|----------|------|-------------|-------------|--------------|
| HIGH | 2.1 | Implement `update_task()` function | Updates title and/or description | Updates one or both fields correctly |
| HIGH | 2.2 | Implement `delete_task()` function | Removes task by ID | Task removed, IDs don't shift |
| MEDIUM | 2.3 | Add input validation for all functions | Validates ID exists, fields not empty | Invalid inputs rejected with clear errors |

**Dependencies**: Phase 1 complete → 2.1, 2.2 (parallel) → 2.3

---

### Phase 3: Main CLI Loop and User Interaction

| Priority | Task | Description | Deliverable | Verification |
|----------|------|-------------|-------------|--------------|
| HIGH | 3.1 | Implement `display_menu()` function | Shows numbered options | All 6 options visible (5 features + exit) |
| HIGH | 3.2 | Implement `get_user_input()` function | Gets and validates menu choice | Accepts 1-6, rejects others |
| HIGH | 3.3 | Implement `route_to_function()` function | Maps choices to functions | All routes work correctly |
| HIGH | 3.4 | Implement `main()` function with loop | Main event loop | Program starts, runs, exits cleanly |
| MEDIUM | 3.5 | Implement `show_help()` function | Displays command reference | Shows all available commands |

**Dependencies**: Phase 1-2 complete → 3.1, 3.2, 3.3, 3.5 (parallel) → 3.4

---

### Phase 4: Polish, Error Handling, and Final Demo Flow

| Priority | Task | Description | Deliverable | Verification |
|----------|------|-------------|-------------|--------------|
| HIGH | 4.1 | Add comprehensive error handling | Try/except blocks, error messages | No uncaught exceptions |
| HIGH | 4.2 | Validate empty/whitespace input | Strips and checks fields | Whitespace-only strings rejected |
| HIGH | 4.3 | Handle invalid task IDs | Check ID exists before operations | Clear error for non-existent IDs |
| MEDIUM | 4.4 | Add confirmations for destructive ops | Confirm before delete/update | User can cancel deletions |
| LOW | 4.5 | Add task count summary | Show "X tasks total" | Visible in list output |
| MEDIUM | 4.6 | Refine output formatting | Consistent spacing, alignment | Professional appearance |

**Dependencies**: Phase 3 complete → 4.1, 4.2, 4.3, 4.4, 4.6 (parallel) → 4.5

---

### Phase 5: Documentation and Verification

| Priority | Task | Description | Deliverable | Verification |
|----------|------|-------------|-------------|--------------|
| HIGH | 5.1 | Create README.md | Setup, usage, examples | All sections present, accurate |
| HIGH | 5.2 | Create CLAUDE.md | Global agent instructions | Contains workflow guidance |
| HIGH | 5.3 | Create .gitignore | Python, UV, OS files | All patterns present |
| HIGH | 5.4 | Run PEP8 check | `ruff check` or similar | No linting errors |
| HIGH | 5.5 | Manual testing - all 5 features | Execute test checklist | All tests pass |
| HIGH | 5.6 | Archive spec v1.0 to history/ | Copy initial-spec.md | File exists in history/ |
| MEDIUM | 5.7 | Final demo walkthrough | Run complete session | Demo script prepared |

**Dependencies**: Phase 4 complete → 5.1, 5.2, 5.3 (parallel) → 5.4, 5.5, 5.6 (parallel) → 5.7

---

## 4. Decision Log

### Decision 4.1: Code Organization (Single File vs Modules)

**Context**: Project is small enough for a single file, but good practice suggests modularity.

**Options**:
1. **Single file** (`src/main.py` only)
   - ✅ Simpler for small project
   - ✅ Easy to read end-to-end
   - ✅ No import complexity
   - ❌ Less scalable
   - ❌ Harder to test individual functions

2. **Multiple modules** (`src/main.py`, `src/task_manager.py`, `src/ui.py`)
   - ✅ Better separation of concerns
   - ✅ More testable
   - ✅ Scalable
   - ❌ Overkill for this phase
   - ❌ More files to manage
   - ❌ Import overhead

3. **Hybrid** (Single file with clear function sections)
   - ✅ Single file simplicity
   - ✅ Logical grouping with comments
   - ✅ Functions are testable in isolation
   - ✅ Scalable to modules later
   - ❌ File may grow large

**Selected Choice**: **Option 3 - Hybrid (Single file with sections)**

**Rationale**:
- Phase I scope is intentionally small
- Single file demonstrates simplicity
- Clear sections with comments provide structure
- Easy to extract to modules in Phase II if needed
- Meets hackathon time constraints

**Tradeoffs Accepted**:
- File will be ~200-300 lines (acceptable)
- Less formal separation than modules
- Test harness will import and test functions directly

---

### Decision 4.2: ID Generation Method

**Context**: Need unique, sequential IDs for tasks.

**Options**:
1. **Auto-increment from counter**
   ```python
   _next_id = 1
   def _get_next_id():
       global _next_id
       id = _next_id
       _next_id += 1
       return id
   ```
   - ✅ Simple, predictable
   - ✅ IDs never reused
   - ✅ No gaps
   - ❌ Gaps if tasks deleted

2. **Max ID + 1**
   ```python
   def _get_next_id():
       if not tasks:
           return 1
       return max(t["id"] for t in tasks) + 1
   ```
   - ✅ Reuses "gaps" after deletion
   - ✅ Always finds next available
   - ❌ O(n) scan each time
   - ❌ Could reuse IDs from deleted tasks

3. **Length of list + 1**
   ```python
   def _get_next_id():
       return len(tasks) + 1
   ```
   - ✅ Very simple
   - ✅ O(1) operation
   - ❌ IDs shift when tasks deleted
   - ❌ Confusing for users (IDs change)

**Selected Choice**: **Option 1 - Auto-increment from counter**

**Rationale**:
- Users expect stable IDs
- O(1) operation is efficient
- Gaps after deletion are acceptable for this phase
- Simplest for users to understand
- Matches common todo app patterns

**Tradeoffs Accepted**:
- IDs not reused (gaps appear after deletions)
- Counter must persist (simple global variable)

---

### Decision 4.3: Menu Design (Numbered vs Text Commands)

**Context**: How users interact with the CLI.

**Options**:
1. **Numbered menu**
   ```
   1. Add Task
   2. List Tasks
   3. Update Task
   4. Delete Task
   5. Mark Complete/Incomplete
   6. Exit
   Enter choice (1-6):
   ```
   - ✅ Simple input (single digit)
   - ✅ Easy to parse
   - ✅ No typos possible
   - ❌ Less memorable
   - ❌ Need to reference menu each time

2. **Text commands**
   ```
   Commands: add, list, update, delete, complete, exit
   Enter command:
   ```
   - ✅ More discoverable
   - ✅ Memorable for power users
   - ✅ Natural language feel
   - ❌ Typo-prone
   - ❌ Case sensitivity issues

3. **Both (numbered with aliases)**
   ```
   1. Add Task (add)
   2. List Tasks (list)
   ...
   Enter choice (1-6 or command name):
   ```
   - ✅ Best of both worlds
   - ✅ Beginner and power user friendly
   - ❌ More complex parsing
   - ❌ More code

**Selected Choice**: **Option 1 - Numbered menu**

**Rationale**:
- Hackathon demo needs clear, foolproof UX
- Beginners prefer numbered options
- Simpler implementation
- Less error-prone for demo
- Help command can show numbered options

**Tradeoffs Accepted**:
- Users must reference menu
- Less "pro" feel
- Not as memorable

---

### Decision 4.4: Error Handling Approach (Exceptions vs Return Codes)

**Context**: How to handle errors in functions.

**Options**:
1. **Exceptions with try/except**
   ```python
   def delete_task(task_id):
       task = find_task(task_id)
       if not task:
           raise ValueError(f"Task {task_id} not found")
   ```
   - ✅ Pythonic approach
   - ✅ Forces handling
   - ✅ Stack traces for debugging
   - ❌ Can be verbose
   - ❌ May confuse non-programmers

2. **Return tuples (success, message)**
   ```python
   def delete_task(task_id):
       task = find_task(task_id)
       if not task:
           return (False, f"Task {task_id} not found")
       return (True, "Task deleted")
   ```
   - ✅ Explicit error checking
   - ✅ Control flow clear
   - ✅ No exceptions to catch
   - ❌ Boilerplate
   - ❌ Easy to ignore errors

3. **Print errors and return None**
   ```python
   def delete_task(task_id):
       task = find_task(task_id)
       if not task:
           print(f"Error: Task {task_id} not found")
           return None
   ```
   - ✅ Simplest
   - ✅ User sees error immediately
   - ❌ Side effects in pure functions
   - ❌ Not testable (print statements)

**Selected Choice**: **Option 1 - Exceptions with try/except**

**Rationale**:
- Pythonic and standard practice
- Forces proper error handling
- Easier to test (exceptions in tests)
- Clear separation of concerns
- Main loop can catch and display user-friendly messages

**Tradeoffs Accepted**:
- More code than Option 3
- Need to educate judges on exceptions (explain in demo)

---

### Decision 4.5: Input Validation Timing

**Context**: When to validate user input.

**Options**:
1. **Validate at collection time**
   - Validate as soon as user enters data
   - Reject and ask again immediately
   - ✅ Immediate feedback
   - ✅ Don't store invalid data
   - ❌ More rounds of input
   - ❌ Can be annoying

2. **Validate at function time**
   - Collect all input, pass to function
   - Function validates and rejects
   - ✅ Simpler collection loop
   - ✅ One validation point
   - ❌ Late feedback
   - ❌ May need to re-enter all data

3. **Validate both**
   - Basic validation at collection (not empty)
   - Full validation at function (ID exists, etc.)
   - ✅ Best of both worlds
   - ✅ Prevents obvious errors early
   - ✅ Context-specific validation later
   - ❌ More code
   - ❌ Duplicate validation logic

**Selected Choice**: **Option 3 - Validate both**

**Rationale**:
- Prevent obvious errors early (empty strings)
- Context-specific validation in functions (ID exists)
- Good UX (immediate feedback on basic errors)
- Clear error messages from functions
- Robust overall

**Tradeoffs Accepted**:
- More validation code
- Slight duplication

---

## 5. Manual Testing Checklist

### 5.1 Feature: Add Task

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Normal add | Title: "Buy milk", Description: "2 cartons" | Success message, task added with ID 1, status ☐ | ☐ |
| Whitespace title | Title: "   ", Description: "Valid desc" | Error: Title cannot be empty | ☐ |
| Whitespace description | Title: "Valid title", Description: "   " | Error: Description cannot be empty | ☐ |
| Long title | Title: 101+ chars, Description: "Valid" | Error: Title too long (max 100) | ☐ |
| Long description | Title: "Valid", Description: 501+ chars | Error: Description too long (max 500) | ☐ |
| Multiple adds | Add 3 tasks | IDs: 1, 2, 3 in order | ☐ |

---

### 5.2 Feature: List Tasks

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Empty list | List tasks with no tasks | "No tasks found" message | ☐ |
| Single task | Add 1 task, list | Shows ID, title, ☐, description | ☐ |
| Multiple tasks | Add 3 tasks, list | Shows all 3 tasks in order | ☐ |
| Mixed status | 2 complete, 1 incomplete, list | Shows ✓ and ☐ correctly | ☐ |
| Task count | Add 3 tasks, list | Shows "3 tasks total" | ☐ |

---

### 5.3 Feature: Update Task

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Update title only | ID: 1, New title: "Updated" | Title changed, description unchanged | ☐ |
| Update description only | ID: 1, New desc: "New desc" | Description changed, title unchanged | ☐ |
| Update both | ID: 1, New title: "A", New desc: "B" | Both fields updated | ☐ |
| Invalid ID | ID: 999, Title: "Test" | Error: Task not found | ☐ |
| Empty update | ID: 1, No new values | Error: At least one field required | ☐ |
| Whitespace update | ID: 1, Title: "   " | Error: Cannot be empty | ☐ |

---

### 5.4 Feature: Delete Task

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Delete existing | ID: 1 (exists) | Task removed, confirmation shown | ☐ |
| Delete non-existent | ID: 999 | Error: Task not found | ☐ |
| Delete with confirmation | ID: 1, confirm "y" | Task deleted | ☐ |
| Delete cancel | ID: 1, confirm "n" | Task not deleted | ☐ |
| Delete middle ID | Add tasks 1,2,3, delete 2 | Tasks 1,3 remain, ID 2 gone (gap) | ☐ |
| Delete from empty | No tasks, delete ID 1 | Error: Task not found | ☐ |

---

### 5.5 Feature: Mark Complete/Incomplete

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Mark incomplete complete | ID: 1 (☐) → Complete | Status changes to ✓ | ☐ |
| Mark complete incomplete | ID: 1 (✓) → Incomplete | Status changes to ☐ | ☐ |
| Toggle multiple | Toggle ID 1, then ID 2 | Both toggled correctly | ☐ |
| Invalid ID | Toggle ID: 999 | Error: Task not found | ☐ |
| Verify status persists | Toggle, list, toggle, list | Status correct each list | ☐ |

---

### 5.6 Edge Cases and Integration

| Test Case | Description | Expected Output | Status |
|-----------|-------------|-----------------|--------|
| Invalid menu choice | Enter "7" or "abc" | Error: Invalid choice | ☐ |
| Case sensitivity | Enter "EXIT" or "Exit" | Handle gracefully | ☐ |
| Special characters | Add task with emojis | Works correctly | ☐ |
| Unicode support | Add task in non-Latin script | Works correctly | ☐ |
| Multiple operations | Add → List → Update → List → Delete → List | All steps work | ☐ |
| Exit clean | Choose exit | Program ends without errors | ☐ |
| Empty after all deletes | Add 3, delete all | Shows "No tasks found" | ☐ |

---

### 5.7 Demo Script (for Hackathon Presentation)

```
# Demo flow - follow exactly for consistency

1. Start application
   $ uv run python src/main.py

2. Show initial state
   Select: 2 (List Tasks)
   Expected: "No tasks found"

3. Add first task
   Select: 1 (Add Task)
   Title: "Complete hackathon project"
   Description: "Build todo app with Claude Code agents"
   Expected: "Task added successfully (ID: 1)"

4. List tasks
   Select: 2
   Expected:
   - Shows task 1 with ☐ status
   - Shows "1 task total"

5. Add second task
   Select: 1
   Title: "Create documentation"
   Description: "Write README and CLAUDE.md files"
   Expected: "Task added successfully (ID: 2)"

6. Mark first task complete
   Select: 5
   Task ID: 1
   Action: Mark Complete
   Expected: "Task 1 marked as complete"

7. List tasks
   Select: 2
   Expected:
   - Task 1: ✓ Complete
   - Task 2: ☐ Incomplete

8. Update second task
   Select: 3
   Task ID: 2
   New title: "Create project documentation"
   Leave description empty (keep existing)
   Expected: "Task 2 updated"

9. Delete first task
   Select: 4
   Task ID: 1
   Confirm: y
   Expected: "Task 1 deleted"

10. List final state
    Select: 2
    Expected:
    - Shows only task 2
    - Shows "1 task total"

11. Exit
    Select: 6
    Expected: Program terminates cleanly

12. Restart to show in-memory only
    $ uv run python src/main.py
    Select: 2
    Expected: "No tasks found" (data lost)
```

---

## 6. Implementation Notes

### 6.1 Code Style

- **PEP8 Compliance**: Use `ruff` for linting
- **Line Length**: Maximum 88 characters (ruff default)
- **Imports**: All imports at top of file
- **Docstrings**: Google style for all functions
- **Comments**: Explain "why", not "what"

### 6.2 Function Signatures

```python
def add_task(title: str, description: str) -> int:
    """Add a new task.

    Args:
        title: Task title (non-empty, max 100 chars)
        description: Task description (non-empty, max 500 chars)

    Returns:
        int: ID of created task

    Raises:
        ValueError: If title or description is invalid
    """
    pass

def list_tasks() -> None:
    """Display all tasks with their status."""
    pass

def update_task(task_id: int, title: str = None, description: str = None) -> None:
    """Update a task's title and/or description.

    Args:
        task_id: ID of task to update
        title: New title (optional)
        description: New description (optional)

    Raises:
        ValueError: If task_id not found or no fields provided
    """
    pass

def delete_task(task_id: int) -> None:
    """Delete a task by ID.

    Args:
        task_id: ID of task to delete

    Raises:
        ValueError: If task_id not found
    """
    pass

def toggle_task_status(task_id: int, complete: bool) -> None:
    """Mark a task as complete or incomplete.

    Args:
        task_id: ID of task to update
        complete: True to mark complete, False for incomplete

    Raises:
        ValueError: If task_id not found
    """
    pass
```

### 6.3 Global Variables

```python
# In-memory task storage
tasks: list[dict] = []

# ID counter for unique IDs
_next_id: int = 1
```

### 6.4 Menu Structure

```
=== Todo Evolution - Phase I ===

1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Help
7. Exit

Enter your choice (1-7):
```

---

## 7. Deliverables Verification

### Checkpoint 1: Phase 1 Complete
- [ ] src/main.py exists
- [ ] `add_task()` function implemented
- [ ] `display_tasks()` function implemented
- [ ] `toggle_task_status()` function implemented
- [ ] Can add 3 tasks with auto-incrementing IDs
- [ ] List shows all tasks with correct status

### Checkpoint 2: Phase 2 Complete
- [ ] `update_task()` function implemented
- [ ] `delete_task()` function implemented
- [ ] Input validation in all functions
- [ ] Can update title, description, or both
- [ ] Can delete tasks by ID
- [ ] Invalid IDs handled correctly

### Checkpoint 3: Phase 3 Complete
- [ ] Menu displays all options
- [ ] User input validated
- [ ] Command routing works
- [ ] Main loop runs and exits cleanly
- [ ] Help function displays commands

### Checkpoint 4: Phase 4 Complete
- [ ] No unhandled exceptions
- [ ] Whitespace-only input rejected
- [ ] Clear error messages for all edge cases
- [ ] Destructive operations have confirmation
- [ ] Output is clean and consistent

### Checkpoint 5: Phase 5 Complete
- [ ] README.md with all sections
- [ ] CLAUDE.md with agent instructions
- [ ] .gitignore with proper patterns
- [ ] PEP8 compliant (ruff check passes)
- [ ] Manual test checklist 100% complete
- [ ] Spec v1.0 archived to history/
- [ ] Demo script executed successfully

---

## 8. Phase Completion Criteria

**Phase I is complete when:**

1. ✅ All 5 features work as specified
2. ✅ No errors in normal operation
3. ✅ All edge cases handled gracefully
4. ✅ PEP8 compliance verified
5. ✅ Demo script runs without issues
6. ✅ All documentation files present
7. ✅ Specification history archived
8. ✅ Code generated entirely by agents (no manual edits)

---

## Appendix A: Function Call Graph

```
main()
├── display_menu()
├── get_user_input()
│   └── validate_choice()
├── route_to_function(choice)
│   ├── add_task()
│   │   ├── validate_title()
│   │   ├── validate_description()
│   │   └── _get_next_id()
│   ├── display_tasks()
│   │   └── format_task()
│   ├── update_task()
│   │   ├── find_task_by_id()
│   │   └── validate_update_fields()
│   ├── delete_task()
│   │   ├── find_task_by_id()
│   │   └── confirm_action()
│   ├── toggle_task_status()
│   │   ├── find_task_by_id()
│   │   └── validate_status_input()
│   ├── show_help()
│   └── exit()
└── error_handler(exception)
    └── display_user_error()
```

---

## Appendix B: Error Message Reference

| Error | Message | Function |
|-------|---------|----------|
| Empty title | "Error: Title cannot be empty" | add_task, update_task |
| Empty description | "Error: Description cannot be empty" | add_task, update_task |
| Title too long | "Error: Title must be 100 characters or less" | add_task |
| Description too long | "Error: Description must be 500 characters or less" | add_task |
| Task not found | "Error: Task {id} not found" | update, delete, toggle |
| Invalid choice | "Error: Please enter a number between 1 and 7" | main |
| No fields to update | "Error: At least one field must be provided" | update_task |
| Invalid status | "Error: Please enter 'c' or 'i'" | toggle_task_status |

---

**Document Version**: 1.0
**Created**: 2025-12-30
**For**: Todo Evolution - Phase I Implementation
**Next Phase**: Phase II (Persistent Storage)
