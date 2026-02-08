# MCP AsyncPG SSL Fix Documentation

## Root Cause
The error `TypeError: connect() got an unexpected keyword argument 'sslmode'` occurred because asyncpg does NOT support the `sslmode` parameter, which is psycopg2-specific. The code was incorrectly passing `sslmode` parameters to asyncpg connections.

## Why asyncpg Rejects sslmode
- `sslmode` is a psycopg2-specific parameter for controlling SSL behavior
- asyncpg uses different SSL configuration methods and does not recognize `sslmode`
- When SQLAlchemy async engines pass `sslmode` to asyncpg, it causes a TypeError

## Solution
The fix removes all psycopg2-specific SSL parameters from database URLs when using asyncpg:
- Filters out: `sslmode`, `sslcert`, `sslkey`, `sslrootcert`, `sslfactory`, `sslcompression`
- Uses proper URL parsing with `urllib.parse` module
- Works deterministically for Kubernetes PostgreSQL services

## Why This Works in Minikube
- Local Kubernetes PostgreSQL typically doesn't require SSL parameters
- Clean URLs without SSL parameters work reliably with asyncpg
- Maintains compatibility with both local and production deployments