#!/bin/bash
# Script to start Minikube with proper resource allocation for Dapr + Kafka + Todo AI Chatbot

set -e  # Exit on any error

echo "🚀 Starting Minikube cluster for Todo AI Chatbot with Dapr..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install Minikube first."
    echo "Installation: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Start Minikube with Docker driver and appropriate resources
echo "🔧 Starting Minikube with Docker driver..."
minikube start \
    --driver=docker \
    --memory=3072 \
    --cpus=4 \
    --disk-size=20g \
    --kubernetes-version=v1.28.3

echo "✅ Minikube cluster started successfully!"

# Verify cluster is ready
echo "🔍 Verifying cluster status..."
kubectl cluster-info
kubectl get nodes

echo "🎉 Minikube cluster is ready for Dapr and Todo AI Chatbot deployment!"
echo "💡 Next steps:"
echo "   1. Run 'dapr init -k' to initialize Dapr in Kubernetes mode"
echo "   2. Deploy Kafka via Strimzi: kubectl apply -f https://strimzi.io/install/latest?namespace=kafka"
echo "   3. Apply Dapr components: kubectl apply -f dapr-components/"
echo "   4. Deploy the application: helm upgrade --install todo-app charts/todo-app/"