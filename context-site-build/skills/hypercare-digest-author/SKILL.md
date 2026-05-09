---
name: hypercare-digest-author
description: >
  Authors the daily hypercare memo across Phase 7 weeks 1-4 —
  error rate, performance, conversion baseline, in-flight issues,
  asks. Audience is PM + Tech Lead + on-call. Output at
  docs/07-postlaunch/hypercare/<YYYY-MM-DD>.md (SOP §10.1.1). Use
  daily across the hypercare window. Do NOT use for: 30-day
  stabilization report (use stabilization-report-author — that
  consolidates 30 daily memos); weekly metric report (use
  weekly-metric-report-author in site-build family — that runs
  after hypercare ends); the T+8 baseline report (use
  baseline-report-author in site-build family); incident
  postmortem (a different artifact; this memo tracks issues, not
  roots them).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [daily-use]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable hypercare-digest skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# hypercare-digest-author

Phase 7 — produce one daily hypercare digest.

## When to Use

- Phase 7 week 1-4 hypercare window is active; today's digest
  is due.
- A late-stage hypercare extension (>4 weeks) and the cadence
  continues until formal stabilization.
- A new launch within an existing project (e.g., feature rollout
  hypercare distinct from the original launch hypercare).

## When NOT to Use

- 30-day stabilization report at end of week 4 —
  `stabilization-report-author`. The digest is daily; the
  stabilization report is monthly.
- Weekly metric report —`weekly-metric-report-author` (site-build
  family). Weekly runs after hypercare ends as the ongoing-ops
  cadence.
- T+8 baseline report — `baseline-report-author` (site-build).
- Incident postmortem — that's a different artifact (root-cause
  analysis); this digest tracks issues at the day-of level.
- Outside the hypercare window — daily digests aren't a
  permanent cadence. Per SOP §10.1.1 hypercare runs weeks 1-4;
  weekly takes over after.

## Capabilities Owned

- Capture **today's snapshot** per SOP §10.1.1:
  - **Error rate** vs baseline (Sentry / Rollbar / etc.).
  - **Performance** — p75 LCP, INP, CLS for key templates
    (CrUX or RUM tool).
  - **Conversion baseline** — key event conversion rate today
    vs trailing 7-day average.
  - **Search Console** signal — crawl errors, redirect issues,
    indexing problems, manual actions.
  - **GA4 signal** — traffic anomalies, conversion shifts.
  - **Heatmap / session replay** — spot-check for friction.
  - **AI search citations** — weekly check (have we lost / gained
    citations?).
- Document the **hotfix queue** state:
  - P0 / P1 issues triaged within 24h.
  - In-flight P2 fixes with ETAs.
  - P3 backlog count.
- Capture **issues opened today** — title, severity, owner,
  expected resolution.
- Capture **issues resolved today** — title, what was done,
  follow-up.
- State **asks** — anything blocked or needing decision from
  Sponsor / cross-team.
- Maintain **memo discipline** — half-page max; the daily
  audience is PM + Tech Lead + on-call, who scan it at standup.
- Write to `docs/07-postlaunch/hypercare/<YYYY-MM-DD>.md`.

## Handoffs to Other Skills

- **From the day's monitoring + ops activity** — operator-driven
  data collection from Sentry, GA4, Search Console, Hotjar,
  AI-search prompts.
- **From `runbook-author`** (site-build family) — incident
  runbooks govern escalation; the digest references runbook
  invocations.
- **To `stabilization-report-author`** — 30 daily digests
  consolidate into the stabilization report at week 4.
- **To `risk-register-author`** (site-build family) — issues
  that fire as incidents update the risk register.
- **To Phase 4 + ongoing-build** — issues attributable to
  recent merges may surface tech debt or test gaps.
- **From the user-invocable `hypercare-digest`** — peer skill
  producing the same artifact via a different procedure.

## Edge Cases

- **No issues today.** Acceptable; the digest documents the
  quiet day with observed metrics. Don't fabricate issues to
  fill the template.
- **Major incident in flight.** The digest mode shifts —
  lead with the incident summary + escalation status; metrics
  section becomes "see incident #N for live status."
- **Operator skipped yesterday's digest.** Don't catch up by
  combining; ship today's digest with a brief gap note. The
  daily cadence is the floor; a missed day is a finding for
  the trio.
- **Weekend / holiday cadence.** The SOP doesn't mandate
  weekend digests; if the team's cadence is weekday-only,
  document the rule explicitly in the project's hypercare
  setup.
- **Hypercare extended past week 4.** Continue daily digests
  with the extension reason logged; revisit stabilization
  cadence weekly.

## References

No external `references/*.md` files yet. The canonical authority
is `internal://site-build-procedure.md` §10.1.1. The
user-invocable `hypercare-digest` is a peer skill producing the
same artifact via a different procedure.

## Self-Audit

Before declaring a daily digest shipped, confirm:
- All 4 metric snapshots present (error / perf / conversion /
  Search-Console + AI-search-citation check on the appropriate
  weekly day).
- Hotfix queue state captured (P0/P1/P2/P3 counts).
- Issues opened today + issues resolved today both present.
- Asks section concrete or explicitly `<none>`.
- Memo is ≤ half-page rendered.
- Date stamped correctly.
