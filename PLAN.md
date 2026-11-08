# Plan

> **In short:** complete Identity's transition to the current architecture and its version-agnostic repository identity.

| Status | Work |
|---|---|
| Complete | Rename active package, module, import, documentation and dependency references to `nuxt-layers` |
| Complete | Regenerate `pnpm-lock.yaml` with pnpm 12 against current `nuxt-layers/theme-manager#master` (PR #38 merged); CI checks remain separate |
| In progress | Add compatibility-preserving one-call `composeIdentity` with refusal-only defaults. Still outstanding: reconcile IAM-specific adapters with ADR-0012's shared shapes, safe event relay and capability-owned tasks; requires explicit design before breaking integration |
| Outstanding | Provide and test `examples/minimal-host` with the ADR-0012 composition budget; the existing `playground` is not a verified substitute |
| Outstanding | Run CI contract, integration, security and acceptance checks, and verify downstream IAM consumers against current `master` |
| Complete | Preserve the original historical roadmap under `docs/roadmap.md` without treating earlier release pins as current instructions |

This is an implementation plan, not a claim that unresolved architectural requirements are satisfied.
