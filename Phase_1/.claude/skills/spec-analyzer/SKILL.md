---
name: spec-analyzer
description: Analyzes and validates todo app specifications for completeness and clarity. Use when reviewing specs, writing new requirements, or checking feature coverage.
---
# Spec Analyzer for Todo App

When analyzing a spec, always check for these required features:
- Add task: with title and description
- List/View tasks: show ID, title, description, and completion status
- Update task: modify title or description by ID
- Delete task: remove by ID
- Mark task as complete or incomplete

Also look for:
- Unique task IDs
- Error handling (invalid ID, empty input)
- Clear user instructions in CLI

Suggest improvements if missing (e.g., "Add validation for empty titles").

Use simple analogies:
- "The todo list is like a paper notebook: easy to add notes, cross them out, or erase."

Output a summary:
- What's covered ✓
- What's missing or unclear ⚠
- Recommendations