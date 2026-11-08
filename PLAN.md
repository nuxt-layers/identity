# Plan

> **In short:** complete Identity's standalone public contract and acceptance evidence; preserve its existing security boundaries while independently migrated IAM capabilities establish compatible public interfaces. Scheduler and message transport remain executor/provider-neutral.

## Completed baseline

| Status | Work |
|---|---|
| Complete | Move active package, module, documentation and dependency references to the version-agnostic `nuxt-layers` organisation (PR #36) |
| Complete | Regenerate and merge the pnpm 12 lockfile against the current Theme Manager development dependency (PR #38) |
| Complete | Introduce backward-compatible, fail-closed `composeIdentity` (PR #39) |
| Complete in source | Add `examples/minimal-host`, composition-budget check, CI build/smoke configuration and capability-owned `getIdentityTasks()` descriptors (PR #40); successful execution on current `master` remains to be verified |
| Partially complete | PR #41 made the public consumer contract provider-neutral and corrected its section order; full operation-level signature and return/error completeness remains to be audited |

## Next work — in dependency order

| Priority | Status | Work | Ownership and acceptance |
|---|---|---|---|
| 1 | Blocked by CI infrastructure | Restore the `Quality` workflow. The 8 November 2026 `master` run 42514864342 ended in `startup_failure` before any job started; successful CodeQL does not prove typecheck, unit/database tests, build or minimal-host smoke. Establish a successful Quality result and diagnose the workflow startup restriction without weakening required security checks. | `nuxt-layers/identity` and the GitHub Actions organisation/repository configuration; no evidence yet that application tests themselves failed. |
| 2 | In progress | Finish the root `CONTRACT.md` operation-level completeness review against actual public exports, including exact callable signatures, request/response types, errors and operational prerequisites. Preserve the independent consumer surface and avoid duplicating detailed internal implementation history. | `nuxt-layers/identity`; public contract and source are reconciled in a dedicated reviewed change. |
| 3 | Waiting on IAM member migrations | Reconcile `capability.json` and structural caller/decision/approval ports with accepted capability contracts. The current manifest names Authentication and Authorisation as required operational integrations, whereas `composeIdentity` permits refusal-only boot without them. Decide how manifest requirements express operational vs boot-only capability requirements; do not silently flip required dependencies to optional or weaken authorisation. | Identity owns the manifest; Authentication and Authorisation own their contracts. Authorisation and Profile migrations precede suite integration. |
| 4 | Deferred to owning capability | Define scheduled execution in `nuxt-layers/scheduler` and message delivery in `nuxt-layers/message-queue`; keep `getIdentityTasks()` and `IdentityEventPublisher` independent of both implementations. | Their separate capabilities own detailed semantics. Identity owns task handlers, events, transactional outbox and delivery acknowledgement expectations. |
| 5 | Waiting on IAM member migrations | Adapt Identity to the accepted shared caller/decision composition boundary through suite integration, without weakening authentication recency, phishing resistance, tenant isolation, governance approvals or reliable outbox delivery. | `nuxt-layers/iam-integration` composes the suite after independent Authorisation and Profile migrations; code changes remain in owning repositories. |
| 6 | Outstanding | Verify accepted current `master`: frozen dependency resolutions, complete Quality checks, minimal-host acceptance and affected downstream IAM consumers. Historical design/roadmap documents remain archival evidence, not parallel plans or current consumer contracts. | CI and affected consumers; record actual pass/fail results rather than inferring acceptance. |

## Architectural boundaries

- **Identity owns:** identities, groups, memberships, governance, its persistence, events, permissions, scheduling requirements and task handlers.
- **Identity consumes:** structural caller, access-decision, event-delivery and database ports. No named implementation is mandatory unless an accepted normative rule expressly makes it so.
- **Scheduler and message transport:** independent infrastructure capabilities whose detailed execution and delivery contracts belong to their own repositories; Identity exposes task descriptors and a public event publisher port without importing them.
- **Composition owns:** connecting supplied services to capabilities. No capability imports a particular consuming application, integration host or Scheduler.
- **Architecture owns:** cross-cutting composition invariants and minimal structural shapes; operational details belong to capability-owned contracts. Accepted ADR-0012 remains authoritative.

This plan records future work, not acceptance of an unamended shared contract or completion of cross-repository integration. Protected branches and separate, reviewed PRs remain mandatory.
