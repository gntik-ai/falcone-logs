# Reference products and feature selection

Checked 2026-11-02 using [primary sources](sources.md). This survey distinguishes error-tracking products from log/trace infrastructure. Features and licenses belong to specific editions/components; this plan copies no upstream implementation.

## Comparison

| Project | Functional features | Scaling/extensibility | Fit for Falcone | Limitations and license boundary |
|---|---|---|---|---|
| **Sentry** | Exception events grouped into issues, stacks/breadcrumbs/tags, release attribution, source maps, regressions, tracing, logs, alerts; broader profiles/replay/feedback products | SDK/envelope ingestion, processing workers and analytical services; integrations and release artifacts | Reference for developer-focused issue triage and linking an error to its execution/release | Full self-hosting has substantial dependencies; self-hosted/SaaS feature parity is not universal. Current server FSL is source-available, not OSI open source; evaluate exact version/component terms before reuse |
| **GlitchTip** | Error tracking, performance, uptime and current log search/correlation; release/debug artifacts | Sentry SDK compatibility; PostgreSQL-based hot data with documented cold archive options | Useful reference for a smaller error-tracking product and focused developer UX | Its current logs documentation uses Sentry envelopes and explicitly does not offer a direct raw OTLP HTTP receiver. Backend MIT; pin components rather than assuming all Sentry features |
| **SigNoz** | OpenTelemetry logs, traces, metrics, exception grouping, dashboards and alerts | Collector ingestion and ClickHouse analytics; SDK/OTel ecosystem | Strong reference for unified log/trace navigation and database-span analysis | Operational analytics backend remains necessary; root license distinguishes MIT core from enterprise directories/features |
| **OpenObserve** | Log search, traces/metrics, dashboards, processing pipelines and alerts | Rust implementation, object-oriented storage architecture and multiple ingestion interfaces | Reference for retention/storage economics and unified search | AGPL-3.0 core; enterprise additions such as advanced IAM/redaction must not be treated as freely reusable core. Falcone implements its own IAM/privacy policies |
| **Uptrace** | OTel traces/logs/metrics, query builder, dashboards, service graph and alerting | Go service, ClickHouse telemetry and PostgreSQL metadata | Useful component split and trace-centered navigation reference | Current repository license is AGPL-3.0; do not rely on older permissive-license summaries or advertised throughput as Falcone evidence |
| **Grafana Loki** | Log ingestion, LogQL search, live exploration, rule/alert integration | Label-indexed streams, scalable components and object storage | Good option when operator-managed Loki already exists; low-cardinality label discipline | Not a Sentry-style issue/release lifecycle by itself. Tenant header is not authentication; trusted gateway required. AGPL-3.0 |
| **OpenSearch Observability** | Indexed log search, trace analytics/correlation, dashboards and alerting | Distributed indexes, Data Prepper/OTel ingestion and plugins | Strong full-text/search alternative for an existing approved OpenSearch deployment | More index/shard operations; still needs Falcone error grouping/triage and scope enforcement. Apache-2.0 project; qualify selected plugins |

OpenTelemetry is the interoperability foundation, not a replacement investigation product. Prometheus/Grafana remain Falcone metrics references. Neither OTel instrumentation nor a log search backend supplies application authorization, durable workflow state or a billing ledger.

## Features to take into the custom service

| Feature | Falcone-specific behavior | Priority |
|---|---|---|
| Structured logs and live tail | Scope by tenant/workspace, flow run, function activation and query execution; show gaps and collection lag | P1/P2 |
| Error grouping | Versioned deterministic grouping inside a Falcone project; distinguish attempts from duplicate transport | P1 |
| Developer issue lifecycle | Assign, acknowledge, resolve, snooze, merge/split with history; source execution state unchanged | P1/P2 |
| Stacks and breadcrumbs | Sanitized, bounded and source-policy-dependent; never restore data deliberately omitted by Falcone's request logger | P1/P2 |
| Distributed correlation | W3C trace context plus trusted Falcone run/node/attempt identities and explicit async links | P1/P2 |
| Query insights | SQL/MongoDB operation shapes, latency/error rates and candidate repeated-call patterns; no default values/results | P1/P2 |
| Releases and regressions | Immutable function revision/flow-definition/build identity, debug artifact provenance and ordered deployment evidence | P2 |
| Source maps/symbols | Uploaded, scoped, hash-verified artifacts; language/profile-specific support | P2; broad native symbolication later |
| Alerts | New/regressed error, sustained error/latency rate, missing telemetry; evidence links and deduplicated notifications | P2 |
| Search, views and exports | Field/text/time filters, scoped facets, safe share links, quotas and export redaction | P1/P2 |
| Profiles/session replay | Separate privacy/cost/runtime capability, not a baseline dependency | Optional later |
| AI investigation | Optional Falcone-model-gateway assistance on approved sanitized evidence; hypotheses with references, no automatic remediation | Optional later |

## Product and licensing implications

Sentry's server license identifies competing-use restrictions and a later change license. Its JavaScript repository has MIT code but explicitly identifies separately licensed transitive CLI tooling. Therefore protocol compatibility and feature inspiration do not authorize copying the server or assuming every SDK dependency is MIT. SigNoz and OpenObserve also separate community and enterprise code. Review concrete dependency versions and notices before reuse; no legal or certification conclusion about a future distribution is implied here.

## Recommended path and alternatives

Build Falcone-owned ingestion policy, error grouping, investigation APIs and console views using maintained protocol/storage libraries. Reuse existing platform services. ClickHouse is the proposed hot analytical store because this workload combines field filtering, aggregates and traces, but it must be approved and benchmarked. Existing Loki/OpenSearch can be evaluated as alternative search backends with explicit capability differences, not as a promise of automatic query-language parity.

A GlitchTip/Sentry façade can validate user workflows quickly but retains a separate product, authorization model and lifecycle. Forking a full observability product adds merge/patch and licensing obligations. A PostgreSQL-only development profile reduces setup but must not be advertised at the same scale as a qualified analytical backend. Custom distributed storage/search is outside this effort.
