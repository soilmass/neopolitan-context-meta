---
name: skill-refactor
description: >
  Restructures one or more existing skills when archetype-mixing or
  scope-drift is detected. Performs split, merge, move, or the three-way
  refactor (mechanism / tool / policy) named in ARCHITECTURE.md, through
  five gated stages: diagnosis, plan, execute new skills, retire source +
  redirect, verification. Delegates to skill-author for new skills and to
  skill-retire for source archival. Do NOT use for: authoring brand-new
  skills (use skill-author); authoring a MIGRATION-v<N>.md for an
  already-bumped MAJOR (use skill-migrate); bootstrapping a new domain
  (use family-bootstrap); scaffolding a new library (use library-bootstrap);
  running health checks (use skill-audit); simple archival without
  restructuring (use skill-retire directly).
license: Apache-2.0
metadata:
  version: "0.1.4"
  archetype: tool
  tags: [lifecycle, rare]
  recency_pin: stable
  changelog: |
    v0.1.4 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.1.3 — patch: metadata.recency_pin: stable declared (v0.6.2 wiring).
    v0.1.2 — patch: description anti-triggers extended (A24/A25 from v0.5.2
            dogfood) — `Do NOT use for` block now names skill-migrate
            (MIGRATION-v<N>.md authoring goes there) and library-bootstrap
            (whole-library scaffolding) to prevent the static-routing
            heuristic from firing skill-refactor for migration-guide or
            library-bootstrap prompts.
    v0.1.1 — patch: Stage 2 plan section unified lockfile terminology with
            the rest of the library — affected dependents are listed via
            their `depends_on:` entries in `SNAPSHOT.lock`.
    v0.1.0 — initial. Authored via skill-author 4-stage procedure.
---

# skill-refactor

The lifecycle skill that restructures existing skills. Implements the
three-way refactor and the split/merge/move operations from
`ARCHITECTURE.md` §"Mechanism vs Policy" and §"Composition Principles".

## Purpose

When an existing skill is doing too much, doing the wrong thing, or has
absorbed siblings it shouldn't have, refactor it into a healthier set of
skills. The four refactor types:

- **Split.** One skill becomes two or more, each with a single archetype
  and clean boundaries.
- **Merge.** Two skills with overlapping responsibilities collapse into
  one (rare — usually the right move is to sharpen anti-triggers
  instead).
- **Move.** A capability migrates from one skill to another (e.g.,
  `revert` moves from `git-history-rewriting` to `git-recovery`).
- **Three-way refactor.** A single skill mixing mechanism and policy
  becomes three: a mechanism atom, a tool that orchestrates the
  mechanism for a workflow, and a policy overlay capturing team-specific
  conventions.

Output: new skills authored, source skill retired, dependents updated
lock-step, library snapshot and coverage updated, breaking changes
flagged and handled.

## When to Use

- `skill-audit` flagged a skill for description drift caused by
  archetype mixing.
- The operator notices a skill's purpose has crept ("…and…" between two
  distinct verbs).
- A capability needs to migrate between skills (e.g., as a domain's
  authority docs reorganize).
- Two siblings have become genuinely redundant.
- A skill mixes domain reality with team conventions and needs to be
  pulled apart per `ARCHITECTURE.md` §"Mechanism vs Policy".

## When NOT to Use

- For authoring a brand-new skill — use `skill-author`. Refactor is for
  *existing* structure, not greenfield.
- For just adding capabilities to an existing skill — that's a MINOR
  bump, authored as an in-place edit (no skill change).
- For *just* archiving — use `skill-retire` directly. Refactor includes
  retirement of the source as Stage 4, but if no new skills are being
  authored, the operation is retire-only.
- For renaming a skill — that's a MAJOR-version-bump edit handled
  through `skill-author` semantics + dependent updates. Refactor is
  about *structure*, not *labels*.

## Stage-Gated Procedure

Five heavyweight stages. Each stage produces a named artifact gated by
a verifiable check. Detail in `references/three-way-refactor.md` and
`references/archetype-mixing-signals.md`.

### Stage 1 — Diagnosis

**Consumes:** the target skill's SKILL.md and the three diagnostic
tests from `ARCHITECTURE.md` §"Mechanism vs Policy".

**Produces:** `diagnosis.md` containing
- The refactor type (one of: split, merge, move, three-way).
- Which diagnostic tests failed (and which passed).
- The proposed new structure: list of new skills with their archetypes
  and one-line purposes.
- The boundary lines — for each capability of the source skill, which
  new skill it lands in.

**Gate:** refactor type is one of the four; every proposed new skill
has a named archetype; every capability of the source skill is assigned
to exactly one destination.

### Stage 2 — Plan

**Consumes:** `diagnosis.md` + the sibling map from `SNAPSHOT.lock`.

**Produces:** `refactor-plan.md` containing
- Capabilities split-tagged: each cap labeled with its destination new
  skill.
- A redirect mapping: what the source skill's `description` will say
  after retirement (pointing at the new skills).
- Affected dependents: every router that dispatches to the source skill;
  every skill that lists the source under `depends_on:` in
  `SNAPSHOT.lock`; every `coverage.md` that references it.
- The version implication: this is always MAJOR for the source skill
  (capabilities are being removed). Each new skill starts at `0.1.0`
  (or `1.0.0` if the operator is confident).

**Gate:** every original capability maps to exactly one destination
(no capability dropped silently). Every dependent is named (catches
lock-step coordination problems before Stage 3).

### Stage 3 — Execute new skills

**Consumes:** `refactor-plan.md`.

**Produces:** new SKILL.md files for each destination skill.

For each new skill: invoke `skill-author` with a pre-filled
`intake.yaml` derived from the refactor plan. `skill-author` walks its
own 4 stages; this stage doesn't pass until each delegated invocation
passes.

**Gate:** every new SKILL.md passes `validate-metadata.py`.

### Stage 4 — Retire source + redirect

**Consumes:** `refactor-plan.md` + the new skills from Stage 3.

**Produces:**
- The source skill marked retired via `skill-retire` (delegates).
- The source skill's `description` rewritten as a redirect note naming
  the new skills.
- The family `coverage.md` updated: source moves to "Retired"; new
  skills appear in "In Scope".
- Dependents updated lock-step:
  - Routers that dispatched to the source now dispatch to one of the
    new skills (depending on which capability the routing entry was
    about — the capability-mapping from Stage 2 drives this).
  - Lockfiles that pinned the source now pin one of the new skills.
- The library `CHANGELOG.md` gets a single coordinated entry under
  "Breaking" naming the source skill, the new skills, and the
  migration guide path.
- A migration guide is authored at the source skill's path
  (`MIGRATION-v<NEW>.md`) per `VERSIONING-POLICY.md` §"Migration
  Guides".

**Gate:** `detect-breaking-changes.py` exits with code 2 (breaking
detected with proper handling). The lock-step PR includes every
dependent identified in Stage 2.

### Stage 5 — Verification

**Consumes:** the post-refactor library state.

**Produces:** `refactor-verification.md` containing
- A capability-coverage check: for every capability of the original
  source, confirm it's reachable through one of the new skills.
- An audit-ritual run (per `skill-author` references/audit-ritual.md)
  across the new skills + their siblings + any rerouted dependents.
- A `validate-metadata.py --all` run against the post-refactor
  library — full pass required.

**Gate:** every original capability is reachable. Audit ritual passes
(no orphan contentions). `validate-metadata.py --all` exits 0.

## Dependencies

- `skill-author` (invoked in Stage 3 — heavily, once per new skill).
- `skill-retire` (invoked in Stage 4 — once for the source).
- `scripts/validate-metadata.py` (Stage 3 gate, Stage 5 gate).
- `scripts/detect-breaking-changes.py` (Stage 4 gate).
- `SNAPSHOT.lock` (read in Stage 2, updated in Stage 4 via skill-author
  and skill-retire).
- `coverage.md` per affected family + library-root (updated in Stage 4).

## Evaluation

`skill-refactor` is correct when, run against five contrived refactor
scenarios (one per refactor type plus an edge case):

1. **Split** — one atom mixing two capabilities → two atoms, each clean.
   Original capabilities all routable through the new skills.
2. **Merge** — two siblings with overlap → one skill. No capability
   lost.
3. **Move** — a capability migrates from atom A to atom B. Original
   atom A's other capabilities preserved; atom B gains the new
   capability; routers updated.
4. **Three-way** — one tool mixing mechanism and policy → mechanism
   atom + tool + policy overlay. Each independently maintainable.
5. **Adversarial** — an attempted refactor that *should fail* the
   Stage 1 gate (e.g., the operator proposes a split that would drop a
   capability silently). The skill must halt and surface the gap.

For each scenario, the verification stage produces a clean audit and
no breaking changes are silently introduced.

## Handoffs

- **From `skill-audit`** — flagged skills with archetype-mixing
  drift are candidates for refactor.
- **From the operator** — direct invocation when an "…and…" purpose is
  observed.
- **To `skill-author`** — Stage 3 invokes once per new skill.
- **To `skill-retire`** — Stage 4 invokes once for the source.
- **To downstream router maintainers** — Stage 4 includes lock-step
  router updates as part of the same PR.
- **From `family-bootstrap` Stage 5** (rare) — when the audit ritual
  during weaving finds the proposed family overlaps with an existing
  skill that itself needs refactoring before the family can land.

## Edge Cases

- **The source skill has no dependents.** Skip the lock-step coordination
  in Stage 4 — just retire and redirect.
- **The source skill has many dependents (>5 routers).** Stage 4 may
  exceed a reasonable PR size. Split into a sequence of PRs: the
  refactor itself in PR 1; the dependent updates over PRs 2..N. Each PR
  bumps the source skill's version with `archived: true` only after the
  last dependent migrates.
- **The refactor plan would create a skill with no clear archetype.**
  Stage 1 gate fails; reconsider the structure.
- **Two refactor types apply** (e.g., split AND move). Sequence them:
  do the move first, then the split, as separate `skill-refactor`
  invocations. Don't try to combine in one diagnosis.
- **The operator wants to refactor one of the lifecycle skills**
  (`skill-author`, etc.). The refactor applies recursively; the audit
  ritual must check the new structure against the *other* lifecycle
  skills explicitly. The risk: a refactor of `skill-author` that
  introduces routing competition with `family-bootstrap` is hard to
  catch from inside.

## Self-Audit

Before invoking `skill-refactor`, confirm:
- The target skill is genuinely failing the diagnostic tests in
  `ARCHITECTURE.md` §"Mechanism vs Policy" (don't refactor for cosmetic
  preference).
- The proposed new skills' names are available (no collision).
- A migration guide template is at hand (`VERSIONING-POLICY.md`
  §"Migration Guides").
- The library is currently healthy (run `skill-audit` first; refactor
  on a flagged-but-not-target skill produces unstable rollouts).
