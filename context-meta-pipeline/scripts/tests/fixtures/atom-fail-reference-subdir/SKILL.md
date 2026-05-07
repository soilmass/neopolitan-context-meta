---
name: atom-fail-reference-subdir
description: >
  An atom with a nested references subdirectory. References must be one
  level deep per METADATA-VALIDATION.md. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# atom-fail-reference-subdir

Demonstrates the "references must be one level deep" rule. Has
`references/sub/x.md` which the validator must reject.

## When to Use

In tests.

## When NOT to Use

In production.

## Capabilities Owned

- A: a single capability.

## Handoffs to Other Skills

- to a.

## Edge Cases

- a.

## References

- `references/sub/x.md` — nested too deep.
