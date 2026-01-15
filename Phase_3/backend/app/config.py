from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    database_url: str = Field(default="postgresql+asyncpg://localhost:5432/todo_chatbot")
    pool_min_size: int = Field(default=1)
    pool_max_size: int = Field(default=16)

    # OpenAI settings (using Google Gemini API endpoint)
    openai_api_key: str = Field(default="")

    # MCP Server settings
    mcp_server_url: str = Field(default="http://localhost:8002")

    # Better Auth settings
    better_auth_secret: str = Field(default="")

    # Application settings
    server_host: str = Field(default="0.0.0.0")
    server_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")

    # CORS settings
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:3001,http://localhost:5173")

    # Session settings
    session_expiry_days: int = Field(default=7)
    password_hash_rounds: int = Field(default=12)

    @field_validator('*', mode='before')
    @classmethod
    def strip_strings(cls, v):
        """Strip whitespace from all string values"""
        if isinstance(v, str):
            return v.strip()
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a singleton instance of settings
settings = Settings()