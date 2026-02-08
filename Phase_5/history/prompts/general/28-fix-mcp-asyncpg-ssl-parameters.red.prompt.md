---
id: 28
title: fix-mcp-asyncpg-ssl-parameters
stage: red
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Wajahat traders
command: /sp.analyze
labels:
  - database
  - asyncpg
  - ssl
  - mcp
  - kubernetes
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\backend\app\database\connection_clean_asyncpg.py
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\mcp-server-clean-asyncpg.Dockerfile
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\mcp-server-final.Dockerfile
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\mcp-server-production.Dockerfile
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\MCP_ASYNC_CONNECTION_FIX_SUMMARY.md
tests_yaml:
  - test_asyncpg_connection_parameters
  - test_ssl_parameter_filtering
  - test_kubernetes_deployment
---

# Fix MCP AsyncPG SSL Parameters

## Prompt Text
```
/sp.analyze

We have a confirmed production bug in the MCP server async database connection.

Error:
TypeError: connect() got an unexpected keyword argument 'sslmode'

Facts:
- MCP uses SQLAlchemy async engine with asyncpg
- asyncpg DOES NOT support `sslmode`
- `sslmode` is a psycopg2-only parameter
- Current code incorrectly injects `sslmode=disable` into asyncpg connections
- This causes MCP DB queries to crash while backend (sync psycopg2) works

Root cause:
- Mixing psycopg2 SSL parameters with asyncpg
- Asyncpg expects `ssl` (bool or SSLContext), NOT `sslmode`

Your task:
1. Remove ALL `sslmode` usage from asyncpg connections
2. Do NOT pass `sslmode` via URL or connect_args for async engines
3. For Kubernetes local Postgres:
   - Use NO SSL parameters at all
   - OR explicitly set `connect_args={"ssl": False}`
4. Ensure backend (sync psycopg2) and MCP (asyncpg) have separate, correct DB configs
5. Return a clean, minimal, production-safe fix

Constraints:
- asyncpg must never receive `sslmode`
- No auto SSL detection heuristics
- Kubernetes Postgres = no SSL
- Fix must be deterministic and explicit

Return:
- Root cause explanation
- Corrected async engine code
- Why this works for asyncpg in Kubernetes
```

## Response Text

Root cause: The error occurs because asyncpg does not support the `sslmode` parameter (psycopg2-specific), but the code was incorrectly passing `sslmode=disable` to asyncpg connections.

Solution: Created a clean asyncpg connection file that removes all SSL parameters instead of forcing them, using proper URL parsing with `urllib.parse` to filter out psycopg2-specific SSL parameters while preserving other valid connection parameters.

The fix works for asyncpg in Kubernetes because it eliminates SSL parameters entirely for local Kubernetes PostgreSQL, uses proper URL parsing, and maintains deterministic behavior compatible with asyncpg requirements.

## Outcome

Successfully implemented a clean, production-safe fix that resolves the asyncpg SSL parameter issue by creating a proper connection file that removes SSL parameters for asyncpg while maintaining all existing functionality.

## Evaluation

The fix addresses all requirements: removes sslmode from asyncpg connections, works deterministically for Kubernetes PostgreSQL, maintains backward compatibility, and follows security best practices.