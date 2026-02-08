---
id: 31
title: fix-mcp-backend-connection-errors
stage: red
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Wajahat traders
command: /sp.analyze
labels:
  - backend
  - mcp
  - connection
  - kubernetes
  - service-discovery
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - kubectl deployment patch
  - kubernetes service configuration
tests_yaml:
  - kubectl logs -l app.kubernetes.io/name=backend
  - kubectl logs -l app=mcp-server
  - kubectl get svc
---

# Fix MCP Backend Connection Errors

## Prompt Text
```
Still my backend was not working run kubectl logs -l app.kubernetes.io/name=backend --tail=100 and check the error also check the error on MCP server resolve that error and give me working MCP with Chat
```

## Response Text

Identified and fixed the connection error between backend and MCP server:

1. The backend service was configured to connect to "mcp-service:8002" but the actual service name was "mcp-server-service"
2. Fixed by patching the backend deployment to use the correct MCP server URL: "http://mcp-server-service:8002"
3. The backend now connects successfully to the MCP server without DNS resolution errors
4. The asyncpg SSL fix is working properly (clean URLs without SSL params)
5. All services are now running and communicating properly

## Outcome

Backend and MCP server are now properly connected and communicating without errors.

## Evaluation

The fix resolved the service discovery issue and restored proper communication between services.