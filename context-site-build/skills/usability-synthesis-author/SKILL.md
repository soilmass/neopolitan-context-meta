---
name: usability-synthesis-author
description: >
  Authors the Usability Test Synthesis covering test design
  (tasks, success criteria, probes) and post-test analysis with
  severity-ranked issues and recommended fixes. Sev-1 blockers
  must resolve before Phase 3 exit; Sev-2 flows to Phase 4
  sprint planning; Sev-3+ flows to the optimization backlog.
  Writes to docs/03-design/usability/<round>.md (SOP §6.3.2 +
  §6.3.3). Use after prototype-author runs and 5+ users complete
  tasks. Do NOT use for: authoring the prototype (use prototype-
  author); authoring wireframes (use wireframe-author);
  recruiting participants or running test sessions (operator-
  driven, not a skill); production code (Phase 4 build);
  authoring the SRS (use srs-author — usability findings inform
  but don't replace it); Phase 7 ongoing usability monitoring
  (out of scope for this family).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
            Modeled on the user-invocable synthesize-usability-notes
            skill but conformed to meta-pipeline frontmatter /
            required-section discipline.
---

# usability-synthesis-author

Phase 3 — design and synthesize one round of usability testing.

## When to Use

- Phase 3 Design is in progress; a clickable prototype exists;
  ≥5 users from the target audience have been (or are about
  to be) tested.
- A re-test is needed after wireframe / prototype revisions
  (per SOP §6.3.4 continuous testing).
- A specific hypothesis-driven test is being run on a single
  flow that's been redesigned.
- The Phase 3 Gate looms and the project needs the usability
  sign-off (no open Sev-1 issues per SOP §6.8 Gate 3 criteria).

## When NOT to Use

- The prototype doesn't exist — `prototype-author` first.
  Testing without a prototype is testing on hopes.
- Authoring the prototype itself — `prototype-author`.
- Authoring wireframes — `wireframe-author`.
- Recruiting participants or running test sessions —
  operator-driven activities, not skill-driven. The
  facilitator + note-taker model per SOP §6.3.2 is procedural.
- Production code — Phase 4 build.
- Authoring the SRS — `srs-author`. Usability findings
  inform NFRs (e.g., "task completion rate >80%") but the
  SRS is its own artifact.
- Phase 7 ongoing usability monitoring (post-launch session
  replays, heatmaps) — out of scope for this family;
  belongs to the future `site-operate` family.

## Capabilities Owned

- Author the **usability test design** per SOP §6.3.2:
  - Per task: **task description** in the user's language;
    **success criteria** (what does completion look like?);
    **probes** (questions when stuck or unexpected paths).
  - Per session: 30–45 min; **think-aloud protocol**;
    recorded with consent; one facilitator + one note-taker
    (typically the product trio rotates).
- Document the **test setup**:
  - Round number / hypothesis being tested.
  - Recruitment criteria (which persona segment).
  - Test environment (remote / in-person; tool — Maze,
    UserTesting, Lyssna, etc.).
  - Test moderator + note-taker named.
- Synthesize the **post-test analysis** per SOP §6.3.3:
  - **Per issue**: severity (Sev-1 blocker / Sev-2 critical
    / Sev-3 important / Sev-4 cosmetic), frequency (how
    many users hit it), recommended fix, trade-offs.
  - **Sev-1 issues** must resolve before exiting Phase 3
    (per SOP §6.8 Gate 3).
  - **Sev-2 issues** flow to Phase 4 sprint planning.
  - **Sev-3+ issues** flow to the post-launch optimization
    backlog.
- Document **patterns across users** — issues hit by ≥3 of
  the 5+ users are systemic; issues hit by 1 user are
  outliers (still log them, but don't over-weight).
- Cite the **prototype** + **wireframes** + **personas** +
  **user tasks** by stable name.
- Write to `docs/03-design/usability/<round>.md` (one doc
  per testing round).

## Handoffs to Other Skills

- **From `prototype-author`** — the prototype is what's
  tested.
- **From `wireframe-author`** — wireframes inform what's
  in scope for testing.
- **From `persona-author`** (site-build family) — recruitment
  criteria reference personas.
- **From Phase 2 user-flow work** (per `srs-author` §5.2.4) —
  the top 5-10 user tasks define the test scope.
- **To `wireframe-author`** — Sev-1 issues trigger wireframe
  revision.
- **To `prototype-author`** — re-prototyping after revisions
  often follows.
- **To `srs-author`** — usability NFRs (task completion rate,
  task completion time) update with test results.
- **To Phase 4 sprint planning** — Sev-2 issues land here.
- **To future `site-operate` family** — Sev-3+ issues land
  in the post-launch optimization backlog.
- **From the user-invocable `synthesize-usability-notes`** —
  peer skill (note: name doesn't have `-author` suffix in
  the user-invocable variant; same artifact via different
  procedure).

## Edge Cases

- **Fewer than 5 users tested.** Surface the limitation;
  results are directional only, not statistically meaningful.
  Per Nielsen, 5 users surface ~85% of issues; below 5,
  signal is sparse.
- **No Sev-1 issues found.** Acceptable but flag for
  scrutiny — either the test was easy (recruitment problem),
  the prototype is genuinely solid, or the facilitator
  missed signal. Re-watch sessions if confidence is low.
- **All Sev-1 issues need wireframe re-do.** Revise
  wireframes; re-prototype; re-test. The iteration loop is
  the value.
- **Stakeholder dismisses Sev-1 as "edge case."** Refuse the
  reduction. Sev-1 = task cannot be completed by multiple
  users. That's the gate criterion per SOP §6.8 Gate 3.
- **Recruiting failed** (couldn't get 5 target-persona
  users). Surface as a research-not-design issue; consider
  proxy recruitment (closest persona match) but document
  the validity gap.
- **Test reveals the concept is wrong** (not just the
  prototype). Halt; this is an upstream finding. Re-enter
  `concept-author` or `vision-author` work as needed.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §6.3.2 +
§6.3.3. The user-invocable `synthesize-usability-notes` is
a peer skill producing the same artifact via a different
procedure.

## Self-Audit

Before declaring a usability synthesis complete, confirm:
- ≥5 users tested (or limitation surfaced explicitly).
- Per-task success criteria defined upfront.
- Per issue: severity + frequency + recommended fix +
  trade-offs.
- Sev-1 issues identified explicitly (the Gate 3 blockers).
- Patterns across users distinguished from outliers.
- Prototype + wireframes + personas + user tasks cited.
- Recruitment + test setup documented for replicability.
