---
name: bl-tool
description: >
  Baseline tool for fixture pairing. Walks a 3-stage procedure:
  intake, process, output. Do NOT use for: real work; this is
  fixture material referenced from breaking-changes/ pair tests.
license: Apache-2.0
allowed-tools: Read, Write
metadata:
  version: "1.0.0"
  archetype: tool
  changelog: |
    v1.0.0 — initial baseline.
---

# bl-tool

Baseline tool used by detect-breaking-changes.py fixture pairs that
need a tool archetype.

## Purpose

Exercise tool-archetype validators with a minimal valid tool.

## When to Use

In fixture tests only.

## When NOT to Use

In real work.

## Stage-Gated Procedure

### Stage 1 — Intake
Consumes operator prompt; produces intake.yaml; gate: schema valid.

### Stage 2 — Process
Consumes intake.yaml; produces output.yaml; gate: produced.

### Stage 3 — Output
Consumes output.yaml; produces final result; gate: emitted.

## Dependencies

- bl-atom (for capability-a)

## Evaluation

Correct when all 3 stages pass against a known-good intake.

## Handoffs

- to bl-router for downstream dispatch.
