# Quick Start: Dapr Integration Implementation

## Overview
This guide provides step-by-step instructions for implementing Dapr integration in the Todo AI Chatbot, replacing direct infrastructure calls with Dapr building blocks.

## Prerequisites
- Minikube cluster running
- Dapr CLI installed (`dapr install -k` for Kubernetes mode)
- Existing Phase V Step 1 & 2 code as base
- Kubernetes cluster access (Minikube for local development)

## Step 1: Install Dapr on Minikube
1. Install Dapr on your Kubernetes cluster:
   ```bash
   dapr init -k
   ```
2. Verify installation:
   ```bash
   dapr status -k
   ```

## Step 2: Create Dapr Component Files
1. Create directory structure:
   ```bash
   mkdir -p dapr-components/pubsub
   mkdir -p dapr-components/state
   mkdir -p dapr-components/secrets
   mkdir -p dapr-components/bindings
   ```
2. Create Kafka pubsub component (`dapr-components/pubsub/kafka-pubsub.yaml`):
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: kafka-pubsub
   spec:
     type: pubsub.kafka
     version: v1
     metadata:
     - name: brokers
       value: "kafka:9092"  # Update with your Kafka broker address
     - name: authRequired
       value: "false"
     - name: consumerGroup
       value: "todo-ai-chatbot-group"
     - name: disableTls
       value: "true"
     - name: version
       value: "2.8.0"
   ```
3. Create PostgreSQL state store component (`dapr-components/state/postgresql-statestore.yaml`):
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: postgresql-statestore
   spec:
     type: state.postgresql
     version: v1
     metadata:
     - name: connectionString
       secretKeyRef:
         name: postgresql-connection-string
         key: connectionString
     - name: actorStateStore
       value: "true"
     - name: keyPrefix
       value: "dapr"
     - name: tableName
       value: "dapr_state_store"
   ```
4. Create Kubernetes secrets component (`dapr-components/secrets/kubernetes-secrets.yaml`):
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: kubernetes-secrets
   spec:
     type: secretstores.kubernetes
     version: v1
     metadata: []
   ```

## Step 3: Deploy Dapr Components
1. Apply the component configurations:
   ```bash
   kubectl apply -f dapr-components/
   ```
2. Verify components are deployed:
   ```bash
   kubectl get components.dapr.io
   ```

## Step 4: Update Application Code
1. Create Dapr client wrapper (`backend/services/dapr_client.py`):
   ```python
   import httpx
   from typing import Any, Dict, Optional
   from ..config.settings import settings

   DAPR_HTTP_ENDPOINT = "http://localhost:3500"

   class DaprClient:
       """Wrapper for Dapr HTTP API calls"""

       @staticmethod
       async def publish_event(pubsub_name: str, topic_name: str, data: Dict[str, Any]) -> bool:
           """Publish an event via Dapr pubsub"""
           try:
               async with httpx.AsyncClient() as client:
                   response = await client.post(
                       f"{DAPR_HTTP_ENDPOINT}/v1.0/publish/{pubsub_name}/{topic_name}",
                       json=data,
                       headers={"Content-Type": "application/json"}
                   )
                   return response.status_code == 204
           except Exception as e:
               print(f"Dapr publish error: {e}")
               return False

       @staticmethod
       async def get_state(store_name: str, key: str) -> Optional[Any]:
           """Get state from Dapr state store"""
           try:
               async with httpx.AsyncClient() as client:
                   response = await client.get(
                       f"{DAPR_HTTP_ENDPOINT}/v1.0/state/{store_name}/{key}"
                   )
                   if response.status_code == 200:
                       return response.json()
                   return None
           except Exception as e:
               print(f"Dapr get state error: {e}")
               return None

       @staticmethod
       async def save_state(store_name: str, key: str, value: Any) -> bool:
           """Save state to Dapr state store"""
           try:
               async with httpx.AsyncClient() as client:
                   response = await client.post(
                       f"{DAPR_HTTP_ENDPOINT}/v1.0/state/{store_name}",
                       json=[{
                           "key": key,
                           "value": value
                       }],
                       headers={"Content-Type": "application/json"}
                   )
                   return response.status_code == 204
           except Exception as e:
               print(f"Dapr save state error: {e}")
               return False

       @staticmethod
       async def get_secret(store_name: str, key: str) -> Optional[str]:
           """Get secret from Dapr secret store"""
           try:
               async with httpx.AsyncClient() as client:
                   response = await client.get(
                       f"{DAPR_HTTP_ENDPOINT}/v1.0/secrets/{store_name}/{key}"
                   )
                   if response.status_code == 200:
                       data = response.json()
                       return data.get(key)
                   return None
           except Exception as e:
               print(f"Dapr get secret error: {e}")
               return None
   ```

2. Update task creation endpoint to use Dapr for event publishing:
   ```python
   # In backend/routes/tasks.py, modify the create_task function:

   from ..services.dapr_client import DaprClient

   # Replace direct Kafka publishing with Dapr publishing:
   # Before:
   # await kafka_publisher.publish_event("task-events", event_payload)

   # After:
   success = await DaprClient.publish_event("kafka-pubsub", "task-events", event_payload)
   if not success:
       # Handle failure appropriately (logging, fallback, etc.)
       print(f"Failed to publish event via Dapr for task {task.id}")
   ```

## Step 5: Update Deployment Manifests
1. Add Dapr annotation to your deployment YAML:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: todo-backend
   spec:
     template:
       metadata:
         annotations:
           dapr.io/enabled: "true"
           dapr.io/app-id: "todo-backend"
           dapr.io/app-port: "8000"
           dapr.io/components-path: "/components"
       spec:
         containers:
         - name: todo-backend
           image: todo-backend:latest
           ports:
           - containerPort: 8000
   ```

## Step 6: Implement Dapr Subscriptions
1. Create a subscription endpoint for receiving events:
   ```python
   # In backend/routes/dapr_webhooks.py
   from fastapi import APIRouter, Request
   import json

   router = APIRouter()

   @router.get("/dapr/subscribe")
   async def dapr_subscribe():
       """Define Dapr pubsub subscriptions"""
       return [
           {
               "pubsubname": "kafka-pubsub",
               "topic": "task-events",
               "route": "/webhooks/task-events"
           }
       ]

   @router.post("/webhooks/task-events")
   async def handle_task_event(request: Request):
       """Handle incoming task events from Dapr"""
       event_data = await request.json()
       # Process the event based on event_type
       event_type = event_data.get('event_type')
       print(f"Received event: {event_type} - {event_data}")

       # Add your event processing logic here
       if event_type == 'task.completed':
           # Handle task completion (e.g., generate next recurring task)
           pass

       return {"success": True}
   ```

## Step 7: Testing
1. Start your application with Dapr:
   ```bash
   dapr run --app-id todo-backend --app-port 8000 -- python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. Test event publishing by creating a task and verifying it's published via Dapr
3. Verify Dapr sidecar is receiving and forwarding events

## Step 8: Validation
1. Check that Dapr sidecars are injected properly:
   ```bash
   kubectl describe pod <your-pod-name>
   ```
2. Verify events are flowing through Dapr:
   ```bash
   dapr logs -k
   ```
3. Confirm no direct Kafka/DB calls remain in application code (only Dapr API calls)
4. Test all functionality works as expected with Dapr integration

## Troubleshooting
- If Dapr sidecar isn't injected: Check annotations in deployment YAML
- If events aren't published: Verify pubsub component is configured and running
- If state operations fail: Check state store component configuration
- If secrets aren't accessible: Verify secret store component and permissions