# Architecture Options for context-site-build v0.2 — Awwwards-tier Build-Out

> Decision document. Evidence: `docs/research/SYNTHESIS.md` and the
> three E1/E2/E3 research reports. Authored 2026-05-08. Decision
> requested before authoring proceeds.

---

## The decision

The research surfaced ~15-20 new atom-shaped capabilities the library needs to be Awwwards-tier-capable, plus stack-specific policy overlays. **How those capabilities land in the library's structure** is the question this document answers.

Four options are on the table, in order of complexity / scope:

| # | Name | Scope | Atom count | Sessions to build |
|---|---|---|---|---|
| **A** | Overlay-only | One `house-site-build-awwwards` overlay; current Tier 2/3 left unbuilt | ~5 overlay atoms | 2-3 sessions |
| **B** | Spine-only completion | Author the 10 Tier 2/3 atoms already specced; no Awwwards-specific phases | ~10 new atoms | 4-5 sessions |
| **C** | Hybrid family expansion (recommended) | Complete Tier 2/3 + bootstrap `site-design` and `site-operate` families with Awwwards-aware atoms; stack overlays | ~25-30 atoms across 3 families + overlays | 8-12 sessions |
| **D** | Full restructure | Reorganize whole library around the Awwwards 6-stage spine instead of the user's 7-phase SOP | Library re-author | Significant (replaces v0.1.x) |

---

## Option A — Overlay-only

### Scope
- Keep the current 16-atom `site-build` family unchanged.
- Author **one policy overlay**: `house-site-build-awwwards` that extends/overrides each Tier 1 atom with Awwwards-tier conventions.
  - `vision-author` overlay → adds "creative territory" + "lore" sections
  - `persona-author` overlay → adds "narrative role" framing
  - `srs-author` overlay → adds "motion language" NFR rows + WebGL performance budget
  - `runbook-author` overlay → GSAP/Lenis-specific deploy steps, CI for WPO/INP
  - `baseline-report-author` overlay → adds Awwwards-criteria scoring (Design/Usability/Creativity/Content)
- Optionally add 2-3 free-standing tool atoms: `motion-conformance-author`, `performance-budget-author`.

### Trade-offs
- **Pros**: Clean mechanism/policy separation per the meta-pipeline architecture. Same library serves any project tier (generic to Awwwards). Composable. Cheap.
- **Cons**: Overlays can override but **cannot invent new phases**. Mood Board, Concept Prototyping, Polish, Awards, Art Direction are *new phases the SOP doesn't cover* — overlay can't add them cleanly. Operators wanting Awwwards-tier work get a thinner answer than research warrants.
- **Discipline impact**: Lowest ahead-of-trigger violation (overlay is a documented mechanism in the meta-pipeline). Per A56, this is the safe choice.

### When to pick this
- If "build out fully" turns out to mean "add the operator's preferred polish on top of the current methodology" rather than "expand the methodology itself."
- If real Awwwards-tier work is months away and the overlay is a hedge.

---

## Option B — Spine-only completion (existing Tier 2/3)

### Scope
- Author the **10 Tier 2/3 atoms already specced** in `skills/site-build/taxonomy.md`:
  - Tier 2 (5): `kpi-author`, `risk-register-author`, `threat-model-author`, `privacy-plan-author`, `master-schedule-author`
  - Tier 3 (5): `ost-author`, `stakeholder-map-author`, `design-philosophy-author`, `weekly-metric-report-author`, `change-request-author`
- Skip the Awwwards-specific phases entirely (Art Direction, Concept Prototyping, Polish, Awards, Mood Board, Motion Language).
- Skip stack-specific overlays.

### Trade-offs
- **Pros**: Honest progression toward "fully built site-build family per the existing taxonomy." Closes the in-family deferred work surfaced in v0.1.0/v0.1.2. Architecturally clean — completes what was already specced.
- **Cons**: **Ignores the user's stated goal** ("deliver Awwwards-level"). The completed library will be capable of producing well-documented but generic-quality sites. None of the secret-sauce phases land. The library does NOT become Awwwards-tier.
- **Discipline impact**: Zero — this is just executing on what was already specced.

### When to pick this
- If the user later decided their primary goal is *complete the SOP*, not *match Awwwards conventions*.
- If "research methodologies" was reconnaissance for a future expansion, but this iteration is just "fill out what we have."

---

## Option C — Hybrid family expansion (recommended)

### Scope

#### Phase 1: Complete the existing site-build family (≈5 sessions)
Author the 10 Tier 2/3 atoms already specced in `taxonomy.md`. Same as Option B.

#### Phase 2: Bootstrap `site-design` family (≈3-4 sessions)
A new family covering Phase 3 design + the Awwwards-tier "art direction" phases. Tier 1 atoms (proposed):
- `art-direction-author` — produces the Art Direction document (mood, palette, type, motion vocabulary)
- `mood-board-author` — produces the Mood Board + Reference list (Lusion's Phase 1)
- `concept-author` — produces the Concept document (creative territory, narrative, lore)
- `motion-language-author` — produces the Motion Language doc (timing, easing, choreography rules; tokens)
- `design-system-tokens-author` — DTCG → Style Dictionary → CSS vars (folds in Phase 3 deliverable)
- `component-states-matrix-author` — 9-state matrix per component (folds in Phase 3 deliverable)
- `engineering-handoff-spec-author` — Design→Engineering contract (folds in Phase 3 deliverable)

Out of scope for this family but specced in coverage.md: `usability-synthesis-author`, `discovery-tick-author` (Phase 4 — too small to bootstrap a separate family).

#### Phase 3: Bootstrap `site-operate` family (≈3-4 sessions)
A new family covering Phase 5/6/7 operations + the Awwwards-tier "polish + awards" phases. Tier 1 atoms (proposed):
- `polish-discipline-author` — produces the Polish phase plan + checklist (the budgeted phase, not bug-fix scraps)
- `awards-submission-author` — produces the SOTD/Honors submission package (case-study writeup, screenshots, video, jury narrative)
- `concept-prototyping-author` — produces the 3D/runtime concept prototype + iteration log (Lusion's Phase 2 in code)
- `launch-comms-author` — internal/external/status-page launch communications
- `conformance-statement-author` — WCAG-EM-flavored a11y conformance statement (folds in Phase 5)
- `optimization-loop-author` — single experimentation cycle
- `optimization-backlog-author` — prioritized optimization backlog
- `stabilization-report-author`, `hypercare-digest-author` — Phase 7 stabilization (folds in)
- `weekly-metric-report-author`, `monthly-stakeholder-report-author`, `qbr-author`, `annual-retro-author` — cadence reports

#### Phase 4: Stack-specific policy overlays (≈2-3 sessions, optional)
- `house-site-build-r3f` — React Three Fiber + drei + GSAP + Lenis conventions
- `house-site-build-nextjs` — Next.js App Router + Vercel + Sanity patterns
- `house-site-build-astro` — Astro static + WebGL islands pattern
- (Optional, lower priority) `house-site-build-svelte`, `house-site-build-nuxt`

#### Phase 5: Cross-cutting tool atoms (≈1-2 sessions)
- `performance-budget-author` — concrete budgets per page type (marketing, WebGL hero); CI enforcement spec
- `motion-conformance-author` — `prefers-reduced-motion` opt-in CSS, focus-visible parity, keyboard-on-scroll-jacked, lite-mode alternative

### Trade-offs
- **Pros**: Architecturally honest. Each family handles a coherent scope. Awwwards-tier atoms live where they belong (in `site-design` for visual phases; in `site-operate` for delivery phases). Mechanism/policy separation maintained via stack overlays. Completes deferred Tier 2/3 work as a side effect of Phase 1. Each phase is independently shippable; we land Phase 1, then decide whether to continue.
- **Cons**: Multi-month commitment. Three families is more cognitive load than one. Some atoms have ambiguous family membership (e.g. `polish-discipline-author` could go in either `site-build` or `site-operate`).
- **Discipline impact**: Each new atom is **ahead of trigger** in the v0.7.0 sense. Per A56, requires explicit operator approval for the discipline shift — which the user's "build out fully" message provides. The discipline-restoration commitment in A56 should be re-affirmed: future libraries that operators bootstrap should not silently re-break it.

### Multi-PR strategy
Each phase is its own PR off the previous merged PR:
- PR #2: Phase 1 (Tier 2/3 atom completion) → merge to main
- PR #3: Phase 2 (`site-design` family bootstrap)
- PR #4: Phase 3 (`site-operate` family bootstrap)
- PR #5: Phase 4 (stack overlays)
- PR #6: Phase 5 (cross-cutting tools)

Operator can stop after any PR; the library remains shippable at every checkpoint.

### When to pick this
- If "build out fully + deliver Awwwards-tier" is the genuine goal.
- If multi-session commitment is acceptable.
- **This is the recommended path.**

---

## Option D — Full restructure around the Awwwards 6-stage spine

### Scope
Replace the 7-phase SOP organization with the Awwwards-tier 6-stage spine:
- `discovery` family (Stage 1)
- `concept` family (Stage 2)
- `art-direction` family (Stage 3)
- `prototyping` family (Stage 4)
- `production` family (Stage 5)
- `launch-polish-awards` family (Stage 6)

The current `site-build` family is decommissioned via `skill-refactor` + `skill-retire`. v0.2.0 of context-site-build is a **MAJOR bump** (per the meta-pipeline VERSIONING-POLICY).

### Trade-offs
- **Pros**: Library structure mirrors the Awwwards-tier methodology cleanly. Vocabulary aligns with what 20+ top agencies actually use. Strongest signal of "this library is for Awwwards-tier work."
- **Cons**: Discards the user's chosen 7-phase SOP structure as the organizing principle. The user's existing `draft-*` skills + the SOP doc still use 7 phases — there will be persistent vocabulary collision between the methodology authority (7 phases) and the library structure (6 stages).
- **Discipline impact**: Largest. Re-authoring the library v0.1 → v0.2 is a MAJOR bump that cascades to every consumer. PR #1's content gets retired before it lands externally.

### When to pick this
- Only if the user is willing to fork the methodology — i.e., update `internal://site-build-procedure.md` to reflect the 6-stage spine, making the new library and the SOP agree.
- Not recommended unless the user wants the existing SOP retired in favor of an explicitly Awwwards-tier methodology.

---

## Recommendation

**Option C — Hybrid family expansion.** Specifically:

1. **Now**: confirm Phase 1 scope (the 10 Tier 2/3 atoms already specced). Land it as PR #2 on a new branch off `feat/context-site-build` (or off `main` after PR #1 merges).
2. **Decide between Phase 2 paths**: either (a) full `site-design` family bootstrap, or (b) Awwwards-overlay on the current Tier 1 atoms first as a thinner experiment. Phase 2 is the biggest single decision; the overlay variant is a hedge if the user wants to validate appetite before bootstrapping a new family.
3. **Phase 3 onward** (`site-operate`, stack overlays, cross-cutting tools) is committed only after Phase 2 lands and the operator decides whether Phase 1+2 is "enough" or to keep going.

This shape matches A56's discipline: each phase is operator-approved at its boundary; the work is checkpoint-shippable; library remains coherent throughout.

---

## What I need to know before starting

1. **Which option above?** A / B / C / D.
2. **PR strategy**: stack PR #2 on `feat/context-site-build`, or merge PR #1 first and branch off main?
3. **SOP access**: do you want me to read `site-build-procedure.md` directly so atoms can cite specific section numbers, or work from the user-invocable `draft-*` skill descriptions (which is what v0.1.x did)?
4. **Discipline re-affirmation**: per A56, ahead-of-trigger expansion needs explicit approval. Is "yes, build out fully toward Awwwards-tier" enough, or do you want the v0.7.0 disclosure-pattern (top-of-file marker on each pre-trigger atom)?
5. **Stack preference**: when stack overlays come (Phase 4 of Option C), which combos do you want first — A (Next.js), B (Nuxt), C (Astro), D (SvelteKit)? Or all four equally?
