# Create Kubernetes Secrets for DOKS Deployment
# Run this after connecting to your DigitalOcean cluster

param(
    [string]$Namespace = "default"
)

Write-Host "🔐 Creating Kubernetes Secrets for DOKS deployment..." -ForegroundColor Cyan

# Check if kubectl is available
$kubectl = Get-Command kubectl -ErrorAction SilentlyContinue
if (-not $kubectl) {
    Write-Host "❌ kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}

# Check current cluster context
$currentContext = kubectl config current-context
Write-Host "📍 Current context: $currentContext" -ForegroundColor Yellow

# Prompt for secrets if not provided
$openaiKey = Read-Host "Enter OpenAI API Key" -MaskInput
$authSecret = Read-Host "Enter Auth Secret" -MaskInput
$dbPassword = Read-Host "Enter DB Password" -MaskInput
$redpandaUsername = "todo-phase5"
$redpandaPassword = Read-Host "Enter Redpanda Password (default: bflLeIafHKGKvshzwRwcIZqvudhMjG)" -MaskInput

if ([string]::IsNullOrWhiteSpace($redpandaPassword)) {
    $redpandaPassword = "bflLeIafHKGKvshzwRwcIZqvudhMjG"
}

# Database URL construction
$databaseUrl = "postgresql+asyncpg://neondb_owner:$dbPassword@ep-calm-frost-ahdmlrul-pooler.c-3.us-east-1.aws.neon.tech:5432/neondb?sslmode=require"

Write-Host "`n📝 Creating secrets in namespace: $Namespace" -ForegroundColor Yellow

# Create backend secrets
Write-Host "  → Creating todo-backend-secrets..." -ForegroundColor White
kubectl create secret generic todo-backend-secrets `
    --from-literal=openai-api-key=$openaiKey `
    --from-literal=auth-secret=$authSecret `
    --from-literal=db-password=$dbPassword `
    --from-literal=database-url=$databaseUrl `
    --namespace=$Namespace

# Create Redpanda credentials
Write-Host "  → Creating redpanda-credentials..." -ForegroundColor White
kubectl create secret generic redpanda-credentials `
    --from-literal=username=$redpandaUsername `
    --from-literal=password=$redpandaPassword `
    --namespace=$Namespace

# Verify secrets
Write-Host "`n✅ Secrets created successfully!" -ForegroundColor Green
Write-Host "`n🔍 Verifying secrets..." -ForegroundColor Yellow

kubectl get secrets --namespace=$Namespace | Select-String "todo-backend-secrets|redpanda-credentials"

Write-Host "`n📋 Secret details:" -ForegroundColor Yellow
Write-Host "`n  todo-backend-secrets:" -ForegroundColor White
kubectl describe secret todo-backend-secrets --namespace=$Namespace | Select-String "openai-api-key|auth-secret|db-password|database-url"

Write-Host "`n  redpanda-credentials:" -ForegroundColor White
kubectl describe secret redpanda-credentials --namespace=$Namespace | Select-String "username|password"

Write-Host "`n✅ All secrets created and verified!" -ForegroundColor Green
