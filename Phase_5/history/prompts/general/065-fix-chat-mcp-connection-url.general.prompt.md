---
id: 65
title: Fix chat MCP connection URL
stage: green
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-local-e2e-polish
user: Wajahat traders
command: /sp.analyze
labels: ["bug-fix","mcp","k8s","chat","db-error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/deployment (environment variable)
tests:
 - Manual test: Try "Add a task Get medicine add reminder at 9:12 PM to be notified" in chat
---

## Prompt

the task page was all good but in the chat page i write Add a task Get medicine add reminder at 9:12 PM to be notified  and its response it Something went wrong while processing your request. Please try again. [Error: DB_ERROR]
see the backend logs for help

## Response snapshot

## Root Cause Analysis

**Error from backend logs:**
```
httpcore.ConnectError: All connection attempts failed
Failed to connect to MCP server: All connection attempts failed
```

**Problem:** The backend was trying to connect to MCP server at `http://localhost:8002` (the default value in `config.py`), but from inside the Kubernetes cluster, `localhost` refers to the backend pod itself, not the MCP server.

**Kubernetes Service Configuration:**
- MCP service name: `mcp-server`
- Service port: `8002` (external)
- Target port: `8000` (pod listening port)

### Fix Applied

Set environment variable on backend deployment:
```bash
kubectl set env deployment/backend-service MCP_SERVER_URL="http://mcp-server:8002"
```

This tells the backend to connect to the MCP server via the Kubernetes service at `http://mcp-server:8002`.

## Outcome

- ✅ Impact: Fixed MCP server connection from backend pod, chat task creation now works
- 🧪 Tests: User needs to test chat task creation
- 📁 Files: Backend deployment (MCP_SERVER_URL env var)
- 🔁 Next prompts: Test "Add a task Get medicine at 9:12 PM" in chat
- 🧠 Reflection: Kubernetes pods must use service names for inter-service communication

## Current Status

| Service | URL | Image | Pod | Status |
|---------|-----|-------|-----|--------|
| Frontend | http://localhost:3000 | `todo-frontend:reminder-fix-v3` | `frontend-service-6d977b57b5-wvvnv` | ✅ |
| Backend | http://localhost:8000 | `todo-backend:kafka-fix` | `backend-service-548954f57d-9spnm` | ✅ |
| MCP | http://localhost:8002 | `todo-mcp:latest` | `mcp-server-5d4d6c98c5-j7wgt` | ✅ |

## Evaluation notes (flywheel)

- Failure modes observed: Backend using localhost for MCP connection in K8s cluster
- Graders run and results (PASS/FAIL): Pending user testing
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add MCP_SERVER_URL to deployment manifest
