# The Tier Model

Every domain claimed by the library produces three tiers of atoms. The
tier model exists to enforce the encompassing property: a flat list of
skills lets long-tail capabilities silently disappear ("we never built
it, nobody asked"). Tiers force the deferral into writing.

## Tier 1 — essential

**Size:** 6-9 atoms.
**Coverage target:** ~70-80% of common usage.
**Disposition:** always shipped at family bootstrap.

Every operator who touches the domain regularly hits Tier 1. These are
the atoms in `taxonomy.md` that have full SKILL.md files in `skills/`.

## Tier 2 — encompassing

**Size:** 4-7 atoms.
**Coverage target:** common specialist needs — subdomains with their
own complexity (hooks, submodules, large-repo handling, debugging
workflows).
**Disposition:** specced but not built at bootstrap; folded into Tier 1
atoms with the split flagged in the family's `coverage.md` until the
trigger fires.

Tier 2 entries live in `coverage.md` under "Specced, Not Yet Built".
Each entry names key concepts and edge cases — enough to author the
atom later without re-doing the analysis.

## Tier 3 — advanced

**Size:** 2-5 atoms.
**Coverage target:** long tail (plumbing, niche workflows, external
bridges).
**Disposition:** documented as deferred with **observable build
triggers**.

Tier 3 entries live in `coverage.md` under "Deferred". Each entry names
a build trigger — *something a maintainer would actually notice* — that
moves it to Tier 2 or Tier 1.

## Build triggers must be observable

The most important rule. "Build when needed" is not a trigger. The
trigger has to be something you would notice; otherwise deferral becomes
permanent abandonment.

### Examples that pass

| Tier 3 atom | Build trigger |
|---|---|
| `git-filter-repo` | Build when a contributor with kernel-style history rewriting joins the cohort. |
| `postgres-large-repo` | Build when a project's data volume crosses 5 GB. |
| `kubectl-custom-resources` | Build when the second team requests CRD authoring help. |
| `aws-organization-management` | Build when a multi-account migration ticket is opened. |

### Examples that fail (rewrite required)

| Tier 3 atom | Bad trigger | Why bad |
|---|---|---|
| `git-rerere` | Build when needed. | Not observable. |
| `postgres-tuning` | Build for advanced users. | Who counts? When? |
| `kubectl-pdb` | Build later. | No trigger at all. |

## Why Tier 1 has a 6-9 cap

Below 6: the domain is too narrow for a family — author a single atom
instead.

Above 9: the domain is too broad — split into two families, or move some
to Tier 2.

The 6-9 cap is a forcing function on scope discipline.

## Why the tiers must be enumerable, not generative

Stage 3 of `family-bootstrap` produces a *fixed* `taxonomy.md`. New
capabilities discovered later are appended via `skill-author` (with the
family's `coverage.md` updated) or via `skill-refactor` (if the
discovery requires reorganizing existing atoms).

The tier list is not regenerated each time. Stability of the taxonomy
is what makes the encompassing property check meaningful — you can ask
"which Tier 3 atoms have triggered?" and get a real answer.

## Output: `taxonomy.md`

```markdown
# <domain> Taxonomy

Authority: <URL — author — title>
Generated: <date>

## Tier 1 — Essential

| Atom | Capabilities | Citation |
|---|---|---|
| `<domain>-<scope>` | … | <authority section> |
| ... | ... | ... |

## Tier 2 — Specced, Not Yet Built

| Atom | Why deferred | Folds into |
|---|---|---|
| ... | ... | <Tier 1 atom> |

## Tier 3 — Deferred

| Atom | Build trigger |
|---|---|
| ... | ... |

## Tier rationale

A short paragraph (2–4 sentences) naming why each tier landed where it
did — especially Tier 2 deferrals (folding decisions) and Tier 3 build
triggers. This section keeps the audit trail for taxonomy decisions
when later contributors revisit the family.
```

Note: the full template in `taxonomy-template.md` includes all sections
above plus a `## Cross-references` block (URLs, adjacent families,
existing skills needing anti-triggers). When the example here and the
template disagree, the template is the source of truth.

The taxonomy is consumed by Stage 4 (per-skill authoring) and Stage 6
(coverage registration). It does not need to be re-validated by
`validate-metadata.py` — it's a planning artifact, not a SKILL.md.

---

## Artifact conventions

These conventions apply to the planning artifacts `family-bootstrap`
produces (`domain-intake.yaml`, `capabilities.json`, `taxonomy.md`)
and were surfaced as audit findings during the v0.4.0 dogfood. Audit
finding numbers are noted for traceability.

### Citation specificity (A3)

Every entry in `capabilities.json` and every Tier 1 row in
`taxonomy.md` must cite a *specific location* in the authority. A
"specific location" is one of:

- **Section/chapter heading**, e.g., `Pro Git §7.6 "Rewriting History"`.
- **Page number**, e.g., `IETF RFC 3986, p. 12`.
- **URL with anchor**, e.g., `https://docs.python.org/3/library/asyncio.html#asyncio.run`.
- **Man-page section**, e.g., `git-rebase(1) §INTERACTIVE MODE`.

Vague citations like "the docs" or "common knowledge" fail the
Stage 2 gate. If the authority doesn't cover a capability you need
to include, that's a Stage 3 signal that the capability is
out-of-scope or belongs in a different domain.

### `capabilities.json` schema (A4)

```json
[
  {
    "name": "string — provisional name lifted from authority vocabulary; may contain spaces or slashes (this is NOT a SKILL.md name); single token preferred but multi-token like 'fixup / autosquash' is acceptable when authority uses paired terminology",
    "description": "string — one sentence, paraphrased from the authority",
    "citation": "string — see Citation specificity above"
  }
]
```

Capability names follow domain vocabulary, **not** the SKILL.md
naming regex. A capability named `fixup / autosquash` is fine here
even though it contains a space and a slash; what matters is that
when the capability lands in some atom's `## Capabilities Owned`
list during Stage 4, the bullet entry is human-readable. (Audit
finding A5 / A8.) The skill names themselves (the *atoms* the
capability lands in) follow `naming.md`'s strict regex.

### `taxonomy.md` ↔ family `coverage.md` consistency (A9)

The Stage 3 `taxonomy.md` (planning artifact) and the Stage 6
family `coverage.md` (ledger artifact) both contain Tier 1 / 2 / 3
tables. Format and content **should match exactly** at bootstrap
time. They diverge over time as `skill-author`, `skill-refactor`,
and `skill-retire` update `coverage.md` but not `taxonomy.md` — the
taxonomy is fixed-at-bootstrap (per `tier-model.md` §"Why the tiers
must be enumerable, not generative"). When they diverge:

- **`coverage.md` is the source of truth** for current state.
- **`taxonomy.md` is the source of truth** for original intent —
  useful for "what did we plan to build, and why is the current
  state different?" investigations.

A future enhancement could automate keeping them aligned via a script;
not in v0.4.x.

### Capability-to-tier mapping convention (A8)

Stage 3's "every capability lands in exactly one tier" gate is
verified via an explicit mapping table at the bottom of
`taxonomy.md`:

```markdown
## Capability → Tier mapping

| Capability | Tier | Atom |
|---|---|---|
| init / add / commit | Tier 1 | git-basics |
| log (filtered) | Tier 1 | git-inspection |
| ...
```

When a `capabilities.json` entry's name contains a slash or maps
to two atoms (e.g., plain `log` in basics vs filtered `log` in
inspection), split the row in this mapping table:

```markdown
| log (plain, current branch) | Tier 1 | git-basics |
| log (filtered / cross-ref) | Tier 1 | git-inspection |
```

The mapping table is the canonical resolution of the "every
capability lands in exactly one tier" gate when capabilities are
split across atoms.
