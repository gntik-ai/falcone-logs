# Open questions and working proposals

These evidence gaps do not block the architecture/backlog. Defaults below are recommendations, not accepted changes to sibling decisions.

| Question | Working proposal | Gate |
|---|---|---|
| Does “queries” include anything beyond PostgreSQL/MongoDB data operations? | Instrument those adapters first; log-search queries are separate, LLM content/replay excluded by default | P0 scope |
| Which sources already emit OTel, structured logs or Sentry events in deployed Falcone? | Inventory actual collectors/versions and producer ownership; no current Sentry deployment assumed | P0 compatibility |
| What daily volume, burst rate, event size, retention and search concurrency are expected? | Measure separately from the earlier function/message estimates; use operations.md arithmetic and benchmark targets | Capacity |
| Is an operator-managed ClickHouse available/approved? | Preferred high-volume projection; compare existing Loki/OpenSearch if provision is unavailable | Backend placement |
| Should service code align entirely with TypeScript? | TypeScript APIs/domain workers, maintained OTel/Go ingestion components only where justified | Component ADR |
| Which function languages/runtime modes need symbolication first? | JS/TS source maps and already-symbolic Node/Python/Go frames; qualify WASM/native debug formats separately | Debug artifacts |
| Is Sentry SDK/envelope compatibility required for customer applications? | Optional tested item/SDK subset; OTel and trusted Falcone adapters are primary | Compatibility scope |
| What retention/privacy/residency requirements apply by source and tenant? | Configurable 7-day hot/30-day total diagnostics starting point; source restrictions win; longer issue metadata explicitly governed | Privacy/retention |
| Are any raw bodies, SQL values, documents or LLM prompts needed? | No default collection; any exception requires a separate scoped policy and evidence | Security |
| Which alert destinations and operators are required? | Falcone console plus approved webhooks/email adapters; no live destinations enabled by this plan | Alert rollout |
| How should error severity, expected cancellation and regression rules behave? | Versioned project policy, safe defaults and previews; late old-release events do not reopen automatically | Product triage |
| Which users can read logs, errors and proprietary source separately? | Consume IAM permissions plus current activation policy; workspace access is not universal source/export access | Authorization |
| What loss, availability and recovery budgets are acceptable? | Explicit bounded async diagnostics, proposed targets in operations.md; governed audit behavior remains unchanged | SLO/readiness |
| What exact OpenShift/Kubernetes builds and network/volume permissions are allowed? | Namespaced SDK/gateway export; no new operator/privileged collector; qualify exact builds | Deployment |
| Which open-source license should this repository use? | Choose explicitly before code distribution; inspect component and transitive tooling licenses | Supply chain |
| Who owns backend operations, privacy review and 24/7 response if required? | Logs maintainers, SRE/platform, security/privacy and Falcone integration owners; actual names/rotations to assign | Production readiness |

Accepted falcone-secrets proposals remain accepted. Workflow-owned state and shared primitives remain unchanged. Serverless backend-placement recommendations remain at their recorded status; this plan does not silently approve a new cluster backend installation.
