# Archetype-Mixing Signals

Stage 1 of `skill-refactor` looks for these signals to decide whether
a refactor is needed and which type applies.

## The "and" test

Per `ARCHITECTURE.md`: if a skill's description has "and" between two
distinct verbs, the skill is two skills.

### Examples that fail the test

| Description fragment | Diagnosis |
|---|---|
| "Authors **and** validates new SKILL.md…" | Two atoms / two tools — split. |
| "Rebases **and** force-pushes…" | One workflow with two stages — *probably* fine; check next test. |
| "Documents **and** enforces conventions…" | Mechanism + policy — three-way. |
| "Reads **and** writes…" | Read/write split — two atoms. |

### Examples that pass

| Description fragment | Why ok |
|---|---|
| "Validates **and** reports" | Same verb cluster (validation produces a report — single workflow). |
| "Audits **and** flags" | Same verb cluster (audit emits flags — single output). |

The test is judgment-based. The "and" is a *signal*, not a *verdict*.

## The "ships unchanged" test

Could this skill ship to another team without modification?

If the answer is "no, because we have specific conventions hard-coded,"
the skill mixes mechanism and policy. Three-way refactor applies.

If the answer is "no, because the skill calls a tool we have specific
to our team," the skill is fine but its dependency tree includes
non-portable skills.

## The "internal mode" test

Does the skill have internal modes that the operator selects from?

```
## Modes
- inspect: read-only audit
- write: creates new file
- delete: removes existing
```

This is silent capability creep. Each mode should be its own skill;
together they may form a family with a router.

## The body-line cliff

A skill body that has grown past 500 lines (the cap from
`METADATA-VALIDATION.md`) is a refactor signal even if the
`validate-metadata.py` checks are passing because the operator pushed
detail to references.

If the SKILL.md is repeatedly hitting the cap and references are
proliferating, the skill is too large. Split.

## The drift-gate signal

`skill-audit` Stage 3 measures description drift. A drift >10% over
two consecutive audits, especially when the description hasn't been
edited, means the body has grown to cover capabilities the description
doesn't claim. Either:
- Update the description (cheap, no version bump).
- Or the new capabilities don't belong here — refactor.

## The router-vs-atom signal

A skill claims to "dispatch" or "route" but also performs operations
directly. Routers per `ARCHITECTURE.md` §"Per-domain routers" do
*intent classification only* — no domain knowledge.

If your router has a `## Capabilities Owned` section, it's not a
router; it's an atom that pretends to be a router. Split.

## The "house" prefix signal

A skill named `house-*` (or `acme-*`, `team-*`) but its body explains
domain mechanics — that's the policy overlay re-explaining mechanism.

Per `ARCHITECTURE.md`: "Reference the mechanism skill rather than
re-explaining commands." If the policy overlay's body explains how
`git rebase` works rather than just "never rebase shared branches,"
mechanism has leaked into policy.

## Refactor type by signal

| Signal | Likely refactor type |
|---|---|
| Two distinct verbs in description | Split |
| Internal modes | Split (or router family) |
| Body >500 lines repeatedly | Split |
| Mechanism + policy mixed | Three-way |
| Router with `## Capabilities Owned` | Split (router → router + atom) |
| Two siblings with overlapping descriptions | Merge (or sharper anti-triggers — try anti-triggers first) |
| A capability moved between domains in the authority | Move |
| Drift gate failing on a healthy-looking body | Description rewrite (no refactor needed) |

## What the signals do NOT justify

- **Aesthetic preference.** "I think the body would read better split"
  is not a refactor reason. Refactor for *correctness*, not style.
- **Future-proofing.** "We might want to split later if X happens."
  Wait for X.
- **Refactor cascades.** Don't refactor skill A to make skill B's
  refactor easier. Refactor each on its own merit.

## When in doubt

Run `skill-audit` first. If multiple gates flag the same skill, the
refactor case is strong. If only one gate flags (especially
description drift), try fixing the description without restructuring.
