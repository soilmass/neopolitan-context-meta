---
name: ost-author
description: >
  Authors the project's Opportunity Solution Tree — outcome → named
  opportunities (rooted in persona pains and JTBD) → candidate
  solutions, with evidence citations and RICE-style scoring per
  branch. Initial sketch at Phase 1; refined at Phase 2 and as
  continuous discovery in Phase 4 produces new evidence. Writes to
  docs/01-discovery/ost.md (site-build-procedure.md §4.2.7). Use
  after personas and KPIs exist. Do NOT use for: authoring the
  project vision (use vision-author); persona authoring (use
  persona-author); KPI definition (use kpi-author); authoring the
  SRS (use srs-author); prioritizing the post-launch optimization
  backlog (Phase 7 artifact — out of scope here).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-ost skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# ost-author

Phase 1 sketch / Phase 2 refinement — produce the project's
Opportunity Solution Tree.

## When to Use

- Phase 1 Discovery; vision + KPIs + ≥1 persona exist; the OST
  is one of the eight Phase 1 deliverables (Sponsor reviews
  it, doesn't approve gating per §4.3).
- Phase 2 begins; the Phase 1 OST sketch needs deepening as
  architecture and SRS surface new candidate solutions.
- Phase 4+ continuous discovery has produced new opportunities;
  the tree is updated to reflect what was learned.
- A new persona segment is added; the tree extends to cover
  their pains.

## When NOT to Use

- Vision, KPIs, or personas are undefined — those are
  prerequisites. Build them first.
- Project vision authoring — `vision-author`.
- Persona authoring — `persona-author`.
- KPI definition — `kpi-author`. The KPI sits at the OST's
  outcome node, but the KPI doc is its own artifact.
- Writing the SRS — `srs-author`. Solutions in the tree become
  candidate FRs only after the OST is reviewed and pruned.
- Phase 7 **optimization backlog** prioritization — that's a
  post-launch artifact downstream of this tree (the user-
  invocable `draft-optimization-backlog` covers it now).
- Solution implementation planning — the master schedule
  (`master-schedule-author`) handles when; the OST handles what.

## Capabilities Owned

- Author the **outcome node** at the top of the tree, sourced
  from the project's primary KPI (per `kpi-author`'s output).
- Enumerate **opportunities** under the outcome — each rooted
  in named persona pains, named jobs-to-be-done, or named
  observed user behavior. Refuses to ship invented opportunities
  ("we think users want X" without persona evidence).
- Per opportunity: cite the persona(s) it serves by stable
  handle; cite the evidence source (interview ID, analytics
  segment, customer-support log).
- Enumerate **candidate solutions** under each opportunity —
  short solution sketches, not specs. Each solution has a
  RICE-style scoring placeholder (Reach × Impact × Confidence
  ÷ Effort) for Phase 2 prioritization.
- Maintain the OST as a **working artifact** through Phase 2
  and Phase 4 — branches are pruned, added, re-scored as
  evidence accumulates.
- Cross-reference: opportunities cite personas by stable
  handle; solutions reference candidate FRs once the SRS is
  sketched.
- Write to `docs/01-discovery/ost.md` (initial sketch in
  Phase 1; refined continuously through Phase 4).

## Handoffs to Other Skills

- **From `vision-author`** — the vision's stated outcome maps
  to the tree's outcome node.
- **From `kpi-author`** — the primary KPI sits at the outcome.
- **From `persona-author`** — opportunities are rooted in
  persona pains and JTBD.
- **To `srs-author`** — candidate solutions become candidate
  FRs once pruned and prioritized.
- **To Phase-4 continuous discovery** (the user-invocable
  `discovery-tick` skill) — discovery findings update the tree
  weekly.
- **To Phase-7 optimization** — post-launch experiments live
  on the tree's solution branches.
- **From the user-invocable `draft-ost`** — peer skill.

## Edge Cases

- **Sponsor wants the tree to reach the launch milestone.**
  This is the wrong artifact — the tree exists past launch.
  Refuse to scope-cap it; instead surface that the master
  schedule (per `master-schedule-author`) handles the launch
  deadline and the OST is a continuous artifact.
- **Opportunities outnumber personas 5:1.** Some opportunities
  span multiple personas; mark them as "cross-persona" rather
  than duplicating. If still bloated, surface that personas
  may be too coarse and re-enter `persona-author` to split.
- **Solution count explodes** (>20 per opportunity). The tree
  is becoming a backlog. Prune to 3–5 highest-evidence
  solutions per opportunity; archive the rest in a "considered
  and parked" appendix.
- **No persona evidence for a proposed opportunity.** Refuse;
  this is the §4.4 anti-pattern "we already know what to
  build" or "internal hypotheses as user evidence." Either
  gather the evidence (re-enter user research) or remove the
  opportunity.
- **Tree spans multiple outcomes.** Each outcome gets its own
  tree (multi-tree appendix); refuse to ship a tree with two
  competing primary outcomes.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §4.2.7.
The user-invocable `draft-ost` is a peer skill producing the
same artifact via a different procedure.

## Self-Audit

Before declaring an OST complete, confirm:
- The outcome node names a primary KPI (cited from the KPI
  doc by stable name).
- Every opportunity cites ≥1 persona by stable handle AND
  ≥1 evidence source.
- Every solution branch has a RICE placeholder (even if
  unscored at Phase 1).
- No "invented" opportunities lacking persona evidence.
- The tree has ≤7 opportunities at the top level (more is
  scope creep; revisit).
- ≤5 solutions per opportunity (more is backlog noise; archive
  the rest).
