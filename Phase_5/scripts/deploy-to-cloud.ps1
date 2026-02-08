# Deploy to DigitalOcean Kubernetes (DOKS)
# Run this script after secrets are created and images are pushed

param(
    [string]$ClusterId = "bfa88bea-fe4a-ea05-843b-2ae1761e9318",
    [string]$DockerUsername = "",
    [switch]$SkipMonitoring = $false,
    [switch]$SkipLogging = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying to DigitalOcean Kubernetes..." -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor White

# Function to check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Command "kubectl")) {
    Write-Host "❌ kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ kubectl found" -ForegroundColor Green

if (-not (Test-Command "helm")) {
    Write-Host "❌ helm not found. Please install helm first." -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ helm found" -ForegroundColor Green

if (-not (Test-Command "doctl")) {
    Write-Host "❌ doctl not found. Please install doctl first." -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ doctl found" -ForegroundColor Green

# Check Docker username
if ([string]::IsNullOrWhiteSpace($DockerUsername)) {
    $DockerUsername = Read-Host "Enter your Docker Hub username"
}

Write-Host "`n📍 Step 1: Get kubeconfig for cluster" -ForegroundColor Yellow
Write-Host "Cluster ID: $ClusterId" -ForegroundColor White
doctl k8s cluster kubeconfig save $ClusterId

# Verify cluster connection
Write-Host "`n📍 Step 2: Verify cluster connectivity" -ForegroundColor Yellow
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Cannot connect to cluster. Check your cluster ID and doctl authentication." -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Cluster connected" -ForegroundColor Green

# Create monitoring namespace
Write-Host "`n📍 Step 3: Create monitoring namespace" -ForegroundColor Yellow
kubectl create namespace monitoring --ignore-not-exists
Write-Host "  ✅ Monitoring namespace ready" -ForegroundColor Green

# Apply Dapr configuration
Write-Host "`n📍 Step 4: Apply Dapr configuration" -ForegroundColor Yellow
kubectl apply -f dapr-components/dapr-config-cloud.yaml
Write-Host "  ✅ Dapr configuration applied" -ForegroundColor Green

# Apply Redpanda Cloud Pub/Sub component
Write-Host "`n📍 Step 5: Apply Redpanda Cloud Pub/Sub component" -ForegroundColor Yellow
kubectl apply -f dapr-components/pubsub/redpanda-cloud-pubsub.yaml
Write-Host "  ✅ Redpanda Pub/Sub component applied" -ForegroundColor Green

# Verify Dapr installation
Write-Host "`n📍 Step 6: Verify Dapr installation" -ForegroundColor Yellow
$daprPods = kubectl get pods -n dapr-system -o json | ConvertFrom-Json
if ($daprPods.items.Count -eq 0) {
    Write-Host "  ⚠️  Dapr not installed. Installing Dapr..." -ForegroundColor Yellow
    dapr init -k --enable-mtls=false
    Write-Host "  ✅ Dapr installed" -ForegroundColor Green
} else {
    Write-Host "  ✅ Dapr already installed" -ForegroundColor Green
}

# Deploy monitoring stack
if (-not $SkipMonitoring) {
    Write-Host "`n📍 Step 7: Deploy monitoring stack (Prometheus + Grafana)" -ForegroundColor Yellow
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update

    helm upgrade --install prometheus prometheus-community/kube-prometheus-stack `
        --namespace monitoring `
        --set grafana.service.type=LoadBalancer `
        --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false `
        --wait --timeout 10m

    Write-Host "  ✅ Monitoring stack deployed" -ForegroundColor Green
}

# Deploy logging stack
if (-not $SkipLogging) {
    Write-Host "`n📍 Step 8: Deploy logging stack (Loki)" -ForegroundColor Yellow
    helm repo add grafana https://grafana.github.io/helm-charts 2>$null
    helm repo update

    helm upgrade --install loki grafana/loki-stack `
        --namespace monitoring `
        --set loki.persistence.enabled=true `
        --set loki.persistence.size=10Gi `
        --set promtail.enabled=true `
        --set grafana.enabled=false `
        --wait --timeout 10m

    Write-Host "  ✅ Logging stack deployed" -ForegroundColor Green
}

# Update values files with Docker username
Write-Host "`n📍 Step 9: Update Helm values with Docker username" -ForegroundColor Yellow

$backendValues = Get-Content "charts/backend/values-doks.yaml" -Raw
$backendValues = $backendValues -replace '<docker-hub-username>', $DockerUsername
$backendValues | Set-Content "charts/backend/values-doks.yaml"

$frontendValues = Get-Content "charts/frontend/values-doks.yaml" -Raw
$frontendValues = $frontendValues -replace '<docker-hub-username>', $DockerUsername
$frontendValues | Set-Content "charts/frontend/values-doks.yaml"

$consumersValues = Get-Content "charts/consumers/values-doks.yaml" -Raw
$consumersValues = $consumersValues -replace '<docker-hub-username>', $DockerUsername
$consumersValues | Set-Content "charts/consumers/values-doks.yaml"

Write-Host "  ✅ Helm values updated" -ForegroundColor Green

# Deploy applications
Write-Host "`n📍 Step 10: Deploy backend" -ForegroundColor Yellow
helm upgrade --install backend ./charts/backend `
    --namespace default `
    --values ./charts/backend/values-doks.yaml `
    --wait --timeout 5m
Write-Host "  ✅ Backend deployed" -ForegroundColor Green

Write-Host "`n📍 Step 11: Deploy frontend" -ForegroundColor Yellow
helm upgrade --install frontend ./charts/frontend `
    --namespace default `
    --values ./charts/frontend/values-doks.yaml `
    --wait --timeout 5m
Write-Host "  ✅ Frontend deployed" -ForegroundColor Green

Write-Host "`n📍 Step 12: Deploy consumers (if enabled)" -ForegroundColor Yellow
helm upgrade --install consumers ./charts/consumers `
    --namespace default `
    --values ./charts/consumers/values-doks.yaml `
    --wait --timeout 5m
Write-Host "  ✅ Consumers deployed" -ForegroundColor Green

# Get LoadBalancer IP
Write-Host "`n⏳ Waiting for LoadBalancer IP..." -ForegroundColor Yellow
$frontendIP = ""
$attempts = 0
$maxAttempts = 30  # 5 minutes

while ($attempts -lt $maxAttempts -and [string]::IsNullOrWhiteSpace($frontendIP)) {
    Start-Sleep 10
    $frontendIP = kubectl get svc frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
    $attempts++

    if ($attempts -le 3) {
        Write-Host "  Waiting for IP... ($attempts/$maxAttempts)" -ForegroundColor White
    }
}

Write-Host "`n================================================" -ForegroundColor White
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor White

Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://$frontendIP`:3000" -ForegroundColor White

$grafanaIP = kubectl get svc prometheus-grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
if ($grafanaIP) {
    Write-Host "  Grafana:  http://$grafanaIP" -ForegroundColor White
}

Write-Host "`n🔐 To get Grafana password:" -ForegroundColor Cyan
Write-Host '  kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode' -ForegroundColor White

Write-Host "`n📝 Run verification:" -ForegroundColor Cyan
Write-Host "  .\scripts\verify-cloud-deployment.ps1" -ForegroundColor White

Write-Host "`n💾 Save this information:" -ForegroundColor Cyan
"Cloud Frontend URL: http://$frontendIP`:3000" | Out-File -FilePath "CLOUD_ACCESS.txt" -Encoding utf8
Write-Host "  Saved to CLOUD_ACCESS.txt" -ForegroundColor White
