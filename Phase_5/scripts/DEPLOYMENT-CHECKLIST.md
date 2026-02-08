# Quick Deployment Checklist - DOKS Cloud Deployment

**Prerequisites**: Complete `docs/WINDOWS-INSTALLATION-GUIDE.md` first

---

## Phase 1: Prerequisites ✅

- [ ] kubectl installed (`kubectl version --client`)
- [ ] doctl installed (`doctl version`)
- [ ] helm installed (`helm version`)
- [ ] Docker Desktop running
- [ ] Docker Hub account created

---

## Phase 2: Cluster Connection ✅

- [ ] doctl authenticated (`doctl auth init`)
- [ ] Kubeconfig saved (`doctl k8s cluster kubeconfig save bfa88bea-fe4a-ea05-843b-2ae1761e9318`)
- [ ] Cluster connected (`kubectl get nodes` shows Ready)
- [ ] Monitoring namespace created (`kubectl create namespace monitoring`)

---

## Phase 3: Build & Push Images ✅

- [ ] Images built:
  ```powershell
  .\scripts\build-and-push-images.ps1 -DockerUsername <your-username>
  ```
- [ ] Backend image pushed to Docker Hub
- [ ] Frontend image pushed to Docker Hub
- [ ] Consumers image pushed to Docker Hub

---

## Phase 4: Create Secrets ✅

- [ ] Secrets created:
  ```powershell
  .\scripts\create-secrets.ps1
  ```
- [ ] OpenAI API key provided
- [ ] Auth secret provided
- [ ] Database password provided
- [ ] Redpanda password provided
- [ ] Secrets verified (`kubectl get secrets`)

---

## Phase 5: Deploy to Cloud ✅

- [ ] Deploy applications:
  ```powershell
  .\scripts\deploy-to-cloud.ps1 -DockerUsername <your-username>
  ```
- [ ] Backend deployed (`helm list` shows backend)
- [ ] Frontend deployed (`helm list` shows frontend)
- [ ] Consumers deployed (`helm list` shows consumers)
- [ ] Monitoring deployed (`helm list -n monitoring` shows prometheus)
- [ ] Logging deployed (`helm list -n monitoring` shows loki)

---

## Phase 6: Verify Deployment ✅

- [ ] Verification passed:
  ```powershell
  .\scripts\verify-cloud-deployment.ps1
  ```
- [ ] All pods Running (`kubectl get pods`)
- [ ] LoadBalancer IP assigned
- [ ] Frontend accessible in browser
- [ ] Backend health endpoint responding
- [ ] Dapr sidecars injected (2/2 containers)
- [ ] Grafana accessible
- [ ] Prometheus metrics visible

---

## Phase 7: Test Features ✅

### Access Verification
- [ ] Frontend loads at http://<external-ip>:3000
- [ ] Login page displays
- [ ] Can register new user
- [ ] Can login with existing user

### Core Features
- [ ] Create task works
- [ ] View tasks works
- [ ] Edit task works
- [ ] Delete task works
- [ ] Mark complete works

### Advanced Features
- [ ] Set due date works
- [ ] Set priority works
- [ ] Add tags works
- [ ] Search tasks works
- [ ] Filter tasks works

### Chat Feature
- [ ] Chat interface loads
- [ ] AI responds to queries
- [ ] Create task via chat works

### Reminders
- [ ] Task with due date creates reminder
- [ ] Reminder visible in API
- [ ] Events published to Redpanda

---

## Phase 8: Monitor & Logging ✅

### Grafana Setup
- [ ] Grafana accessible (port-forward or LoadBalancer)
- [ ] Logged in with admin password
- [ ] Prometheus data source configured
- [ ] Kubernetes dashboards imported
  - [ ] Cluster Overview (ID: 7249)
  - [ ] Pod Metrics (ID: 315)

### Loki Setup
- [ ] Loki data source added in Grafana
- [ ] Can query logs with `{app="backend-service"}`
- [ ] Logs show recent activity

---

## Phase 9: Documentation ✅

- [ ] CLOUD_ACCESS.txt updated with actual IPs
- [ ] Grafana password saved securely
- [ ] LoadBalancer IP documented
- [ ] Demo script prepared (≤90 seconds)

---

## Troubleshooting Quick Commands

```powershell
# Check all pods
kubectl get pods -A

# Check pod logs
kubectl logs -l app=backend-service --tail=50

# Check Dapr logs
kubectl logs -l app=backend-service -c daprd --tail=50

# Describe failing pod
kubectl describe pod <pod-name>

# Get LoadBalancer IP
kubectl get svc frontend-service

# Port-forward for testing
kubectl port-forward svc/frontend-service 3000:3000

# Restart deployment
kubectl rollout restart deployment backend-service

# Check secrets
kubectl get secrets
kubectl describe secret todo-backend-secrets
```

---

## Success Criteria

✅ **Deployment successful when:**
- All pods show Running status
- Frontend accessible at http://<external-ip>:3000
- User can login and create tasks
- Grafana dashboards show metrics
- Loki shows logs in queries
- Redpanda Cloud shows events

---

**Expected Timeline**: 1-2 hours (after prerequisites installed)
