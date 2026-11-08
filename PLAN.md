# Plan

> **In short:** complete Identity's transition to the current architecture and its version-agnostic repository identity.

| Status | Work |
|---|---|
| Complete | Rename active package, module, import, documentation and dependency references to `nuxt-layers` |
| Complete | Regenerate `pnpm-lock.yaml` with pnpm 12 against current `nuxt-layers/theme-manager#master` (PR #38 merged); CI checks remain separate |
| In progress | `composeIdentity` is merged (PR #39). Capability-owned scheduler descriptors are proposed here. Still outstanding: reconcile IAM-specific adapters with ADR-0012 shared caller and decision shapes and reliable IAM event delivery; this needs coordinated work with `iam-integration` and Authorisation |
| In progress | Add `examples/minimal-host`, an automated <=50-line composition check, a CI Nuxt build and HTTP smoke test; verify CI before claiming acceptance |
| Outstanding | Run CI contract, integration, security and acceptance checks, and verify downstream IAM consumers against current `master` |
| Complete | Preserve the original historical roadmap under `docs/roadmap.md` without treating earlier release pins as current instructions |

This is an implementation plan, not a claim that unresolved architectural requirements are satisfied.
