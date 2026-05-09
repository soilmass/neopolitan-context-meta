---
name: polish-discipline-author
description: >
  Authors the project's polish phase plan — areas to polish,
  budget allocation (often 30-80% of remaining time at
  Awwwards-tier), polish gate / readiness criteria,
  per-iteration polish notes. Polish is a budgeted phase, not
  bug-fix work. Saves to docs/05-hardening/polish-plan.md and
  per-iteration docs/05-hardening/polish-notes/<iter>.md. Use
  across Phase 5 hardening, with re-application during Phase 7
  re-polish cycles. Do NOT use for: launch-day runbook (use
  runbook-author in site-build); the engineering handoff spec
  (use engineering-handoff-spec-author in site-design —
  handoff is the contract; polish is the post-handoff
  iteration); generic QA / functional testing (operator-driven;
  QA Lead owns); the optimization loop (use
  optimization-loop-author — that is post-launch
  experimentation, not polish).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. No user-invocable peer
            exists for this Awwwards-tier addition; this atom
            establishes the pattern.
---

# polish-discipline-author

Phase 5 → Phase 7 — produce the project's polish phase plan +
running polish notes.

## When to Use

- Phase 5 hardening starts; the build is feature-complete; the
  polish phase plan governs which areas get polish budget and
  in what order.
- Phase 7 re-polish cycle (uncommon but valuable for Awwwards
  resubmissions or a re-launch) — re-apply the polish
  discipline against named regressions.
- An Awwwards-tier ambition project where polish is the
  competitive moat — Active Theory's verbatim claim:
  *"polish taking about 80 percent"* of project time.
- Sponsor wants visibility into polish budget vs feature
  budget; this plan articulates the trade-off.

## When NOT to Use

- Launch-day runbook — `runbook-author` (site-build family).
  Polish is pre-launch + iteration; runbook is launch-day
  procedure.
- Engineering handoff spec — `engineering-handoff-spec-author`
  (site-design family). Handoff is the contract from Design
  to Engineering at Phase 3 close; polish is the iteration
  post-handoff.
- Generic functional QA — operator-driven via QA Lead's test
  plan. Polish is craft-iteration on the visual + interaction
  + motion + perceptual quality, not bug-finding.
- Optimization loop — `optimization-loop-author` (Tier 1
  here). Loop is post-launch hypothesis testing; polish is
  pre-launch iteration on what's already designed.
- Awards submission preparation — `awards-submission-author`
  (Tier 3). Polish is upstream of awards work.
- Per-page design tweaks during build (those happen via
  design-system + handoff; if they're piling up, polish
  budget is being spent in a fragmented way — surface that
  finding).

## Capabilities Owned

- Author the **polish budget allocation**:
  - Total polish time available (often 30-80% of remaining
    pre-launch time at Awwwards-tier; 10-20% at typical
    project tier).
  - Per-area allocation (hero / nav / forms / motion /
    accessibility / responsive / dark mode / etc.).
  - Per-iteration time-box (typically 2-3 day iteration cycles).
- Document **polish areas with priority**:
  - **Hero / above-fold** — first impression; always Tier 1.
  - **Motion polish** — easings, durations, choreography
    refinement against `motion-language-author`.
  - **Type polish** — line-height, kerning at hero size,
    optical adjustments.
  - **Microcopy polish** — button labels, error messages,
    empty states.
  - **State polish** — hover / focus / active visual finesse.
  - **Edge-case polish** — empty / error / loading states
    (per `component-states-matrix-author`).
  - **Accessibility polish** — focus indicators, ARIA
    announcements (per `a11y-annotations-author`).
  - **Performance perception polish** — skeleton screens,
    perceived speed, optimistic UI.
- Define the **polish gate / readiness criteria**:
  - "Could a member of the Awwwards jury find a Sev-1
    visual / interaction issue in the first 5 minutes?"
  - "Does each Tier 1 area meet the art direction's
    defended creative territory?"
  - "Are all 9 component states polished, not just default
    + hover?"
  - Per-area gate criteria customized to project.
- Run **per-iteration polish notes** —
  `docs/05-hardening/polish-notes/<iter>.md`:
  - What got polished this iteration.
  - What's still rough.
  - Polish budget consumed vs remaining.
  - Areas deferred to next iteration with rationale.
- Refuse **polish-as-bug-fix-scraps** — polish is intentional
  craft work; bug fixes go through the hotfix queue.
- Cite **art direction** + **motion language** + **component
  states matrix** + **a11y annotations** by stable name —
  polish iterates against them.
- Write to `docs/05-hardening/polish-plan.md` (the plan) +
  per-iteration notes.

## Handoffs to Other Skills

- **From `art-direction-author`** (site-design) — polish
  iterates against the defended visual language.
- **From `motion-language-author`** (site-design) — polish
  refines easings + durations against the motion contract.
- **From `component-states-matrix-author`** (site-design) —
  polish refines per-state visual + behavior.
- **From `a11y-annotations-author`** (site-design) — polish
  on focus / ARIA / contrast.
- **From `engineering-handoff-spec-author`** (site-design) —
  the handoff is the starting state polish iterates on.
- **To Phase 5 Gate 5** — the polish gate / readiness
  criteria are part of Gate 5 sign-off.
- **To Phase 6 launch readiness** — final polish iteration
  closes before launch.
- **To `awards-submission-author`** (Tier 3) — Awwwards-
  tier polish is the substrate the awards submission
  builds on.

## Edge Cases

- **Sponsor insists "polish is gold-plating"** and cuts the
  budget. Surface the cost: at typical-tier polish (10-20%),
  Awwwards-tier outcomes are unreachable; SOTD scoring
  (Animations 8.7 mean) requires the discipline. Document
  the trade-off; refuse silent acceptance.
- **Polish area exposes upstream design problem** (e.g.,
  the art direction can't survive responsive scrutiny).
  Halt polish on that area; trigger a
  `art-direction-author` revision; resume polish after.
- **Polish iteration runs out of budget**. Refuse to
  silently drop areas. Document explicit deferred areas
  + the trade-off. Sponsor decides whether to extend
  budget or accept reduced polish.
- **Polish becomes endless** (perfectionism creep). The
  polish gate enforces stopping. The first time a Tier 1
  area passes the gate, it's done; revisit only on
  user-evidence regression.
- **Different team members polish at different bars.**
  The polish gate criteria are objective; the discipline
  is the bar. Document divergence as a finding for
  Phase 7 retro.
- **Polish plan never authored** (operator skips this
  atom). Per A56 the discipline is the skill; surface
  that polishing without a plan tends to be ad-hoc and
  un-budgeted, leaving Awwwards-tier outcomes to chance.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://docs/research/E2-agency-methodologies.md`
§C.3 (Active Theory's "polish taking about 80 percent")
plus the SOP §8 Phase 5 hardening (which the polish phase
operates within). No user-invocable peer exists for this
Awwwards-tier addition; this atom establishes the pattern.

## Self-Audit

Before declaring a polish plan + iteration complete,
confirm:
- Total polish budget stated explicitly with rationale
  (% of remaining time).
- Per-area allocation sums to ≤100% of total.
- Polish areas prioritized (Tier 1 / Tier 2 / Tier 3).
- Polish gate / readiness criteria stated objectively
  (the Awwwards-jury 5-minute test, etc.).
- Per-iteration notes cover: what's polished + what's
  still rough + budget remaining.
- Cross-references to art direction + motion language +
  states matrix + a11y annotations by stable name.
- Areas deferred with rationale (not silently dropped).
