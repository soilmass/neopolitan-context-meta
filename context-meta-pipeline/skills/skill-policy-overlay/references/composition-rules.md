# composition-rules.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library
> (specifically: when ≥1 real `house-*` overlay exists on a mechanism atom).

How policy overlays compose with mechanism atoms and (in the speculative
multi-tier case) with each other.

## Single-tier composition (the v0.5.0+ case)

One overlay applied on top of one mechanism atom:

```
mechanism atom: postgres-history-rewriting (archetype: atom)
    ↑ applies on top of
overlay: house-postgres-conventions (archetype: policy)
```

The overlay's body documents:
- which mechanism atom(s) it applies to (named under `## Applies On Top Of`)
- which capabilities it overrides or constrains
- which `Do NOT use for` clauses it adds beyond the mechanism's own

When the operator invokes via the overlay, the routing layer should fire
the overlay's stages (which then delegate to the mechanism). When the
operator invokes via the mechanism directly, no overlay applies.

Single-tier is what `skill-policy-overlay` ships with. v0.7.0 thickening
documents the discipline; multi-tier (below) is still deferred.

## Multi-tier composition (deferred — v0.7.0 speculative)

Two overlays on the same mechanism, applied in order:

```
mechanism atom: postgres-history-rewriting
    ↑ applies on top of
overlay-base: acme-postgres-base (org-wide conventions)
    ↑ applies on top of
overlay-team: acme-frontend-postgres (frontend-team specifics that override base)
```

Open questions for the multi-tier case (per `ARCHITECTURE.md` §"Open
Questions"):

1. **Composition order**: which overlay's `Do NOT use for` wins when they
   disagree? Proposed: the *outermost* overlay (frontend-team, in the
   example above) takes precedence; the inner overlay's clauses are
   additive unless explicitly overridden via `## Overrides` section.
2. **Where the order is declared**: in the outermost overlay's `## Applies
   On Top Of` section (a list, in priority order), OR in a separate
   `## Composition Order` section, OR in a library-level manifest. Open.
3. **Whether overlays can override each other's stage logic** (vs only
   their gates). Open.

These resolve when 2+ tiers of `house-*` overlays exist on the same
mechanism — the build trigger from `coverage.md` Domains Deferred row.

## When NOT to author an overlay

- The override is a one-off (single project, no cross-team value). Document
  in the project's README; don't pollute the library.
- The "override" is really just a different mechanism. If the diff is
  >50% of the mechanism's stages, you're authoring a new atom, not an
  overlay — use `skill-author` directly.
- The override is temporary (e.g., during a migration). Use a CHANGELOG
  entry naming the deviation; archive the change when the migration ships.

## Policy-overlay archetype invariants (v0.7.0)

- `metadata.archetype: policy` (the only required-section difference vs
  tool/atom is that policy adds `## Applies On Top Of` per
  `governance/METADATA-VALIDATION.md`).
- Description must include `house-` prefix (or organization-specific
  equivalent) — distinguishes overlays from mechanisms in routing.
- Overlay's `metadata.changelog` should reference the mechanism's version
  it was authored against. When the mechanism MAJOR-bumps, the overlay
  needs a refresh.
