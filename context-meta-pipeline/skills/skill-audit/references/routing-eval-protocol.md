# Routing Eval Protocol

This document describes how `skill-audit` Stage 4 will measure
triggering accuracy *when the routing-eval infrastructure exists*.

In v0.1.0 the protocol is **not implemented** — Stage 4 records
`gate_pass: "N/A"` with reason "no routing eval suite". The protocol
is documented here so that when the deferred `skill-evaluate` skill is
built (per library-root `coverage.md` build trigger), the v0.1.0 docs
already specify the contract.

## Anatomy of the eval suite

The eval suite lives at `scripts/tests/routing-eval.yaml`. Each entry
is a `(prompt, expected_skill)` pair plus optional metadata:

```yaml
- prompt: "I want to add a new skill for parsing HTML metadata."
  expected: skill-author
  rationale: "single skill request — not a family"
  added: 2026-05-15
  added_by: <author>

- prompt: "Scaffold a postgres family for me."
  expected: family-bootstrap
  rationale: "domain bootstrap — explicit family ask"

- prompt: "Health-check the git family."
  expected: skill-audit
  rationale: "audit ask"
```

Target size: 100-200 entries spanning all skills in the library, with
balanced positive cases (where each skill should fire) and negative
cases (where each skill should NOT fire).

## How Stage 4 uses it

When the eval suite exists at `scripts/tests/routing-eval.yaml`:

1. Load the YAML; partition by `expected` skill.
2. For each skill in the audit's `audit-scope.yaml`:
   - Take the held-out positive prompts for that skill.
   - For each prompt, run the prompt through the routing layer
     (whatever mechanism the library is using — at small library
     sizes, that's just LLM matching against descriptions).
   - Count: how many prompts actually triggered this skill?
3. Compute `accuracy = correct_triggers / total_prompts`.
4. Record in `routing-report.json` for that skill.

## Held-out vs in-distribution

The eval suite may include prompts written *to* match a specific
skill's description (in-distribution) and prompts derived from real
operator usage (held-out). Stage 4 should use only held-out prompts
for accuracy measurement — in-distribution prompts measure
description fidelity to itself, not routing accuracy.

The split is enforced by tagging:

```yaml
- prompt: "..."
  expected: skill-author
  source: held_out  # or: in_distribution
```

Stage 4 filters on `source: held_out`.

## Negative cases

For each skill, also include prompts that should *not* trigger it
(true negatives):

```yaml
- prompt: "Run a health check on the library."
  expected: skill-audit
  not_expected: [skill-author, family-bootstrap]
  source: held_out
```

The accuracy metric for skill-author then includes whether
`skill-author` correctly *abstained* on this prompt. False positives
count against accuracy as much as false negatives.

## When to add to the suite

- Whenever a routing failure is observed in real usage, add the prompt
  with the correct `expected` skill.
- Whenever a new skill is authored, add 5-10 positive prompts and
  3-5 negative prompts as part of `skill-author` Stage 4.
- Whenever a skill's description is rewritten, add a held-out prompt
  exercising the new wording.

The eval suite is itself a maintained artifact. It has the same
freshness gate (recency check) as skills do.

## What this protocol does not do (yet)

- It doesn't run automatically. v0.1.0 has no scheduler. The deferred
  `skill-evaluate` skill (per library-root `coverage.md`) will own
  scheduled runs.
- It doesn't gate description-changes at PR time. That's also part
  of the deferred `skill-evaluate` work.
- It doesn't measure response *quality* — only *routing*. Whether the
  skill produces good output once invoked is a separate concern.

## When this gets implemented

Build trigger (from library-root `coverage.md` §"Domains Deferred"):

> First library reaches 25 skills OR first description-change
> regression slips through.

When that fires, build the deferred `skill-evaluate` skill, populate
`scripts/tests/routing-eval.yaml`, and update this document to match
the implementation.
