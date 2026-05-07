---
name: example
description: >
  Router for the example domain — dispatches across example-* atoms by
  intent. Do NOT use for: performing operations directly (route to the
  matching atom).
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: router
  changelog: |
    v1.0.0 — initial.
---

# Example (Router Pass Fixture)

## When to Use

When the operator's prompt names the example domain but doesn't pin a
specific failure-mode atom.

## When NOT to Use

When the prompt names a specific atom by failure mode (`example-recovery`,
`example-config`). Atom precedence wins on specificity.

## Routing Table

| Intent | Target atom |
|---|---|
| Inspect example state | `example-inspection` |
| Repair broken example | `example-recovery` |
| Configure example | `example-config` |

## Disambiguation Protocol

When the prompt could match two atoms, ask one clarifying question keyed
to the failure mode in the user's wording.

## Atoms in This Family

- `example-inspection`
- `example-recovery`
- `example-config`
