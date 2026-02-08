#!/bin/bash
# Script to deploy Kafka via Strimzi for Todo AI Chatbot event-driven architecture

set -e  # Exit on any error

echo ".kafka 🚀 Deploying Kafka via Strimzi..."

# Check if kubectl is available and connected to a cluster
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ kubectl is not connected to a cluster. Please start Minikube first."
    exit 1
fi

# Create kafka namespace if it doesn't exist
echo "🔧 Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Install Strimzi operator
echo "🔧 Installing Strimzi Kafka operator..."
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the operator to be ready
echo "⏳ Waiting for Strimzi operator to be ready..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy Kafka cluster with ephemeral storage (for local development)
echo "🔧 Deploying Kafka cluster with ephemeral storage..."
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
echo "⏳ Waiting for Kafka cluster to be ready..."
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=600s -n kafka

# Create necessary topics for Todo AI Chatbot
echo "🔧 Creating Kafka topics for Todo AI Chatbot..."
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824 # 1GB
EOF

kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: reminders
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824 # 1GB
EOF

kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-updates
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824 # 1GB
EOF

# Wait for topics to be ready
echo "⏳ Waiting for Kafka topics to be ready..."
kubectl wait kafkatopic/task-events --for=condition=Ready --timeout=60s -n kafka
kubectl wait kafkatopic/reminders --for=condition=Ready --timeout=60s -n kafka
kubectl wait kafkatopic/task-updates --for=condition=Ready --timeout=60s -n kafka

# Verify Kafka cluster status
echo "🔍 Verifying Kafka cluster status..."
kubectl get pods -n kafka
kubectl get kafka -n kafka

# Test Kafka connectivity (using Kafka tools pod)
echo "🧪 Testing Kafka connectivity..."
kubectl run kafka-test-producer -ti --image=quay.io/strimzi/kafka:latest-kafka-3.6.0 --rm=true --restart=Never --namespace kafka -- bin/kafka-topics.sh --list --bootstrap-server my-cluster-kafka-bootstrap:9092

echo "✅ Kafka cluster deployed and configured successfully!"
echo "📋 Created resources:"
echo "   - Strimzi operator in kafka namespace"
echo "   - Kafka cluster (my-cluster) with ephemeral storage"
echo "   - ZooKeeper cluster for Kafka"
echo "   - Kafka topics: task-events, reminders, task-updates"
echo ""
echo "💡 Kafka is ready for Dapr pubsub component integration."
echo "   The bootstrap server address is: my-cluster-kafka-bootstrap.kafka:9092"