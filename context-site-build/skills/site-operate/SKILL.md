---
name: site-operate
description: >
  Routes site-operate deliverable-authoring prompts to the right
  atom. Covers Phase 5 a11y conformance, Phase 6 launch comms,
  and Phase 7 post-launch (stabilization, hypercare, optimization
  backlog + loop, monthly / quarterly / annual reports,
  win-regression, diagnostic sweep, AEO baseline) plus
  Awwwards-tier polish + awards. Use when the operator names a
  Phase 5/6/7 deliverable but no specific atom. Do NOT use for:
  site-build family deliverables (vision / persona / KPI / SRS /
  ADR / runbook / baseline / weekly / change request — use
  site-build router); site-design family deliverables (mood
  board / art direction / concept / motion / tokens / states /
  handoff / wireframe / prototype / usability / a11y annotations
  / design system / discovery tick — use site-design router);
  meta-pipeline lifecycle (use meta router); domains other than
  site-operate.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: router
  tags: [router, daily-use]
  changelog: |
    v0.1.0 — initial. Authored as part of family-bootstrap Stage 4
            during the v0.4.0 site-operate family bootstrap (Phase
            3 of Option C per docs/ARCHITECTURE-OPTIONS-v0.2.md).
            Routing Table covers all 14 in-family atoms. Family
            scope is Phase 5 (a11y conformance only) + Phase 6
            (launch comms) + Phase 7 (full) + Awwwards-tier polish
            + awards.
---

# site-operate

Per-family router for the site-operate cluster in the
context-site-build library. Dispatches operator prompts to the
deliverable-authoring atom that owns the artifact.

## When to Use

- The operator names a Phase 5/6/7 deliverable (a11y conformance
  statement, launch communications, stabilization report,
  hypercare digest, optimization backlog, optimization loop /
  experiment, monthly stakeholder report, quarterly business
  review, win-regression report, diagnostic sweep, AEO baseline,
  annual retrospective, polish discipline, awards submission)
  without specifying which atom should produce it.
- The operator describes a phase (Phase 5 hardening close, Phase
  6 launch, Phase 7 stabilization / measurement / optimization)
  and the next deliverable to produce isn't named.
- The operator says "draft the …", "write the …", "log the …",
  "spec the …" for any artifact in this family.
- The operator asks "which skill should I use to author X" where
  X is one of the 14 atoms claimed by this family.

## When NOT to Use

- The operator names a specific atom directly
  (`stabilization-report-author`, `launch-comms-author`, etc.)
  — invoke that atom, no routing needed.
- The prompt is about a **site-build family** deliverable
  (vision / persona / KPI / OST / stakeholder map / risk
  register / SRS / ADR / threat model / privacy plan / master
  schedule / runbook / baseline report / weekly metric report
  / change request) — that's the `site-build` router in this
  same library.
- The prompt is about a **site-design family** deliverable
  (mood board / art direction / concept / motion language /
  design tokens / component states / engineering handoff /
  concept prototyping / wireframe / prototype / usability
  synthesis / a11y annotations / design system / discovery
  tick) — that's the `site-design` router in this same
  library.
- The prompt is about meta-pipeline lifecycle — that's the
  `meta` router in `context-meta-pipeline`.
- The prompt is about Phase 4 build sprint planning,
  ceremonies, or working software — out of family scope.
- The prompt is about non-site-operate domains (git, postgres,
  etc.).

## Routing Table

| Intent | Target atom |
|---|---|
| 30-day stabilization report at hypercare close | `stabilization-report-author` |
| Daily hypercare digest during weeks 1-4 | `hypercare-digest-author` |
| Launch communications — internal + external + status-page | `launch-comms-author` |
| WCAG 2.2 conformance statement at Phase 5 close | `conformance-statement-author` |
| Prioritized optimization backlog with RICE / ICE scoring | `optimization-backlog-author` |
| Single experimentation cycle (hypothesize → analyze → decide) | `optimization-loop-author` |
| Polish phase plan + per-iteration polish notes | `polish-discipline-author` |
| Monthly stakeholder report consolidating 4 weeklies | `monthly-stakeholder-report-author` |
| Quarterly Business Review with metrics + ROI + competitive | `quarterly-business-review-author` |
| Win/regression report at T+8 — wins, regressions, surprises | `win-regression-report-author` |
| Phase-7 diagnostic sweep — heatmap + funnel + survey + perf + a11y | `diagnostic-sweep-author` |
| AI Search baseline — manual prompt testing across 5 engines | `aeo-baseline-author` |
| Annual retrospective + roadmap proposal | `annual-retrospective-author` |
| Awwwards / SOTD / SOTM / SOTY submission package | `awards-submission-author` |

All 14 in-family atoms are built (v0.4.0 of library).

## Disambiguation Protocol

When two atoms could plausibly handle a prompt:

- **Stabilization report vs hypercare digest**: stabilization is
  the 30-day consolidated report; hypercare is the daily during-
  hypercare memo. Daily during weeks 1-4 → hypercare-digest;
  end-of-week-4 consolidated → stabilization-report.
- **Stabilization report vs T+8 baseline** (cross-family):
  stabilization is at T+30 closing the hypercare window; T+8
  baseline is at T+56 days (~8 weeks) — different artifacts at
  different times. Operations close at T+30; baseline measures
  full settled state at T+56.
- **Optimization backlog vs optimization loop**: backlog is the
  *queue* (prioritized list of candidates); loop is the *per-
  experiment* execution. Queue management → backlog;
  individual experiment → loop.
- **Diagnostic sweep vs win-regression report**: sweep produces
  findings (problems + opportunities) at T+4 to T+8;
  win-regression interprets the baseline at T+8 (wins +
  declines + surprises). Sweep is the deeper investigation;
  win-regression is the sponsor-facing interpretation.
- **Diagnostic sweep vs baseline report** (cross-family):
  baseline is the metric snapshot; sweep is the qualitative +
  quantitative diagnostic that often runs in parallel with
  baseline at T+8. Different methods, complementary.
- **Monthly stakeholder report vs QBR**: monthly consolidates
  four weeklies; QBR consolidates three monthlies + adds
  ROI + competitive + strategic recommendations. Cadence
  determines.
- **QBR vs annual retro**: QBR is per-quarter; annual
  consumes four QBRs + adds year-narrative + next-year
  priorities.
- **Weekly metric report vs monthly stakeholder report**
  (cross-family): weekly is in `site-build` (working memo);
  monthly is in this family (stakeholder consolidation).
- **AEO baseline vs classic SEO baseline** (out-of-scope):
  AEO is in this family; classic SEO baseline is operator-
  driven via Search Console / Ahrefs (out of scope).
- **Polish discipline vs engineering handoff spec** (cross-
  family): handoff (site-design) is the contract at Phase 3
  close; polish (site-operate) is the iteration during
  Phase 5 hardening that refines what's been handed off.
- **Awards submission vs launch comms**: launch comms is
  customer-facing; awards is jury-facing. Different audience,
  different framing.
- **Awards submission vs marketing case study**: awards is
  jury-targeted (per Awwwards or peer-body criteria);
  marketing case study is sales-targeted. Awards-submission-
  author is the seed; marketing derivation is downstream.
- **Conformance statement vs a11y annotations** (cross-
  family): annotations (site-design) are *design intent*;
  conformance (this family) is *post-implementation
  verification*.
- **Optimization backlog vs change request** (cross-family):
  backlog items below the Major scope threshold stay in the
  backlog; items at or above promote to Change Request via
  `change-request-author` (site-build).
- **When the prompt spans phases or families**: ask the
  operator which deliverable they're producing right now.
  Routers don't fan out across deliverables.

## Atoms in This Family

All 14 atoms are built and live (v0.4.0 of library).

**Tier 1 — Essential spine (7):**

- `stabilization-report-author`
- `hypercare-digest-author`
- `launch-comms-author`
- `conformance-statement-author`
- `optimization-backlog-author`
- `optimization-loop-author`
- `polish-discipline-author`

**Tier 2 — Specialist (5):**

- `monthly-stakeholder-report-author`
- `quarterly-business-review-author`
- `win-regression-report-author`
- `diagnostic-sweep-author`
- `aeo-baseline-author`

**Tier 3 — Long tail (2):**

- `annual-retrospective-author`
- `awards-submission-author`

## Self-Audit

Before declaring a routing decision:

- The chosen atom's `## When to Use` section names the
  prompt's trigger phrasing OR a clear paraphrase.
- The chosen atom's `## When NOT to Use` does NOT exclude
  the current prompt.
- If two atoms could fit, the **Disambiguation Protocol**
  above was consulted and the choice is justified.
- If the prompt is for a cross-family deliverable (Phase
  1/2/3/4 — site-build / site-design family), the operator
  is told explicitly to use the appropriate sibling router.
