# Operations, performance and ownership

## Deployment profiles

Use non-root arbitrary-UID Deployments, bounded worker resources, approved writable volumes and namespace-scoped RBAC. Application SDKs and trusted runtime shims export to a namespaced gateway. Do not require a cluster-wide log DaemonSet, operator, CRD, host filesystem, custom SCC or eBPF capability. Sidecars/shared application files are optional where approved; node/container logs can be consumed from an existing operator-managed facility with verified scope.

Native serverless ADR 0008 does not approve installing a new backend. The proposed ClickHouse instance must be provided/approved by platform operators or replaced through an explicit alternative-backend decision. Existing Kafka/PostgreSQL/S3 are dependencies with their own budgets. Deploy ingestion, query and heavy symbolication/archive workers independently. Keep small-development and production profiles visibly distinct.

Qualify the latest two Kubernetes releases at each service release and the actual corporate OpenShift build requested for the Kubernetes 1.33.12 baseline. Record exact cluster/runtime/library/image versions and capabilities; no build mapping or availability is inferred from a patch number alone. Support air-gapped dependency/artifact packaging where needed, without runtime source-map Internet fetch by default.

## Capacity model

Measure logs/errors/spans per second, average/p95 event size, burst factor, attribute cardinality, source count, search concurrency/time ranges, retention, debug artifacts, exports and tail subscribers. The historical 100k WebSocket/event messages per second is not a telemetry rate.

Uncompressed daily volume is `events_per_second × mean_bytes × 86,400`. For example, 10,000 records/second at 1 KiB is approximately 885 GB/day decimal (824 GiB/day) before compression, replicas, indexes, queue retention and archives. This is arithmetic, not a target or compression forecast. Benchmark storage, query scanning, dedupe and retention independently; critical error traffic can have a different budget from verbose debug logs.

Use fair per-tenant/source queues, batch sizes, byte limits, query deadlines, scanned-byte caps and export concurrency. Avoid one table/topic/partition per function or run. Query planning includes a mandatory time range and scope; large archive searches become bounded jobs. S3 egress/request and key-provider costs remain profile-dependent inputs to Falcone policy.

## Initial objectives, subject to qualification

| Measure | Proposed objective | Qualification conditions |
|---|---|---|
| Ingest/query availability | 99.9% monthly each initially | Separate indicators; report dependency failures and rejected overload explicitly |
| Ingest acceptance latency | p95 ≤200 ms for ≤256 KiB batches | Approved broker durability and representative local network/load; not search visibility |
| Hot search freshness | p95 ≤5 seconds from acceptance | Healthy pipeline; backlog age visible during recovery |
| Error issue freshness | p95 ≤10 seconds from acceptance | Includes scoped dedupe/grouping; symbolication can enrich later |
| Interactive hot search | p95 ≤2 seconds for bounded 24-hour queries | Qualification dataset, concurrency, selected fields and scan caps published |
| Live-tail visibility | p95 ≤3 seconds after admission | Bounded subscribers; explicit gaps/resume horizon; not workflow SSE cursor replacement |
| Alert transition/delivery enqueue | p95 ≤60 seconds after a satisfied evaluated condition | Defined windows/watermarks; external destination delivery measured separately |
| Producer overhead | Initial ≤5% CPU/latency budget on representative workloads | Benchmark instrumentation, batching and error storms; arbitrary workloads cannot inherit this guarantee |
| Permission freshness | Proposed ≤30 seconds for new queries/stream rechecks | Stream/token expiry and IAM outage behavior qualified; direct download URLs have separate limits |
| Metadata recovery | Backup RPO ≤5 minutes; service RTO ≤60 minutes initially | Independent secrets/bootstrap and restore drills; analytics rebuild duration is dataset-dependent |

No numerical guarantee of zero diagnostic loss: producers can crash before export and bounded queues can overflow. Measure loss and prioritize critical records within caps. After broker-acknowledged admission, verify recoverability under the selected replication/min-in-sync/leader-election/retention configuration; end-to-end archives are not implied by Kafka acknowledgement. Publish the actual tolerated failure domain.

## Alerts and incident operation

Support new/regressed-error rules, sustained threshold/rate rules, slow-query conditions and telemetry no-data/lag. Define evaluation windows, event-time lateness, watermarks, hysteresis, cooldown, mute schedules/timezone and recovery transitions. Invalid or incomplete denominators yield unknown/insufficient-data rather than a misleading 0% error rate. Use exact deduped error occurrence counts where promised.

Alert state and notification intent commit in PostgreSQL with a durable outbox. Delivery retries have bounded backoff, stable identity, rate limits and DLQ. External providers may deliver duplicates after a lost acknowledgement; expose that limit instead of claiming exactly-once email/webhooks. Core alerting remains independent of the workflow/serverless health it observes. Optional downstream workflow automation must not cause a notification loop or become a core availability dependency.

Monitor acceptance/rejection/drop counts, queue lag, processing/index watermarks, duplicate/conflict rates, redaction failures, cardinality/scan costs, query cancellations, tail overflow, symbolication failure, archive verification, deletion backlog, credential expiry and notification delivery. Minimal independent metrics/health and bounded local safe logs prevent the service from hiding its own outage.

## Responsibilities

Product owners define triage behavior, entitlements and retention. Logs maintainers own schemas, grouping, protocol/SDK compatibility and dependency patches. Falcone integration owners implement producer/console/shared-contract handoffs. SRE/platform teams own backend placement, capacity, on-call, backups and recovery. Security/privacy engineers review scope, redaction, exports, debug artifacts and retention; IAM and secrets owners supply their own trust/custody contracts. Assign actual people/rotations during readiness; this plan does not invent operational coverage.
