---
name: skill-audit
description: >
  Runs the four health-gates from MAINTENANCE.md (recency, test pass rate,
  triggering accuracy, description drift) against one or more existing
  skills, through five gated stages: scope selection, recency scan, drift
  scan, test-pass-rate & triggering-accuracy probes, and synthesis & banner
  emit. Produces a per-skill rollup, banner blocks for failing skills, and
  a CHANGELOG Health entry. Do NOT use for: library-shape health (coverage.md
  alignment, snapshot integrity — use library-audit); authoring new skills
  (use skill-author); bootstrapping families (use family-bootstrap);
  refactoring archetype mixes (use skill-refactor); archiving (use
  skill-retire); routing-accuracy probing in isolation (use skill-evaluate).
license: Apache-2.0
metadata:
  version: "0.2.4"
  archetype: tool
  tags: [lifecycle, health, weekly]
  recency_pin: stable
  changelog: |
    v0.2.4 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.2.3 — patch: metadata.recency_pin: stable declared (v0.6.2 wiring).
    v0.2.2 — patch: description anti-triggers extended (A24/A25 from v0.5.2
            dogfood) — `Do NOT use for` block now names library-audit and
            skill-evaluate explicitly to prevent routing contention with the
            v0.5.0 cluster (library-shape audits go to library-audit; routing-
            accuracy probing goes to skill-evaluate).
    v0.2.1 — patch: Stage 4b text updated to reflect that the routing-eval
            YAML now exists as a starter set; what's deferred is the runner,
            not the file. audit-skill.py reports "suite present but runner
            deferred" for triggering-accuracy, captured in the SKILL.md.
    v0.2.0 — minor: Gates 1 + 4 mechanized via scripts/audit-skill.py.
            Drift formula corrected from Jaccard (always too eager) to
            asymmetric containment with prefix-based token matching.
            Dependencies and Self-Audit updated to point at the new script.
    v0.1.1 — patch: renamed Stage 4 to "Test-pass-rate & triggering-accuracy probes"
            so the description and stage prose agree; pinned the Gate 4 drift
            formula in references/health-gates.md.
    v0.1.0 — initial. Authored via skill-author 4-stage procedure.
---

# skill-audit

The lifecycle skill that health-checks existing skills. Implements the
four-gate maintenance discipline from `MAINTENANCE.md`.

## Purpose

Apply the four health gates — **recency**, **test pass rate**, **triggering
accuracy**, **description drift** — to one or more existing skills, and
produce:

- A per-skill rollup naming each gate's pass/fail status.
- A banner block (per `MAINTENANCE.md` §"Auto-Warn Mechanism") for any
  failing skill, suitable for prepending to the skill's description.
- A `CHANGELOG.md` "Health" entry summarizing flagged skills.

The audit does *not* fix anything. It surfaces health state. Fixes are
authored via `skill-author` (description rewrites, version bumps),
`skill-refactor` (archetype splits), or human-authored PRs.

## When to Use

- On a schedule (recommended weekly for the routing-accuracy gate;
  monthly for full audit).
- After a `skill-author` Stage 4 completes — confirms the new skill
  meets all four gates immediately.
- After a `skill-refactor` Stage 5 completes — confirms the post-
  refactor library is healthy.
- When investigating a specific skill ("why is X being mis-routed?").

## When NOT to Use

- For authoring or modifying skills — `skill-audit` is read-only on
  SKILL.md content. Modifications go through `skill-author` or
  `skill-refactor`.
- For deciding whether to retire a skill — that decision is human.
  `skill-audit` flags health failures; the operator decides whether
  to fix or retire.
- For testing a skill's behavior end-to-end. The "test pass rate" gate
  in v0.1.0 is marked N/A — no SKILL.md test infrastructure exists yet
  (see Stage 4 below).

## Stage-Gated Procedure

Five heavyweight stages. Detail in `references/health-gates.md` and
`references/routing-eval-protocol.md`.

### Stage 1 — Scope selection

**Consumes:** the operator's prompt (e.g., "audit the whole library",
"audit skill-author", "audit the git family") and `SNAPSHOT.lock`.

**Produces:** `audit-scope.yaml` listing the skills to audit, by name.

**Gate:** scope is non-empty; every named skill exists in the snapshot
(catches typos before the audit runs).

### Stage 2 — Recency scan

**Consumes:** `audit-scope.yaml` + `git log` per skill directory.

**Produces:** `recency-report.json` per skill:
- `last_touched`: most recent commit date affecting the skill's directory
- `gate_pass`: true if `last_touched` is within 6 months
- `pinned_stable`: true if the skill's `metadata` declares `recency_pin: stable`
  (acknowledged-as-complete; passes the gate even if older)

**Gate:** every skill in scope has either a `last_touched` date OR a
`pinned_stable: true` marker. No skills with missing dates.

### Stage 3 — Description drift scan

**Consumes:** each skill's SKILL.md.

**Produces:** `drift-report.json` per skill:
- `description_capabilities`: list of capability-like phrases extracted
  from the description
- `body_capabilities`: list of capability names from `## Capabilities
  Owned` (atoms) or `## Routing Table` (routers) or stage names (tools/
  orchestrators)
- `gap_percent`: 1 - (intersection / union); how far the description
  drifts from the body
- `gate_pass`: true if `gap_percent` ≤ 10%

**Gate:** drift report produced for every skill in scope. Skills above
10% are flagged; specific drift lines are surfaced with line numbers
in the SKILL.md body.

### Stage 4 — Test-pass-rate & triggering-accuracy probes

This stage covers the two `MAINTENANCE.md` gates that depend on
infrastructure deferred in v0.1.0. Both are run together because their
inputs (an eval suite, a test suite) are external to the SKILL.md and are
either both present or — in v0.1.0 — both absent. Either way, the audit
records explicit N/A rather than silently skipping. Splitting into two
stages becomes worthwhile once at least one input exists.

**4a — Test pass rate (Gate 2 in MAINTENANCE.md).**

Consumes: each skill's evaluation suite output. Deferred in v0.1.0 — no
SKILL.md test infrastructure exists. The audit records
`test_pass_rate: "N/A — INTEGRATION-TESTING.md deferred per
governance/INDEX.md"`.

Build trigger to reactivate: see `governance/INDEX.md` §`INTEGRATION-TESTING.md`.

**4b — Triggering accuracy (Gate 3 in MAINTENANCE.md).**

Consumes: held-out routing-eval prompts from a YAML at
`scripts/tests/routing-eval.yaml`. A starter set of ~30 prompts ships in
v0.2.0; the format is locked, but the routing-layer *runner* that scores
prompts against the live skill descriptions is deferred per `coverage.md`
build trigger for `skill-evaluate` ("library reaches 25 skills OR first
description-change regression").

Produces `routing-report.json` per skill:
- If eval suite **and runner** exist: `accuracy` (% of held-out prompts
  where the skill fires when expected); `gate_pass: accuracy >= 85%`.
- If suite exists but runner is deferred: `gate_pass: "N/A"` with
  `reason: "eval suite present but runner deferred"` — what
  `audit-skill.py` reports today.
- If no suite: `gate_pass: "N/A"` with `reason: "no routing eval
  suite — see coverage.md Deferred section for skill-evaluate"`.

In v0.2.0 this sub-gate reports the second case (suite-without-runner)
for every skill.

**Gate:** every skill has either a real number or an explicit N/A *for
each of the two sub-gates*. Silent gate-skips are not allowed.

### Stage 5 — Synthesis & banner emit

**Consumes:** all reports from Stages 2-4.

**Produces:**
- `audit-report.md` — per-skill rollup. Each skill gets a row showing
  the four gates' status: ✓ / ✗ / N/A.
- For each failing skill: a banner block (matching the format in
  `MAINTENANCE.md` §"Auto-Warn Mechanism") suitable for prepending to
  that skill's description on its next release.
- A suggested entry for `CHANGELOG.md` under "Health" listing every
  flagged skill and which gate(s) failed.

**Gate:** rollup written; every skill in scope appears; every failing
gate has a banner emitted; CHANGELOG suggestion drafted.

## Dependencies

- `SNAPSHOT.lock` (read in Stage 1).
- Each skill's `SKILL.md` (read in Stage 3).
- `git log` (read in Stage 2; via subprocess. `scripts/audit-skill.py`
  shells out to git directly).
- `scripts/tests/routing-eval.yaml` (read in Stage 4 if present;
  starter set ships in v0.2.0; full eval suite remains deferred per
  library-root `coverage.md`).
- `scripts/audit-skill.py` (v0.2.0+) — mechanizes Gates 1 + 4.
- `references/health-gates.md` and `references/routing-eval-protocol.md`.

This skill does NOT invoke `validate-metadata.py` directly — that
script is a structural check at authoring time, not a health check.

## Evaluation

`skill-audit` is correct when, run against a known-fresh library where
every skill was authored within the last 30 days:

1. Every skill passes the recency gate.
2. Every skill passes the drift gate (the authoring procedure should
   have produced descriptions that match bodies).
3. Every skill records an explicit N/A for triggering accuracy and
   test pass rate (until those gates are implementable).
4. The synthesis emits no banners.
5. The CHANGELOG "Health" suggestion is empty (or notes "no flags").

The first dogfood run is Phase 5 of the v0.1.0 plan: this audit is run
against the five lifecycle skills. They should all pass cleanly.

## Handoffs

- **From `skill-author` Stage 4** (optional verification step): can be
  invoked to confirm a newly-authored skill passes all gates.
- **From `family-bootstrap` Stage 6** (optional verification step): can
  be invoked to confirm a newly-bootstrapped family is healthy.
- **To the operator:** the audit-report.md is read by humans; banners
  are applied to descriptions by humans (no auto-edit).
- **To `skill-author`** (later): when a flagged skill needs a description
  rewrite, that's a `skill-author`-style edit (with `metadata.version`
  bumped to PATCH or MINOR per `VERSIONING-POLICY.md`).
- **To `skill-refactor`**: when the drift gate fails because the skill
  is mixing archetypes (description claims router-like dispatch but body
  is an atom), the fix is a refactor.
- **To `skill-retire`**: when a skill repeatedly fails health gates and
  no one is maintaining it, the operator may invoke `skill-retire`.

## Edge Cases

- **Skill exists in the directory but not in `SNAPSHOT.lock`**. Stage 1
  flags this as an inconsistency: either the snapshot needs updating
  (run the operator workflow) or the skill is orphaned. Halt with a
  specific error.
- **A skill with no commits yet** (just authored, not yet committed).
  Stage 2 records `last_touched: null` and treats it as a gate pass
  with reason `freshly_authored: true` (the timestamp is the working
  tree mtime).
- **A skill whose description was rewritten >30% in the last commit**
  (recency-gate-passing but drift-gate-suspect). The audit still runs
  Stage 3 normally; if drift fails, the banner appears.
- **The library has no `SNAPSHOT.lock` yet**. Stage 1 emits an error
  pointing to `family-bootstrap` Stage 6 or hand-authoring.
- **Triggering accuracy probe finds zero held-out prompts for a skill**
  (the eval suite has been started but lacks coverage for this skill).
  Stage 4 records `gate_pass: "N/A"` with `reason: "no eval coverage
  for this skill"` — never silent.

## Self-Audit

Before running `skill-audit` for the first time on the library, confirm:
- `SNAPSHOT.lock` exists and parses as YAML.
- `git log` works in the plugin directory (the audit shells out to git;
  if no git repo, Stage 2 falls back to working-tree mtime per the
  Stage 2 edge-case in this SKILL.md).
- `python3` and PyYAML are on PATH; v0.2.0+ runs Gates 1 + 4 via
  `scripts/audit-skill.py` rather than purely by hand. Run
  `python3 scripts/audit-skill.py --all` for a one-shot health check.
- For Gates 2 + 3 (deferred), the operator records explicit N/A —
  the script does this automatically.

As of v0.2.0, `scripts/audit-skill.py` mechanizes Gates 1 (recency via
`git log`) and 4 (drift via the asymmetric containment formula in
`references/health-gates.md`). Stages 2 and 3 of this skill are now a
script call. Gates 2 and 3 remain explicit N/A — both depend on the
deferred infrastructure named in `governance/INDEX.md`
(INTEGRATION-TESTING.md) and library-root `coverage.md` (skill-evaluate).
The script also reports "eval suite present but no runner" when
`scripts/tests/routing-eval.yaml` exists but the routing layer is
deferred.
