---
name: art-direction-author
description: >
  Authors the project's Art Direction document — a defended visual
  language synthesized from the mood board, with named palette
  (often two-color per Awwwards-tier convention), type system,
  motion vocabulary, photography or illustration direction, and
  rules for tone. The phase ~20 top agencies (Active Theory, Lusion,
  Bonhomme, Locomotive, Build in Amsterdam) treat as a named,
  billable deliverable upstream of UI design. Writes to
  docs/03-design/art-direction.md (research/E2-agency-methodologies.md
  §A.3 + glossary; SOP §6 implicit). Use after mood-board-author
  has shipped. Do NOT use for: curating the mood board (use
  mood-board-author — that is the upstream input); authoring the
  concept (use concept-author — that adds narrative); authoring
  motion specs (use motion-language-author); authoring design
  tokens (use design-tokens-author — that is the code-side
  expression of art direction).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C). No
            user-invocable peer exists for this Awwwards-tier
            addition; this atom establishes the pattern.
---

# art-direction-author

Phase 3 — produce the project's Art Direction document.

## When to Use

- Phase 3 Design is in progress; the mood board has shipped; the
  art direction is the next deliverable.
- A redesign / rebrand is taking the project in a new visual
  direction and the existing art direction no longer matches.
- A multi-property project (marketing site + product app + content
  site) needs a unified art direction across surfaces.
- A design competition / pitch demands a defendable visual
  language commitment before design-system work begins.

## When NOT to Use

- The mood board doesn't exist yet — `mood-board-author` first.
  Art direction synthesizes the mood board; without it, this
  atom is producing fiction.
- Authoring the design philosophy — `design-philosophy-author`
  (site-build family) is the strategic stance; art direction is
  the visual stance derived from it.
- Authoring the concept — `concept-author`. Concept is the
  narrative thread; art direction is the visual language.
- Authoring motion specs — `motion-language-author`. Art direction
  states the motion *vocabulary* (high-level — energetic vs
  restrained vs cinematic); motion language operationalizes it
  into timing/easing/tokens.
- Producing design tokens — `design-tokens-author`. Tokens are
  the code-side expression; art direction is the human-readable
  contract.
- Per-component visual specs — those follow once art direction
  + tokens exist (component-states-matrix-author handles them).

## Capabilities Owned

- Synthesize the mood board into a **defended visual language**:
  - **Palette** — named colors with usage rules (often a
    two-color palette per Awwwards-tier convention; primary +
    accent + neutrals).
  - **Type system** — display, body, mono families with type
    scale and usage rules (display weight at hero only, etc.).
  - **Motion vocabulary** — the high-level motion stance
    (cinematic / restrained / energetic / playful) that the
    motion language doc operationalizes.
  - **Photography / illustration direction** — when imagery
    is in scope (product shots, hero photography,
    illustration system).
  - **Texture / surface qualities** — paper / glass / grain /
    glow / matte / chrome.
- Produce **rules for tone** — when each visual element
  intensifies vs recedes (hero vs detail; entry vs depth).
- Capture **defended creative territory** — one paragraph that
  governs review conversations ("does this fit the territory?"
  beats "do I like it?").
- Document **anti-references explicitly** — what the design
  will NOT do, carried over from the mood board's anti-refs
  with rationale.
- Cite **vision** + **persona** + **design philosophy** by
  stable name as the strategic upstream context.
- Write to `docs/03-design/art-direction.md`.

## Handoffs to Other Skills

- **From `mood-board-author`** — the mood board is the input.
- **From `vision-author`** + **`persona-author`** + **`design-
  philosophy-author`** (all site-build family) — the strategic
  upstream context.
- **To `concept-author`** — concept builds narrative on top of
  the art direction's visual language.
- **To `motion-language-author`** — motion vocabulary stated
  here gets operationalized into tokens + rules.
- **To `design-tokens-author`** — palette + type + spacing get
  encoded as DTCG tokens.
- **To `component-states-matrix-author`** — visual states use
  the art direction's palette + motion vocabulary.
- **To `wireframe-author`** (Tier 2) — wireframes apply the
  art direction at increasing fidelity.

## Edge Cases

- **No mood board exists.** Halt; mood board is the
  prerequisite. Refuse to produce art direction from
  Pinterest-shaped vibes.
- **Stakeholder demands a third or fourth palette color.**
  Surface that two-color palettes are an Awwwards-tier signal
  (per E1 research, ~75% of recent SOTY winners are
  two-color); refuse silently expanding. If a third color is
  truly needed, document it as a defended choice with named
  use-case.
- **Type licensing constraint** (open-source-only, brand-
  font-mandated). Art direction respects the constraint but
  surfaces the trade-off explicitly.
- **Multi-stack project** (site + app + content) where one
  art direction can't honestly cover all surfaces. Split into
  parent art direction + per-surface variants (e.g.,
  "marketing art direction" vs "app art direction") and
  cross-link.
- **Stakeholder wants "modern and timeless" / "playful and
  serious"** — both poles. Refuse the synthesis; force the
  Sponsor to pick a pole. The territory is defended, not
  hedged.

## References

No external `references/*.md` files yet. The canonical
authorities are `internal://docs/research/E2-agency-methodologies.md`
§A.3 (Awwwards-tier vocabulary glossary including "Art Direction"
as a named upstream phase across Active Theory, Lusion, Bonhomme,
Build in Amsterdam, Locomotive, Mathematic, Dogstudio, Immersive
Garden) and the implicit SOP §6 design phase. No user-invocable
peer exists for this Awwwards-tier addition.

## Self-Audit

Before declaring an art-direction doc complete, confirm:
- Palette is defended with named usage rules (often
  two-color; document if more).
- Type system has ≥3 facets (display + body + mono at
  minimum).
- Motion vocabulary states the high-level stance
  (cinematic / restrained / energetic / playful).
- Photography/illustration direction stated OR explicitly
  marked "no imagery in scope."
- Defended creative territory captured in one paragraph.
- ≥3 anti-references carried from mood board with rationale.
- Vision + persona + design philosophy cited by stable name.
- Doc is ≤4 pages rendered (longer is design-system territory).
