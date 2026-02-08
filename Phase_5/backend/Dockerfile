# FastAPI Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build and runtime dependencies including database drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install psycopg2-binary asyncpg aiohttp

# Copy the entire app directory (crud.py is now inside app/)
COPY app/ ./app/
COPY __init__.py ./

# Copy MCP server scripts
COPY mcp_server_working.py ./

# Expose port for FastAPI backend and MCP server
EXPOSE 8000
EXPOSE 8002

# Start the FastAPI app with uvicorn (default)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]