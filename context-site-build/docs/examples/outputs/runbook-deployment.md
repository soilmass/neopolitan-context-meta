# Runbook — Deployment (`<project>` v1.0; anonymized example)

> **Note**: anonymized illustrative output of `runbook-author` with
> kind=deployment. Cites `house-site-build-nextjs` deploy verbs +
> `house-site-operate-vercel` host conventions + `release-plan.md`
> go/no-go checklist.

---

## When to use this runbook

- **Routine deploy**: when a PR is approved and ready to ship.
- **Emergency deploy**: when a hotfix is needed (skips canary;
  documented escalation path below).
- **Rollback**: when a deploy is causing production issues.

For incident response, see `incident.md`. For launch, see
`launch.md`.

---

## Pre-conditions

Before invoking the deploy, verify:

- [ ] PR is approved by `<n-reviewers>` reviewer(s).
- [ ] CI is green (lint + typecheck + unit + e2e + Lighthouse CI +
      axe-core).
- [ ] Preview URL has been smoke-tested by the PR author.
- [ ] No active incident (status page in `<all-systems-operational>`
      state).
- [ ] If shipping during weekend / overnight: an on-call ack from
      `<oncall-rotation>`.

If any pre-condition is unmet → STOP. Resolve first.

---

## Procedure

### Routine deploy (canary)

1. Merge the PR to `main`. Vercel Git integration auto-deploys to
   production.
2. Verify the production deployment URL: `vercel inspect
   <production-url>` shows `READY` status.
3. **Canary phase — 10% traffic** via Vercel Edge Config flag:
   - Update `flag-canary-pct` to `10` in Edge Config dashboard.
   - Wait 1 hour.
   - Verify Sentry: error rate within baseline + 0.5pp.
   - Verify Speed Insights: LCP/INP/CLS within baseline + 5%.
4. **Canary phase — 50% traffic**:
   - Update `flag-canary-pct` to `50`.
   - Wait 4 hours.
   - Verify same metrics.
5. **Full rollout — 100% traffic**:
   - Update `flag-canary-pct` to `100`.
   - Verify production stable for 24h.

### Emergency deploy (hotfix)

1. Same pre-conditions, EXCEPT canary may be skipped.
2. Deploy to production via Vercel auto-deploy.
3. Notify on-call channel (`#oncall-eng`).
4. Monitor Sentry for 30 min.
5. Backfill the canary discipline: open a follow-up PR canarying
   the change at 10% → 50% over the next 24h.

### Rollback

When error rate > 5% sustained 3 min, OR LCP regresses > 10%, OR
CWV-fail rate > 10% sustained:

1. **Automated rollback** triggers via `release-plan.md` automation
   (Sentry → GitHub Action → `vercel rollback`).
2. **Manual rollback** if automation fails:
   - Run `vercel rollback` (interactive) and select the prior
     production deployment.
   - OR run `vercel promote <prior-deployment-url>` directly.
3. Verify rollback complete: `vercel inspect <production-url>`
   shows the prior commit SHA.
4. Post-rollback:
   - Page on-call.
   - File incident in `incident.md` runbook flow.
   - Determine root cause; do NOT re-deploy until fix is in place
     + has passed canary on the next deploy attempt.

---

## Step-by-step verifiers

After each step, the on-call engineer verifies the following
observable signals:

| Signal | Where to check | Acceptable threshold |
|---|---|---|
| Error rate | Sentry dashboard | ≤ 0.5% sustained 5 min |
| Sentry release marker | Sentry → Releases | New release shown with current Git SHA |
| LCP p75 | Vercel Speed Insights | ≤ 2.0s (per SRS NFR1.1) |
| INP p75 | Vercel Speed Insights | ≤ 200ms (per SRS NFR1.2) |
| CLS p75 | Vercel Speed Insights | ≤ 0.05 (per SRS NFR1.3) |
| Function timeout rate | Vercel Logs | ≤ 1% |
| Status page state | `<status-page-URL>` | `<all-systems-operational>` |

If any threshold is breached → ROLLBACK (per the rollback
procedure above).

---

## Escalation contacts

| Role | Name | Channel |
|---|---|---|
| On-call engineer (rotation) | per `<oncall-rotation>` | `#oncall-eng` Slack |
| Engineering lead | `<anonymized>` | `<contact>` |
| Founding team (P0 only) | `<anonymized>` | `<contact>` |
| Vercel support (account manager) | `<anonymized>` | `<contact>` |
| Sentry support | (paid tier) | `<contact>` |
| Sanity support | (CMS provider) | `<contact>` |

For **P0** (production down for all users): page founding team
within 15 min of incident detection.

---

## Authority + cross-references

- `release-plan.md` — go/no-go checklist + canary strategy +
  rollback automation thresholds.
- `house-site-build-nextjs` — Combo A deploy verbs.
- `house-site-operate-vercel` — host-specific operational
  conventions.
- `observability-spec.md` — SLI definitions powering the
  rollback-trigger thresholds.
- `srs.md` NFR2 — uptime + error rate + rollback target.

---

## Revision history

| Version | Date | Change | Reason |
|---|---|---|---|
| v0.1.0 | 2026-05-09 | Initial | Authored at v1.0 launch. |

Reviewed quarterly per the `release-plan.md` discipline.

---

*Authored 2026-05-09 by runbook-author v0.1.1 (kind=deployment).
Reviewed by on-call team 2026-05-09. Sign-off: 2026-05-09.*
