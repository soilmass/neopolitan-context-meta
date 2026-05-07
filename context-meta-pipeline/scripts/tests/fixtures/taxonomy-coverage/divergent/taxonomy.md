# Sample Domain Taxonomy

Authority: <fixture — internal — divergent variant>
Generated: 2026-05-06 by fixture authoring

## Scope statement

Fixture-only. The coverage.md sibling is intentionally OUT OF SYNC with this
taxonomy: coverage.md is missing `sample-cap-b` from Tier 1 and adds an extra
`extra-cap` not in this taxonomy. Used to exercise taxonomy-coverage-sync.py
divergence detection.

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
