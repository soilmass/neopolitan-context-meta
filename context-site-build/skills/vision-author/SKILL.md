---
name: vision-author
description: >
  Authors the project's Vision & Value Proposition document — a
  one-page artifact naming the target user, the problem, the
  intended outcome, and qualitative success criteria distinct from
  KPIs. Reads sponsor inputs and produces docs/01-discovery/vision.md
  (site-build-procedure.md §4.2.5). Use at Phase 1 Discovery, before
  personas and KPIs exist. Do NOT use for: persona authoring (use
  persona-author); measurement and KPI work (use kpi-author once
  built; the user-invocable draft-kpi-doc covers it now); software
  requirements (use srs-author); decision recording (use adr-author);
  scaffolding a whole new project (the user-invocable
  bootstrap-site-project does that).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-triggers fall back to user-invocable peers
            for unbuilt skills (B6/A62 self-review pass);
            "Authority surface" reframed as "Sibling skill in operator
            environment"; deferred references/template.md row dropped;
            handoff/edge-case contradiction on no-personas resolved
            in favor of the provisional-vision path.
    v0.1.0 — initial. Authored via skill-author 4-stage procedure
            during the v0.7.0 first-real-consumer dogfood (P6 closure
            in context-meta-pipeline/docs/PATH-TO-V1.md). Modeled on
            the user-invocable draft-vision skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# vision-author

Phase 1 — produce the project's Vision & Value Proposition document.

## When to Use

- A new project enters Phase 1 Discovery and no vision document exists.
- The sponsor or product lead has named the problem and target audience
  in prose form; the Vision is the next deliverable that turns that into
  a single shareable artifact.
- A project pivots significantly and the existing vision no longer
  describes the work — re-author rather than patch.

## When NOT to Use

- Authoring a persona — `persona-author` owns that.
- Defining measurable success criteria with thresholds — that's
  `kpi-author` (Tier 2 in this family).
- Writing the technical software requirements — `srs-author`.
- Recording a single architectural decision — `adr-author`.
- Mapping opportunities and solution branches — `ost-author` (Tier 3).
- Scaffolding the project's whole repo + docs tree — that's the
  user-invocable `bootstrap-site-project` skill, not this atom.
- Patching an existing vision after a small wording tweak — edit the
  doc directly. This atom is for full authoring.

## Capabilities Owned

- Compose a one-paragraph **vision statement** from sponsor inputs
  (named user × problem × intended outcome).
- Articulate the **value proposition**: target user → problem →
  outcome → differentiator (vs status quo or alternative).
- Identify **success criteria** that are qualitative and aspirational
  — distinct from the quantitative thresholds owned by `kpi-author`.
- Cross-reference personas and KPIs by stable name (when those docs
  exist) without re-deriving their content.
- Surface the **out-of-scope statement** — what the project will NOT
  attempt, so the vision remains a fence rather than a wishlist.
- Write the artifact to `docs/01-discovery/vision.md` in the
  consuming project's repo.

## Handoffs to Other Skills

- **To `persona-author`** — every vision should ground in named
  personas. If none exist yet, the Edge Cases below cover the
  provisional-vision path; persona-author becomes the natural next
  invocation.
- **To `srs-author`** — once vision + personas + KPIs converge, the
  SRS authoring becomes possible. The vision is one of the SRS's input
  references (per `srs-author` Capabilities Owned).
- **To `adr-author`** — when a vision-shaping decision was made (e.g.,
  "we explicitly target small-business users, not enterprise"), record
  it as an ADR alongside the vision.
- **From `bootstrap-site-project`** (user-invocable) — the project
  scaffold creates `docs/01-discovery/vision.md` as an empty stub;
  this atom is the authoring step that fills it.
- **From the user-invocable `draft-vision`** — peer skill that
  produces the same artifact via a different procedure. This atom
  adds meta-pipeline conformance (frontmatter discipline, audit
  ritual, anti-triggers).

## Edge Cases

- **Sponsor inputs conflict** (e.g., sponsor wants enterprise, founder
  wants SMB). Halt; surface the conflict to the operator. The vision
  document is not the place to paper over a strategic disagreement.
- **No personas yet** (Phase 1 is just starting). Author a *provisional*
  vision noting that personas are pending; mark the doc with a
  `## Status` block reading "Provisional — re-confirm after persona-
  author runs." Re-enter at vision-author once personas exist.
- **Project is a re-skin of an existing product** (no fresh problem
  framing, just re-platforming). Vision authoring is lightweight —
  carry over the existing vision verbatim where applicable; the
  authoring is then an alignment exercise rather than a synthesis.
- **Multiple competing vision drafts exist** (different stakeholders
  authored their own). Halt; this is a `stakeholder-map-author` /
  `comms-plan-author` problem first. Resolve stakeholder consensus
  before vision-author runs.

## References

No external `references/*.md` files yet — first real authoring run
will produce a template worth promoting. The canonical authority is
`internal://site-build-procedure.md` §4.2.5 (Edison Steele).

## Examples

(Deferred to v0.1.x — first real authoring run produces the worked
example. Per the v0.7.0 speculative-skill convention, the absence is
flagged here rather than papered over.)

## Self-Audit

Before declaring a vision document complete, confirm:
- The vision statement names a **specific user** (not "everyone").
- The value proposition identifies a **differentiator** vs the status
  quo or named alternatives.
- Success criteria are **qualitative** — quantitative thresholds belong
  in the KPI doc, not here.
- Out-of-scope statement names ≥1 thing the project will not do.
- The doc is **one page** when rendered (≤500 words is a useful proxy).
