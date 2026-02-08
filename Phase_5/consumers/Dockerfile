FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    psycopg2-binary \
    asyncpg \
    aiohttp \
    pydantic \
    pydantic-settings \
    python-dotenv \
    dapr

# Create consumers package structure
RUN mkdir -p /app/consumers

# Copy consumer code
COPY *.py /app/consumers/

# Create __init__.py for consumers package
RUN touch /app/consumers/__init__.py

# Create basic config for consumers
ENV PYTHONPATH=/app
ENV DAPR_HTTP_PORT=3500
ENV DAPR_GRPC_PORT=50001

EXPOSE 8001

# Default command (will be overridden by Helm chart)
CMD ["python", "-m", "uvicorn", "consumers.recurring_task_consumer:app", "--host", "0.0.0.0", "--port", "8001"]
