# Research & Architecture Decisions: Local E2E Testing & Polish

**Feature**: 001-local-e2e-polish
**Created**: 2026-02-02

## Decision: Testing Depth Approach

**Decision**: Use primarily manual testing with lightweight automated health checks via kubectl and curl.

**Rationale**:
- Fastest path to validation given hackathon time constraints
- Manual testing provides immediate feedback and observation capabilities
- Lightweight automated checks (kubectl get pods, curl health) provide quick regression detection
- Setting up full pytest framework would take significant time without proportional value
- Focus on validating functionality rather than test infrastructure

**Alternatives Considered**:

| Option | Advantages | Disadvantages | Decision |
|--------|------------|---------------|----------|
| Manual + lightweight automated | Fast execution, adequate coverage, easy to document | Less repeatable than full automation | **SELECTED** |
| Full automated with pytest | Repeatable, CI/CD ready, comprehensive coverage | Time-intensive setup, maintenance overhead | Not selected - time constraint |
| Manual only | Simplest approach | Slow for repeated validation, prone to human error | Not selected - need some automation |

**Implementation Notes**:
- Create structured test scenario checklist
- Use kubectl commands for automated health checks
- Document expected results for each manual test step
- Capture log excerpts for verification evidence

---

## Decision: Log Level & Format

**Decision**: Use INFO level with structured JSON logging, DEBUG enabled via environment variable.

**Rationale**:
- INFO level provides production-like visibility without excessive noise
- JSON format enables log parsing and tool integration
- DEBUG available via ENV variable for deep troubleshooting when needed
- Balances observability with log volume for hackathon demo

**Alternatives Considered**:

| Option | Advantages | Disadvantages | Decision |
|--------|------------|---------------|----------|
| INFO + JSON | Production-like, tool-friendly, balanced volume | Less human-readable than text | **SELECTED** |
| DEBUG + text | Maximum visibility, human-readable | Noisy, hard to parse, large volume | Not selected - too noisy |
| INFO + text | Simpler, human-readable | Not tool-friendly, harder to analyze | Not selected - less flexible |
| DEBUG + JSON | Maximum detail with structure | Very high volume, resource intensive | Not selected - overkill |

**Implementation Notes**:
- Backend: Use Python `structlog` for structured JSON logging
- Default level: INFO
- Set LOG_LEVEL=DEBUG for verbose output
- Include: timestamp, level, component, request_id, message, context
- Consumers: Same pattern for consistency

---

## Decision: Error Handling Strategy

**Decision**: Graceful degradation with user-friendly UI messages + detailed backend logging.

**Rationale**:
- Users see actionable, non-technical error messages
- Developers get full stack traces and context in logs
- Balances user experience with debugging visibility
- Demonstrates mature error handling for hackathon judges

**Alternatives Considered**:

| Option | Advantages | Disadvantages | Decision |
|--------|------------|---------------|----------|
| Graceful UI + detailed logs | Good UX, full visibility for debugging | More complex to implement | **SELECTED** |
| Crash-fast | Maximum visibility, fail-fast principle | Poor UX, confusing for users | Not selected - bad demo experience |
| Silent failures | Best perceived UX | Impossible to debug, misleading | Not selected - unacceptable |
| Full stack traces in UI | Maximum transparency | Technical, overwhelming for users | Not selected - bad UX |

**Implementation Notes**:
- Frontend: Catch errors and display user-friendly messages
- Backend: Log full error with stack trace, request context
- Use HTTP status codes appropriately (400, 404, 500)
- Include request ID for log correlation
- Common error message patterns:
  - "Task creation failed. Please try again."
  - "Connection error. Check your internet and retry."
  - "Invalid input. Please check the form and try again."

---

## Decision: Demo Readiness Approach

**Decision**: 90-second scripted demo with pre-captured commands and log excerpts.

**Rationale**:
- Focused demo maximizes impact within short attention span
- Pre-captured commands/log ensure reliability during live demo
- 90 seconds aligns with hackathon pitch video expectations
- Scripted flow ensures all key features are shown

**Alternatives Considered**:

| Option | Advantages | Disadvantages | Decision |
|--------|------------|---------------|----------|
| 90-second scripted demo | Focused, reliable, impactful | Less authentic than ad-hoc | **SELECTED** |
| Live unscripted demo | Authentic, impressive | Risky, may fail, unpredictable | Not selected - too risky |
| Comprehensive walkthrough | Shows all features | Too long, loses attention | Not selected - attention span |
| Screen recording only | Guaranteed success | Less impressive than live | Not selected - less engagement |

**Implementation Notes**:
- Script: ~8-10 discrete steps
- Target time: 90 seconds
- Include: login → create recurring task → show event flow → reminder scheduling
- Pre-capture: kubectl commands, log excerpts, screenshots
- Provide fallback: screenshots for each step in README
- Timing breakdown:
  - 0:00-0:15: Introduction and login (15s)
  - 0:15-0:35: Create recurring task with priority/tag (20s)
  - 0:35-0:55: Show event flow in logs (20s)
  - 0:55-0:75: Schedule reminder and show Dapr Jobs (20s)
  - 0:75-0:90: Summary and conclusion (15s)

---

## Technology Stack Considerations

### Existing Components (from Phase V Steps 1-4)
- **Frontend**: React/Next.js with ChatKit
- **Backend**: Python FastAPI with async/await
- **Database**: PostgreSQL (Neon or local)
- **Pub/Sub**: Kafka/Redpanda via Dapr
- **Orchestration**: Dapr (Pub/Sub, State, Jobs, Secrets)
- **Deployment**: Minikube with Helm charts

### Testing & Validation Tools
- **kubectl**: Pod/service inspection and log retrieval
- **curl**: Health endpoint and API testing
- **Dapr CLI**: Sidecar and component verification
- **Minikube CLI**: Service URL exposure
- **Browser DevTools**: Frontend error observation

### Logging & Monitoring
- **structlog**: Python structured JSON logging
- **Dapr sidecar logs**: Dapr system observations
- **kubectl logs**: Pod log aggregation

---

## Best Practices Applied

1. **Test-Driven Validation**: Each test scenario defined before execution
2. **Smoke Testing**: Quick health checks after every fix
3. **Log-Driven Debugging**: All errors logged with full context
4. **User-Centric Error Messages**: Error text written for non-technical users
5. **Documentation-First**: README and troubleshooting written before final validation
6. **Demo-Ready Preparation**: Script and captures prepared before final demo

---

## Open Questions Resolved

1. **Q**: Should we add pytest for automated testing?
   **A**: No - manual + lightweight automated provides adequate coverage for hackathon timeline

2. **Q**: What log level for production-like demo?
   **A**: INFO with JSON format - balances visibility with noise

3. **Q**: How technical should error messages be?
   **A**: Non-technical in UI, full details in logs

4. **Q**: Live demo or pre-recorded?
   **A**: Live scripted demo with pre-captured fallbacks

5. **Q**: Include performance testing?
   **A**: No - functional correctness only per spec constraints
