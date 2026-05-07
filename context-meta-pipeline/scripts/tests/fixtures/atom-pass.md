---
name: example-atom-pass
description: >
  Demonstrates a passing atom skill for the validator. Performs a single
  domain capability with disciplined boundaries. Do NOT use for: anything
  that needs orchestration of multiple skills (use a tool or orchestrator).
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: atom
  changelog: |
    v1.0.0 — initial.
---

# Example Atom (Pass Fixture)

A fixture used to verify validate-metadata.py accepts a well-formed atom.

## When to Use

When the operator needs the single capability this atom owns and no other
sibling fits.

## When NOT to Use

When the work is multi-step or requires orchestration. Do not use as a
substitute for a router.

## Capabilities Owned

- Capability A: a single, narrow operation.
- Capability B: an adjacent operation tightly bound to A.

## Handoffs to Other Skills

- For multi-step workflows: hand off to a tool skill.
- For dispatch decisions: hand off to the family router.

## Edge Cases

- Empty input — return early with a no-op.
- Hostile input — fail loudly with a structured error.

## References

- `references/example.md` — extended notes on the canonical edge cases.
