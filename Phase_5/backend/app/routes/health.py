"""
Health check endpoints for the Dapr-integrated Todo AI Chatbot.
Includes Dapr-specific health checks.
"""
from fastapi import APIRouter
from typing import Dict, Any
import asyncio
from datetime import datetime

from ..services.dapr_client import dapr_client
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    General health check endpoint that verifies the application and Dapr sidecar are healthy.
    """
    health_status = {
        "status": "healthy",
        "service": "Todo AI Chatbot Backend",
        "version": "Phase V - Dapr Integration",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "app_status": "healthy",
            "dapr_sidecar": "checking...",
            "dapr_components": [],
            "dependencies": []
        }
    }

    # Check Dapr sidecar connectivity
    try:
        dapr_metadata = await dapr_client.get_metadata()
        if dapr_metadata:
            health_status["checks"]["dapr_sidecar"] = "healthy"
            health_status["checks"]["dapr_components"] = dapr_metadata.get("components", [])
            health_status["checks"]["actors"] = dapr_metadata.get("actors", [])
        else:
            health_status["checks"]["dapr_sidecar"] = "unreachable"
            health_status["status"] = "degraded"
    except Exception as e:
        logger.error(f"Dapr health check failed: {e}")
        health_status["checks"]["dapr_sidecar"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    return health_status


@router.get("/health/dapr")
async def dapr_health_check() -> Dict[str, Any]:
    """
    Specific health check for Dapr sidecar and components.
    """
    dapr_health = {
        "status": "checking",
        "timestamp": datetime.utcnow().isoformat(),
        "dapr_info": {},
        "components": [],
        "actors": [],
        "errors": []
    }

    try:
        # Get Dapr metadata to verify connectivity
        metadata = await dapr_client.get_metadata()
        if metadata:
            dapr_health["status"] = "healthy"
            dapr_health["dapr_info"] = {
                "id": metadata.get("id", "unknown"),
                "version": metadata.get("version", "unknown"),
                "actors_supported": bool(metadata.get("actors", []))
            }

            # Check each component's status
            components = metadata.get("components", [])
            for component in components:
                comp_status = {
                    "name": component.get("name", "unknown"),
                    "type": component.get("type", "unknown"),
                    "version": component.get("version", "unknown"),
                    "status": "loaded"
                }
                dapr_health["components"].append(comp_status)

            dapr_health["actors"] = metadata.get("actors", [])
        else:
            dapr_health["status"] = "unreachable"
            dapr_health["errors"].append("Could not retrieve Dapr metadata")
    except Exception as e:
        dapr_health["status"] = "error"
        dapr_health["errors"].append(f"Dapr connectivity error: {str(e)}")
        logger.error(f"Dapr-specific health check failed: {e}")

    return dapr_health


@router.get("/health/dapr/publish")
async def dapr_publish_health_check() -> Dict[str, Any]:
    """
    Health check for Dapr publish functionality.
    Tests the ability to publish events via Dapr.
    """
    test_result = {
        "status": "testing",
        "timestamp": datetime.utcnow().isoformat(),
        "test_name": "Dapr Publish Functionality",
        "component": "pubsub.kafka-pubsub",
        "topic": "health-check",
        "success": False,
        "message": ""
    }

    try:
        # Create a simple test event
        test_event = {
            "event_type": "health.check",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Health check event for Dapr publish functionality"
        }

        # Try to publish to a test topic
        success = await dapr_client.publish_event("kafka-pubsub", "health-check", test_event)

        if success:
            test_result["status"] = "healthy"
            test_result["success"] = True
            test_result["message"] = "Successfully published test event via Dapr"
        else:
            test_result["status"] = "failed"
            test_result["success"] = False
            test_result["message"] = "Failed to publish test event via Dapr"
    except Exception as e:
        test_result["status"] = "error"
        test_result["success"] = False
        test_result["message"] = f"Error during Dapr publish test: {str(e)}"
        logger.error(f"Dapr publish health check failed: {e}")

    return test_result


@router.get("/health/dapr/state")
async def dapr_state_health_check() -> Dict[str, Any]:
    """
    Health check for Dapr state store functionality.
    Tests the ability to get/save state via Dapr.
    """
    test_result = {
        "status": "testing",
        "timestamp": datetime.utcnow().isoformat(),
        "test_name": "Dapr State Store Functionality",
        "component": "state.postgresql-statestore",
        "store_name": "postgresql-statestore",
        "success": False,
        "message": ""
    }

    try:
        # Create a test key and value
        test_key = f"health-check-{int(datetime.utcnow().timestamp())}"
        test_value = {
            "timestamp": datetime.utcnow().isoformat(),
            "test_data": "Health check data for Dapr state functionality"
        }

        # Try to save state
        save_success = await dapr_client.save_state("postgresql-statestore", test_key, test_value)
        if not save_success:
            test_result["status"] = "failed"
            test_result["success"] = False
            test_result["message"] = "Failed to save state via Dapr"
            return test_result

        # Try to retrieve the saved state
        retrieved_value = await dapr_client.get_state("postgresql-statestore", test_key)
        if retrieved_value is None:
            test_result["status"] = "failed"
            test_result["success"] = False
            test_result["message"] = "Failed to retrieve state via Dapr"
            return test_result

        # Verify the retrieved value matches what we saved
        if retrieved_value.get("test_data") == test_value["test_data"]:
            test_result["status"] = "healthy"
            test_result["success"] = True
            test_result["message"] = "Successfully saved and retrieved state via Dapr"
        else:
            test_result["status"] = "failed"
            test_result["success"] = False
            test_result["message"] = "Retrieved state does not match saved state"
    except Exception as e:
        test_result["status"] = "error"
        test_result["success"] = False
        test_result["message"] = f"Error during Dapr state test: {str(e)}"
        logger.error(f"Dapr state health check failed: {e}")

    return test_result


@router.get("/health/dapr/secrets")
async def dapr_secrets_health_check() -> Dict[str, Any]:
    """
    Health check for Dapr secrets functionality.
    Tests the ability to retrieve secrets via Dapr.
    """
    test_result = {
        "status": "testing",
        "timestamp": datetime.utcnow().isoformat(),
        "test_name": "Dapr Secrets Functionality",
        "component": "secretstores.kubernetes-secrets",
        "store_name": "kubernetes-secrets",
        "success": False,
        "message": ""
    }

    try:
        # Try to retrieve a test secret (we'll use a common one that should exist)
        # For this test, we'll try to get a non-existent secret to verify the connection works
        # without exposing real secrets
        secret_value = await dapr_client.get_secret("kubernetes-secrets", "test-health-check")

        # If we get here without an exception, the connection is working
        # The secret might not exist (which is fine for this test)
        test_result["status"] = "healthy"
        test_result["success"] = True
        test_result["message"] = "Successfully connected to Dapr secrets store"
    except Exception as e:
        test_result["status"] = "error"
        test_result["success"] = False
        test_result["message"] = f"Error during Dapr secrets test: {str(e)}"
        logger.error(f"Dapr secrets health check failed: {e}")

    return test_result