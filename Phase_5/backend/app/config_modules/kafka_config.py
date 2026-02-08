"""
Kafka configuration settings for the event-driven architecture.
"""
from typing import Optional
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    """
    Settings for Kafka connection and topics.
    """
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_task_events_topic: str = "task-events"
    kafka_reminders_topic: str = "reminders"
    kafka_task_updates_topic: str = "task-updates"
    kafka_group_id: str = "todo-ai-chatbot-group"
    kafka_max_retries: int = 3
    kafka_retry_backoff_ms: int = 1000
    kafka_batch_size: int = 16384
    kafka_linger_ms: int = 5
    kafka_buffer_memory: int = 33554432

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global instance of Kafka settings
kafka_settings = KafkaSettings()