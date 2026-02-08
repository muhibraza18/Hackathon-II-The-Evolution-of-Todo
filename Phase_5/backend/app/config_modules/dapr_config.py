"""
Dapr configuration settings for the Todo AI Chatbot.
"""
from typing import Optional
from pydantic_settings import BaseSettings


class DaprSettings(BaseSettings):
    """
    Settings for Dapr integration.
    """
    # Dapr sidecar configuration
    dapr_http_port: int = 3500
    dapr_grpc_port: int = 50001
    dapr_app_id: str = "todo-backend"
    dapr_app_port: int = 8000

    # Dapr component names
    dapr_pubsub_component: str = "kafka-pubsub"
    dapr_state_component: str = "postgresql-statestore"
    dapr_secret_component: str = "kubernetes-secrets"

    # Dapr topic names
    dapr_task_events_topic: str = "task-events"
    dapr_reminders_topic: str = "reminders"
    dapr_task_updates_topic: str = "task-updates"

    # Dapr configuration
    dapr_log_level: str = "info"
    dapr_enable_api_logging: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global instance of Dapr settings
dapr_settings = DaprSettings()