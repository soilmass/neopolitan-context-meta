---
name: skill-author
description: >
  Authors a single SKILL.md (atom, tool, router, or policy overlay) through
  four gated stages: intake, ecosystem audit, drafting, and validation &
  registration. Produces a SKILL.md plus optional references that pass
  validate-metadata.py, with the library CHANGELOG, SNAPSHOT.lock, and the
  relevant coverage.md updated. Do NOT use for: bootstrapping a whole new
  domain family (use family-bootstrap); scaffolding an entire new library
  (use library-bootstrap); splitting an existing skill into multiple skills
  (use skill-refactor); archiving a skill (use skill-retire); running health
  checks (use skill-audit); authoring a MIGRATION-v<N>.md (use skill-migrate);
  authoring a policy overlay specifically (skill-policy-overlay handles the
  policy-archetype intake; this skill handles all other archetypes).
license: Apache-2.0
metadata:
  version: "0.1.9"
  archetype: tool
  tags: [lifecycle, daily-use]
  recency_pin: stable
  changelog: |
    v0.1.9 — patch: references/audit-ritual.md "Common drift signals
            on fresh atoms" gains a 6th drift cause — YAML folded-
            scalar mid-word hyphen wraps. Surfaced by audit finding
            A66 from the context-site-build v1.0.0-rc1 audit pass:
            14 of 75 skills initially failed the drift gate; the
            dominant cause was descriptions wrapping mid-word at
            hyphens inside YAML `description: >` blocks (folded
            scalars join lines with spaces, breaking hyphenation).
            The reference now documents the anti-pattern check
            ("if any line ends with `-`, you're at risk") and the
            fix (line breaks at SPACE boundaries only).
    v0.1.8 — patch: added "Anti-trigger fallback discipline"
            subsection to references/audit-ritual.md naming the
            user-invocable-peer fallback pattern; covers the three
            patterns (bare future reference, "(when authored)"
            qualifier, the correct user-invocable-peer fallback)
            and the no-peer case. Surfaced by audit finding A62
            from context-site-build first-real-consumer dogfood
            self-review.
    v0.1.7 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.1.6 — patch: metadata.recency_pin: stable declared (v0.6.2 wiring of
            the previously write-only escape hatch). Skill is intentionally
            stable; future edits should re-read MAINTENANCE.md before
            removing the pin.
    v0.1.5 — patch: description anti-triggers extended (A24/A25 from v0.5.2
            dogfood) — `Do NOT use for` block now explicitly names
            family-bootstrap, library-bootstrap, skill-refactor, skill-retire,
            skill-audit, skill-migrate, and skill-policy-overlay so the
            static-routing heuristic does not fire skill-author for prompts
            owned by the v0.5.0 cluster.
    v0.1.4 — patch: references/naming.md clarifies that the SKILL.md naming
            regex applies to skill names only, not capability-name body
            bullets or citation strings (audit findings A5/A8).
            references/archetypes.md adds explicit "source of truth" note
            naming `governance/METADATA-VALIDATION.md` as canonical when
            the rubric and the validator disagree (audit finding A12).
    v0.1.3 — patch: Stage 2 now documents the supersession when delegated
            from family-bootstrap Stage 4 (the family-level Stage 5 audit
            ritual replaces per-atom Stage 2 audits). Surfaced by the
            v0.4.0 family-bootstrap dogfood (audit finding A11).
    v0.1.2 — patch: Stage 4 now documents the third coverage-update branch
            (atom authored inside family-bootstrap Stage 4 against a not-yet-
            existing family coverage.md → defer to orchestrator Stage 6).
    v0.1.1 — patch: documented `metadata.recency_pin` in references/frontmatter-spec.md;
            clarified that audit-ritual.md `audit-report.md` is ephemeral.
    v0.1.0 — initial. Hand-authored as the bootstrap skill.
---

# skill-author

The lifecycle skill that creates a single new SKILL.md. Used directly by
operators authoring tools, routers, and policy overlays, and by
`family-bootstrap` (Stage 4) for each Tier 1 atom in a new family.

## Purpose

Produce one SKILL.md and any supporting references such that:

1. The result conforms to `governance/METADATA-VALIDATION.md` (universal
   frontmatter rules + archetype-specific required sections).
2. The audit ritual (`ARCHITECTURE.md` §"Routing and Contention") has been
   run against existing siblings, with anti-triggers added where contention
   is found.
3. The library `CHANGELOG.md`, `SNAPSHOT.lock`, and the relevant
   `coverage.md` are updated atomically.
4. The new skill is invokable as soon as the plugin reloads.

## When to Use

- Creating a new tool, router, or policy overlay outside any family.
- Adding a new Tier 1 atom to an existing family (after the family's
  `coverage.md` has been updated to spec it).
- Re-authoring a skill from scratch when a refactor produces new skills
  (called by `skill-refactor` Stage 3).

## When NOT to Use

- For whole new domain families with multiple atoms and a router. Use
  `family-bootstrap`; it delegates back here for each atom.
- For splitting an existing mixed-archetype skill into several skills. Use
  `skill-refactor`; it delegates here for the new skills.
- For archiving a skill. Use `skill-retire`.
- For health-checking existing skills. Use `skill-audit`.
- For library-root coverage updates that span families. Those are
  hand-authored against the library-root `coverage.md` directly.

## Stage-Gated Procedure

Four heavyweight stages. Each stage produces a named intermediate artifact
the next stage consumes; transitions are gated on the artifact passing a
verifiable check. Detail for each stage lives in the references.

### Stage 1 — Intake

**Consumes:** the operator's prompt and any pointer the operator gives to
authority docs for the skill's domain.

**Produces:** `intake.yaml` containing
- `archetype` (one of: atom, tool, router, orchestrator, policy)
- `name` (provisional, kebab-case, ≤4 segments)
- `purpose` (one sentence, third person)
- `family` (the parent family if this is an atom, otherwise null)
- `siblings` (the list of existing skills the operator believes this is
  closest to)

**Gate:** `name` matches the naming regex from
`references/frontmatter-spec.md`; `archetype` is one of the five.

### Stage 2 — Ecosystem audit

**Consumes:** `intake.yaml` + the current `SNAPSHOT.lock`.

**Produces:** `audit-report.md` containing
- The top three skills by description-keyword overlap with the proposed
  skill's purpose.
- Five ambiguous prompts that could plausibly route to any of those three
  plus the new skill.
- For each prompt: the operator's prediction of which skill the LLM should
  pick, and a justification.
- For each contended sibling: either an anti-trigger string to add to that
  sibling's description, or an explicit "no contention — descriptions are
  already disjoint" justification.

**Gate:** every contended sibling has either an anti-trigger update queued
or a written no-contention justification. No silent contentions allowed.

This stage implements the audit ritual from `ARCHITECTURE.md` §"Routing
and Contention" — see `references/audit-ritual.md` for the procedure.

**When invoked from `family-bootstrap` Stage 4:** the family-level
`family-bootstrap` Stage 5 ("Weaving") runs the audit ritual across
the *whole family at once* — once per Tier 1 atom plus once for the
router, with the sibling pool spanning every other atom in the family
plus the router (per `family-bootstrap` Stage 5 description). When
this skill is delegated by the orchestrator, the per-atom Stage 2
here defers to that family-wide ritual: the operator (or the
orchestrator) does NOT re-run a separate Stage 2 audit for each
atom during Stage 4. The orchestrator's Stage 5 is the single source
of audit coverage for atoms produced by family-bootstrap. Standalone
`skill-author` invocations (no orchestrator) DO run this Stage 2
fully.

### Stage 3 — Drafting

**Consumes:** `intake.yaml`, `audit-report.md`, and the appropriate
archetype rubric from `references/archetypes.md`.

**Produces:** the SKILL.md draft and any necessary `references/*.md`
files.

The draft must include:
- Frontmatter complying with `references/frontmatter-spec.md`:
  `name`, `description` (≤1024 chars, third-person, includes a
  "Do NOT use for" block), `license`, `metadata.version` (start at
  `0.1.0`), `metadata.archetype`, `metadata.changelog`.
- All required sections for the chosen archetype, per
  `references/archetypes.md`.
- Body ≤500 lines. Detail beyond the body cap goes into references.

**Gate:** the draft is internally complete — no `TODO` markers, every
required section has substantive content, all references referenced from
the body actually exist.

### Stage 4 — Validation & registration

**Consumes:** the Stage 3 draft.

**Produces:**
- A clean run of `scripts/validate-metadata.py --skill <draft>` (exit 0).
- Anti-trigger updates applied to siblings flagged in Stage 2.
- A new entry in the library `CHANGELOG.md` under today's date in the
  `Added` category.
- A new entry in `SNAPSHOT.lock` for the skill.
- An update to the relevant `coverage.md`:
  - For an atom in an existing family: move the atom's row from
    "Specced, Not Yet Built" to "In Scope (Tier 1)".
  - For a tool/router/orchestrator/policy outside any family: add to
    library-root `coverage.md` if it represents a new claimed domain.
  - For an atom being authored *during* `family-bootstrap` Stage 4
    (initial bootstrap of a brand-new family that does not yet have a
    `coverage.md`): defer the update. The orchestrator's Stage 6
    writes the family's `coverage.md` fresh from the woven Stage 5
    state, so per-atom updates would be redundant and would race the
    orchestrator's atomic write. Stage 4's gate treats this case as
    "coverage update deferred to caller".

**Gate:** validator exits 0; CHANGELOG, SNAPSHOT.lock, and coverage.md
are all updated in the same change set; sibling anti-trigger updates are
applied.

## Dependencies

- `scripts/validate-metadata.py` — runs at the Stage 4 gate.
- `SNAPSHOT.lock` (root) — read in Stage 2; updated in Stage 4.
- The relevant `coverage.md` — updated in Stage 4.
- `CHANGELOG.md` (root) — appended in Stage 4.
- The four references attached to this skill:
  - `references/archetypes.md` — required-sections per archetype
  - `references/naming.md` — naming conventions and the regex
  - `references/frontmatter-spec.md` — frontmatter schema
  - `references/audit-ritual.md` — the Stage 2 procedure

## Evaluation

`skill-author` is correct when, run against ten varied intakes spanning all
five archetypes, every produced SKILL.md:

1. Passes `validate-metadata.py --skill <produced>` with exit 0.
2. Has a `Do NOT use for` block in its description that names at least
   one specific sibling.
3. Has its name and version reflected in `SNAPSHOT.lock`.
4. Has an entry in `CHANGELOG.md` under today's date.
5. Has the appropriate `coverage.md` row updated.

The first dogfood test of `skill-author` is the authoring of the four other
lifecycle skills (`family-bootstrap`, `skill-audit`, `skill-refactor`,
`skill-retire`) — if any of them fails to pass these five checks after
going through `skill-author`'s procedure, `skill-author` itself is failing
its evaluation.

## Handoffs

- **From `family-bootstrap` Stage 4:** invoked once per Tier 1 atom in the
  new family. The orchestrator passes a pre-filled `intake.yaml` so this
  skill's Stage 1 is a confirm-or-edit rather than a full intake.
- **From `skill-refactor` Stage 3:** invoked once per new skill produced by
  the refactor.
- **To `skill-audit`:** the produced skill becomes a target the next time
  `skill-audit` runs against the library.
- **To downstream maintainers** of router skills that should now dispatch
  to the new skill: the operator updates the router separately (per
  `GOVERNANCE.md` §"Adding a New Skill" step 7).

## Edge Cases

- **The operator names a skill that already exists.** Stage 1 fails the
  gate; the operator either chooses a different name or invokes
  `skill-refactor` instead.
- **The intake produces an archetype mix** ("…and…" in purpose; two
  distinct verbs). Stage 1 fails the gate; the operator authors two
  separate skills, one per archetype.
- **The audit (Stage 2) finds three or more contended siblings.** This is
  a signal that the proposed skill's domain is too broad. Either narrow
  the scope, or escalate to `skill-refactor` to consider redrawing
  boundaries across the contended siblings.
- **The validator (Stage 4) flags a body line count over 500.** Push
  detail into references and re-run. The cap is binding — the validator
  blocks merge.
- **The skill being authored is itself a meta-skill** (a sibling of the
  five lifecycle skills). The procedure applies recursively. The
  description's anti-triggers must explicitly name the existing four to
  prevent routing competition.

## Self-Audit

Before running this skill on its first real authoring task, run it against
itself: confirm the SKILL.md you are reading passes
`validate-metadata.py --skill skills/skill-author/SKILL.md` with exit 0.
This is the bootstrap check. If it fails, fix the validator or this
SKILL.md before authoring anything else.
