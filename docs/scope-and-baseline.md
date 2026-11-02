# Scope and inspected Falcone contracts

## Confirmed scope

Provide a first-party Falcone service to analyze logs and errors in **flows, functions and queries**, with architecture, epics and user stories in this repository. This is an additive product capability. There is no evidence that Falcone currently runs Sentry, and this plan does not invent a Sentry migration requirement.

Queries initially means Falcone PostgreSQL/MongoDB data operations, including operations called by flows/functions. It does not mean unrestricted access to every database's server logs. Log-search queries are a separate API concept. LLM prompts/completions, browser replay, full profiling, arbitrary user SQL execution and automatic production remediation are outside the baseline.

## Evidence at Falcone `4b6ef9736cb78deec346537b1c0b8eea8b79c34c`

| Inspected source | Existing behavior | Required preservation/integration |
|---|---|---|
| `docs-site/operations/observability.md` | Prometheus-based metrics; tenant observability, audit, quotas and freshness | Extend investigation UX; do not replace metrics or relabel stale data healthy |
| `observability-metrics-stack.json`, `observability-dashboards.json` | Scope/label contracts; global/tenant/workspace views and bounded cardinality | Separate scope-aware telemetry fields from metric labels; preserve current metric families |
| `observability-audit-event-schema.json`, `observability-audit-pipeline.json` | Canonical governed audit events and Kafka transport | Keep audit as a distinct unsampled governed stream; logs may correlate through authorized adapters |
| `observability-audit-correlation-surface.json` | Scoped correlation with complete/partial/broken/not_found states | Existing audit correlation is not proof that an OTel trace is complete |
| `runtime/flow-monitoring-executor.mjs` | Temporal history translated into ordered `node-status` and `log-line` SSE frames; stable resume sequence | Preserve flow run view and Last-Event-ID behavior; new log tail has its own cursor |
| `runtime/flow-audit-relay.mjs` | Database outbox with Kafka acknowledgement and possible replay after a crash; `AUDIT_UNAVAILABLE` can fail a governed mutation | Do not weaken transactional audit or mislabel at-least-once delivery exactly once |
| `runtime/functions-executor.mjs`, `apps/control-plane/function-executor.mjs` | Activation IDs, status, duration and captured logs; production Knative path and development worker path | Keep activation contracts and distinguish runtime revision/pod/attempt logs |
| `functions-data-console-contract.md` | Activation policies include separate logs/result access, manual rerun and retention; workspace authorization is explicit | Log read does not imply result/source read, rerun permission or access from an actor-type label |
| `runtime/postgres-data-executor.mjs` | Real data execution through workspace connection registry and non-superuser tenant/workspace RLS context | Instrument the trusted adapter, not arbitrary database server capture |
| `runtime/mongo-data-executor.mjs` | Executed adapter plans and opaque public driver errors | Capture safe driver classification/timing; no recursive raw `cause` export |
| `packages/internal-contracts/src/request-log.mjs` and fix-1118 specification | Query-bearing request errors keep normalized pathname and bounded safe metadata, omitting raw message/stack/cause/query material | New telemetry must obey this boundary before persistence, including error collectors and exporters |

These are source observations, not a live deployment audit. Some descriptors still use legacy `openwhisk` names; do not install OpenWhisk or silently rename published contracts based on that label.

## Ownership and non-goals

`falcone-logs` owns ingestion contracts, normalized diagnostic events, error grouping, issue triage, search APIs, alert state and observability-specific retention. Main Falcone owns product routes/console, entitlements, datasource authorization and shared contracts. Producer services own their instrumentation and authoritative execution state. IAM owns identity/roles; secrets owns credentials/key custody; S3 owns object persistence. Existing audit and metering remain governed separately.

The current serverless observability ADR recommends operator-managed backends and approved namespaced export, remains proposed, and does not authorize a new cluster-wide collector. Its OCI amendment distinguishes pod-level stdout/stderr from per-invocation shim logs. Workflow decisions already require shared outbox/inbox/fencing contracts, with owners identified in the main repository. This service consumes those contracts instead of creating another execution protocol.

The previous 20 tenants, 10,000 deployed functions and 100k WebSocket/event messages per second are context, not log-ingestion measurements. Estimate events/second, bytes/second, retention and search concurrency separately.
