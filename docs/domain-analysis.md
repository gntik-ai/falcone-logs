# Investigation for flows, functions and queries

## Flows

From a flow execution page, show its authoritative graph/timeline with diagnostic overlays: node occurrence and attempt, retries/backoff, queued versus executing time, timeout/cancel status, child-run links, function calls and datasource calls. Users can move from a failed node to the related grouped error, surrounding logs and trace segment without widening scope.

Current Temporal-backed monitoring emits `node-status` and `log-line` SSE frames with stable source-derived sequence/resume behavior. Preserve that route and framing while adding a separate diagnostic overlay. Custom falcone-workflow owns durable run events and incidents; falcone-logs can link to them but cannot change `needs-attention`, resume, retry, cancel or compensate a run through issue triage. A retry that eventually succeeds still has diagnostic occurrences, while its final run outcome is successful.

Handle nested flows, maps/loops, retries, signals and long waits. A node ID alone cannot identify a particular execution. Use engine/run/node-occurrence/attempt lineage, deterministic producer identity and gap markers. Workflow replay/reconstruction must not re-emit old logs as new failures; transport replay deduplicates the same source events. A historical import has its own mode and notification suppression.

## Functions

Show activation status from the owning runtime, immutable revision, runtime mode, attempt, timing, error type and sanitized logs. Distinguish scheduling/cold-start time, execution time, host-call time and telemetry-delivery delay; absent timing is unknown, not zero. Keep log access, result access and source/debug-artifact access as separate permissions under the existing activation policy.

For WASM, collect allowed structured host/shim events and bounded guest output through the runtime's trusted identity boundary. For OCI, pod stdout/stderr is revision/pod-level unless the producer can prove invocation attribution; concurrent invocations must not inherit each other's logs. Per-invocation records use the shim capability API. Native crashes, OOM, forced termination and host failure may have no application stack; collect safe runtime termination evidence with provenance and an explicit collection gap.

Do not install tenant-selected collectors inside trusted control-plane processes or grant guest code platform ingestion/read credentials. Log emission gets a scoped channel and byte/event budget. Flush cooperatively within a deadline; hard-kill loss remains observable. Logs-service outages must not change a successful execution into a failure, except where a separately governed audit contract already requires blocking.

## Database queries

Initial coverage is trusted Falcone PostgreSQL and MongoDB adapters, including calls made by workflows/functions. Instrument the real execution seam after authorization. Capture logical datasource, operation, sanitized query shape/version, safe SQLSTATE/driver category, timing, cancellation/timeout and approved row-count fields. Separate connection-pool wait, client duration and server execution time; the latter is unknown unless actually measured. Mongo cursor consumption may outlive initial dispatch and needs defined end/duration semantics.

Never capture connection strings, credentials, bind values, returned rows, document bodies, embedding vectors or prompts by default. SQL and Mongo normalization must use dialect-aware parsing/known adapter plans, remove values/comments and bound identifier exposure. If a statement cannot be safely normalized, retain a coarse operation/error category and mark the shape unavailable. An unkeyed hash of raw sensitive text is not an adequate privacy boundary.

Group performance by tenant/workspace, datasource and sanitized query shape. Show observed count, latency percentiles, errors and sample/coverage context. Repeated-call/N+1, timeout and regression detectors produce evidence-backed candidates; they do not assert a definitive root cause from timing alone. Compare equivalent environment/deployment windows and valid denominators. Query text and table/collection names may themselves be sensitive and require access policy.

Explain plans are optional, explicitly authorized artifacts from an approved source. Do not automatically run user SQL, `EXPLAIN ANALYZE` or an equivalent operation that executes work. Even ordinary EXPLAIN requires datasource rights, timeout/overhead controls and plan redaction; baseline users can investigate timing/error shapes without granting the logs service database execution authority.

## Cross-domain example

A flow node invokes function revision A; attempt 1 calls a PostgreSQL adapter and times out, then attempt 2 succeeds. The investigation shows two distinct attempts and two query executions, connected by trusted lineage. The error issue counts one timeout occurrence, deduplicated if its transport retries. A trace missing because of sampling is shown as unavailable. Marking the error resolved does not rerun the function or alter the successful flow result. Deployment of revision B can be correlated with subsequent observations, but a delayed event from A must not automatically become a new B regression.
