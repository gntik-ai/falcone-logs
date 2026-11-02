# Functional requirements

Baseline: 2026-11-02. These are target requirements, not implemented features. Every requirement traces to one user story. Read with [architecture](architecture.md), [telemetry](telemetry-contract.md), [privacy](security-and-privacy.md) and [integration ownership](integration-matrix.md).

## Falcone contracts and product boundaries

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-CON-001-1 | The project must inventory deployed log/error sources, flow SSE, activation policies, query adapters, audit and metric contracts against a pinned Falcone revision. | LOG-CON-001 |
| FR-LOG-CON-001-2 | Existing public schemas, scope checks, error precedence and stream resume behavior must remain covered by compatibility fixtures. | LOG-CON-001 |
| FR-LOG-CON-002-1 | Logs must own investigation/error state while IAM, secrets, S3, workflow, runtime, audit and metering retain their existing authorities. | LOG-CON-002 |
| FR-LOG-CON-002-2 | Every producer integration must identify its owning repository and the versioned scope, lineage and delivery contracts it consumes. | LOG-CON-002 |
| FR-LOG-CON-003-1 | Dependency intake must pin component versions/licenses and distinguish open-source, source-available and enterprise-only code before reuse. | LOG-CON-003 |
| FR-LOG-CON-003-2 | Capacity decisions must measure telemetry rates, bytes, cardinality, retention and query concurrency independently from application message counts. | LOG-CON-003 |

## Ingestion and SDK compatibility

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-ING-001-1 | Ingestion must validate schema, source authority, size/decompression limits and mandatory redaction before any persistent queue. | LOG-ING-001 |
| FR-LOG-ING-001-2 | Durable acceptance must follow the configured broker acknowledgement while preserving protocol-specific success, partial-success and retry responses. | LOG-ING-001 |
| FR-LOG-ING-002-1 | SDK adapters must emit versioned trusted Falcone context and bounded logs/errors using pinned supported runtime/library versions. | LOG-ING-002 |
| FR-LOG-ING-002-2 | Any Sentry compatibility endpoint must advertise tested envelope item types and SDK versions and reject unsupported items explicitly. | LOG-ING-002 |
| FR-LOG-ING-003-1 | Producer/gateway buffers and retries must be bounded by bytes, time and policy, with explicit accepted/rejected/sampled/dropped reasons. | LOG-ING-003 |
| FR-LOG-ING-003-2 | Application diagnostics must export asynchronously without changing execution results, while existing governed audit blocking semantics remain intact. | LOG-ING-003 |

## Identity, tenancy and access

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-TEN-001-1 | All management/query operations must authenticate through Falcone IAM and authorize tenant/workspace/resource/action scope. | LOG-TEN-001 |
| FR-LOG-TEN-001-2 | Log read, error read, source-artifact read, triage, export, destination configuration and platform investigation must be distinct permissions. | LOG-TEN-001 |
| FR-LOG-TEN-002-1 | Producer enrollment must bind a source/project to verified tenant/workspace ownership, resource grants and allowed signals. | LOG-TEN-002 |
| FR-LOG-TEN-002-2 | Reserved identity fields must be supplied or verified by trusted host/dispatch adapters, with conflicting untrusted attributes rejected or isolated. | LOG-TEN-002 |
| FR-LOG-TEN-003-1 | Every detail, search, facet, aggregate, join, cursor, tail, artifact and export must enforce authorized scope before returning data. | LOG-TEN-003 |
| FR-LOG-TEN-003-2 | Backend roles, query compilation and caches must prevent arbitrary SQL/table-function access and cross-scope data reuse. | LOG-TEN-003 |

## Privacy and collection controls

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-PRV-001-1 | The pipeline must apply allowlists and redaction before Kafka, persistent queues, DLQs, archives and internal diagnostic logging. | LOG-PRV-001 |
| FR-LOG-PRV-001-2 | Query-bearing request errors must preserve fix-1118 by omitting raw exception messages, stacks, causes and URL/query material. | LOG-PRV-001 |
| FR-LOG-PRV-002-1 | Default policies must exclude request/response bodies, query parameters/results, documents, vectors, secrets and LLM content from telemetry. | LOG-PRV-002 |
| FR-LOG-PRV-002-2 | Field exceptions, pseudonymous user grouping and source/debug capture must be explicit scoped policies with retention and audit. | LOG-PRV-002 |
| FR-LOG-PRV-003-1 | Log/source/comment rendering and exports must neutralize script, control-character and spreadsheet-formula injection. | LOG-PRV-003 |
| FR-LOG-PRV-003-2 | Parsers and enrichment jobs must enforce time/memory/archive limits and prohibit execution of uploaded code or arbitrary network fetch. | LOG-PRV-003 |

## Telemetry schema and execution correlation

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-COR-001-1 | The event contract must define scoped source identity, signal/time fields, execution lineage, content policy and quality metadata. | LOG-COR-001 |
| FR-LOG-COR-001-2 | Adapters must preserve original public contracts while recording normalized schema/version and trusted versus reported fields. | LOG-COR-001 |
| FR-LOG-COR-002-1 | Trusted adapters must propagate W3C trace context and Falcone correlation/causation IDs across requests, messages and runtime calls. | LOG-COR-002 |
| FR-LOG-COR-002-2 | Long-running or asynchronous work must use bounded trace segments and explicit links rather than requiring one indefinitely open span. | LOG-COR-002 |
| FR-LOG-COR-003-1 | Flow investigation must distinguish run, node occurrence, loop/map iteration and retry attempt and link authoritative status to diagnostic evidence. | LOG-COR-003 |
| FR-LOG-COR-003-2 | Existing flow SSE frame/sequence/resume semantics must remain unchanged when adding diagnostic overlays and new tail cursors. | LOG-COR-003 |

## Function and runtime diagnostics

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-FUN-001-1 | Function diagnostics must identify trusted action/revision, activation/job/attempt, runtime mode and source stream where available. | LOG-FUN-001 |
| FR-LOG-FUN-001-2 | WASM host/shim and OCI per-invocation logs must preserve their distinct identity boundaries and resource budgets. | LOG-FUN-001 |
| FR-LOG-FUN-002-1 | Runtime failure events must distinguish application errors, timeout/cancel, host termination and unavailable diagnostic evidence. | LOG-FUN-002 |
| FR-LOG-FUN-002-2 | Timing fields must distinguish scheduling/cold-start, execution, host-call and telemetry delay and mark unmeasured values unknown. | LOG-FUN-002 |
| FR-LOG-FUN-003-1 | Function investigations must link trusted caller lineage and immutable artifact/release identity without exposing unauthorized source or payloads. | LOG-FUN-003 |
| FR-LOG-FUN-003-2 | Log retrieval and export must honor effective activation/source retention and current permission rules across hot and archived data. | LOG-FUN-003 |

## Database query diagnostics

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-QRY-001-1 | Query diagnostics must capture verified logical datasource, execution ID, operation, safe error category and defined timing/row-count semantics. | LOG-QRY-001 |
| FR-LOG-QRY-001-2 | Instrumentation must preserve existing query authorization, RLS, error responses and execution behavior. | LOG-QRY-001 |
| FR-LOG-QRY-002-1 | Query normalization must use supported dialect parsers or known adapter plans and omit unsafe/unparseable text instead of retaining raw statements. | LOG-QRY-002 |
| FR-LOG-QRY-002-2 | Query summaries must provide scoped latency/error statistics with coverage, sampling and denominator quality explicitly reported. | LOG-QRY-002 |
| FR-LOG-QRY-003-1 | Query error views must link safe classification, sanitized shape and originating run/activation under datasource-aware authorization. | LOG-QRY-003 |
| FR-LOG-QRY-003-2 | Query plans must be optional authorized artifacts; the logs service must not automatically execute user SQL or EXPLAIN ANALYZE. | LOG-QRY-003 |

## Error grouping and issue lifecycle

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-ERR-001-1 | Grouping must use versioned deterministic normalized fingerprints inside trusted tenant/workspace/project scope. | LOG-ERR-001 |
| FR-LOG-ERR-001-2 | Transport duplicate occurrences must not increase issue counts, while distinct failed execution attempts must remain separate occurrences. | LOG-ERR-001 |
| FR-LOG-ERR-002-1 | Issues must support unresolved, acknowledged, resolved and snoozed states, authorized assignment, priority/tags and transition history. | LOG-ERR-002 |
| FR-LOG-ERR-002-2 | Issue mutations must use revision checks/idempotency and remain independent from workflow incidents or runtime control actions. | LOG-ERR-002 |
| FR-LOG-ERR-003-1 | Merge/split and grouping changes must preserve immutable occurrence identity, prior mapping provenance and auditable transitions. | LOG-ERR-003 |
| FR-LOG-ERR-003-2 | Regrouping/reprocessing must be bounded, resumable and notification-safe without duplicating occurrence counts. | LOG-ERR-003 |

## Releases and source-level diagnosis

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-REL-001-1 | Release records must bind trusted project/environment to immutable function/flow/build identity and deployment provenance. | LOG-REL-001 |
| FR-LOG-REL-001-2 | Debug artifacts must be uploaded through scoped CI credentials with digests, ownership and explicit retention/access policies. | LOG-REL-001 |
| FR-LOG-REL-002-1 | Symbolication must use verified matching artifacts and supported language/debug profiles with bounded isolated parsing. | LOG-REL-002 |
| FR-LOG-REL-002-2 | Original sanitized frames and enriched projections must remain versioned, scoped and subject to source-access/redaction rules. | LOG-REL-002 |
| FR-LOG-REL-003-1 | Regression detection must evaluate validated release/deployment lineage and explicit resolution boundaries rather than lexical version ordering. | LOG-REL-003 |
| FR-LOG-REL-003-2 | Unknown or late old-release events must be distinguished from qualified new regressions and must not spuriously reopen resolved issues. | LOG-REL-003 |

## Search, live tail and exports

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-SEA-001-1 | The query API must compile an allowlisted AST with mandatory scope/time bounds, pagination and bounded aggregation/full-text capabilities. | LOG-SEA-001 |
| FR-LOG-SEA-001-2 | Search responses must expose projection freshness, coverage, sampling, truncation and partial/timeout status. | LOG-SEA-001 |
| FR-LOG-SEA-002-1 | Live tail must use a typed scoped cursor, bounded subscriber buffers, permission rechecks and an explicit resume horizon. | LOG-SEA-002 |
| FR-LOG-SEA-002-2 | Tail gaps, overflow, retention expiry and disconnects must be visible rather than silently dropping records. | LOG-SEA-002 |
| FR-LOG-SEA-003-1 | Exports and archive queries must reauthorize scope and apply current masking, retention and resource budgets before producing results. | LOG-SEA-003 |
| FR-LOG-SEA-003-2 | Large exports/rehydration must be asynchronous jobs with progress, expiry, checksums and auditable download access. | LOG-SEA-003 |

## Storage, idempotency and retention

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-STO-001-1 | PostgreSQL must own scoped product/issue state and deduplicated error transitions while the approved analytical backend owns query projections. | LOG-STO-001 |
| FR-LOG-STO-001-2 | Projection writes and queries must handle transport/batch retries without relying on eventual background merges for immediate exact counts. | LOG-STO-001 |
| FR-LOG-STO-002-1 | Archive batches must use versioned sanitized schemas, scope/time metadata and checksummed manifests published only after verified object completion. | LOG-STO-002 |
| FR-LOG-STO-002-2 | Archive/debug/export storage must work through qualified falcone-s3 native or external bindings with appropriate retention and credentials. | LOG-STO-002 |
| FR-LOG-STO-003-1 | Effective retention must honor source/activation restrictions and scoped privacy policy across hot data, archives, artifacts, caches and exports. | LOG-STO-003 |
| FR-LOG-STO-003-2 | Deletion must create authoritative query-enforced tombstones and track asynchronous physical cleanup including replay/restore handling. | LOG-STO-003 |

## Alerts and controlled integrations

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-ALT-001-1 | Alert rules must define scoped conditions, windows, lateness/watermarks, thresholds, cooldown/hysteresis and no-data behavior. | LOG-ALT-001 |
| FR-LOG-ALT-001-2 | Alert evaluation must distinguish deduplicated exact counts from sampled or incomplete rates and commit each transition once. | LOG-ALT-001 |
| FR-LOG-ALT-002-1 | Notification delivery must use approved destinations, redacted payloads, secrets references, retry budgets, deduplication identity and DLQ state. | LOG-ALT-002 |
| FR-LOG-ALT-002-2 | Users must be able to inspect/test authorized delivery status and retry safe failures without claiming exactly-once external effects. | LOG-ALT-002 |
| FR-LOG-ALT-003-1 | External ticket creation or workflow response must require explicit configured authority and permitted scoped diagnostic content. | LOG-ALT-003 |
| FR-LOG-ALT-003-2 | Integration actions must be auditable, idempotent where supported and loop-safe, with dry-run/preview behavior. | LOG-ALT-003 |

## Falcone console and developer API

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-UI-001-1 | The console must provide scoped Logs, Errors and Trace/Execution views with entry points from flows, activations and datasources. | LOG-UI-001 |
| FR-LOG-UI-001-2 | Every view must show permissions, freshness, missing evidence and sampling states with safe accessible rendering. | LOG-UI-001 |
| FR-LOG-UI-002-1 | Saved filters/dashboards must preserve query version, scope, time semantics and permissions without storing credentials or hidden raw payloads. | LOG-UI-002 |
| FR-LOG-UI-002-2 | Shared views must authorize the current viewer and display explicit coverage/freshness for all widgets. | LOG-UI-002 |
| FR-LOG-UI-003-1 | The service must publish versioned ingestion/query/issue/release/alert schemas and scoped SDK/CLI examples. | LOG-UI-003 |
| FR-LOG-UI-003-2 | Examples must distinguish new proposed routes, existing Falcone contracts, protocol compatibility and quality/error states. | LOG-UI-003 |

## Quotas, sampling and resource governance

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-GOV-001-1 | Ingest bytes/events, retention, scan budget, tail connections, exports and notification limits must come from Falcone entitlements/policy. | LOG-GOV-001 |
| FR-LOG-GOV-001-2 | The service must enforce bounded per-tenant/source fairness and physical safety limits with explicit policy-unavailable behavior. | LOG-GOV-001 |
| FR-LOG-GOV-002-1 | Sampling and filtering decisions must expose policy/version, known probability and accepted/rejected/dropped coverage metadata. | LOG-GOV-002 |
| FR-LOG-GOV-002-2 | Usage facts must distinguish transport retries, accepted logical events, stored bytes and scan/transfer resources under Falcone accounting rules. | LOG-GOV-002 |
| FR-LOG-GOV-003-1 | Replay/reprocessing must use scoped jobs, checkpoints, versioned schemas and a documented dedupe horizon covering supported retry/replay windows. | LOG-GOV-003 |
| FR-LOG-GOV-003-2 | Historical reimports must honor deletion/source-retention rules and suppress new notifications unless explicitly authorized. | LOG-GOV-003 |

## Restricted deployment and reliability

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-OPS-001-1 | Baseline workloads must run non-root/arbitrary UID with namespace-scoped RBAC and no privileged DaemonSet, hostPath, new operator, CRD or eBPF prerequisite. | LOG-OPS-001 |
| FR-LOG-OPS-001-2 | Backend endpoints, storage budgets and operator ownership must be explicit prerequisites with qualified version/profile evidence. | LOG-OPS-001 |
| FR-LOG-OPS-002-1 | Operational telemetry must expose acceptance/loss, backlog, projection freshness, query cost, deletion lag and delivery health without sensitive high-cardinality labels. | LOG-OPS-002 |
| FR-LOG-OPS-002-2 | The release must publish benchmarked objectives, dependency-failure behavior and named on-call/patch responsibilities. | LOG-OPS-002 |
| FR-LOG-OPS-003-1 | Backups must include issue/alert/dedupe state, policy/deletion records and required archive/debug manifests and key dependencies. | LOG-OPS-003 |
| FR-LOG-OPS-003-2 | Restore/rebuild must preserve authorization and deletion before serving reads and report recoverable coverage and measured RPO/RTO. | LOG-OPS-003 |

## Implementation quality and controlled rollout

| ID | Requirement | Story |
|---|---|---|
| FR-LOG-DEV-001-1 | Builds must pin dependencies/images, publish SBOM/provenance and verify selected component/transitive licenses. | LOG-DEV-001 |
| FR-LOG-DEV-001-2 | The project must define vulnerability response, supported SDK/backend versions and compatible schema upgrade/rollback gates. | LOG-DEV-001 |
| FR-LOG-DEV-002-1 | Production candidates must pass cross-tenant, synthetic-secret, protocol, grouping/dedupe, retention and outage tests for every enabled profile. | LOG-DEV-002 |
| FR-LOG-DEV-002-2 | Independent review must cover privacy-before-persistence, source/artifact access, analytical query isolation and recovery/notification semantics. | LOG-DEV-002 |
| FR-LOG-DEV-003-1 | Rollout must progress from synthetic fixtures through shadow ingestion and scoped canaries with measurable privacy/performance/integration gates. | LOG-DEV-003 |
| FR-LOG-DEV-003-2 | Rollback must preserve admitted issue/audit/deletion state and prevent notification replay while disabling new producers/routes safely. | LOG-DEV-003 |

