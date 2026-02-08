# Windows Installation Guide: DOKS Deployment Prerequisites

**Purpose**: Install kubectl, doctl, and verify DigitalOcean cluster connectivity

---

## Table of Contents

1. [Install kubectl](#1-install-kubectl)
2. [Install doctl](#2-install-doctl)
3. [Install Dapr CLI](#3-install-dapr-cli-optional)
4. [Verify Installations](#4-verify-installations)
5. [Authenticate with DigitalOcean](#5-authenticate-with-digitalocean)
6. [Get Cluster Kubeconfig](#6-get-cluster-kubeconfig)
7. [Test Cluster Connectivity](#7-test-cluster-connectivity)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Install kubectl

### Option A: Using winget (Recommended - Windows 10/11)

```powershell
# Run PowerShell as Administrator
winget install Kubernetes.kubectl
```

### Option B: Using Chocolatey

```powershell
# Run PowerShell as Administrator
choco install kubernetes-cli
```

### Option C: Manual Download (If winget/choco not available)

```powershell
# Run PowerShell as Administrator
# Download latest stable release
curl -LO "https://dl.k8s.io/release/stable.txt"

# Get version and download binary
$version = Get-Content stable.txt
curl -LO "https://dl.k8s.io/release/$version/bin/windows/amd64/kubectl.exe"

# Move to PATH (choose one location)
# Option 1: System-wide (requires Admin)
Move-Item .\kubectl.exe C:\Windows\System32\kubectl.exe

# Option 2: User directory
$userPath = [Environment]::GetFolderPath("UserProfile")
Move-Item .\kubectl.exe "$userPath\kubectl.exe"
# Then add "$env:USERPROFILE" to your PATH environment variable
```

---

## 2. Install doctl (DigitalOcean CLI)

### Option A: Using winget (Recommended - Windows 10/11)

```powershell
# Run PowerShell as Administrator
winget install DigitalOcean.doctl
```

### Option B: Using Chocolatey

```powershell
# Run PowerShell as Administrator
choco install doctl
```

### Option C: Manual Download

```powershell
# Run PowerShell as Administrator
# Download latest release (check for latest version at https://github.com/digitalocean/doctl/releases)
$version = "1.114.0"  # Update with latest version
curl -LO "https://github.com/digitalocean/doctl/releases/download/v$version/doctl-$version-windows-amd64.zip"

# Extract
Expand-Archive .\doctl-$version-windows-amd64.zip

# Move to PATH
Move-Item .\doctl-$version-windows-amd64\doctl.exe C:\Windows\System32\doctl.exe
```

---

## 3. Install Dapr CLI (Optional - for Dapr management)

```powershell
# Run PowerShell as Administrator
# Install Dapr CLI using PowerShell script
irm https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex
```

---

## 4. Verify Installations

```powershell
# Open NEW PowerShell window (to refresh PATH)
# Check kubectl
kubectl version --client --short
# Expected output: v1.xx.x

# Check doctl
doctl version
# Expected output: doctl version 1.xx.x-release

# Check Dapr CLI (if installed)
dapr version
# Expected output: CLI version: 1.xx.x
```

---

## 5. Authenticate with DigitalOcean

```powershell
# Authenticate doctl with your DigitalOcean account
doctl auth init

# This will:
# 1. Open a browser
# 2. Prompt you to log in to DigitalOcean
# 3. Generate an access token
# 4. Display the token to copy

# Copy the token and paste it when prompted
# Output should show: OK
```

**Alternative: Create access token manually**

1. Go to https://cloud.digitalocean.com/account/api/tokens
2. Click "Generate New Token"
3. Name it "DOKS Deployment" and select "Read & Write" scope
4. Click "Generate Token"
5. Copy the token (you won't see it again!)
6. Use it with:

```powershell
doctl auth init --token <paste-token-here>
```

---

## 6. Get Cluster Kubeconfig

```powershell
# Save kubeconfig for your DigitalOcean cluster
# Replace with your actual cluster ID
$clusterId = "bfa88bea-fe4a-ea05-843b-2ae1761e9318"

doctl kubernetes cluster kubeconfig save $clusterId

# Expected output: Notice: added cluster credentials to kubeconfig file for cluster do-nyc1-xxx

# Verify current context
kubectl config current-context
# Expected output: do-nyc1-xxx (your cluster name)
```

**To list all your clusters:**

```powershell
doctl kubernetes cluster list
```

---

## 7. Test Cluster Connectivity

```powershell
# Test connection to your DigitalOcean cluster
kubectl get nodes

# Expected output:
# NAME                   STATUS   ROLES    AGE   VERSION
# pool-xxx1-xxxxx        Ready    <none>   XXd   v1.xx.x
# pool-xxx2-xxxxx        Ready    <none>   XXd   v1.xx.x

# Test Helm
helm list
# Expected output: (empty list or existing deployments)
# NAME    NAMESPACE       REVISION        UPDATED STATUS
```

---

## 8. Troubleshooting

### "kubectl: command not found"

**Problem**: kubectl not in PATH

**Solution**:
```powershell
# Close and reopen PowerShell to refresh PATH
# Or add to PATH manually:
$env:Path += ";C:\Windows\System32"

# For permanent fix, add via System Settings:
# 1. Press Win + R, type "sysdm.cpl"
# 2. Advanced → Environment Variables
# 3. Edit Path → Add → C:\Windows\System32
```

### "doctl: command not found"

**Problem**: doctl not in PATH

**Solution**: Same as kubectl above

### "Cannot connect to cluster"

**Problem**: Kubeconfig not saved or wrong context

**Solution**:
```powershell
# Verify kubeconfig
kubectl config view

# Re-save kubeconfig
doctl kubernetes cluster kubeconfig save bfa88bea-fe4a-ea05-843b-2ae1761e9318

# Switch to correct context
kubectl config use-context do-nyc1-xxx

# Test again
kubectl get nodes
```

### "Unauthorized" or "Authentication failed"

**Problem**: Expired or invalid access token

**Solution**:
```powershell
# Re-authenticate
doctl auth init

# Or set token directly
doctl auth init --token <your-new-token>
```

### "SSL certificate problem"

**Problem**: SSL certificate verification failure

**Solution**:
```powershell
# (Temporary - not recommended for production)
kubectl get nodes --insecure-skip-tls-verify

# For permanent fix, update DigitalOcean CA certificates
# Or use DigitalOcean's kubeconfig which includes proper certificates
```

### "winget command not found"

**Problem**: winget not available (Windows 10 version < 1709)

**Solution**: Use Chocolatey or manual download options

### "chocolatey command not found"

**Problem**: Chocolatey not installed

**Solution**: Install Chocolatey first
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

---

## Next Steps After Installation

Once all tools are installed and `kubectl get nodes` works:

```powershell
# 1. Navigate to Phase_4 directory
cd C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4

# 2. Build and push Docker images
.\scripts\build-and-push-images.ps1 -DockerUsername <your-docker-hub-username>

# 3. Create Kubernetes secrets
.\scripts\create-secrets.ps1

# 4. Deploy to cloud
.\scripts\deploy-to-cloud.ps1 -DockerUsername <your-docker-hub-username>

# 5. Verify deployment
.\scripts\verify-cloud-deployment.ps1
```

---

## Quick Reference Commands

```powershell
# Verify all tools
kubectl version --client --short
doctl version
helm version

# List DigitalOcean clusters
doctl kubernetes cluster list

# Get cluster info
doctl kubernetes cluster get bfa88bea-fe4a-ea05-843b-2ae1761e9318

# Save kubeconfig
doctl kubernetes cluster kubeconfig save bfa88bea-fe4a-ea05-843b-2ae1761e9318

# Check current context
kubectl config current-context

# Get nodes (test connectivity)
kubectl get nodes

# List all pods
kubectl get pods -A

# Check Dapr pods
kubectl get pods -n dapr-system
```

---

**End of Installation Guide**
