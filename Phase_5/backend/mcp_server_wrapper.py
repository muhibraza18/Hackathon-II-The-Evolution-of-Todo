#!/usr/bin/env python3
"""
Wrapper script for MCP server to bind to 0.0.0.0 instead of localhost
This works around the hardcoded localhost binding in the original code.
"""
import sys
import os
import logging

# Add the app directory to the Python path
sys.path.insert(0, '/app')

# Import the required modules from the original file
from mcp_server_working import app  # Import the app object that was created in the original file
from aiohttp import web

def main():
    """Main function to start the server on 0.0.0.0"""
    port = 8002

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    logger.info("=" * 60)
    logger.info("🚀 Starting DATABASE-CONNECTED MCP Server (wrapper)")
    logger.info(f"📍 Port: {port}")
    logger.info(f"🌐 Binding to: 0.0.0.0 (accessible from outside container)")
    logger.info(f"📊 Database: Neon PostgreSQL (persistent storage)")
    logger.info(f"🔗 Health check: http://0.0.0.0:{port}/health")
    logger.info("=" * 60)

    # Run the server on 0.0.0.0 instead of localhost
    # This is the key fix: binding to 0.0.0.0 makes it accessible from outside the container
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()