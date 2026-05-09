---
name: diagnostic-sweep-author
description: >
  Authors the Phase 7 diagnostic sweep at T+4 to T+8 — heatmaps +
  funnel analysis on top conversion paths + on-site survey + form
  analytics + search analytics + page-level performance audit +
  accessibility re-audit. Output is a findings document with
  prioritized improvement candidates that seed the optimization
  backlog. Writes to docs/07-postlaunch/diagnostic-sweep-<YYYY-MM-DD>.md
  (SOP §10.2.2). Use at T+4 to T+8 weeks once traffic patterns
  settle. Do NOT use for: T+8 baseline report (use baseline-report-
  author in site-build family — baseline is the snapshot;
  diagnostic is the deeper investigation); win-regression report
  (use win-regression-report-author Tier 2); optimization backlog
  (use optimization-backlog-author Tier 1 — backlog consumes
  diagnostic findings); per-experiment design (use
  optimization-loop-author Tier 1).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable diagnostic-sweep skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# diagnostic-sweep-author

Phase 7 — produce the diagnostic sweep findings document.

## When to Use

- T+4 to T+8 weeks; traffic patterns have settled (post-
  launch novelty fades around week 4); a structured
  diagnostic surfaces optimization opportunities.
- A specific friction signal (sudden conversion drop;
  unexpected support volume) warrants targeted diagnostic
  work outside the routine T+8 sweep.
- Quarterly diagnostic re-sweep (some teams run this on
  cadence).
- A re-launch / major release at T+4 to T+8 against the
  new launch.

## When NOT to Use

- T+8 baseline report — `baseline-report-author` (site-build).
  Baseline is the metric snapshot; diagnostic is the deeper
  investigation across qualitative + quantitative signals.
- Win-regression report — `win-regression-report-author`
  (Tier 2 here). Win-regression interprets the baseline; this
  diagnoses with deeper tooling.
- Optimization backlog — `optimization-backlog-author`
  (Tier 1 here). Diagnostic produces findings; backlog
  prioritizes.
- Per-experiment design — `optimization-loop-author`
  (Tier 1 here). Diagnostic surfaces hypotheses; loop tests
  them.
- Phase 5 functional QA test plan — those are sprint
  outputs, not Phase 7 diagnostic.
- Phase 5 a11y audit — that's done at Phase 5 hardening
  (consumed by `conformance-statement-author`); the
  diagnostic sweep includes an a11y *re-audit* to catch
  post-launch regressions.
- Standalone marketing-funnel analysis — funnel work is
  one input to the diagnostic; the diagnostic is the
  cross-cutting synthesis.

## Capabilities Owned

- Run + document **heatmap and session-recording sweep**
  on the top 5-10 templates per SOP §10.2.2:
  - Hotjar / Microsoft Clarity / FullStory equivalent.
  - Patterns: rage-clicks, scroll-depth distributions,
    confusion areas (back-and-forth between sections),
    abandonment hotspots.
- Run + document **funnel analysis** for each conversion
  path:
  - Drop-off per step.
  - Per-segment (persona) drop-off where data permits.
  - Time-to-conversion distribution.
- Document **on-site survey or exit-intent feedback**
  qualitative themes.
- Document **form analytics** — drop-off per field;
  field-level error rate; time-on-form distribution.
- Document **search analytics** — internal search queries,
  zero-result rate, click-through, refinement patterns.
- Run + document **page-level performance audit** —
  which pages pull down the perf average; per-template
  CWV breakdown.
- Run + document **accessibility re-audit** — automated
  axe / Lighthouse scan; manual SR sample on top 3 user
  flows; surface any post-launch regressions.
- Synthesize **prioritized improvement candidates** with
  preliminary RICE scoring (per `optimization-backlog-
  author` Tier 1 schema).
- Cite the **baseline report** + **KPIs** + **content
  matrix** + **a11y annotations** by stable name.
- Write to `docs/07-postlaunch/diagnostic-sweep-<YYYY-MM-DD>.md`.

## Handoffs to Other Skills

- **From `baseline-report-author`** (site-build) — the
  baseline informs which areas warrant deeper diagnostic.
- **From the analytics + heatmap + survey + perf + a11y
  tooling** — operator-driven data collection.
- **From `kpi-author`** (site-build) — KPIs anchor the
  diagnostic's success-criteria framing.
- **To `optimization-backlog-author`** (Tier 1 here) —
  diagnostic findings seed the backlog (the largest single
  source of backlog items at T+8).
- **To `win-regression-report-author`** (Tier 2 here) —
  diagnostic findings inform the regressions analysis.
- **To `aeo-baseline-author`** (Tier 2 here) — AI search
  diagnostic is its own deeper artefact.
- **To `conformance-statement-author`** (Tier 1 here) —
  a11y re-audit findings update the conformance
  statement.
- **From the user-invocable `diagnostic-sweep`** — peer
  skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Tooling not yet in place** (no heatmap; no session
  replay; no analytics events configured). Halt the
  sweep at the missing tooling level; recommend a
  Phase 5 / 6 catch-up before re-trying. Don't run a
  partial sweep that misleads.
- **Insufficient traffic for funnel analysis** (small-
  audience site). Use cohort analysis instead of
  funnel; document the methodology change.
- **Diagnostic surfaces a Sev-1 issue** (broken
  conversion path; major a11y regression). Promote to
  immediate fix via the hotfix queue; don't wait for
  the optimization backlog.
- **Diagnostic findings exceed 50 candidates.** Bucket
  by theme; promote top 10-15 to the backlog with
  preliminary scoring; archive the rest with a "watch"
  disposition.
- **A11y re-audit shows new violations not present at
  Phase 5.** Cross-reference to recent merges; check
  whether new components shipped without
  `a11y-annotations-author` review.
- **Conflicting signals across tools** (heatmap says X;
  funnel says Y). Surface the conflict; recommend a
  triangulating method (interview, exit survey,
  experiment) to resolve.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.2.2.
The user-invocable `diagnostic-sweep` is a peer skill
producing the same artifact via a different procedure.

## Self-Audit

Before declaring a diagnostic sweep complete, confirm:
- All 7 method areas covered (heatmap / funnel / survey /
  form / search / perf / a11y).
- Top-template list explicit (which 5-10 templates were
  swept).
- Findings count + initial RICE scoring per finding.
- Cross-references to baseline + KPIs + content matrix
  + a11y annotations.
- Tool stack documented (which heatmap / analytics /
  survey / perf / a11y tools were used).
- Methodology changes flagged where data was thin
  (cohort vs funnel, etc.).
