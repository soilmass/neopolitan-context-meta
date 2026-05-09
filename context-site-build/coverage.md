# context-site-build Coverage

Last verification: 2026-05-08 (v0.5.0 — Phase 4 stack-specific
policy overlays authored; library now hosts 3 families + 21 stack
overlays = 68 skills total. **Significant ahead-of-trigger build**;
see "v0.5.0–v1.0.0 Ahead-of-Trigger Note" section below).

Previous verification: 2026-05-08 (v0.4.0 — site-operate family
bootstrapped; library hosts 3 families = 47 skills total).

Previous verification: 2026-05-08 (v0.3.0 — site-design family
bootstrapped; 2 families = 32 skills).

Previous verification: 2026-05-08 (v0.2.0 — site-build family
Tier 2/3 completion; 16 atoms + 1 router).

Previous verification: 2026-05-08 (v0.1.0–v0.1.2 — initial library
+ site-build Tier 1 + self-review).

The library claims the **site-build methodology** super-domain,
authoring it across multiple phase-aligned families. Each family
covers a coherent slice of the 7-phase methodology.

Per the meta-pipeline's `ARCHITECTURE.md` §"Coverage Discipline",
silent gaps are the failure mode this document exists to prevent.

---

## Domains Claimed

### Family-organized atoms (47)

| Domain | Family | Coverage |
|---|---|---|
| Methodology spine — Phase 1 (Discovery) + Phase 2 (Requirements) + Phase 5/6 (Hardening + Launch spine) + Phase 7 (Post-launch spine) + cross-phase change control | `site-build` | 16 atoms (6 Tier 1, 5 Tier 2, 5 Tier 3) + 1 router. Authored v0.1.0–v0.2.0. |
| Phase 3 Design + Awwwards-tier creative phases (mood board, art direction, concept, motion language) + Phase 4 continuous discovery synthesis | `site-design` | 14 atoms (7 Tier 1, 5 Tier 2, 2 Tier 3) + 1 router. Authored v0.3.0. |
| Phase 5 a11y conformance + Phase 6 launch communications + Phase 7 full (stabilization, hypercare, optimization, monthly + quarterly + annual reports) + Awwwards-tier polish + awards | `site-operate` | 14 atoms (7 Tier 1, 5 Tier 2, 2 Tier 3) + 1 router. Authored v0.4.0. |

### Stack-specific policy overlays (21, v0.5.0)

Per docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4. All 21 ahead-of-
trigger; see "v0.5.0–v1.0.0 Ahead-of-Trigger Note" below.

| Bucket | Overlays | Applies on top of |
|---|---|---|
| Combo A (Next.js × 3) | `house-site-{build,design,operate}-nextjs` | site-build / site-design / site-operate mechanism atoms |
| Combo B (Nuxt × 3) | `house-site-{build,design,operate}-nuxt` | same |
| Combo C (Astro × 3) | `house-site-{build,design,operate}-astro` | same |
| Combo D (SvelteKit × 3) | `house-site-{build,design,operate}-sveltekit` | same |
| Webflow visual-editor (× 3) | `house-site-{build,design,operate}-webflow` | same |
| Cross-stack (× 2) | `house-site-design-motion`, `house-site-design-a11y` | motion-language-author + design-tokens-author / a11y-annotations-author |
| Design-tool (× 1) | `house-site-design-figma` | design-tokens-author + design-system-author + engineering-handoff + states-matrix |
| Hosting (× 3) | `house-site-operate-{vercel,cloudflare,netlify}` | runbook-author + launch-comms-author + optimization-loop-author + optimization-backlog-author |

The three families are siblings within `context-site-build`. They
cross-reference at phase boundaries:
- `design-philosophy-author` (site-build Tier 3) hands off to
  site-design's Tier 1 atoms.
- `art-direction-author` (site-design) cites `vision-author` and
  `persona-author` (site-build).
- `polish-discipline-author` (site-operate) cites
  `art-direction-author` + `motion-language-author` +
  `component-states-matrix-author` (all site-design).
- `awards-submission-author` (site-operate) cites virtually every
  prior atom — the awards package is the cumulative output.
- `optimization-loop-author` (site-operate) cites the SRS NFRs
  (`srs-author`, site-build) as guardrail metrics.

---

## Domains Deferred

| Domain | Why deferred | Build trigger |
|---|---|---|
| Cross-cutting tools (`performance-budget-author`, `motion-conformance-author`, `analytics-instrumentation-author`, `aeo-schema-author`, `i18n-strategy-author`, `error-monitoring-setup-author`, `release-discipline-author`) | Free-standing tool atoms outside any family. | Phase 5 of Option C per `docs/ARCHITECTURE-OPTIONS-v0.2.md`; planned for v0.6.0 (PR #7). |
| Phase 4 Build ceremonies (sprint planning, working software per sprint, sprint review notes) | Build-phase ceremonies are operator-driven, not skill-driven. | n/a — out of library scope per family Out-of-Scope rows. |
| Adjacent-awards-body submissions (Webby, FWA, CSSDA, Communication Arts) | `awards-submission-author` (site-operate Tier 3) covers Awwwards as the canonical pattern; adjacent bodies follow but with body-specific criteria. | Operator decides to submit for an adjacent body; pattern adapts from awards-submission-author with per-body deltas documented. |

---

## Domains Out of Scope

| Domain | Why out of scope | Where to look instead |
|---|---|---|
| Skill lifecycle (author / audit / refactor / retire / migrate / evaluate / policy-overlay / snapshot-diff) | Belongs to the meta-pipeline | `context-meta-pipeline` plugin |
| Library lifecycle (library-audit / library-bootstrap) | Belongs to the meta-pipeline | `context-meta-pipeline` plugin |
| Cross-orchestration | Belongs to the meta-pipeline | `context-meta-pipeline` plugin |
| Domain skills outside site-build (git, postgres, kubectl, …) | Out of this library's scope | Their own consumer libraries (e.g., `context-git`) |
| Plugin packaging mechanics | Belongs to Claude Code itself | Claude Code documentation |
| Runtime / load-time skill loading | Belongs to Claude Code itself | Claude Code documentation |

---

## v0.5.0–v1.0.0 Ahead-of-Trigger Note

Per `context-meta-pipeline` audit finding **A56** (the v0.7.0
discipline-shift commitment): "any future v0.7.x or v0.8.0 work
that proposes building ahead-of-trigger items must include explicit
operator approval matching v0.7.0's approach." The v0.5.0 stack-
overlay batch is the largest single ahead-of-trigger build to date
in this library; all 21 overlays were authored without the trigger
("≥2 tiers of `house-*` overlays exist on the same mechanism atom"
per the meta-pipeline's `docs/PATH-TO-V1.md` P4) firing.

**Operator approval source**: 2026-05-08 plan-mode approval of the
maximalist Phase 4 scope (21 overlays vs the 3-5 originally specced
in `docs/ARCHITECTURE-OPTIONS-v0.2.md`). User chose
`maximalist on every dimension` for this PR + the 4 PRs that follow.

**Disclosure pattern adopted** (mirrors meta-pipeline v0.7.0):

1. Each overlay's SKILL.md body begins with a top-of-body comment:
   `> pre-trigger build (v0.5.0); reassess when ≥2 tiers of house-*
   overlays exist on the same mechanism atom per docs/ARCHITECTURE-
   OPTIONS-v0.2.md Phase 4.`
2. The library's CHANGELOG.md `[0.5.0]` block leads with a
   `### ⚠ Discipline-shift disclosure` subsection.
3. Audit-finding ledger entry **B9** (below) documents the operator
   approval + the discipline-restoration commitment for v1.0.x
   onward.

**Discipline-restoration commitment for v1.0.x and beyond**: After
v1.0.0 ships, no new atoms or overlays will be authored without an
organic build trigger firing on a real consumer project. Library
growth post-v1.0 is consumer-driven, not speculation-driven. The
v0.5.0–v1.0.0 ahead-of-trigger window is bounded; v1.0.x is the
restoration boundary.

---

## Cross-Domain Orchestrators

None at v0.5.0. The three families (`site-build` + `site-design` +
`site-operate`) cross-reference at phase boundaries via per-atom
Handoffs sections; the 21 stack overlays compose with mechanism
atoms via CSS-cascade-style overrides. No orchestrator skill yet
bundles a multi-family workflow.

Build trigger: a recurring multi-family workflow with ≥3 stages
emerges (e.g., a "phase-1-to-3 walk" that runs vision-author →
persona-author → kpi-author → ost-author → mood-board-author →
art-direction-author → concept-author in sequence). Until then,
operators sequence the atoms manually.

---

## Coverage Matrix Status

Last verification: 2026-05-08 (v0.5.0).

| Family | Atoms | Router | Health |
|---|---|---|---|
| `site-build` | 16 (6 Tier 1, 5 Tier 2, 5 Tier 3) | `site-build` v0.1.2 | All 17 healthy; drift 0.0%–8.8% |
| `site-design` | 14 (7 Tier 1, 5 Tier 2, 2 Tier 3) | `site-design` v0.1.0 | All 15 healthy; drift 0.0%–9.1% |
| `site-operate` | 14 (7 Tier 1, 5 Tier 2, 2 Tier 3) | `site-operate` v0.1.0 | All 15 fresh; audit pending |
| **Stack overlays** | 21 (15 stack-family + 2 cross-stack + 1 design-tool + 3 hosting) | n/a | All 21 fresh; audit pending |

Total: **68 skills** (44 atoms + 3 routers + 21 policy overlays).
All three families' in-family deferred queues remain empty.

Tier transitions since last verification: 21 stack-specific policy
overlays authored at v0.1.0; library version bumped to v0.5.0
(MINOR — new skills).

---

## Audit-finding ledger

Findings produced by dogfood walkthroughs against this library.
Numbering is contiguous across releases and prefixed `B` to
distinguish from the meta-pipeline's `A` series.

| ID | Source | Finding | Disposition |
|----|--------|---------|-------------|
| B1 | 2026-05-08 library-bootstrap Stage 7 (first real-consumer dogfood) | `validate-metadata.py --all` errors with exit 2 on an empty `skills/` directory. The library-skeleton.md verify.sh template assumed it would exit 0 for fresh libraries (mirroring `coverage-check.py` which was patched per A31). | **Fixed** — meta-pipeline patch added `--allow-empty` flag; `verify.sh` template (this library) updated to use it. Cross-referenced as A57 in meta-pipeline ledger. |
| B2 | 2026-05-08 family-bootstrap Stage 1 intake (initial discovery-only attempt) | Phase-per-family was the obvious-but-wrong cut. Each individual phase (Phase 1 discovery: ~7 deliverables; Phase 5 hardening: ~2; Phase 6 launch: ~1) falls below the 10-capability gate at family-bootstrap Stage 2. The site-build SOP is one methodology with phase-organized chapters, not 7 disjoint domains. | **Restructured** — coverage.md now declares one `site-build` family covering the whole methodology with phase-organized tiers. Cross-referenced as A58 in meta-pipeline ledger (informational; the gate isn't wrong, the mental model was). |
| B3 | 2026-05-08 family-bootstrap Stage 1 (site-build domain intake) | The Stage 1 gate "authority cites a URL AND a named author" excludes legitimate internal/private SOPs. The site-build-procedure.md is a real authored SOP with a named author (operator) and canonical local path, but no public URL. The gate's intent (no "general consensus" sources) is satisfied; the literal URL requirement is not. | **Workaround** — `domain-intake.yaml` records `url: internal://...` plus a `path:` field. **Suggested patch (deferred to L7)**: `family-bootstrap/references/domain-intake-checklist.md` should document the `internal://` URI convention and the additional `path:` field for internal authorities. Cross-referenced as A59 in meta-pipeline ledger. |
| B4 | 2026-05-08 family-bootstrap Stage 6 advisory audit | All 4 of vision-author / persona-author / adr-author / baseline-report-author flagged for description drift on first audit (10.0% – 22.6% vs <10% threshold). Description vocabulary diverged from body vocabulary — words like "kickoff", "set", "who", "why", "structured", "around" appeared in description but not body. **Reproduces the v0.2.0 family-bootstrap dogfood finding** ("8 of 9 freshly-bootstrapped skills failed the drift gate immediately"). | **Resolved by iteration** — tightened descriptions to align vocabulary; all 7 atoms now pass drift gate (≤8.8%, vision-author at 0.0%). Cross-referenced as A60 in meta-pipeline ledger. **Validates the procedure** — Stage 6 advisory audit correctly surfaced drift; the iterate-to-pass loop is the right shape. |
| B5 | 2026-05-08 L7 backfill (meta-pipeline patch authoring) | When authoring two new reference docs (`methodology-domains.md` for A58 and an addition to `domain-intake-checklist.md` for A59), operator cross-referenced them via `references/<other>.md` paths. `validate-metadata.py` correctly rejected with: "references must not link to other references in the same skill (per METADATA-VALIDATION.md)". | **Validator working as designed** — no patch needed. Cross-references rewritten as prose mentions without paths. Cross-referenced as A61 in meta-pipeline ledger. **Useful observation**: the rule prevents reference-doc DAGs that get fragile under refactor; the operator surfaced this rule by violating it during normal authoring. |
| B6 | 2026-05-08 self-review of v0.1.0 family (post-bootstrap) | 5 of 6 atoms had description anti-triggers of the form `(use X-author when authored)` for skills that don't exist yet. Pattern is unactionable as routing guidance — the LLM router cannot route to a non-existent skill. The 6th atom (`adr-author`) had the correct pattern: `(use the user-invocable draft-X, or X-author when built)`. | **Fixed in v0.1.2** — 5 atoms updated to follow the adr-author pattern (anti-trigger names the user-invocable peer in the operator's environment as the fallback). Cross-referenced as A62 in meta-pipeline ledger. **Suggested addition to `skill-author/references/audit-ritual.md`** (deferred): a "anti-trigger fallback discipline" sub-section naming this pattern. |
| B7 | 2026-05-08 self-review | `runbook-author` and `baseline-report-author` cited cross-family siblings (launch-comms-author, hypercare-digest, stabilization-report-author, win-regression-report-author, optimization-backlog-author, etc.) using "(deferred)" or "(when built)" qualifiers, suggesting "coming soon to this family" when reality is "different family that doesn't exist yet". Per the family's coverage.md Out of Scope, those siblings belong to a future `site-operate` family. | **Fixed in v0.1.2** — anti-triggers and Handoffs re-framed as "handled by the future site-operate family; user-invocable peer covers it now." Cross-referenced as A63 in meta-pipeline ledger. **Validates the Out-of-Scope discipline** in coverage.md — without explicit OoS rows, the operator would have absorbed these siblings into the family's nominal scope. |
| B8 | 2026-05-08 self-review | `site-build` router's Routing Table listed 10 deferred Tier 2/3 atoms alongside the 6 Tier 1 atoms. 62% of the table pointed at unbuilt skills, polluting routing-eval signal (the LLM router treats every row as a real target). | **Fixed in v0.1.2** — Routing Table reduced to 6 Tier 1 rows. Deferred atoms remain documented in "Atoms in This Family" and in `taxonomy.md`. Disambiguation Protocol updated to cover user-invocable fallback. Cross-referenced as A64 in meta-pipeline ledger. **Suggested addition to `family-bootstrap` Stage 4 procedure** (deferred): the router's Routing Table should include only built atoms; specced atoms belong in `## Atoms in This Family` only. |
| B9 | 2026-05-08 v0.5.0 stack-overlay batch authoring | The maximalist Phase 4 build (21 overlays in one PR) is the largest single ahead-of-trigger commitment in this library to date. Per A56 the v0.7.0 disclosure pattern should mirror across the consumer library. | **Disclosed** — v0.5.0–v1.0.0 Ahead-of-Trigger Note added to coverage.md (above); per-overlay top-of-body markers added; CHANGELOG `[0.5.0]` block leads with `### ⚠ Discipline-shift disclosure`. **Discipline-restoration commitment**: post-v1.0.0, no new atoms ship without an organic trigger firing on a real consumer project. The v0.5.0–v1.0.0 ahead-of-trigger window is bounded; v1.0.x is the restoration boundary. |
