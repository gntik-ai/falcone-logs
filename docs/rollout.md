# Rollout and validation

1. **Freeze contracts and privacy:** inventory existing log sources, activation policies, flow SSE/audit behavior, query adapters and live collectors. Publish producer/permission schemas and fixtures pinned to the inspected Falcone revision. Measure real telemetry demand.
2. **Build a synthetic vertical slice:** two tenants; one flow invokes a function that performs a successful query and a controlled failing query. Show trusted lineage, a sanitized log, grouped error and scoped search. Use no production secrets or copied customer records.
3. **Shadow ingestion:** add bounded producer export alongside current views. Compare event identity, byte overhead, privacy, gaps and scope; keep execution outcomes and existing audit/metrics unchanged. Disable alert delivery during historical/shadow import.
4. **Canary investigation:** enable read-only console/search for selected workspaces. Preserve flow SSE sequence/resume and activation policies. Test missing data, late events, retries, runtime crashes and tenant-denial cases.
5. **Enable triage/releases and configured alerts:** qualify source-map artifacts, release/regression logic and notification destinations. Preview rules before enabling deliveries; retain safe rollback of UI/routing/configuration.
6. **Qualify retention/recovery:** rehearse pipeline/broker/index/key/IAM failures, purge plus replay, archive restoration, metadata restore and alert-state recovery. Independent security review gates production data ingestion/exports.
7. **Expand coverage:** roll out by source/workspace and publish supported SDK/runtime/backend versions. Retire duplicated diagnostic views only after parity and explicit product migration; audit/metering/workflow histories remain authoritative.

## Meaningful verification

| Risk | Required evidence |
|---|---|
| Scope forgery or leakage | Same IDs in two tenants; forged SDK fields; facets, joins, source maps, tails, saved links, exports and cache policy changes |
| Secret capture | Synthetic canaries in URL queries, messages/stacks/causes, SQL/Mongo values, nested logs and artifacts; verify every persistent sink and DLQ |
| Duplicate/regression errors | Producer retries, changed batches, Kafka replay, late old-release events and concurrent issue mutation |
| Lost/partial data | Hard kill, exporter overflow, unavailable broker/index, missing spans and out-of-order workflow events with visible quality flags |
| Incorrect query analysis | SQL dialect/parser failures, Mongo cursor timing, cancelled queries, no EXPLAIN execution, unbiased/qualified rate denominators |
| Retention bypass | Source activation expiry, archive rehydrate, caches, tombstones, restore and delayed replay; logical versus physical completion |
| Operational blast radius | Error/log storms, noisy tenant, bounded queries/tails, self-monitoring loop and independent alert evaluation |

No full Sentry database migration is assumed. If an existing deployment is later discovered, add an explicit importer for supported sanitized events, issue history and release mapping with source identity, permissions, retention and notification-suppression rules. Do not copy unsupported attachments or assume Sentry issue IDs have Falcone meaning.

Rollback can disable new exporters, routes or alert delivery while preserving admitted data and triage/audit state. It must not restore deleted data, lose retention tombstones or replay old notifications as new. Schema changes use compatible versioning and tested rollback windows. This bootstrap publishes design/issues only; deployment and production cutover are subsequent work.
