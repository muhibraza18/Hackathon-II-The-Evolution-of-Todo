"""
Kafka publisher service with abstraction layer for the event-driven architecture.
This service provides an abstraction that can be swapped with Dapr or other pub/sub systems later.
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from ..config_modules.kafka_config import kafka_settings
from ..utils.event_validator import EventValidator
from ..utils.logger import get_logger

logger = get_logger(__name__)


class KafkaPublisher:
    """
    Kafka publisher service with abstraction layer.
    This class provides an abstraction that can be replaced with Dapr or other pub/sub systems later.
    """

    def __init__(self):
        self.producer = None
        self._initialized = False

    async def initialize(self):
        """
        Initialize the Kafka publisher.
        This method should be called during application startup.
        """
        try:
            # Import aiokafka here to avoid dependency issues if not needed
            from aiokafka import AIOKafkaProducer

            self.producer = AIOKafkaProducer(
                bootstrap_servers=kafka_settings.kafka_bootstrap_servers,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                batch_size=kafka_settings.kafka_batch_size,
                linger_ms=kafka_settings.kafka_linger_ms,
                buffer_memory=kafka_settings.kafka_buffer_memory
            )

            await self.producer.start()
            self._initialized = True
            logger.info("Kafka publisher initialized successfully")
        except ImportError:
            logger.warning("aiokafka not installed, event publishing disabled")
            self._initialized = False
        except Exception as e:
            logger.error(f"Failed to initialize Kafka publisher: {e}")
            self._initialized = False

    async def close(self):
        """
        Close the Kafka publisher.
        This method should be called during application shutdown.
        """
        if self.producer and self._initialized:
            await self.producer.stop()
            self._initialized = False
            logger.info("Kafka publisher closed successfully")

    async def publish_event(self, topic: str, event_data: Dict[str, Any]):
        """
        Publish an event to the specified topic.

        Args:
            topic: The Kafka topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully, False otherwise
        """
        if not self._initialized:
            logger.warning("Kafka publisher not initialized, skipping event publish")
            return False

        # Validate the event before publishing
        if not EventValidator.validate_event_by_type(event_data):
            logger.error(f"Invalid event data: {event_data}")
            return False

        try:
            # Add timestamp if not present
            if 'timestamp' not in event_data:
                event_data['timestamp'] = datetime.utcnow().isoformat()

            # Publish the event
            await self.producer.send_and_wait(topic, event_data)
            logger.info(f"Event published to topic '{topic}': {event_data['event_type']}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish event to topic '{topic}': {e}")
            # Attempt to retry based on configuration
            return await self._retry_publish(topic, event_data)

    async def _retry_publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Retry publishing an event with exponential backoff.

        Args:
            topic: The Kafka topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully after retries, False otherwise
        """
        for attempt in range(kafka_settings.kafka_max_retries):
            try:
                await asyncio.sleep((2 ** attempt) * (kafka_settings.kafka_retry_backoff_ms / 1000))
                await self.producer.send_and_wait(topic, event_data)
                logger.info(f"Event published to topic '{topic}' after {attempt + 1} attempts")
                return True
            except Exception as e:
                logger.error(f"Retry {attempt + 1} failed to publish event to topic '{topic}': {e}")

        logger.error(f"Failed to publish event to topic '{topic}' after {kafka_settings.kafka_max_retries} attempts")
        return False


# Global instance of the Kafka publisher
kafka_publisher = KafkaPublisher()


# Alternative abstraction layer for future Dapr integration
class EventPublisherInterface:
    """
    Abstract interface for event publishing that can be implemented by different backends.
    This allows switching between Kafka, Dapr, or other pub/sub systems without changing core code.
    """

    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic.

        Args:
            topic: The topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully, False otherwise
        """
        raise NotImplementedError("Subclasses must implement the publish method")


class KafkaEventPublisher(EventPublisherInterface):
    """
    Kafka implementation of the event publisher interface.
    """

    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event using Kafka.

        Args:
            topic: The Kafka topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully, False otherwise
        """
        return await kafka_publisher.publish_event(topic, event_data)


class MockEventPublisher(EventPublisherInterface):
    """
    Mock implementation of the event publisher interface for testing.
    """

    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Mock publish method that just logs the event.

        Args:
            topic: The topic to publish to (ignored in mock)
            event_data: The event data to publish

        Returns:
            True (always succeeds in mock)
        """
        logger.info(f"MOCK EVENT PUBLISHED - Topic: {topic}, Type: {event_data.get('event_type', 'unknown')}")
        return True


# Global event publisher that can be swapped between implementations
event_publisher: EventPublisherInterface = KafkaEventPublisher()


def set_event_publisher(publisher: EventPublisherInterface):
    """
    Set the global event publisher implementation.
    This allows switching between Kafka, Dapr, or mock implementations.

    Args:
        publisher: The event publisher implementation to use
    """
    global event_publisher
    event_publisher = publisher