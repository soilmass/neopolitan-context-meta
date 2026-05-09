---
name: stabilization-report-author
description: >
  Authors the 30-day Stabilization Report after the Phase 7
  hypercare window closes. Synthesizes 30 daily hypercare memos
  into one sponsor-facing memo with operational baseline,
  in-flight issues summary, warranty status, and operational
  handoff status. Output at
  docs/07-postlaunch/stabilization-report.md (SOP §10.1). Use at
  week 4 of Phase 7. Do NOT use for: daily hypercare digest (use
  hypercare-digest-author); the T+8 baseline report (use
  baseline-report-author in site-build family — that is the next
  downstream artifact); the win-regression report (use
  win-regression-report-author); weekly metric report (use
  weekly-metric-report-author in site-build family).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap (Phase 3 of Option C per
            docs/ARCHITECTURE-OPTIONS-v0.2.md). Modeled on the
            user-invocable draft-stabilization-report skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# stabilization-report-author

Phase 7 — produce the 30-day Stabilization Report.

## When to Use

- End of week 4 of Phase 7 (post-launch); the hypercare window
  closes; the report consolidates the past month's daily digests
  into a sponsor-facing memo.
- A re-baseline launch (rebrand / re-platform) needs a 30-day
  stabilization report against the new baseline.
- An operator + sponsor agree the project is exiting hypercare
  ahead of schedule (rare; document the call).

## When NOT to Use

- Daily hypercare digest — `hypercare-digest-author`. Stabilization
  consolidates 30 days of digests; doesn't replace them.
- T+8-week baseline report — `baseline-report-author` (site-build
  family). Baseline is the next downstream artifact (T+8 vs T+30);
  different audience, deeper scope.
- Win-regression report — `win-regression-report-author` (Tier 2).
  Win-regression is at T+8 paired with baseline; stabilization is
  at T+30 and earlier in the cadence.
- Weekly metric report — `weekly-metric-report-author` (site-build
  family Tier 3). Weekly is the working memo; stabilization is the
  monthly synthesis.

## Capabilities Owned

- Synthesize the **30-day operational baseline** per SOP §10.1:
  - **Error rate** trajectory (daily snapshots → trend).
  - **Performance (CWV)** trajectory (LCP / INP / CLS at p75).
  - **Conversion baseline** trajectory (key conversion events).
  - **Customer support volume** trajectory.
  - **Hotfix queue** summary (P0 / P1 fixed; P2 batched; P3
    backlogged).
- Document the **hot-issue list** — issues that surfaced during
  hypercare with severity, root cause, mitigation, status.
- Capture the **warranty period** outcome — defects attributed to
  the build resolved at no incremental cost; sponsor sign-off at
  end-of-warranty per SOP §10.1.4.
- Document **operational handoff status** per SOP §10.1.5:
  - Project team handed off to ongoing ops (or remained as the
    ongoing team).
  - Runbooks reviewed + updated based on real incidents.
  - On-call rotation transitioned.
  - Documentation complete and accessible.
  - Lingering risks transitioned to ops risk register.
- State the **next-step recommendation** — readiness for the
  T+8 baseline report; any items deferred from hypercare into
  the next phase.
- Cite **launch date** + **runbooks** + **incidents from
  hypercare** by stable name / IDs.
- Write to `docs/07-postlaunch/stabilization-report.md`.

## Handoffs to Other Skills

- **From `hypercare-digest-author`** — 30 daily digests are the
  raw input.
- **From `runbook-author`** (site-build family) — runbooks are
  reviewed + updated based on real incidents during hypercare.
- **From `risk-register-author`** (site-build family) — lingering
  risks transition to the ops risk register.
- **To `baseline-report-author`** (site-build family) — the
  T+8 baseline references the stabilization report's operational
  baseline trajectory.
- **To `win-regression-report-author`** (Tier 2 here) — at T+8,
  win-regression complements baseline.
- **To Phase 7 ongoing operations** — the report's next-step
  recommendation flows into ongoing optimization work.
- **From the user-invocable `draft-stabilization-report`** — peer
  skill producing the same artifact via a different procedure.

## Edge Cases

- **Hypercare extended beyond 30 days** (major issues unresolved).
  Mark the report as **interim** with the trigger to re-issue
  when hypercare formally closes. The 30-day mark isn't sacred;
  honesty is.
- **No incidents during hypercare.** Surface the unusual quietness
  as a finding — either the launch was genuinely smooth, or
  monitoring is missing signal. Recommend a re-verification of
  monitoring coverage.
- **Operational handoff didn't happen** (project team lingers).
  Surface as the §10.1.5 dysfunction; the report's recommendation
  becomes "complete the handoff before T+8."
- **Warranty disputes** (build defect vs new request vs
  environment issue). Document each dispute with attribution
  decision; refuse silent resolution.
- **Stabilization report becomes a victory-lap presentation.**
  Refuse the polish creep; the report is sponsor-facing but
  working — synthesizing what happened, not selling success.

## References

No external `references/*.md` files yet. The canonical authority
is `internal://site-build-procedure.md` §10.1. The user-invocable
`draft-stabilization-report` is a peer skill producing the same
artifact via a different procedure.

## Self-Audit

Before declaring a stabilization report complete, confirm:
- All 5 trajectory categories (error / perf / conversion /
  support / hotfix) reported with daily-resolution data.
- Hot-issue list with severity + root cause + mitigation +
  status.
- Warranty status documented (sign-off captured if at boundary).
- Operational handoff §10.1.5 checklist evaluated.
- Next-step recommendation states T+8 readiness.
- Cross-references to runbooks + incidents + risk register.
