---
name: prototype-author
description: >
  Authors a clickable prototype for usability testing — Figma /
  Framer / coded prototype that stitches mid-fi or hi-fi wireframes
  into a navigable flow. Tests the top 3-5 user tasks identified in
  Phase 2 with happy paths plus the most likely error paths. Writes
  the prototype spec to docs/03-design/prototypes/<id>.md and links
  the prototype URL (SOP §6.3.1). Use after wireframes (mid-fi or
  hi-fi) ship and before usability testing. Do NOT use for:
  authoring wireframes (use wireframe-author); 3D / runtime concept
  prototypes (use concept-prototyping-author — different fidelity,
  different tool, different goal); usability test design or
  synthesis (use usability-synthesis-author — that covers both
  test design and analysis); production code (Phase 4 build);
  authoring the SRS (use srs-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
---

# prototype-author

Phase 3 — produce a clickable prototype for usability testing.

## When to Use

- Phase 3 Design is in progress; mid-fi or hi-fi wireframes
  exist for the feature areas being tested; the next step is
  testing them with real users.
- Phase 2 identified the top 3-5 user tasks; the prototype
  needs to cover those flows end-to-end.
- A specific design hypothesis ("does our checkout flow work
  for first-time buyers?") needs validation before code is
  written.
- A redesigned area needs re-prototyping for a follow-up
  usability round.

## When NOT to Use

- Wireframes don't exist for the flow — `wireframe-author`
  first. Prototyping without wireframes is designing
  on-the-fly during prototyping (slow + low-quality).
- 3D / runtime concept prototype — that's
  `concept-prototyping-author`. Different fidelity (real-time
  vs click-through), different tool (Houdini / WebGL vs
  Figma / Framer), different goal (technical-feasibility vs
  flow-feasibility).
- Usability test *design* (questions to ask, success
  criteria) or *synthesis* (analyzing results) —
  `usability-synthesis-author` covers both.
- Per-component state matrices — `component-states-matrix-
  author`.
- Production code — Phase 4 build.
- Authoring the SRS — `srs-author`. Prototype findings inform
  the SRS but the prototype isn't a spec.
- A polished marketing demo — prototypes are for testing,
  not pitching. (If a sponsor demo is needed, clearly
  separate "test prototype" from "demo prototype" and don't
  conflate.)

## Capabilities Owned

- **Pick the prototype tool** per goal:
  - **Figma** — most common; cheap; good for click-through.
  - **Framer** — when Figma's interactions aren't enough
    (variants, complex hover states, simulated data).
  - **Coded prototype** — highest fidelity, highest cost;
    only when fidelity gap matters for the test result.
- **Scope the prototype** to top 3-5 user tasks (per SOP
  §6.3.1). Refuse a "prototype the whole site" scope; that's
  building the site.
- Cover **happy paths plus the most likely error paths**.
  Empty states, error messages, loading states for the
  flows tested.
- Use **real content where possible** (per SOP §6.3.1: "test
  users notice lorem ipsum"). Stitch in real product names,
  pricing, copy.
- Stitch the prototype together at a **fidelity that doesn't
  distract from the task** — usually mid-fi for early
  testing; hi-fi for final validation.
- Document the **prototype scope spec** at
  `docs/03-design/prototypes/<id>.md`:
  - Tasks covered (with stable IDs).
  - Fidelity level + tool.
  - Real content sources.
  - Known gaps (parts of the site not in the prototype).
  - Link to the prototype URL.
- Cite the **wireframes** (mid-fi or hi-fi) by stable name
  + path; cite the **user tasks** from Phase 2 user-flow work.

## Handoffs to Other Skills

- **From `wireframe-author`** — wireframes are the input;
  prototype stitches them.
- **From `srs-author`** — Phase 2 user-flows define the
  tasks tested.
- **From `art-direction-author`** + **`design-tokens-author`**
  (transitively, when hi-fi).
- **To `usability-synthesis-author`** — the prototype is
  what gets tested; usability synthesis analyzes the test
  results.
- **To `wireframe-author`** — usability findings often
  trigger wireframe revision.
- **To `engineering-handoff-spec-author`** — the prototype
  is part of the handoff bundle when usability validates
  hi-fi.

## Edge Cases

- **Stakeholder wants 100% coverage** (every page in the
  prototype). Refuse — top 3-5 tasks is the discipline.
  Beyond that, prototyping cost exceeds the value of the
  test signal. The site itself is the full coverage.
- **Real content not available.** Halt or partner with
  content lead. Per SOP §6.7 anti-pattern "lorem ipsum in
  usability testing" — signal degraded.
- **Prototype tool can't do the interaction needed**
  (e.g., Figma can't simulate a complex state machine).
  Either escalate to Framer / coded, OR accept the
  limitation and design the test around it.
- **Prototype + production code diverge during Phase 4.**
  Expected — prototype is throwaway. Don't try to keep
  prototype and code in sync; let prototype age out.
- **Sponsor wants to show the prototype to executives as a
  demo.** Surface the conflation risk; separate test
  prototype from demo prototype if needed (different
  fidelity, different polish).

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §6.3.1.

## Self-Audit

Before declaring a prototype shipped for testing,
confirm:
- Tool chosen with rationale.
- Scope is top 3-5 user tasks (not "the whole site").
- Happy paths + likely error paths covered.
- Real content used (no lorem ipsum).
- Fidelity matches the test goal.
- Prototype URL + spec doc both shipped.
- Wireframes + user tasks cited by stable name.
