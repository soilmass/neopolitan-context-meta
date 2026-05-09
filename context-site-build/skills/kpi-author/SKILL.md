---
name: kpi-author
description: >
  Authors the project's KPI & Success Metrics document. Translates
  business outcomes into measurable KPIs — per KPI: definition,
  current baseline, target (specific and time-bound), owner,
  measurement method. Mixes leading and lagging indicators. Writes
  the artifact to docs/01-discovery/kpi.md (site-build-procedure.md
  §4.2.6). Use during Phase 1 Discovery, after vision and at least
  one persona exist. Do NOT use for: authoring the project vision
  (use vision-author); persona authoring (use persona-author);
  mapping opportunities to KPIs (use ost-author once built;
  draft-ost covers it now); risk tracking (use risk-register-author);
  authoring the SRS (use srs-author); post-launch baseline reporting
  (use baseline-report-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass (Phase 1 of Option C per
            docs/ARCHITECTURE-OPTIONS-v0.2.md). Modeled on the
            user-invocable draft-kpi-doc skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# kpi-author

Phase 1 — produce the project's KPI & Success Metrics document.

## When to Use

- Phase 1 Discovery is in progress; vision exists; at least one
  persona has been authored; KPIs are the next deliverable.
- A major scope change has invalidated the existing KPIs and a
  re-baseline is needed.
- A new persona or feature has been scoped and the KPI set needs a
  new measurable to track its outcome.

## When NOT to Use

- Project vision is undefined — `vision-author` first. KPIs hang
  off the vision's stated business outcomes.
- Persona authoring — `persona-author`. KPIs reference personas
  by stable name; the personas exist before KPIs do.
- Mapping persona pains to opportunities — that's `ost-author`
  (Tier 3; the user-invocable `draft-ost` covers it now). KPIs
  anchor the OST's outcome node, but they're not the tree itself.
- Risk tracking — `risk-register-author`. KPI degradation may
  surface a risk, but the register is its own artifact.
- Software requirements — `srs-author`. NFRs *reference* KPIs as
  success criteria but the KPI doc is upstream.
- Post-launch baseline — `baseline-report-author`. The baseline
  *measures* against KPI targets; it doesn't define them.
- A "vanity metric" without a behavior or conversion tie — refuse.
  Page views without a conversion context fail this atom's gate.

## Capabilities Owned

- Translate stated business outcomes into 3–5 **measurable KPIs**
  (per SOP §4.2.6).
- Per KPI capture: precise **definition**, **current baseline**
  (existing analytics or industry benchmark for greenfield),
  **target** (specific value AND time-bound), **owner** (named
  individual accountable for moving the metric), and
  **measurement method** (which tool, which event, which
  calculation).
- Mix **leading** indicators (predictive, fast feedback —
  activation rate, time-to-first-value, NPS from new users) with
  **lagging** indicators (confirmatory, slow feedback — retention,
  revenue, churn). Refuses to ship a KPI set with all of one type.
- Cite the **vision** by stable name; cite **personas** by stable
  handle for any persona-specific KPI (e.g., "primary-persona
  activation rate").
- Refuse vanity metrics — KPIs must tie to a behavior change or a
  conversion event with business impact.
- Write the artifact to `docs/01-discovery/kpi.md`.

## Handoffs to Other Skills

- **From `vision-author`** — the vision states business outcomes;
  this atom translates them to measurable form.
- **From `persona-author`** — persona-specific KPIs cite the
  persona by stable handle.
- **To `ost-author`** (Tier 3) — KPIs anchor the OST's outcome
  node. The user-invocable `draft-ost` is the peer skill until the
  Tier 3 atom is built.
- **To `srs-author`** — NFRs reference KPI targets as success
  criteria.
- **To `baseline-report-author`** — KPI targets become the
  baseline report's comparison points at T+8 weeks.
- **To `weekly-metric-report-author`** (Tier 3) — KPIs are the
  weekly memo's spine. The user-invocable `weekly-metric-report`
  is the peer skill until that atom is built.
- **From the user-invocable `draft-kpi-doc`** — peer skill
  producing the same artifact via a different procedure. This
  atom adds meta-pipeline conformance.

## Edge Cases

- **Greenfield project, no baseline.** Use industry benchmarks
  (cite the source); mark the baseline `"TBD — first measurement
  window"`. Re-enter this atom once the first 4 weeks of analytics
  are collected.
- **Vanity metric proposed.** Refuse; require a behavior change
  or conversion event. Page-view counts without a downstream
  outcome get rejected. The operator either sharpens the metric
  or removes it.
- **KPI with no measurement source.** Halt; either name a tool +
  event + calculation, or move the item to an "operational
  metric" sheet outside the strategic KPI set.
- **More than 5 strategic KPIs proposed.** Force a primary +
  2–3 supporting. Beyond five is operational tracking, not
  strategic alignment.
- **Conflicting KPIs** (e.g., "increase signups" vs "improve
  signup quality"). Both can stand; the doc states the trade-off
  policy explicitly so the team knows which wins under conflict.

## References

No external `references/*.md` files yet — first real authoring
run will produce a template worth promoting. The canonical
authority is `internal://site-build-procedure.md` §4.2.6
(Edison Steele). The user-invocable `draft-kpi-doc` is a peer
skill producing the same artifact via a different procedure.

## Self-Audit

Before declaring a KPI document complete, confirm:
- ≥1 **leading** indicator AND ≥1 **lagging** indicator.
- Each KPI has all 5 fields: definition, baseline, target,
  owner, measurement method.
- Targets are **time-bound** (`+12pts by EoQ`, not `improve`).
- Each persona-specific KPI cites a persona by stable handle.
- ≤5 strategic KPIs total.
- Doc is ≤2 pages rendered.
