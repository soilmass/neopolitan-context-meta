---
name: bl-house-policy
description: >
  Baseline policy overlay for fixture pairing. Overlays bl-atom with
  two house conventions. Do NOT use for: real work; this is fixture
  material referenced from breaking-changes/ pair tests.
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: policy
  changelog: |
    v1.0.0 — initial baseline.
---

# bl-house-policy

Baseline policy overlay used by detect-breaking-changes.py fixture
pairs that exercise policy-archetype validators.

## Purpose

Apply house conventions on top of `bl-atom`.

## Applies On Top Of

- `bl-atom` (the mechanism atom)

## Conventions Enforced

- Always lowercase identifiers.
- Always tab-indent (no spaces).

## Override Behavior

- If `bl-atom` is missing, fail loudly rather than silently substitute.
- House rules override the mechanism's defaults; mechanism does not
  re-apply after the overlay has fired.
