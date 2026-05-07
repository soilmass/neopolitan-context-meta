---
name: example-orch-broken
description: >
  An orchestrator fixture that omits the required `## The Stages` and
  `## Skills Coordinated` sections. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: orchestrator
  changelog: |
    v0.1.0 — initial.
---

# example-orch-broken

Missing `## The Stages` and `## Skills Coordinated`.

## Purpose

Test the failure path.

## When to Use

In tests.

## When NOT to Use

In production.

## Failure Modes

- Validator rejects the fixture.

## Handoffs

- None.
