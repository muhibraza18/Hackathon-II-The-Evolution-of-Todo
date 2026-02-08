#!/bin/bash
# Script to apply all Dapr components for Todo AI Chatbot

set -e  # Exit on any error

echo "🔄 Applying Dapr components for Todo AI Chatbot..."

# Check if kubectl is available and connected to a cluster
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ kubectl is not connected to a cluster. Please start Minikube first."
    exit 1
fi

# Check if Dapr is initialized
if ! dapr status -k >/dev/null 2>&1; then
    echo "❌ Dapr is not initialized in Kubernetes. Please run 'dapr init -k' first."
    exit 1
fi

# Apply Dapr pubsub component (Kafka)
echo "🔧 Applying Dapr pubsub component (Kafka)..."
kubectl apply -f dapr-components/pubsub/kafka-pubsub.yaml

# Apply Dapr state store component (PostgreSQL)
echo "🔧 Applying Dapr state store component (PostgreSQL)..."
kubectl apply -f dapr-components/state/postgresql-statestore.yaml

# Apply Dapr secrets store component (Kubernetes secrets)
echo "🔧 Applying Dapr secrets store component (Kubernetes secrets)..."
kubectl apply -f dapr-components/secrets/kubernetes-secrets.yaml

# Apply Dapr jobs component (cron for reminders)
echo "🔧 Applying Dapr jobs component (cron for reminders)..."
kubectl apply -f dapr-components/jobs/dapr-jobs.yaml

# Wait a moment for components to be processed
sleep 5

# Verify all Dapr components are applied
echo "🔍 Verifying Dapr components..."
kubectl get components.dapr.io -A

# Get detailed status of each component
echo ""
echo "📋 Dapr pubsub component status:"
kubectl get component kafka-pubsub -o yaml

echo ""
echo "📋 Dapr state store component status:"
kubectl get component state-postgresql -o yaml

echo ""
echo "📋 Dapr secrets component status:"
kubectl get component kubernetes-secrets -o yaml

echo ""
echo "📋 Dapr jobs component status:"
kubectl get component reminder-jobs -o yaml

# Test Dapr component connectivity
echo ""
echo "🧪 Testing Dapr component connectivity..."
dapr components -k

echo ""
echo "✅ All Dapr components applied successfully!"
echo "📋 Applied components:"
echo "   - kafka-pubsub: Pub/Sub for task events and reminders"
echo "   - state-postgresql: State management for tasks and conversations"
echo "   - kubernetes-secrets: Secure access to secrets"
echo "   - reminder-jobs: Cron-based reminder scheduling"
echo ""
echo "💡 Dapr components are ready for application integration."
echo "   Applications can now use Dapr APIs to access these building blocks."