#!/usr/bin/env python3
"""
Startup script for the OpenAI Agents Chat API for Todo AI Chatbot

This script provides a clean entry point for starting the FastAPI server
with proper configuration loading and error handling.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from app.config import settings


def main():
    """Main entry point for the API server"""
    print(f"Starting OpenAI Agents Chat API on {settings.server_host}:{settings.server_port}")
    print(f"Log level set to: {settings.log_level}")

    try:
        uvicorn.run(
            "app.main:app",
            host=settings.server_host,
            port=settings.server_port,
            reload=False,  # Set to True for development
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()