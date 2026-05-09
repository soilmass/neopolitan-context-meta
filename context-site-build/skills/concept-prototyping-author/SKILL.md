---
name: concept-prototyping-author
description: >
  Authors a concept prototype in 3D / runtime tools (Houdini, Cinema
  4D, vvvv, WebGL, Unity, Unreal, Blender) — the Awwwards-tier
  Lusion calls "Phase 2: Concept Prototyping" and Active Theory
  calls "Designing with Code." Distinct from the clickable Figma /
  Framer prototype: this prototype tests visual + dynamic + technical
  feasibility before the brief is signed. Writes to
  docs/03-design/concept-prototype/<id>.md plus any source-tool
  files (research/E2-agency-methodologies.md §C.2). Use after
  concept-author + motion-language-author ship and the project's
  ambition needs runtime-grade proof. Do NOT use for: clickable
  Figma / Framer prototypes (use prototype-author); production
  WebGL implementation (Phase 4 build); authoring the concept
  itself (use concept-author); writing the motion language (use
  motion-language-author); writing the SRS (use srs-author).
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

# concept-prototyping-author

Phase 3 — produce a concept prototype in 3D / runtime tools.

## When to Use

- The project's creative thesis (per `concept-author`) is
  ambitious enough that a Figma prototype can't prove
  feasibility — WebGL hero, scroll-driven 3D narrative,
  procedural generation, custom shaders.
- A pitch / competition needs a moving demo before the brief
  is signed. Lusion's case-study language: *"invite our
  clients to view their product in real-time animation."*
- The motion language commits to specific timing / easing
  patterns and the team needs runtime-grade evidence the
  patterns hold up at 60fps with real assets.
- An asset-pipeline question (Draco compression, KTX2
  textures, voxel-PNG cloth animation) needs a real test.

## When NOT to Use

- Concept or motion language don't exist — those are the
  upstream creative + motion sources. Without them, this
  atom would be producing arbitrary 3D demos.
- A clickable Figma / Framer prototype suffices for the
  brief — `prototype-author`. Concept prototyping is for
  ambition that exceeds Figma's expressiveness.
- Production WebGL / Three.js implementation — that's Phase
  4 build. Concept prototypes are throwaway proof-of-concept;
  production code is durable.
- Writing the concept itself — `concept-author`.
- Writing the motion language — `motion-language-author`.
- Writing the SRS — `srs-author`. NFRs reference the concept
  prototype's results; the prototype isn't a spec.
- A static visualization (mockup, marketing render). Concept
  prototypes are *runtime* — they run, they animate, they
  respond.

## Capabilities Owned

- Pick the **runtime tool** appropriate to the prototype's
  goal. Per E2 §C.2 (Lusion):
  - **Houdini FX** — procedural geometry, simulation,
    particle systems.
  - **Cinema 4D** — character / motion-graphics-grade
    animation.
  - **vvvv** — node-based real-time visual programming
    (live performance work).
  - **WebGL / Three.js / R3F** — the production-adjacent
    runtime; concept prototype here doubles as a starting
    point for Phase 4.
  - **Unity / Unreal** — game-engine-grade prototypes when
    the project reaches into installation / VR / AR.
  - **Blender** — 3D asset authoring + animated turntables.
- Build the **prototype scope** — narrow to ≤3 hero
  interactions; the prototype tests these, not the whole site.
- Test **technical feasibility** — does the shader work?
  Does the asset budget fit (per E3 §3.3 Draco + KTX2 = 70-90%
  reduction)? Does the motion run at 60fps on the project's
  device tier?
- Test **visual feasibility** — does the art direction
  translate from static mockup to real-time render? Where
  do compromises emerge?
- Test **dynamic feasibility** — does the concept's
  narrative thread hold up when scrubbed in real time? Where
  does the user lose context?
- Document the **prototype findings**:
  - What worked.
  - What didn't (and the technical reason).
  - What needed compromise (and the trade-off).
  - The tooling / asset-pipeline decisions implied for
    Phase 4.
- Cite the **concept** + **motion language** + **art
  direction** by stable name.
- Write to `docs/03-design/concept-prototype/<id>.md` (the
  doc) plus any source-tool files (Houdini scenes, Blender
  files, R3F starter repo) referenced from the doc.

## Handoffs to Other Skills

- **From `concept-author`** — the creative thesis the
  prototype tests.
- **From `motion-language-author`** — the timing / easing
  rules the prototype validates.
- **From `art-direction-author`** — the visual language the
  prototype renders.
- **From `mood-board-author`** — visual references inform
  the prototype's aesthetic targets.
- **To `srs-author`** (site-build family) — prototype
  findings inform NFRs (perf budgets, asset budgets, motion
  budgets).
- **To `engineering-handoff-spec-author`** — the prototype
  is part of the handoff bundle when it doubles as the
  Phase 4 starter code.
- **To Phase 4 build** — successful prototype patterns
  graduate to production; rejected ones inform the SRS's
  "out of scope" or trigger a concept revision.

## Edge Cases

- **Prototype reveals concept is unbuildable.** The prototype's
  job. Surface honestly; either revise the concept (re-enter
  `concept-author`) or document the trade-offs in the
  prototype findings.
- **Prototype reveals motion language is unrealistic.** Same
  loop — re-enter `motion-language-author` with the
  prototype evidence.
- **Stakeholder wants the prototype as production code.**
  Refuse the conflation. The prototype is throwaway by
  design. Production patterns live in Phase 4 build, with
  proper testing, accessibility, and performance budgets.
- **Asset pipeline doesn't exist yet** (no Blender → Draco
  → KTX2 set up). Acceptable to ship the prototype with
  uncompressed assets + a finding "asset pipeline TBD";
  Phase 4 does the production pipeline work.
- **Prototype runs at 30fps on target devices.** Surface
  as a finding; the concept may need to relax (drop
  particle count, simplify shaders) OR the device tier
  may need to be re-stated.
- **Operator skips concept prototyping for an
  Awwwards-ambition project.** Surface the risk: per E2
  Lusion's Phase 2 is the lock-down phase before Phase 3
  Production; skipping it surfaces problems in production
  where they're 10× more expensive.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://docs/research/E2-agency-methodologies.md`
§C.2 (Lusion's three-phase methodology, Phase 2: Concept
Prototyping, with Houdini FX / Cinema 4D / vvvv / WebGL).
Also referenced: `docs/research/E3-technical-conventions.md`
§3 (WebGL / Three.js conventions) for the asset-pipeline
discipline. No user-invocable peer exists for this
Awwwards-tier addition.

## Self-Audit

Before declaring a concept prototype shipped, confirm:
- Runtime tool chosen with rationale tied to the prototype's
  goal.
- Scope narrowed to ≤3 hero interactions (not "the whole
  site").
- Findings document covers: what worked / what didn't / what
  compromised / asset-pipeline implications.
- 60fps target tested on the project's device tier.
- Concept + motion language + art direction cited by stable
  name.
- Prototype is treated as throwaway (or explicitly graduates
  to Phase 4 starter code with a note).
