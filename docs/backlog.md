# Epics and user stories

Generated with `python3 tools/build_docs.py`. S/M/L are relative small/medium/large complexity estimates, not dates. P0 = discovery/decisions; P1 = core; P2 = integrations/hardening; P3 = qualification/rollout. Phase is earliest start subject to dependencies.

The logs repository owns these product stories. Producer, console and shared-module changes must be decomposed into their owning repositories before implementation; see integration-matrix.md. Epic task lists and parent links express hierarchy; no GitHub Project board or native sub-issue relationships are implied.

- **[LOG-CON](https://github.com/gntik-ai/falcone-logs/issues/1): Falcone contracts and product boundaries** — Define a custom investigation service that preserves current Falcone behavior.

  - **[LOG-CON-001](https://github.com/gntik-ai/falcone-logs/issues/17): Freeze log, error and execution contract inventory** (P0, M)
    - As a Falcone maintainer, I want versioned fixtures for all diagnostic producers and consumers, so that new analysis preserves existing contracts.
    - Description: Versioned fixtures for all diagnostic producers and consumers.
    - Requirements: FR-LOG-CON-001-1, FR-LOG-CON-001-2
    - Dependencies: None
    - Acceptance: Include main Falcone, current Temporal/Knative paths and planned native sibling contracts without treating proposals as deployed functionality.
    - Acceptance: Preserve fix-1118 query-key logging restrictions, separate log/result permissions and governed audit failure semantics.
    - Acceptance: Identify actual collectors, versions, raw Sentry consumers if any, datasource coverage and current retention; record evidence gaps.

  - **[LOG-CON-002](https://github.com/gntik-ai/falcone-logs/issues/18): Define ownership, source enrollment and integration handoffs** (P0, M)
    - As a platform architect, I want clear authority for diagnostics and execution state, so that Falcone services do not compete to own policies or histories.
    - Description: Clear authority for diagnostics and execution state.
    - Requirements: FR-LOG-CON-002-1, FR-LOG-CON-002-2
    - Dependencies: [LOG-CON-001](https://github.com/gntik-ai/falcone-logs/issues/17)
    - Acceptance: Use shared Falcone outbox/inbox/fencing contracts; gaps become owning-repository handoffs, not duplicate implementations.
    - Acceptance: Respect serverless ADR 0008 status and OCI pod-versus-invocation attribution; use accepted secrets decisions.
    - Acceptance: Document diagnostics as additive projections: resolving an issue never changes run state, reruns code or executes a query.

  - **[LOG-CON-003](https://github.com/gntik-ai/falcone-logs/issues/19): Qualify reference licenses, components and telemetry capacity** (P0, L)
    - As a maintainer, I want reviewed technology and sizing decisions, so that the service can be operated and distributed responsibly.
    - Description: Reviewed technology and sizing decisions.
    - Requirements: FR-LOG-CON-003-1, FR-LOG-CON-003-2
    - Dependencies: [LOG-CON-001](https://github.com/gntik-ai/falcone-logs/issues/17)
    - Acceptance: Review Sentry FSL and SDK transitive tooling, MIT/community and enterprise boundaries, AGPL references and the repository-license decision.
    - Acceptance: Benchmark TypeScript processing and proposed Go/OTel ingestion; require approved ClickHouse or a tested alternative backend profile.
    - Acceptance: Record infrastructure and data-volume assumptions; no performance or compliance claim is inherited from a reference project.

- **[LOG-ING](https://github.com/gntik-ai/falcone-logs/issues/2): Ingestion and SDK compatibility** — Accept bounded, scoped diagnostics with honest acknowledgement and loss semantics.

  - **[LOG-ING-001](https://github.com/gntik-ai/falcone-logs/issues/20): Implement authenticated OTLP and Falcone batch ingestion** (P1, L)
    - As an application developer, I want standard log/trace ingestion plus Falcone adapters, so that diagnostics enter one supported service.
    - Description: Standard log/trace ingestion plus Falcone adapters.
    - Requirements: FR-LOG-ING-001-1, FR-LOG-ING-001-2
    - Dependencies: [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23), [LOG-PRV-001](https://github.com/gntik-ai/falcone-logs/issues/26), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29)
    - Acceptance: Implement qualified OTLP HTTP/protobuf and custom batch profiles; optional gRPC requires its own tests.
    - Acceptance: Test mixed valid/invalid batches, oversized attributes, wrong audience, broker failure and lost acknowledgement without persisting raw rejection payloads.
    - Acceptance: Publish per-interface outcomes and limits; do not substitute a generic HTTP 202 for required OTLP semantics.

  - **[LOG-ING-002](https://github.com/gntik-ai/falcone-logs/issues/21): Implement producer SDKs and optional Sentry envelope compatibility** (P1, L)
    - As an integration developer, I want supported instrumentation for Node, Go and Python, so that applications can export diagnostics predictably.
    - Description: Supported instrumentation for Node, Go and Python.
    - Requirements: FR-LOG-ING-002-1, FR-LOG-ING-002-2
    - Dependencies: [LOG-ING-001](https://github.com/gntik-ai/falcone-logs/issues/20), [LOG-CON-003](https://github.com/gntik-ai/falcone-logs/issues/19)
    - Acceptance: Test Node/Go/Python log/exception propagation, stable transport-retry IDs and current checksum/compression/protocol behavior.
    - Acceptance: Sentry read/admin APIs, replay, profiling and attachments are not implied by accepting error envelopes; review all transitive licenses.
    - Acceptance: Browser/public keys, if enabled, are scoped write-only untrusted sources and cannot assert verified user/runtime identity.

  - **[LOG-ING-003](https://github.com/gntik-ai/falcone-logs/issues/22): Implement bounded buffering, retries and loss reporting** (P1, M)
    - As an SRE, I want controlled telemetry pressure and visible loss, so that an observability outage does not exhaust applications.
    - Description: Controlled telemetry pressure and visible loss.
    - Requirements: FR-LOG-ING-003-1, FR-LOG-ING-003-2
    - Dependencies: [LOG-ING-001](https://github.com/gntik-ai/falcone-logs/issues/20), [LOG-GOV-001](https://github.com/gntik-ai/falcone-logs/issues/56)
    - Acceptance: Exercise hard kill, queue exhaustion, slow broker and poison batches; sanitize before any persistent exporter WAL.
    - Acceptance: Prioritize critical summaries within caps without promising all errors survive arbitrary overload.
    - Acceptance: Expose retry guidance and drain/shutdown budgets; no unbounded synchronous log flush on function completion.

- **[LOG-TEN](https://github.com/gntik-ai/falcone-logs/issues/3): Identity, tenancy and access** — Enforce Falcone scope across ingestion, investigation and sharing.

  - **[LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23): Integrate IAM and separate diagnostic permissions** (P1, L)
    - As a workspace administrator, I want Falcone-controlled log and error permissions, so that users see only authorized investigation data.
    - Description: Falcone-controlled log and error permissions.
    - Requirements: FR-LOG-TEN-001-1, FR-LOG-TEN-001-2
    - Dependencies: [LOG-CON-002](https://github.com/gntik-ai/falcone-logs/issues/18)
    - Acceptance: Preserve activation log/result policies and verified workspace claims; role-name or actor-type strings alone do not widen access.
    - Acceptance: Test expired tokens, wrong issuer/audience, scoped grants and platform-global redacted views.
    - Acceptance: Define bounded policy-cache and live-stream recheck behavior; unavailable required authorization fails closed.

  - **[LOG-TEN-002](https://github.com/gntik-ai/falcone-logs/issues/24): Implement trusted producer context and project enrollment** (P1, L)
    - As a runtime owner, I want resource-bound ingestion identities, so that tenant code cannot forge another execution or scope.
    - Description: Resource-bound ingestion identities.
    - Requirements: FR-LOG-TEN-002-1, FR-LOG-TEN-002-2
    - Dependencies: [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29)
    - Acceptance: Test malicious guest tenant/run/activation IDs, identical trace IDs in different tenants and revoked ingestion credentials.
    - Acceptance: Projects are Falcone configuration under existing workspaces, not a second organization/team directory.
    - Acceptance: Keep public browser ingestion explicitly untrusted and rate-limited; credentials and rotations use falcone-secrets.

  - **[LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25): Enforce isolation across search, artifacts and sharing** (P1, L)
    - As a security engineer, I want consistent scope on every retrieval path, so that facets or exports cannot bypass tenant isolation.
    - Description: Consistent scope on every retrieval path.
    - Requirements: FR-LOG-TEN-003-1, FR-LOG-TEN-003-2
    - Dependencies: [LOG-TEN-002](https://github.com/gntik-ai/falcone-logs/issues/24), [LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47)
    - Acceptance: Use PostgreSQL RLS and restricted analytical roles/policies; tenants cannot set trusted backend namespace headers.
    - Acceptance: Test saved links, autocomplete, archive rehydrate, reused cursors and scope/policy changes with same-name resources.
    - Acceptance: Source snippets require source permission; correlation IDs remain locators, never bearer authority.

- **[LOG-PRV](https://github.com/gntik-ai/falcone-logs/issues/4): Privacy and collection controls** — Prevent sensitive diagnostic content from reaching unauthorized persistence or viewers.

  - **[LOG-PRV-001](https://github.com/gntik-ai/falcone-logs/issues/26): Implement source and gateway redaction before persistence** (P1, L)
    - As a privacy engineer, I want mandatory minimization and redaction, so that logs do not become a secondary secret store.
    - Description: Mandatory minimization and redaction.
    - Requirements: FR-LOG-PRV-001-1, FR-LOG-PRV-001-2
    - Dependencies: [LOG-CON-001](https://github.com/gntik-ai/falcone-logs/issues/17), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Inject synthetic keys into nested logs, headers, signed URLs, causes, breadcrumbs and truncation boundaries; scan every persistent sink.
    - Acceptance: A policy-engine failure rejects/drops protected content with safe metadata, never stores an unfiltered fallback.
    - Acceptance: Generic auto-capture cannot bypass producer restrictions; document residual limits of redacting arbitrary unstructured text.

  - **[LOG-PRV-002](https://github.com/gntik-ai/falcone-logs/issues/27): Implement safe collection profiles and sensitive-field controls** (P1, M)
    - As a tenant privacy owner, I want explicit diagnostic collection policies, so that useful investigation does not require collecting application data.
    - Description: Explicit diagnostic collection policies.
    - Requirements: FR-LOG-PRV-002-1, FR-LOG-PRV-002-2
    - Dependencies: [LOG-PRV-001](https://github.com/gntik-ai/falcone-logs/issues/26)
    - Acceptance: Use metadata-only rejection/quarantine by default; disabled content cannot leak through enrichment, exports or alerts.
    - Acceptance: Test policy version changes, nested attribute limits and unparseable SQL/Mongo shapes; hashing raw secrets is not anonymization.
    - Acceptance: Publish per-source available/omitted fields so the UI does not imply a missing stack or payload can be reconstructed.

  - **[LOG-PRV-003](https://github.com/gntik-ai/falcone-logs/issues/28): Harden untrusted content, enrichment and export rendering** (P1, L)
    - As a security reviewer, I want bounded safe processing of logs and artifacts, so that hostile tenant content cannot attack operators.
    - Description: Bounded safe processing of logs and artifacts.
    - Requirements: FR-LOG-PRV-003-1, FR-LOG-PRV-003-2
    - Dependencies: [LOG-PRV-002](https://github.com/gntik-ai/falcone-logs/issues/27), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Test stored XSS, ANSI injection, archive traversal/bombs, regex denial of service and malicious source maps.
    - Acceptance: Disable arbitrary source-map URLs; any future fetch/destination uses scoped egress, TLS, DNS and redirect checks.
    - Acceptance: Keep model-assisted investigation optional and treat log content as untrusted data, not tool instructions.

- **[LOG-COR](https://github.com/gntik-ai/falcone-logs/issues/5): Telemetry schema and execution correlation** — Connect diagnostic signals to trusted Falcone execution lineage.

  - **[LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29): Define canonical events and provenance metadata** (P0, M)
    - As an integration architect, I want one versioned diagnostic envelope, so that sources can be analyzed without losing their semantics.
    - Description: One versioned diagnostic envelope.
    - Requirements: FR-LOG-COR-001-1, FR-LOG-COR-001-2
    - Dependencies: [LOG-CON-002](https://github.com/gntik-ai/falcone-logs/issues/18)
    - Acceptance: Cover log/error/span/query events, producer epoch/sequence, source/observed times and truncation/sampling/loss flags.
    - Acceptance: Keep audit event schema and existing Falcone correlation IDs distinct from OTel trace identity.
    - Acceptance: Publish fixtures for two tenants, legacy aliases, unknown fields and version evolution; reject ambiguous ownership.

  - **[LOG-COR-002](https://github.com/gntik-ai/falcone-logs/issues/30): Propagate trace context across asynchronous boundaries** (P1, L)
    - As a developer, I want linked logs and spans across services, so that I can follow one operation through Falcone.
    - Description: Linked logs and spans across services.
    - Requirements: FR-LOG-COR-002-1, FR-LOG-COR-002-2
    - Dependencies: [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29), [LOG-TEN-002](https://github.com/gntik-ai/falcone-logs/issues/24)
    - Acceptance: Test flow-to-function-to-database, Kafka delivery, child runs, retry attempts and missing trace headers.
    - Acceptance: Preserve source sequence and clock uncertainty; do not infer global order or root cause from receipt time.
    - Acceptance: Expose sampled/missing spans and link provenance; reused trace IDs cannot cross tenant authorization.

  - **[LOG-COR-003](https://github.com/gntik-ai/falcone-logs/issues/31): Integrate flow timelines and resumable diagnostic overlays** (P2, L)
    - As a flow author, I want node and attempt diagnostics beside the run graph, so that I can investigate failed or retried steps.
    - Description: Node and attempt diagnostics beside the run graph.
    - Requirements: FR-LOG-COR-003-1, FR-LOG-COR-003-2
    - Dependencies: [LOG-COR-002](https://github.com/gntik-ai/falcone-logs/issues/30), [LOG-ING-003](https://github.com/gntik-ai/falcone-logs/issues/22), [LOG-SEA-002](https://github.com/gntik-ai/falcone-logs/issues/45)
    - Acceptance: Test current Temporal history frames and native workflow events, long waits, nested flows and terminal/retry outcomes.
    - Acceptance: Reconstruction/replay cannot emit old logs as new occurrences; late diagnostics cannot rewrite workflow outcome.
    - Acceptance: Issue triage cannot resolve workflow incidents or rerun nodes; cross-repository producer/console changes require owned handoffs.

- **[LOG-FUN](https://github.com/gntik-ai/falcone-logs/issues/6): Function and runtime diagnostics** — Capture scoped execution evidence without changing runtime authority or isolation.

  - **[LOG-FUN-001](https://github.com/gntik-ai/falcone-logs/issues/32): Capture trusted activation and attempt logs** (P1, L)
    - As a function developer, I want logs tied to the correct activation and revision, so that concurrent executions can be investigated separately.
    - Description: Logs tied to the correct activation and revision.
    - Requirements: FR-LOG-FUN-001-1, FR-LOG-FUN-001-2
    - Dependencies: [LOG-ING-002](https://github.com/gntik-ai/falcone-logs/issues/21), [LOG-COR-002](https://github.com/gntik-ai/falcone-logs/issues/30)
    - Acceptance: Test concurrent invocations and tenant-supplied forged context; OCI pod stdout remains pod/revision-level unless attribution is proven.
    - Acceptance: Integrate current Knative activation responses plus native host/shim contracts without exposing broad ingestion credentials to guests.
    - Acceptance: Keep logs, results and source read permissions separate and preserve activation retention/error envelopes.

  - **[LOG-FUN-002](https://github.com/gntik-ai/falcone-logs/issues/33): Capture runtime failures and execution timing safely** (P1, M)
    - As an operator, I want termination and timing evidence beyond application exceptions, so that timeouts or host crashes are diagnosable.
    - Description: Termination and timing evidence beyond application exceptions.
    - Requirements: FR-LOG-FUN-002-1, FR-LOG-FUN-002-2
    - Dependencies: [LOG-FUN-001](https://github.com/gntik-ai/falcone-logs/issues/32)
    - Acceptance: Test OOM/kill, crash before flush, cancelled attempts, missing stacks and successful execution during logs-service outage.
    - Acceptance: Do not infer invocation attribution from pod labels alone when several executions share a runtime.
    - Acceptance: Collection remains namespaced and approved; no privileged node agent or eBPF dependency is introduced.

  - **[LOG-FUN-003](https://github.com/gntik-ai/falcone-logs/issues/34): Link function diagnostics to callers, artifacts and releases** (P2, M)
    - As a runtime maintainer, I want verified diagnostic links to invoking flows and deployed code, so that developers can identify the affected execution context.
    - Description: Verified diagnostic links to invoking flows and deployed code.
    - Requirements: FR-LOG-FUN-003-1, FR-LOG-FUN-003-2
    - Dependencies: [LOG-FUN-002](https://github.com/gntik-ai/falcone-logs/issues/33), [LOG-REL-001](https://github.com/gntik-ai/falcone-logs/issues/41), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25)
    - Acceptance: Test flow caller, standalone invocation, stale revision, artifact digest mismatch and missing debug data.
    - Acceptance: Expired activation access cannot be bypassed by trace lookup, archive search or a saved error link.
    - Acceptance: Record serverless/main Falcone instrumentation and UI handoffs separately; logs does not own runtime scheduling.

- **[LOG-QRY](https://github.com/gntik-ai/falcone-logs/issues/7): Database query diagnostics** — Analyze datasource errors and performance without capturing business data by default.

  - **[LOG-QRY-001](https://github.com/gntik-ai/falcone-logs/issues/35): Instrument trusted PostgreSQL and MongoDB execution seams** (P1, L)
    - As a data-service developer, I want safe per-operation timing and failure events, so that I can diagnose datasource behavior from Falcone.
    - Description: Safe per-operation timing and failure events.
    - Requirements: FR-LOG-QRY-001-1, FR-LOG-QRY-001-2
    - Dependencies: [LOG-ING-002](https://github.com/gntik-ai/falcone-logs/issues/21), [LOG-COR-002](https://github.com/gntik-ai/falcone-logs/issues/30), [LOG-PRV-002](https://github.com/gntik-ai/falcone-logs/issues/27)
    - Acceptance: Test workflow/function-origin queries, direct data API operations, cancellation, timeout and opaque driver causes.
    - Acceptance: Separate pool wait, client duration and measured server time; define Mongo cursor lifetime rather than reporting dispatch as full execution.
    - Acceptance: Never include connection strings, bind values, rows/documents or embedding vectors in default events.

  - **[LOG-QRY-002](https://github.com/gntik-ai/falcone-logs/issues/36): Implement sanitized query shapes and performance analysis** (P1, L)
    - As a workspace developer, I want aggregates by safe query shape, so that I can find slow or repeatedly failing operations.
    - Description: Aggregates by safe query shape.
    - Requirements: FR-LOG-QRY-002-1, FR-LOG-QRY-002-2
    - Dependencies: [LOG-QRY-001](https://github.com/gntik-ai/falcone-logs/issues/35), [LOG-SEA-001](https://github.com/gntik-ai/falcone-logs/issues/44)
    - Acceptance: Test literals/comments, identifiers, SQL dialects and Mongo filters without exposing values; version normalized fingerprints.
    - Acceptance: Repeated-call/N+1 and regression results are evidence-backed candidates, not automatic root-cause claims.
    - Acceptance: Do not derive exact failure rates from sampled errors or conflate client/network latency with server execution time.

  - **[LOG-QRY-003](https://github.com/gntik-ai/falcone-logs/issues/37): Provide safe query error detail and optional plan artifacts** (P2, M)
    - As a database operator, I want controlled query investigation details, so that I can investigate failures without granting execution rights to logs.
    - Description: Controlled query investigation details.
    - Requirements: FR-LOG-QRY-003-1, FR-LOG-QRY-003-2
    - Dependencies: [LOG-QRY-002](https://github.com/gntik-ai/falcone-logs/issues/36), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25)
    - Acceptance: Test plan/source access distinct from log access and redact plan constants or sensitive identifiers.
    - Acceptance: Unknown normalization/plan data is shown as unavailable; no hidden diagnostic re-execution changes production state.
    - Acceptance: Publish supported PostgreSQL/MongoDB categories and plan-profile limits; add other query systems through separate adapters.

- **[LOG-ERR](https://github.com/gntik-ai/falcone-logs/issues/8): Error grouping and issue lifecycle** — Turn occurrences into actionable Falcone issues with correct counts and history.

  - **[LOG-ERR-001](https://github.com/gntik-ai/falcone-logs/issues/38): Implement deterministic scoped error grouping** (P1, L)
    - As a developer, I want similar exceptions grouped into issues, so that I can prioritize recurring problems.
    - Description: Similar exceptions grouped into issues.
    - Requirements: FR-LOG-ERR-001-1, FR-LOG-ERR-001-2
    - Dependencies: [LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29), [LOG-PRV-001](https://github.com/gntik-ai/falcone-logs/issues/26)
    - Acceptance: Test exception types/stacks/templates with variable IDs and values, expected cancellations and missing stacks.
    - Acceptance: Release IDs do not fragment default grouping; client fingerprint hints cannot merge another scope.
    - Acceptance: Record grouping version and provenance; unrelated flow/function/query errors can be linked without pretending causal identity.

  - **[LOG-ERR-002](https://github.com/gntik-ai/falcone-logs/issues/39): Implement assignment, triage and concurrent state transitions** (P1, M)
    - As a team maintainer, I want assignable and auditable error states, so that developers can coordinate investigation.
    - Description: Assignable and auditable error states.
    - Requirements: FR-LOG-ERR-002-1, FR-LOG-ERR-002-2
    - Dependencies: [LOG-ERR-001](https://github.com/gntik-ai/falcone-logs/issues/38), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Test concurrent resolve/assign, stale revisions, unauthorized assignees and expired snoozes.
    - Acceptance: Assignments refer to Falcone IAM users/teams rather than a new directory; comments are escaped and scoped.
    - Acceptance: Display exact accepted occurrence counts separately from sampled estimates, affected-user estimates and actual business impact.

  - **[LOG-ERR-003](https://github.com/gntik-ai/falcone-logs/issues/40): Implement grouping revisions, merge and split** (P2, L)
    - As an error-triage owner, I want controlled grouping corrections, so that noisy or incorrectly combined issues can be repaired.
    - Description: Controlled grouping corrections.
    - Requirements: FR-LOG-ERR-003-1, FR-LOG-ERR-003-2
    - Dependencies: [LOG-ERR-002](https://github.com/gntik-ai/falcone-logs/issues/39), [LOG-GOV-003](https://github.com/gntik-ai/falcone-logs/issues/58)
    - Acceptance: Preview affected scoped events, apply with fencing/revision checks and support an auditable reversal where defined.
    - Acceptance: Test algorithm upgrades, late events, replay windows and duplicate storage rows.
    - Acceptance: Do not execute tenant scripts/unbounded regexes; related-error suggestions retain confidence/provenance and never auto-merge across scope.

- **[LOG-REL](https://github.com/gntik-ai/falcone-logs/issues/9): Releases and source-level diagnosis** — Connect errors to immutable deployed code and qualified debug artifacts.

  - **[LOG-REL-001](https://github.com/gntik-ai/falcone-logs/issues/41): Implement release, deployment and artifact identity** (P1, M)
    - As a release engineer, I want scoped build and deployment records, so that errors can be investigated against the deployed revision.
    - Description: Scoped build and deployment records.
    - Requirements: FR-LOG-REL-001-1, FR-LOG-REL-001-2
    - Dependencies: [LOG-CON-002](https://github.com/gntik-ai/falcone-logs/issues/18), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Treat release strings as opaque IDs; track actual deployment ordering, rollback and concurrent canary deployments.
    - Acceptance: Store artifacts through falcone-s3 native/external bindings with secrets-managed credentials and verified manifests.
    - Acceptance: Wrong digest/debug ID or unauthorized upload cannot replace another release artifact.

  - **[LOG-REL-002](https://github.com/gntik-ai/falcone-logs/issues/42): Implement safe source-map and stack enrichment** (P2, L)
    - As a developer, I want readable source locations for approved runtimes, so that I can diagnose exceptions in deployed code.
    - Description: Readable source locations for approved runtimes.
    - Requirements: FR-LOG-REL-002-1, FR-LOG-REL-002-2
    - Dependencies: [LOG-REL-001](https://github.com/gntik-ai/falcone-logs/issues/41), [LOG-PRV-003](https://github.com/gntik-ai/falcone-logs/issues/28), [LOG-ERR-001](https://github.com/gntik-ai/falcone-logs/issues/38)
    - Acceptance: Start with JS/TS source maps and already-symbolic Node/Python/Go frames; WASM/native formats require separate qualification.
    - Acceptance: Test missing/late maps, malicious archives, embedded source secrets and mismatched builds without executing code or fetching arbitrary URLs.
    - Acceptance: Enrichment cannot duplicate events, silently change counts or expose source snippets to log-only viewers.

  - **[LOG-REL-003](https://github.com/gntik-ai/falcone-logs/issues/43): Detect regressions using deployment-aware evidence** (P2, L)
    - As a release owner, I want reliable new/regressed-error indicators, so that late data does not create false release alarms.
    - Description: Reliable new/regressed-error indicators.
    - Requirements: FR-LOG-REL-003-1, FR-LOG-REL-003-2
    - Dependencies: [LOG-REL-002](https://github.com/gntik-ai/falcone-logs/issues/42), [LOG-ERR-002](https://github.com/gntik-ai/falcone-logs/issues/39)
    - Acceptance: Test resolve-in-release, rollback, redeploy, parallel canaries and delayed event ingestion.
    - Acceptance: Compare only compatible collection/sampling windows and show observed counts/coverage.
    - Acceptance: Commit regression transition and alert intent once; release correlation is not proof that a commit caused the bug.

- **[LOG-SEA](https://github.com/gntik-ai/falcone-logs/issues/10): Search, live tail and exports** — Provide useful investigation queries within enforced scope and cost limits.

  - **[LOG-SEA-001](https://github.com/gntik-ai/falcone-logs/issues/44): Implement scoped log, error and trace search** (P1, L)
    - As a developer, I want field/text/time search and safe aggregates, so that I can find relevant diagnostic evidence quickly.
    - Description: Field/text/time search and safe aggregates.
    - Requirements: FR-LOG-SEA-001-1, FR-LOG-SEA-001-2
    - Dependencies: [LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47), [LOG-TEN-002](https://github.com/gntik-ai/falcone-logs/issues/24), [LOG-GOV-001](https://github.com/gntik-ai/falcone-logs/issues/56)
    - Acceptance: Test severity/service/release/run/activation/query filters, facets and logs-to-trace joins under two tenants.
    - Acceptance: No raw backend SQL or external table functions; enforce deadline/scanned-byte limits and server-side cancellation.
    - Acceptance: Use opaque scoped cursors and defined concurrent-ingest ordering; missing data is not returned as healthy or zero errors.

  - **[LOG-SEA-002](https://github.com/gntik-ai/falcone-logs/issues/45): Implement resumable authorized live tail** (P1, M)
    - As an operator, I want live logs with clear reconnect behavior, so that I can investigate running work without losing track of gaps.
    - Description: Live logs with clear reconnect behavior.
    - Requirements: FR-LOG-SEA-002-1, FR-LOG-SEA-002-2
    - Dependencies: [LOG-SEA-001](https://github.com/gntik-ai/falcone-logs/issues/44), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Test reconnect, slow clients, tenant changes, token expiry and concurrent source streams; no globally ordered log promise.
    - Acceptance: Preserve current workflow SSE endpoint/cursor independently; add new tail transport through Falcone conventions.
    - Acceptance: Support SSE first where appropriate and a qualified WebSocket adapter if required, with equivalent auth/backpressure semantics.

  - **[LOG-SEA-003](https://github.com/gntik-ai/falcone-logs/issues/46): Implement redacted exports and bounded archive investigations** (P2, L)
    - As a support engineer, I want controlled exports and older evidence retrieval, so that investigations remain reproducible without bypassing policy.
    - Description: Controlled exports and older evidence retrieval.
    - Requirements: FR-LOG-SEA-003-1, FR-LOG-SEA-003-2
    - Dependencies: [LOG-SEA-001](https://github.com/gntik-ai/falcone-logs/issues/44), [LOG-STO-002](https://github.com/gntik-ai/falcone-logs/issues/48), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25), [LOG-PRV-003](https://github.com/gntik-ai/falcone-logs/issues/28)
    - Acceptance: Test hot/cold overlap dedupe, cancelled jobs, expired data, cross-tenant manifests and partial archives.
    - Acceptance: Protect CSV/JSON downloads from injection and secret leakage; choose proxied retrieval when immediate revocation is required.
    - Acceptance: Saved export links do not preserve access after policy revocation; all objects have explicit lifecycle and cleanup.

- **[LOG-STO](https://github.com/gntik-ai/falcone-logs/issues/11): Storage, idempotency and retention** — Store diagnostic evidence with truthful consistency and deletion guarantees.

  - **[LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47): Implement analytical projections and exact issue-state persistence** (P1, L)
    - As a platform engineer, I want separate transactional state and scalable telemetry storage, so that search load does not corrupt issue lifecycle.
    - Description: Separate transactional state and scalable telemetry storage.
    - Requirements: FR-LOG-STO-001-1, FR-LOG-STO-001-2
    - Dependencies: [LOG-CON-003](https://github.com/gntik-ai/falcone-logs/issues/19), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Test broker replay, changed insert batch boundaries, lost acknowledgements and index failure around PostgreSQL commit.
    - Acceptance: Qualify ClickHouse dedupe/FINAL or equivalent semantics; naive materialized sums of duplicate raw rows cannot drive exact alerts.
    - Acceptance: Expose independent consumer watermarks; no cross-Kafka/PostgreSQL/ClickHouse transaction or unlimited dedupe window is claimed.

  - **[LOG-STO-002](https://github.com/gntik-ai/falcone-logs/issues/48): Implement verified S3 archives and debug/export storage** (P2, L)
    - As a storage operator, I want scoped immutable diagnostic archives, so that hot retention can be bounded while selected evidence remains available.
    - Description: Scoped immutable diagnostic archives.
    - Requirements: FR-LOG-STO-002-1, FR-LOG-STO-002-2
    - Dependencies: [LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47), [LOG-PRV-002](https://github.com/gntik-ai/falcone-logs/issues/27)
    - Acceptance: Test interrupted uploads, orphan cleanup, missing/wrong object versions, failed manifest commit and restore.
    - Acceptance: Rehydrate only authorized bounded ranges, with temporary index expiry and visible coverage/cost.
    - Acceptance: Do not assume every S3 provider supports identical retention or instant signed-link revocation.

  - **[LOG-STO-003](https://github.com/gntik-ai/falcone-logs/issues/49): Implement retention, tombstones and privacy purge** (P2, L)
    - As a privacy administrator, I want effective deletion across all diagnostic copies, so that expired or deleted data cannot reappear through archives or replay.
    - Description: Effective deletion across all diagnostic copies.
    - Requirements: FR-LOG-STO-003-1, FR-LOG-STO-003-2
    - Dependencies: [LOG-STO-002](https://github.com/gntik-ai/falcone-logs/issues/48), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25)
    - Acceptance: Test source expiry, tenant purge, late Kafka delivery, archive rehydrate and restore before serving reads.
    - Acceptance: Separate logical inaccessibility from physical deletion in ClickHouse, mixed Kafka segments, shared archives and backups.
    - Acceptance: Audit legal holds and conflicts; derived fingerprints/comments/source snippets are part of the deletion inventory.

- **[LOG-ALT](https://github.com/gntik-ai/falcone-logs/issues/12): Alerts and controlled integrations** — Notify on actionable diagnostic conditions without duplicate storms or hidden side effects.

  - **[LOG-ALT-001](https://github.com/gntik-ai/falcone-logs/issues/50): Implement scoped alert rules and state transitions** (P2, L)
    - As an application owner, I want alerts on new errors, regressions and sustained failures, so that problems are visible before users report them.
    - Description: Alerts on new errors, regressions and sustained failures.
    - Requirements: FR-LOG-ALT-001-1, FR-LOG-ALT-001-2
    - Dependencies: [LOG-ERR-002](https://github.com/gntik-ai/falcone-logs/issues/39), [LOG-REL-003](https://github.com/gntik-ai/falcone-logs/issues/43), [LOG-SEA-001](https://github.com/gntik-ai/falcone-logs/issues/44)
    - Acceptance: Support new/regressed issue, error/latency threshold, slow query and ingestion-lag conditions with previews.
    - Acceptance: Test late events, missing denominators, changed sampling, snooze/mute schedules and recovery transitions.
    - Acceptance: Alert state/outbox commit atomically in its store; core evaluation does not depend on workflow/serverless health.

  - **[LOG-ALT-002](https://github.com/gntik-ai/falcone-logs/issues/51): Implement approved notification delivery and incident history** (P2, L)
    - As an on-call operator, I want reliable scoped notifications, so that alerts can be routed without leaking customer data.
    - Description: Reliable scoped notifications.
    - Requirements: FR-LOG-ALT-002-1, FR-LOG-ALT-002-2
    - Dependencies: [LOG-ALT-001](https://github.com/gntik-ai/falcone-logs/issues/50), [LOG-PRV-003](https://github.com/gntik-ai/falcone-logs/issues/28)
    - Acceptance: Test webhook signing/rotation, timeout after remote success, provider rate limits, disabled endpoints and SSRF/redirect changes.
    - Acceptance: Console/email/webhook adapters are capabilities; no live destination is enabled by repository bootstrap.
    - Acceptance: Maintain incident/notification history separately from error triage and workflow-owned incidents.

  - **[LOG-ALT-003](https://github.com/gntik-ai/falcone-logs/issues/52): Implement explicit GitHub and workflow integration commands** (P2, M)
    - As a team lead, I want controlled links to engineering and response workflows, so that investigation can lead to authorized follow-up work.
    - Description: Controlled links to engineering and response workflows.
    - Requirements: FR-LOG-ALT-003-1, FR-LOG-ALT-003-2
    - Dependencies: [LOG-ALT-002](https://github.com/gntik-ai/falcone-logs/issues/51), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25)
    - Acceptance: Default to links and previews; log-read permission alone cannot send data to GitHub, a webhook or a model.
    - Acceptance: Test ticket dedupe, bidirectional status conflicts, revoked credentials and alert-triggered workflow recursion.
    - Acceptance: Resolving an error never automatically reruns a function or executes a database query; such commands use owning-service authorization.

- **[LOG-UI](https://github.com/gntik-ai/falcone-logs/issues/13): Falcone console and developer API** — Provide one coherent investigation experience inside Falcone.

  - **[LOG-UI-001](https://github.com/gntik-ai/falcone-logs/issues/53): Build integrated log, issue and execution investigation views** (P2, L)
    - As a Falcone developer, I want connected investigation pages, so that I can move from a failure to its context without switching products.
    - Description: Connected investigation pages.
    - Requirements: FR-LOG-UI-001-1, FR-LOG-UI-001-2
    - Dependencies: [LOG-SEA-002](https://github.com/gntik-ai/falcone-logs/issues/45), [LOG-ERR-002](https://github.com/gntik-ai/falcone-logs/issues/39), [LOG-COR-003](https://github.com/gntik-ai/falcone-logs/issues/31), [LOG-FUN-003](https://github.com/gntik-ai/falcone-logs/issues/34), [LOG-QRY-002](https://github.com/gntik-ai/falcone-logs/issues/36)
    - Acceptance: Test one flow-function-query failure journey plus empty, denied, stale, partial and expired-evidence states.
    - Acceptance: Keep current navigation and IAM context; issue assignment/status is visibly distinct from run status and action controls.
    - Acceptance: Implement console changes in the owning Falcone repository with contracts and links tracked from this story.

  - **[LOG-UI-002](https://github.com/gntik-ai/falcone-logs/issues/54): Implement saved views, dashboards and scoped sharing** (P2, M)
    - As a workspace team member, I want reusable investigation views, so that the team can compare incidents and releases consistently.
    - Description: Reusable investigation views.
    - Requirements: FR-LOG-UI-002-1, FR-LOG-UI-002-2
    - Dependencies: [LOG-UI-001](https://github.com/gntik-ai/falcone-logs/issues/53), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25)
    - Acceptance: Support release/error/latency/log-volume panels using compatible denominators and bounded queries.
    - Acceptance: Test revoked members, copied URLs, timezone changes, deleted resources and renamed fields.
    - Acceptance: No workspace share becomes a public link or widens to tenant/platform scope automatically.

  - **[LOG-UI-003](https://github.com/gntik-ai/falcone-logs/issues/55): Publish versioned APIs, CLI workflows and synthetic examples** (P1, M)
    - As an integration developer, I want documented machine interfaces, so that I can automate safe diagnostic workflows.
    - Description: Documented machine interfaces.
    - Requirements: FR-LOG-UI-003-1, FR-LOG-UI-003-2
    - Dependencies: [LOG-CON-001](https://github.com/gntik-ai/falcone-logs/issues/17), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: Provide synthetic Node/Go/Python scenarios with two tenants, a retrying flow, a function exception and sanitized query failure.
    - Acceptance: Document safe credential handling, pagination, retry/partial success and cancellation; no production tokens or raw data in fixtures.
    - Acceptance: API compatibility tests protect existing audit/SSE/activation behavior while new schemas evolve additively.

- **[LOG-GOV](https://github.com/gntik-ai/falcone-logs/issues/14): Quotas, sampling and resource governance** — Keep diagnostic cost and fairness under Falcone policy.

  - **[LOG-GOV-001](https://github.com/gntik-ai/falcone-logs/issues/56): Implement Falcone ingestion and query resource budgets** (P1, L)
    - As a platform administrator, I want central limits for diagnostic resources, so that one noisy tenant cannot exhaust the service.
    - Description: Central limits for diagnostic resources.
    - Requirements: FR-LOG-GOV-001-1, FR-LOG-GOV-001-2
    - Dependencies: [LOG-CON-002](https://github.com/gntik-ai/falcone-logs/issues/18), [LOG-TEN-001](https://github.com/gntik-ai/falcone-logs/issues/23)
    - Acceptance: No independent billing-plan definitions; record current quota failure semantics and any new policy decision explicitly.
    - Acceptance: Test bursty tenants, high-cardinality attributes, slow queries/subscribers and competing archive/symbolication work.
    - Acceptance: Security/privacy denials never fail open; physical queue/memory safety remains enforced regardless of business quota mode.

  - **[LOG-GOV-002](https://github.com/gntik-ai/falcone-logs/issues/57): Implement sampling, usage facts and coverage reporting** (P1, L)
    - As a product operator, I want visible cost and loss decisions, so that sampled diagnostics do not misrepresent platform usage.
    - Description: Visible cost and loss decisions.
    - Requirements: FR-LOG-GOV-002-1, FR-LOG-GOV-002-2
    - Dependencies: [LOG-GOV-001](https://github.com/gntik-ai/falcone-logs/issues/56), [LOG-COR-001](https://github.com/gntik-ai/falcone-logs/issues/29)
    - Acceptance: Keep sampled telemetry separate from authoritative billing/audit and execution-success denominators.
    - Acceptance: Test error-priority overload, head/tail sampling constraints and changes between comparison windows.
    - Acceptance: Do not extrapolate exact users/error rates from unknown sampling; duplicates cannot become fresh billable logical events by accident.

  - **[LOG-GOV-003](https://github.com/gntik-ai/falcone-logs/issues/58): Implement bounded replay, reprocessing and schema evolution** (P2, L)
    - As a maintainer, I want safe replay and enrichment upgrades, so that historical data can be repaired without resurrecting deleted events.
    - Description: Safe replay and enrichment upgrades.
    - Requirements: FR-LOG-GOV-003-1, FR-LOG-GOV-003-2
    - Dependencies: [LOG-STO-001](https://github.com/gntik-ai/falcone-logs/issues/47), [LOG-GOV-002](https://github.com/gntik-ai/falcone-logs/issues/57)
    - Acceptance: Test changed batches, DLQ replay, algorithm upgrades, expired dedupe windows and import namespaces.
    - Acceptance: Track independent projection watermarks and partial completion; processing failures do not silently discard admitted events.
    - Acceptance: Keep original sanitized identity immutable while derived projections evolve; no blind reset of alert/dedupe state during recovery.

- **[LOG-OPS](https://github.com/gntik-ai/falcone-logs/issues/15): Restricted deployment and reliability** — Operate the service without expanding Falcone runtime privileges.

  - **[LOG-OPS-001](https://github.com/gntik-ai/falcone-logs/issues/59): Package namespaced collection and approved backend profiles** (P1, L)
    - As a platform operator, I want deployment compatible with restricted OpenShift, so that observability does not require unavailable cluster permissions.
    - Description: Deployment compatible with restricted OpenShift.
    - Requirements: FR-LOG-OPS-001-1, FR-LOG-OPS-001-2
    - Dependencies: [LOG-CON-003](https://github.com/gntik-ai/falcone-logs/issues/19), [LOG-ING-001](https://github.com/gntik-ai/falcone-logs/issues/20)
    - Acceptance: Test standard Kubernetes and actual corporate OpenShift builds, writable volume permissions, egress/TLS and pinned images.
    - Acceptance: Reuse approved infrastructure and namespaced SDK/gateway export; no compatible ClickHouse/Loki/OpenSearch deployment is assumed.
    - Acceptance: Development/small profiles expose their limits and cannot advertise production throughput or durability.

  - **[LOG-OPS-002](https://github.com/gntik-ai/falcone-logs/issues/60): Implement SLOs, independent health and incident runbooks** (P2, M)
    - As an SRE, I want measurable ingestion/search/alert health, so that the logs service can diagnose its own degradation.
    - Description: Measurable ingestion/search/alert health.
    - Requirements: FR-LOG-OPS-002-1, FR-LOG-OPS-002-2
    - Dependencies: [LOG-OPS-001](https://github.com/gntik-ai/falcone-logs/issues/59), [LOG-GOV-002](https://github.com/gntik-ai/falcone-logs/issues/57), [LOG-ALT-002](https://github.com/gntik-ai/falcone-logs/issues/51)
    - Acceptance: Measure proposed availability, acceptance/freshness/search/overhead targets against stated datasets and concurrency.
    - Acceptance: Exercise broker/index/IAM/secrets/S3 outages and logging storms; minimal independent health metrics remain available.
    - Acceptance: Provide runbooks for poison events, raw-data exposure, stuck purges, duplicate alerts and incomplete restores.

  - **[LOG-OPS-003](https://github.com/gntik-ai/falcone-logs/issues/61): Implement coordinated backup and diagnostic recovery** (P2, L)
    - As a recovery operator, I want restorable product state and evidence, so that incidents can be investigated after infrastructure failure.
    - Description: Restorable product state and evidence.
    - Requirements: FR-LOG-OPS-003-1, FR-LOG-OPS-003-2
    - Dependencies: [LOG-OPS-001](https://github.com/gntik-ai/falcone-logs/issues/59), [LOG-STO-003](https://github.com/gntik-ai/falcone-logs/issues/49), [LOG-GOV-003](https://github.com/gntik-ai/falcone-logs/issues/58)
    - Acceptance: Test cold start with independent secrets bootstrap, PostgreSQL recovery and ClickHouse rebuild from available Kafka/archive windows.
    - Acceptance: Do not resend historical alerts or resurrect expired telemetry after offset reset/backup restore.
    - Acceptance: Measure dataset-dependent analytical recovery separately from the proposed metadata service target; missing source data remains a reported gap.

- **[LOG-DEV](https://github.com/gntik-ai/falcone-logs/issues/16): Implementation quality and controlled rollout** — Qualify the new service before collecting production diagnostic data.

  - **[LOG-DEV-001](https://github.com/gntik-ai/falcone-logs/issues/62): Implement reproducible builds and maintenance gates** (P1, M)
    - As a maintainer, I want attributable secure releases, so that components can be updated without silent protocol or policy drift.
    - Description: Attributable secure releases.
    - Requirements: FR-LOG-DEV-001-1, FR-LOG-DEV-001-2
    - Dependencies: [LOG-CON-003](https://github.com/gntik-ai/falcone-logs/issues/19), [LOG-UI-003](https://github.com/gntik-ai/falcone-logs/issues/55)
    - Acceptance: Scan for credentials, vulnerable dependencies and unsafe permissions with owned time-limited exceptions.
    - Acceptance: Do not copy FSL/enterprise code under an assumed open-source license; choose the repository license before implementation distribution.
    - Acceptance: Keep requirement/backlog/issue IDs reproducible and validate dependency/parent links without claiming a generated plan is tested runtime code.

  - **[LOG-DEV-002](https://github.com/gntik-ai/falcone-logs/issues/63): Qualify privacy, isolation, protocol and failure behavior** (P3, L)
    - As an independent reviewer, I want adversarial and recovery evidence, so that the investigation service does not expose tenant data or misreport incidents.
    - Description: Adversarial and recovery evidence.
    - Requirements: FR-LOG-DEV-002-1, FR-LOG-DEV-002-2
    - Dependencies: [LOG-DEV-001](https://github.com/gntik-ai/falcone-logs/issues/62), [LOG-TEN-003](https://github.com/gntik-ai/falcone-logs/issues/25), [LOG-PRV-003](https://github.com/gntik-ai/falcone-logs/issues/28), [LOG-OPS-003](https://github.com/gntik-ai/falcone-logs/issues/61), [LOG-REL-003](https://github.com/gntik-ai/falcone-logs/issues/43), [LOG-QRY-003](https://github.com/gntik-ai/falcone-logs/issues/37)
    - Acceptance: Test all sinks including exporter WAL/DLQ, caches, facets, archives and backup restore with synthetic data.
    - Acceptance: Inject crashes around broker/PG/index/outbox boundaries, changed batches, stale workers and late release events.
    - Acceptance: Record residual source-loss/privacy limits and owned exceptions; no upstream certification or perfect redaction claim.

  - **[LOG-DEV-003](https://github.com/gntik-ai/falcone-logs/issues/64): Run cross-service canaries and controlled production rollout** (P3, L)
    - As a Falcone product owner, I want verified incremental adoption, so that the new service improves investigation without disrupting workloads.
    - Description: Verified incremental adoption.
    - Requirements: FR-LOG-DEV-003-1, FR-LOG-DEV-003-2
    - Dependencies: [LOG-DEV-002](https://github.com/gntik-ai/falcone-logs/issues/63), [LOG-UI-002](https://github.com/gntik-ai/falcone-logs/issues/54), [LOG-COR-003](https://github.com/gntik-ai/falcone-logs/issues/31), [LOG-FUN-003](https://github.com/gntik-ai/falcone-logs/issues/34), [LOG-QRY-003](https://github.com/gntik-ai/falcone-logs/issues/37), [LOG-ALT-003](https://github.com/gntik-ai/falcone-logs/issues/52), [LOG-SEA-003](https://github.com/gntik-ai/falcone-logs/issues/46), [LOG-OPS-002](https://github.com/gntik-ai/falcone-logs/issues/60)
    - Acceptance: Demonstrate flow-function-query investigations for two tenants including retries, crash gaps, source maps and archive recovery.
    - Acceptance: Keep current audit, metrics and execution history authoritative; no Sentry migration or runtime replacement is assumed.
    - Acceptance: Track reviewed changes in main Falcone, sibling services and charts before enabling production collection or outgoing actions.

