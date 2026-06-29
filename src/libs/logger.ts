/**
 * Debug logger — outputs only in development builds.
 * In production Vite tree-shakes these calls away entirely.
 *
 * Usage:
 *   import { log, dir } from '@/libs/logger'
 *   log('clicked', itemdata)   // dev only
 *   dir(node)                  // dev only — safe on large Proxy objects
 */

const DEV = import.meta.env.DEV

export const log = DEV
  ? (...args: unknown[]) => console.log(...args)
  : () => {}

export const dir = DEV
  ? (...args: unknown[]) => console.dir(...args)
  : () => {}

export const warn = DEV
  ? (...args: unknown[]) => console.warn(...args)
  : () => {}

// error 始终输出（不受环境限制）
export const error = (...args: unknown[]) => console.error(...args)
