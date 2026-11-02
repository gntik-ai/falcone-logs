# Telemetry identity, delivery and correlation

## Versioned event envelope

The following is a proposed internal contract, not a claim that these fields already exist in every producer. Preserve published Falcone camelCase/SSE fields through adapters; normalize internally without silently renaming public schemas.

| Field group | Fields and meaning |
|---|---|
| Identity | `schema_version`, `event_id`, `producer_id`, producer epoch/sequence when available; gateway receipt/batch identity is separate |
| Trust and scope | Verified tenant/workspace, application/project, environment, authenticated producer class and source ownership; platform events have explicit platform scope |
| Time | Source event time, observation/ingestion time, monotonic duration if available and clock-quality flags |
| Signal | Log, error occurrence, span or diagnostic control event; normalized severity and bounded event category |
| Correlation | Existing Falcone correlation ID, W3C trace/span IDs, parent/span links and trusted causation references |
| Flow | Definition ID/version, execution/run ID, node occurrence ID, loop/map iteration, attempt, parent/child run link and engine |
| Function | Action/resource ID, immutable revision, activation/job/attempt ID, `runtime_mode` (`wasm`/`oci` when supplied), source kind and stream sequence |
| Query | Logical datasource ID, operation, query execution ID, sanitized shape/fingerprint version, duration, row-count semantics, safe error class |
| Release | Build/debug ID, artifact digest, release ID, deployment ID/environment; all scoped and provenance-qualified |
| Content | Sanitized message template/body, approved attributes, exception chain/frames and bounded breadcrumbs where source policy permits |
| Quality | Redaction policy/version, truncated/missing fields, sampling policy/rate, loss/gap markers, duplicate status, enrichment provenance and completeness |

Do not promote a guest-supplied `tenant_id`, arbitrary `trace_id`, browser user ID or datasource name into trusted ownership. Keep reported attributes separate from verified context; reject conflicting reserved fields. Scope an event ID by tenant/workspace and authenticated producer identity. IDs must remain stable across transport retry; genuine retry attempts are new occurrences, not transport duplicates.

## Correlation rules

Use W3C Trace Context for request spans and explicit links for asynchronous boundaries. A correlation ID may join several traces; a trace can be sampled or partially observed. Store both rather than coercing Falcone IDs into trace IDs. Repeated node names, concurrent loop iterations, retries and workflow child runs need occurrence/attempt identities.

Long-running flows use bounded trace segments linked by durable execution lineage. Do not hold one in-memory span/tail-sampling decision open for days. The workflow run timeline comes from its authoritative event history, with diagnostic overlays retrieved separately. Late spans may enrich an investigation; they cannot rewrite the run's outcome.

Use a source's monotonic sequence where its contract provides one. Wall-clock order across hosts is not causality. Preserve source/observed timestamps and clock-skew flags; do not infer that the earliest received log is the root cause. User-visible links explain whether they derive from a trusted causal edge, matching trace context or heuristic similarity.

## Ingestion interfaces

| Interface | Baseline contract |
|---|---|
| OTLP logs/traces | Authenticated HTTP/protobuf first; optional gRPC after tests. Respect OTLP success, partial-success and retry semantics |
| Falcone internal batch | Explicit schema and producer ownership, per-item accepted/rejected outcome and retry guidance; identifiers survive retries |
| Existing flow/activation adapters | Read approved histories/log responses and map identities; do not mutate original execution records |
| Optional Sentry envelope adapter | Advertise only tested SDK versions and item types; separate error/log/span/artifact capabilities; no full Sentry API promise |
| Browser/public ingestion, if enabled | Project-scoped write-only key is public/untrusted, abuse-limited and never grants read or authenticates a runtime/user claim |

HTTP status `202` may be appropriate for the custom batch API, but must not replace the required OTLP or Sentry-adapter status/response format. OTLP partial success is not permission for clients to retry already accepted records indiscriminately. Publish endpoint-level behavior and limits for bytes, decompression, attributes, stack depth, breadcrumbs and event age.

Authentication and mandatory redaction precede durable queues. The accepted internal envelope is immutable and has a scoped integrity digest. Conflicting reuse of an event ID is reported without logging the raw conflicting body. Deduplication retention must cover producer retry, Kafka replay, DLQ and supported archive replay windows; older explicit reimports get a controlled import namespace and no automatic alerting.

## Delivery, sampling and accounting

Delivery is at least once after acknowledged admission under the configured broker durability profile. Sources may lose diagnostics before admission, especially on hard kill or exhausted buffers. Report produced, attempted, accepted, rejected, sampled, dropped, retried and indexed signals separately. Replays do not become new billable ingestion just because the transport repeats them; Falcone defines actual metering policy.

Prefer keeping errors and terminal-failure summaries, but maintain hard resource caps and expose any losses. Head sampling cannot recover spans it never captured. Tail sampling needs bounded trace-affine routing and cannot wait indefinitely for a long workflow. Store effective sampling policy/known probability; never present sampled counts or incomplete denominators as exact failure rates or unique-user counts.

Logs can exist without traces, traces without logs and errors without symbolication. Search and alert APIs must return coverage/freshness metadata. No data is `unknown` or `no_data` when collection is unavailable; it is not evidence of zero errors.
