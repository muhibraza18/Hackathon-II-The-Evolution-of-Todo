FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-mcp.txt /app/
RUN pip install --no-cache-dir -r requirements-mcp.txt

# Copy MCP server code
COPY mcp_server.py /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV BACKEND_API_URL=http://backend-service:8000

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import aiohttp; aiohttp.ClientSession().get('http://localhost:8002/health')" || exit 1

# Run the MCP server
CMD ["python", "-u", "mcp_server.py"]
