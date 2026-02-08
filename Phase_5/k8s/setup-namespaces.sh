#!/bin/bash
# Script to set up Kubernetes namespaces for Todo AI Chatbot with Dapr integration

set -e  # Exit on any error

echo "📦 Setting up Kubernetes namespaces..."

# Check if kubectl is available and connected to a cluster
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ kubectl is not connected to a cluster. Please start Minikube first."
    exit 1
fi

# Create kafka namespace for Strimzi
echo "🔧 Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Create dapr namespace (though Dapr init should handle this, we ensure it exists)
echo "🔧 Creating dapr namespace if needed..."
kubectl create namespace dapr-system --dry-run=client -o yaml | kubectl apply -f - || true

# Create default namespace configurations
echo "🔧 Setting up default namespace configurations..."
kubectl config set-context --current --namespace=default

# Label the default namespace for Dapr
echo "🏷️  Labeling default namespace for Dapr sidecar injection..."
kubectl label namespace default dapr.io/enabled=true --overwrite

# Verify namespaces were created
echo "🔍 Verifying namespace creation..."
kubectl get namespaces

echo "✅ Namespaces created successfully!"
echo "📋 Created namespaces:"
echo "   - default (with Dapr sidecar injection enabled)"
echo "   - kafka (for Strimzi Kafka deployment)"
echo "   - dapr-system (for Dapr control plane components)"
echo ""
echo "💡 The default namespace is labeled for automatic Dapr sidecar injection."
echo "   Deployed pods in this namespace will automatically get Dapr sidecars."