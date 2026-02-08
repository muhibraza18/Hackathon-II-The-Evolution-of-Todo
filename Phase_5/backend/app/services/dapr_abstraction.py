"""
Dapr abstraction layer interface for the event-driven architecture.
This provides a clean interface that can be swapped with different infrastructure backends (Kafka, Dapr, etc.).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime


class EventPublisherInterface(ABC):
    """
    Abstract interface for publishing events to a pub/sub system.
    This allows swapping between different implementations (Kafka, Dapr, etc.).
    """

    @abstractmethod
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic.

        Args:
            topic: The topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully, False otherwise
        """
        pass

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the event publisher.

        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Close the event publisher and clean up resources.
        """
        pass


class StateManagerInterface(ABC):
    """
    Abstract interface for managing state in a key-value store.
    This allows swapping between different implementations (PostgreSQL, Redis, Dapr, etc.).
    """

    @abstractmethod
    async def get_state(self, key: str, store_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get state from the store.

        Args:
            key: The key to retrieve
            store_name: Optional store name if multiple stores are supported

        Returns:
            State data if found, None otherwise
        """
        pass

    @abstractmethod
    async def save_state(self, key: str, value: Any, store_name: Optional[str] = None) -> bool:
        """
        Save state to the store.

        Args:
            key: The key to save to
            value: The value to save
            store_name: Optional store name if multiple stores are supported

        Returns:
            True if saved successfully, False otherwise
        """
        pass

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the state manager.

        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Close the state manager and clean up resources.
        """
        pass


class SecretManagerInterface(ABC):
    """
    Abstract interface for managing secrets from a secure store.
    This allows swapping between different implementations (env vars, Kubernetes secrets, Vault, etc.).
    """

    @abstractmethod
    async def get_secret(self, key: str, store_name: Optional[str] = None) -> Optional[str]:
        """
        Get a secret from the store.

        Args:
            key: The secret key to retrieve
            store_name: Optional store name if multiple stores are supported

        Returns:
            Secret value if found, None otherwise
        """
        pass

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the secret manager.

        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Close the secret manager and clean up resources.
        """
        pass


class ServiceInvocationInterface(ABC):
    """
    Abstract interface for service-to-service communication.
    This allows swapping between different implementations (direct HTTP, Dapr service invocation, etc.).
    """

    @abstractmethod
    async def invoke(self, service_id: str, method: str, data: Optional[Dict[str, Any]] = None,
                     verb: str = "POST") -> Optional[Dict[str, Any]]:
        """
        Invoke a method on another service.

        Args:
            service_id: The ID of the target service
            method: The method/path to invoke
            data: Optional request body data
            verb: HTTP verb to use (GET, POST, PUT, etc.)

        Returns:
            Response data if successful, None otherwise
        """
        pass

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the service invoker.

        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Close the service invoker and clean up resources.
        """
        pass


class DaprEventPublisher(EventPublisherInterface):
    """
    Dapr implementation of the event publisher interface.
    """

    def __init__(self, dapr_client):
        self.dapr_client = dapr_client
        self.pubsub_name = "kafka-pubsub"  # Default pubsub component name

    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event using Dapr pubsub API.

        Args:
            topic: The topic to publish to
            event_data: The event data to publish

        Returns:
            True if published successfully, False otherwise
        """
        from .dapr_client import dapr_client
        return await dapr_client.publish_event(self.pubsub_name, topic, event_data)

    async def initialize(self) -> bool:
        """
        Initialize the Dapr event publisher.

        Returns:
            True if initialization was successful, False otherwise
        """
        # Verify Dapr is accessible
        from .dapr_client import dapr_client
        try:
            metadata = await dapr_client.get_metadata()
            return metadata is not None
        except Exception:
            return False

    async def close(self):
        """
        Close the Dapr event publisher.
        Currently a no-op for Dapr since it uses HTTP calls to sidecar.
        """
        pass


class DaprStateManager(StateManagerInterface):
    """
    Dapr implementation of the state manager interface.
    """

    def __init__(self, dapr_client):
        self.dapr_client = dapr_client
        self.store_name = "postgresql-statestore"  # Default state store component name

    async def get_state(self, key: str, store_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get state using Dapr state API.

        Args:
            key: The key to retrieve
            store_name: Optional store name to override default

        Returns:
            State data if found, None otherwise
        """
        from .dapr_client import dapr_client
        target_store = store_name or self.store_name
        return await dapr_client.get_state(target_store, key)

    async def save_state(self, key: str, value: Any, store_name: Optional[str] = None) -> bool:
        """
        Save state using Dapr state API.

        Args:
            key: The key to save to
            value: The value to save
            store_name: Optional store name to override default

        Returns:
            True if saved successfully, False otherwise
        """
        from .dapr_client import dapr_client
        target_store = store_name or self.store_name
        return await dapr_client.save_state(target_store, key, value)

    async def initialize(self) -> bool:
        """
        Initialize the Dapr state manager.

        Returns:
            True if initialization was successful, False otherwise
        """
        # Verify Dapr is accessible
        from .dapr_client import dapr_client
        try:
            metadata = await dapr_client.get_metadata()
            return metadata is not None
        except Exception:
            return False

    async def close(self):
        """
        Close the Dapr state manager.
        Currently a no-op for Dapr since it uses HTTP calls to sidecar.
        """
        pass


class DaprSecretManager(SecretManagerInterface):
    """
    Dapr implementation of the secret manager interface.
    """

    def __init__(self, dapr_client):
        self.dapr_client = dapr_client
        self.store_name = "kubernetes-secrets"  # Default secret store component name

    async def get_secret(self, key: str, store_name: Optional[str] = None) -> Optional[str]:
        """
        Get a secret using Dapr secrets API.

        Args:
            key: The secret key to retrieve
            store_name: Optional store name to override default

        Returns:
            Secret value if found, None otherwise
        """
        from .dapr_client import dapr_client
        target_store = store_name or self.store_name
        return await dapr_client.get_secret(target_store, key)

    async def initialize(self) -> bool:
        """
        Initialize the Dapr secret manager.

        Returns:
            True if initialization was successful, False otherwise
        """
        # Verify Dapr is accessible
        from .dapr_client import dapr_client
        try:
            metadata = await dapr_client.get_metadata()
            return metadata is not None
        except Exception:
            return False

    async def close(self):
        """
        Close the Dapr secret manager.
        Currently a no-op for Dapr since it uses HTTP calls to sidecar.
        """
        pass


class DaprServiceInvoker(ServiceInvocationInterface):
    """
    Dapr implementation of the service invocation interface.
    """

    def __init__(self, dapr_client):
        self.dapr_client = dapr_client

    async def invoke(self, service_id: str, method: str, data: Optional[Dict[str, Any]] = None,
                     verb: str = "POST") -> Optional[Dict[str, Any]]:
        """
        Invoke a service using Dapr service invocation API.

        Args:
            service_id: The ID of the target service
            method: The method/path to invoke
            data: Optional request body data
            verb: HTTP verb to use (GET, POST, PUT, etc.)

        Returns:
            Response data if successful, None otherwise
        """
        from .dapr_client import dapr_client
        return await dapr_client.invoke_service(service_id, method, data, verb)

    async def initialize(self) -> bool:
        """
        Initialize the Dapr service invoker.

        Returns:
            True if initialization was successful, False otherwise
        """
        # Verify Dapr is accessible
        from .dapr_client import dapr_client
        try:
            metadata = await dapr_client.get_metadata()
            return metadata is not None
        except Exception:
            return False

    async def close(self):
        """
        Close the Dapr service invoker.
        Currently a no-op for Dapr since it uses HTTP calls to sidecar.
        """
        pass


# Global instances of the Dapr abstraction implementations
from .dapr_client import dapr_client

dapr_event_publisher = DaprEventPublisher(dapr_client)
dapr_state_manager = DaprStateManager(dapr_client)
dapr_secret_manager = DaprSecretManager(dapr_client)
dapr_service_invoker = DaprServiceInvoker(dapr_client)