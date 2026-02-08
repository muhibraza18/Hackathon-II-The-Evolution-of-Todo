# Quick Start: Local Minikube + Dapr Deployment

## Overview
This guide provides step-by-step instructions for deploying the Todo AI Chatbot with Dapr integration to a local Minikube cluster.

## Prerequisites
- Docker Desktop running (with WSL 2 backend if on Windows)
- kubectl installed and configured
- helm installed and configured
- dapr CLI installed and available
- minikube installed and available
- At least 4GB of free RAM recommended

## Step 1: Start Minikube Cluster
```bash
# Start Minikube with Docker driver and appropriate resources
minikube start --driver=docker --memory=3072 --cpus=4 --disk-size=20g

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Step 2: Initialize Dapr
```bash
# Initialize Dapr in Kubernetes mode (single node for local development)
dapr init -k --enable-ha=false

# Verify Dapr is running
dapr status -k

# Check Dapr control plane pods
kubectl get pods -n dapr-system
```

## Step 3: Deploy Kafka via Strimzi
```bash
# Create kafka namespace
kubectl create namespace kafka

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the operator to be ready
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy Kafka cluster with ephemeral storage (for local development)
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.6"
    storage:
      type: ephemeral
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Wait for Kafka cluster to be ready
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

## Step 4: Deploy Dapr Components
```bash
# Create Dapr pubsub component for Kafka
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-bootstrap.kafka:9092"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "todo-ai-chatbot-group"
  - name: disableTls
    value: "true"
  - name: version
    value: "3.6.0"
EOF

# Create Dapr state store component for PostgreSQL
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: state-postgresql
  namespace: default
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
  - name: timeout
    value: "30s"
EOF

# Create Dapr secret store component for Kubernetes secrets
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
EOF

# Verify components are applied
kubectl get components.dapr.io
```

## Step 5: Update Helm Charts with Dapr Annotations
```bash
# Example of how to add Dapr annotations to a deployment in Helm chart
# This would be added to the deployment YAML template in your Helm chart

# For the backend service
dapr.io/enabled: "true"
dapr.io/app-id: "todo-backend"
dapr.io/app-port: "8000"
dapr.io/config: "dapr-config"
dapr.io/log-level: "info"

# For consumer services
dapr.io/enabled: "true"
dapr.io/app-id: "todo-consumer-{type}"
dapr.io/app-port: "8001"  # or appropriate port
dapr.io/config: "dapr-config"
dapr.io/log-level: "info"
```

## Step 6: Deploy Application Stack
```bash
# Create secrets for database connection and API keys
kubectl create secret generic postgresql-connection-string \
  --from-literal=connectionString="postgresql://user:password@neon-db-url:5432/dbname"

kubectl create secret generic api-keys \
  --from-literal=openaiApiKey="your-openai-key" \
  --from-literal=betterAuthSecret="your-auth-secret"

# Deploy the application using updated Helm chart
helm upgrade --install todo-app charts/todo-app/ \
  --set dapr.enabled=true \
  --set dapr.appId="todo-backend" \
  --set dapr.appPort=8000 \
  --set replicaCount=1

# Verify all pods are running with Dapr sidecars
kubectl get pods -o wide
# Look for pods with 2/2 READY (app + dapr sidecar)
```

## Step 7: Verify Deployment
```bash
# Check all pods are running with Dapr sidecars
kubectl get pods
# All pods should show 2/2 or more containers ready

# Check Dapr sidecar logs for each pod
kubectl logs <pod-name> -c daprd

# Verify services are accessible
kubectl get services

# Get frontend URL via minikube service
minikube service todo-frontend --url

# Test basic functionality by creating a task
# You can use curl or access the UI at the minikube service URL
```

## Step 8: End-to-End Testing
```bash
# 1. Create a recurring task and verify it generates next occurrence
curl -X POST $(minikube service todo-backend --url)/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Recurring Test Task","recurring_config":{"type":"daily","interval":1}}'

# 2. Verify events are published and consumed
kubectl logs -l app=todo-consumer-recurring

# 3. Check Dapr pubsub functionality
dapr components -k | grep pubsub

# 4. Verify state operations work via Dapr
dapr components -k | grep state
```

## Troubleshooting Common Issues

### Issue: Pods stuck in "Init" state
**Solution**: Check if Dapr sidecar injector is running:
```bash
kubectl get pods -n dapr-system
kubectl logs -n dapr-system -l app=dapr-sidecar-injector
```

### Issue: Kafka not connecting
**Solution**: Verify Kafka is running and check broker address:
```bash
kubectl get pods -n kafka
kubectl describe service my-cluster-kafka-bootstrap -n kafka
```

### Issue: Dapr components not found
**Solution**: Check component syntax and namespace:
```bash
kubectl get components.dapr.io -A
kubectl describe component <component-name>
```

### Issue: Insufficient resources
**Solution**: Adjust Minikube resources or reduce application replica counts:
```bash
minikube ssh 'free -h'  # Check available memory
kubectl top nodes       # Check resource usage
```

## Cleanup
```bash
# To stop the Minikube cluster
minikube stop

# To delete the cluster completely
minikube delete

# To uninstall Dapr
dapr uninstall -k
```