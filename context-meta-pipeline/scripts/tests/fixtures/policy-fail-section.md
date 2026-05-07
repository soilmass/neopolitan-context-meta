---
name: house-example-broken
description: >
  A policy overlay fixture that omits the required `## Conventions Enforced`
  and `## Override Behavior` sections. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  changelog: |
    v0.1.0 — initial.
---

# house-example-broken

Missing the required `## Conventions Enforced` and `## Override Behavior`
sections — the validator must reject this.

## Purpose

Test the policy archetype failure path.

## Applies On Top Of

- `example`
