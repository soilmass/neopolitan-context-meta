# Library Coverage

The plugin claims one domain — **skill governance and lifecycle**.
Everything else is out of scope or deferred. Per `ARCHITECTURE.md`
§"Coverage Discipline", silent gaps are the failure mode this document
exists to prevent.

Last verification: 2026-05-06 (v0.7.0 — Phase 3 of v0.7.0 build-out. ⚠
**discipline shift, deliberately taken**: built five pre-trigger pieces
of deferred infrastructure (integration-test-runner, search-skills +
gen-index + INDEX.md, snapshot-hash + signed tags, notify-dependents +
notification-channels, analytics-rollup + telemetry stub) per consumer-
library readiness. metadata.tags rollout to all 14 skills + check_tags
validator. 9 reference docs across 7 thickened skills (each marked
speculative). 4 governance docs flipped Deferred → Built ahead of trigger.
ARCHITECTURE.md §"v0.7.0 Ahead-of-Trigger Note" explicitly discloses the
discipline shift. release-tag.sh now signs tags by default. 14 SKILL.md
hashes computed + stored. 14 PATCH bumps. verify.sh now 15 steps.)

Previous verification: 2026-05-06 (v0.6.2 — compose what exists. Phase 2 of
v0.7.0 build-out. audit-skill --apply-banners + --write-health (string-replace
surgery on frontmatter; idempotent). changelog-sync.py cross-references skill
↔ library changelogs. routing-eval-runner --input + --operator-transcript
let verify.sh exercise external + operator modes. recency_pin: stable rolled
out to 5 lifecycle skills. release-tag.sh Step 1.5 runs health audits
before tagging; refuses on unhealthy unless --allow-unhealthy. SNAPSHOT.lock
health transitioned all 14 from fresh → healthy.)

Previous verification: 2026-05-06 (v0.6.1 — code-quality cleanup + foundational
wiring. Phase 1 of v0.7.0 build-out. _skill_io.py shared module replaces
7 in-script parsers. check_depends_on_freshness catches stale pins.
gate_eval_coverage Gate 5 added (mechanizable today). routing-eval.yaml
expanded so every skill has ≥3 prompts. verify.sh step 10 + unified summary.
Zero per-skill version bumps; pure library-side refactor.)

Previous verification: 2026-05-06 (v0.6.0 — expansion docs + extension-seam
contract tests landed. EXTENSION-POINTS.md / docs/PATH-TO-V1.md /
ARCHITECTURE.md §"Extension Points" / 3 fixture trees / verify.sh step 9
/ Makefile target extension-check / CI extension-seams job. Library
is feature-complete for skill-governance self-administration; further
v1.0 path requires real consumer libraries. validate-metadata.py
gained explicit archetype rejection (silent fallback to atom was a
real gap surfaced by the dummy-archetype fixture).)

Previous verification: 2026-05-06 (v0.5.2 — testing pass Phase 2: 9 v0.5.0
skills walked end-to-end as in-memory dogfood; 13 audit findings
A22-A34 captured below; 6 PATCH-bumped skills with explicit changelog
entries; 2 cross-skill handoff fixtures added under
scripts/tests/fixtures/handoffs/; routing-eval.yaml extended with 16
v0.5.0-cluster prompts; static_routing in routing-eval-runner.py
de-ranks routers 0.7×).

Previous verification: 2026-05-06 (v0.5.1 — testing pass Phase 1: closed
zero-fixture gaps for 4 load-bearing scripts; added 6 adversarial
inputs + boundary cases; verify.sh extended to 8 steps; caught and
fixed git-cwd bug in rollback-skill.py).

Previous verification: 2026-05-06 (v0.5.0 — kitchen-sink meta-tooling
release; 8 new lifecycle skills + 1 router added (skill-author/
skill-audit/skill-refactor/skill-retire/family-bootstrap remain;
new: skill-evaluate, skill-policy-overlay, skill-migrate,
skill-snapshot-diff, library-bootstrap, library-audit,
cross-library-orchestrator, cross-domain-orchestrator-author + meta
router). 7 governance docs moved Deferred → Currently Documented
(each with pre-trigger N/A disclaimer). 7 new scripts. Three
ARCHITECTURE.md open questions resolved (library-level routing,
cross-domain orchestrator pattern, policy overlay composition);
one new open question (cross-cluster meta-router threshold).

---

## Domains Claimed

| Domain | Family | Coverage |
|---|---|---|
| Skill lifecycle (author, audit, refactor, retire, migrate, evaluate, policy-overlay, snapshot-diff) + library lifecycle (audit, bootstrap) + cross-orchestration (cross-domain, cross-library) + family bootstrap | meta (router) | this plugin |

As of v0.5.0 the cluster has 13 atoms + 1 router (`meta`). The router
was added when the cluster exceeded the 5-atom threshold from
`ARCHITECTURE.md` §"Routing and Contention" / §"Per-domain routers".
The mental-model name is `meta` rather than `skill` (which would
collide with the `skill-*` prefix used by 8 of the 13 atoms).

The 13 atoms cluster around three sub-themes:

- **Per-skill lifecycle** (author / audit / refactor / retire / migrate
  / evaluate / policy-overlay / snapshot-diff)
- **Library lifecycle** (library-audit / library-bootstrap)
- **Composition** (family-bootstrap / cross-domain-orchestrator-author
  / cross-library-orchestrator)

---

## Domains Deferred

After v0.5.0 moved the four previously-deferred lifecycle / library /
cross-orchestrator skills to Domains Claimed (each shipping with a
pre-trigger note acknowledging the build trigger may not yet have
fired), the remaining deferred concerns are infrastructure-level
and depend on consumer-side dogfood:

| Domain | Why deferred | Build trigger |
|---|---|---|
| Real routing-layer runner (paired with `skill-evaluate`) | The runner authored at `scripts/routing-eval-runner.py` operates in static-heuristic / operator / external modes only — without a real LLM-based routing classifier, machine-graded triggering accuracy is approximate | Claude Code load-time hooks exist OR a consumer library builds a routing-judge pipeline |
| Multi-tier policy composition system | Single-tier composition via `skill-policy-overlay` covers v0.5.0; multi-tier (`acme-base` + `acme-frontend` overrides on the same mechanism) is documented in `ARCHITECTURE.md` §"Policy Overlay Composition" but not built | 2+ tiers of `house-*` overlays exist on the same mechanism atom |
| Cross-cluster meta-router | The per-cluster `meta` router covers the meta-pipeline. Cross-cluster (across families in a consuming library) needs concrete prompts spanning families to inform design | First consumer library hosts 5+ families AND prompts spanning ≥3 families become common |
| Auto-prepending health banners at skill load time | Documented in `MAINTENANCE.md` §Auto-Warn; ships with `audit-skill.py` Stage 5 generating banners and operators applying them | Claude Code core gains a load-time hook for description-prepending |
| Persistent dogfood smoke runner | Smoke fixture exists at `scripts/tests/smoke/bootstrap-git-family/`; an automated runner that walks `family-bootstrap` end-to-end against the fixture is rejected per Out of Scope (procedural skills should not have script-driven runners) | n/a — rejected. Operator-driven walk against the fixture is the procedure. |

---

## Domains Out of Scope

These are domains the meta-pipeline will not claim, with rationale and
pointer.

| Domain | Why out of scope | Where to look instead |
|---|---|---|
| Domain skills themselves (git, postgres, kubectl, pdf, …) | This is a meta-pipeline; it produces such skills, doesn't ship them | Use `family-bootstrap` to produce them in your own consuming library |
| Plugin packaging mechanics (`plugin.json` schema, `marketplace.json` schema) | Belongs to Claude Code itself, not to skill governance | Claude Code documentation |
| Skill *runtime* (how skills load, frontmatter parsing at load time) | Belongs to Claude Code itself | Claude Code documentation |
| Website-build skills (`building-website-specs`, `frontend-design`, etc.) | Domain-specific; mentioned in `ARCHITECTURE.md` §"The Layered Map" only as examples | Separate domain plugins (e.g., `site-context-core`) |
| Stack adapters (e.g., a `nextjs` policy overlay) | Domain-specific | `site-context-nextjs` is the existing pattern |
| **Script-driven runners for procedural lifecycle skills** (e.g., a hypothetical `scripts/family-bootstrap.py` that runs `family-bootstrap`'s 6 stages automatically) | Re-introduces the framework antipattern the architecture rejects: the lifecycle skills are *procedural by intent*. Their value is in the gated stages requiring operator judgment, not in the steps a script could take. Authoring a runner would shift the contract from "operator follows a procedure" to "script enforces a workflow," eroding the read/write boundaries that the procedural design exists to preserve. | The skills themselves under `skills/` — invoked by the operator following the SKILL.md. v0.5.0 audit finding M4 (rejected). |

---

## Cross-Domain Orchestrators

None in v0.1.0. The meta-pipeline operates on a single library at a
time. When a second consumer library exists, a
`cross-library-orchestrator` will become real (and migrates from the
Deferred table above).

---

## Coverage Matrix Status

| Skill | Recency | Test pass | Triggering | Drift | Status |
|---|---|---|---|---|---|
| `skill-author` | ✓ fresh | N/A | N/A | ✓ | passing |
| `family-bootstrap` | ✓ fresh | N/A | N/A | ✓ | passing |
| `skill-audit` | ✓ fresh | N/A | N/A | ✓ | passing |
| `skill-refactor` | ✓ fresh | N/A | N/A | ✓ | passing |
| `skill-retire` | ✓ fresh | N/A | N/A | ✓ | passing |

N/A entries: per `MAINTENANCE.md` and `skill-audit/references/health-gates.md`,
the test-pass-rate gate is deferred until SKILL.md test infrastructure
exists (`INTEGRATION-TESTING.md` build trigger), and the triggering-
accuracy gate is deferred until the routing-eval suite exists
(`skill-evaluate` build trigger above).

Tier transitions since last verification: none.

v0.4.1 verification 2026-05-06: all 21 dogfood audit findings
applied (3 in v0.4.0 + 18 in v0.4.1). 5/5 skills validate clean,
17/17 fixtures behave correctly. Reference docs grew within
bounds (`tier-model.md` 117→221, `naming.md` 92→110,
`archetypes.md` 142→153 — all under 300-line ToC threshold).
Detailed in `CHANGELOG.md` under `[0.4.1]`.

v0.4.0 verification 2026-05-06: 5/5 skills validate clean, 17/17
fixtures behave correctly, audit passes implementable gates,
new router-atom-resolves check works correctly (silent on the
meta-pipeline's own skills since none are routers; correctly
warns about 9 unresolved Tier 2/3 atoms when run on the dogfood
`git` router). family-bootstrap dogfood produced 21 audit findings;
3 highest-leverage procedure gaps (A11, A19, A21) applied.
Detailed in `CHANGELOG.md` under `[0.4.0]`.

v0.3.0 verification 2026-05-06: 5/5 skills validate clean, 17/17
fixtures behave correctly, audit passes implementable gates,
boundary-condition sweep clean (1024/500/300/1000 thresholds exact),
triple-consistency check on required-sections agrees across
METADATA-VALIDATION.md / validate-metadata.py / detect-breaking-changes.py.
Real bugs (SemVer regex + numeric-name crash) fixed and verified.
Operational scaffolding (LICENSE, requirements.txt, .gitignore,
Makefile, CONTRIBUTING.md, GitHub Actions CI) all shipped.
Detailed in `CHANGELOG.md` under `[0.3.0]`.

v0.2.1 verification 2026-05-06: all five lifecycle skills present and
`validate-metadata.py --all` clean (exit 0). 11-category test sweep
all green; doc-vs-implementation audit complete with no remaining
stale claims. Detailed in `CHANGELOG.md` under `[0.2.1]`.

v0.2.0 verification 2026-05-06: all five lifecycle skills present and
`validate-metadata.py --all` clean (exit 0). `audit-skill.py --all`
exits 0 with drift between 0.0% and 9.1%. `verify.sh` exits 0 with
version triangulation consistent. 18-fixture matrix exercises the new
validator checks across all five archetypes. Detailed in `CHANGELOG.md`
under `[0.2.0]`.

v0.1.2 verification 2026-05-06: all five lifecycle skills present and
`validate-metadata.py --all` clean (exit 0). Four skills now at v0.1.1+
(skill-author at v0.1.2; family-bootstrap / skill-audit / skill-refactor
/ skill-retire at v0.1.1). Detailed in `CHANGELOG.md` under `[0.1.2]`.

v0.1.1 verification 2026-05-06: all five lifecycle skills present and
`validate-metadata.py --all` clean (exit 0). Two skills (`skill-author`,
`skill-audit`) bumped to v0.1.1 for clarification-only changes; the
other three remained at v0.1.0. Detailed in `CHANGELOG.md` under
`[0.1.1]`.

Initial verification 2026-05-06: all five lifecycle skills present and
`validate-metadata.py --all` clean.

---

## Audit-finding ledger

Findings produced by dogfood walkthroughs. The numbering is contiguous
across releases. Each row records what surfaced and where the fix
landed (if any).

| ID | Source | Finding | Disposition |
|----|--------|---------|-------------|
| A1–A21 | v0.4.0/v0.4.1 family-bootstrap dogfood | 21 findings; documented in `CHANGELOG.md` `[0.4.0]` and `[0.4.1]` | All applied by v0.4.1. |
| A22 | v0.5.2 walkthrough #1+#2 (meta + skill-evaluate) | `routing-eval.yaml` ships ~30 prompts covering only the 5 v0.4.x lifecycle skills + `none` cases; the 8 v0.5.0 skills + `meta` router have no held-out coverage | **Fixed in v0.5.2** — added 16 prompts covering library-bootstrap, library-audit, skill-evaluate, skill-migrate, skill-snapshot-diff, skill-policy-overlay, cross-domain-orchestrator-author, cross-library-orchestrator, meta. |
| A23 | v0.5.2 walkthrough #2 (skill-evaluate static heuristic) | Static keyword-overlap heuristic over-fires routers because router descriptions enumerate every atom name in the routing table. A prompt like "I want to write a new SKILL.md" matches the `meta` router as strongly as it matches `skill-author`. | **Fixed in v0.5.2** — `routing-eval-runner.py:static_routing()` de-ranks `archetype: router` skills by 0.7× so a tied router loses to a tied atom. |
| A24 | v0.5.2 walkthrough #1+#2 + audit ritual | The 5 original lifecycle skills (`skill-author`, `skill-audit`, `skill-refactor`, `skill-retire`, `family-bootstrap`) had `Do NOT use for` blocks that named only the original siblings, missing the v0.5.0-added skills. Predicted contention against library-bootstrap, skill-migrate, skill-policy-overlay, library-audit, etc. | **Fixed in v0.5.2** — anti-trigger blocks extended on all 5; per-skill PATCH bump (skill-author 0.1.5, skill-audit 0.2.2, skill-refactor 0.1.2, skill-retire 0.1.2, family-bootstrap 0.2.2). |
| A25 | (subsumed by A24) | Routing contention prediction for v0.5.0 skills against original 5 | Closed by A24 fix. |
| A26 | v0.5.2 walkthrough #4 (skill-migrate against synthesized v1→v2) | If `migration-guide-gen.py` produces an all-empty diff (Frontmatter / Capability / Routing / Section all empty), the original Stage 2 gate quietly proceeds to Stage 3 — author context is added onto an inert skeleton. The bump may not actually be MAJOR. | **Fixed in v0.5.2** — Stage 2 gate now halts on all-empty diff with explicit "this is not a MAJOR bump; re-check via detect-breaking-changes.py" message. skill-migrate v0.1.1. |
| A27 | v0.5.2 walkthrough #5 (library-audit) | Stage 4 snapshot integrity check reads "every `depends_on:` pin resolves to an existing skill at the pinned version" — ambiguous whether equality or floor. Confusing for any consumer authoring against this gate. | **Fixed in v0.5.2** — Stage 4 now defines pinned-version semantics: floor + same-MAJOR compatibility window; MINOR jumps are warnings, not fails. library-audit v0.1.1. |
| A28 | v0.5.2 walkthrough #5 | library-audit body cites `references/rollup-template.md` for the report format but the file did not ship in v0.5.0. | **Fixed in v0.5.2** — authored `references/rollup-template.md`. library-audit v0.1.1. |
| A29 | v0.5.2 walkthrough #5 | library-audit body cites `references/library-gates.md` for the L1-L4 library-shape gates (vs the per-skill 4 gates) but the file did not ship in v0.5.0. | **Fixed in v0.5.2** — authored `references/library-gates.md`. library-audit v0.1.1. |
| A30 | v0.5.2 walkthrough #6 (skill-policy-overlay against invented postgres family) | `house-postgres-conventions` overlay walked Stage 1-4 cleanly; no structural finding. Documentation reads correctly for the speculative case. | **No fix needed.** Documented as "speculative skill validates procedurally; first real consumer overlay will produce real findings." |
| A31 | v0.5.2 walkthrough #9 (library-bootstrap against invented new library) | `coverage-check.py` complains about empty libraries — the freshly-bootstrapped library has no skills yet, so coverage.md must accommodate "stub" content. The validator's schema check rejects valid stub forms. | **Fixed in v0.5.2** — `coverage-check.py` recognizes `("no skills yet", "n/a", "fresh library", "initial bootstrap")` markers and returns no findings for them. |
| A32 | v0.5.2 walkthrough #9 | library-bootstrap body cites `references/library-skeleton.md` for the new-library template tree (SNAPSHOT.lock / coverage.md / governance/INDEX.md / CHANGELOG.md / README.md / Makefile / verify.sh / requirements.txt / .gitignore / CONTRIBUTING.md / LICENSE / .github/workflows/verify.yml) but the file did not ship in v0.5.0. | **Fixed in v0.5.2** — authored `references/library-skeleton.md` with full templates. library-bootstrap v0.1.1. |
| A33 | v0.5.2 walkthrough #9 | library-bootstrap body cites `references/plugin-manifest.md` (plugin.json schema). | **Fixed in v0.5.2** — authored. library-bootstrap v0.1.1. |
| A34 | v0.5.2 walkthrough #9 | library-bootstrap body cites `references/marketplace-row.md` (Stage 5 marketplace.json edit pattern). | **Fixed in v0.5.2** — authored. library-bootstrap v0.1.1. |
| A35 | v0.6.0 dummy-archetype fixture | `validate-metadata.py:detect_archetype()` silently fell back to `atom` for unknown archetype values. The extension seam at `governance/EXTENSION-POINTS.md` §4 was *implicit*; the validator did not reject 6th-archetype attempts at the gate. | **Fixed in v0.6.0** — added `check_archetype_known()` finding that emits an explicit error naming the EXTENSION-POINTS.md §4 doc. |
| A36 | v0.6.0 dummy-health-gate seam test | 3 of 4 `gate_*` functions in `audit-skill.py` had no docstrings, violating the documented health-gate shape contract. | **Fixed in v0.6.0** — added docstrings to `gate_recency`, `gate_test_pass_rate`, `gate_triggering_accuracy`. |
| A37 | v0.6.0 retrospective | Audit-finding ledger discipline (this table) needed to migrate from CHANGELOG-only entries (A1-A21 in the v0.4.x release notes) to a single canonical table here. | **Fixed in v0.6.0** — ledger table introduced in v0.5.2 and grown in v0.6.0; CHANGELOG entries continue to point at this table. |
| A38 | v0.6.1 underutilized-features inventory | `metadata.recency_pin: stable` parsed in `audit-skill.py:154` but never declared on any of the 14 skills — write-only feature shipped at v0.1.0. | **Deferred to v0.6.2** — Phase 2 will roll out `recency_pin: stable` to the 5 lifecycle skills + add `check_recency_pin_value` validator. |
| A39 | v0.6.1 wiring inventory | 7 scripts (audit-skill, validate-metadata, detect-breaking-changes, migration-guide-gen, coverage-check, rollback-skill, taxonomy-coverage-sync) each independently re-implemented `parse_skill` / `split_h2_bodies` / `split_sections` / `detect_archetype`. Cumulative ~150 lines of duplicated logic. | **Fixed in v0.6.1** — `scripts/_skill_io.py` is the canonical home; all 7 scripts import. Thin call-shape wrappers preserve per-script APIs. |
| A40 | v0.6.1 wiring inventory | `depends_on:` pins in SNAPSHOT.lock could drift silently past the live skill version. No validator caught the case where a skill's pin was older than its current version. | **Fixed in v0.6.1** — `validate-metadata.py:check_depends_on_freshness` runs library-wide on `--all`. Same-MAJOR drift is warning; MAJOR boundary crossed is error. 3 fixture harnesses exercise pass / fail-stale-major / warn-stale-minor. |
| A41 | v0.6.1 underutilized-features inventory | `routing-eval.yaml` had uneven coverage — 9 skills under 3 positive prompts/skill. No automated enforcement threshold. | **Fixed in v0.6.1** — `gate_eval_coverage` (audit-skill.py) reports per-skill prompt count vs configurable threshold (default 3). routing-eval.yaml expanded from 46 to 55 prompts; every skill now has ≥3. |
| A42 | v0.6.1 underutilized-features inventory | `EvalEntry.rationale` (routing-eval-runner.py:71) was loaded from YAML but never rendered. | **Fixed in v0.6.1** — `--verbose` flag on routing-eval-runner.py renders rationale on misses. |
| A43 | v0.6.1 underutilized-features inventory | `SkillRollup.has_any_data` property (audit-skill.py:98) defined but never called. | **Fixed in v0.6.1** — removed (dead code cleanup). |
| A44 | v0.6.1 wiring inventory | `taxonomy-coverage-sync.py` existed in the tree but was not invoked by `verify.sh` or `Makefile`. | **Fixed in v0.6.1** — verify.sh step 10 runs against matching/divergent fixtures; `make taxonomy-sync` smoke target added. |
| A45 | v0.6.1 wiring inventory | `verify.sh` ran 9 independent checks with no synthesis step or unified headline. | **Fixed in v0.6.1** — final summary line consolidates pass/fail across all 10 steps. |
| A46 | v0.6.2 wiring inventory | Health-gate banners "suggested" by `audit-skill.py:render_banner` but never auto-applied. The operator had to hand-prepend each banner. Loop never closed. | **Fixed in v0.6.2** — `--apply-banners [--dry-run]` flag does the prepend via string-replace surgery (no PyYAML round-trip). Idempotent. Round-trip fixture exercises the full path: drift-failing skill → banner prepended → still parses → second apply is no-op. |
| A47 | v0.6.2 wiring inventory | Per-skill `metadata.changelog` blocks were never cross-referenced against library `CHANGELOG.md`. Drift accumulated silently when an operator forgot to add a CHANGELOG entry for a per-skill bump. | **Fixed in v0.6.2** — `scripts/changelog-sync.py` walks every skill's changelog and looks for the skill name in any library CHANGELOG block. verify.sh step 11. Live state passes (14/14). |
| A48 | v0.6.2 wiring inventory | SNAPSHOT.lock's 6-state `health` enum (`fresh|healthy|flagged|unhealthy|rolled-back|retired`) was write-only — all 14 skills perpetually `fresh` because nothing wrote back. | **Fixed in v0.6.2** — `audit-skill.py --write-health` updates SNAPSHOT.lock from gate results. Idempotent (run twice: second `git diff` empty). All 14 skills transitioned `fresh → healthy` on first run. `release-tag.sh Step 1.5` invokes it before tagging; refuses if any skill is `unhealthy` (unless `--allow-unhealthy`). |
| A49 | v0.6.2 underutilized-features inventory | `--mode external` and `--mode operator` on `routing-eval-runner.py` were unexercised in CI. External mode required stdin redirect (impractical for verify.sh); operator mode required interactive input. | **Fixed in v0.6.2** — `--input <path>` and `--operator-transcript <path>` flags. Two new fixtures (`routing-eval-external/responses.json`, `routing-eval-operator/transcript.txt`). verify.sh step 8 exercises both modes. |
| A50 | v0.7.0 ahead-of-trigger build | `governance/INTEGRATION-TESTING.md` shipped at v0.5.0 with explicit pre-trigger N/A. Trigger (10+ cross-dep skills + 2 regressions) had not fired by v0.7.0. | **Built ahead-of-trigger v0.7.0** by operator choice. `scripts/integration-test-runner.py` + 3 fixture scenarios + verify.sh step 14 + `make integration` target. Marked with pre-trigger comment; reassessment commitment in ARCHITECTURE.md §"v0.7.0 Ahead-of-Trigger Note". |
| A51 | v0.7.0 ahead-of-trigger build | `governance/SKILL-DISCOVERABILITY.md` shipped pre-trigger. Trigger (50+ skills) had not fired. | **Built ahead-of-trigger v0.7.0** — `scripts/search-skills.py` + `scripts/gen-index.py` + `INDEX.md` (generated artifact) + `metadata.tags` field + `validate-metadata.py:check_tags` + verify.sh step 13 + `make index` target. |
| A52 | v0.7.0 ahead-of-trigger build | `governance/SKILL-PROVENANCE.md` shipped pre-trigger. Trigger (external publishing) had not fired. | **Built ahead-of-trigger v0.7.0** — `scripts/snapshot-hash.py` + `--verify` mode + `release-tag.sh` Step 1.5 hash-verify + Step 6 signed tags (`git tag -as`) + `--allow-unsigned` for CI without GPG + verify.sh step 12. |
| A53 | v0.7.0 ahead-of-trigger build | `governance/DEPRECATION-COMMUNICATION.md` shipped pre-trigger. Trigger (external consumers) had not fired. | **Built ahead-of-trigger v0.7.0** — `scripts/notify-dependents.py` (emits per-channel JSON; does NOT send) + `governance/notification-channels.yaml` (declarative config; empty `channels: []`). |
| A54 | v0.7.0 ahead-of-trigger build | `governance/USAGE-ANALYTICS.md` shipped pre-trigger. Telemetry hook physically blocked on Claude Code core. | **Built partially v0.7.0** — `scripts/analytics-rollup.py` + synthetic JSONL fixture + verify.sh step 15. `scripts/telemetry-hook.py` ships as STUB documenting the schema; real load-time hook still blocked on Claude Code core. |
| A55 | v0.7.0 underutilized-features inventory | 7 skills had empty/zero `references/` directories at v0.6.x. Speculative skills had thin procedural depth. | **Fixed in v0.7.0** — 9 new reference docs across 7 skills (skill-evaluate, skill-policy-overlay, skill-migrate, skill-snapshot-diff, meta, cross-domain-orchestrator-author, cross-library-orchestrator). Each marked speculative; revise when skill becomes load-bearing. |
| A56 | v0.7.0 retrospective | The v0.1.0+ "do not build ahead of trigger" discipline was broken in v0.7.0 by operator choice. Future releases must not silently re-break it. | **Discipline-restoration commitment** documented in ARCHITECTURE.md §"v0.7.0 Ahead-of-Trigger Note": any future v0.7.x or v0.8.0 work that proposes building ahead-of-trigger items must include explicit operator approval matching v0.7.0's approach. |
| A57 | 2026-05-08 first real-consumer dogfood (context-site-build library-bootstrap Stage 7) | `validate-metadata.py --all` errored with exit 2 on the freshly-bootstrapped empty `skills/` directory. `coverage-check.py` was patched in v0.5.2 (A31) to recognize stub libraries; `validate-metadata.py` was the architectural mirror that was missed. Symmetric gap. | **Fixed in [Unreleased]** — added `--allow-empty` flag to `validate-metadata.py`. `verify.sh` template in `library-bootstrap/references/library-skeleton.md` should be updated to use it (this dogfood library uses the patched flag directly). Cross-referenced as B1 in context-site-build's ledger. **First real consumer dogfood finding** — closes part of P6 in `docs/PATH-TO-V1.md` (real consumer surfacing real meta-pipeline findings). |
| A58 | 2026-05-08 family-bootstrap Stage 1 intake (context-site-build) | Operator's initial mental model cut the site-build methodology into one family per phase (discovery / requirements / design / build / hardening / launch / postlaunch). Most individual phases have fewer than the 10 capabilities required by family-bootstrap Stage 2's gate (Phase 1 has ~7; Phase 6 has ~1). Mid-Stage-1 catch via the gate; restructured to one `site-build` family with phase-organized Tier 1/2/3 atoms. | **Disposition: informational, no patch.** The gate is correctly calibrated; the mental model was wrong. Adding a reference doc would help: `family-bootstrap/references/methodology-domains.md` documenting that methodology domains (where each capability is a heavyweight deliverable) typically fit best as one family with tier-stratified atoms across phases, not one family per phase. Cross-referenced as B2 in context-site-build's ledger. **Add the reference doc** as part of L7 backfill (deferred from this session). |
| A59 | 2026-05-08 family-bootstrap Stage 1 (context-site-build) | Stage 1 gate text reads "authority cites a URL AND a named author". Internal/private SOPs satisfy the gate's intent (no general-consensus sources, named author present) but lack a public URL. Operator worked around with `url: "internal://..."` plus a `path:` field; gate text and the domain-intake-checklist.md reference do not document this convention. | **Suggested patch (deferred to L7)**: extend `skills/family-bootstrap/references/domain-intake-checklist.md` to document the `internal://` URI scheme and the `path:` field. Update the gate prose in family-bootstrap SKILL.md to explicitly accept `internal://` URIs. Cross-referenced as B3 in context-site-build's ledger. |
| A60 | 2026-05-08 family-bootstrap Stage 6 advisory audit (context-site-build) | 4 of 7 freshly-authored atoms (vision-author, persona-author, adr-author, baseline-report-author) failed the description-drift gate on first audit (10.0% – 22.6% vs <10% threshold). Description vocabulary used "kickoff", "set", "who", "structured", "around", "writes" while bodies used different forms. **Reproduces** the v0.2.0 family-bootstrap dogfood observation ("8 of 9 freshly-bootstrapped skills failed the drift gate immediately"). | **No meta-pipeline patch needed.** The Stage 6 advisory audit correctly surfaced the drift; the iterate-until-clean loop in family-bootstrap Stage 6 is the right shape. The pattern is endemic to fresh authoring (description gets written first / abstractly; body uses concrete verbs). Added "Common drift signals on fresh atoms" subsection to `skill-author/references/audit-ritual.md` in [Unreleased]. Cross-referenced as B4 in context-site-build's ledger. **Validates v0.2.0's audit-at-Stage-6 design decision** — without it, this drift would have shipped to consumers. |
| A61 | 2026-05-08 L7 backfill authoring | While drafting reference docs to close A58/A59, operator added `references/<other>.md` chained cross-references between two refs in the same skill. `validate-metadata.py` rejected at next verify run: "references must not link to other references in the same skill (per METADATA-VALIDATION.md)". | **Validator working as designed.** Cross-references rewritten as prose mentions. **Useful real-consumer signal**: the rule's existence is correct (prevents reference-doc DAGs that become fragile under refactor) but the rule was previously discovered only by operators violating it. Suggested addition to `governance/METADATA-VALIDATION.md` — name this rule explicitly in the "validator catches" table so operators see it before they violate. **Deferred** to v0.7.1. Cross-referenced as B5 in context-site-build's ledger. |
| A62 | 2026-05-08 self-review of context-site-build v0.1.0 atoms | 5 of 6 newly-authored atoms had anti-triggers of the form `(use X-author when authored)` pointing at unbuilt skills. Pattern is routing-unactionable. Only `adr-author` had the correct pattern: `(use the user-invocable draft-X, or X-author when built)` — fall back to the user-invocable peer that exists in the operator's environment today. | **Suggested addition** (deferred to v0.7.1) to `skill-author/references/audit-ritual.md`: a sub-section "Anti-trigger fallback discipline" naming the pattern. When the anti-trigger references a skill that doesn't yet exist, name the user-invocable peer (or external system) as the fallback. Avoids unactionable routing dead-ends. Cross-referenced as B6 in context-site-build's ledger. |
| A63 | 2026-05-08 self-review | When an atom in family A references siblings in family B (where family B doesn't exist yet), the natural framing is "(deferred)" — but this conflates two cases: (1) deferred Tier 2/3 atom in *this* family, vs (2) atom in a *different* future family. The operator wrote (2) using the qualifier for (1), making out-of-scope siblings look in-scope. | **Suggested doc addition** (deferred to v0.7.1) to family-bootstrap's references: distinguish "in-family-deferred" (Specced, Not Yet Built) from "out-of-scope" (handled by a future-or-different family) explicitly in atom-authoring guidance. The Out-of-Scope rows in coverage.md are the canonical list; atoms should reference them by phrase like "handled by the future X family; user-invocable peer Y covers it now." Cross-referenced as B7 in context-site-build's ledger. |
| A64 | 2026-05-08 self-review | `site-build` router shipped with 10 of 16 Routing Table rows pointing at unbuilt deferred Tier 2/3 atoms. The router-atom-resolves validator check (added v0.4.0) treats this as a *warning, not an error*, on the grounds that "Tier 2/3 specced atoms are expected." But warnings are easy to ignore, and the operator authored the Routing Table with deferred entries by default (the family-bootstrap Stage 4 procedure does not say to omit them). | **Suggested addition** (deferred to v0.7.1) to `family-bootstrap` Stage 4 procedure: routers' Routing Tables list only built atoms. Specced atoms appear in `## Atoms in This Family` (where they get the Tier 2/3 header) and in `taxonomy.md`, but not in the Routing Table. Routing-eval contention drops materially when speculative rows are removed. Cross-referenced as B8 in context-site-build's ledger. |
