---
name: bl-orch
description: >
  Baseline orchestrator for fixture pairing. Coordinates two baseline
  skills across 3 stages. Do NOT use for: real work; this is fixture
  material referenced from breaking-changes/ pair tests.
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: orchestrator
  changelog: |
    v1.0.0 — initial baseline.
---

# bl-orch

Baseline orchestrator used by detect-breaking-changes.py fixture
pairs that exercise orchestrator-archetype validators.

## Purpose

Compose bl-atom + bl-tool into a 3-stage workflow.

## When to Use

In fixture tests only.

## When NOT to Use

In real work.

## The Stages

### Stage 1 — Plan
Consume operator intent; produce plan.yaml.

### Stage 2 — Execute
For each item in plan: invoke bl-atom; capture results.

### Stage 3 — Verify
Verify aggregate result; produce verification.md.

## Skills Coordinated

- bl-atom — invoked in Stage 2 once per plan item
- bl-tool — invoked in Stage 3 for verification

## Failure Modes

- Plan parsing fails → halt at Stage 1.
- Atom invocation fails → mark item failed; continue if --continue-on-error.
- Verify fails → halt; report mismatch.

## Handoffs

- to bl-router after verification for dispatch.
