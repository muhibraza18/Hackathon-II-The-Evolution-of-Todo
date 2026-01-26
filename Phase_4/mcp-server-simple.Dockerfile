# Single stage build for MCP server
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

# Create app directory structure and copy files
RUN mkdir -p app/database
COPY backend/mcp_server_working.py .
COPY backend/app/database/connection.py app/database/
COPY backend/app/database/models.py app/database/
COPY backend/app/database/__init__.py app/database/ 2>/dev/null || echo "No __init__.py file"
COPY backend/app/__init__.py app/ 2>/dev/null || echo "No __init__.py file"
COPY backend/app/config.py app/ 2>/dev/null || echo "No config.py file"

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port for MCP server
EXPOSE 8002

# Start the MCP server
CMD ["python", "mcp_server_working.py"]