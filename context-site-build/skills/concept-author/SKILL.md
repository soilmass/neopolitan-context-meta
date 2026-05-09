---
name: concept-author
description: >
  Authors the project's Concept document — the creative thesis,
  narrative, lore, and defended creative territory at Phase 3
  Design. Captures voice in 3+ facets and the narrative purpose
  of motion. Output goes to docs/03-design/concept.md (research/E2
  §A.2 + glossary). Use after mood-board-author and
  art-direction-author run. Do NOT use for: curating the mood
  board (use mood-board-author); authoring the visual language
  (use art-direction-author — concept builds narrative on top of
  visual language); authoring the project vision (use vision-
  author — vision is business-outcome focused; concept is
  creative-direction focused); authoring copy (concept defines
  voice; copy implements it); authoring motion specs (use
  motion-language-author).
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

# concept-author

Phase 3 — produce the project's Concept document.

## When to Use

- Phase 3 Design is in progress; mood board + art direction have
  shipped; the concept is the next deliverable that adds the
  narrative thread the design will tell.
- A pitch / competition / Awwwards submission demands a
  defendable creative thesis that goes beyond "good design."
- A multi-page narrative / scrolly-tell experience is in scope
  and the concept governs the scroll's narrative arc.
- An Awwwards-tier project where the visual language alone won't
  carry the brief — the concept is the differentiator.

## When NOT to Use

- The mood board or art direction don't exist yet — those are
  prerequisites. Concept builds atop visual language, not
  underneath it.
- Authoring the project vision — `vision-author` (site-build
  family). Vision is business-outcome focused (target user ×
  problem × outcome); concept is creative-direction focused
  (what story does this project tell, what feeling does it
  evoke, what creative territory does it occupy).
- Authoring the visual language itself — `art-direction-author`.
  Concept builds on art direction; doesn't replace it.
- Writing copy / microcopy — concept defines the voice but copy
  is its own discipline (writers / content leads).
- Authoring motion specs — `motion-language-author`. Concept
  states the *narrative* purpose of motion ("scroll IS the
  experience"); motion language defines the timing/easing rules.
- Per-page / per-section storyboarding — that's a wireframe-author
  + prototype-author concern, downstream of concept.

## Capabilities Owned

- Articulate the **creative thesis** — one paragraph stating
  what this project is *about* creatively, beyond what it does
  functionally. The thesis is defendable in one sentence
  (similar to Lusion's "every project gets its own system, its
  own logic, and its own flavour" but project-specific).
- Build the **narrative** — what's the through-line a user
  experiences from arrival to departure? For scroll-driven
  sites: the chaptered structure. For app-shell projects: the
  emotional posture of each major surface.
- Capture **lore** when applicable — the project's internal
  fictional universe (Antinomy's "lore & narrative"). Even
  non-fictional projects benefit from internal-consistency
  rules ("the brand's relationship to its users is X").
- Define **defended creative territory** — where this concept
  lives that no competitor occupies. Survives stakeholder
  revision; serves as the disambiguation point in design
  reviews.
- State the **voice** — first-person plural? authoritative?
  warm? technical? playful? Each voice facet gets one sentence
  with an example phrasing.
- Document the **narrative purpose of motion** — does motion
  lead the story (scrolly-tell), accent the story (transitions
  between content), or recede (functional motion only)?
  Hands off to motion-language-author for operationalization.
- Cite **vision** + **persona** + **art direction** by stable
  name.
- Write to `docs/03-design/concept.md`.

## Handoffs to Other Skills

- **From `art-direction-author`** — visual language is the
  concept's palette of expression.
- **From `mood-board-author`** — mood-board references inform
  but don't constrain the concept.
- **From `vision-author`** + **`persona-author`** (site-build
  family) — strategic upstream context.
- **To `motion-language-author`** — narrative purpose of
  motion stated here gets operationalized.
- **To `concept-prototyping-author`** (Tier 2) — concept
  prototypes test the creative thesis in 3D / runtime tools
  before the brief is signed (Lusion Phase 2).
- **To `wireframe-author`** + **`prototype-author`** (Tier 2)
  — concept governs the narrative structure of the user
  journey.
- **To copywriting / content streams** — voice stated here
  governs all written content.

## Edge Cases

- **Stakeholder treats "concept" as "tagline."** Refuse the
  reduction. A tagline is a copy artefact; concept is the
  creative thesis governing visual + narrative + motion
  decisions across the whole project.
- **No defendable creative territory exists** (project is
  generic by intent — e.g., a transactional checkout flow).
  Acceptable; mark the concept as "minimal — functional
  excellence is the concept" and document the stance. Don't
  invent lore where there is none.
- **Concept conflicts with vision.** Halt; one or the other
  needs revision. Concept can't override the business
  outcome the vision states; vision can't dictate the
  creative voice the concept defends.
- **Multiple concepts proposed** (different stakeholders
  pitching). Sponsor arbitrates; the concept doc captures
  the rejected concepts in an appendix with rationale (so
  the design review doesn't relitigate).
- **Concept changes mid-project.** Re-author rather than
  patch; the old concept becomes appendix; design + dev
  re-align.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://docs/research/E2-agency-methodologies.md`
§A.2 (concept as named deliverable across Lusion, Resn, AT,
Antinomy, Immersive Garden) plus §E vocabulary glossary
(concept, creative direction, narrative, lore, creative
territory). No user-invocable peer exists for this Awwwards-
tier addition.

## Self-Audit

Before declaring a concept doc complete, confirm:
- Creative thesis stated in one paragraph + one defendable
  sentence.
- Narrative through-line described (chaptered scroll, surface
  emotional posture, etc.).
- Lore present OR explicitly marked "minimal — functional
  excellence."
- Defended creative territory captured.
- Voice stated in ≥3 facets with example phrasings.
- Narrative purpose of motion declared (lead / accent /
  recede).
- Vision + persona + art direction cited by stable name.
- Doc is ≤3 pages rendered.
