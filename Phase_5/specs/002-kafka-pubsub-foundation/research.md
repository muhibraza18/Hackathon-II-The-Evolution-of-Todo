# Research: Event-Driven Foundation Implementation

## Decision: Kafka Implementation Choice
**Rationale**: Using Strimzi operator for local Kafka setup on Minikube to provide the most educational value and production-like setup for Kubernetes environment. This approach provides learning opportunities for Kafka administration while maintaining compatibility with cloud deployments.
**Alternatives considered**:
- Strimzi operator: Kubernetes-native, educational value, complex setup
- Redpanda Docker: Simple setup, single binary, less learning value
- Redpanda Cloud: Managed service, no local learning, defers to later phase

## Decision: Event Schema Format
**Rationale**: Using plain JSON format for event schemas to maintain simplicity and compatibility with both Kafka and future Dapr Pub/Sub implementations. This reduces complexity while maintaining flexibility.
**Alternatives considered**:
- Plain JSON: Simple, flexible, less type safety
- Avro with schema registry: Strong typing, schema evolution, increased complexity

## Decision: Producer Library
**Rationale**: Using aiokafka directly for the producer wrapper to maintain performance while creating an abstraction layer that can be swapped for Dapr in the future. This provides the right balance of performance and portability.
**Alternatives considered**:
- aiokafka direct: High performance, direct Kafka dependency
- Dapr-ready HTTP wrapper: Portable, lower performance initially

## Decision: Consumer Deployment Model
**Rationale**: Using separate deployments per consumer service to provide better isolation, independent scaling, and fault tolerance. Each consumer can be scaled independently based on load.
**Alternatives considered**:
- Separate deployments: Better isolation, more resources
- Single multi-consumer pod: Resource efficient, less isolation

## Decision: Topic Partitioning
**Rationale**: Using single partition for local Minikube setup to maintain simplicity while planning for multiple partitions in production environments.
**Alternatives considered**:
- Single partition: Simple, limited scalability
- Multiple partitions: Scalable, more complex

## Decision: Error Handling
**Rationale**: Implementing simple retry mechanism with configurable attempts for local development, with plans to enhance with dead-letter queues in production.
**Alternatives considered**:
- Simple retry: Simple, basic reliability
- Dead-letter queue: Advanced, higher reliability, more complexity