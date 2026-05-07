---
name: house-example-conventions
description: >
  Overlays house conventions on top of the example mechanism atom. Applies
  team-specific style rules. Do NOT use for: domain mechanics (use the
  underlying atom directly).
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: policy
  changelog: |
    v1.0.0 — initial.
---

# house-example-conventions

A fixture used to verify validate-metadata.py accepts a well-formed policy
overlay.

## Purpose

Apply house conventions on top of the example domain.

## Applies On Top Of

- `example` (the mechanism atom)

## Conventions Enforced

- Always lowercase.
- Always tab-indent.
- Never operate on shared state without an audit trail.

## Override Behavior

- If the underlying mechanism atom is missing, fail loudly rather than
  silently substitute a default.
- House rules override the mechanism's defaults; the mechanism never
  re-applies after the overlay has fired.
