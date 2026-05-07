---
name: example-tool-broken
description: >
  A tool fixture that omits the required `## Stage-Gated Procedure` section.
  The validator should reject it. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: tool
  changelog: |
    v0.1.0 — initial.
---

# example-tool-broken

Missing `## Stage-Gated Procedure`, `## Dependencies`, and `## Evaluation`.
The validator must report each missing required section.

## Purpose

Demonstrate the failure path.

## When to Use

In tests.

## When NOT to Use

In production.

## Handoffs

- To no one.
