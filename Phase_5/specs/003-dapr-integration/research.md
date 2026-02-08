# Research: Dapr Integration for Todo AI Chatbot

## Decision: HTTP vs gRPC for Dapr API Calls
**Rationale**: Using HTTP for Dapr API calls to maintain simplicity and broad compatibility. HTTP is easier to debug and works well with existing Python HTTP libraries like httpx/requests. For the scope of this project, the performance difference between HTTP and gRPC is negligible compared to the developer experience benefits.
**Alternatives considered**:
- HTTP: Simpler implementation, easier debugging, broader tool support
- gRPC: Potentially better performance, more complex client setup and debugging

## Decision: Pub/Sub Component Type
**Rationale**: Using Kafka as the Dapr Pub/Sub component to maintain consistency with Phase V Step 2 implementation. This allows for seamless migration without changing the underlying messaging system, reducing risk and complexity during the transition.
**Alternatives considered**:
- Kafka: Consistent with existing implementation, proven at scale, enterprise-grade features
- Redis: Simpler local setup, faster for basic pub/sub, less robust for complex event processing

## Decision: State Store Choice
**Rationale**: Using PostgreSQL as the Dapr state store to maintain data persistence and consistency with existing database. This provides ACID properties and reliable storage for conversation state while minimizing changes to the data layer.
**Alternatives considered**:
- PostgreSQL: Persistent storage, ACID compliance, fits existing architecture
- Redis: Higher performance for cache-like operations, potential data loss on restart

## Decision: Jobs API vs Cron Bindings
**Rationale**: Using Dapr Jobs API for reminders to achieve exact-time scheduling without polling. This provides precise timing for due date reminders and aligns with the requirement for exact-time execution without polling mechanisms.
**Alternatives considered**:
- Jobs API: Exact timing, event-driven, newer feature requiring more setup
- Cron bindings: Proven approach, polling-based, simpler for basic scheduling

## Decision: Secret Store
**Rationale**: Using Kubernetes secrets as the Dapr secret store for native integration with the Kubernetes environment and simplicity. This leverages existing Kubernetes security patterns without adding additional infrastructure complexity.
**Alternatives considered**:
- Kubernetes secrets: Native integration, simple setup, standard Kubernetes approach
- HashiCorp Vault: Advanced security features, more complex setup and operations

## Decision: Sidecar Resource Limits
**Rationale**: Setting conservative but adequate resource limits (200m CPU, 256Mi memory requests; 500m CPU, 512Mi memory limits) to ensure stable operation on Minikube while maintaining good performance. This provides a good balance between stability and resource utilization.
**Tradeoffs**: Stability on resource-constrained environments vs performance capabilities

## Decision: Migration Strategy
**Rationale**: Implementing a gradual migration approach where Dapr APIs are introduced alongside existing infrastructure calls, allowing for gradual transition while maintaining functionality. This reduces risk and allows for rollback if issues arise.
**Alternatives considered**:
- Gradual migration: Lower risk, allows phased rollout, more complex temporarily
- Big bang migration: Faster completion, higher risk, difficult to rollback

## Dapr Component Configuration Best Practices
Based on research of Dapr documentation and best practices:

1. **Component YAML Structure**: Components should be organized in a dapr-components/ directory with subdirectories for each component type (pubsub, state, secrets, etc.)

2. **Secret Management**: Sensitive information like Kafka brokers, database connection strings should be stored in Kubernetes secrets and referenced in component configurations using secretKeyRef

3. **Sidecar Injection**: Use Kubernetes annotations in deployment manifests to enable automatic Dapr sidecar injection

4. **Service Invocation**: Use Dapr's service invocation with application-specific app-ids to enable resilient communication with built-in retries and circuit breakers

5. **State Store Partitions**: For PostgreSQL state store, consider using the 'table' metadata property to specify which table to use for different types of state

## Dapr API Usage Patterns
Based on research of Dapr Python SDK and HTTP API patterns:

1. **Publish Events**: Use POST to `http://localhost:3500/v1.0/publish/{pubsub-name}/{topic}` for publishing messages

2. **Subscribe to Events**: Implement webhook endpoints that Dapr can call when messages arrive, using the `/dapr/subscribe` endpoint to define subscriptions

3. **State Operations**: Use GET/POST to `http://localhost:3500/v1.0/state/{statestore-name}` for state management

4. **Secret Retrieval**: Use GET to `http://localhost:3500/v1.0/secrets/{secret-store-name}/{key}` for secure secret access

5. **Service Invocation**: Use POST to `http://localhost:3500/v1.0/invoke/{app-id}/method/{method}` for service-to-service communication

## Potential Challenges and Solutions

1. **Local Development Setup**: Dapr requires a Kubernetes environment or Dapr standalone mode for full functionality. Solution: Document both approaches with clear instructions for developers.

2. **Error Handling**: Dapr API calls can fail if the sidecar is unavailable. Solution: Implement proper error handling with fallback mechanisms or graceful degradation.

3. **Debugging Complexity**: Additional layer with Dapr sidecars can complicate debugging. Solution: Ensure proper logging and monitoring of Dapr API calls.

4. **Migration Complexity**: Replacing existing infrastructure calls requires careful refactoring. Solution: Implement behind feature flags initially and gradually enable.

## Testing Strategies for Dapr Integration

1. **Unit Testing**: Mock Dapr HTTP responses to test application logic without requiring Dapr runtime
2. **Integration Testing**: Use Dapr's test containers or local Dapr runtime for full integration tests
3. **End-to-End Testing**: Deploy to Minikube with Dapr to validate complete functionality
4. **Chaos Testing**: Test application behavior when Dapr sidecars are unavailable or slow