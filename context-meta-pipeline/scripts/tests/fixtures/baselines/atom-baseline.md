---
name: bl-atom
description: >
  Baseline atom for fixture pairing. Owns capability-a and capability-b.
  Hands off to other baseline skills. Do NOT use for: real work; this
  is fixture material referenced from breaking-changes/ and migration/
  pair tests.
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: atom
  changelog: |
    v1.0.0 — initial baseline.
---

# bl-atom

Baseline atom used by `detect-breaking-changes.py` and
`migration-guide-gen.py` fixture pairs.

## When to Use

In fixture tests only.

## When NOT to Use

In real work; this skill is fixture material.

## Capabilities Owned

- `capability-a` — first baseline capability.
- `capability-b` — second baseline capability.

## Handoffs to Other Skills

- to `bl-router` for dispatch decisions.

## Edge Cases

- empty input → no-op.

## References

- (none — fixture material).
