# ADR 0001 — Custom Falcone log and error investigation

Date: 2026-11-02. Status: **proposed detailed design**. The owner requested the product and this architecture/backlog publication. Existing sibling decisions keep their original status.

## Decision

Build Falcone-owned ingestion policy, log/error correlation, deterministic issue grouping, triage, release analysis, search/alert APIs and integrated console views. Use OTel conventions and explicit trusted Falcone execution context. Reuse existing Kafka, PostgreSQL, IAM, secrets and S3 contracts; propose approved ClickHouse for high-volume analytical projections. Source redaction precedes persistence. Keep governed audit, billing and execution-state authority separate.

TypeScript is recommended for APIs/domain workers, with maintained OTel/Go collection components where necessary. No custom search database, crypto protocol, workflow scheduler or cluster-wide collection operator is required. Errors, spans and logs can be incomplete; freshness and loss are product data.

## Alternatives and trade-offs

| Option | Developer/scale benefit | Operational cost | Falcone compatibility and choice |
|---|---|---|---|
| Custom Falcone product over standard storage/OTel | Native run/activation/query context and one permission model; independent scaling of ingest/search | Own grouping, projection, privacy and recovery correctness | Recommended target |
| Sentry or GlitchTip behind a façade | Fast existing issue UX and SDK support | Separate auth/product lifecycle and upstream patch/license surface | Optional prototype or migration adapter, not the requested final custom product |
| Approved ClickHouse hot store | Efficient typed/time aggregates, traces and logs | Backend provisioning, replicated operations and explicit duplicate/deletion semantics | Proposed baseline; capacity/operator qualification first |
| Existing Loki/OpenSearch backend | Reuse installed infrastructure and established search tooling | Different query/index/retention behavior and adapter testing | Viable alternative; issue state remains Falcone-owned; no automatic full feature parity |
| PostgreSQL-only small profile | Lower development deployment burden | Limited analytical scale and contention with exact issue state | Development or explicitly bounded small deployments only |
| S3 archives and asynchronous rehydration | Lower hot retention footprint; native/external storage choice | Manifest/replay/deletion complexity and slower investigation | Recommended after hot path; disclose cold-query coverage and cost |
| Full Sentry SDK compatibility | Familiar instrumentation for external apps | Envelope/item/SDK drift and mixed transitive licenses | Optional tested subset; OTel plus Falcone producer contracts are primary |
| Node/eBPF collection | Broad low-touch infrastructure visibility | Elevated permissions and weaker tenant attribution | Not a baseline for restricted OpenShift; consume approved external collectors if available |
| Profiling/replay/AI diagnosis | Richer context and assisted investigation | Sensitive data, runtime overhead, model/privacy and storage costs | Optional later capabilities with explicit gates; no automatic remediation |

## Consequences

Falcone gains one investigation model across services, but storing telemetry does not prove complete causality, exactly-once delivery or zero source loss. The project must qualify privacy, scope, query cost, replay, lifecycle and operational budgets. Sentry FSL/enterprise source is not implicitly approved for copying. The repository license remains an explicit owner decision before implementation distribution.
