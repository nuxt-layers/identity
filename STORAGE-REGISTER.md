# Storage Register

> **In short:** Identity persists its own PostgreSQL records and outbox; it does not create browser storage or cookies.

| Mechanism | Purpose and contents | Scope and retention | Essential, fallback and controls |
|---|---|---|---|
| PostgreSQL `identity` schema | Identity records, tenant metadata, personal and other groups, memberships and external opaque identifiers, invitations and token digests, join requests, governance changes, safety periods, service identities, break-glass reviews and recovery holds | Capability-owned schema; tenant isolation where applicable. Retention and disposal follow lifecycle and legal-hold rules implemented by Identity | **Essential.** Without the host-supplied pool the capability fails closed. Migration and runtime roles are distinct; runtime access is limited by RLS and restricted database functions |
| PostgreSQL transactional outbox | Contract events and delivery state for eventual relay | Capability-owned; delivery is at least once, and failed publishing is retried; operational retention governed by event and database maintenance policies | **Essential to event delivery.** Host supplies publisher and schedules the relay; do not remove records merely because publishing failed |
| Browser storage and cookies | None created by this capability | Not applicable | Authentication owns sessions and any associated cookies; Identity reads the authenticated subject through a supplied server resolver |
| Host-owned logs and infrastructure | Host may record operational failures, correlation identifiers or database backups | Host-defined retention, access and region | Not directly created or controlled by Identity; must follow host privacy and security policies |

Identity's group and service-identity names are constrained safe names; it is not a repository for people's names, email addresses or other profile data. Invitations retain token digests rather than plaintext tokens. No consent-requiring optional browser storage is introduced by this layer. Deployments must establish actual database backup, retention, deletion and geographic policies; this inventory is not a claim of a particular jurisdiction's legal compliance.
