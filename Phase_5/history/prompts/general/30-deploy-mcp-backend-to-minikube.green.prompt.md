---
id: 30
title: deploy-mcp-backend-to-minikube
stage: green
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Wajahat traders
command: /sp.clarify
labels:
  - docker
  - minikube
  - kubernetes
  - deployment
  - mcp
  - backend
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\backend\mcp-deployment.yaml
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\backend\Dockerfile
  - C:\Users\Wajahat traders\Desktop\Quarter 4\Hackathon-2\Phase_4\backend\db\connection.py
tests_yaml:
  - kubectl get pods
  - kubectl logs -l app=mcp-server
  - minikube status
---

# Deploy MCP Backend to Minikube

## Prompt Text
```
You shift all perfect but push them to docker container read the tasks specs for better understanding then pus them to minukube
```

## Response Text

Successfully deployed the MCP backend to Minikube:

1. Built the Docker image: `mcp-backend:latest` from the backend directory
2. Started Minikube cluster with Docker driver and 3072MB memory
3. Loaded the Docker image into Minikube
4. Created and applied Kubernetes deployment for the MCP server
5. Created required database secret for the deployment
6. Verified the pod is running successfully with no SSL errors
7. Confirmed the service is accessible within the cluster

The MCP server is now running in Minikube with the asyncpg SSL fix properly implemented, showing healthy startup logs and no connection errors.

## Outcome

MCP server successfully deployed to Minikube with proper asyncpg SSL configuration.

## Evaluation

Deployment completed successfully with all components running properly and no SSL-related errors.