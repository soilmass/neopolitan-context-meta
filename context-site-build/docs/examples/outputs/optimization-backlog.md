# Optimization Backlog — `<project>` (anonymized example output)

> **Note**: anonymized illustrative output of `optimization-backlog-
> author`. RICE-scored hypotheses for the next 8-12 weeks of
> Phase 7 experimentation. Reads `weekly-metric-report.md`,
> `kpis.md`, and `analytics-spec.md`.

**Cadence**: weekly review; bi-weekly grooming; per-experiment
update via `optimization-loop-author`.

**Reviewers**: founding team + product lead (when present).

---

## RICE scoring

| Letter | Meaning | Scale |
|---|---|---|
| **R** | Reach (users / week affected) | 1, 10, 100, 1k, 10k, 100k |
| **I** | Impact (per-user lift estimate) | 0.25 (minimal), 0.5 (low), 1 (med), 2 (high), 3 (massive) |
| **C** | Confidence | 0.5 (low), 0.8 (medium), 1.0 (high) |
| **E** | Effort (engineer-weeks) | 0.5, 1, 2, 4, 8, 16 |

**RICE score** = R × I × C / E. Higher = better. The backlog is
sorted by RICE score descending.

---

## Top 10 backlog (sorted by RICE score)

| Rank | Hypothesis | KPI affected | R | I | C | E | RICE |
|---|---|---|---|---|---|---|---|
| 1 | Add post-signup welcome-tour (3 steps) → activation rate ↑ | activation rate | 1k | 1 | 0.8 | 1 | **800** |
| 2 | Move custom-domain setup from settings to first-publish flow → custom-domain rate ↑ | custom-domain rate | 1k | 0.5 | 0.8 | 0.5 | **800** |
| 3 | Add image-upload progress bar + cancel UI → edit-session abandonment ↓ | edit-session retention | 1k | 0.5 | 0.8 | 0.5 | **800** |
| 4 | A/B test homepage hero copy: cinematic vs minimal | signup rate | 10k | 0.5 | 0.5 | 1 | **2,500** |
| 5 | Add Schema.org `Person` markup to creator profile pages → AI-search citation ↑ | AI-search citation count | 10k | 1 | 0.5 | 0.5 | **10,000** |
| 6 | Lazy-load hero scene to second-paint → LCP p75 ↓ | LCP p75 | 10k | 1 | 0.8 | 1 | **8,000** |
| 7 | Add free-tier upsell banner on hit-rate-warn pages → free→paid ↑ | free→paid conversion | 1k | 1 | 0.5 | 1 | **500** |
| 8 | Replace email-verify CAPTCHA with cloudflare turnstile → signup rate ↑ | signup rate | 10k | 0.25 | 0.8 | 0.5 | **4,000** |
| 9 | Add loading-skeleton on portfolio grid (vs spinner) → perceived perf | INP p75 | 10k | 0.5 | 1.0 | 0.5 | **10,000** |
| 10 | Cache portfolio renders at the edge (Vercel KV) → repeat visit LCP | LCP p75 (repeat) | 10k | 1 | 0.5 | 2 | **2,500** |

(11-25 elided for length)

---

## In-flight (per `optimization-loop-author` outputs)

| Experiment | Started | Status | KPI being tested |
|---|---|---|---|
| `<exp-id-001>` Welcome tour A/B | 2026-05-09 | day 0; ramping to 50% | activation rate |
| `<exp-id-002>` Hero copy A/B | 2026-05-08 | day 1; 25% bucket | signup rate |
| `<exp-id-003>` Image-upload progress UI | 2026-05-07 | day 2; 50% bucket | edit-session retention |

---

## Recently completed (last 4 weeks)

| Experiment | Closed | Result | Action |
|---|---|---|---|
| `<exp-id-000>` Email-verify CAPTCHA → Turnstile | 2026-05-04 | +12% signup rate (p<0.05) | Promoted to 100%; merged. |
| `<exp-id--001>` Free-tier upsell banner location | 2026-04-28 | +3% free→paid (p<0.10; not significant); minor regression (-1%) on engagement | Reverted. |
| `<exp-id--002>` Schema.org Person on profile pages | 2026-04-21 | +18% AI-search citation count over 4 weeks | Promoted to 100% via `aeo-schema-spec.md` v0.2 update. |

---

## Hypothesis pipeline (not yet RICE-scored)

Surfaced by `discovery-tick-author` weekly digest:

- Add bulk-delete UI to image gallery (4 support tickets in last 30 days).
- Add Stripe-billing portal integration so users self-serve cancellations
  (12 cancellation-via-support tickets in last 30 days).
- Add "Duplicate site" feature for users running multiple portfolios
  (5 feature requests in last 30 days).
- Add custom 404 page (currently default Next.js).
- Migrate `/blog` to MDX (currently Sanity blog feels heavyweight).
- Investigate INP regression on `/edit/<slug>` route — climbing 180
  → 220ms over last 2 weeks (post-launch baseline).

These get RICE-scored in next backlog grooming.

---

## Anti-pattern: experiments NOT to run

Documented for the team. Do NOT run experiments that:

- Affect billing / subscription flow without legal review (compliance
  scope creep risk).
- Require >1 week of engineering investment without
  conviction-level evidence (the experiment IS investment;
  high-effort experiments should be smaller scoping decisions in
  ADRs, not RICE-scored hypotheses).
- Test the brand voice (the brand is established; test mechanics,
  not voice).
- Are statistically underpowered — the homepage hero copy A/B is
  on the boundary; minimum-detectable-effect calculation should
  precede every experiment.

---

## Cumulative impact

Since post-launch (2026-05-09) — 4 weeks elapsed:

| KPI | Baseline | Current | Cumulative attributable lift |
|---|---|---|---|
| Signup rate | 58% | 65% | +7pp (Turnstile experiment) |
| AI-search citations / month | 12 | 18 | +6 (Person schema experiment) |
| Activation rate | 38% | 38% | none yet (welcome-tour in flight) |
| LCP p75 | 1.95s | 1.82s | -0.13s (deploys + minor optimizations) |

---

## Authority

- KPIs: `kpis.md` v0.1.
- Analytics events: `analytics-spec.md` v0.1.
- Per-experiment writeups: `07-post-launch/experiments/<exp-id>.md`.

---

*Authored 2026-05-09 by optimization-backlog-author v0.1.0. Last
refresh 2026-05-09. Next refresh 2026-05-16.*
