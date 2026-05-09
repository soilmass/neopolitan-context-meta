---
name: aeo-baseline-author
description: >
  Authors the AI Search (AEO / GEO / LLMO) baseline — manual
  prompt testing across ChatGPT, Perplexity, Google AI Overviews,
  Gemini, Claude. Per engine: 10-20 prompts in the project's
  topic area; track citation rate, accuracy of brand
  representation, sentiment. Writes to
  docs/07-postlaunch/aeo-baseline-<YYYY-MM-DD>.md (SOP §10.2.3 +
  §10.3.3 monthly cadence). Use at T+8 baseline and monthly
  during Phase 7. Do NOT use for: classic SEO ranking baseline
  (operator-driven via Search Console / Ahrefs / Semrush — out
  of scope here); content audit (folds into optimization-backlog-
  author); the diagnostic sweep (use diagnostic-sweep-author —
  AEO is one diagnostic dimension; this atom is its dedicated
  spec); the optimization loop (use optimization-loop-author for
  AI-search experiments).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable aeo-baseline skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# aeo-baseline-author

Phase 7 — produce the AI Search baseline + monthly tracking.

## When to Use

- T+8 weeks; classic SEO baseline is settled; AEO baseline is
  due as part of the Phase 7 measure phase per SOP §10.2.3.
- Monthly during Phase 7 ongoing operations per §10.3.3 — AI
  citation tracking is monthly cadence.
- Post-major-content-launch (e.g., a new pillar published)
  warrants AEO measurement to track citation acquisition
  velocity.
- A regulatory request for transparency about AI brand
  representation needs a documented AEO baseline.

## When NOT to Use

- Classic SEO ranking baseline — operator-driven via Search
  Console / Ahrefs / Semrush; this atom is AEO-specific
  (see SOP §5.4.5 two-track measurement; classic SEO is the
  first track, AEO is the second).
- Content audit — folds into `optimization-backlog-author`
  (Tier 1 here) and ongoing content-team work.
- Diagnostic sweep — `diagnostic-sweep-author` (Tier 2 here).
  AEO is one diagnostic dimension; this atom is its
  dedicated artefact.
- Optimization loop — `optimization-loop-author` (Tier 1).
  Use loop for testing AI-search-targeting experiments.
- Schema markup specification — that's a Phase 2 deliverable
  (per SOP §5.4.3), out of scope here. AEO measures the
  *effects* of schema; doesn't author the schema itself.
- E-E-A-T / entity authority work — Phase 2 +
  ongoing-content-team work; this atom measures the result.
- A single-prompt diagnostic — refuse; AEO baseline is
  ≥10 prompts per engine to surface patterns.

## Capabilities Owned

- Define **prompt sets per engine** (ChatGPT, Perplexity,
  Google AI Overviews, Gemini, Claude per SOP §10.2.3):
  - 10-20 prompts in the project's topic area.
  - Mix of intent types: informational, navigational,
    transactional, commercial, comparison.
  - Brand-direct prompts ("Tell me about [Brand]") + topic-
    direct prompts (no brand mention, see if brand is
    cited).
- Track **per prompt + engine**:
  - Citation rate (was the brand cited at all?).
  - Citation position (first / middle / last in the
    response?).
  - Accuracy of representation (brand description correct?
    factually right? aligned with positioning?).
  - Sentiment (positive / neutral / negative).
  - Linked URL (which page got cited; canonical?).
- Document **brand mentions monitoring** — sentiment trend
  across the prompt set; outlier hits or misses.
- Track **competitive AI citations** — for each prompt, who
  else got cited; pattern across competitors.
- Synthesize **monthly delta** — citation rate up / down vs
  prior month; new citations gained; citations lost.
- Recommend **AEO-targeted optimization** candidates for the
  optimization backlog — content gaps surfaced (topics
  competitors get cited for that we don't), schema gaps
  (page types not getting cited that should), entity-
  authority gaps (E-E-A-T signals weak).
- Cite the **content matrix** + **schema spec** (SOP §5.4.3)
  + **classic SEO baseline** by stable reference.
- Write to `docs/07-postlaunch/aeo-baseline-<YYYY-MM-DD>.md`
  (one per month at first; consolidate quarterly).

## Handoffs to Other Skills

- **From the manual prompt testing** — operator-driven
  data collection via the engine UIs (or via a tool like
  Profound / Otterly that automates).
- **From the content matrix** (SOP §5.4.2) — content
  inventory anchors prompt-set design.
- **From `kpi-author`** (site-build) — AEO citation rate
  is often a KPI in 2026-tier projects.
- **To `optimization-backlog-author`** (Tier 1 here) —
  AEO findings seed backlog items.
- **To `monthly-stakeholder-report-author`** (Tier 2 here)
  — AEO movement is a monthly memo section.
- **To `quarterly-business-review-author`** (Tier 2) —
  AEO trajectory feeds competitive position.
- **To `optimization-loop-author`** (Tier 1) —
  AI-search-targeting experiments use the baseline.
- **From the user-invocable `aeo-baseline`** — peer skill
  producing the same artifact via a different procedure.

## Edge Cases

- **No citations across all engines.** Surface as a finding
  — the project is AI-invisible. Recommend immediate
  content + schema + entity-authority work.
- **Competitor citation rate dominates.** Document the gap;
  recommend specific catch-up content (the topics the
  competitor owns that we don't).
- **Inaccurate brand representation in AI responses.**
  Document each inaccuracy; recommend canonical-content
  updates (often E-E-A-T signals at the source).
- **Volatility between runs** (AI engines return different
  results day-to-day). Run the prompt set twice 24h apart
  in the baseline; document variability; treat low-
  variability prompts as more reliable signals.
- **Tool automation unavailable** (Profound / Otterly
  budget; manual testing only). Document the manual
  methodology + sample size; surface the limitation.
- **A new AI search engine emerges** (post-2026
  expansion). Add to the prompt set; document baseline
  immediately so trends start from now.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.2.3
+ §10.3.3 + §5.4.5 (two-track measurement). The
user-invocable `aeo-baseline` is a peer skill producing
the same artifact via a different procedure.

## Self-Audit

Before declaring an AEO baseline complete, confirm:
- All 5 engines covered (ChatGPT / Perplexity / AI
  Overviews / Gemini / Claude) OR explicit waiver with
  rationale.
- 10-20 prompts per engine spanning intent types.
- Per prompt × engine: citation rate + position +
  accuracy + sentiment + linked URL.
- Monthly delta surfaced (when running monthly cadence).
- Competitive AI citations tracked.
- Optimization-backlog candidates derived.
- Cross-references to content matrix + schema spec +
  classic SEO baseline.
- Volatility note (re-runs same-day or 24h-apart).
