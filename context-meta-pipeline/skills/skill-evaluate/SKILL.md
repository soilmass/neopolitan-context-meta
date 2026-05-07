---
name: skill-evaluate
description: >
  Runs held-out routing-eval prompts against the live skill descriptions
  and reports triggering accuracy per skill (Health Gate 3 from
  MAINTENANCE.md). Wraps scripts/routing-eval-runner.py in static /
  operator / external mode. Builds when: 25 skills OR first description
  regression slips past skill-audit. Do NOT use for: per-skill recency
  or drift gates (use skill-audit); authoring new prompts (edit
  routing-eval.yaml directly per skill-audit/references/routing-eval-protocol.md);
  evaluating skill *output quality* (out of scope — see USAGE-ANALYTICS.md).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: tool
  tags: [health, weekly]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/eval-suite-format.md`, `references/threshold-rationale.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
            Build trigger had not yet fired (library at 14 skills, no description regression);
            tool ships ahead of trigger to claim the surface area.
---

# skill-evaluate

The Tier 1 tool that mechanizes Health Gate 3 (triggering accuracy)
from `MAINTENANCE.md`. Calls `scripts/routing-eval-runner.py` with the
held-out prompt suite at `scripts/tests/routing-eval.yaml` and reports
per-skill accuracy.

## Purpose

Per `MAINTENANCE.md` §Gate 3 and `coverage.md` §"Domains Deferred",
triggering accuracy was N/A in v0.1.x–v0.4.x because no runner existed.
v0.5.0 ships the runner (`scripts/routing-eval-runner.py`) and this
tool — the procedural wrapper that decides which mode to use, captures
the report, and emits CHANGELOG `Health` entries for any below-threshold
skill.

The build trigger ("library reaches 25 skills OR first regression")
has NOT fired in the meta-pipeline itself (14 skills as of v0.5.0).
The tool ships ahead of trigger so consumer libraries that reach the
threshold have the procedure ready.

## When to Use

- Periodically (recommended weekly per `MAINTENANCE.md` cadence)
  once a real routing layer exists (the static heuristic mode is
  approximate).
- After any description rewrite on a skill (drift-on-description-edit
  is the most common cause of routing regression).
- When `skill-audit` flags a skill but its descriptive content
  looks fine — possibly a routing-side issue, not a content issue.
- Before a release: run as part of `library-audit` to catch
  description regression across the whole library.

## When NOT to Use

- For Gate 1 (recency) or Gate 4 (description drift) — use `skill-audit`.
- For Gate 2 (test pass rate) — that's a separate deferred concern
  (`governance/INTEGRATION-TESTING.md`).
- For authoring routing-eval prompts — edit `routing-eval.yaml`
  directly per `skill-audit/references/routing-eval-protocol.md`.
- For evaluating skill *output* (does the skill produce the right
  answer once it fires?) — that's out of scope for routing accuracy;
  see `governance/USAGE-ANALYTICS.md` for the related concern.

## Stage-Gated Procedure

Five stages.

### Stage 1 — Mode selection

**Consumes:** the operator's prompt; whether a real routing layer is
available.

**Produces:** `eval-mode.yaml` with one of:
- `mode: static` — keyword-overlap heuristic against the SKILL.md
  descriptions. Approximate; useful for regression detection during
  development.
- `mode: operator` — interactive; the operator scores each prompt by
  hand. Suitable for ≤30-prompt suites.
- `mode: external` — the caller invokes a real routing layer
  (LLM-based) and pipes JSON `{prompt, actual}` into stdin.

**Gate:** mode is one of the three; for `external`, the JSON input
schema is documented and the caller is identified.

### Stage 2 — Prompt suite scope

**Consumes:** `eval-mode.yaml` + `scripts/tests/routing-eval.yaml`.

**Produces:** `eval-scope.yaml` listing
- The skills under evaluation
- The prompts per skill (held-out only by default)
- The threshold (default 85% per `MAINTENANCE.md` Gate 3; can be
  overridden for development calibration)

**Gate:** every named skill exists in `SNAPSHOT.lock`; every prompt
has `expected: <skill> | none` set.

### Stage 3 — Run the runner

**Consumes:** the scope.

**Produces:** the output of `scripts/routing-eval-runner.py
--mode <mode> [--threshold <X>]` — per-skill accuracy report.

**Gate:** the script runs to completion (exit 0 or 1); failures are
captured in the report, not lost to script errors.

### Stage 4 — Synthesis

**Consumes:** the runner's per-skill rollup.

**Produces:** `eval-report.md` with
- Headline: "PASS — all skills above threshold" or "FLAGGED — N skills below"
- Per-skill row: accuracy / threshold / pass-fail / sample failures
- Suggested remedies per below-threshold skill (description rewrite,
  anti-trigger update, refactor)

**Gate:** every flagged skill has a named remedy (description
rewrite via `skill-author`, restructure via `skill-refactor`).

### Stage 5 — CHANGELOG entry

**Consumes:** the synthesis.

**Produces:** a `CHANGELOG.md` `Health` entry naming flagged skills,
suitable for the consuming library's next release notes.

**Gate:** the entry references every flagged skill explicitly;
banner blocks for those skills are queued for `skill-author` to
apply on the next description rewrite.

## Dependencies

- `scripts/routing-eval-runner.py` — Stage 3.
- `scripts/tests/routing-eval.yaml` — the prompt suite (must exist;
  starter ships in v0.2.0).
- `MAINTENANCE.md` §Gate 3 + `skill-audit/references/health-gates.md`
  — Gate 3 specification.
- `skill-audit/references/routing-eval-protocol.md` — the held-out vs
  in-distribution discipline.

## Evaluation

`skill-evaluate` is correct when, run against a known-fresh suite:

1. Every prompt is classified (no silent drops).
2. Skills above threshold report ✓; below report ✗.
3. The synthesis names a remedy per flagged skill.
4. The CHANGELOG entry is well-formed.

The static mode is approximate; the first dogfood with a real
routing layer is whenever the build trigger fires (library reaches
25 skills, or a description regression slips past `skill-audit`'s
drift gate).

## Handoffs

- **From `skill-audit` Stage 4** — when the audit reports
  `triggering_accuracy: N/A` and the operator wants real numbers,
  this tool produces them.
- **From `library-audit` Stage 2** — composes Gate 3 alongside Gates
  1 and 4.
- **To `skill-author`** — flagged skills need description rewrites
  (PATCH or MINOR bump, depending on the change).
- **To `skill-refactor`** — when below-threshold skills cluster
  around a sibling boundary, the routing problem is structural.
- **To CHANGELOG `Health`** — flagged-skill entries roll up into the
  next release.
