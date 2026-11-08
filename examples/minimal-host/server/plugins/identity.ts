import pg from 'pg'

/**
 * The composition budget includes every host line naming Identity.
 * No host-owned store, event relay, authorisation policy or fake is used.
 * In the absence of IAM integrations, all privileged actions fail closed.
 */
export default defineNitroPlugin(() => {
  const pool = new pg.Pool({
    connectionString: process.env.IDENTITY_DATABASE_URL ?? 'postgres://localhost/identity',
  })
  composeIdentity({ database: { dialect: 'postgres', pool } })
})
