# Error tracking, releases and debug artifacts

## Event and issue model

An **error occurrence** is an observed, scoped event from a specific execution/attempt. An **issue** groups similar occurrences for developer triage. A **workflow incident** remains a workflow-owned operational condition. An alert notification and a GitHub planning/product issue are separate records; none is implicitly the other.

Classify failures as application exception, runtime/host failure, dependency/connector error, database failure, timeout, cancellation, policy rejection or platform fault. Expected cancellation/validation/policy events need configurable handling rather than an automatic high-priority bug for every non-success response.

Default grouping key: trusted tenant/workspace/project, error category, language/runtime family, normalized exception type and stable in-application stack frames or safe message template, plus grouping-algorithm version. Resource topology can refine grouping through explicit rules. Do not include timestamps, random IDs or release ID in the default fingerprint; they would fragment recurrence. Environment is a filter/occurrence dimension unless a reviewed project rule splits groups by environment.

Remove volatile values and sensitive material before fingerprinting. Prefer maintained parsers and bounded algorithms; no execution of tenant-provided grouping scripts or unbounded regexes. A client-provided fingerprint is a scoped hint, not permission to merge another project's issue. Similarity between related flow/function/query failures is a suggested link, not an automatic cross-scope merge or causal proof.

## Triage and counts

Support new/unresolved, acknowledged, resolved and snoozed states, assignment to authorized Falcone users/teams, priority, tags, comments and first/last-seen history. Preserve a transition log with actor and optimistic revision checks. Merge/split operations are reversible mappings with provenance, not destructive rewriting of original events; reprocessing uses a versioned grouping job and safe notification policy.

A PostgreSQL unique occurrence key/inbox transaction updates issue counters and alert intent once per accepted error occurrence. Transport duplicates do not increase counters; distinct failed retry attempts do. Accepted error occurrence counts are not the number of affected real-world users or all failures in the platform. Any approximate cardinality, sampled rate or incomplete collection has an explicit label.

## Releases and regressions

Release/build identity maps to immutable function revision, flow definition/version and deployed application artifact. Record deployment environment, time/sequence and commit/artifact provenance. Treat release strings as identifiers, not lexicographically ordered versions. A commit that merely precedes an error is correlation, not proof it introduced the bug.

Support resolution at a deployment/release boundary and regression detection using validated event/deployment lineage. Late old-release observations must not spuriously reopen a resolved new-release issue. Unknown lineage remains unknown; report the new occurrence without inventing a regression. Rollback/redeploy, parallel releases and canaries require explicit environment/deployment rules and tests. Counts before/after release must show collection/sampling changes.

## Source maps and symbolication

CI uploads scoped, immutable debug artifacts with build/debug ID, content digest, allowed language/profile and ownership. Artifacts live behind falcone-s3 and protected metadata in PostgreSQL. Start with JavaScript/TypeScript source maps and already-symbolic Node/Python/Go frames; native/WASM symbols need profile-specific toolchain evidence before enabling support. Do not claim JavaScript source maps cover every runtime.

Prefer uploaded artifacts over arbitrary runtime URL fetching. Disable external source-map fetch by default. If later enabled, require approved destinations, TLS, size/time limits and SSRF protection. Parse artifacts in an isolated bounded worker; prevent path traversal, archive bombs and embedded HTML/script rendering. Never execute uploaded source code. Source access permission is distinct from log/issue read.

Store original **sanitized** frames and versioned symbolicated projections. Artifact absence/mismatch yields a clear unresolved state; a later correct upload can enrich events without changing their immutable identity or duplicating counts. Redaction rules apply to enriched source snippets too. Source maps can embed proprietary source and secrets, so they are not public merely because a client emitted a stack frame.

## Optional enhancements

Profiling/flamegraphs, browser RUM, session replay, user feedback and advanced native crash dumps are separate capabilities with privacy, storage and runtime gates. Error tracking, safe stacks and correlation deliver the first product without requiring them. Optional AI summaries must cite scoped evidence, distinguish hypotheses and obey the separate model/data policy; no automatic patch, query execution or workflow rerun follows a summary.
