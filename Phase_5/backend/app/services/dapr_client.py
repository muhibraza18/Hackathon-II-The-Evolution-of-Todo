"""
Dapr client wrapper for the event-driven architecture.
Provides an abstraction layer for all Dapr API calls.
"""
import httpx
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from ..config_modules.dapr_config import dapr_settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DaprClient:
    """
    Wrapper class for Dapr API calls providing an abstraction layer
    that can be easily swapped with different infrastructure backends.
    """

    def __init__(self):
        self.http_endpoint = f"http://localhost:{dapr_settings.dapr_http_port}"
        self.app_id = dapr_settings.dapr_app_id

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[str, Any],
                           metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Publish an event to a Dapr pubsub component.

        Args:
            pubsub_name: Name of the pubsub component (e.g., "kafka-pubsub")
            topic_name: Name of the topic to publish to
            data: The event data to publish
            metadata: Optional metadata for the event

        Returns:
            True if published successfully, False otherwise
        """
        try:
            # Add timestamp if not present
            if 'timestamp' not in data:
                data['timestamp'] = datetime.utcnow().isoformat()

            url = f"{self.http_endpoint}/v1.0/publish/{pubsub_name}/{topic_name}"

            async with httpx.AsyncClient() as client:
                headers = {"Content-Type": "application/json"}
                if metadata:
                    # Add metadata as headers with dapr-metadata prefix
                    for key, value in metadata.items():
                        headers[f"metadata.{key}"] = str(value)

                response = await client.post(url, json=data, headers=headers)

            if response.status_code == 204:
                logger.info(f"Event published successfully to {pubsub_name}/{topic_name}: {data.get('event_type', 'unknown')}")
                return True
            else:
                logger.error(f"Failed to publish event to {pubsub_name}/{topic_name}. Status: {response.status_code}, Response: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Exception in Dapr publish_event: {e}")
            return False

    async def get_state(self, store_name: str, key: str,
                       metadata: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Get state from a Dapr state store.

        Args:
            store_name: Name of the state store component (e.g., "postgresql-statestore")
            key: Key of the state to retrieve
            metadata: Optional metadata for the request

        Returns:
            State data if found, None otherwise
        """
        try:
            url = f"{self.http_endpoint}/v1.0/state/{store_name}/{key}"

            async with httpx.AsyncClient() as client:
                headers = {}
                if metadata:
                    for key, value in metadata.items():
                        headers[f"metadata.{key}"] = str(value)

                response = await client.get(url, headers=headers)

            if response.status_code == 200:
                logger.debug(f"State retrieved successfully from {store_name}/{key}")
                return response.json()
            elif response.status_code == 404:
                logger.debug(f"State not found for {store_name}/{key}")
                return None
            else:
                logger.error(f"Failed to get state from {store_name}/{key}. Status: {response.status_code}, Response: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Exception in Dapr get_state: {e}")
            return None

    async def save_state(self, store_name: str, key: str, value: Any,
                         etag: Optional[str] = None,
                         metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Save state to a Dapr state store.

        Args:
            store_name: Name of the state store component
            key: Key of the state to save
            value: Value to save
            etag: Optional etag for concurrency control
            metadata: Optional metadata for the request

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            url = f"{self.http_endpoint}/v1.0/state/{store_name}"

            state_item = {
                "key": key,
                "value": value
            }

            if etag:
                state_item["etag"] = etag

            if metadata:
                state_item["metadata"] = metadata

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=[state_item])

            if response.status_code == 204:
                logger.debug(f"State saved successfully to {store_name}/{key}")
                return True
            else:
                logger.error(f"Failed to save state to {store_name}/{key}. Status: {response.status_code}, Response: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Exception in Dapr save_state: {e}")
            return False

    async def get_secret(self, store_name: str, key: str,
                         metadata: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Get a secret from a Dapr secret store.

        Args:
            store_name: Name of the secret store component (e.g., "kubernetes-secrets")
            key: Key of the secret to retrieve
            metadata: Optional metadata for the request

        Returns:
            Secret value if found, None otherwise
        """
        try:
            url = f"{self.http_endpoint}/v1.0/secrets/{store_name}/{key}"

            async with httpx.AsyncClient() as client:
                headers = {}
                if metadata:
                    for k, v in metadata.items():
                        headers[f"metadata.{k}"] = str(v)

                response = await client.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                secret_value = data.get(key)
                if secret_value:
                    logger.debug(f"Secret retrieved successfully from {store_name}/{key}")
                    return secret_value
                else:
                    logger.warning(f"Secret key {key} not found in response from {store_name}")
                    return None
            elif response.status_code == 404:
                logger.debug(f"Secret not found for {store_name}/{key}")
                return None
            else:
                logger.error(f"Failed to get secret from {store_name}/{key}. Status: {response.status_code}, Response: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Exception in Dapr get_secret: {e}")
            return None

    async def invoke_service(self, target_app_id: str, method: str,
                            data: Optional[Dict[str, Any]] = None,
                            verb: str = "POST",
                            headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Invoke a method on another service via Dapr service invocation.

        Args:
            target_app_id: The app ID of the target service
            method: The method/path to invoke
            data: Optional request body data
            verb: HTTP verb to use (GET, POST, PUT, etc.)
            headers: Optional headers to include in the request

        Returns:
            Response data if successful, None otherwise
        """
        try:
            url = f"{self.http_endpoint}/v1.0/invoke/{target_app_id}/method/{method}"

            async with httpx.AsyncClient() as client:
                req_headers = {"Content-Type": "application/json"}
                if headers:
                    req_headers.update(headers)

                if verb.upper() == "GET":
                    response = await client.get(url, headers=req_headers)
                elif verb.upper() == "POST":
                    response = await client.post(url, json=data, headers=req_headers)
                elif verb.upper() == "PUT":
                    response = await client.put(url, json=data, headers=req_headers)
                elif verb.upper() == "DELETE":
                    response = await client.delete(url, headers=req_headers)
                else:
                    logger.error(f"Unsupported HTTP verb: {verb}")
                    return None

            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:  # No content
                    logger.debug(f"Service invocation to {target_app_id}/{method} succeeded (no content)")
                    return {}
                else:
                    logger.debug(f"Service invocation to {target_app_id}/{method} succeeded")
                    return response.json()
            else:
                logger.error(f"Failed to invoke service {target_app_id}/{method}. Status: {response.status_code}, Response: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Exception in Dapr invoke_service: {e}")
            return None

    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Get metadata from the Dapr sidecar.

        Returns:
            Metadata dictionary if successful, None otherwise
        """
        try:
            url = f"{self.http_endpoint}/v1.0/metadata"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            if response.status_code == 200:
                logger.debug("Dapr metadata retrieved successfully")
                return response.json()
            else:
                logger.error(f"Failed to get Dapr metadata. Status: {response.status_code}, Response: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Exception in Dapr get_metadata: {e}")
            return None

    async def bulk_get_state(self, store_name: str, keys: List[str],
                           metadata: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Bulk get state from a Dapr state store.

        Args:
            store_name: Name of the state store component
            keys: List of keys to retrieve
            metadata: Optional metadata for the request

        Returns:
            List of state items
        """
        try:
            url = f"{self.http_endpoint}/v1.0/state/{store_name}/bulk"

            request_data = {
                "keys": keys
            }

            if metadata:
                request_data["metadata"] = metadata

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=request_data)

            if response.status_code == 200:
                logger.debug(f"Bulk state retrieval from {store_name} succeeded for {len(keys)} keys")
                return response.json()
            else:
                logger.error(f"Failed to bulk get state from {store_name}. Status: {response.status_code}, Response: {response.text}")
                return []

        except Exception as e:
            logger.error(f"Exception in Dapr bulk_get_state: {e}")
            return []


# Global instance of the Dapr client
dapr_client = DaprClient()