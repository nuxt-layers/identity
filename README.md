# Identity

> **In short:** Identity owns opaque identities, personal groups, tenants, group hierarchies and memberships. It never owns credentials, personal profiles or access decisions.

This is the `@nuxt-layers/identity` foundation capability in the Nuxt Layers IAM suite. It is developed in the version-agnostic `nuxt-layers` organisation; the current implementation uses Nuxt 4. Its contract is version 1, while formal release-based integration is suspended.

## Responsibility

Identity provides identity lifecycle and provisioning, one permanent personal group for each person, many independent memberships, a zero-or-one-parent group hierarchy, tenant boundaries, governance approvals, invitations, and service identities. Group hierarchy and membership never imply permission. Identity stores opaque identifiers and safe group/service names, not people's names, contact details, credentials or session information.

Authentication owns sign-in, Profile owns personal information and Authorisation owns decisions. Identity accepts their capabilities through typed ports without importing other IAM packages.

## Integration

Read the complete [host integration contract](CONTRACT.md) to install, configure and compose this layer, including its PostgreSQL roles, required ports, security rules, optional presentation, API and background tasks. Public schemas and helper types are exported by `@nuxt-layers/identity/contracts`; adapter conformance by `@nuxt-layers/identity/conformance`.

## Documentation

- [CONTRACT.md](CONTRACT.md) — standalone consumer contract
- [RESOURCES.md](RESOURCES.md) — verified external architectural authorities
- [PLAN.md](PLAN.md) — current planned remediation
- [STORAGE-REGISTER.md](STORAGE-REGISTER.md) — persistent storage inventory
- [Threat model](docs/threat-model.md) — security risks and controls
- [Internal contract detail](docs/contracts.md) and [composition detail](docs/composition-contract.md) — implementation evidence, not a competing public integration contract
- [Design history](docs/design-decisions.md) and [historical roadmap](docs/roadmap.md)

## Development

Use Node.js 26 LTS and pnpm 12 for development and CI. The package currently declares Nuxt 4 as a peer dependency and Node.js 22 or newer as its consumer runtime requirement; these are implementation declarations, not restrictions on the organisation name.

Run `corepack pnpm install --frozen-lockfile` after dependency resolutions have been refreshed, then `corepack pnpm check`, `corepack pnpm build:playground` and `python3 scripts/check_markdown.py` as appropriate. CI is the quality gate.

## Licence

MIT
