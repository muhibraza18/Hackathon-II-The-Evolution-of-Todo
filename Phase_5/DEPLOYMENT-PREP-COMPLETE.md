# DOKS Deployment - Preparation Complete ✅

**Date**: 2026-02-07
**Status**: Ready for deployment after prerequisites are installed

---

## Summary

All deployment preparation files have been created. You can now deploy to DigitalOcean Kubernetes once you install the prerequisites (kubectl, doctl).

---

## Files Created

### Helm Values (Cloud Overrides)

| File | Purpose |
|------|---------|
| `charts/backend/values-doks.yaml` | Backend cloud configuration |
| `charts/frontend/values-doks.yaml` | Frontend cloud configuration with LoadBalancer |
| `charts/consumers/values-doks.yaml` | Consumers cloud configuration |

### Dapr Components

| File | Purpose |
|------|---------|
| `dapr-components/pubsub/redpanda-cloud-pubsub.yaml` | Redpanda Cloud Pub/Sub component |
| `dapr-components/dapr-config-cloud.yaml` | Dapr configuration with mTLS disabled |

### PowerShell Scripts (Windows)

| Script | Purpose |
|--------|---------|
| `scripts/build-and-push-images.ps1` | Build and push Docker images to Docker Hub |
| `scripts/create-secrets.ps1` | Create Kubernetes secrets |
| `scripts/deploy-to-cloud.ps1` | Complete deployment automation |
| `scripts/verify-cloud-deployment.ps1` | Post-deployment verification |

### Documentation

| File | Purpose |
|------|---------|
| `docs/WINDOWS-INSTALLATION-GUIDE.md` | Complete Windows installation guide |
| `scripts/DEPLOYMENT-CHECKLIST.md` | Step-by-step deployment checklist |
| `CLOUD_ACCESS_TEMPLATE.txt` | Template for cloud access credentials |

---

## Next Steps

### Step 1: Install Prerequisites (Windows)

Follow the guide: `docs/WINDOWS-INSTALLATION-GUIDE.md`

**Quick Install Commands:**

```powershell
# Install kubectl via winget
winget install Kubernetes.kubectl

# Install doctl via winget
winget install DigitalOcean.doctl

# Or use Chocolatey
choco install kubernetes-cli doctl
```

### Step 2: Verify Installation

```powershell
# Open NEW PowerShell window
kubectl version --client --short
doctl version
helm version
```

### Step 3: Authenticate & Connect

```powershell
# Authenticate with DigitalOcean
doctl auth init

# Save kubeconfig for your cluster
doctl k8s cluster kubeconfig save bfa88bea-fe4a05-843b-2ae1761e9318

# Test connection
kubectl get nodes
```

### Step 4: Deploy

```powershell
# Navigate to Phase_4
cd "C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4"

# Build and push images (replace with your Docker Hub username)
.\scripts\build-and-push-images.ps1 -DockerUsername <your-docker-hub-username>

# Create secrets
.\scripts\create-secrets.ps1

# Deploy everything
.\scripts\deploy-to-cloud.ps1 -DockerUsername <your-docker-hub-username>

# Verify deployment
.\scripts\verify-cloud-deployment.ps1
```

---

## Values Files Update Required ⚠️

Before deploying, update the placeholder in values files:

**Files to update:**
- `charts/backend/values-doks.yaml`
- `charts/frontend/values-doks.yaml`
- `charts/consumers/values-doks.yaml`

**Replace:**
```
<docker-hub-username>
```

**With:**
```
your-actual-docker-hub-username
```

The deployment script will do this automatically if you use:
```powershell
.\scripts\deploy-to-cloud.ps1 -DockerUsername your-actual-docker-hub-username
```

---

## Secrets Required

You will need these values when running `create-secrets.ps1`:

| Secret | Value |
|--------|-------|
| OpenAI API Key | Your OpenAI API key |
| Auth Secret | `2e7a66444e20fa4fbaf6e20bd06c94eca3ad1ae0aaca54c19f236786d9973328` |
| DB Password | `npg_l3WKQFsvo7uH` |
| Redpanda Username | `todo-phase5` |
| Redpanda Password | `bflLeIafHKGKvshzwRwcIZqvudhMjG` |

---

## Deployment Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| Prerequisites Install | 15-30 min | Install kubectl, doctl |
| Build & Push Images | 10-20 min | Docker images |
| Deploy Applications | 10-15 min | Helm deployments |
| LoadBalancer IP | 5-10 min | DO assigns IP |
| Total | ~45-75 min | End-to-end |

---

## Troubleshooting

**LoadBalancer shows `<pending>`?**
- Wait 5-10 minutes for DigitalOcean to provision
- Run: `kubectl describe svc frontend-service`

**Pods not starting?**
- Check logs: `kubectl logs <pod-name>`
- Describe pod: `kubectl describe pod <pod-name>`

**Can't access Grafana?**
- Port-forward: `kubectl port-forward -n monitoring svc/prometheus-grafana 3001:80`
- Access at: `http://localhost:3001`

---

## Tasks Completed ✅

- [X] T011 - Dapr configuration created
- [X] T012 - Redpanda Cloud Pub/Sub component created
- [X] T022 - Backend values-doks.yaml created
- [X] T023 - Frontend values-doks.yaml created
- [X] T024-T027 - Values files configured
- [X] T106 - Deployment script created
- [X] T107 - Secrets script created
- [X] T108 - Verification script created
- [X] T109 - Demo checklist created
- [X] T112 - Rollback procedures documented
- [X] T114 - Cloud access template created

**Remaining tasks require cluster access and prerequisite installation.**

---

**Ready to deploy once you confirm `kubectl get nodes` works!**
