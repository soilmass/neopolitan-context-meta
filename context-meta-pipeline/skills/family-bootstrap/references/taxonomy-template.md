# taxonomy.md Template

Stage 3 of `family-bootstrap` produces this artifact. It's consumed by
Stage 4 (per-skill authoring) and Stage 6 (coverage registration).

The taxonomy is a *planning* artifact, not a SKILL.md. It does not pass
through `validate-metadata.py`. It lives at `skills/<domain>/taxonomy.md`
in the final family.

## Template

```markdown
# <Domain> Taxonomy

Authority: <URL — author — title>
Generated: <YYYY-MM-DD> by family-bootstrap

## Scope statement

<One paragraph from `domain-intake.yaml` Stage 1.>

## Tier 1 — Essential (6-9 atoms, always shipped)

| # | Atom name | Capabilities owned (one-line) | Authority citation |
|---|---|---|---|
| 1 | `<domain>-<scope>` | <description> | <section / page> |
| 2 | ... | ... | ... |

## Tier 2 — Specced, Not Yet Built (4-7 atoms)

| Atom name | Key concepts | Edge cases | Folds into Tier 1 atom |
|---|---|---|---|
| `<domain>-<scope>` | <list> | <list> | `<Tier 1 atom>` |

## Tier 3 — Deferred (2-5 atoms)

| Atom name | Build trigger (must be observable) |
|---|---|
| `<domain>-<scope>` | <event you would notice> |

## Out of Scope

| Capability | Why excluded |
|---|---|
| <name> | <rationale + pointer> |

## Tier rationale

(Brief paragraph explaining why the splits land where they do — what
made an atom Tier 1 vs Tier 2, what made something Tier 3 vs out-of-scope.
This justifies the design when re-read months later.)

## Cross-references

- Authority used: <URL>
- Adjacent families that may interact: <list>
- Existing skills that will need anti-triggers: <list>
```

## Tier sizing rules

- Tier 1: 6-9 atoms. Below 6 means the family is too narrow (author one
  atom instead). Above 9 means too broad (split or push to Tier 2).
- Tier 2: 4-7 atoms. Specialist needs that an encompassing family must
  enumerate even if not built.
- Tier 3: 2-5 atoms. Long tail; deferred with build triggers.

## Why the table format

Each row in each tier becomes a row in the per-family `coverage.md` and
(for Tier 1) a directory in `skills/<domain>/<atom>/`. The table format
is a one-to-one mapping of plan to delivery — no translation step.

## What goes where in subsequent stages

| Tier | Stage 4 outcome | Stage 6 coverage.md section |
|---|---|---|
| 1 | SKILL.md authored via skill-author | "In Scope (Tier 1)" |
| 2 | not authored at bootstrap | "Specced, Not Yet Built" |
| 3 | not authored at bootstrap | "Deferred" |
| Out of Scope | not authored ever (without re-tiering) | "Out of Scope" |
