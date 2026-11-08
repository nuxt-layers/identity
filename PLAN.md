# Plan

> **In short:** complete Identity's transition to the current architecture and its version-agnostic repository identity.

| Status | Work |
|---|---|
| In progress | Rename active package, module, import, documentation and dependency references to `nuxt-layers` |
| Outstanding | Regenerate `pnpm-lock.yaml` with pnpm 12 against current `nuxt-layers/theme-manager#master` and verify frozen resolution |
| Outstanding | Reconcile the existing host-specific IAM adapters and mandatory event publisher with ADR-0012's shared host shapes and capability-provided defaults; requires an explicit design decision before breaking integration |
| Outstanding | Provide and test `examples/minimal-host` with the ADR-0012 composition budget; the existing `playground` is not a verified substitute |
| Outstanding | Run CI contract, integration, security and acceptance checks, and verify downstream IAM consumers against current `master` |
| Complete | Preserve the original historical roadmap under `docs/roadmap.md` without treating earlier release pins as current instructions |

This is an implementation plan, not a claim that unresolved architectural requirements are satisfied.
