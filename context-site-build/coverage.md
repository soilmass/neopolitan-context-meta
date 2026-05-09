# context-site-build Coverage

Last verification: 2026-05-08 (initial bootstrap; no skills yet).

The library claims one super-domain — **site-build methodology** —
broken into seven phase-aligned families. Each family corresponds
to one phase of the documented SOP and produces the deliverables
for that phase.

Per the meta-pipeline's `ARCHITECTURE.md` §"Coverage Discipline",
silent gaps are the failure mode this document exists to prevent.

---

## Domains Claimed

| Domain | Family | Coverage |
|---|---|---|
| (none yet) | — | bootstrap families via family-bootstrap |

No families bootstrapped yet. Each entry in **Domains Deferred**
below has an explicit build trigger; the first to fire becomes the
first claimed family.

---

## Domains Deferred

| Domain | Why deferred | Build trigger |
|---|---|---|
| `site-build` | Not yet bootstrapped | First Phase-N deliverable (any of: vision / persona / SRS / ADR / runbook / baseline-report / etc.) needs an audited, conformant skill |

(Per finding B2 / A58: each individual phase has fewer than the 10 capabilities required by `family-bootstrap` Stage 2's gate; the natural cut for a methodology domain is **one family with phase-organized tiers**, not one family per phase. The authority — site-build-procedure.md — describes a single methodology with ~30+ deliverables across 7 phases.)

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

## Cross-Domain Orchestrators

None at v0.1.0. When two phase-aligned families both claim
deliverables (e.g., `discovery` produces personas, `requirements`
references them), a cross-domain orchestrator may be authored via
the meta-pipeline's `cross-domain-orchestrator-author`.

Build trigger: ≥2 families exist AND a workflow spans both.

---

## Coverage Matrix Status

No skills yet — fresh library (will populate after first
family-bootstrap run).

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
