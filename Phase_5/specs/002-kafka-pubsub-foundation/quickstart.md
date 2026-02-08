# Quick Start: Event-Driven Foundation Implementation

## Overview
This guide provides step-by-step instructions for implementing the event-driven foundation using Kafka/Redpanda for the Todo AI Chatbot. The implementation establishes a decoupled architecture where task operations trigger events published to Kafka topics, which are then consumed by separate services for processing.

## Prerequisites
- Phase V Step 1 backend (FastAPI + SQLModel) running
- Minikube cluster with kubectl access
- Docker installed for local development
- Existing task management functionality from Phase V Step 1

## Step 1: Deploy Kafka/Redpanda
1. Install Strimzi operator on Minikube:
   ```bash
   kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka'
   kubectl create namespace kafka
   kubectl apply -f 'https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml' -n kafka
   ```
2. Wait for Kafka cluster to be ready:
   ```bash
   kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
   ```
3. Create required topics:
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: kafka.strimzi.io/v1beta2
   kind: KafkaTopic
   metadata:
     name: task-events
     labels:
       strimzi.io/cluster: my-cluster
     namespace: kafka
   spec:
     partitions: 1
     replicas: 1
   EOF

   kubectl apply -f - <<EOF
   apiVersion: kafka.strimzi.io/v1beta2
   kind: KafkaTopic
   metadata:
     name: reminders
     labels:
       strimzi.io/cluster: my-cluster
     namespace: kafka
   spec:
     partitions: 1
     replicas: 1
   EOF

   kubectl apply -f - <<EOF
   apiVersion: kafka.strimzi.io/v1beta2
   kind: KafkaTopic
   metadata:
     name: task-updates
     labels:
       strimzi.io/cluster: my-cluster
     namespace: kafka
   spec:
     partitions: 1
     replicas: 1
   EOF
   ```

## Step 2: Define Event Schemas
1. Create standardized JSON schemas for all event types
2. Document event payload structures in the data model
3. Implement schema validation utilities

## Step 3: Implement Producer Wrapper
1. Create Kafka abstraction layer in `backend/services/kafka_publisher.py`
2. Implement async `publish_event(topic, payload)` function
3. Add error handling and retry mechanisms
4. Test connection to Kafka cluster

## Step 4: Develop Consumer Services
1. Create recurring task consumer service in `consumers/recurring_task_consumer.py`
2. Create notification placeholder consumer in `consumers/notification_consumer.py`
3. Create audit logging consumer in `consumers/audit_consumer.py`
4. Add health checks and monitoring capabilities

## Step 5: Integrate with Existing Backend
1. Add event publishing to task CRUD operations in the existing backend
2. Connect reminder events to due date logic in the existing services
3. Verify no direct Kafka dependencies in core application code
4. Test integration with existing Phase V Step 1 functionality

## Step 6: Testing & Validation
1. Run unit tests for producer wrapper
2. Run integration tests for consumer logic
3. Perform manual verification of event flow:
   - Create task → verify task-created event in logs
   - Complete recurring task → verify next instance created by consumer
   - Set due date → verify reminder event published
   - Check Kafka consumer group status
4. Test failure scenarios and recovery mechanisms

## Step 7: Deployment & Configuration
1. Update deployment configurations to include Kafka connectivity
2. Configure environment variables for Kafka connection
3. Set up proper resource limits and health checks
4. Verify all services can connect to Kafka cluster

## Verification Commands
- Check Kafka cluster status: `kubectl get kafka -n kafka`
- Check topic creation: `kubectl get kafkatopic -n kafka`
- Monitor consumer groups: `kubectl exec -n kafka -it my-cluster-entity-operator-... -- bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`
- Verify event publishing: Check application logs for event publication messages