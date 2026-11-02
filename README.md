# falcone-logs

**Falcone's custom log analysis, error tracking and execution investigation service.** It connects flow runs, function activations and database operations in one tenant-scoped investigation experience inside Falcone.

Status: **proposed architecture and delivery backlog; no runtime implementation or deployment in this bootstrap.** Research date: 2026-11-02. Falcone baseline: [`4b6ef97`](https://github.com/gntik-ai/falcone/tree/4b6ef9736cb78deec346537b1c0b8eea8b79c34c).

## What the service will provide

- Structured log search, live tail, saved views and safe exports.
- Grouped exceptions, stack traces where permitted, breadcrumbs, ownership, triage and regression detection.
- Correlation across flow runs/node occurrences, function revisions/attempts, database calls and distributed traces.
- Slow-query and failure analysis using sanitized query shapes, with no collection of parameter values or result rows by default.
- Release/source-map support, scoped alerts and controlled integrations.
- Falcone IAM, secrets, S3, workflow, serverless, quota and console integration.

The service owns the investigation product and error lifecycle. Existing Prometheus/Grafana metrics, governed audit records, workflow histories and billing ledgers retain their own authority. Telemetry is not a substitute for execution history or evidence that a query/function completed.

## Documentation

| Document | Contents |
|---|---|
| [Reference survey](docs/reference-survey.md) | Sentry, GlitchTip, SigNoz, OpenObserve, Uptrace, Loki and OpenSearch |
| [Scope and current contracts](docs/scope-and-baseline.md) | Inspected Falcone behavior, ownership and integration boundaries |
| [Architecture](docs/architecture.md) | Components, stack, diagrams, ingestion and investigation flows |
| [Telemetry contract](docs/telemetry-contract.md) | Identity, correlation, trust, delivery and sampling semantics |
| [Flows, functions and queries](docs/domain-analysis.md) | Domain-specific investigation and compatibility |
| [Errors and releases](docs/errors-and-releases.md) | Grouping, triage, source maps and regressions |
| [Storage and lifecycle](docs/storage-and-lifecycle.md) | PostgreSQL, ClickHouse, S3, deduplication, retention and recovery |
| [Security and privacy](docs/security-and-privacy.md) | Tenant isolation, redaction, data minimization and safe integrations |
| [Integration matrix](docs/integration-matrix.md) | Repository ownership and cross-service handoffs |
| [Operations](docs/operations.md) | Restricted OpenShift, capacity, SLOs and on-call |
| [Rollout](docs/rollout.md) | Incremental instrumentation, shadow comparison and release gates |
| [Requirements](docs/requirements.md) | 96 testable requirements |
| [Epics and stories](docs/backlog.md) | 16 epics and 48 user stories with criteria, dependencies and effort |
| [Decision and alternatives](docs/decisions/0001-falcone-investigation-service.md) | Recommended architecture and trade-offs |
| [Open questions](docs/open-questions.md) | Defaults and evidence required before implementation/release |
| [Sources](docs/sources.md) | Primary references and pinned Falcone evidence |

## Delivery path

1. **P0:** freeze contracts, privacy rules, trusted identity and backend/capacity decisions.
2. **P1:** authenticated ingestion, redaction, storage/search, core grouping and domain instrumentation.
3. **P2:** integrated console/timelines, releases, alerts, archive/retention and operational qualification.
4. **P3:** cross-service canaries, failure/security evidence and controlled production rollout.

Recommended implementation: TypeScript product API/workers, OpenTelemetry-compatible collection with a qualified Go gateway where needed, existing Kafka, PostgreSQL for control/error state, approved ClickHouse for hot analytics and `falcone-s3` for scoped archives/debug artifacts. Backend placement is a qualification decision; no new cluster-wide operator is assumed.

## Backlog maintenance

[GitHub issues](https://github.com/gntik-ai/falcone-logs/issues) are linked through stable LOG IDs, epic task lists and parent/dependency references. [CSV](docs/backlog.csv), [JSON](docs/backlog.json), [issue payloads](docs/issue-payloads.json) and [issue mapping](docs/github-issues.json) are included. No GitHub Project board or native sub-issue relationship is implied; CSV is portable planning data, not a universal GitHub importer.

Edit `tools/build_docs.py` and run `python3 tools/build_docs.py` to regenerate requirements/backlog. It validates identifiers, references and dependency cycles; it does not publish automatically. Maintain architectural documents directly.

Reference projects supply feature ideas, not copied implementations. Current Sentry server code is source-available under FSL, not OSI open source; SDKs and transitive tooling have separate licenses. Select the Falcone logs repository license explicitly before distributing implementation code.
