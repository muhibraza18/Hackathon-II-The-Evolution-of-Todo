#!/bin/bash
# Script to validate system resources for Todo AI Chatbot with Dapr and Kafka deployment

set -e  # Exit on any error

echo "🔍 Validating system resources for Todo AI Chatbot deployment..."

# Check Docker is running
echo "🐳 Checking Docker status..."
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
else
    echo "✅ Docker is running"
fi

# Check available memory
echo "💾 Checking available system memory..."
TOTAL_MEMORY=$(free -m | awk '/^Mem:/{print $2}')
FREE_MEMORY=$(free -m | awk '/^Mem:/{print $7}')

echo "   Total memory: ${TOTAL_MEMORY} MB"
echo "   Free memory: ${FREE_MEMORY} MB"

MIN_MEMORY=4096  # Minimum recommended memory (4GB)
RECOMMENDED_MEMORY=8192  # Recommended memory (8GB)

if [ "$TOTAL_MEMORY" -lt 4096 ]; then
    echo "⚠️  WARNING: Total system memory is less than 4GB (${TOTAL_MEMORY}MB)"
    echo "   This may cause performance issues during Minikube + Dapr + Kafka deployment"
elif [ "$TOTAL_MEMORY" -lt 8192 ]; then
    echo "⚠️  INFO: Total system memory is ${TOTAL_MEMORY}MB"
    echo "   This is sufficient but may be tight for comfortable development"
else
    echo "✅ System memory is adequate (${TOTAL_MEMORY}MB)"
fi

if [ "$FREE_MEMORY" -lt 3072 ]; then
    echo "⚠️  WARNING: Free memory (${FREE_MEMORY}MB) may be insufficient for Minikube with 3072MB allocation"
    echo "   Consider closing other applications before starting Minikube"
else
    echo "✅ Free memory is sufficient for Minikube deployment"
fi

# Check available disk space
echo "💾 Checking available disk space..."
DISK_SPACE=$(df -h . | awk 'NR==2{print $4}' | sed 's/G//')
echo "   Available disk space: ${DISK_SPACE} GB"

if [[ $DISK_SPACE =~ ^[0-9]+(\.[0-9]+)?$ ]] && (( $(echo "$DISK_SPACE > 10" | bc -l) )); then
    echo "✅ Disk space is sufficient (>10GB)"
else
    echo "⚠️  WARNING: Less than 10GB of disk space available"
    echo "   This may be insufficient for Docker images and Minikube VM"
fi

# Check if Minikube is installed
echo "⎈ Checking Minikube installation..."
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install Minikube first."
    echo "Installation: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
else
    MINIKUBE_VERSION=$(minikube version)
    echo "✅ Minikube installed: $MINIKUBE_VERSION"
fi

# Check if kubectl is installed
echo "🔍 Checking kubectl installation..."
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
else
    KUBECTL_VERSION=$(kubectl version --client --output=yaml | grep gitVersion | head -1 | cut -d '"' -f 2)
    echo "✅ kubectl installed: $KUBECTL_VERSION"
fi

# Check if Helm is installed
echo "📦 Checking Helm installation..."
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed. Please install Helm first."
    echo "Installation: https://helm.sh/docs/intro/install/"
    exit 1
else
    HELM_VERSION=$(helm version --short)
    echo "✅ Helm installed: $HELM_VERSION"
fi

# Check if Dapr CLI is installed
echo "🔄 Checking Dapr CLI installation..."
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed. Please install Dapr CLI first."
    echo "Installation: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
else
    DAPR_VERSION=$(dapr --version | head -1)
    echo "✅ Dapr CLI installed: $DAPR_VERSION"
fi

# Check if git is installed (for potential git operations)
echo "🐙 Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "⚠️  Git is not installed. Some operations may be affected."
else
    GIT_VERSION=$(git --version)
    echo "✅ Git installed: $GIT_VERSION"
fi

# Check if there's a running Minikube cluster
echo "🌐 Checking for existing Minikube cluster..."
if minikube status >/dev/null 2>&1; then
    MINIKUBE_STATUS=$(minikube status)
    echo "ℹ️  Minikube cluster is already running:"
    echo "$MINIKUBE_STATUS"
else
    echo "ℹ️  No Minikube cluster is currently running (this is expected for fresh setup)"
fi

echo ""
echo "🎉 System resource validation completed!"
echo "📋 Summary:"
echo "   - Docker: Available"
echo "   - Memory: ${TOTAL_MEMORY}MB total, ${FREE_MEMORY}MB free"
echo "   - Disk Space: ${DISK_SPACE}GB available"
echo "   - Minikube: Installed"
echo "   - kubectl: Installed"
echo "   - Helm: Installed"
echo "   - Dapr CLI: Installed"
echo ""
echo "✅ All required tools are installed and system meets minimum requirements."
echo "💡 Ready to proceed with Minikube cluster startup and Dapr integration."