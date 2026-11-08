import { relayIdentityOutbox, runIdentityMaintenance } from './identity-server'

/**
 * Capability-owned, scheduler-neutral task descriptors (ADR-0012).
 * The host schedules these functions; it does not reproduce Identity's
 * retention, governance or outbox implementation.
 *
 * Runs require a composed database. The relay additionally requires a
 * functioning event publisher and never acknowledges undelivered events.
 */
export interface IdentityScheduledTask {
  name: string
  /** Standard five-field cron expression; interpreted by the host scheduler. */
  every: string
  run: () => Promise<unknown>
}

export function getIdentityTasks(): IdentityScheduledTask[] {
  return [
    {
      name: 'identity:maintenance',
      every: '*/5 * * * *',
      run: () => runIdentityMaintenance(),
    },
    {
      name: 'identity:outbox',
      every: '* * * * *',
      run: () => relayIdentityOutbox({ limit: 100 }),
    },
  ]
}
