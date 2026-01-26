# Production-ready MCP server Dockerfile with explicit SSL disable for Kubernetes
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
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install psycopg2-binary asyncpg aiohttp

# Create directory structure first
RUN mkdir -p app/database

# Copy the MCP server files - with explicit PRODUCTION SSL DISABLE FIX for Kubernetes
COPY backend/mcp_server_working_fixed.py /app/mcp_server_working.py
COPY backend/app/config.py /app/app/config.py
COPY backend/__init__.py /app/__init__.py
COPY backend/app/__init__.py /app/app/__init__.py

# CRITICAL: Copy the PRODUCTION database connection file that forces sslmode=disable
# This is the definitive fix for "PostgreSQL server rejected SSL upgrade" in Kubernetes
COPY backend/app/database/connection_asyncpg_fixed.py /app/app/database/connection.py

COPY backend/app/database/models.py /app/app/database/
RUN mkdir -p /app/app/database/__pycache__ 2>/dev/null || true

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port for MCP server
EXPOSE 8002

# Start the MCP server that binds to 0.0.0.0
CMD ["python", "mcp_server_working.py"]