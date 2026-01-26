# Single stage build for FastAPI backend to avoid multi-stage copying issues
FROM python:3.11-slim

WORKDIR /app

# Install build and runtime dependencies including database drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    musl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install psycopg2-binary asyncpg

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check - using a basic HTTP request once the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]