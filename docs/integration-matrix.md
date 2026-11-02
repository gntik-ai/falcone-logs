# Falcone integration and repository ownership

This plan publishes only in `gntik-ai/falcone-logs`. Producer, console, shared-library and deployment changes need explicit handoffs in their owning repositories; no sibling implementation or ADR is silently changed.

| Owner/system | Integration | Required evidence |
|---|---|---|
| Main Falcone control plane/API gateway | Additive diagnostic APIs and project configuration; preserve existing audit/metrics/routes/error precedence | Current route/OpenAPI fixtures, authenticated scope, gateway host/path/log hygiene |
| Main Falcone console | Unified Logs/Errors/Traces views and entry points from run, activation and datasource pages | Current tenant/workspace context, separate logs/results/source rights, accessible and escaped rendering |
| `falcone-workflow` and transitional Temporal monitoring | Run/node-occurrence/attempt events, linked trace segments, durable timeline overlay | Existing SSE framing/resume; long waits and retries; authoritative incidents/status remain workflow-owned |
| `falcone-serverless` and current Knative adapters | Scoped host/shim logs, activation/revision/runtime-mode and termination evidence | Respect proposed ADR 0008 placement and OCI amendment; pod-level logs are not automatically invocation logs |
| Falcone PostgreSQL/MongoDB adapters | Query operation shapes, timing/error classification and execution lineage | No bind values/rows/connection strings; distinguish client/server/pool timing; preserve RLS/tenant rules |
| `falcone-iam` / current Keycloak | User/workload authentication and fine-grained ingestion/read/triage/export/source permissions | No second login/team directory; enterprise federation stays in IAM; fail closed on invalid scope |
| `falcone-secrets` / current OpenBao | Ingest/integration credentials, signing keys and protected storage access | Accepted secrets ADR 0002, bounded key caching/rotation and independent recovery |
| `falcone-s3` / current storage façade | Archive, debug artifacts, exports and backups through explicit native/external bindings | Immutable manifest/checksum/version identity, scoped retrieval, retention and actual provider capabilities |
| Kafka/eventing and shared primitives | Diagnostic topics, durable inbox/outbox and alert intent | Consume shared Falcone primitive contracts; do not create a rival workflow/outbox protocol |
| Prometheus/Grafana | Existing infrastructure/usage metrics plus ingestion/search/loss health | Bounded labels; keep platform-global metrics separate; diagnostics do not replace authoritative rates/billing |
| Audit correlation/export | Authorized linked governed evidence | Preserve canonical schema, permissions, partial/broken states and audit transaction failure semantics |
| Quotas/entitlements | Ingest bytes/events, storage days, search scans, exports, tail connections and notification budgets | Falcone owns definitions; logs reports measured accepted/dropped/retained usage with idempotent accounting |
| Charts/platform operations | Approved namespaced collection and operator-managed backends | No mandatory privileged DaemonSet/operator/hostPath/eBPF; actual endpoints, permissions and budgets supplied |
| Optional notifications/GitHub/model integrations | User-configured scoped outgoing actions | Explicit destination/data policy, dry run, dedupe, audit and revocation; no actions enabled by this planning publication |

## Shared contract alignment

Current workflow decisions identify Falcone's shared outbox/inbox/fencing work (main repository issues #1331, #1343, #1356, #1361 and #1381; related #1349). `ctr-worker-execution-api` v1 ownership is in falcone-serverless #124/#130; checkpoint ownership is defined by its JOB-01.t1 plan. These are source references for coordination, not evidence the contracts have been deployed. Confirm delivered paths/versions and transaction participation before integrating.

Use stable execution/source identities to align instrumentation with those contracts. Error grouping and analytics projection are new logs-owned behavior; workflow state, retries, leases and durable run history are not. Existing logs may be ingested through compatibility adapters while current Temporal/Knative services continue running.

## Product entry points

New API families are proposed under Falcone's published versioning convention for log search/tail, errors/triage, trace lookup, releases/artifacts, saved views and alert policy. Exact paths are frozen in LOG-CON-001/LOG-UI-003 rather than presented here as existing endpoints. Existing flow SSE and activation responses retain their shapes; opt-in log references/links are additive. Search cursors and workflow event cursors are distinct typed values.

No button in the logs UI may implicitly rerun a function, execute a database statement, resume a workflow or create an external ticket. Such actions call the owning service through separately authorized, auditable commands with the existing confirmation/idempotency semantics.
