# Contributing

This plugin is the meta-pipeline that authors / audits / refactors / retires
*other* skills. Contributions to it are themselves lifecycle operations.
Rather than re-explaining the architecture, this guide tells you which
existing tool to use for which contribution shape, and what's expected
before you ship.

## Before you start

Read these in order if you're new:

1. `README.md` — entry point and library map.
2. `ARCHITECTURE.md` — five archetypes, layering, naming, tier model.
3. `governance/INDEX.md` — operational layer map.
4. The two operational governance docs you'll touch most:
   - `governance/METADATA-VALIDATION.md` (what every SKILL.md must satisfy)
   - `governance/BREAKING-CHANGE-DETECTION.md` (what counts as breaking)

## Common contribution shapes

| You want to... | Use this skill | Then verify with |
|---|---|---|
| Add a single new skill (atom / tool / router / policy) | `skill-author` (4 stages) | `make validate` |
| Add a whole new domain family | `family-bootstrap` (6 stages) | `make verify` |
| Health-check the library | `skill-audit` (5 stages) | `make audit` |
| Restructure a skill that's mixing archetypes | `skill-refactor` (5 stages) | `make verify` |
| Archive a skill | `skill-retire` (4 stages) | `make verify` |
| Fix a typo / clarify prose without changing meaning | Edit directly; PATCH bump | `make verify` |
| Bump a skill's MAJOR for breaking changes | Edit + migration guide; coordinate dependents | `scripts/detect-breaking-changes.py` |

If your contribution doesn't fit into these shapes, it probably falls
into one of the deferred concerns named in `governance/INDEX.md` or
`coverage.md` §"Domains Deferred". Read those before authoring something
new.

## Pre-flight checks

Before opening a PR, run from the plugin root:

```bash
make verify        # validators + fixtures + audit + version triangulation
make lint          # ruff over scripts/ (optional but recommended)
make typecheck     # mypy --strict over scripts/ (optional)
```

`make verify` exiting 0 is the merge gate. Lint and typecheck failures
are not blocking but should be addressed in the same PR if they touch
code you're modifying.

## What every PR needs

Per `GOVERNANCE.md` §"Adding a New Skill":

1. Skill passes metadata validation (`scripts/validate-metadata.py`).
2. Archetype is named in `metadata.archetype` (and the skill's filesystem
   location matches).
3. If adding to an existing family, the family's `coverage.md` is updated.
4. Library `SNAPSHOT.lock` is updated (per-skill version, archetype,
   path, health, and `depends_on:` if applicable).
5. `CHANGELOG.md` has a new entry under today's date.
6. Routers that should dispatch to the new skill are updated.
7. The audit ritual has been run against existing siblings and any
   anti-trigger updates are queued in the same PR.

The lifecycle skills mechanize most of this. Skip them only if you're
genuinely outside the supported contribution shapes.

## What counts as breaking

See `governance/BREAKING-CHANGE-DETECTION.md`. Short version:

- Removing a required section: breaking.
- Renaming the `name` field: breaking.
- Removing or moving a capability from an atom: breaking.
- Changing or removing a routing-table entry from a router: breaking.
- Changing the description by >30% character count: flagged for review.

Breaking changes require a MAJOR bump, a migration guide at
`<skill-dir>/MIGRATION-v<NEW>.md`, and lock-step updates to every
dependent named in `SNAPSHOT.lock` `depends_on:`. The detector
(`scripts/detect-breaking-changes.py`) blocks merge if any of these
are missing.

## Versioning

`VERSIONING-POLICY.md` is the source of truth. Quick rules:

- **PATCH** (X.Y.Z): typo fixes, clarifications, reference reorganization.
- **MINOR** (X.Y.0): new capability added, new section, new optional
  frontmatter field — without breaking dependents.
- **MAJOR** (X.0.0): any change the breaking-change detector flags as
  breaking.

The library snapshot (`SNAPSHOT.lock` `snapshot_version`) bumps with
the *largest* per-skill bump in a release. A coordinated MAJOR for
one skill is a MAJOR snapshot bump.

## Health-check expectations

`MAINTENANCE.md` defines four gates; v0.2.x mechanizes Gates 1 (recency
via `git log`) and 4 (description drift). Run `make audit` to see your
contribution's standing. Drift gates above 10% mean the skill's
description claims things its body doesn't deliver — fix the description
or extend the body before shipping.

## What's deferred

If you're tempted to add infrastructure that doesn't exist yet
(SECURITY-AUDIT.md, INTEGRATION-TESTING.md, the routing-eval runner,
etc.) — first check `governance/INDEX.md` and `coverage.md` for whether
the build trigger has fired. Premature standardization is worse than
no procedure; the deferred-with-trigger discipline exists to enforce
that.

If a build trigger has fired but the deferred document hasn't been
authored yet, that's a contribution shape worth taking on. Open an
issue first to discuss scope.

---

## 30-minute onboarding ramp

If you're picking this codebase up cold, here's the fastest path to
productive contribution.

### Minute 0–5: orient

1. `ls` the plugin root. Notice: `skills/` (14 SKILL.md), `scripts/`
   (11 Python scripts), `governance/` (10 docs + an INDEX), one
   plugin manifest, four versioned ledgers (`SNAPSHOT.lock`,
   `CHANGELOG.md`, `coverage.md`, `governance/INDEX.md`).
2. Run `make verify`. Watch the six-step output (validators,
   fixtures, audit, version triangulation, coverage-check,
   snapshot-diff sanity). Confirm exit 0.

### Minute 5–15: read the architecture

1. `README.md` — Library Map + Where to Start.
2. `ARCHITECTURE.md` — five archetypes (Atom, Tool, Router,
   Orchestrator, Policy), tier model (6–9 / 4–7 / 2–5),
   read/write separation, mechanism vs policy. Skip §"Open
   Questions" first read; come back later.
3. `governance/INDEX.md` — what governance docs exist, what's
   pre-trigger N/A.

### Minute 15–25: trace a lifecycle skill

Pick one of the 14 skills (e.g., `skill-author/SKILL.md`).
Read top-to-bottom. Notice the structure:

- frontmatter (`name`, `description` with anti-trigger block,
  `metadata.version`, `metadata.archetype`, `metadata.changelog`)
- Required sections per archetype (e.g., for tools: Purpose,
  When to Use, When NOT to Use, Stage-Gated Procedure,
  Dependencies, Evaluation, Handoffs)
- Per-stage gate definitions (Consumes / Produces / Gate)
- References under `references/`

Cross-reference what you read against
`governance/METADATA-VALIDATION.md` to see how the validator
enforces the structure.

### Minute 25–30: pick a contribution

Match your contribution to the table at the top of this document.
If your contribution doesn't fit, check `coverage.md` Domains
Deferred and `governance/INDEX.md` Deferred — the gap may be
named there with a build trigger you can verify against.

### After the 30 minutes

Run `make help` for the full target list. Look at recent
`CHANGELOG.md` entries to see what shipped recently and how the
ledger is structured. The git log + the four versioned ledgers
*are* the audit trail; learn to read them.

Recommended first contribution shapes for new contributors:

- **Doc fix** (typo / clarification) — PATCH bump, no migration
  guide, low review burden. Good ramp for getting your first PR
  merged.
- **Anti-trigger update on a sibling** — if the audit ritual
  surfaced contention you've experienced. Run the ritual per
  `skills/skill-author/references/audit-ritual.md`; submit the
  proposed anti-trigger as a PR against the affected sibling.
- **A new fixture** under `scripts/tests/fixtures/` exercising a
  validator path that's not yet covered. Read the existing
  fixtures first.

Avoid these for first contributions:

- Authoring a new lifecycle skill (heavy review burden; coordinate
  with maintainers via an issue first).
- Bumping a MAJOR version on an existing skill (lock-step, migration
  guide, coordination — not a first-PR scope).
- Modifying the validators themselves (tight invariants; audit
  the four scripts' triple-consistency before changing).
