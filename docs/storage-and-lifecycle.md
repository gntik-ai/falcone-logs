# Storage, projections and lifecycle

## Data authority

| Store | Contents | Authority and recovery |
|---|---|---|
| Kafka diagnostic topics | Sanitized admitted envelopes, partitions and retention | Replay source for the declared window; broker receipt is not permanent archive |
| PostgreSQL | Projects/sources, policy revisions, bounded error-occurrence dedupe, issues/transitions, releases/artifact manifests, views, alert state/outbox, deletion tombstones | Transactional product authority with scoped roles/RLS; no object payload blobs |
| ClickHouse | Logs, spans, sanitized query summaries and versioned error/search projections | Analytical projection; exposes freshness and deduplicated query semantics; not workflow/audit/billing authority |
| falcone-s3 | Scoped immutable archive batches, debug artifacts, export jobs and backup manifests | Native or external provider through bindings; manifests verify completeness/checksums and lifecycle |
| Existing audit/metering stores | Governed actions and usage facts | Retained separately under their current contracts; diagnostic search is an authorized correlated view |

Use bounded time partitions and scope-leading sort keys appropriate to measured query patterns. Do not create a Kafka topic, ClickHouse table or label series for every function, run, query ID or raw attribute. A trusted router assigns scope, fair queues and partitions; tenants cannot choose backend namespace headers. Define maximum attribute count/value length and promote only approved fields into indexes.

## Idempotency and projection lag

Kafka delivery is at least once. Each record has a stable scoped source identity and canonical accepted content. Consumers write an idempotent PostgreSQL inbox/error transition where exact issue/alert state is needed; they commit offsets only after their own required write succeeds. There is no atomic transaction across Kafka, PostgreSQL, ClickHouse and S3.

ClickHouse batch retries can create duplicate physical rows. Use qualified insert/dedup tokens and a schema/query strategy that yields one logical event per scoped identity, including retries with changed batch boundaries and imports. `ReplacingMergeTree` background merging alone does not establish immediate deduplicated counts. Use a tested query-time latest-row/FINAL strategy where appropriate and account for its cost. Do not feed exact alert counts from a naive materialized sum of duplicate raw inserts. Separate exact error counts from approximate/high-volume aggregates, and label any approximation.

Track per-consumer partition watermarks and backlog age. An event can be accepted but not searchable or grouped yet. Issue events missing from the analytical store retain a visible indexing status and bounded recovery path. Archive writers upload/checksum data before atomically publishing a manifest; a failed manifest leaves an orphan eligible for delayed safe cleanup. Replays obey current deletion tombstones and cannot resurrect purged data.

## Hot and archive access

Proposed initial retention is 7 days hot for general logs/spans and up to 30 days total diagnostic retention, configurable by Falcone policy. Error/triage metadata may use a longer explicit policy, such as 90 days, but source log access restrictions still apply. Existing activation `retentionHours` can be shorter: effective access/retention must honor the strictest applicable source/privacy policy unless a separately authorized product contract changes it. Archive is not a way to bypass source retention.

Archive older sanitized batches to scoped Parquet objects with schema/version, time bounds, scope, event identity range, checksum and object version. Initially rehydrate approved ranges asynchronously through bounded jobs and temporary search tables with expiry; do not promise transparent arbitrary cold SQL at hot-query latency. Query results expose archive coverage, scan budgets and partial status. Duplicate hot/cold overlap uses event identity dedupe.

Debug artifacts and exports use separate bucket/prefix policy and lifetimes. Downloads go through authorized retrieval or an explicitly approved short-lived signed link; provider presigned links may outlive immediate Falcone policy revocation and must not be used where that is unacceptable. No sensitive data in exported filenames or object keys by default.

## Deletion, privacy and legal hold

Retention/purge creates an authoritative scoped tombstone immediately checked by every query, live tail, facet, cache, export and rehydration path. Background jobs remove relevant hot rows, archives, debug artifacts, derived projections and export objects under an auditable deletion plan. ClickHouse TTL/mutations and object deletion can be asynchronous; report logical inaccessibility separately from verified physical completion.

Kafka segments and immutable/shared archive files may contain mixed events. Use bounded retention, safe rewrite/compaction where required and a documented maximum purge deadline; do not promise selective immediate erasure from every copy. Backups have a separate expiry/hold policy; restore must reapply tombstones before serving reads. Derived fingerprints, comments and source snippets may also contain personal/sensitive data and need scope in the deletion inventory.

Legal hold is a restricted, audited policy with explicit conflict handling. It cannot silently widen viewer access or become an excuse to keep all telemetry indefinitely. Tenant deletion blocks new ingestion and delayed replay for the deleted identity; opaque IDs are not reused as new authorization identities.

## Recovery

Back up PostgreSQL control state, required key custody, archive/debug manifests and referenced objects. Choose whether hot ClickHouse data is restored from backups or rebuilt from Kafka/archive; publish the coverage window and unavailable gaps. A restore must preserve issue identity, dedupe/alert notification state, policy versions and deletion tombstones. Never resend every historical alert by resetting consumers without a replay mode. Native/external S3 availability and independent secrets bootstrap are prerequisites, not assumed properties of an S3-compatible endpoint.
