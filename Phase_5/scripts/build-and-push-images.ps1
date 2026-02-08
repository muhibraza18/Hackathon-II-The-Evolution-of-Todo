# Build and Push Docker Images to Docker Hub
# Run this before deploying to cloud

param(
    [Parameter(Mandatory=$true)]
    [string]$DockerUsername,

    [string]$Tag = "doks-v1"
)

$ErrorActionPreference = "Stop"

Write-Host "🐳 Building and Pushing Docker Images..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor White

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>$null
    if ($dockerVersion) {
        Write-Host "  ✅ Docker running (version $dockerVersion)" -ForegroundColor Green
    } else {
        throw "Docker not responding"
    }
} catch {
    Write-Host "  ❌ Docker not running or not installed" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Docker Hub
Write-Host "`n🔍 Checking Docker Hub login..." -ForegroundColor Yellow
$loginStatus = docker info 2>&1 | Select-String "Username"
if (-not $loginStatus) {
    Write-Host "  ⚠️  Not logged in to Docker Hub" -ForegroundColor Yellow
    docker login
}

$backendImage = "${DockerUsername}/todo-backend:${Tag}"
$frontendImage = "${DockerUsername}/todo-frontend:${Tag}"
$consumersImage = "${DockerUsername}/todo-consumers:${Tag}"

Write-Host "`n📝 Image names:" -ForegroundColor Yellow
Write-Host "  Backend:   $backendImage" -ForegroundColor White
Write-Host "  Frontend:  $frontendImage" -ForegroundColor White
Write-Host "  Consumers: $consumersImage" -ForegroundColor White

# Build backend
Write-Host "`n📍 Step 1: Building backend image..." -ForegroundColor Yellow
Write-Host "  docker build -t $backendImage -f backend/Dockerfile backend" -ForegroundColor Gray
docker build -t $backendImage -f backend/Dockerfile backend
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Backend image built" -ForegroundColor Green
} else {
    Write-Host "  ❌ Backend image build failed" -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "`n📍 Step 2: Building frontend image..." -ForegroundColor Yellow
Write-Host "  docker build -t $frontendImage -f frontend/Dockerfile frontend" -ForegroundColor Gray
docker build -t $frontendImage -f frontend/Dockerfile frontend
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Frontend image built" -ForegroundColor Green
} else {
    Write-Host "  ❌ Frontend image build failed" -ForegroundColor Red
    exit 1
}

# Build consumers
Write-Host "`n📍 Step 3: Building consumers image..." -ForegroundColor Yellow
Write-Host "  docker build -t $consumersImage -f consumers/Dockerfile consumers" -ForegroundColor Gray
docker build -t $consumersImage -f consumers/Dockerfile consumers
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Consumers image built" -ForegroundColor Green
} else {
    Write-Host "  ❌ Consumers image build failed" -ForegroundColor Red
    exit 1
}

# Push images
Write-Host "`n📍 Step 4: Pushing backend image..." -ForegroundColor Yellow
Write-Host "  docker push $backendImage" -ForegroundColor Gray
docker push $backendImage
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Backend image pushed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Backend push failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n📍 Step 5: Pushing frontend image..." -ForegroundColor Yellow
Write-Host "  docker push $frontendImage" -ForegroundColor Gray
docker push $frontendImage
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Frontend image pushed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Frontend push failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n📍 Step 6: Pushing consumers image..." -ForegroundColor Yellow
Write-Host "  docker push $consumersImage" -ForegroundColor Gray
docker push $consumersImage
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Consumers image pushed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Consumers push failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor White
Write-Host "✅ All images built and pushed!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor White

Write-Host "🚀 Ready to deploy!" -ForegroundColor Cyan
Write-Host "  Run: .\scripts\deploy-to-cloud.ps1 -DockerUsername $DockerUsername" -ForegroundColor White
