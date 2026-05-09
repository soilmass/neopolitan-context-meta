# Awwwards-Tier Synthesis

> Consolidates findings from `E1-awwwards-judging-and-winners.md`,
> `E2-agency-methodologies.md`, and `E3-technical-conventions.md`
> (research conducted 2026-05-08). This doc is the load-bearing
> input for `docs/ARCHITECTURE-OPTIONS-v0.2.md` — what the library
> needs to teach skills about, in priority order.

The research findings cluster into eight load-bearing observations. Each shapes a specific category of skill the library should produce.

---

## 1. The Awwwards-tier methodology spine is 6 stages, not 5

Verified across ~20 top agencies. Spine + canonical vocabulary:

| # | Stage | Verbatim vocabulary |
|---|---|---|
| 1 | **Discovery / Strategy** | "Discovery" / "Strategy" / "Empathize" / "Kickoff" |
| 2 | **Concept / Creative Direction** | "Concept" / "Innovative Concepts" / "Ideation" / "Creative Direction" / "Lore & narrative" |
| 3 | **Art Direction / Visual Direction** | "Art Direction" / "Visual Direction" / "Mood Board and Visual References" / "Artistic Direction" (Bonhomme) |
| 4 | **Prototyping** | "Concept Prototyping" / "Innovation Sprints & Prototyping" / "Wireframing & prototyping" |
| 5 | **Design + Development (often parallel)** | "Building" / "Production" / "Designing with Code" |
| 6 | **Launch / Wrap-up / Polish / Awards** | "Wrap-up" + "Project launch" + "Follow-up" + "Awards (optional)" |

**Two stages are missing from the user's existing site-build SOP** (which is 7-phase but maps to the conventional 5-stage software process):

- **Art Direction** as a *named, billable phase* between Concept and Design.
- **Polish + Awards** as a final phase distinct from "QA" or "launch."

The current `context-site-build` Tier 1 covers parts of stages 1, 2, 5, 6 implicitly. **Stages 3 (Art Direction) and 4 (Concept Prototyping) are unaddressed.**

## 2. Awwwards judging weights are publicly documented

| Criterion | Weight |
|---|---|
| **Design** | 40% |
| **Usability** | 30% |
| **Creativity** | 20% |
| **Content** | 10% |

Plus six dev-award sub-scores (≥7.0 average for Developer Award): Animations/Transitions, Responsive Design, WPO, Semantics/SEO, Accessibility, Markup/Meta-data.

**Implication for the skill library**: the Self-Audit checks at the end of every atom should reference Awwwards-relevant criteria. Two-color palette discipline is a Design lever; semantic markup + a11y cover the dev-award downside.

## 3. The "secret sauce" is three named phases most SOPs lack

The agencies that consistently win Awwwards have these phases as *first-class deliverables*:

1. **Mood Board / Reference Phase** — a billable, sign-offable deliverable. Lusion's Phase 1.
2. **Concept Prototyping in 3D/runtime tools** (Houdini, Cinema 4D, vvvv, WebGL) before the brief is signed. NOT Figma. Lusion's Phase 2.
3. **Polish as a named phase consuming 30-80% of project time**. Active Theory's verbatim claim: *"polish taking about 80 percent."*

Plus three more rare-but-distinctive:

4. **Three-fidelity prototype ladder** (Hello Monday): paper → low-fi → high-fi.
5. **Awards Phase as an explicit, optional project step** (Ueno).
6. **Project Filter / Brief Triage** (Hello Monday "the Fs" — 8 alliterative criteria).

**Implication**: there are at minimum 3-6 atoms the library doesn't currently have, each producing a named, time-boxed deliverable.

## 4. The composite winning stack is now well-defined

**Highest-probability stack for an Awwwards-tier site in 2025–2026**:

> **Nuxt 3 (Vue) or Next.js (React)** + **vanilla Three.js or R3F** + **GSAP + ScrollTrigger** + **Lenis** + **Sanity / Storyblok / Contentful** + **Vercel**, with **Blender → Draco-compressed glTF + KTX2 textures**, optional **Web Audio API** for narrative sound, optional **Rive** for 3D motion.

Four canonical combos by stack:
- **A — React-cinematic**: Next.js + R3F + drei + GSAP + Lenis + Sanity + Vercel
- **B — Vue/Nuxt-cinematic**: Nuxt 3 + TresJS + GSAP + Storyblok + Vercel
- **C — Astro-static-with-WebGL-islands**: Astro + Three.js + GSAP + Lenis (>50% pass CWV)
- **D — SvelteKit performance-pure**: Svelte + vanilla Three.js + GSAP (Igloo Inc tier)

GSAP went **fully free under MIT in mid-2024** (Webflow acquisition) — historical licensing friction is gone.

**Implication**: the library should ship stack-specific *policy overlays* (`house-site-build-r3f`, `house-site-build-nextjs`, `house-site-build-astro`) that encode the stack's specific conventions atop the generic mechanism atoms.

## 5. Performance reality differs from Lighthouse-green myth

- WPO scores in Awwwards SOTY winners range **6.80–8.80**, mean ~7.7/10.
- **Only 48% of mobile pages pass all three CWV** (HTTP Archive 2025 Web Almanac).
- The trick winning sites use: **HTML element is the LCP, canvas initialises behind it, swap on ready**. Without this, 4G LCP routinely fails.
- **INP is the real Achilles heel** of WebGL + scroll-jacked sites (300-500ms on mid-range Android).

Concrete budgets:
- Critical-path JS ≤130-170 KB (marketing) / ≤200 KB excluding three.js core (WebGL)
- Total page weight ≤2 MB (marketing) / 3-6 MB acceptable for WebGL (10 MB+ danger)
- ≤100 draw calls/frame at 60fps; ≤3 active lights with shadows; ≤100 MB GPU VRAM with KTX2

**Implication**: the library needs a `performance-budget-author` atom that codifies these numbers AND a `lcp-strategy` reference for the HTML-LCP-then-canvas pattern. It should NOT prescribe Lighthouse 100 — that contradicts winning practice.

## 6. Accessibility on motion-heavy sites is honestly weak across the tier

Mean Accessibility sub-score on 12 SOTY winners reviewed: **7.0/10** (vs Animations 8.7/10).

Six WCAG 2.2 success criteria are routinely violated on Awwwards-tier sites:
- 2.1.1 Keyboard (A) — custom cursors and drag-only interactions break this
- 2.2.2 Pause/Stop/Hide (A) — hero loops rarely have a pause control
- 2.3.3 Animation from Interactions (AAA) — only honoured via `prefers-reduced-motion`, often not even that
- 2.4.7 Focus Visible (AA) — custom cursors suppress focus rings
- 2.5.7 Dragging Movements (AA, new in 2.2) — drag-to-explore fails
- 2.5.8 Target Size 24×24 (AA, new in 2.2) — tight cursor UIs fail

Three flavours of `prefers-reduced-motion` honoring: hard-disable / soft-degrade / alternative experience. The "opt-in" pattern (write base CSS without motion, layer it inside `@media (prefers-reduced-motion: no-preference)`) makes "no motion" the safe default.

**Implication**: the library should ship an explicit `motion-conformance-author` atom that produces a motion-a11y posture doc with: `prefers-reduced-motion` opt-in CSS, global motion toggle, focus-visible parity for custom cursors, keyboard scroll bindings, and a non-WebGL "lite mode" alternative experience. **Be honest** that automated tools catch only 30-40% of real barriers.

## 7. Vocabulary upgrade is non-trivial

Awwwards-tier vocabulary is *materially different* from generic web-agency talk. 25 terms with verbatim sources documented in E2 §(E). Most-impactful upgrades for the library's atom names:

| Generic term | Awwwards-tier term | Why |
|---|---|---|
| Visual design | **Art Direction** | Upstream of UI; has its own owner; governs all visual decisions |
| Idea / brief | **Concept** | Time-boxed, sign-offable artefact with its own approval gate |
| Style direction | **Creative Territory** | A defended creative zone, survives revisions |
| Animations | **Motion Language / Animation Principles** | A documented system of timing/easing/choreography |
| Copy | **Narrative / Lore** | Interactive thread through experience, separate from copywriting |
| Long-form page | **Narrative Scroll / Scrollytelling** | Choreographed content reveals on scroll |
| Microsite | **Microverse** | Persistent, social, 3D — designed for long sessions |
| QA | **Polish** | Budgeted, intentional phase — not bug-fix scraps |
| Side project | **Lab / Labs** | Named, staffed, rotating R&D incubator |
| Custom / bespoke | **Build from scratch** | Per-project tech stack, design system, even tooling |
| Project criteria | **The Fs / Project filter** | Brief-triage built into methodology |

**Implication**: existing atom names like `vision-author` and `srs-author` are fine for the strategic spine, but new atoms covering the secret-sauce phases should use Awwwards-tier vocabulary: `concept-author`, `art-direction-author`, `mood-board-author`, `motion-language-author`, `polish-discipline-author`.

## 8. Tooling conventions are rapidly converging

W3C DTCG specification reached stable Oct 2025. The canonical token pipeline is now:

```
Figma + Tokens Studio
     ↓ (DTCG JSON export)
Style Dictionary v4
     ↓ (transforms)
CSS variables + Tailwind v4 @theme + TypeScript types
```

Plus the 9-state component matrix as a hard contract: default / hover / focus / focus-visible / active / disabled / loading / error / empty / skeleton.

**Implication**: the library needs `design-tokens-author`, `component-states-matrix-author` (already specced in Tier 3) atoms that codify the W3C DTCG → Style Dictionary → CSS-vars+Tailwind pipeline as the canonical convention.

---

## What this means for the library's evolution

The current `context-site-build` v0.1.2 has 6 Tier 1 atoms covering the 7-phase SOP spine. The research surfaces three categories of gap:

### Category A — Atoms missing from the methodology spine
The SOP's 7 phases conflated some of the Awwwards-tier 6 stages, particularly:
- **Art Direction** (between Concept and Design — currently absent)
- **Concept Prototyping** (Phase 2 of Lusion's three-phase model — currently absent)
- **Polish discipline** (Phase 6 named phase — currently absent)
- **Awards submission** (the optional but named Phase 7 of Ueno — currently absent)
- **Mood Board / Reference list** (Phase 1 of Lusion's three-phase model — currently absent)

Plus the ten Tier 2/3 atoms already specced in `taxonomy.md`.

### Category B — Stack-specific policy overlays
Each of the four canonical stack combos warrants a `house-site-build-<stack>` overlay encoding:
- The stack's specific motion stack (R3F + drei vs vanilla Three.js)
- The stack's CMS conventions
- The stack's performance budget specifics
- The stack's a11y patterns (e.g. Astro's progressive enhancement vs Next.js's hydration)

### Category C — Cross-cutting performance + a11y discipline
- Performance budget atom (concrete numbers; CI enforcement)
- LCP-on-WebGL strategy reference
- Motion conformance / prefers-reduced-motion atom
- Keyboard-on-scroll-jacked atom
- Token pipeline atom (DTCG → Style Dictionary → CSS vars)
- Component states matrix atom (already specced; promote to Tier 1)
- Motion language / motion tokens atom (currently absent)

These three categories suggest **at minimum 15-20 new atoms** plus stack overlays. That's a multi-month build-out, not a single PR.

The next document, `ARCHITECTURE-OPTIONS-v0.2.md`, proposes 3-4 architectural paths for landing this work.
