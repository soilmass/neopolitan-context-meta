---
name: example-router-broken
description: >
  A router fixture that omits the required `## Routing Table` section.
  The validator should reject it. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: router
  changelog: |
    v0.1.0 — initial.
---

# example-router-broken

Missing the `## Routing Table` and `## Disambiguation Protocol` sections.

## When to Use

For testing.

## When NOT to Use

In production.

## Atoms in This Family

- `example-inspection`
- `example-recovery`
- `example-config`
