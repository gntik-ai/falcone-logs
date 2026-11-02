#!/usr/bin/env python3
"""Generate Falcone logs planning artifacts. No runtime or remote publication."""
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPO='gntik-ai/falcone-logs'
DATE='2026-11-02'
BASELINE='4b6ef9736cb78deec346537b1c0b8eea8b79c34c'
EPICS=[]

def epic(code,title,outcome):
    e=dict(id=f'LOG-{code}',category=code.lower(),title=title,outcome=outcome,stories=[])
    EPICS.append(e)
    return e

def story(e,title,persona,want,benefit,phase,effort,deps,requirements,acceptance):
    sid=f"{e['id']}-{len(e['stories'])+1:03d}"
    e['stories'].append(dict(id=sid,title=title,description=want[0].upper()+want[1:]+'.',
        story=f'As {persona}, I want {want}, so that {benefit}.',phase=phase,effort=effort,dependencies=deps,
        requirements=[dict(id=f'FR-{sid}-{i+1}',statement=r) for i,r in enumerate(requirements)],acceptance=acceptance))

e=epic('CON','Falcone contracts and product boundaries','Define a custom investigation service that preserves current Falcone behavior.')
story(e,'Freeze log, error and execution contract inventory','a Falcone maintainer','versioned fixtures for all diagnostic producers and consumers','new analysis preserves existing contracts','P0','M',[],[
 'The project must inventory deployed log/error sources, flow SSE, activation policies, query adapters, audit and metric contracts against a pinned Falcone revision.',
 'Existing public schemas, scope checks, error precedence and stream resume behavior must remain covered by compatibility fixtures.'
],[ 'Include main Falcone, current Temporal/Knative paths and planned native sibling contracts without treating proposals as deployed functionality.', 'Preserve fix-1118 query-key logging restrictions, separate log/result permissions and governed audit failure semantics.', 'Identify actual collectors, versions, raw Sentry consumers if any, datasource coverage and current retention; record evidence gaps.' ])
story(e,'Define ownership, source enrollment and integration handoffs','a platform architect','clear authority for diagnostics and execution state','Falcone services do not compete to own policies or histories','P0','M',['LOG-CON-001'],[
 'Logs must own investigation/error state while IAM, secrets, S3, workflow, runtime, audit and metering retain their existing authorities.',
 'Every producer integration must identify its owning repository and the versioned scope, lineage and delivery contracts it consumes.'
],[ 'Use shared Falcone outbox/inbox/fencing contracts; gaps become owning-repository handoffs, not duplicate implementations.', 'Respect serverless ADR 0008 status and OCI pod-versus-invocation attribution; use accepted secrets decisions.', 'Document diagnostics as additive projections: resolving an issue never changes run state, reruns code or executes a query.' ])
story(e,'Qualify reference licenses, components and telemetry capacity','a maintainer','reviewed technology and sizing decisions','the service can be operated and distributed responsibly','P0','L',['LOG-CON-001'],[
 'Dependency intake must pin component versions/licenses and distinguish open-source, source-available and enterprise-only code before reuse.',
 'Capacity decisions must measure telemetry rates, bytes, cardinality, retention and query concurrency independently from application message counts.'
],[ 'Review Sentry FSL and SDK transitive tooling, MIT/community and enterprise boundaries, AGPL references and the repository-license decision.', 'Benchmark TypeScript processing and proposed Go/OTel ingestion; require approved ClickHouse or a tested alternative backend profile.', 'Record infrastructure and data-volume assumptions; no performance or compliance claim is inherited from a reference project.' ])

e=epic('ING','Ingestion and SDK compatibility','Accept bounded, scoped diagnostics with honest acknowledgement and loss semantics.')
story(e,'Implement authenticated OTLP and Falcone batch ingestion','an application developer','standard log/trace ingestion plus Falcone adapters','diagnostics enter one supported service','P1','L',['LOG-TEN-001','LOG-PRV-001','LOG-COR-001'],[
 'Ingestion must validate schema, source authority, size/decompression limits and mandatory redaction before any persistent queue.',
 'Durable acceptance must follow the configured broker acknowledgement while preserving protocol-specific success, partial-success and retry responses.'
],[ 'Implement qualified OTLP HTTP/protobuf and custom batch profiles; optional gRPC requires its own tests.', 'Test mixed valid/invalid batches, oversized attributes, wrong audience, broker failure and lost acknowledgement without persisting raw rejection payloads.', 'Publish per-interface outcomes and limits; do not substitute a generic HTTP 202 for required OTLP semantics.' ])
story(e,'Implement producer SDKs and optional Sentry envelope compatibility','an integration developer','supported instrumentation for Node, Go and Python','applications can export diagnostics predictably','P1','L',['LOG-ING-001','LOG-CON-003'],[
 'SDK adapters must emit versioned trusted Falcone context and bounded logs/errors using pinned supported runtime/library versions.',
 'Any Sentry compatibility endpoint must advertise tested envelope item types and SDK versions and reject unsupported items explicitly.'
],[ 'Test Node/Go/Python log/exception propagation, stable transport-retry IDs and current checksum/compression/protocol behavior.', 'Sentry read/admin APIs, replay, profiling and attachments are not implied by accepting error envelopes; review all transitive licenses.', 'Browser/public keys, if enabled, are scoped write-only untrusted sources and cannot assert verified user/runtime identity.' ])
story(e,'Implement bounded buffering, retries and loss reporting','an SRE','controlled telemetry pressure and visible loss','an observability outage does not exhaust applications','P1','M',['LOG-ING-001','LOG-GOV-001'],[
 'Producer/gateway buffers and retries must be bounded by bytes, time and policy, with explicit accepted/rejected/sampled/dropped reasons.',
 'Application diagnostics must export asynchronously without changing execution results, while existing governed audit blocking semantics remain intact.'
],[ 'Exercise hard kill, queue exhaustion, slow broker and poison batches; sanitize before any persistent exporter WAL.', 'Prioritize critical summaries within caps without promising all errors survive arbitrary overload.', 'Expose retry guidance and drain/shutdown budgets; no unbounded synchronous log flush on function completion.' ])

e=epic('TEN','Identity, tenancy and access','Enforce Falcone scope across ingestion, investigation and sharing.')
story(e,'Integrate IAM and separate diagnostic permissions','a workspace administrator','Falcone-controlled log and error permissions','users see only authorized investigation data','P1','L',['LOG-CON-002'],[
 'All management/query operations must authenticate through Falcone IAM and authorize tenant/workspace/resource/action scope.',
 'Log read, error read, source-artifact read, triage, export, destination configuration and platform investigation must be distinct permissions.'
],[ 'Preserve activation log/result policies and verified workspace claims; role-name or actor-type strings alone do not widen access.', 'Test expired tokens, wrong issuer/audience, scoped grants and platform-global redacted views.', 'Define bounded policy-cache and live-stream recheck behavior; unavailable required authorization fails closed.' ])
story(e,'Implement trusted producer context and project enrollment','a runtime owner','resource-bound ingestion identities','tenant code cannot forge another execution or scope','P1','L',['LOG-TEN-001','LOG-COR-001'],[
 'Producer enrollment must bind a source/project to verified tenant/workspace ownership, resource grants and allowed signals.',
 'Reserved identity fields must be supplied or verified by trusted host/dispatch adapters, with conflicting untrusted attributes rejected or isolated.'
],[ 'Test malicious guest tenant/run/activation IDs, identical trace IDs in different tenants and revoked ingestion credentials.', 'Projects are Falcone configuration under existing workspaces, not a second organization/team directory.', 'Keep public browser ingestion explicitly untrusted and rate-limited; credentials and rotations use falcone-secrets.' ])
story(e,'Enforce isolation across search, artifacts and sharing','a security engineer','consistent scope on every retrieval path','facets or exports cannot bypass tenant isolation','P1','L',['LOG-TEN-002','LOG-STO-001'],[
 'Every detail, search, facet, aggregate, join, cursor, tail, artifact and export must enforce authorized scope before returning data.',
 'Backend roles, query compilation and caches must prevent arbitrary SQL/table-function access and cross-scope data reuse.'
],[ 'Use PostgreSQL RLS and restricted analytical roles/policies; tenants cannot set trusted backend namespace headers.', 'Test saved links, autocomplete, archive rehydrate, reused cursors and scope/policy changes with same-name resources.', 'Source snippets require source permission; correlation IDs remain locators, never bearer authority.' ])

e=epic('PRV','Privacy and collection controls','Prevent sensitive diagnostic content from reaching unauthorized persistence or viewers.')
story(e,'Implement source and gateway redaction before persistence','a privacy engineer','mandatory minimization and redaction','logs do not become a secondary secret store','P1','L',['LOG-CON-001','LOG-TEN-001'],[
 'The pipeline must apply allowlists and redaction before Kafka, persistent queues, DLQs, archives and internal diagnostic logging.',
 'Query-bearing request errors must preserve fix-1118 by omitting raw exception messages, stacks, causes and URL/query material.'
],[ 'Inject synthetic keys into nested logs, headers, signed URLs, causes, breadcrumbs and truncation boundaries; scan every persistent sink.', 'A policy-engine failure rejects/drops protected content with safe metadata, never stores an unfiltered fallback.', 'Generic auto-capture cannot bypass producer restrictions; document residual limits of redacting arbitrary unstructured text.' ])
story(e,'Implement safe collection profiles and sensitive-field controls','a tenant privacy owner','explicit diagnostic collection policies','useful investigation does not require collecting application data','P1','M',['LOG-PRV-001'],[
 'Default policies must exclude request/response bodies, query parameters/results, documents, vectors, secrets and LLM content from telemetry.',
 'Field exceptions, pseudonymous user grouping and source/debug capture must be explicit scoped policies with retention and audit.'
],[ 'Use metadata-only rejection/quarantine by default; disabled content cannot leak through enrichment, exports or alerts.', 'Test policy version changes, nested attribute limits and unparseable SQL/Mongo shapes; hashing raw secrets is not anonymization.', 'Publish per-source available/omitted fields so the UI does not imply a missing stack or payload can be reconstructed.' ])
story(e,'Harden untrusted content, enrichment and export rendering','a security reviewer','bounded safe processing of logs and artifacts','hostile tenant content cannot attack operators','P1','L',['LOG-PRV-002','LOG-TEN-001'],[
 'Log/source/comment rendering and exports must neutralize script, control-character and spreadsheet-formula injection.',
 'Parsers and enrichment jobs must enforce time/memory/archive limits and prohibit execution of uploaded code or arbitrary network fetch.'
],[ 'Test stored XSS, ANSI injection, archive traversal/bombs, regex denial of service and malicious source maps.', 'Disable arbitrary source-map URLs; any future fetch/destination uses scoped egress, TLS, DNS and redirect checks.', 'Keep model-assisted investigation optional and treat log content as untrusted data, not tool instructions.' ])

e=epic('COR','Telemetry schema and execution correlation','Connect diagnostic signals to trusted Falcone execution lineage.')
story(e,'Define canonical events and provenance metadata','an integration architect','one versioned diagnostic envelope','sources can be analyzed without losing their semantics','P0','M',['LOG-CON-002'],[
 'The event contract must define scoped source identity, signal/time fields, execution lineage, content policy and quality metadata.',
 'Adapters must preserve original public contracts while recording normalized schema/version and trusted versus reported fields.'
],[ 'Cover log/error/span/query events, producer epoch/sequence, source/observed times and truncation/sampling/loss flags.', 'Keep audit event schema and existing Falcone correlation IDs distinct from OTel trace identity.', 'Publish fixtures for two tenants, legacy aliases, unknown fields and version evolution; reject ambiguous ownership.' ])
story(e,'Propagate trace context across asynchronous boundaries','a developer','linked logs and spans across services','I can follow one operation through Falcone','P1','L',['LOG-COR-001','LOG-TEN-002'],[
 'Trusted adapters must propagate W3C trace context and Falcone correlation/causation IDs across requests, messages and runtime calls.',
 'Long-running or asynchronous work must use bounded trace segments and explicit links rather than requiring one indefinitely open span.'
],[ 'Test flow-to-function-to-database, Kafka delivery, child runs, retry attempts and missing trace headers.', 'Preserve source sequence and clock uncertainty; do not infer global order or root cause from receipt time.', 'Expose sampled/missing spans and link provenance; reused trace IDs cannot cross tenant authorization.' ])
story(e,'Integrate flow timelines and resumable diagnostic overlays','a flow author','node and attempt diagnostics beside the run graph','I can investigate failed or retried steps','P2','L',['LOG-COR-002','LOG-ING-003','LOG-SEA-002'],[
 'Flow investigation must distinguish run, node occurrence, loop/map iteration and retry attempt and link authoritative status to diagnostic evidence.',
 'Existing flow SSE frame/sequence/resume semantics must remain unchanged when adding diagnostic overlays and new tail cursors.'
],[ 'Test current Temporal history frames and native workflow events, long waits, nested flows and terminal/retry outcomes.', 'Reconstruction/replay cannot emit old logs as new occurrences; late diagnostics cannot rewrite workflow outcome.', 'Issue triage cannot resolve workflow incidents or rerun nodes; cross-repository producer/console changes require owned handoffs.' ])

e=epic('FUN','Function and runtime diagnostics','Capture scoped execution evidence without changing runtime authority or isolation.')
story(e,'Capture trusted activation and attempt logs','a function developer','logs tied to the correct activation and revision','concurrent executions can be investigated separately','P1','L',['LOG-ING-002','LOG-COR-002'],[
 'Function diagnostics must identify trusted action/revision, activation/job/attempt, runtime mode and source stream where available.',
 'WASM host/shim and OCI per-invocation logs must preserve their distinct identity boundaries and resource budgets.'
],[ 'Test concurrent invocations and tenant-supplied forged context; OCI pod stdout remains pod/revision-level unless attribution is proven.', 'Integrate current Knative activation responses plus native host/shim contracts without exposing broad ingestion credentials to guests.', 'Keep logs, results and source read permissions separate and preserve activation retention/error envelopes.' ])
story(e,'Capture runtime failures and execution timing safely','an operator','termination and timing evidence beyond application exceptions','timeouts or host crashes are diagnosable','P1','M',['LOG-FUN-001'],[
 'Runtime failure events must distinguish application errors, timeout/cancel, host termination and unavailable diagnostic evidence.',
 'Timing fields must distinguish scheduling/cold-start, execution, host-call and telemetry delay and mark unmeasured values unknown.'
],[ 'Test OOM/kill, crash before flush, cancelled attempts, missing stacks and successful execution during logs-service outage.', 'Do not infer invocation attribution from pod labels alone when several executions share a runtime.', 'Collection remains namespaced and approved; no privileged node agent or eBPF dependency is introduced.' ])
story(e,'Link function diagnostics to callers, artifacts and releases','a runtime maintainer','verified diagnostic links to invoking flows and deployed code','developers can identify the affected execution context','P2','M',['LOG-FUN-002','LOG-REL-001','LOG-TEN-003'],[
 'Function investigations must link trusted caller lineage and immutable artifact/release identity without exposing unauthorized source or payloads.',
 'Log retrieval and export must honor effective activation/source retention and current permission rules across hot and archived data.'
],[ 'Test flow caller, standalone invocation, stale revision, artifact digest mismatch and missing debug data.', 'Expired activation access cannot be bypassed by trace lookup, archive search or a saved error link.', 'Record serverless/main Falcone instrumentation and UI handoffs separately; logs does not own runtime scheduling.' ])

e=epic('QRY','Database query diagnostics','Analyze datasource errors and performance without capturing business data by default.')
story(e,'Instrument trusted PostgreSQL and MongoDB execution seams','a data-service developer','safe per-operation timing and failure events','I can diagnose datasource behavior from Falcone','P1','L',['LOG-ING-002','LOG-COR-002','LOG-PRV-002'],[
 'Query diagnostics must capture verified logical datasource, execution ID, operation, safe error category and defined timing/row-count semantics.',
 'Instrumentation must preserve existing query authorization, RLS, error responses and execution behavior.'
],[ 'Test workflow/function-origin queries, direct data API operations, cancellation, timeout and opaque driver causes.', 'Separate pool wait, client duration and measured server time; define Mongo cursor lifetime rather than reporting dispatch as full execution.', 'Never include connection strings, bind values, rows/documents or embedding vectors in default events.' ])
story(e,'Implement sanitized query shapes and performance analysis','a workspace developer','aggregates by safe query shape','I can find slow or repeatedly failing operations','P1','L',['LOG-QRY-001','LOG-SEA-001'],[
 'Query normalization must use supported dialect parsers or known adapter plans and omit unsafe/unparseable text instead of retaining raw statements.',
 'Query summaries must provide scoped latency/error statistics with coverage, sampling and denominator quality explicitly reported.'
],[ 'Test literals/comments, identifiers, SQL dialects and Mongo filters without exposing values; version normalized fingerprints.', 'Repeated-call/N+1 and regression results are evidence-backed candidates, not automatic root-cause claims.', 'Do not derive exact failure rates from sampled errors or conflate client/network latency with server execution time.' ])
story(e,'Provide safe query error detail and optional plan artifacts','a database operator','controlled query investigation details','I can investigate failures without granting execution rights to logs','P2','M',['LOG-QRY-002','LOG-TEN-003'],[
 'Query error views must link safe classification, sanitized shape and originating run/activation under datasource-aware authorization.',
 'Query plans must be optional authorized artifacts; the logs service must not automatically execute user SQL or EXPLAIN ANALYZE.'
],[ 'Test plan/source access distinct from log access and redact plan constants or sensitive identifiers.', 'Unknown normalization/plan data is shown as unavailable; no hidden diagnostic re-execution changes production state.', 'Publish supported PostgreSQL/MongoDB categories and plan-profile limits; add other query systems through separate adapters.' ])

e=epic('ERR','Error grouping and issue lifecycle','Turn occurrences into actionable Falcone issues with correct counts and history.')
story(e,'Implement deterministic scoped error grouping','a developer','similar exceptions grouped into issues','I can prioritize recurring problems','P1','L',['LOG-STO-001','LOG-COR-001','LOG-PRV-001'],[
 'Grouping must use versioned deterministic normalized fingerprints inside trusted tenant/workspace/project scope.',
 'Transport duplicate occurrences must not increase issue counts, while distinct failed execution attempts must remain separate occurrences.'
],[ 'Test exception types/stacks/templates with variable IDs and values, expected cancellations and missing stacks.', 'Release IDs do not fragment default grouping; client fingerprint hints cannot merge another scope.', 'Record grouping version and provenance; unrelated flow/function/query errors can be linked without pretending causal identity.' ])
story(e,'Implement assignment, triage and concurrent state transitions','a team maintainer','assignable and auditable error states','developers can coordinate investigation','P1','M',['LOG-ERR-001','LOG-TEN-001'],[
 'Issues must support unresolved, acknowledged, resolved and snoozed states, authorized assignment, priority/tags and transition history.',
 'Issue mutations must use revision checks/idempotency and remain independent from workflow incidents or runtime control actions.'
],[ 'Test concurrent resolve/assign, stale revisions, unauthorized assignees and expired snoozes.', 'Assignments refer to Falcone IAM users/teams rather than a new directory; comments are escaped and scoped.', 'Display exact accepted occurrence counts separately from sampled estimates, affected-user estimates and actual business impact.' ])
story(e,'Implement grouping revisions, merge and split','an error-triage owner','controlled grouping corrections','noisy or incorrectly combined issues can be repaired','P2','L',['LOG-ERR-002','LOG-GOV-003'],[
 'Merge/split and grouping changes must preserve immutable occurrence identity, prior mapping provenance and auditable transitions.',
 'Regrouping/reprocessing must be bounded, resumable and notification-safe without duplicating occurrence counts.'
],[ 'Preview affected scoped events, apply with fencing/revision checks and support an auditable reversal where defined.', 'Test algorithm upgrades, late events, replay windows and duplicate storage rows.', 'Do not execute tenant scripts/unbounded regexes; related-error suggestions retain confidence/provenance and never auto-merge across scope.' ])

e=epic('REL','Releases and source-level diagnosis','Connect errors to immutable deployed code and qualified debug artifacts.')
story(e,'Implement release, deployment and artifact identity','a release engineer','scoped build and deployment records','errors can be investigated against the deployed revision','P1','M',['LOG-CON-002','LOG-TEN-001'],[
 'Release records must bind trusted project/environment to immutable function/flow/build identity and deployment provenance.',
 'Debug artifacts must be uploaded through scoped CI credentials with digests, ownership and explicit retention/access policies.'
],[ 'Treat release strings as opaque IDs; track actual deployment ordering, rollback and concurrent canary deployments.', 'Store artifacts through falcone-s3 native/external bindings with secrets-managed credentials and verified manifests.', 'Wrong digest/debug ID or unauthorized upload cannot replace another release artifact.' ])
story(e,'Implement safe source-map and stack enrichment','a developer','readable source locations for approved runtimes','I can diagnose exceptions in deployed code','P2','L',['LOG-REL-001','LOG-PRV-003','LOG-ERR-001'],[
 'Symbolication must use verified matching artifacts and supported language/debug profiles with bounded isolated parsing.',
 'Original sanitized frames and enriched projections must remain versioned, scoped and subject to source-access/redaction rules.'
],[ 'Start with JS/TS source maps and already-symbolic Node/Python/Go frames; WASM/native formats require separate qualification.', 'Test missing/late maps, malicious archives, embedded source secrets and mismatched builds without executing code or fetching arbitrary URLs.', 'Enrichment cannot duplicate events, silently change counts or expose source snippets to log-only viewers.' ])
story(e,'Detect regressions using deployment-aware evidence','a release owner','reliable new/regressed-error indicators','late data does not create false release alarms','P2','L',['LOG-REL-002','LOG-ERR-002'],[
 'Regression detection must evaluate validated release/deployment lineage and explicit resolution boundaries rather than lexical version ordering.',
 'Unknown or late old-release events must be distinguished from qualified new regressions and must not spuriously reopen resolved issues.'
],[ 'Test resolve-in-release, rollback, redeploy, parallel canaries and delayed event ingestion.', 'Compare only compatible collection/sampling windows and show observed counts/coverage.', 'Commit regression transition and alert intent once; release correlation is not proof that a commit caused the bug.' ])

e=epic('SEA','Search, live tail and exports','Provide useful investigation queries within enforced scope and cost limits.')
story(e,'Implement scoped log, error and trace search','a developer','field/text/time search and safe aggregates','I can find relevant diagnostic evidence quickly','P1','L',['LOG-STO-001','LOG-TEN-002','LOG-GOV-001'],[
 'The query API must compile an allowlisted AST with mandatory scope/time bounds, pagination and bounded aggregation/full-text capabilities.',
 'Search responses must expose projection freshness, coverage, sampling, truncation and partial/timeout status.'
],[ 'Test severity/service/release/run/activation/query filters, facets and logs-to-trace joins under two tenants.', 'No raw backend SQL or external table functions; enforce deadline/scanned-byte limits and server-side cancellation.', 'Use opaque scoped cursors and defined concurrent-ingest ordering; missing data is not returned as healthy or zero errors.' ])
story(e,'Implement resumable authorized live tail','an operator','live logs with clear reconnect behavior','I can investigate running work without losing track of gaps','P1','M',['LOG-SEA-001','LOG-TEN-001'],[
 'Live tail must use a typed scoped cursor, bounded subscriber buffers, permission rechecks and an explicit resume horizon.',
 'Tail gaps, overflow, retention expiry and disconnects must be visible rather than silently dropping records.'
],[ 'Test reconnect, slow clients, tenant changes, token expiry and concurrent source streams; no globally ordered log promise.', 'Preserve current workflow SSE endpoint/cursor independently; add new tail transport through Falcone conventions.', 'Support SSE first where appropriate and a qualified WebSocket adapter if required, with equivalent auth/backpressure semantics.' ])
story(e,'Implement redacted exports and bounded archive investigations','a support engineer','controlled exports and older evidence retrieval','investigations remain reproducible without bypassing policy','P2','L',['LOG-SEA-001','LOG-STO-002','LOG-TEN-003','LOG-PRV-003'],[
 'Exports and archive queries must reauthorize scope and apply current masking, retention and resource budgets before producing results.',
 'Large exports/rehydration must be asynchronous jobs with progress, expiry, checksums and auditable download access.'
],[ 'Test hot/cold overlap dedupe, cancelled jobs, expired data, cross-tenant manifests and partial archives.', 'Protect CSV/JSON downloads from injection and secret leakage; choose proxied retrieval when immediate revocation is required.', 'Saved export links do not preserve access after policy revocation; all objects have explicit lifecycle and cleanup.' ])

e=epic('STO','Storage, idempotency and retention','Store diagnostic evidence with truthful consistency and deletion guarantees.')
story(e,'Implement analytical projections and exact issue-state persistence','a platform engineer','separate transactional state and scalable telemetry storage','search load does not corrupt issue lifecycle','P1','L',['LOG-CON-003','LOG-COR-001','LOG-TEN-001'],[
 'PostgreSQL must own scoped product/issue state and deduplicated error transitions while the approved analytical backend owns query projections.',
 'Projection writes and queries must handle transport/batch retries without relying on eventual background merges for immediate exact counts.'
],[ 'Test broker replay, changed insert batch boundaries, lost acknowledgements and index failure around PostgreSQL commit.', 'Qualify ClickHouse dedupe/FINAL or equivalent semantics; naive materialized sums of duplicate raw rows cannot drive exact alerts.', 'Expose independent consumer watermarks; no cross-Kafka/PostgreSQL/ClickHouse transaction or unlimited dedupe window is claimed.' ])
story(e,'Implement verified S3 archives and debug/export storage','a storage operator','scoped immutable diagnostic archives','hot retention can be bounded while selected evidence remains available','P2','L',['LOG-STO-001','LOG-PRV-002'],[
 'Archive batches must use versioned sanitized schemas, scope/time metadata and checksummed manifests published only after verified object completion.',
 'Archive/debug/export storage must work through qualified falcone-s3 native or external bindings with appropriate retention and credentials.'
],[ 'Test interrupted uploads, orphan cleanup, missing/wrong object versions, failed manifest commit and restore.', 'Rehydrate only authorized bounded ranges, with temporary index expiry and visible coverage/cost.', 'Do not assume every S3 provider supports identical retention or instant signed-link revocation.' ])
story(e,'Implement retention, tombstones and privacy purge','a privacy administrator','effective deletion across all diagnostic copies','expired or deleted data cannot reappear through archives or replay','P2','L',['LOG-STO-002','LOG-TEN-003'],[
 'Effective retention must honor source/activation restrictions and scoped privacy policy across hot data, archives, artifacts, caches and exports.',
 'Deletion must create authoritative query-enforced tombstones and track asynchronous physical cleanup including replay/restore handling.'
],[ 'Test source expiry, tenant purge, late Kafka delivery, archive rehydrate and restore before serving reads.', 'Separate logical inaccessibility from physical deletion in ClickHouse, mixed Kafka segments, shared archives and backups.', 'Audit legal holds and conflicts; derived fingerprints/comments/source snippets are part of the deletion inventory.' ])

e=epic('ALT','Alerts and controlled integrations','Notify on actionable diagnostic conditions without duplicate storms or hidden side effects.')
story(e,'Implement scoped alert rules and state transitions','an application owner','alerts on new errors, regressions and sustained failures','problems are visible before users report them','P2','L',['LOG-ERR-002','LOG-REL-003','LOG-SEA-001'],[
 'Alert rules must define scoped conditions, windows, lateness/watermarks, thresholds, cooldown/hysteresis and no-data behavior.',
 'Alert evaluation must distinguish deduplicated exact counts from sampled or incomplete rates and commit each transition once.'
],[ 'Support new/regressed issue, error/latency threshold, slow query and ingestion-lag conditions with previews.', 'Test late events, missing denominators, changed sampling, snooze/mute schedules and recovery transitions.', 'Alert state/outbox commit atomically in its store; core evaluation does not depend on workflow/serverless health.' ])
story(e,'Implement approved notification delivery and incident history','an on-call operator','reliable scoped notifications','alerts can be routed without leaking customer data','P2','L',['LOG-ALT-001','LOG-PRV-003'],[
 'Notification delivery must use approved destinations, redacted payloads, secrets references, retry budgets, deduplication identity and DLQ state.',
 'Users must be able to inspect/test authorized delivery status and retry safe failures without claiming exactly-once external effects.'
],[ 'Test webhook signing/rotation, timeout after remote success, provider rate limits, disabled endpoints and SSRF/redirect changes.', 'Console/email/webhook adapters are capabilities; no live destination is enabled by repository bootstrap.', 'Maintain incident/notification history separately from error triage and workflow-owned incidents.' ])
story(e,'Implement explicit GitHub and workflow integration commands','a team lead','controlled links to engineering and response workflows','investigation can lead to authorized follow-up work','P2','M',['LOG-ALT-002','LOG-TEN-003'],[
 'External ticket creation or workflow response must require explicit configured authority and permitted scoped diagnostic content.',
 'Integration actions must be auditable, idempotent where supported and loop-safe, with dry-run/preview behavior.'
],[ 'Default to links and previews; log-read permission alone cannot send data to GitHub, a webhook or a model.', 'Test ticket dedupe, bidirectional status conflicts, revoked credentials and alert-triggered workflow recursion.', 'Resolving an error never automatically reruns a function or executes a database query; such commands use owning-service authorization.' ])

e=epic('UI','Falcone console and developer API','Provide one coherent investigation experience inside Falcone.')
story(e,'Build integrated log, issue and execution investigation views','a Falcone developer','connected investigation pages','I can move from a failure to its context without switching products','P2','L',['LOG-SEA-002','LOG-ERR-002','LOG-COR-003','LOG-FUN-003','LOG-QRY-002'],[
 'The console must provide scoped Logs, Errors and Trace/Execution views with entry points from flows, activations and datasources.',
 'Every view must show permissions, freshness, missing evidence and sampling states with safe accessible rendering.'
],[ 'Test one flow-function-query failure journey plus empty, denied, stale, partial and expired-evidence states.', 'Keep current navigation and IAM context; issue assignment/status is visibly distinct from run status and action controls.', 'Implement console changes in the owning Falcone repository with contracts and links tracked from this story.' ])
story(e,'Implement saved views, dashboards and scoped sharing','a workspace team member','reusable investigation views','the team can compare incidents and releases consistently','P2','M',['LOG-UI-001','LOG-TEN-003'],[
 'Saved filters/dashboards must preserve query version, scope, time semantics and permissions without storing credentials or hidden raw payloads.',
 'Shared views must authorize the current viewer and display explicit coverage/freshness for all widgets.'
],[ 'Support release/error/latency/log-volume panels using compatible denominators and bounded queries.', 'Test revoked members, copied URLs, timezone changes, deleted resources and renamed fields.', 'No workspace share becomes a public link or widens to tenant/platform scope automatically.' ])
story(e,'Publish versioned APIs, CLI workflows and synthetic examples','an integration developer','documented machine interfaces','I can automate safe diagnostic workflows','P1','M',['LOG-CON-001','LOG-COR-001','LOG-TEN-001'],[
 'The service must publish versioned ingestion/query/issue/release/alert schemas and scoped SDK/CLI examples.',
 'Examples must distinguish new proposed routes, existing Falcone contracts, protocol compatibility and quality/error states.'
],[ 'Provide synthetic Node/Go/Python scenarios with two tenants, a retrying flow, a function exception and sanitized query failure.', 'Document safe credential handling, pagination, retry/partial success and cancellation; no production tokens or raw data in fixtures.', 'API compatibility tests protect existing audit/SSE/activation behavior while new schemas evolve additively.' ])

e=epic('GOV','Quotas, sampling and resource governance','Keep diagnostic cost and fairness under Falcone policy.')
story(e,'Implement Falcone ingestion and query resource budgets','a platform administrator','central limits for diagnostic resources','one noisy tenant cannot exhaust the service','P1','L',['LOG-CON-002','LOG-TEN-001'],[
 'Ingest bytes/events, retention, scan budget, tail connections, exports and notification limits must come from Falcone entitlements/policy.',
 'The service must enforce bounded per-tenant/source fairness and physical safety limits with explicit policy-unavailable behavior.'
],[ 'No independent billing-plan definitions; record current quota failure semantics and any new policy decision explicitly.', 'Test bursty tenants, high-cardinality attributes, slow queries/subscribers and competing archive/symbolication work.', 'Security/privacy denials never fail open; physical queue/memory safety remains enforced regardless of business quota mode.' ])
story(e,'Implement sampling, usage facts and coverage reporting','a product operator','visible cost and loss decisions','sampled diagnostics do not misrepresent platform usage','P1','L',['LOG-GOV-001','LOG-COR-001'],[
 'Sampling and filtering decisions must expose policy/version, known probability and accepted/rejected/dropped coverage metadata.',
 'Usage facts must distinguish transport retries, accepted logical events, stored bytes and scan/transfer resources under Falcone accounting rules.'
],[ 'Keep sampled telemetry separate from authoritative billing/audit and execution-success denominators.', 'Test error-priority overload, head/tail sampling constraints and changes between comparison windows.', 'Do not extrapolate exact users/error rates from unknown sampling; duplicates cannot become fresh billable logical events by accident.' ])
story(e,'Implement bounded replay, reprocessing and schema evolution','a maintainer','safe replay and enrichment upgrades','historical data can be repaired without resurrecting deleted events','P2','L',['LOG-STO-001','LOG-GOV-002'],[
 'Replay/reprocessing must use scoped jobs, checkpoints, versioned schemas and a documented dedupe horizon covering supported retry/replay windows.',
 'Historical reimports must honor deletion/source-retention rules and suppress new notifications unless explicitly authorized.'
],[ 'Test changed batches, DLQ replay, algorithm upgrades, expired dedupe windows and import namespaces.', 'Track independent projection watermarks and partial completion; processing failures do not silently discard admitted events.', 'Keep original sanitized identity immutable while derived projections evolve; no blind reset of alert/dedupe state during recovery.' ])

e=epic('OPS','Restricted deployment and reliability','Operate the service without expanding Falcone runtime privileges.')
story(e,'Package namespaced collection and approved backend profiles','a platform operator','deployment compatible with restricted OpenShift','observability does not require unavailable cluster permissions','P1','L',['LOG-CON-003','LOG-ING-001'],[
 'Baseline workloads must run non-root/arbitrary UID with namespace-scoped RBAC and no privileged DaemonSet, hostPath, new operator, CRD or eBPF prerequisite.',
 'Backend endpoints, storage budgets and operator ownership must be explicit prerequisites with qualified version/profile evidence.'
],[ 'Test standard Kubernetes and actual corporate OpenShift builds, writable volume permissions, egress/TLS and pinned images.', 'Reuse approved infrastructure and namespaced SDK/gateway export; no compatible ClickHouse/Loki/OpenSearch deployment is assumed.', 'Development/small profiles expose their limits and cannot advertise production throughput or durability.' ])
story(e,'Implement SLOs, independent health and incident runbooks','an SRE','measurable ingestion/search/alert health','the logs service can diagnose its own degradation','P2','M',['LOG-OPS-001','LOG-GOV-002','LOG-ALT-002'],[
 'Operational telemetry must expose acceptance/loss, backlog, projection freshness, query cost, deletion lag and delivery health without sensitive high-cardinality labels.',
 'The release must publish benchmarked objectives, dependency-failure behavior and named on-call/patch responsibilities.'
],[ 'Measure proposed availability, acceptance/freshness/search/overhead targets against stated datasets and concurrency.', 'Exercise broker/index/IAM/secrets/S3 outages and logging storms; minimal independent health metrics remain available.', 'Provide runbooks for poison events, raw-data exposure, stuck purges, duplicate alerts and incomplete restores.' ])
story(e,'Implement coordinated backup and diagnostic recovery','a recovery operator','restorable product state and evidence','incidents can be investigated after infrastructure failure','P2','L',['LOG-OPS-001','LOG-STO-003','LOG-GOV-003'],[
 'Backups must include issue/alert/dedupe state, policy/deletion records and required archive/debug manifests and key dependencies.',
 'Restore/rebuild must preserve authorization and deletion before serving reads and report recoverable coverage and measured RPO/RTO.'
],[ 'Test cold start with independent secrets bootstrap, PostgreSQL recovery and ClickHouse rebuild from available Kafka/archive windows.', 'Do not resend historical alerts or resurrect expired telemetry after offset reset/backup restore.', 'Measure dataset-dependent analytical recovery separately from the proposed metadata service target; missing source data remains a reported gap.' ])

e=epic('DEV','Implementation quality and controlled rollout','Qualify the new service before collecting production diagnostic data.')
story(e,'Implement reproducible builds and maintenance gates','a maintainer','attributable secure releases','components can be updated without silent protocol or policy drift','P1','M',['LOG-CON-003','LOG-UI-003'],[
 'Builds must pin dependencies/images, publish SBOM/provenance and verify selected component/transitive licenses.',
 'The project must define vulnerability response, supported SDK/backend versions and compatible schema upgrade/rollback gates.'
],[ 'Scan for credentials, vulnerable dependencies and unsafe permissions with owned time-limited exceptions.', 'Do not copy FSL/enterprise code under an assumed open-source license; choose the repository license before implementation distribution.', 'Keep requirement/backlog/issue IDs reproducible and validate dependency/parent links without claiming a generated plan is tested runtime code.' ])
story(e,'Qualify privacy, isolation, protocol and failure behavior','an independent reviewer','adversarial and recovery evidence','the investigation service does not expose tenant data or misreport incidents','P3','L',['LOG-DEV-001','LOG-TEN-003','LOG-PRV-003','LOG-OPS-003','LOG-REL-003','LOG-QRY-003'],[
 'Production candidates must pass cross-tenant, synthetic-secret, protocol, grouping/dedupe, retention and outage tests for every enabled profile.',
 'Independent review must cover privacy-before-persistence, source/artifact access, analytical query isolation and recovery/notification semantics.'
],[ 'Test all sinks including exporter WAL/DLQ, caches, facets, archives and backup restore with synthetic data.', 'Inject crashes around broker/PG/index/outbox boundaries, changed batches, stale workers and late release events.', 'Record residual source-loss/privacy limits and owned exceptions; no upstream certification or perfect redaction claim.' ])
story(e,'Run cross-service canaries and controlled production rollout','a Falcone product owner','verified incremental adoption','the new service improves investigation without disrupting workloads','P3','L',['LOG-DEV-002','LOG-UI-002','LOG-COR-003','LOG-FUN-003','LOG-QRY-003','LOG-ALT-003','LOG-SEA-003','LOG-OPS-002'],[
 'Rollout must progress from synthetic fixtures through shadow ingestion and scoped canaries with measurable privacy/performance/integration gates.',
 'Rollback must preserve admitted issue/audit/deletion state and prevent notification replay while disabling new producers/routes safely.'
],[ 'Demonstrate flow-function-query investigations for two tenants including retries, crash gaps, source maps and archive recovery.', 'Keep current audit, metrics and execution history authoritative; no Sentry migration or runtime replacement is assumed.', 'Track reviewed changes in main Falcone, sibling services and charts before enabling production collection or outgoing actions.' ])

def generate():
    mp=ROOT/'docs/github-issues.json'
    mapping=json.loads(mp.read_text()) if mp.exists() else {}
    by_id={s['id']:s for e in EPICS for s in e['stories']}
    assert len(by_id)==sum(len(e['stories']) for e in EPICS)
    assert len({e['id'] for e in EPICS})==len(EPICS)
    seen=set()
    def visit(sid,stack):
        assert sid not in stack,f'Dependency cycle: {stack} -> {sid}'
        if sid in seen:return
        for dep in by_id[sid]['dependencies']:
            assert dep in by_id,f'Unknown dependency {dep}'
            visit(dep,stack+[sid])
        seen.add(sid)
    for sid in by_id:visit(sid,[])
    def link(sid):
        n=mapping.get(sid,{}).get('number')
        return f'[{sid}](https://github.com/{REPO}/issues/{n})' if n else sid
    req=['# Functional requirements\n',f'Baseline: {DATE}. These are target requirements, not implemented features. Every requirement traces to one user story. Read with [architecture](architecture.md), [telemetry](telemetry-contract.md), [privacy](security-and-privacy.md) and [integration ownership](integration-matrix.md).\n']
    backlog=['# Epics and user stories\n','Generated with `python3 tools/build_docs.py`. S/M/L are relative small/medium/large complexity estimates, not dates. P0 = discovery/decisions; P1 = core; P2 = integrations/hardening; P3 = qualification/rollout. Phase is earliest start subject to dependencies.\n','The logs repository owns these product stories. Producer, console and shared-module changes must be decomposed into their owning repositories before implementation; see integration-matrix.md. Epic task lists and parent links express hierarchy; no GitHub Project board or native sub-issue relationships are implied.\n']
    issues=[];rows=[];req_ids=set()
    for e in EPICS:
        req += [f"## {e['title']}\n",'| ID | Requirement | Story |','|---|---|---|']
        backlog += [f"- **{link(e['id'])}: {e['title']}** — {e['outcome']}\n"]
        body=f"<!-- falcone-logs:{e['id']} -->\n\n## Outcome\n\n{e['outcome']}\n\n## Scope\n\nCustom Falcone log/error investigation for flows, functions and queries. Preserve Falcone scope, privacy and execution authority. See [architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) and [integration ownership](https://github.com/{REPO}/blob/main/docs/integration-matrix.md).\n\n## Stories\n\n"
        body+=''.join(f"- [ ] {link(s['id'])}: {s['title']}\n" for s in e['stories'])
        body+='\n## Exit criteria\n\nAll child acceptance criteria have linked evidence and applicable privacy, scope, compatibility and recovery review. Planning publication does not mean implementation is complete.\n'
        issues.append(dict(id=e['id'],title=f"[Epic][{e['id']}] {e['title']}",body=body,labels=['type:epic',f"area:{e['category']}"]))
        rows.append(dict(ID=e['id'],Type='Epic',Title=e['title'],Parent='',Phase='',Effort='',Dependencies='',URL=mapping.get(e['id'],{}).get('url','')))
        for s in e['stories']:
            assert len(s['requirements'])==2 and len(s['acceptance'])>=3
            body=f"<!-- falcone-logs:{s['id']} -->\n\nParent: {link(e['id'])}\n\n## User story\n\n{s['story']}\n\n## Description\n\n{s['description']}\n\nPhase: {s['phase']} · Effort: {s['effort']}\n\n## Requirements\n\n"
            for r in s['requirements']:
                assert r['id'] not in req_ids
                req_ids.add(r['id']);req.append(f"| {r['id']} | {r['statement']} | {link(s['id'])} |")
                body+=f"- **{r['id']}**: {r['statement']}\n"
            body+='\n## Acceptance criteria\n\n'+''.join(f'- [ ] {a}\n' for a in s['acceptance'])
            body+='\n## Dependencies\n\n'+(', '.join(link(d) for d in s['dependencies']) or 'None; discovery can begin independently.')+'\n'
            body+=f'\n## Design and ownership\n\n[Architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) · [Telemetry](https://github.com/{REPO}/blob/main/docs/telemetry-contract.md) · [Privacy](https://github.com/{REPO}/blob/main/docs/security-and-privacy.md) · [Repository handoffs](https://github.com/{REPO}/blob/main/docs/integration-matrix.md).\n'
            issues.append(dict(id=s['id'],title=f"[{s['id']}] {s['title']}",body=body,labels=['type:story',f"area:{e['category']}",f"phase:{s['phase'].lower()}",f"effort:{s['effort'].lower()}"]))
            backlog += [f"  - **{link(s['id'])}: {s['title']}** ({s['phase']}, {s['effort']})",f"    - {s['story']}",f"    - Description: {s['description']}",f"    - Requirements: {', '.join(r['id'] for r in s['requirements'])}",f"    - Dependencies: {', '.join(link(d) for d in s['dependencies']) or 'None'}"]
            backlog += [f"    - Acceptance: {a}" for a in s['acceptance']]+['']
            rows.append(dict(ID=s['id'],Type='Story',Title=s['title'],Parent=e['id'],Phase=s['phase'],Effort=s['effort'],Dependencies=';'.join(s['dependencies']),URL=mapping.get(s['id'],{}).get('url','')))
        req.append('')
    assert len(EPICS)==16 and len(by_id)==48 and len(req_ids)==96 and len(issues)==64
    assert set(mapping)<=set(x['id'] for x in issues)
    (ROOT/'docs/requirements.md').write_text('\n'.join(req)+'\n')
    (ROOT/'docs/backlog.md').write_text('\n'.join(backlog)+'\n')
    (ROOT/'docs/backlog.json').write_text(json.dumps(dict(schema_version=1,date=DATE,baseline=BASELINE,epics=EPICS),indent=2)+'\n')
    (ROOT/'docs/issue-payloads.json').write_text(json.dumps(issues,indent=2)+'\n')
    out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (ROOT/'docs/backlog.csv').write_text(out.getvalue())
    print(json.dumps(dict(epics=len(EPICS),stories=len(by_id),requirements=len(req_ids),issues=len(issues),mapped=len(mapping))))

if __name__=='__main__':generate()
