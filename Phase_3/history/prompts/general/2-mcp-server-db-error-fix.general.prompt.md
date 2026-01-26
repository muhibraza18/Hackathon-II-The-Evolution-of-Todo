---
id: 2
title: MCP Server DB Error Fix
stage: general
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-chatkit-frontend
user: Wajahat traders
command: fix-mcp-db-error
labels: [mcp,database,bug-fix,integration]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ./backend/mcp_server.py
  - ./backend/models.py
tests:
---

## Prompt

User reported that chat messages fail with DB_ERROR when trying to add tasks. When sending "Add a task to buy groceries", the AI agent attempts to call the add_task MCP tool but fails with a database error. The error occurs when the MCP tool tries to interact with the database to save the task.

## Response snapshot

Identified and fixed two critical issues in the MCP server:
1. Missing models.py file at backend root that the MCP server was trying to import
2. Type mismatch where MCP server functions received user_id as string but database expected integer

Created backend/models.py to re-export models from the main app and updated all MCP server functions to convert string user_id to integer before database operations.

## Outcome

- ✅ Impact: Resolved DB_ERROR when adding tasks via MCP tools
- 🧪 Tests: Manual verification shows successful task creation and database operations
- 📁 Files: Modified 2 files to fix import and type conversion issues
- 🔁 Next prompts: Ready for full chat functionality testing
- 🧠 Reflection: Critical integration issue between main app and MCP server

## Evaluation notes (flywheel)

- Failure modes observed: Import error and type mismatch causing DB_ERROR
- Graders run and results (PASS/FAIL): N/A - manual verification completed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - issue resolved