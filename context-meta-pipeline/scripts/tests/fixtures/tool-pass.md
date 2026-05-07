---
name: example-tool-pass
description: >
  Demonstrates a passing tool skill. Single workflow that produces one kind
  of output. Do NOT use for: dispatching across atoms (use a router).
license: Apache-2.0
metadata:
  version: "0.2.0"
  archetype: tool
  changelog: |
    v0.2.0 — added stage 4.
    v0.1.0 — initial.
---

# Example Tool (Pass Fixture)

## Purpose

Run a single, well-bounded workflow producing one named artifact.

## When to Use

When the operator wants the workflow this tool encapsulates and not a
generic dispatch.

## When NOT to Use

When the request requires multiple skills cooperating — use an orchestrator.

## Stage-Gated Procedure

1. Stage 1: intake → produces `intake.yaml`.
2. Stage 2: planning → produces `plan.md`.
3. Stage 3: execution → produces the output artifact.

## Dependencies

- None internal.
- External: PyYAML (for parsing intake).

## Evaluation

The tool is correct iff the produced artifact matches the contract in
`references/output-contract.md` for ten worked examples.

## Handoffs

- Output is consumed by the family router or downstream tool by name.
