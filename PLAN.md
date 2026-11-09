# Plan

> **In short:** Identity's standalone implementation and security checks are established. Finish independent consumer acceptance; integrate IAM through public contracts when its providers are ready. Scheduling and message transport belong to separate capabilities.

## Completed

| Work | Evidence |
|---|---|
| Version-agnostic organisation and dependency migration | PRs #36 and #38 |
| Refusal-only, one-call `composeIdentity` | PR #39 |
| Minimal-host example, composition-budget check and neutral task descriptors | PR #40; standalone acceptance evidence still to be confirmed below |
| Public contract operation, client and permission coverage | PR #48; independent consumer acceptance remains below |
| Manifest inventory and distinction between standalone startup and operational IAM dependencies | PR #49 |
| Restored Quality workflow | Successful checks on current `master`; future changes must also pass CI |

## Remaining — Identity-owned

| Priority | Work | Acceptance |
|---|---|---|
| 1 | Independently validate the root `CONTRACT.md` against every exported operation, input, output, error and configuration requirement. Correct only demonstrated omissions or inaccuracies. | A consumer installs and uses Identity from `CONTRACT.md` alone without private source or supplementary design documents. |
| 2 | Confirm standalone acceptance evidence on current `master`: frozen dependencies, PostgreSQL/security tests, Quality, minimal-host smoke and the ADR-0012 composition budget. | Record verified CI results and resolve failures; do not infer that passing unit tests proves consumer acceptance. |

## External dependencies — do not block standalone completion

| Dependency | Owner | Identity's condition for integration |
|---|---|---|
| Verified caller, access decisions and independent approval qualification | `authentication`, `authorisation` and `iam-integration` | Reconcile accepted public contracts; preserve authentication recency, phishing resistance, tenant isolation and fail-closed decisions. Adapt Identity only where integration proves necessary. |
| End-to-end IAM consumer acceptance | `iam-integration` and consuming applications | Exercise Identity with real IAM providers and record security/integration results. |
| Scheduled execution and message transport | `nuxt-layers/schedule` and `nuxt-layers/message-queue` | Consume `getIdentityTasks()` and `IdentityEventPublisher` through public contracts; retain Identity-owned handlers, transactional outbox and delivery acknowledgement rules. |

## Boundaries

Identity owns its domain, PostgreSQL schema, permissions, governance, business events, durable outbox and task handlers. The host composes trusted providers; it does not reproduce domain logic. Refusal-only defaults permit safe startup, **not** functional privileged operations. No external implementation dependency is added without an accepted contract and verified consumer need.

Protected branches, reviewed pull requests and CI remain mandatory. Avoid speculative redesign or duplicate architectural rules.
