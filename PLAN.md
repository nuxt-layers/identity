# Plan

> **In short:** finish Identity's ADR-0012 integration by keeping its public contract provider-neutral, defining common caller and decision requirements at the architectural level, and exposing its own scheduled operations without depending on the future `nuxt-layers/scheduler` capability.

## Completed baseline

| Status | Work |
|---|---|
| Complete | Move active package, module, documentation and dependency references to the version-agnostic `nuxt-layers` organisation (PR #36) |
| Complete | Regenerate and merge the pnpm 12 lockfile against the current Theme Manager development dependency (PR #38) |
| Complete | Introduce backward-compatible, fail-closed `composeIdentity` (PR #39) |
| Complete | Add an independent `examples/minimal-host`, composition-budget check, CI build/smoke checks and capability-owned `getIdentityTasks()` descriptors (PR #40 merged; inspect its recorded CI results separately before claiming comprehensive downstream acceptance) |

## Next work — in dependency order

| Priority | Status | Work | Ownership and acceptance |
|---|---|---|---|
| 1 | In progress | Review accepted ADR-0012 shared caller, decision and scheduled-task shapes. Record required assurance (level, authentication recency, phishing resistance), tenant/resource context and fail-closed semantics. Assess scheduler concurrency, retries, timeouts, idempotency and distributed execution without assuming these are already normative. | `nuxt-layers/architecture-rules` owns any amendments; proposed changes require explicit architectural acceptance before adoption. Do not silently change shared shapes. |
| 2 | Outstanding | Reconcile Identity's root `CONTRACT.md` with its public exports and code. Make it self-contained and provider-neutral: Identity documents only its capability, ports, returned values, errors, permissions, security requirements, presentation and tasks. Remove prescriptions about named consumers, IAM integration implementations and Scheduler. Keep necessary integration instructions and exact structural interfaces. | `nuxt-layers/identity`; docs-only first, with contract checks. Any code/contract behaviour discrepancy is separately tracked rather than hidden by documentation. |
| 3 | Outstanding | Design the independent `nuxt-layers/scheduler` capability, following approved shared task shapes. Clarify task registration, triggering, distributed execution, concurrency, failure handling, retries, observability and persistence boundaries. Identity owns its job definitions and handlers; Scheduler does not own Identity business logic. | `nuxt-layers/scheduler` owns its design, `CONTRACT.md` and implementation. Identity MUST NOT import Scheduler or require its presence. |
| 4 | Outstanding | Implement the common caller and decision provision through the suite integration boundary and adapt Identity without breaking or weakening privileged approvals, assurance checks, tenant isolation or reliable events. Use the accepted provider-neutral interfaces and keep composition within ADR-0012's budget. | Coordinated changes in `nuxt-layers/iam-integration`, Authorisation and other affected providers/consumers. Each repository owns its own code, contract and PR. |
| 5 | Outstanding | Verify the integrated result on current `master`: frozen dependency resolutions, contract tests, fail-closed/security tests, CI minimal-host smoke, scheduler execution and affected downstream IAM consumers. | CI and consuming repositories; report results and remaining failures rather than implying success from provider CI alone. |

## Architectural boundaries

- **Identity owns:** identities, groups, memberships, governance, its persistence, events, permissions, scheduling requirements and task handlers.
- **Identity consumes:** structural caller, access-decision, event-delivery and database ports. No named implementation is mandatory unless an accepted normative rule expressly makes it so.
- **Scheduler owns:** the generic mechanism to register, trigger, coordinate and observe jobs; not Identity's business operations. The canonical repository name is `nuxt-layers/scheduler`.
- **Composition owns:** connecting supplied services to capabilities. No capability imports a particular consuming application, integration host or Scheduler.
- **Architecture owns:** shared port and task shapes. Existing ADR-0012 is authoritative until changes are formally accepted.

This plan records future work, not acceptance of an unamended shared contract or completion of cross-repository integration. Protected branches and separate, reviewed PRs remain mandatory.
