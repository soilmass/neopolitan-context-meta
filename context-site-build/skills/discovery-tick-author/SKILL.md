---
name: discovery-tick-author
description: >
  Authors the weekly continuous-discovery synthesis during Phase 4
  Build — pulls the past week's user-research signal (interview
  notes, analytics shifts, support tickets, A/B test results) into
  a one-page memo for the product trio with 1–3 backlog candidates
  in hypothesis form. Writes to
  docs/04-build/discovery/weekly/<YYYY-WW>.md (SOP §7.5 + §2.3
  continuous discovery). Use weekly during Phase 4 when the
  product trio has committed to a continuous-discovery cadence.
  Do NOT use for: Phase 1 user research synthesis (use
  persona-author + ost-author in site-build family); usability
  test synthesis from Phase 3 (use usability-synthesis-author —
  that is per-prototype; this is per-week); writing the post-launch
  baseline report (use baseline-report-author in site-build
  family); writing the SRS (use srs-author); writing the
  optimization backlog (Phase 7 artifact in future site-operate
  family; user-invocable draft-optimization-backlog covers it now).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
            Modeled on the user-invocable discovery-tick skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# discovery-tick-author

Phase 4 — produce the weekly continuous-discovery memo.

## When to Use

- Phase 4 Build is in progress; the product trio (PdM + Tech
  Lead + Lead Designer) has committed to a continuous-
  discovery cadence (per SOP §7.5).
- The end of a Phase 4 sprint (or end-of-week, depending on
  cadence) — the memo synthesizes the week's discovery
  signal.
- A discovery anomaly has surfaced mid-week that warrants
  immediate triage rather than waiting for the regular
  cadence.
- A pre-Phase-7 transition memo when continuous discovery
  is handing off to post-launch optimization.

## When NOT to Use

- Phase 1 user research synthesis — that's done via
  `persona-author` (synthesis into personas) and
  `ost-author` (mapping into opportunities); both in the
  site-build family.
- Phase 3 usability test synthesis — `usability-synthesis-
  author` covers per-prototype testing rounds. Discovery-
  tick is per-week; usability synthesis is per-test-round.
- Phase 7 post-launch baseline report —
  `baseline-report-author` (site-build family).
- Writing the SRS — `srs-author`. Discovery findings inform
  but don't replace the SRS.
- Writing the optimization backlog — Phase 7 artifact in a
  future `site-operate` family. The user-invocable
  `draft-optimization-backlog` covers it now.
- Replacing user research itself — discovery-tick *
  synthesizes* the week's research; it doesn't *do* the
  research (interviews, surveys, analytics review).
- A standalone weekly status report — that's
  `weekly-metric-report-author` (Phase 7, site-build
  family). Discovery tick is research-focused; metric
  report is metric-focused.

## Capabilities Owned

- **Pull the week's signal** from named sources:
  - Interview notes (≥1 interview per week is the
    continuous-discovery cadence per Teresa Torres'
    "weekly user contact").
  - Analytics shifts (GA4 / Mixpanel / PostHog) — what
    behavior changed week-over-week.
  - Support tickets — what users complained about.
  - A/B test interim signal (without peeking at
    significance — per SOP §10.6 anti-pattern).
  - Sales / customer-success input — what objections /
    questions surfaced.
- Synthesize into **one-page memo** for the product trio:
  - **What we heard** — themes across the week's signal.
  - **What surprised us** — patterns that contradict
    assumptions.
  - **What's stable** — observations that confirm
    existing model.
  - **Open questions** — what we don't know yet, what
    next week's research should target.
- Produce **1–3 backlog candidates in hypothesis form**:
  - Format: *"We believe <change> will <effect> for
    <users> because <evidence>. We will know we're right
    if <signal> within <time>. We are wrong if
    <counter-signal>."* (per SOP §10.3.1 experimentation
    loop hypothesis form).
- Cite **personas** (the segments the signal came from),
  the **OST** (where the candidate sits in the tree), and
  named research sessions (interview IDs, analytics
  segments) by stable handle.
- Write to `docs/04-build/discovery/weekly/<YYYY-WW>.md`
  (ISO week numbering).

## Handoffs to Other Skills

- **From the week's discovery activities** — interviews,
  analytics, support, A/B tests. Operator-driven; this
  atom synthesizes them.
- **From `persona-author`** (site-build family) — personas
  are the segments the signal organizes around.
- **From `ost-author`** (site-build family) — backlog
  candidates land on the OST's solution branches.
- **To `srs-author`** — high-confidence findings update
  the SRS (FR adjustments, NFR refinements).
- **To Phase 4 sprint planning** — backlog candidates
  flow into the next sprint's prioritization.
- **To Phase 7 optimization** — at Phase 4 → Phase 7
  transition, the discovery cadence either continues into
  Phase 7 (often) or hands off to the
  `optimization-loop` workflow (future site-operate
  family).
- **From the user-invocable `discovery-tick`** — peer
  skill producing the same artifact via a different
  procedure.

## Edge Cases

- **No discovery activity happened this week.** Surface
  honestly; the memo says "no contact this week, here's
  why" — don't fabricate signal. If it persists for >2
  weeks, the continuous-discovery commitment is broken;
  escalate.
- **A finding is unambiguous and high-confidence.**
  Don't wait for the next sprint to act — surface as an
  immediate-action item with named owner. The weekly
  cadence is the floor, not the ceiling.
- **Findings contradict the OST** (a persona pain we
  thought was real isn't, or vice versa). The OST is a
  living artifact; trigger a re-enter of `ost-author`.
- **Findings contradict the vision.** Halt; this is an
  upstream signal warranting product trio + sponsor
  review. Memo flags it explicitly; doesn't paper over.
- **Stakeholder wants the memo to be a polished
  presentation.** Refuse the polish creep; this is a
  working memo for the product trio (per §7.5). Polished
  versions can be derived for the broader audience but
  the working memo stays lightweight.
- **Multiple weeks of memos pile up un-actioned.** The
  point of the cadence is action; un-actioned memos
  surface a process dysfunction. Memo flags accumulating
  un-actioned candidates; trio retro should address.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §7.5
(Continuous Discovery During Build) plus §2.3 (continuous
discovery as a parallel track to delivery). Teresa Torres'
"Continuous Discovery Habits" is the named industry
reference. The user-invocable `discovery-tick` is a peer
skill producing the same artifact via a different
procedure.

## Self-Audit

Before declaring a discovery-tick memo complete, confirm:
- Sources cited (interview IDs, analytics segments,
  ticket IDs).
- Themes synthesized across ≥2 sources (no single-source
  findings claimed as "patterns").
- 1–3 backlog candidates in hypothesis form (with named
  signal and counter-signal).
- Personas + OST cited by stable handle.
- Open questions captured for next week's research.
- Memo is ≤1 page rendered (working memo, not
  presentation).
- ISO week numbering correct.
