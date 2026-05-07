---
name: skill-retire
description: >
  Archives an existing skill with a redirect note, updates the family
  coverage.md, removes the skill from SNAPSHOT.lock, and emits a
  CHANGELOG entry — through four gated stages: justification, dependent
  check, archive & redirect, snapshot & coverage update. The SKILL.md
  remains in git history and remains pinnable. Do NOT use for: authoring
  new skills (use skill-author); bootstrapping families or libraries (use
  family-bootstrap / library-bootstrap); running health checks (use
  skill-audit); restructuring without retirement (use skill-refactor);
  rolling back a single broken release of a skill that's still canonical
  (use rollback-skill.py — retirement is permanent within a snapshot,
  rollback is reversible).
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
            dogfood) — `Do NOT use for` block now names library-bootstrap
            (whole-library scaffolding is bootstrap, not retirement) and
            rollback-skill.py (rolling back a single broken release of a
            still-canonical skill is reversible; retirement is permanent).
    v0.1.1 — patch: Stage 2 dependent-check terminology unified — replaced
            speculative `metadata.lockfile` reference with the actually-
            implemented `SNAPSHOT.lock depends_on:` mechanism.
    v0.1.0 — initial. Authored via skill-author 4-stage procedure.
---

# skill-retire

The lifecycle skill that archives a skill. Implements `GOVERNANCE.md`
§"Removing a Skill" — the SKILL.md remains in git history; the snapshot
stops listing it as canonical; users with explicit pins continue to get
it; everyone else stops seeing it.

## Purpose

Take a skill out of the canonical library without deleting it. After
retirement:

- The skill's SKILL.md remains in git history and remains pinnable.
- `SNAPSHOT.lock` no longer lists the skill as canonical.
- The family's `coverage.md` moves the skill to a "Retired" section.
- A redirect note is prepended to the SKILL.md naming the replacement
  (or explicitly stating no replacement exists, with rationale).
- The library `CHANGELOG.md` gets a `Removed` or `Deprecated` entry.

What this skill does not do:
- Delete files. Per `GOVERNANCE.md`: "The library does not delete skills.
  Deletion creates surprises for pinned users."
- Decide *whether* to retire. The decision is upstream — `skill-audit`
  flags problems; `skill-refactor` decides to redraw boundaries; the
  operator decides to retire. This skill enforces the procedure.

## When to Use

- A skill has been absorbed into a more comprehensive sibling
  (refactor outcome — `skill-refactor` Stage 4 invokes this).
- A skill has been replaced by a newer skill with the same scope; the
  old one is deprecated.
- A skill's domain stopped existing (rare, but possible — e.g., a tool
  that wraps a deprecated external API).
- A skill has been failing health gates for ≥12 months and no one is
  maintaining it (the operator decides retirement is cleaner than
  unmaintained-with-a-banner).

## When NOT to Use

- For *deleting* files. The library does not delete skills.
- For renaming a skill. A rename is a MAJOR-version-bump edit through
  `skill-author` semantics + dependent updates, not a retirement.
- For temporarily disabling a skill. Disabling is a per-operator
  setting, not a library operation.
- As a substitute for fixing health failures. If a skill is failing
  gates because the operator can fix it, fix it; retire only when no
  one will.

## Stage-Gated Procedure

Four heavyweight stages.

### Stage 1 — Justification

**Consumes:** the operator's prompt (or `skill-refactor` Stage 4's
invocation) plus the target skill's SKILL.md.

**Produces:** `retirement-justification.md` containing
- The reason, exactly one of:
  1. **Absorbed** — the skill was merged into a sibling. Names the
     absorbing sibling.
  2. **Replaced** — a new skill supersedes this one. Names the
     replacement skill.
  3. **Domain-gone** — the underlying domain stopped existing. Cites
     the deprecation announcement.
  4. **Health-failure** — the skill has been failing gates for ≥12
     months without maintenance. Cites the audit reports.
- A one-paragraph rationale.
- A pointer (URL or skill name) for users who hit the retired skill —
  where should they go instead?

**Gate:** the reason is exactly one of the four; if "replaced" or
"absorbed," the named replacement/absorbing skill exists in
`SNAPSHOT.lock`.

### Stage 2 — Dependent check

**Consumes:** target skill's name + `SNAPSHOT.lock` + every router's
SKILL.md.

**Produces:** `dependents-report.md` containing
- Every router that has a routing-table entry pointing at the target
  skill.
- Every skill whose `SNAPSHOT.lock` block lists the target under
  `depends_on:` (the per-skill dependency mechanism per
  `GOVERNANCE.md` §"Dependency Model").
- Every `coverage.md` that references the target.
- Every cross-reference in `## Handoffs to Other Skills` body sections.

**Gate:** if dependents exist AND the retirement reason is not
"replaced" or "absorbed" with a clear redirect, halt with an explicit
error. The operator must either:
- Specify a redirect target before proceeding.
- Confirm the dependents are also being retired (Level 2 rollback /
  coordinated retirement — escalate to procedural).
- Cancel the retirement.

### Stage 3 — Archive & redirect

**Consumes:** target SKILL.md + `retirement-justification.md`.

**Produces:** modified target SKILL.md with
- Frontmatter `archived: true` added.
- `metadata.changelog` prepended with a retirement entry:
  ```
  v<current> (retired, <YYYY-MM-DD>) — <reason>. <pointer>.
  ```
- A redirect block prepended to the body, immediately after the H1:
  ```
  > **⚠️ This skill is retired.**
  > <One-paragraph reason from the justification.>
  > **Replacement:** `<replacement-skill>` (or "no direct replacement —
  > see <pointer>").
  > Last canonical version: v<current>.
  ```

**Gate:** the SKILL.md still passes `validate-metadata.py` (warnings
ok) — the redirect block doesn't violate any structural rules. The
file remains pinnable: a user with `<skill-name>@<old-version>` in
their lockfile still gets the pre-archive content from git history.

See `references/redirect-note-template.md`.

### Stage 4 — Snapshot & coverage update

**Consumes:** post-archive state.

**Produces:**
- `SNAPSHOT.lock` no longer lists the target as canonical (the entry
  is removed from `skills:` or moved to a `retired:` block — see
  `coverage.md` library-root for the pattern).
- The family `coverage.md` moves the skill to a new "Retired" section
  (added if not already present) with the retirement date and
  redirect pointer.
- The library-root `coverage.md` is updated only if the retirement
  affects a domain claim.
- The library `CHANGELOG.md` gets a new entry under today's date,
  in `Removed` (for absorbed/replaced/domain-gone) or `Deprecated`
  (for health-failure with no immediate replacement) category. The
  entry names the skill, the version at retirement, the reason, and
  the redirect pointer.
- Lockfiles in dependent skills updated lock-step (if the dependent
  isn't also being retired).

**Gate:** all four files (`SNAPSHOT.lock`, family `coverage.md`,
library `coverage.md` if applicable, library `CHANGELOG.md`) updated
in the same change set. `git status` should show exactly these
modifications plus the SKILL.md from Stage 3.

See `references/retirement-checklist.md`.

## Dependencies

- The target skill's SKILL.md (read in Stage 1, modified in Stage 3).
- `SNAPSHOT.lock` (read in Stage 2, modified in Stage 4).
- The family's `coverage.md` (modified in Stage 4).
- `CHANGELOG.md` (modified in Stage 4).
- Every router that dispatches to the target (read in Stage 2; modified
  in Stage 4 if dependent updates apply).

## Evaluation

`skill-retire` is correct when:

1. After retirement, `git checkout <pre-retire-ref> -- skills/<name>/`
   restores the pre-retirement SKILL.md exactly. Pinning works.
2. `validate-metadata.py --skill skills/<name>/SKILL.md` still passes
   (or passes with the warning that the skill is archived).
3. `SNAPSHOT.lock` does not list the skill as canonical.
4. The family's `coverage.md` lists the skill in a "Retired" section.
5. `CHANGELOG.md` has a single coordinated entry for this retirement.
6. Every dependent has either been updated to point elsewhere or
   itself been retired in the same coordinated PR.

The first dogfood test is hypothetical for v0.1.0 — none of the five
lifecycle skills will be retired at v0.1.0 release. The first real test
is whenever the operator first invokes `skill-retire` on a real skill.

## Handoffs

- **From `skill-refactor` Stage 4** — invoked once for the source skill
  being refactored.
- **From the operator** — direct invocation when the four reasons apply.
- **To `skill-audit`** — after retirement, the next audit run skips the
  retired skill (or reports it under a separate "Retired" rollup).
- **To dependent router maintainers** — Stage 4 includes lock-step
  router updates as part of the same PR.

## Edge Cases

- **The target skill has no dependents.** Stage 2 passes immediately;
  no lock-step coordination needed.
- **The target skill is a router.** Retiring a router is unusual — its
  atoms become stranded. Halt unless every atom has another router or
  is also being retired.
- **The target skill has a policy overlay applied to it.** The overlay
  is broken if the mechanism is retired. Stage 2 must surface the
  overlay; the operator decides whether to retire the overlay too.
- **The target's `metadata.archetype` is `policy`.** Retiring a policy
  overlay is the simplest case — only the overlay itself goes archived;
  no mechanism is affected.
- **The retirement is being undone** (a previously-retired skill is
  being un-archived). Out of scope for v0.1.0. Treat un-archive as a
  *new authoring* via `skill-author` (because the canonical version
  pointer needs to be re-established and the redirect note removed).

## Self-Audit

Before invoking `skill-retire`, confirm:
- The decision to retire is genuinely upstream (audit/refactor/operator
  decision), not a substitute for fixing.
- The named replacement (if any) is in `SNAPSHOT.lock` and is healthy
  (run `skill-audit` against it).
- Dependents have been mapped (Stage 2 will repeat this; do it
  informally first to estimate PR size).
- The PR title will be: `retire: <skill-name> (<reason>)`.
