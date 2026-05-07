# Per-Family coverage.md Template

Every family produced by `family-bootstrap` ships with a `coverage.md`
at the family root. Six sections, all required. The "Out of Scope"
section is load-bearing.

## Template

```markdown
# <Family> Coverage

Authority: <URL — author — title>
Last verification: <YYYY-MM-DD>

## In Scope (Tier 1)

| Atom | Owns | Last health check |
|---|---|---|
| `<domain>-<scope>` | <one-line responsibility statement> | <YYYY-MM-DD> |
| ... | ... | ... |

## Specced, Not Yet Built (Tier 2)

| Atom | Key concepts | Edge cases | Folds into |
|---|---|---|---|
| `<domain>-<scope>` | <list> | <list> | <Tier 1 atom currently absorbing this> |

## Deferred (Tier 3)

| Atom | Build trigger |
|---|---|
| `<domain>-<scope>` | <observable trigger> |

## Policy Overlay

`<context>-<domain>-<aspect>` — applies on top of this family's mechanism
atoms. <Or: "No policy overlay exists for this family.">

## Out of Scope

| Capability | Why out of scope | Where to look instead |
|---|---|---|
| <capability> | <rationale> | <pointer> |

## Coverage Matrix Status

Last `skill-audit` run: <YYYY-MM-DD>. <PASS|FLAGGED — reasons>.

Tier transitions since last verification:
- <atom> moved Tier 3 → Tier 2 on <date> (trigger: <event>)
- ...
```

## Section discipline

### `In Scope (Tier 1)`

Every atom shipped in `skills/<domain>/<atom>/` has a row here. The
"Owns" column is one line — the same one-line statement that lives in
the atom's `## Capabilities Owned`.

### `Specced, Not Yet Built (Tier 2)`

Atoms identified in Stage 3 of `family-bootstrap` as encompassing-tier
but not built at bootstrap. Each row names key concepts and edge cases
so that a future authoring run can pick up without re-doing the analysis.

The "Folds into" column names the Tier 1 atom currently absorbing this
capability — so when the Tier 2 atom is built later, the absorbing
atom's split is documented.

### `Deferred (Tier 3)`

Atoms named with **observable build triggers**. "Build when needed" is
not a trigger; see `tier-model.md`.

### `Policy Overlay`

If a `house-<domain>-conventions` (or similar) skill exists for this
family, name it here. If none exists, write "No policy overlay exists
for this family." — the *absence* is documented, not silent.

### `Out of Scope`

The most important section. Capabilities the family explicitly does
not cover. Each row has rationale and a pointer to where the operator
should look instead. **Must have at least one entry** — Stage 6 gate
fails on an empty Out of Scope section.

This section is load-bearing because *silent gaps are where encompassing
claims actually fail*. A documented gap is a covered gap.

### `Coverage Matrix Status`

Last `skill-audit` run output for this family. PASS / FLAGGED with
reasons. Includes any tier transitions since the last verification.

## When this gets updated

| Event | Section affected | Updated by |
|---|---|---|
| New atom added to family | In Scope (Tier 1) | `skill-author` Stage 4 |
| Tier 2 atom built | In Scope, Specced removed | `skill-author` Stage 4 |
| Tier 3 atom built | In Scope, Deferred removed | `skill-author` Stage 4 |
| Atom retired | Retired (new section) added | `skill-retire` Stage 4 |
| Atom split into two | In Scope updated | `skill-refactor` Stage 4 |
| Audit run | Coverage Matrix Status | `skill-audit` Stage 5 |
| Out of Scope claim contested | Out of Scope updated | hand-edit (with PR) |
