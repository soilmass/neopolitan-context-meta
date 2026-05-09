---
name: mood-board-author
description: >
  Authors the project's Mood Board — a curated set of visual
  references with critique of why each works, anti-references with
  rationale, and signal categories (palette, type, motion,
  composition, texture). Writes to docs/03-design/mood-board.md
  (research/E2 §C.1; SOP §6 implicit). Use at Phase 3 Design,
  after vision and design-philosophy exist but before
  art-direction-author. Do NOT use for: authoring the project
  vision (use vision-author); authoring the design philosophy
  (use design-philosophy-author in the site-build family);
  authoring the art direction (use art-direction-author — that
  synthesizes the mood board); authoring the concept (use
  concept-author — that adds narrative atop the art direction).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C per
            docs/ARCHITECTURE-OPTIONS-v0.2.md). No user-invocable
            peer exists for this Awwwards-tier addition; this atom
            establishes the pattern.
---

# mood-board-author

Phase 3 — produce the Mood Board + curated Reference list.

## When to Use

- Phase 3 Design begins; vision + persona + design-philosophy
  exist; the mood board is the first design-phase deliverable.
- A new direction is being explored mid-project (e.g., a stale
  mood board no longer reflects current intent) and the operator
  is re-curating before art-direction-author runs.
- A design competition / pitch needs a presentable visual
  exploration before commitment.
- Phase 1 brand-territory exploration produced enough material to
  warrant a structured mood board (rather than a Pinterest dump).

## When NOT to Use

- Vision or persona work — those are Phase 1 deliverables.
- The design philosophy itself — that's `design-philosophy-author`
  in the site-build family. The philosophy is the strategic
  stance; the mood board is the visual evidence.
- Authoring the art direction — `art-direction-author`. The mood
  board is the input to art direction; art direction synthesizes
  the mood board into a defended visual language with named
  palette, type, motion vocabulary.
- Authoring the concept — `concept-author`. The concept adds
  narrative / lore on top of the art direction.
- Curating references without critique. A mood board without
  written critique of why each reference works is just a
  Pinterest board — refuse that mode.
- Stack-specific motion library decisions (GSAP vs Motion vs
  native). Those follow art direction + motion language; the
  mood board collects motion *examples*, not stack picks.

## Capabilities Owned

- Curate **5–15 visual references** — agency sites, products,
  print work, motion reels, illustrations. Each reference has:
  - Source (URL or citation).
  - Snapshot / annotated screenshot.
  - **Written critique of why it works** (what specifically the
    operator wants to learn from it).
- Curate **≥3 anti-references** — patterns the design will
  deliberately avoid. Anti-references are often more decisive
  than inspirations because they cut design-by-committee
  conflicts.
- Group references into **signal categories**:
  - **Palette** — color directions worth exploring.
  - **Type** — typographic systems worth modeling.
  - **Motion** — motion language references (timing, easing,
    choreography).
  - **Composition** — layout / hierarchy / negative-space
    references.
  - **Texture / surface** — material qualities (paper, glass,
    grain, glow).
- Capture **defended visual territory** — a one-paragraph
  written stance: what the design will FEEL like, in language a
  client can review against. Not a logo, not a palette, not a
  layout — the *territory* the design occupies.
- Refuse **vibe-only mode** — every reference must have a
  critique; the curation effort is the deliverable.
- Cite the **vision** (business outcome) and the **design
  philosophy** (strategic stance) by stable name.
- Write to `docs/03-design/mood-board.md`.

## Handoffs to Other Skills

- **From `vision-author`** (site-build family) — vision shapes
  the brand expression goals.
- **From `persona-author`** (site-build family) — audience
  attributes shape what references resonate.
- **From `design-philosophy-author`** (site-build family) — the
  philosophy is the strategic frame the mood board fills in
  visually.
- **To `art-direction-author`** — the mood board is the input.
  Art direction synthesizes it into a defended visual language.
- **To `concept-author`** — visual references inform but don't
  constrain the concept (concept is narrative, mood board is
  visual).
- **To `motion-language-author`** — motion references in the
  mood board feed the motion language doc.

## Edge Cases

- **Operator wants a "vibes" mood board with no critique.**
  Refuse; the critique is the work. Without it, the mood board
  is decorative and won't survive design review.
- **References are all from one agency** (e.g., 12 Resn sites).
  Surface this as a finding — narrow inspiration produces
  narrow output. Push for 3–5 distinct sources at minimum.
- **No anti-references identified.** Push hard for ≥3. "What
  this won't be" is a faster path to consensus than "what this
  will be."
- **Stakeholder wants their pet reference included** that
  doesn't fit the territory. The mood board is curated, not
  inclusive — refuse to include with critique. If they insist,
  it goes into anti-references with their name on the dispute.
- **Mood board exceeds 15 references.** That's a Pinterest
  board, not a curated mood board. Force the cut to ≤15. The
  discipline of removal is the curatorial work.

## References

No external `references/*.md` files yet. The canonical authority
is `internal://docs/research/E2-agency-methodologies.md` §C.1
(Lusion's three-phase methodology, Phase 1: Mood Board and
Visual References) plus the implicit SOP §6 design phase. No
user-invocable peer exists for this Awwwards-tier addition; this
atom establishes the pattern.

## Self-Audit

Before declaring a mood board complete, confirm:
- 5–15 references, each with a written critique.
- ≥3 anti-references, each with a rationale.
- Signal categories (palette / type / motion / composition /
  texture) each have ≥1 reference.
- Defended visual territory captured in one paragraph.
- Vision + design philosophy cited by stable name.
- No "vibe-only" references (every one has a critique).
