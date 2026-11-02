# Security and privacy

## Trusted scope and authorization

Use Falcone IAM for users, machine identities and authorization; preserve SAML/OIDC/LDAP/AD/SCIM in IAM. A Falcone project is a logging configuration under a verified tenant/workspace/application, not a new account hierarchy. Separate permissions for ingest, read logs, read errors, view source/debug artifacts, manage triage, create alerts/destinations, export, change retention and perform platform investigations.

Scope comes from authenticated producer enrollment and trusted host/dispatch context. Untrusted functions and browser SDKs cannot choose platform scope, another tenant or a verified activation/run ID. A public browser DSN is an abuse-controlled write key, not proof of user identity or a read secret. Backend keys/grants should be short-lived and resource-bound; credentials and webhook signing material belong in falcone-secrets.

Every query, detail lookup, facet/autocomplete, count, trace join, saved view, cursor, export and stream revalidates scope. A trace/correlation/event ID is only a locator. Apply RLS to PostgreSQL; protect analytical stores behind the query service with restricted backend roles/policies and an AST compiler that inserts immutable predicates on all branches/joins. Do not provide arbitrary ClickHouse SQL, table functions, filesystem/network access or raw Loki tenant headers to tenants. Cache keys include authorized scope and relevant policy revision.

## Collection minimization and redaction

Default exclusion: passwords, API keys, bearer/cookie headers, signed URL queries, connection strings, secret values, request/response bodies, query bind values, database rows/documents, vectors and LLM content. Allowlisted operational metadata is safer than collecting whole objects then applying regexes. Sensitive data can occur in exception messages, causes, stacks, breadcrumbs, URLs, object keys and source snippets.

Preserve Falcone fix-1118: query-bearing request errors emit normalized pathname and bounded safe diagnostic fields only; they must not pass raw exception/message/stack/cause or nested driver material to a log/exporter. Generic exception auto-capture must not bypass this source rule. Other sources may publish stacks only under their own reviewed sanitization contract. The backend cannot reconstruct data intentionally omitted by the producer.

Redact at source where possible and enforce the mandatory policy at the gateway **before Kafka, persistent exporter queues, DLQs, debug diagnostics or archive**. Invalid/unattributable events yield safe metadata-only rejection evidence. On policy-engine failure, reject/drop protected content with a loss reason; never persist an unsanitized fallback. Test nested/encoded/multiline secrets and truncation boundaries. Redaction is a tested best-effort control over allowed fields, not a promise to recognize every arbitrary secret in unrestricted text.

Query normalization uses known adapter plans or supported dialect parsers; unparseable text is omitted. If pseudonymous affected-user grouping is enabled, use scoped keyed derivation and explicit retention; do not treat hashes of emails/raw query text as anonymous by default. Per-request body capture and crash dumps remain off until separately justified.

## Untrusted content and integrations

Render logs/comments/source as escaped text. Strip/neutralize ANSI and control characters; prevent stored XSS, CSV formula injection, archive path traversal, parser bombs and regex denial of service. Symbolication workers parse but never execute uploaded source or plugins. Bound bytes, decompression ratio, time and memory; no privileged runtime is required.

Notification and artifact endpoints are operator-approved with credential references, TLS checks, destination/DNS/redirect policy and private-network exceptions for approved corporate services. Prevent SSRF and credential forwarding to changed hosts. Alert previews/test delivery need explicit permission, and all delivered payloads are redacted. A logs read permission does not automatically authorize sending that data to a webhook, GitHub issue or model provider.

Optional AI analysis uses Falcone's approved model route and data policy, scoped retrieved evidence and a separately enabled entitlement. Treat log text as untrusted content, never as instructions to the agent or tool. Outputs identify evidence and uncertainty; no arbitrary SQL, command execution, workflow rerun or automated code deployment is granted by model output.

## Audit and review

Audit sensitive configuration, export, source-artifact access, triage mutation, cross-scope operator access, retention changes and integration actions through Falcone's governed audit mechanism. Do not replace that stream with sampled logs or recursively send every audit failure back into the same failing pipeline.

Review access to platform-global errors carefully: redact shared dependency details for tenant views, and do not grant cross-tenant visibility because an actor has a role-name string such as `superadmin`. Verify trusted platform-observability authority. Qualify isolated accounts, forged attributes, stream revocation, policy cache expiry, data deletion/replay and source/artifact leakage before release.
