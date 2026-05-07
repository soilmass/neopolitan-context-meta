---
name: atom-fail-reference-chain
description: >
  An atom whose references chain to each other (a.md links to b.md). The
  validator should reject this per METADATA-VALIDATION.md. Do NOT use for:
  real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# atom-fail-reference-chain

Demonstrates the intra-skill reference-chain rule: `references/a.md`
links to `references/b.md`, which is forbidden.

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

- `references/a.md` — entry point.
- `references/b.md` — chained target.
