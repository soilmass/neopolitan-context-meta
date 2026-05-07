---
name: library-audit
description: >
  Library-shape health check: composes audit-skill (per-skill gates),
  coverage-check (coverage.md schema), verify.sh (version triangulation),
  and snapshot integrity (depends_on resolves, no cycles) into a single
  procedure. Operates on the library as a whole, not on one skill. Do NOT
  use for: per-skill health (use skill-audit); authoring new skills (use
  skill-author); diffing snapshots for release notes (use skill-snapshot-diff);
  retiring or refactoring (use skill-retire / skill-refactor).
license: Apache-2.0
metadata:
  version: "0.1.2"
  archetype: tool
  tags: [health, weekly]
  changelog: |
    v0.1.2 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.1.1 — patch: Stage 4 snapshot-integrity gate gained an explicit
            "pinned-version semantics" paragraph (A27): a `depends_on:`
            entry is a floor plus same-MAJOR compatibility window, not a
            strict equality. Added supporting references/library-gates.md
            (Gates L1-L4) and references/rollup-template.md (A28/A29).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
---

# library-audit

Library-shape health check. Per-skill health is `skill-audit`'s job;
this tool answers a different question: "is the library, as a whole,
internally consistent?"

## Purpose

Surface inconsistencies that span multiple skills:
- coverage.md format compliance (six required sections; non-empty Out
  of Scope; tier-transition log).
- SNAPSHOT.lock integrity: every recorded skill exists; every
  `depends_on` pin resolves; no cycles in the dependency graph.
- Version triangulation: plugin.json, marketplace.json, SNAPSHOT.lock
  all agree.
- Cross-skill consistency: every skill's archetype in SNAPSHOT.lock
  matches the SKILL.md frontmatter; every router's `Atoms in This
  Family` resolves (or is documented as deferred).

The output is a per-library rollup; failures point at the right
remedy (skill-author for adding, skill-refactor for boundary fixes,
skill-retire for archival, manual edit for ledger drift).

## When to Use

- Periodically (recommended monthly per MAINTENANCE.md cadence) as
  part of routine library health.
- Immediately after a release (Phase H of any version bump).
- When investigating a library-wide regression.
- Before a major version bump on the snapshot itself
  (snapshot_version 0.X → 1.0).

## When NOT to Use

- For per-skill health gates (recency / drift / etc.) — use `skill-audit`.
- For authoring or modifying a skill — use `skill-author` /
  `skill-refactor`.
- For diffing two snapshots — use `skill-snapshot-diff`.
- For finding routing-accuracy issues — use `skill-evaluate` (deferred
  in v0.5.x without a real routing layer).
- For one-off "is my SKILL.md valid?" — use `validate-metadata.py`
  directly.

## Stage-Gated Procedure

Five lightweight stages.

### Stage 1 — Scope selection

**Consumes:** the operator's prompt and the library root path.

**Produces:** `library-audit-scope.yaml` with
- `root` — the plugin root (default: cwd)
- `include_fixtures` — whether to also audit `scripts/tests/fixtures/`
  (default: false; fixtures are intentionally broken)

**Gate:** root contains `SNAPSHOT.lock`, `coverage.md`,
`.claude-plugin/plugin.json`, and a `skills/` directory.

### Stage 2 — Per-skill audit (delegated)

**Consumes:** the scope + every skill in `SNAPSHOT.lock`.

**Produces:** `audit-skill.py --all --root <root>` output. Recency +
drift gates run; test-pass-rate and triggering-accuracy report N/A
in v0.5.x.

**Gate:** the script exits 0 (all skills pass implementable gates) OR
the operator acknowledges the flagged skills and decides to fix
(handoff to skill-author / skill-refactor) or retire (handoff to
skill-retire) before proceeding.

### Stage 3 — Coverage schema check (delegated)

**Consumes:** `coverage.md` at the library root.

**Produces:** `coverage-check.py --file coverage.md` output.

**Gate:** the script exits 0; six required sections present; Out of
Scope non-empty.

### Stage 4 — Snapshot integrity

**Consumes:** `SNAPSHOT.lock`.

**Produces:** the output of `dependency-graph.py --format json`,
plus a check that:
- every recorded skill has an existing `path:` (the SKILL.md file
  actually exists)
- every `depends_on:` pin resolves to an existing skill at the
  pinned version that the dependent declares
- no cycles exist in the depends_on graph

**Pinned-version semantics (clarified A27, v0.5.2):** a `depends_on:`
entry of the form `<skill-name>@<version>` is satisfied when the
target skill's *current* `metadata.version` in its SKILL.md is
**greater than or equal to** the pinned version, AND no MAJOR-bump
boundary has been crossed since the pin (i.e., the leading SemVer
segment matches). The pin is a floor + compatibility window, not a
strict equality. A pin of `skill-author@0.1.0` is satisfied by
`skill-author` at 0.1.4 but is *not* satisfied by 0.2.0 (MINOR is
backward-compatible per VERSIONING-POLICY.md, so this script could
relax later — but at v0.5.2 the audit treats MINOR jumps as a
warning, not a fail, until a real consumer dogfood validates that
relaxation).

**Gate:** the three checks pass; warnings (MINOR jump from pinned
version) are surfaced in the rollup but do not flip exit code.

### Stage 5 — Synthesis

**Consumes:** all reports from Stages 2-4.

**Produces:** `library-audit-report.md` with:
- one-line headline (PASS / FLAGGED with N issues)
- per-stage rollup
- recommended remedies per flagged item, naming the right skill
  (skill-author / skill-refactor / skill-retire / skill-snapshot-diff
  / manual edit)
- suggested CHANGELOG `Health` entry if anything is flagged

**Gate:** report written; every flagged item has a named remedy; the
operator decides whether to act now or defer to the next health-check
cycle.

## Dependencies

- `scripts/audit-skill.py` — Stage 2.
- `scripts/coverage-check.py` — Stage 3.
- `scripts/dependency-graph.py` — Stage 4.
- `scripts/validate-metadata.py` — used inside `audit-skill.py`.
- `verify.sh` — composes the same checks for CI; this skill is the
  procedural rollup that interprets results and decides remedies.

## Evaluation

`library-audit` is correct when, run against a known-fresh library,
all five stages pass and Stage 5 emits a "PASS — no flagged items"
synthesis. Run against a library with one synthetic regression
(e.g., a stale `depends_on:` pin), the report flags exactly that
issue with the right remedy named.

The first dogfood is `make verify` itself plus this tool's
description-tightening pass — the procedure that runs after any
substantive library change.

## Handoffs

- **From periodic health-check cadence** — recommended monthly run.
- **To `skill-author`** — when audit flags missing required sections
  or stale anti-triggers.
- **To `skill-refactor`** — when audit flags archetype-mixing drift
  spanning multiple skills.
- **To `skill-retire`** — when audit flags ≥12-month health failures
  with no maintainer.
- **To `skill-snapshot-diff`** — when the audit output forms part of
  a release note.
