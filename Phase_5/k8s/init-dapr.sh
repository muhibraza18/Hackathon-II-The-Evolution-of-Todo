#!/bin/bash
# Script to initialize Dapr in Kubernetes mode for Todo AI Chatbot

set -e  # Exit on any error

echo "🚀 Initializing Dapr in Kubernetes mode..."

# Check if kubectl is available and connected to a cluster
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ kubectl is not connected to a cluster. Please start Minikube first with 'minikube start'."
    exit 1
fi

# Check if Dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed. Please install Dapr CLI first."
    echo "Installation: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
fi

# Initialize Dapr in Kubernetes mode
echo "🔧 Installing Dapr control plane to Kubernetes cluster..."
dapr init -k --enable-ha=false

echo "✅ Dapr control plane installed successfully!"

# Wait for Dapr system pods to be ready
echo "⏳ Waiting for Dapr system pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr --timeout=300s -n dapr-system

# Verify Dapr installation
echo "🔍 Verifying Dapr installation..."
dapr status -k

# Check Dapr control plane services
echo "📋 Dapr control plane services:"
kubectl get pods -n dapr-system

echo "🎯 Dapr is ready for Todo AI Chatbot integration!"
echo "💡 Next steps:"
echo "   1. Apply Dapr components: kubectl apply -f dapr-components/"
echo "   2. Deploy Kafka via Strimzi for pubsub functionality"
echo "   3. Update Helm charts with Dapr annotations"
echo "   4. Deploy the application with Dapr sidecars"