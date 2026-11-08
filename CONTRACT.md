# Identity — Consumer Contract

> **In short:** compose Identity as a peer Nuxt layer, supply its secure PostgreSQL pool and IAM decision ports, and consume only its declared server, HTTP and presentation interfaces. Identity owns identity state, groups, memberships and approvals, not credentials or personal profiles.

**Development status:** Package `@nuxt-layers/identity` uses development version `0.0.0`, contract version `1`, Nuxt `^4.5.0` as its current peer requirement, and Node.js `>=22` as its declared consumer runtime minimum. Formal releases and pins to superseded development revisions are suspended. Cross-capability composition is under migration towards ADR-0012's shared shapes; the implementation currently requires the explicit ports below.

## Install

Add `"@nuxt-layers/identity": "github:nuxt-layers/identity#master"` to the host's `dependencies`. Resolve it with pnpm and commit the generated lockfile; CI installs with `--frozen-lockfile`. Use the current upstream `master` during development.

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  extends: ['@nuxt-layers/identity'],
  identity: { presentation: true, pages: { enabled: true } },
})
```

The layer provides package exports `.` (Nuxt layer), `./contracts` (public Zod schemas, types, permissions, errors), `./conformance` (directory adapter tests), `./capability` (manifest), `./presentation` (presentation entry point) and `./tailwind.css`. Do not import `server/internal`, database migrations or private adapters from consuming code.

## Settings

| Setting | Default | Purpose |
|---|---|---|
| `NUXT_IDENTITY_BASE_URL` / `runtimeConfig.identity.baseUrl` | Empty; mutations refused | Public origin; state-changing requests require a matching `Origin` or `Referer` |
| `NUXT_PUBLIC_IDENTITY_LOCALE` / `runtimeConfig.public.identity.locale` | `en-GB` | Localisation of standard screens |
| `runtimeConfig.public.identity.routes.signIn` | `/sign-in` | Host authentication page |
| `runtimeConfig.public.identity.routes.account` | `/account/groups` | Account navigation |
| `runtimeConfig.public.identity.routes.group` | `/groups/:groupId` | Group navigation |
| `runtimeConfig.public.identity.routes.invitation` | `/invitations/accept` | Invitation navigation |
| `runtimeConfig.public.identity.routes.change` | `/changes/:changeId` | Governance-change navigation |
| `identity.presentation` | `true` | When false, registers no presentation pages, components or styles |
| `identity.pages.enabled` | `true` | When false, hides default pages but retains presentation components |
| `identity.pages.paths` | Paths in Screens | Change paths; group/change must keep their required route parameters |

The layer's mandatory database schema defaults to `identity`. Pass `schema` only when needed; it must be a lower-case PostgreSQL identifier matching `^[a-z_][a-z0-9_]{0,62}$`. The default policy is secure; `provideIdentityPolicy` validates overrides and rejects unmitigated weakening.

## Host passes

At deployment, a privileged **migration pool** applies `migrateIdentityDatabase({ pool: migrationPool, runtimeRole, schema? })`. The runtime role must not own tables, be a superuser or have `BYPASSRLS`. Migration credentials must not be available to ordinary request handling. The host provisions tenants and their initial root groups using this privileged pool only.

At startup, use the one-call `composeIdentity` server utility from a Nitro plugin. The following basic configuration is **refusal-only** until Authentication, Authorisation and reliable event delivery are connected:

```ts
export default defineNitroPlugin(() => {
  composeIdentity({ database: { dialect: 'postgres', pool: runtimePool } })
})
```

The host must construct `runtimePool` securely before this call (for example, a `pg.Pool` using a server-only `IDENTITY_DATABASE_URL` environment variable). The consuming host must install its own PostgreSQL driver, configure a least-privileged runtime role and apply migrations separately with a privileged operator connection. To enable authenticated administration, supply `accessDecision`, `approvalPolicy`, `subjectResolver` and `eventPublisher` in the same `composeIdentity({ database, accessDecision, approvalPolicy, subjectResolver, eventPublisher, policy?, clock? })` call. These are the **current** Identity-specific port shapes; the future ADR-0012 shared caller and decision shapes are not yet adapted. Without an access decision every privileged decision is denied; without an approval policy no approver qualifies; without a subject resolver HTTP requests are anonymous; without a publisher the outbox relay rejects without acknowledging delivery. Never use these refusal-only defaults as a working production IAM integration.

For compatibility, the individual `provideIdentity*` server utilities remain available. Their current structural shapes (with public TypeScript types from `@nuxt-layers/identity/contracts`) are:

| Function | Expected structural shape | Mandatory |
|---|---|---|
| `provideIdentityDatabase({ dialect: 'postgres', pool, schema? })` | `pool.query(text, values?)`, `pool.connect()`, `pool.end()` as a `pg`-compatible pool | Yes; pass in `composeIdentity.database` |
| `provideIdentityAccessDecision({ decide })` | `decide({ subject, permission, groupId, correlationId }) → Promise< { allowed: true } \| { allowed: false, reason: 'not-permitted' } \| { allowed: false, reason: 'insufficient-assurance', requirement } >` | For operational permissions; otherwise deny-all default |
| `provideIdentityApprovalPolicy({ riskOf, qualifies, countQualifying })` | `riskOf(permission) → riskLevel \| null`; `qualifies({ approverId, permission, groupId }) → boolean`; `countQualifying({ permission, groupId, excludingId, limit }) → number`, all asynchronous | For operational approvals; otherwise no-approval default |
| `provideIdentityEventPublisher({ publish })` | `publish(event) → Promise<void>`; must reject on unsuccessful delivery | For successful outbox relays; otherwise delivery refused |
| `provideIdentitySubjectResolver({ resolve })` | `resolve(event)` supplies Authentication's principal or null; required for HTTP use | For authenticated endpoints; otherwise anonymous default |
| `provideIdentityClock({ now })` | `now() → Date`; defaults to system clock, invalid results fail closed | No |
| `provideIdentityPolicy(input)` | Validated `IdentityPolicyInput`; defaults to secure policy | No |

Authenticated subjects have `{ principalId, authenticatedAt, assurance: { level: 'aal1' | 'aal2', phishingResistant: boolean } }`; `principalId` is Identity's opaque identifier. Access and policy failures must reject, not authorise by default. The platform group is set through `provideIdentityPolicy({ platformGroupId })`; without it privileged governance operations are refused. Add `IDENTITY_PERMISSIONS` from `./contracts` to the Authorisation catalogue.

These are the **current implemented** ports, not ADR-0012's final simplified `resolveCaller` and `decide` wiring. Do not silently substitute those new shapes until Identity's implementation and its IAM consumers have been migrated.

## Scheduled operations

`getIdentityTasks()` is a public server utility returning scheduler-neutral descriptors of the ADR-0012 shape `{ name, every, run }`. The `every` value is a five-field cron expression: `identity:maintenance` runs every five minutes, and `identity:outbox` runs every minute. A host's central scheduler calls `run()`; Identity owns the implementation and its PostgreSQL outbox, not the host. Production outbox relaying requires a real `eventPublisher`; without one, delivery fails rather than marking messages as published. These tasks are **not** automatically scheduled on import.

`examples/minimal-host` is a standalone Nuxt consumer that invokes `composeIdentity` once in its server plugin. Its default configuration demonstrates refusal-only operation and is not a full IAM application. CI builds the example, checks an unauthenticated health endpoint and measures host composition against the 50-line ADR-0012 budget. To use protected operations, the host must supply verified Authentication, Authorisation and event-delivery ports.

## Client and server functions

Server composition functions are available through Nuxt/Nitro's public server utilities: `getIdentityTasks`, `composeIdentity`, `provideIdentityDatabase`, `provideIdentityAccessDecision`, `provideIdentityApprovalPolicy`, `provideIdentityEventPublisher`, `provideIdentitySubjectResolver`, `provideIdentityClock`, `provideIdentityPolicy`. Their counterparts `useIdentity*` read the effective ports and refuse absent mandatory providers.

The supported server functions and entry points are:

| Function | Role |
|---|---|
| `migrateIdentityDatabase({ pool, runtimeRole, schema? })` | Apply owned migrations and database privilege checks |
| `getIdentityProvisioning()` | `reserve`, `confirm` and sign-in status for Authentication |
| `getIdentityDirectory()`, `getIdentityAccessGovernance()` | Strong directory and group governance reads for Authorisation |
| `getIdentityDisclosureContext()` | Disclosure context for Profile |
| `getIdentityGovernance()` | Ordinary group and membership management |
| `getIdentityApprovals()` | Request, decide, cancel, object and inspect governed changes |
| `getIdentityJoining()` | Invitations, join requests and acceptance decisions |
| `getIdentityLifecycle()` | Person's pause, resume, closure and ownership checks |
| `getIdentityBreakGlass()` | Emergency actions and review |
| `getIdentityQueries()` | Signed-in identity, group, members and change reads |
| `getIdentityScimStructure()` | Structural SCIM user/group data; host supplies sign-in and profile fields |
| `getIdentityServiceIdentities()` | List, read, rename, leave, credential governance and owner audience |
| `recordIdentityCredentialRecovery({ identityId, recoveredAt, correlationId })` | Trigger governance safety hold |
| `exportIdentityData({ identityId, correlationId })` | Verified access-request export |
| `provisionIdentityTenant({ pool, jurisdiction, dataRegion, externalId?, correlationId, schema? })` | Privileged tenant creation |
| `bootstrapIdentityRootGroup({ pool, tenantId, name, firstOwnerId, correlationId, schema? })` | Privileged founding root group |
| `provisionIdentityBreakGlass({ pool, homeTenantId, correlationId, schema? })` | Privileged emergency identity creation |
| `runIdentityMaintenance()` | Apply due lifecycle, approval and retention transitions |
| `relayIdentityOutbox({ limit? })` | Publish pending events at least once (default limit 100) |
| `identityLegalHoldCovers({ kind, id })`, `recordIdentityDisposal({ subject, member, eventId, correlationId })`, `getIdentityDisposal({ kind, id })` | Retention and cross-capability disposal |
| `exportIdentityTenantData({ subject, tenantId, correlationId })` | Closing tenant's governance export |

The factory methods above return typed services with operation-specific inputs and outputs under `./contracts`. Each operation validates against those schemas and returns a typed result or an `IdentityError`, never an unchecked provider response. The layer's `/api/identity/*` HTTP surface delegates to these functions, with the identity principal resolved server-side. It includes `/me` lifecycle, group CRUD and members, memberships, invitations and join requests, governance `/changes`, break-glass actions and service identities. `useIdentity()` exposes matching typed client operations; it is not an authorisation boundary.

Errors are `unauthenticated` (401), `forbidden` (403), `insufficient-assurance` (403), `validation-failed` (400), `conflict` (409), `rate-limited` (429) and `unavailable` (503). HTTP error bodies contain `{ code, messageKey, reason? }`, with `reason` only for eligible validation/conflict responses. A missing required port raises `IdentityCompositionError`; outages and invalid clocks are refused, never replaced by an implicit allow.

## Permissions

Identity's permission catalogue is `IDENTITY_PERMISSIONS` in `./contracts`, including group creation, view and rename; membership viewing and changes; invitation handling and joining; approval of governance operations; service identity management; tenant export; break-glass and legal-hold governance. The catalogue's `risk` and `effect` fields are authoritative for the host's decision/approval integration. Sensitive actions require the declared assurance and, where applicable, independent approval and safety periods. Membership alone never grants unrestricted permissions. Failed decisions are denied, without leaking whether another identity or group exists.

## Screens

Default page paths are `/account/groups`, `/groups/:groupId`, `/invitations/accept` and `/changes/:changeId`. They display only contract-authorised data; the host supplies its own sign-in route, Profile name renderer (`IdentityPersonName`) and semantic Theme Manager stylesheet where available. For styling import `@nuxt-layers/theme-manager/presentation.css` and `@nuxt-layers/identity/tailwind.css` into the host's Tailwind stylesheet. Theme Manager is optional for behaviour, and without its stylesheet screens remain functional but unstyled. The host may move default routes via `identity.pages.paths`, turn off pages with `identity.pages.enabled: false` or turn off all presentation registration with `identity.presentation: false`.

## Headless surface

Custom screens MUST use the published functions or HTTP API, never direct schema access; must preserve step-up, authorisation, approval, tenant and lifecycle checks on the server; must not reveal group or identity existence through forbidden responses; and must not expose invitation tokens in server routes, logs or referrers. Invitations carry tokens in URL fragments. Administrative screens and any equivalent host replacement must be non-cacheable, non-frameable and use `Referrer-Policy: no-referrer`. Apply WCAG 2.2 AA, localisation and Theme Manager's semantic styling vocabulary when presenting this capability.

## You will hit this

A human identity has exactly one permanent personal group; other groups have at most one parent and may not form cycles. Multiple direct memberships are supported; hierarchy confers no permissions. Use the public safe-name and identifier schemas. Never put profile data, email addresses, raw invitation tokens or credentials in Identity. Provision tenants and first root groups from an operator-only procedure, not an HTTP endpoint. The host owns invitation-address delivery, authenticated principals, migration credentials, scheduling and lifecycle of its database connection. It must run `runIdentityMaintenance()` and `relayIdentityOutbox()` on a suitable recurring schedule and must integrate the provided provisioning, directory and disclosure contracts with other IAM members through supported composition. The existing host-adapter burden remains a documented architectural gap until ADR-0012 is implemented.
