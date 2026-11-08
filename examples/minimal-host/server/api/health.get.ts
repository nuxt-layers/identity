import { defineEventHandler } from 'h3'

// A public composition smoke endpoint; no Identity database query or secret.
export default defineEventHandler(() => ({ status: 'ok' }))
