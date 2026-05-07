---
name: example-orch
description: >
  Orchestrator that coordinates example-tool and example-other through
  three named stages. Do NOT use for: single-skill workflows (use the
  individual tool).
license: Apache-2.0
metadata:
  version: "1.0.0"
  archetype: orchestrator
  changelog: |
    v1.0.0 — initial.
---

# Example Orchestrator (Pass Fixture)

## Purpose

Run a multi-skill workflow with explicit stage gates and named hand-offs.

## When to Use

When the workflow spans two or more skills and the order matters.

## When NOT to Use

When a single tool produces the desired output — use the tool directly.

## The Stages

1. **Plan** — call `example-tool` to produce a plan.
2. **Apply** — call `example-other` to act on the plan.
3. **Verify** — re-call `example-tool` in inspection mode to confirm.

## Skills Coordinated

- `example-tool`
- `example-other`

## Failure Modes

- Plan fails → halt; emit reason.
- Apply fails → roll back via `example-other --undo`.
- Verify fails → flag for human review.

## Handoffs

- On completion: emit a summary artifact for the calling agent.
