---
id: 64
title: Fix kafka import and CORS errors
stage: green
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-local-e2e-polish
user: Wajahat traders
command: /sp.analyze
labels: ["bug-fix","import-error","kafka","cors","module"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/app/services/kafka_publisher.py
tests:
 - Manual test: Try "Add a task Get medicine at 9:12 PM" in chat
 - Manual test: Try completing a task on tasks page
---

## Prompt

Still same error was coming read the backend and mcp logs here is the browser error Add a task Get medicine add reminder at 9:12 PM to be notified
tasks:1 Access to fetch at 'http://localhost:8000/api/tasks' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.Understand this error

## Response snapshot

## Root Cause Analysis

**Error from backend logs:**
```
ModuleNotFoundError: No module named 'app.config.kafka_config'; 'app.config' is not a package
```

**Problem:** The backend was crashing when trying to create or complete tasks because:
1. `reminder_scheduler.py` imports `kafka_publisher.py`
2. `kafka_publisher.py` imports from `..config.kafka_config`
3. But the file is actually at `..config_modules.kafka_config` (wrong import path)

**Why CORS was "not present":**
- When the backend crashes with an import error, it crashes **before** CORS headers can be added to the response
- The browser receives a connection error instead of a proper HTTP response with CORS headers
- This makes it look like a CORS issue when it's actually a server crash

### Fix Applied

**File: `backend/app/services/kafka_publisher.py`**

Changed line 11 from:
```python
from ..config.kafka_config import kafka_settings
```

To:
```python
from ..config_modules.kafka_config import kafka_settings
```

**Why this fixes both problems:**
1. **Import error fixed**: Module now loads from correct path
2. **CORS "fixed"**: Backend no longer crashes, so CORS middleware runs properly and adds headers

## Outcome

- ✅ Impact: Fixed module import path, backend no longer crashes on task operations
- 🧪 Tests: User needs to test chat and task completion
- 📁 Files: backend/app/services/kafka_publisher.py
- 🔁 Next prompts: Test "Add a task Get medicine at 9:12 PM"
- 🧠 Reflection: Module import errors can masquerade as CORS issues - check server logs first

## Current Status

| Service | URL | Image | Pod | Status |
|---------|-----|-------|-----|--------|
| Frontend | http://localhost:3000 | `todo-frontend:chat-fix-v2` | Running | ✅ |
| Backend | http://localhost:8000 | `todo-backend:kafka-fix` | `backend-service-bd85d8477-2x666` | ✅ |
| MCP | http://localhost:8002 | `todo-mcp:latest` | `mcp-server-5d4d6c98c5-j7wgt` | ✅ |

**CORS Headers Verified:**
```
access-control-allow-origin: http://localhost:3000
access-control-allow-credentials: true
access-control-allow-headers: *
access-control-allow-methods: GET, POST, PUT, DELETE, OPTIONS, HEAD
```

## Evaluation notes (flywheel)

- Failure modes observed: (1) Module import path error (2) Apparent CORS issue caused by crash
- Graders run and results (PASS/FAIL): Pending user testing
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Monitor backend logs for any remaining errors
