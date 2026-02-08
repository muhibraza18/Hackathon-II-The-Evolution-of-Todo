# Verify DigitalOcean Kubernetes Cloud Deployment
# Run this after deployment to verify everything is working

param(
    [switch]$Detailed
)

$ErrorActionPreference = "Stop"

Write-Host "🔍 Verifying Cloud Deployment..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor White

$allPassed = $true

# Function to print test result
function Test-Result {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Details = ""
    )

    if ($Passed) {
        Write-Host "  ✅ $Name" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $Name" -ForegroundColor Red
        $script:allPassed = $false
    }

    if ($Details -and $Detailed) {
        Write-Host "     $Details" -ForegroundColor Gray
    }
}

# Test 1: Check cluster connectivity
Write-Host "📍 Step 1: Cluster Connectivity" -ForegroundColor Yellow
try {
    $nodes = kubectl get nodes -o json | ConvertFrom-Json
    $readyNodes = ($nodes.items | Where-Object { $_.status.conditions[0].type -eq "Ready" -and $_.status.conditions[0].status -eq "True" }).Count
    Test-Result "Cluster accessible" ($readyNodes -gt 0) "$readyNodes node(s) Ready"
} catch {
    Test-Result "Cluster accessible" $false $_.Exception.Message
}

# Test 2: Check Helm releases
Write-Host "`n📍 Step 2: Helm Releases" -ForegroundColor Yellow
try {
    $releases = helm list -o json | ConvertFrom-Json
    $backendRelease = $releases | Where-Object { $_.name -eq "backend" }
    $frontendRelease = $releases | Where-Object { $_.name -eq "frontend" }
    $consumersRelease = $releases | Where-Object { $_.name -eq "consumers" }

    Test-Result "Backend release deployed" ($null -ne $backendRelease)
    Test-Result "Frontend release deployed" ($null -ne $frontendRelease)
    Test-Result "Consumers release deployed" ($null -ne $consumersRelease)
} catch {
    Test-Result "Helm releases check" $false $_.Exception.Message
}

# Test 3: Check pods
Write-Host "`n📍 Step 3: Pod Status" -ForegroundColor Yellow
try {
    $pods = kubectl get pods -o json | ConvertFrom-Json

    $backendPods = $pods.items | Where-Object { $_.metadata.labels.app -eq "backend-service" }
    $frontendPods = $pods.items | Where-Object { $_.metadata.labels.app -eq "frontend-service" }

    $backendRunning = ($backendPods | Where-Object { $_.status.phase -eq "Running" }).Count
    $frontendRunning = ($frontendPods | Where-Object { $_.status.phase -eq "Running" }).Count

    Test-Result "Backend pods running" ($backendRunning -gt 0) "$backendRunning pod(s)"
    Test-Result "Frontend pods running" ($frontendRunning -gt 0) "$frontendRunning pod(s)"

    # Check Dapr sidecars
    if ($backendPods) {
        $backendContainers = $backendPods[0].spec.containers.Count
        Test-Result "Dapr sidecar injected" ($backendContainers -ge 2) "$backendContainers container(s) (app + daprd)"
    }
} catch {
    Test-Result "Pod status check" $false $_.Exception.Message
}

# Test 4: Check LoadBalancer
Write-Host "`n📍 Step 4: LoadBalancer" -ForegroundColor Yellow
try {
    $service = kubectl get svc frontend-service -o json | ConvertFrom-Json
    $externalIP = $service.status.loadBalancer.ingress[0].ip

    if ([string]::IsNullOrWhiteSpace($externalIP) -or $externalIP -eq "<pending>") {
        Test-Result "LoadBalancer IP assigned" $false "Still pending or not assigned"
    } else {
        Test-Result "LoadBalancer IP assigned" $true "IP: $externalIP"

        # Test frontend connectivity
        if (Get-Command curl -ErrorAction SilentlyContinue) {
            $response = curl -I -s "http://${externalIP}:3000" -UseBasicParsing 2>$null
            if ($response -and $response.StatusCode -eq 200) {
                Test-Result "Frontend accessible" $true "HTTP 200 OK"
            } else {
                Test-Result "Frontend accessible" $false "No HTTP response"
            }
        }
    }
} catch {
    Test-Result "LoadBalancer check" $false $_.Exception.Message
}

# Test 5: Check monitoring stack
Write-Host "`n📍 Step 5: Monitoring Stack" -ForegroundColor Yellow
try {
    $monitoringPods = kubectl get pods -n monitoring -o json | ConvertFrom-Json
    $prometheusPods = $monitoringPods.items | Where-Object { $_.metadata.labels.app -like "*prometheus*" }
    $grafanaPods = $monitoringPods.items | Where-Object { $_.metadata.labels.app -like "*grafana*" }

    $prometheusRunning = ($prometheusPods | Where-Object { $_.status.phase -eq "Running" }).Count
    $grafanaRunning = ($grafanaPods | Where-Object { $_.status.phase -eq "Running" }).Count

    Test-Result "Prometheus running" ($prometheusRunning -gt 0) "$prometheusRunning pod(s)"
    Test-Result "Grafana running" ($grafanaRunning -gt 0) "$grafanaRunning pod(s)"
} catch {
    Test-Result "Monitoring stack check" $false $_.Exception.Message
}

# Test 6: Check logging stack
Write-Host "`n📍 Step 6: Logging Stack" -ForegroundColor Yellow
try {
    $monitoringPods = kubectl get pods -n monitoring -o json | ConvertFrom-Json
    $lokiPods = $monitoringPods.items | Where-Object { $_.metadata.labels.app -like "*loki*" }
    $promtailPods = $monitoringPods.items | Where-Object { $_.metadata.labels.app -like "*promtail*" }

    $lokiRunning = ($lokiPods | Where-Object { $_.status.phase -eq "Running" }).Count
    $promtailRunning = ($promtailPods | Where-Object { $_.status.phase -eq "Running" }).Count

    Test-Result "Loki running" ($lokiRunning -gt 0) "$lokiRunning pod(s)"
    Test-Result "Promtail running" ($promtailRunning -gt 0) "$promtailRunning pod(s)"
} catch {
    Test-Result "Logging stack check" $false $_.Exception.Message
}

# Test 7: Check secrets
Write-Host "`n📍 Step 7: Kubernetes Secrets" -ForegroundColor Yellow
try {
    $secrets = kubectl get secrets -o json | ConvertFrom-Json
    $backendSecret = $secrets.items | Where-Object { $_.metadata.name -eq "todo-backend-secrets" }
    $redpandaSecret = $secrets.items | Where-Object { $_.metadata.name -eq "redpanda-credentials" }

    Test-Result "Backend secrets exist" ($null -ne $backendSecret)
    Test-Result "Redpanda secrets exist" ($null -ne $redpandaSecret)
} catch {
    Test-Result "Secrets check" $false $_.Exception.Message
}

# Test 8: Check Dapr components
Write-Host "`n📍 Step 8: Dapr Components" -ForegroundColor Yellow
try {
    $pubsubComponent = kubectl get component kafka-pubsub -o json 2>$null | ConvertFrom-Json
    Test-Result "Redpanda Pub/Sub component" ($null -ne $pubsubComponent)
} catch {
    Test-Result "Dapr components check" $false $_.Exception.Message
}

# Test 9: Backend health check
Write-Host "`n📍 Step 9: Backend Health" -ForegroundColor Yellow
try {
    $backendPods = kubectl get pods -l app=backend-service -o jsonpath='{.items[0].metadata.name}' 2>$null
    if ($backendPods) {
        $healthCheck = kubectl exec $backendPods -- curl -s http://localhost:8000/health 2>$null
        Test-Result "Backend health endpoint" ($healthCheck -like "*healthy*") "$healthCheck"
    } else {
        Test-Result "Backend health endpoint" $false "No backend pod found"
    }
} catch {
    Test-Result "Backend health check" $false "Could not execute health check"
}

# Summary
Write-Host "`n========================================" -ForegroundColor White
if ($allPassed) {
    Write-Host "✅ All verification checks passed!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor White

    $externalIP = kubectl get svc frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
    if ($externalIP) {
        Write-Host "🌐 Access your application:" -ForegroundColor Cyan
        Write-Host "   Frontend: http://$externalIP`:3000" -ForegroundColor White
    }
} else {
    Write-Host "❌ Some verification checks failed!" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor White
    Write-Host "Run with -Detailed for more information:" -ForegroundColor Yellow
    Write-Host "  .\scripts\verify-cloud-deployment.ps1 -Detailed" -ForegroundColor White
    exit 1
}
