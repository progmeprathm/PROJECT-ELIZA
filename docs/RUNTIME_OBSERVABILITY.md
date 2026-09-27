# Runtime Observability

## 1. Explicit Telemetry
The `ecos/observability` framework formalizes telemetry for E.L.I.Z.A. 
- **`metrics.py`**: Tracks live execution statistics (`RuntimeMetrics`), including replan counts and context token limits, via counters and gauges.
- **`tracing.py`**: Serializes `RuntimeEvent` output arrays (`RuntimeTrace`), yielding perfect point-in-time debugging logs for every cycle of the multi-agent decision path.

## 2. Diagnostic Interception
`RuntimeDiagnostics` runs passively alongside the core loop, scanning for anomalies such as high memory pollution or recurring execution loops (excessive replans), rendering warnings cleanly without disrupting execution.

## 3. Interface Integration
The emitted logs are fully JSON-serializable, enabling future integration directly into the React+Vite E.L.I.Z.A. Studio UI components without rewriting backend parsing logic.
