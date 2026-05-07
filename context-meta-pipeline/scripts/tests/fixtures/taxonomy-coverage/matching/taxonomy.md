# Sample Domain Taxonomy

Authority: <fixture — internal — taxonomy-coverage-sync test>
Generated: 2026-05-06 by fixture authoring

## Scope statement

Fixture-only taxonomy used to exercise taxonomy-coverage-sync.py against a
matching coverage.md. Atoms in Tier 1 / Tier 2 / Tier 3 here must equal the
atoms named in the sibling coverage.md.

## Tier 1 — Essential

| # | Atom name | Capabilities owned (one-line) | Authority citation |
|---|---|---|---|
| 1 | `sample-cap-a` | Owns capability A. | fixture |
| 2 | `sample-cap-b` | Owns capability B. | fixture |

## Tier 2 — Specced, Not Yet Built

| Atom name | Key concepts | Edge cases | Folds into Tier 1 atom |
|---|---|---|---|
| `sample-cap-c` | concept | none | `sample-cap-a` |

## Tier 3 — Deferred

| Atom name | Build trigger (must be observable) |
|---|---|
| `sample-cap-d` | when consumer demand surfaces |
