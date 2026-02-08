# Data Model: Local Minikube + Dapr Deployment for Todo AI Chatbot

## Kubernetes Resources

### MinikubeCluster
- **driver**: String (docker, hyperv, virtualbox) - defaults to "docker"
- **memory**: Integer (MiB) - defaults to 3072, range 2048-4096
- **cpus**: Integer - defaults to 4, range 2-8
- **disk_size**: String - defaults to "20g"
- **kubernetes_version**: String - matches local kubectl version

### DaprSystem
- **control_plane_pods**: List[String] - sidecar-injector, operator, placement, sentry services
- **sidecar_injection_enabled**: Boolean - whether automatic sidecar injection is enabled
- **dapr_runtime_version**: String - version of Dapr runtime installed
- **namespaces**: List[String] - dapr-system namespace and application namespaces

### KafkaCluster (Strimzi-based)
- **kafka_replicas**: Integer - number of Kafka broker replicas (defaults to 1 for local)
- **zookeeper_replicas**: Integer - number of Zookeeper replicas (defaults to 1 for local)
- **storage_type**: String - "ephemeral" for local development
- **topics**: List[TopicConfig] - configured topics (task-events, reminders, task-updates)
- **listeners**: List[ListenerConfig] - internal/external listener configurations

### DaprComponents
- **pubsub_component**: PubSubConfig - configuration for Kafka pubsub
  - type: "pubsub.kafka"
  - version: "v1"
  - brokers: List[String] - Kafka broker addresses
  - auth_required: Boolean - whether authentication is required
- **state_store_component**: StateStoreConfig - configuration for PostgreSQL state store
  - type: "state.postgresql"
  - version: "v1"
  - connectionString: SecretReference - reference to DB connection string
  - actorStateStore: Boolean - whether to use for actor state
- **secret_store_component**: SecretStoreConfig - configuration for Kubernetes secrets
  - type: "secretstores.kubernetes"
  - version: "v1"
- **job_component**: JobConfig - configuration for job scheduling
  - type: "bindings.cron"
  - version: "v1"
  - schedule: String - cron expression for job execution

### AppDeployments
- **backend_deployment**: DeploymentConfig
  - name: "todo-backend"
  - replicas: 1
  - dapr_annotations: Map[String, String] - Dapr sidecar configuration
  - resources: ResourceRequirements - CPU/memory requests/limits
  - service_type: "LoadBalancer" for local access
- **consumer_deployments**: List[DeploymentConfig] - recurring, notification, audit consumers
  - name: "todo-consumer-*"
  - dapr_annotations: Map[String, String] - Dapr sidecar configuration
  - resource_requirements: ResourceRequirements

## Dapr Integration Entities

### DaprSidecarConfig
- **enabled**: Boolean - whether Dapr sidecar is enabled
- **app_id**: String - unique identifier for the application
- **app_port**: Integer - port the application listens on
- **app_protocol**: String - protocol used by the application (http/grpc)
- **config**: String - Dapr configuration name
- **enable_metrics**: Boolean - whether to enable metrics collection
- **enable_tracing**: Boolean - whether to enable distributed tracing

### DaprPubSubMessage
- **data**: JSON - message payload
- **datacontenttype**: String - content type of the data
- **topic**: String - topic to publish to
- **pubsubname**: String - name of the pubsub component
- **metadata**: Map[String, String] - optional metadata for the message

### DaprStateOperation
- **key**: String - key for the state operation
- **value**: JSON - value to store or update
- **etag**: String - optional etag for concurrency control
- **options**: StateOptions - consistency, concurrency options
- **operation**: String - operation type (upsert, get, delete, transaction)

### DaprSecretRequest
- **store_name**: String - name of the secret store
- **key**: String - key of the secret to retrieve
- **metadata**: Map[String, String] - optional metadata for the request

### DaprServiceInvocation
- **appId**: String - ID of the target application
- **methodName**: String - name of the method to invoke
- **httpVerb**: String - HTTP verb to use (GET, POST, PUT, DELETE)
- **data**: JSON - optional data to send with the request
- **metadata**: Map[String, String] - optional metadata for the invocation

## Service Configuration

### ServiceDefinition
- **name**: String - name of the service
- **type**: String - service type (ClusterIP, NodePort, LoadBalancer)
- **ports**: List[PortConfig] - port configurations
- **selector**: Map[String, String] - labels to select pods
- **annotations**: Map[String, String] - service annotations including Dapr

### PortConfig
- **port**: Integer - port number
- **targetPort**: Integer - target port on the pod
- **protocol**: String - protocol (TCP, UDP)
- **name**: String - optional name for the port

## Helm Chart Configuration

### HelmValues
- **global**: Map[String, Any] - global configuration values
- **dapr**: DaprConfig - Dapr-specific configuration
  - enabled: Boolean - whether Dapr is enabled
  - appId: String - application ID for Dapr
  - appPort: Integer - application port for Dapr
- **resources**: ResourceRequirements - resource allocation for pods
- **service**: ServiceConfig - service configuration
  - type: String - service type
  - port: Integer - service port
- **replicaCount**: Integer - number of pod replicas

### ResourceRequirements
- **requests**: ResourceLimits - minimum resource requirements
  - cpu: String - CPU request (e.g., "100m")
  - memory: String - memory request (e.g., "128Mi")
- **limits**: ResourceLimits - maximum resource limits
  - cpu: String - CPU limit
  - memory: String - memory limit

## Deployment Verification

### HealthStatus
- **service_name**: String - name of the service
- **status**: String - status (healthy, unhealthy, unknown)
- **dapr_sidecar**: Boolean - whether Dapr sidecar is healthy
- **ready_pods**: Integer - number of ready pods
- **total_pods**: Integer - total number of pods
- **last_checked**: DateTime - timestamp of last health check

### VerificationResult
- **test_name**: String - name of the test performed
- **passed**: Boolean - whether the test passed
- **details**: String - details about the test result
- **timestamp**: DateTime - when the test was performed
- **component**: String - component being tested (dapr, kafka, app, etc.)