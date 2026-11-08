import { afterEach, describe, expect, it, vi } from 'vitest'
import { clearIdentityComposition, composeIdentity, useIdentityEventPublisher } from '../server/utils/identity-composition'
import { getIdentityTasks } from '../server/utils/identity-tasks'

afterEach(() => clearIdentityComposition())

describe('Identity scheduler descriptors', () => {
  it('publishes capability-owned tasks with stable names and cron cadences', () => {
    const tasks = getIdentityTasks()
    expect(tasks.map(task => [task.name, task.every])).toEqual([
      ['identity:maintenance', '*/5 * * * *'],
      ['identity:outbox', '* * * * *'],
    ])
    expect(tasks.every(task => typeof task.run === 'function')).toBe(true)
  })

  it('does not acknowledge an event when no event publisher is configured', async () => {
    const pool = { query: vi.fn(), connect: vi.fn(), end: vi.fn() }
    composeIdentity({ database: { dialect: 'postgres', pool } })
    await expect(useIdentityEventPublisher().publish({} as never)).rejects.toMatchObject({ code: 'unavailable' })
  })
})
