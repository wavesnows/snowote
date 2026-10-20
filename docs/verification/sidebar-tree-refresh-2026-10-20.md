# Sidebar tree refresh verification

Snowote retains FileTree across menu switches and already scans directories asynchronously. However, binding reactive notebook data directly to Element Plus's deep data watcher still rebuilds the tree when refreshed data changes. Refresh also filters the entire tree with an empty query.

The fix isolates the raw view data and reconciles nodes by path, retaining selection and expansion. Removed descendants are unregistered, canonical deletion uses paths, and Markdown/JSON note and folder creation refresh canonical data after writing instead of mutating view snapshots. Pin changes are observed explicitly.

Validation on 2026-10-20:
- Regression tests added before implementation failed against the original code.
- Node 23.11.0 `node --test tests/*.test.cjs`: 16 passed. Includes 25,000-node addition, ordering, subtree removal, stale selection, canonical deletion and Markdown/JSON/folder creation integration.
- `vue-tsc --noEmit`: passed (no diagnostics).
- `vite build`: passed.
- `electron tests/tree-view-electron.smoke.cjs`: passed against the production renderer with isolated home and userData. Adding one file created only one node (42 ms measured); 24 actual menu DOM clicks retained selection and expansion. Pin ordering, bulk removal and note restoration passed.
- `git diff --check`: passed.

The installed application was not replaced, and no user notes were changed. The Electron check uses synthetic data; it does not claim to reproduce or eliminate every possible intermittent freeze in the user's live instance.
