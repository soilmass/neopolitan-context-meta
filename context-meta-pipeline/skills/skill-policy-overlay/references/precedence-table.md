# precedence-table.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

When the operator's prompt is ambiguous between an overlay and the underlying
mechanism atom, this table defines who fires first.

## Single-tier precedence (the v0.5.0+ case)

| Prompt shape | Fires |
|---|---|
| Mentions overlay name explicitly (e.g., `house-postgres-conventions`) | overlay |
| Mentions mechanism name explicitly (e.g., `postgres-history-rewriting`) | mechanism |
| Domain-only ("rewrite some postgres history") with NO overlay context | mechanism |
| Domain + team context ("our postgres rebase rules") | overlay (operator's team conventions implied) |
| Cross-team / library-wide ("the standard postgres-rebase pattern") | mechanism (no overlay applies) |

Tiebreaker rules:
- if `meta` router's routing-table entry resolves the ambiguity, follow it;
- if the routing layer (LLM-based) is uncertain, prefer the mechanism (the
  overlay is opt-in by definition);
- if the operator's team has only one overlay on a mechanism, prefer the
  overlay when team context is present in any form.

## Multi-tier precedence (deferred — v0.7.0 speculative)

When 2+ overlays apply to the same mechanism:

| Stack | Routing layer fires |
|---|---|
| `frontend-overlay` ⤳ `base-overlay` ⤳ `mechanism` | frontend-overlay (outermost) |
| Operator names the mechanism explicitly | mechanism (skips both overlays) |
| Operator names the base overlay explicitly | base-overlay (skips frontend) |

Open questions for the multi-tier case (see also `composition-rules.md`):

- What happens if the operator's prompt mentions BOTH `frontend-overlay`
  and `mechanism`? Proposed: frontend-overlay wins (operator opted into
  the overlay context). Confirmed at first real consumer dogfood.
- What happens if `frontend-overlay`'s `Do NOT use for` clause names the
  mechanism explicitly? Proposed: error; the overlay can't refuse the
  mechanism it applies to. Operator must rephrase the clause.

## Drift signals

When precedence is ambiguous in practice, that's a drift signal. The audit
ritual (`skill-author/references/audit-ritual.md`) should surface it:

- if 3+ ambiguous prompts could route to either overlay or mechanism, the
  overlay's anti-triggers need sharpening;
- if the routing-eval suite shows the wrong one firing, sharpen the
  description (overlay or mechanism, whichever is mis-firing).

## When to use this table

- Authoring a new overlay: walk the table, confirm each row's
  decision matches operator intent; add anti-triggers to the overlay's
  description if any row's decision is wrong.
- Reviewing an overlay PR: cross-check the proposed routing claims against
  this table.
- Audit-ritual Stage 2: flag ambiguity rows that the table doesn't resolve.
