---
defaults: &defaults
  archetype: atom
  license: Apache-2.0

name: yaml-anchor-test
description: >
  YAML anchor in frontmatter. The validator's strict YAML parser may
  accept this (anchors are valid YAML). The fixture exists to confirm
  no crash; expected outcome is exit 0 (parses) or exit 1 (validation
  finding) — but never exit 137 (uncaught crash). Do NOT use for: real work.
license: Apache-2.0
metadata:
  <<: *defaults
  version: "0.1.0"
  changelog: |
    v0.1.0 — initial.
---

# yaml-anchor

## When to Use
in fixture tests.

## When NOT to Use
in real work.

## Capabilities Owned
- A: x.

## Handoffs to Other Skills
- to a.

## Edge Cases
- a.

## References
- (none).
