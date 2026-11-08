// A minimal, independent Nuxt consumer of Identity's published layer.
export default defineNuxtConfig({
  extends: ['../..'],
  compatibilityDate: '2026-06-30',
  identity: { presentation: false },
})
