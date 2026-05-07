---
name: bl-router
description: >
  Baseline router for fixture pairing. Dispatches to three baseline
  atoms by intent. Do NOT use for: real work; this is fixture material
  referenced from breaking-changes/ pair tests for routing changes.
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: router
  changelog: |
    v1.0.0 — initial baseline.
---

# bl-router

Baseline router used by detect-breaking-changes.py fixture pairs that
exercise routing-table changes.

## When to Use

In fixture tests when routing-table behavior is under test.

## When NOT to Use

In real work.

## Routing Table

| Intent | Target atom |
|---|---|
| Inspect baseline state | `bl-atom-inspect` |
| Modify baseline state | `bl-atom` |
| Recover from baseline failure | `bl-atom-recovery` |
| Configure baseline state | `bl-atom-config` |

## Disambiguation Protocol

When a prompt could match two atoms, ask one clarifying question:
"inspect (read-only)" vs "modify (write)".

## Atoms in This Family

- `bl-atom`
- `bl-atom-inspect`
- `bl-atom-recovery`
- `bl-atom-config`
