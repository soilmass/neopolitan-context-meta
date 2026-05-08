# Changelog

Cross-skill change log for the library. Every notable change to any skill produces an entry here. Skills do not maintain their own CHANGELOG.md files — this is the canonical source.

Format follows the conventions documented in `GOVERNANCE.md`. Categories: Breaking, Added, Changed, Deprecated, Removed, Health, Rolled back, Security.

---

## [Unreleased]

First real-consumer dogfood findings (A57-A60) and fixes. The
`context-site-build` library was scaffolded via `library-bootstrap`
+ `family-bootstrap` + `skill-author` × 7 on 2026-05-08, surfacing 4
findings across 3 lifecycle stages. P6 in `docs/PATH-TO-V1.md` moves
from "blocked on consumer library" to "consumer library exists; first
audit + refactor + retire pass pending."

### Added

- **`validate-metadata.py:--allow-empty`** — opt-in flag that returns
  exit 0 with a notice when `skills/` is empty under `--all`.
  Architectural mirror of the v0.5.2 A31 fix to `coverage-check.py`.
  Surfaced as A57. Existing CI behavior preserved (flag is opt-in);
  `library-skeleton.md` verify.sh template should be updated next
  time it's edited.

- **`skills/family-bootstrap/references/methodology-domains.md`** —
  new reference doc covering the methodology-domain case (heavyweight
  document deliverables, phase-organized capability count). Surfaced
  as A58 when the operator's initial mental model cut the site-build
  methodology into one family per phase, falling below Stage 2's
  ≥10-capability gate on most phases. Documents the
  one-family-with-phase-organized-tiers pattern.

### Changed

- **`skills/family-bootstrap/references/domain-intake-checklist.md`** —
  added "Authorities for internal SOPs" subsection documenting the
  `internal://` URI convention plus optional `path:` field for
  internal / private authorities. Surfaced as A59 when the site-build
  SOP (a private authored document) couldn't satisfy the literal URL
  requirement of the Stage 1 gate. Cross-references the new
  `methodology-domains.md` reference.

- **`skills/skill-author/references/audit-ritual.md`** — added
  "Common drift signals on fresh atoms" subsection. Surfaced as A60
  when 4 of 7 freshly-authored atoms in the context-site-build dogfood
  reproduced the v0.2.0 family-bootstrap drift-gate-failure pattern
  ("8 of 9 freshly-bootstrapped skills failed the drift gate
  immediately"). The new subsection enumerates common offenders
  (phase-name suffixes, temporal hedges, verb-form mismatches,
  abstract framing) and the fix discipline (tighten description, not
  body).

### Health

- All 14 skills remain `healthy` in SNAPSHOT.lock. No SKILL.md
  bodies / frontmatter changed in [Unreleased]; only references and
  one script. Per-skill version bumps deferred to v0.7.1 release.

### Notes

- A57-A60 are the first findings produced by an **external consumer
  library**, not in-memory dogfood. Per `docs/PATH-TO-V1.md` P6, this
  kind of finding is the load-bearing signal v1.0 has been waiting
  for.
- All 4 findings have suggested patches; A57 is shipped, A58/A59/A60
  shipped as reference doc updates. SKILL.md body / frontmatter
  changes deferred to v0.7.1 (the per-skill version bumps will mark
  family-bootstrap → 0.2.5, skill-author → 0.1.8 to claim the
  reference updates).
- v1.0 P6 status: **partial** — one consumer library exists with
  ≥3 atoms authored + audited. Refactor + retire still need real
  signal (premature on a freshly-bootstrapped family). Per A56's
  discipline-restoration commitment, manufactured refactor / retire
  exercises were declined.

---

## [0.7.0] - 2026-05-06

Phase 3 (final phase) of the v0.7.0 build-out pass. **MINOR bump** —
`metadata.tags` becomes documented optional field, four governance docs
flip Deferred → Built (ahead of trigger), six new scripts ship, INDEX.md
becomes a generated artifact, signed-tag enforcement available in
release-tag.sh.

### ⚠ Discipline-shift disclosure

This release contradicts the v0.1.0+ "do not build ahead of trigger"
discipline. The user has chosen this consciously. Each ahead-of-trigger
artifact is marked with a top-of-file comment:
`# pre-trigger build (v0.7.0); reassess when trigger fires per
governance/<doc>.md`. See `ARCHITECTURE.md` §"v0.7.0 Ahead-of-Trigger
Note" for the full disclosure and the discipline-restoration commitment
for v0.7.x onward.

The five pre-trigger pieces:
1. `scripts/integration-test-runner.py` (per `governance/INTEGRATION-TESTING.md`)
2. `scripts/search-skills.py` + `scripts/gen-index.py` + `INDEX.md`
   (per `governance/SKILL-DISCOVERABILITY.md`)
3. `scripts/snapshot-hash.py` + signed-tag enforcement
   (per `governance/SKILL-PROVENANCE.md`)
4. `scripts/notify-dependents.py` + `governance/notification-channels.yaml`
   (per `governance/DEPRECATION-COMMUNICATION.md`)
5. `scripts/analytics-rollup.py` + `scripts/telemetry-hook.py` (the latter
   is a STUB — real load-time hook blocked on Claude Code core; per
   `governance/USAGE-ANALYTICS.md`)

### Added — six new scripts (deferred infrastructure)

- **`scripts/integration-test-runner.py`** — loads YAML scenarios, executes
  existing scripts via subprocess, asserts exit codes / artifacts. Does NOT
  walk SKILL.md stages (M4 antipattern; reaffirmed). 3 fixture scenarios at
  `scripts/tests/fixtures/integration/`. verify.sh step 14.
- **`scripts/search-skills.py`** — token-overlap search over description +
  Capabilities Owned + tags. Reuses `_skill_io.tokens` (relocated from
  routing-eval-runner.py). Tag matches weighted 3.0×, description 1.0×,
  capabilities 0.5×.
- **`scripts/gen-index.py`** — generates `INDEX.md` listing every skill
  (name, archetype, version, tags, one-liner). `--check` mode for
  staleness detection. verify.sh step 13.
- **`scripts/snapshot-hash.py`** — SHA-256 per SKILL.md, written to
  SNAPSHOT.lock `sha256:` field. `--verify` mode recomputes + compares.
  Idempotent. First-run init populates fields; subsequent missing-field
  is an error. verify.sh step 12.
- **`scripts/notify-dependents.py`** — reads SNAPSHOT.lock + new
  `governance/notification-channels.yaml`. For `--skill <retired>`, emits
  per-channel JSON. Does NOT send (channel-wiring per consumer team).
- **`scripts/telemetry-hook.py`** — STUB. Documents JSONL event schema.
  Real load-time hook depends on Claude Code core support.
- **`scripts/analytics-rollup.py`** — consumes synthetic JSONL and produces
  per-skill activation count, co-invocation matrix, outcome distribution.
  Tested against `scripts/tests/analytics/synthetic-events.jsonl`.
  verify.sh step 15.

### Added — INDEX.md (generated artifact)

- **`INDEX.md`** — library-root living artifact. Regenerated via
  `make index` or as part of `release-tag.sh`. Per
  `governance/EXTENSION-POINTS.md` §5, INDEX.md is a stable schema:
  columns may evolve in MINOR bumps; existence + script-generated
  authoring is invariant.

### Added — `metadata.tags` optional frontmatter field

- All 14 SKILL.md files declare `metadata.tags:` (2-3 tags each from the
  canonical 8-tag taxonomy: `lifecycle | composition | health | provenance |
  router | discoverability | daily-use | weekly | rare`). Documented in
  `skills/skill-author/references/frontmatter-spec.md` §"metadata.tags".
- **`validate-metadata.py:check_tags`** — kebab-case validation; cap at 5
  tags per skill (warning); list-of-strings shape (error).

### Added — speculative-skill thickening (9 reference docs across 7 skills)

Each opens with `> Note: this reference is speculative (authored v0.7.0
ahead of skill-trigger). Revise when the skill becomes load-bearing in
a consuming library.`

- `skills/skill-evaluate/references/eval-suite-format.md`
- `skills/skill-evaluate/references/threshold-rationale.md`
- `skills/skill-policy-overlay/references/composition-rules.md`
- `skills/skill-policy-overlay/references/precedence-table.md`
- `skills/skill-migrate/references/migration-checklist.md`
- `skills/skill-snapshot-diff/references/diff-output-shape.md`
- `skills/meta/references/router-disambiguation.md`
- `skills/cross-domain-orchestrator-author/references/orchestration-patterns.md`
- `skills/cross-library-orchestrator/references/dependency-resolution.md`

### Added — 5 new verify.sh steps (12-15)

Step counts: v0.6.0 had 9 → v0.6.1 had 10 → v0.6.2 had 11 → v0.7.0 has **15**.
- 12: snapshot-hash --verify
- 13: gen-index --check
- 14: integration-test-runner.py against 3 fixture scenarios
- 15: analytics-rollup smoke against synthetic events

### Added — 5 new Makefile targets

`make index` / `make hashes` / `make integration` / `make notify-dependents-dry` /
`make analytics-rollup`.

### Changed — 4 governance docs flipped (Deferred → Built ahead of trigger)

- `governance/INTEGRATION-TESTING.md` — mechanizer built v0.7.0
- `governance/SKILL-DISCOVERABILITY.md` — mechanizer built v0.7.0
- `governance/SKILL-PROVENANCE.md` — mechanizer built v0.7.0
- `governance/DEPRECATION-COMMUNICATION.md` — mechanizer built v0.7.0
- `governance/USAGE-ANALYTICS.md` — rollup built; telemetry hook stubbed

### Changed — release-tag.sh extended

Step 1.5 (added v0.6.2) now also runs `snapshot-hash.py --verify` and
`gen-index.py --check`. Step 6 uses `git tag -as` (signed) by default;
`--allow-unsigned` flag bypasses GPG for CI environments.

### Changed — `_skill_io.tokens` (relocated from routing-eval-runner.py)

Tokenizer used by both `routing-eval-runner.py` (static mode) and the new
`search-skills.py`. Behavior unchanged; just lives in one place.

### Changed — ARCHITECTURE.md gains v0.7.0 ahead-of-trigger note

New §"v0.7.0 Ahead-of-Trigger Note" before §"Open Questions". Names the
five pre-trigger artifacts, the discipline shift, and the
discipline-restoration commitment for future releases.

### Health

- All 14 skills PATCH-bump for tags rollout. The 7 thickened skills' bumps
  also cover their new reference files.
  - `skill-author` 0.1.6 → 0.1.7 (tags)
  - `skill-audit` 0.2.3 → 0.2.4 (tags)
  - `skill-refactor` 0.1.3 → 0.1.4 (tags)
  - `skill-retire` 0.1.3 → 0.1.4 (tags)
  - `family-bootstrap` 0.2.3 → 0.2.4 (tags)
  - `library-audit` 0.1.1 → 0.1.2 (tags)
  - `library-bootstrap` 0.1.1 → 0.1.2 (tags)
  - `skill-evaluate` 0.1.0 → 0.1.1 (tags + 2 refs)
  - `skill-policy-overlay` 0.1.0 → 0.1.1 (tags + 2 refs)
  - `skill-migrate` 0.1.1 → 0.1.2 (tags + 1 ref)
  - `skill-snapshot-diff` 0.1.0 → 0.1.1 (tags + 1 ref)
  - `meta` 0.1.0 → 0.1.1 (tags + 1 ref)
  - `cross-domain-orchestrator-author` 0.1.0 → 0.1.1 (tags + 1 ref)
  - `cross-library-orchestrator` 0.1.0 → 0.1.1 (tags + 1 ref)
- All 14 skills health: `healthy` (transitioned in v0.6.2). All 14 hashes
  computed and stored in SNAPSHOT.lock.

### Notes

- v0.7.0 is feature-complete for skill-governance self-administration AND
  for the deferred-infrastructure surface area (with telemetry hook
  stubbed). Per `docs/PATH-TO-V1.md`, v1.0 still requires real consumer
  libraries to exercise the lifecycle.
- The discipline shift is OPERATOR-CHOSEN. Future releases that propose
  building further ahead-of-trigger items must include the same explicit
  approval step.

---

## [0.6.2] - 2026-05-06

Phase 2 of the v0.7.0 build-out pass. Compose what exists. Every audit
signal now flows into artifact mutation. Banners auto-apply. Per-skill
changelogs cross-referenced. SNAPSHOT.lock health writes back. release-tag.sh
runs audits before tagging. recency_pin gets first declarations.

### Added

- **`audit-skill.py:--apply-banners`** flag — prepends health banners to
  descriptions of failing skills via string-replace surgery (no PyYAML
  round-trip; preserves quoting + key order). `--dry-run` previews without
  writing. Idempotent (refuses if `BANNER_MARKER` is already present).
- **`audit-skill.py:--write-health`** flag — writes per-skill health states
  back to SNAPSHOT.lock per the 6-state enum (`fresh|healthy|flagged|
  unhealthy|rolled-back|retired`). Reads `git show HEAD~1:SNAPSHOT.lock`
  for "two-consecutive-flagged → unhealthy" transitions; gracefully degrades
  on shallow / non-git working trees. Idempotent on repeat invocation.
  All 14 skills transitioned `fresh` → `healthy` on first run.
- **`scripts/changelog-sync.py`** — cross-references each skill's
  `metadata.changelog` entries against library `CHANGELOG.md` per-version
  blocks. Reports drift when a skill has a changelog entry not mentioned
  in any library block. Skips `[Unreleased]`. New verify.sh step 11.
  New `make changelog-sync` target.
- **`routing-eval-runner.py:--input <path>`** — replaces stdin for
  `--mode external`, lets verify.sh exercise the production-mode code
  path without redirect tricks. Fixture at
  `scripts/tests/fixtures/routing-eval-external/responses.json`.
- **`routing-eval-runner.py:--operator-transcript <path>`** — replaces
  stdin for `--mode operator`. Replays pre-canned operator answers
  deterministically. Fixture at
  `scripts/tests/fixtures/routing-eval-operator/transcript.txt`.
- **`validate-metadata.py:check_recency_pin_value`** — warns on non-`stable`
  recency_pin values; errors on non-string values. Closes the v0.6.1
  finding A38 about the field being write-only.
- **`audit-banners` apply-roundtrip fixture** — exercises the full
  banner application: drift-failing skill → banner prepended → still
  parses cleanly → second apply is a no-op.

### Changed

- 5 lifecycle skills declare `metadata.recency_pin: stable` and PATCH-bump:
  - `skill-author@0.1.5 → 0.1.6`
  - `skill-audit@0.2.2 → 0.2.3`
  - `skill-refactor@0.1.2 → 0.1.3`
  - `skill-retire@0.1.2 → 0.1.3`
  - `family-bootstrap@0.2.2 → 0.2.3`
  audit-skill now reports `pinned stable` for these 5; the remaining 9
  skills continue probing `git log`.
- **SNAPSHOT.lock health states** transitioned from `fresh` (write-only)
  to `healthy` for all 14 skills via the first `--write-health` run.
  `fresh` is now reserved for genuinely-unaudited skills (newly-authored
  before first health check).
- **`release-tag.sh:Step 1.5`** (new) — runs `audit-skill --all
  --write-health` between Step 1 (verify.sh) and Step 2 (extract version).
  Refuses to tag if any skill is `unhealthy`. Print library-audit
  procedural checklist. `--allow-unhealthy` flag for emergency CI tagging.
- **`verify.sh`**: 10 → 11 steps. Step 11 is changelog-sync; step 8 (CLI
  exercise) extended with `--apply-banners --dry-run`,
  `--mode external --input`, `--mode operator --operator-transcript`.

### Removed

- (nothing removed; v0.6.2 is purely additive)

### Health

- All 14 skills pass implementable gates (recency + drift + eval_coverage).
  5 lifecycle skills now health: `healthy` with `recency_pin: stable`;
  9 newer skills health: `healthy` (recency probed via git log).

### Notes

- Pure compose-what-exists release. No pre-trigger discipline shift; every
  added capability is mechanizable today and consumes existing primitives.
- `--write-health` is idempotent: running it twice in a row produces no
  diff. Verified via the audit-banners fixture's md5sum comparison.
- Audit-finding ledger entries A38 (recency_pin write-only — closed),
  A41-A45 (closed in v0.6.1) and A46 (banner application gap — closed),
  A47 (changelog drift gap — closed), A48 (health state machine frozen — closed)
  added to `coverage.md`.

---

## [0.6.1] - 2026-05-06

Phase 1 of the v0.7.0 build-out pass. Code-quality cleanup + foundational
wiring. Zero parse-skill duplications across scripts. Every dataclass field
has a consumer. `depends_on:` pins can no longer drift silently. New
`gate_eval_coverage` health gate. `verify.sh` step 10 + unified summary.
No skill-body or governance-doc edits.

### Added

- **`scripts/_skill_io.py`** — internal shared utility module. Houses
  `parse_skill`, `parse_skill_text`, `split_h2_bodies`, `detect_archetype`,
  `iter_live_skills`, `load_snapshot`, `Finding`, `Report`, `SkillDoc`,
  `ARCHETYPES`. Replaces 7 independent in-script parser implementations.
  Internal-only (no CLI surface; not subject to validator interface contract).
- **`validate-metadata.py:check_depends_on_freshness`** — library-wide
  (`--all` only) check that `depends_on:` pins in SNAPSHOT.lock match
  current target versions. Floor + same-MAJOR semantics: same-MAJOR lag
  is a warning; MAJOR boundary crossed is an error. Closes A38 (write-only
  `depends_on:` discipline).
- **`audit-skill.py:gate_eval_coverage`** — Gate 5 (mechanizable today,
  no deferred infra). Threshold ≥3 positive prompts/skill in
  `routing-eval.yaml`. Reports `n/a` only when the suite file is missing.
  Each `gate_*` extension-seam contract satisfied.
- **routing-eval.yaml expansion** — 12 new prompts so every skill in
  SNAPSHOT.lock has ≥3 positive prompts (was 9 skills under-covered).
  Total: 55 prompts, 14 skills covered, every skill ≥3.
- **`routing-eval-runner.py:--verbose`** flag — renders `EvalEntry.rationale`
  on misses (text mode). Closes A39 (rationale loaded but never rendered).
- **`scripts/tests/fixtures/snapshot-pins/`** — 3 shell harnesses exercising
  `check_depends_on_freshness`: pass-current, fail-stale-major,
  warn-stale-minor.
- **`scripts/tests/fixtures/taxonomy-coverage/`** — 2 fixture pairs (matching
  + divergent) exercising `taxonomy-coverage-sync.py`.
- **verify.sh step 10** — Synthesis check (taxonomy-coverage-sync against
  the matching/divergent fixture pair, plus the snapshot-pin harnesses).
  verify.sh now runs 10 steps total. Final summary line consolidates pass/fail
  across all steps.
- **Makefile target `taxonomy-sync`** — smoke-tests
  `taxonomy-coverage-sync.py` against the matching fixture.

### Changed

- 7 scripts (`audit-skill.py`, `validate-metadata.py`,
  `detect-breaking-changes.py`, `migration-guide-gen.py`, `coverage-check.py`,
  `rollback-skill.py`, `taxonomy-coverage-sync.py`) now import shared parsers
  from `_skill_io`. Inline `parse_skill` / `split_h2_bodies` / `split_sections`
  / `detect_archetype` definitions removed. Thin call-shape wrappers preserve
  existing per-script APIs.
- `SkillRollup.has_any_data` removed from `audit-skill.py` (defined v0.5.0;
  never called by any consumer; cleanup).

### Health

- All 14 skills pass implementable gates (recency + drift + eval_coverage).
- Zero per-skill version bumps. Library-wide refactor; no SKILL.md content
  changes.

### Notes

- Pure code-quality release. No external contract changes for consumers.
- Discipline preserved: pre-trigger N/A items remain N/A (Gate 2 test-pass-rate,
  Gate 3 triggering-accuracy still report N/A; their build triggers have not
  fired). The new Gate 5 is implementable today and contributes real signal.
- Audit-finding ledger entries A38 (recency_pin write-only — deferred to v0.6.2),
  A39 (parser duplication closed), A40 (depends_on staleness closed) added to
  `coverage.md`.

---

## [0.6.0] - 2026-05-06

Phase 3 of the v0.6.0 testing + expansion pass. The 8 extension seams
discovered through Phases 1-2 are now consolidated into authoritative
docs. Extension-seam contract tests prove each seam holds. The path to
v1.0 is named with build triggers attached.

**Why MINOR.** Per `governance/VERSIONING-POLICY.md`, MINOR triggers
include "a new section is added to a skill's body" and "an optional
frontmatter field is added." The library-scope analog is "a new
governance doc is added" and "a new ARCHITECTURE.md section." The
v0.6.0 additions are functionality-adding without breaking dependents.

### Added — expansion docs

- **`governance/EXTENSION-POINTS.md`** — five sections naming the
  stable seams: (1) adding a new skill, (2) adding a new validator/
  script, (3) adding a new health gate, (4) adding a new archetype
  (explicitly OUT OF SCOPE at v0.6.0 — barred with a fail-as-expected
  fixture), (5) the six artifact contracts (`SNAPSHOT.lock`/
  `coverage.md`/`SKILL.md`/`MIGRATION-v<N>.md`/`routing-eval.yaml`/
  `CHANGELOG.md`) and their schema-stability promises.
- **`docs/PATH-TO-V1.md`** — names the seven prerequisites for v1.0,
  each with a build trigger, current state, blocking item, and exit
  criterion. Best case 6 months; worst case 18+ months.
- **`ARCHITECTURE.md` §"Extension Points"** — orientation pointer
  to EXTENSION-POINTS.md. Avoids duplication; ARCHITECTURE.md
  remains the orientation entry point.

### Added — extension-seam fixtures

- `scripts/tests/fixtures/extension-seams/dummy-archetype/SKILL.md` —
  fixture with `archetype: connector` (a hypothetical 6th archetype).
  validate-metadata.py is *expected to fail* with "Unknown archetype".
  If a future PR adds the connector archetype, the fixture flips to
  pass — making the seam test self-documenting.
- `scripts/tests/fixtures/extension-seams/dummy-validator-shape/dummy-validator.py`
  — 30-line stub matching the validator interface contract (argparse
  + exit codes 0/1/2 + Finding/Report dataclasses + JSON output).
  verify.sh step 9 ast-parses it.
- `scripts/tests/fixtures/extension-seams/dummy-health-gate/expected-shape.md`
  — documents the `gate_<name>()` contract: name pattern + return
  annotation `GateResult` + docstring required. verify.sh step 9
  ast-parses `audit-skill.py` and confirms every existing `gate_*`
  function follows it.

### Added — verify.sh step 9 + Makefile target + CI job

- `verify.sh` step 9 runs the three extension-seam contract checks.
  Library is now at 9 steps total.
- `Makefile` target `extension-check` runs only step 9 for fast
  iteration.
- `.github/workflows/verify.yml` gains a fourth job `extension-seams`
  that runs step 9 on every push and PR. CI now has 4 jobs total
  (verify / lint / extension-seams / detect-breaking-changes).

### Added — validate-metadata.py archetype rejection

`scripts/validate-metadata.py:check_archetype_known()` is a new check
that emits an explicit error when `archetype:` holds an unknown value.
Previously, an unknown archetype silently fell back to `atom`, which
was the original gap the dummy-archetype fixture surfaced. The error
now names governance/EXTENSION-POINTS.md §4 explicitly so the
authoring operator gets pointed at the right doc.

### Added — gate_* docstrings

`scripts/audit-skill.py:gate_recency()`, `gate_test_pass_rate()`, and
`gate_triggering_accuracy()` gained docstrings to satisfy the
extension-seam shape contract. The seam test caught their absence
during Phase 3 fixture authoring — a real finding from the seam test.

### Changed — governance/INDEX.md

The doc count moves from 10 → 11 with EXTENSION-POINTS.md added.
"Currently Documented" preamble updated.

### Health

All 14 skills pass implementable gates (recency + drift). Per-skill
versions unchanged from v0.5.2 — Phase 3 is library-scope work that
does not touch SKILL.md content.

### Notes

- v0.6.0 closes the validation surface and documents the growth path.
  The library is feature-complete for skill-governance self-administration.
- Per `docs/PATH-TO-V1.md`, the path to v1.0 requires real consumer
  libraries to exercise the lifecycle. The meta-pipeline cannot v1.0
  in isolation.

---

## [0.5.2] - 2026-05-06

Phase 2 of the v0.6.0 testing + expansion pass. Every v0.5.0 skill
walked end-to-end as in-memory dogfood. 13 audit findings (A22-A34)
captured in `coverage.md` ledger; 12 of 13 fixed in this release
(A30 was a no-fix-needed result). Six skills received PATCH bumps
with explicit changelog entries. Two cross-skill handoff fixtures
added.

### Added — walkthroughs

- `dogfood/WALKTHROUGH-meta-and-evaluate.md` — covers walkthrough #1
  (meta router) and #2 (skill-evaluate). Findings A22-A25.
- `dogfood/WALKTHROUGH-snapshot-diff.md` — walkthrough #3. No findings.
- `dogfood/WALKTHROUGH-skill-migrate.md` — walkthrough #4. Finding A26.
- `dogfood/WALKTHROUGH-library-audit.md` — walkthrough #5. Findings
  A27, A28, A29.
- `dogfood/WALKTHROUGH-skill-policy-overlay.md` — walkthrough #6.
  Finding A30 (no fix needed).
- `dogfood/WALKTHROUGH-7-9-orchestrators-and-bootstrap.md` —
  walkthroughs #7 (cross-domain-orchestrator-author),
  #8 (cross-library-orchestrator), #9 (library-bootstrap).
  Findings A31-A34.

### Added — cross-skill handoff fixtures

- **`scripts/tests/fixtures/handoffs/family-bootstrap-to-skill-author/`**
  — atom-count parity check between intake.yaml row count and
  per-atom skill-author invocations. Stage 4 of family-bootstrap is
  the most-load-bearing handoff in the library.
- **`scripts/tests/fixtures/handoffs/skill-refactor-to-skill-retire/`**
  — post-refactor sibling count parity. Catches the "we forgot to
  author the second sibling" failure mode of split refactors.

### Added — routing-eval coverage for v0.5.0 cluster

- 16 new prompts in `scripts/tests/routing-eval.yaml` covering
  library-bootstrap, library-audit, skill-evaluate, skill-migrate,
  skill-snapshot-diff, skill-policy-overlay,
  cross-domain-orchestrator-author, cross-library-orchestrator,
  and the meta router. Closes A22.

### Added — library-audit references

- `skills/library-audit/references/library-gates.md` — defines the
  L1-L4 library-shape gates. Closes A29.
- `skills/library-audit/references/rollup-template.md` — the
  `library-audit-report.md` template. Closes A28.

### Added — library-bootstrap references

- `skills/library-bootstrap/references/library-skeleton.md` — full
  templates for SNAPSHOT.lock, coverage.md, governance/INDEX.md,
  CHANGELOG.md, README.md, Makefile, verify.sh, requirements.txt,
  .gitignore, CONTRIBUTING.md, LICENSE, .github/workflows/verify.yml.
  Closes A32.
- `skills/library-bootstrap/references/plugin-manifest.md` — plugin.json
  schema reference. Closes A33.
- `skills/library-bootstrap/references/marketplace-row.md` — Stage 5
  marketplace.json edit pattern. Closes A34.

### Changed — anti-trigger updates on the 5 original lifecycle skills

The original 5 had `Do NOT use for` blocks naming only their original-
cohort siblings. The v0.5.0 cluster introduced predicted contention;
the static keyword-overlap heuristic confirmed it. Each received an
extended anti-trigger block plus a PATCH bump:

- `skill-author` 0.1.4 → 0.1.5 (names family-bootstrap, library-bootstrap,
  skill-refactor, skill-retire, skill-audit, skill-migrate, skill-policy-overlay).
- `skill-audit` 0.2.1 → 0.2.2 (names library-audit, skill-evaluate).
- `skill-refactor` 0.1.1 → 0.1.2 (names skill-migrate, library-bootstrap).
- `skill-retire` 0.1.1 → 0.1.2 (names library-bootstrap, rollback-skill.py).
- `family-bootstrap` 0.2.1 → 0.2.2 (names library-bootstrap,
  cross-domain-orchestrator-author, cross-library-orchestrator,
  skill-audit, library-audit).

Closes A24/A25.

### Changed — skill-migrate Stage 2 halt condition

`skill-migrate` 0.1.0 → 0.1.1: Stage 2 gate now halts on an all-empty
structural diff with explicit "this is not a MAJOR bump; re-check via
detect-breaking-changes.py" message. Closes A26.

### Changed — library-audit Stage 4 pinned-version semantics

`library-audit` 0.1.0 → 0.1.1: Stage 4 snapshot integrity check now
defines pinned-version semantics — `depends_on:` is a floor + same-MAJOR
compatibility window, not a strict equality. MINOR jumps are warnings,
not fails. Closes A27.

### Changed — library-bootstrap references shipped

`library-bootstrap` 0.1.0 → 0.1.1: SKILL.md body remains; three
referenced files now exist. Closes A32/A33/A34.

### Changed — coverage-check.py fresh-library marker

`scripts/coverage-check.py` recognizes the markers
`("no skills yet", "n/a", "fresh library", "initial bootstrap")` in
coverage.md bodies and returns no findings for them. Closes A31.

### Changed — routing-eval-runner.py de-ranks routers

`scripts/routing-eval-runner.py:static_routing()` multiplies router-
archetype scores by 0.7 so a tied router loses to a tied atom. Closes A23.

### Changed — verify.sh step 7 covers handoff fixtures

`verify.sh` step 7 grew a `7e` block exercising the two handoff
fixtures. Step count remains at 8.

### Health

All 14 skills pass implementable gates (recency + drift). The 6 skills
receiving PATCH bumps remain `health: fresh` in SNAPSHOT.lock.

### Notes

A30 produced no fix — the `skill-policy-overlay` walkthrough against an
invented `house-postgres-conventions` overlay walked cleanly.

---

## [0.5.1] - 2026-05-06

Phase 1 of the v0.6.0 testing + expansion pass. Closes the zero-fixture
gaps for the four load-bearing scripts, validates JSON output paths,
and exercises previously-untested CLI flags. Caught and fixed a real
bug in `rollback-skill.py`.

### Added — fixture coverage for previously-zero-fixture scripts

- **`scripts/tests/fixtures/baselines/`** — 5 archetype baselines
  (atom / tool / router / orchestrator / policy) shared across
  breaking-changes and migration pair tests, plus `BASELINES.md`
  documenting the directory's role.
- **`scripts/tests/fixtures/breaking-changes/`** — 8 pair fixtures
  covering all four detector passes and exit codes 0 / 1 / 2:
  no-change, capability-removed-no-bump, capability-removed-major-bumped,
  section-removed, description-30pct-rewrite, router-target-changed,
  router-entry-added, tool-allowed-tools-removed.
- **`scripts/tests/fixtures/migration/`** — 4 pair fixtures + 1
  malformed-yaml case. Each pair has an `expected-fragments.txt`
  for grep-based output validation (avoids golden-file brittleness).
- **`scripts/tests/fixtures/rollback/`** — 3 shell harnesses creating
  temp git repos and exercising rollback-skill.py: `pass-dry-run.sh`,
  `fail-version-not-in-history.sh`, `fail-snapshot-mismatch.sh`.
  Skip-with-warning if `git` not on PATH (mirrors ruff/mypy pattern).
- **`scripts/tests/fixtures/audit/`** — 4 shell harnesses for
  audit-skill: `pass-fresh-skill.sh`, `fail-stale-recency.sh`,
  `fail-description-drift.sh`, `fail-multi-gate.sh`.
- **6 adversarial input fixtures** under top-level `fixtures/`:
  `atom-fail-unicode-name.md` (regex fail),
  `atom-pass-yaml-anchor.md` (anchors are valid YAML),
  `atom-pass-boundary-description-1024.md` (exact boundary),
  `atom-fail-boundary-description-1025.md` (one over),
  `atom-fail-empty-frontmatter.md` and
  `atom-fail-missing-frontmatter.md` (both exit 2).

### Added — verify.sh steps 7 + 8

- **Step 7**: invokes script-script fixtures (breaking-changes pairs,
  migration pairs, rollback harnesses with skip-if-no-git, audit
  harnesses).
- **Step 8**: exercises CLI flag paths previously untested — JSON
  output for 6 scripts (validates against `python3 -m json.tool`),
  repeatable `--skill`, custom `--recency-months`, `--format dot`,
  `release-tag.sh --help`.

### Added — Makefile targets

- `make test-scripts` — runs verify.sh steps 7 + 8 only.
- `make smoke-bootstrap` — lints the smoke fixture's expected/
  tree against current SNAPSHOT.lock for staleness.

### Changed — verify.sh step 2 case statement

Extended to recognize three exit-2-expected fixture name patterns:
`*fail-empty-frontmatter*`, `*fail-missing-frontmatter*`,
`*fail-malformed*`. Previously all `*fail*` fixtures were expected
to exit 1; the new boundary-input fixtures correctly exit 2
(invocation failure) which is now handled.

### Fixed

- **`scripts/rollback-skill.py:find_ref_for_version()`** —
  surfaced by the rollback fixture during Phase 1.4: `git log` was
  invoked from `skill_dir` with a repo-root-relative path, which
  silently resolved to a nonexistent location. git returned no
  commits and the loop never matched any version, so every
  rollback failed with "target version not found in git history."
  Fix: run git from the repo root with the repo-relative path.
  Both `git log` and `git show` now resolve correctly.

### Verified

- `verify.sh` exit 0 with 8 steps now passing (was 6).
- 23 SKILL.md fixtures behave correctly (was 17).
- 8 breaking-changes pairs + 5 migration cases + 3 rollback
  harnesses + 4 audit harnesses all behave as documented.
- 6 JSON outputs all parse via `python3 -m json.tool`.
- ruff / mypy --strict / pyflakes still clean (10 source files).
- snapshot_version 0.5.0 → 0.5.1; per-skill versions unchanged
  (no SKILL.md content edits in this release).

---

## [0.5.0] - 2026-05-06

Kitchen-sink meta-tooling release. Per the user's planning choice,
v0.5.0 ships every meta-tooling concern that can be built without
external infrastructure — even those whose original "build trigger"
hasn't fired. The discipline of "don't build before trigger fires" is
explicitly suspended for this release, with the trade-off documented
in the plan file as a premature-abstraction risk to monitor against
the first real consumer dogfood.

### Added — lifecycle skills (8 atoms + 1 router)

- **`skill-snapshot-diff`** v0.1.0 (tool, 3 stages) — diffs two
  SNAPSHOT.lock states; produces release-note markdown. Wraps
  `scripts/snapshot-diff.py` with the release-note composition step.
- **`library-audit`** v0.1.0 (tool, 5 stages) — library-shape health
  check composing `audit-skill.py` (per-skill gates) +
  `coverage-check.py` (schema) + `verify.sh` (version triangulation)
  + snapshot integrity (depends_on resolution + cycle detection).
- **`skill-migrate`** v0.1.0 (tool, 4 stages) — authors
  MIGRATION-v\<N\>.md guides for MAJOR version bumps. Wraps
  `scripts/migration-guide-gen.py`.
- **`skill-evaluate`** v0.1.0 (tool, 5 stages) — runs held-out
  routing-eval prompts and reports triggering accuracy per skill
  (Health Gate 3 mechanizer). Wraps `scripts/routing-eval-runner.py`.
  Build trigger had not fired (library at 14 skills); ships ahead of
  trigger to claim surface area.
- **`skill-policy-overlay`** v0.1.0 (tool, 4 stages) — authors
  `house-<domain>-conventions` policy overlays. Build trigger had not
  fired (zero `house-*` skills exist); ships ahead of trigger.
- **`library-bootstrap`** v0.1.0 (orchestrator, 7 stages) — scaffolds
  a brand-new consuming library: plugin.json, SNAPSHOT.lock,
  coverage.md, governance/INDEX.md, README, scripts/, verify.sh,
  Makefile, CONTRIBUTING.md, LICENSE, .github/workflows. Build trigger
  had not fired (no second consumer library exists); ships ahead of
  trigger.
- **`cross-library-orchestrator`** v0.1.0 (orchestrator, 5 stages) —
  authors orchestrators that compose skills from two installed
  libraries. Build trigger had not fired; ships ahead of trigger.
- **`cross-domain-orchestrator-author`** v0.1.0 (tool, 5 stages) —
  authors orchestrators that span two families within one library.
  Build trigger had not fired (zero cross-domain orchestrators exist);
  ships ahead of trigger.
- **`meta`** v0.1.0 (router) — per-cluster router for the meta-pipeline
  lifecycle cluster. Bare-domain mental-model name (not `skill` —
  collides with `skill-*` prefix). Routes 13 atoms across per-skill
  / library / composition sub-clusters.

### Added — governance docs (7)

All seven moved from `governance/INDEX.md` Deferred → Currently
Documented. Each names its build trigger in the first paragraph and
disclaims pre-trigger applicability:

- **`governance/INTEGRATION-TESTING.md`** — Gate 2 (test pass rate)
  specification. Pre-trigger: 10+ skills with cross-deps + 2 cross-skill
  regressions.
- **`governance/SKILL-DISCOVERABILITY.md`** — tagging / search / index
  for discoverability beyond LLM matching. Pre-trigger: 50+ skills.
- **`governance/SKILL-PROVENANCE.md`** — GPG signing + per-skill SHA-256
  hashes for cross-trust-boundary distribution. Pre-trigger: skills
  distributed beyond original author's environment.
- **`governance/SECURITY-AUDIT.md`** — audit logs + forensics for skills
  touching sensitive operations. Pre-trigger: skills touch
  credentials / production / user-facing surfaces.
- **`governance/EMERGENCY-HOTFIX.md`** — placeholder skeleton for
  bypass procedures. To be rewritten against the first real incident.
- **`governance/DEPRECATION-COMMUNICATION.md`** — multi-channel
  deprecation notices (CHANGELOG + banner + dependent notification +
  sunset timeline). Pre-trigger: external consumers exist.
- **`governance/USAGE-ANALYTICS.md`** — privacy-preserving telemetry
  on activation / dead-code / co-invocation patterns. Pre-trigger:
  25+ skills.

### Added — scripts (7)

- **`scripts/coverage-check.py`** — validates coverage.md against the
  library schema or family schema (six required sections, non-empty
  Out of Scope, build-trigger column on Deferred). Wired into
  `verify.sh` step 5.
- **`scripts/snapshot-diff.py`** — diffs two SNAPSHOT.lock states;
  Added / Removed / Bumped / Health / Dependency categories. Wired
  into `verify.sh` step 6 (sanity).
- **`scripts/migration-guide-gen.py`** — auto-generates draft
  MIGRATION-v\<N\>.md from a structural diff between two SKILL.md
  versions. Per VERSIONING-POLICY.md §"Auto-generation".
- **`scripts/dependency-graph.py`** — text / DOT / JSON visualization
  of SNAPSHOT.lock depends_on edges; cycle detection.
- **`scripts/routing-eval-runner.py`** — runs the routing-eval suite
  in static / operator / external mode. Gate 3 mechanizer.
- **`scripts/taxonomy-coverage-sync.py`** — verifies a family's
  taxonomy.md ↔ coverage.md alignment (Tier 1/2/3 atom membership;
  tier mismatches flagged as drift).
- **`scripts/release-tag.sh`** — one-command release: refuses if
  verify.sh fails; reads snapshot_version; generates release notes via
  snapshot-diff.py against the previous tag; dry-run by default
  (--confirm to actually tag).

### Added — operational scaffolding

- **Smoke fixture** at `scripts/tests/smoke/bootstrap-git-family/`
  capturing the v0.4.0 dogfood input + expected output skeleton. Fixed
  input, fixed expected — does not regenerate from upstream Pro Git
  docs (per the v0.5.0 plan §Risks).
- **3 coverage fixtures** at `scripts/tests/fixtures/coverage/` (1
  pass + 2 fail) for `coverage-check.py`.
- **2 snapshot fixtures** at `scripts/tests/fixtures/snapshot/` for
  `snapshot-diff.py`.
- **CONTRIBUTING.md extension** — 30-minute onboarding ramp section
  for new contributors.
- **`coverage.md` Domains Out of Scope** — formal rejection record
  for `family-bootstrap.py` / `skill-author.py` runner pattern (item
  #22 from the original plan inventory; rejected because it would
  re-introduce the framework antipattern the architecture rejects).

### Changed — ARCHITECTURE.md

Three open questions resolved in new sections:

- **§"Library-Level Routing"** — distinguishes per-cluster routers
  (5+ atom threshold; the `meta` router shipped in v0.5.0) from
  cross-cluster meta-router (50+ skills threshold; deferred).
- **§"Cross-Domain Orchestrator Pattern"** — extracted pattern
  documentation; references `cross-domain-orchestrator-author` skill.
  Pattern *meta-extraction* (the hand-authored-N-times-then-extract
  step) remains deferred until 2-3 hand-authored examples exist.
- **§"Policy Overlay Composition"** — single-tier composition is
  shipped via `skill-policy-overlay`; multi-tier composition is
  documented but deferred.

§"Open Questions" reduced from 4 to 3 (cross-cluster meta-router,
eval-suite real routing layer, multi-tier policy composition — each
with reaffirmed triggers).

### Changed — Makefile / verify.sh / governance/INDEX.md / README.md

- Makefile gains targets: `coverage-check`, `snapshot-diff`,
  `dep-graph`, `routing-eval`, `release`, `smoke`.
- verify.sh extended from 4 steps to 6 (added coverage-check step 5
  and snapshot-diff sanity step 6). Fixture loop hardened to skip
  non-SKILL.md content (the new coverage/ and snapshot/ subdirs).
- governance/INDEX.md restructured: 3 load-bearing + 7 v0.5.0-authored
  in Currently Documented; 1 sole entry (plugin-publish.md) in
  Deferred; reading order updated.
- README.md Library Map updated to reflect 14 skills + 11 scripts +
  10 governance docs + new fixtures + new operational additions.

### Changed — per-skill versions

The 5 pre-existing lifecycle skills are NOT bumped in v0.5.0:
their descriptions still pass the drift gate (between 0.0% and 5.0%),
and the planned anti-trigger updates from family-bootstrap Stage 5's
audit ritual are explicitly **deferred to v0.5.1** as a focused
contention-audit patch. Reasoning: drift gate doesn't catch routing
contention; the new `meta` router's anti-triggers already absorb
most of the contention surface from the new siblings. Running the
full audit ritual across the 14-skill cluster is its own ~30-minute
discipline that benefits from being its own change set.

- `skill-author` stays at 0.1.4
- `family-bootstrap` stays at 0.2.1
- `skill-audit` stays at 0.2.1
- `skill-refactor` stays at 0.1.1
- `skill-retire` stays at 0.1.1

### Verified

- `verify.sh` exit 0 (six steps).
- `make verify` / `make lint` / `make typecheck` all clean.
- All 14 skills validate clean (atoms / tools / orchestrators / router
  archetype-required-sections all met).
- All 17 SKILL.md fixtures + 3 coverage fixtures + 2 snapshot fixtures
  behave correctly.
- `audit-skill.py --all` reports drift between 0.0% and 9.5% across
  the 14 skills (all under 10% threshold).
- `coverage-check.py --file coverage.md` exit 0 (library schema valid).
- `dependency-graph.py` shows the new cluster's depends_on edges:
  `library-audit` depends on `skill-audit`; `library-bootstrap`
  depends on `family-bootstrap` + `skill-author`; `skill-migrate`
  depends on `skill-author`; etc.
- mypy --strict zero issues across 11 scripts; ruff clean; pyflakes
  clean.

### Premature-abstraction risks

Per the v0.5.0 plan §Risks, several skills ship before their original
build triggers fired:

- `library-bootstrap` and `cross-library-orchestrator`: speculative
  abstraction. First real consumer dogfood will produce v0.5.x
  patches the same way v0.4.0's git-family dogfood produced v0.4.x.
- `skill-evaluate`: works in static / operator / external modes; real
  machine-graded results require a routing-layer that's partly
  outside this plugin's scope.
- `cross-domain-orchestrator-author`: per ARCHITECTURE.md, the
  meta-pattern itself only extracts after 2-3 hand-authored examples.
  v0.5.0 ships the *authoring tool*, not the *extracted pattern*.

These risks are accepted in exchange for surface-area completeness;
each skill ships with explicit "first dogfood will reveal procedural
gaps" disclaimers in its `metadata.changelog`.

---

## [0.4.1] - 2026-05-06

Applied the remaining 18 audit findings from the v0.4.0
family-bootstrap dogfood. All edits are clarifications, gate
extensions that align with already-declared specs, or
disambiguations — no new functionality, no breaking changes.

### Changed

- **`family-bootstrap` v0.2.0 → v0.2.1** *(PATCH)*
  - Stage 3 gate now enforces all-tier size caps (Tier 2: 4–7,
    Tier 3: 2–5). The caps were declared in `tier-model.md` from
    v0.1.0 but only Tier 1's 6–9 was checked at the gate. Audit
    findings A6/A7.
  - Stage 5 reworded: per-skill dependency declarations are flagged
    as rare for atoms (common only for orchestrators / tools and
    three-way refactor results), with the empty-set case declared
    normal. Audit finding A15.
  - Stage 5 cross-handoff gate adds a **strong-recommendation** that
    the family hand-off graph be connected (no isolated atoms),
    even though the gate itself only requires ≥1 sibling per atom.
    Audit finding A17.
  - Stage 5 routing gate now states explicitly that the operator
    cross-checks "every Tier 1 atom from `coverage.md` In Scope
    appears in the router's Routing Table" (the inverse direction
    of v0.4.0's `router-atom-resolves` validator check). Audit
    finding A14.
  - Stage 5 references `audit-ritual.md`'s "Note on the
    audit-report.md artifact" — the per-atom audit reports are
    ephemeral, not committed; the persistent outputs are
    description anti-trigger updates. Audit finding A18.
  - Stage 6 now says explicitly that "the new family lands in a
    *consuming library*", not the meta-pipeline itself. References
    to "the snapshot" / "coverage.md" / "CHANGELOG.md" in this
    stage refer to the consuming library's, not the meta-pipeline's.
    Audit finding A20.
- **`family-bootstrap/references/domain-intake-checklist.md`**
  Stage 1 gate now clarifies (a) "the snapshot" means the
  *consuming library's* `SNAPSHOT.lock` (audit A2) and (b) URL
  reachability is operator-confirmed in v0.x; an automated check
  would land if a `family-bootstrap` runner is built later
  (audit A1).
- **`family-bootstrap/references/tier-model.md`** gained an
  "Artifact conventions" section: citation specificity (A3),
  `capabilities.json` schema (A4), capability names vs SKILL.md
  names (A5/A8), `taxonomy.md` ↔ family `coverage.md` consistency
  policy (A9), capability-to-tier mapping convention for split
  capabilities (A8).
- **`skill-author` v0.1.3 → v0.1.4** *(PATCH)*
  - `references/naming.md` clarifies the regex applies to SKILL.md
    `name` only — not capability-name body bullets, not citation
    strings (audit A5/A8). Cross-references the new tier-model
    section.
  - `references/archetypes.md` gained an explicit "Source of truth"
    note: `governance/METADATA-VALIDATION.md` is canonical when
    the rubric and the validator disagree. The rubric is
    illustrative (audit A12).

### Verified

- `verify.sh` exit 0; `make verify` exit 0; ruff clean; mypy
  --strict zero issues; pyflakes clean.
- All 17 fixtures still behave correctly.
- `audit-skill.py --all` reports drift between 0.0% and 9.1% across
  the five lifecycle skills (all under 10% threshold).
- Reference line counts: `tier-model.md` grew from 117 to 221
  lines (well under the 300-line ToC threshold and the 1000-line
  cap). `naming.md` grew from 92 to 110 lines; `archetypes.md`
  grew from 142 to 153 lines. All references still well-bounded.

### Audit-finding ledger (final state from v0.4.0 dogfood)

All 21 findings now applied:

- v0.4.0: A11 (skill-author/family-bootstrap supersession),
  A19 (Stage 6 audit-skill sub-gate), A21 (validator
  router-atom-resolves check).
- v0.4.1: A1, A2, A3, A4, A5/A8, A6/A7, A9, A10, A12, A13†, A14,
  A15, A16†, A17, A18, A20.

† A10 and A13 were partially addressed in v0.4.0 (A10 by the
intake.yaml schema added to Stage 4) or are non-procedure issues
(A13 was about reference-file authoring effort during the
dogfood, not a procedure gap). A16 (manual cross-checks have no
script support) is captured in Stage 5 prose with the explicit
note that the orchestrator is procedural in v0.x; future
script-driven runner is deferred.

---

## [0.4.0] - 2026-05-06

Dogfood-driven release. Walked `family-bootstrap`'s 6 gated stages
end-to-end on the canonical `git` domain (in-memory, no committed
artifacts) — produced 8 Tier 1 atoms + 1 router that all pass
`validate-metadata.py`. Surfaced 21 audit findings; this release
applies the 3 highest-leverage real-procedure gaps.

### Changed

- **`family-bootstrap` v0.1.1 → v0.2.0** *(MINOR)*
  - Stage 6 gate is now a three-check sequence: structural validation,
    coverage discipline, **advisory health audit** via `audit-skill.py
    --all`. The dogfood found that 8 of 9 freshly-bootstrapped skills
    failed the drift gate immediately — without an audit at Stage 6,
    the operator finds out only on the next periodic skill-audit
    cycle, by which time the family has shipped to consumers
    (audit finding A19).
  - Stage 4 now spells out the `intake.yaml` schema the orchestrator
    pre-fills per atom (archetype, name, purpose, family, siblings).
    Previously implicit (audit finding A10).
  - Stage 4 now points operators to `skill-author` Stage 2's
    "When invoked from family-bootstrap" supersession note (audit
    finding A11).
- **`skill-author` v0.1.2 → v0.1.3** *(PATCH)*
  - Stage 2 (ecosystem audit) now documents the supersession when
    delegated from `family-bootstrap`: the family-level Stage 5
    audit ritual replaces per-atom Stage 2 audits. Standalone
    `skill-author` invocations still run Stage 2 fully (audit
    finding A11).

### Added

- **`scripts/validate-metadata.py` router-atom-resolves check** —
  for skills with archetype `router`, every `git-foo`-style entry in
  `## Atoms in This Family` is checked against `<plugin-root>/skills/`.
  Atoms that don't resolve produce a warning (not an error) — Tier 2/3
  specced/deferred atoms are expected to be unresolved per the
  family's `coverage.md`. Without this check, a router and its
  family can drift silently. Surfaced by the dogfood (audit
  finding A21). Smoke-tested against the dogfood `git` router:
  correctly warned about 9 unresolved Tier 2/3 entries.

### Verified

- `verify.sh` exit 0; ruff clean; mypy --strict zero issues; pyflakes
  clean. All 17 fixtures still behave as expected. All 5 lifecycle
  skills validate clean. Dogfood `git` router produces the
  expected single warning when validated against its own family
  root; no false positives on the meta-pipeline's own skills (which
  have no routers).
- `family-bootstrap` v0.2.0's three-check Stage 6 gate is now
  exercised in the procedure docs; the actual end-to-end test
  is the next time a real consumer bootstraps a family. The
  dogfood under `/tmp/dogfood-git/` was the first run.

---

## [0.3.0] - 2026-05-06

Deep audit + library hardening release. Found and fixed two real
correctness bugs in `validate-metadata.py`; added the operational
scaffolding the library was missing (LICENSE, requirements.txt,
.gitignore, Makefile, CONTRIBUTING.md, GitHub Actions CI).

### Fixed

- **`validate-metadata.py` SemVer regex now accepts SemVer 2.0** — the
  prior regex `^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$` rejected valid
  versions like `1.0.0-pre.1+meta` (combined pre-release + build
  metadata). New regex `^\d+\.\d+\.\d+(?:-[\w.-]+)?(?:\+[\w.-]+)?$`
  matches the canonical SemVer 2.0 grammar.
- **`validate-metadata.py` no longer crashes on numeric `name:`** —
  YAML can parse `name: 12345` as int; the duplicate-name warning's
  `name.lower()` call was unguarded and crashed with AttributeError.
  Added an `isinstance(name, str)` guard so non-string names produce
  a clean error finding instead.
- **`validate-metadata.py` ToC heuristic widened** — previously matched
  only `## table of contents` (H2). Now matches H1–H6 with
  "Table of Contents", "Contents", or "ToC" headings, aligning with
  the spec's "table of contents at the top" without specifying level.
- **`detect-breaking-changes.py`** — removed unused `tempfile` import
  (ruff F401).
- **All four scripts** — added missing generic type parameters
  (`dict[str, Any]`, `list[X]`); `mypy --strict` now reports zero
  errors across the four scripts.

### Added

- **`LICENSE`** at plugin root — Apache-2.0 full text. `plugin.json`
  has declared `Apache-2.0` since v0.1.0; the license text now ships
  with the plugin.
- **`requirements.txt`** — pins `PyYAML>=6.0,<7` (the only runtime
  dependency).
- **`.gitignore`** — Python build artifacts, virtualenvs, editor
  files, mypy/ruff caches.
- **`Makefile`** — convenience targets `make verify` / `validate` /
  `audit` / `lint` / `typecheck` / `install-deps` / `clean`. Wraps
  the existing scripts and `verify.sh`.
- **`CONTRIBUTING.md`** — entry-point doc for contributors. Maps each
  contribution shape to the lifecycle skill that handles it; states
  pre-flight checks; defers to existing docs for detail.
- **`.github/workflows/verify.yml`** — three CI jobs:
  1. `verify` (blocking): runs `verify.sh` on every push and PR.
  2. `lint` (informational): runs ruff + mypy --strict.
  3. `detect-breaking-changes` (PR-only): runs the detector against
     base branch for every modified SKILL.md.

### Changed

- **`skills/skill-retire/references/redirect-note-template.md`** —
  removed stale "v0.2.0 enhancement may add archived: true
  recognition" note. v0.2.0 shipped without the relaxed-rules path
  and the actual procedure works because the redirect block is
  *prepended* (not a replacement). Doc now states the current
  behavior honestly and names what would be required to add a
  relaxed-rules path later.
- **`SNAPSHOT.lock`** — `snapshot_version` bumped to `0.3.0`. No
  per-skill version changes — the bumps in this release are to
  the validator and to operational scaffolding, not to any single
  SKILL.md's content.

### Verified

11-category test sweep all green pre-fix; re-ran post-fix:
- `verify.sh` exit 0
- `validate-metadata.py --all` clean across 5 skills
- 17-fixture matrix (5 pass + 12 fail) behaves as expected
- `detect-breaking-changes.py` correct across all 5 archetypes
- `audit-skill.py` reports all 5 skills pass implementable gates
- New SemVer regex handles SemVer 2.0 cases that previously failed
- Numeric-name input no longer crashes; produces clean error finding
- ruff: clean
- mypy --strict: clean
- pyflakes: clean

Boundary tests (passes 1024-char description / fails 1025; passes
500-line body / fails 501; warns at 301-line ref / errors at
1001-line ref) all hold exactly.

Triple-consistency check confirmed: `governance/METADATA-VALIDATION.md`
section lists agree exactly with `validate-metadata.py` and
`detect-breaking-changes.py`. `recency_pin: stable` and `archived: true`
both work end-to-end as documented.

---

## [0.2.1] - 2026-05-06

Doc-completeness pass. Every doc claim that could be cross-checked
against the implementation was verified; stale claims found in the
v0.1.x → v0.2.0 transition are corrected.

### Changed

- **`README.md`** — Library Map updated to list `verify.sh`,
  `audit-skill.py`, `routing-eval.yaml`, and the reserved scaffold
  dirs (`agents/`, `commands/`, `hooks/`). Current State section
  upgraded from "three Python validators" to four scripts plus the
  one-command `verify.sh` runner; explicit fixture-matrix size
  (17 = 5 pass + 12 fail).
- **`MAINTENANCE.md`** — Gate 4 description no longer claims
  per-archetype structural matching; points at the asymmetric
  containment formula in `health-gates.md`. Auto-warn section softens
  "automatically prepended at load time" to current behavior (operator
  applies banner; load-time hook is a future enhancement). Cadence
  section labels each gate as implementable-now or
  deferred-with-pointer. "What This Doesn't Cover" pointer fix:
  routing-eval runner is deferred per `coverage.md` §`skill-evaluate`,
  not under the (incorrect) `SKILL-DISCOVERABILITY.md`.
- **`governance/METADATA-VALIDATION.md`** — Implementation Notes now
  document the four v0.2.0 hardening checks (reference chaining,
  name-version-segment heuristic, empty-section warning,
  duplicate-H2 warning).
- **`governance/INDEX.md`** — added "Adjacent Implementation"
  subsection naming `audit-skill.py` as the v0.2.0 mechanization of
  `MAINTENANCE.md` Gates 1 + 4.
- **`skill-audit` v0.2.0 → v0.2.1** — Stage 4b text reflects that
  `scripts/tests/routing-eval.yaml` ships in v0.2.0 as a starter set;
  what's deferred is the routing-layer runner, not the file. The
  audit-skill.py output already reported "suite present but runner
  deferred" — the SKILL.md now matches.
- **`SNAPSHOT.lock`** — `snapshot_version` bumped to `0.2.1`;
  `skill-audit` to v0.2.1.

### Health

- All 5 lifecycle skills pass `validate-metadata.py --all` (exit 0).
- All 17 test fixtures behave correctly (5 pass + 12 fail).
- `audit-skill.py --all` reports all 5 skills pass implementable
  gates (drift between 0.0% and 9.1%; recency 0.0 months ago).
- `verify.sh` exits 0 with version triangulation consistent.
- 11-category test sweep (verify.sh, validators, fixtures, exit-2
  paths, detector across all 5 archetypes including properly-handled
  exit 2, JSON outputs, rollback CLI, audit-skill CLI variants,
  routing-eval YAML structure, drift gate firing on synthetic skill)
  all green.

---

## [0.2.0] - 2026-05-06

Library hardening release. Validator gains four new checks; fixture
matrix triples; new automation script (`audit-skill.py`) mechanizes the
two implementable health gates; new top-level `verify.sh` runner; new
starter routing-eval suite. No breaking changes — all existing skills
continue to validate clean.

### Added

- **`scripts/audit-skill.py`** — mechanizes Gates 1 (recency via `git log`)
  and 4 (description drift) from `skill-audit/references/health-gates.md`.
  Gates 2 and 3 explicitly report N/A pending the deferred infrastructure
  named in `governance/INDEX.md` and library-root `coverage.md`. Output
  is per-skill rollup plus auto-generated banner blocks for any failing
  skill, in text or JSON.
- **`verify.sh`** at plugin root — one-command self-check that runs
  `validate-metadata.py --all`, exercises the fixture matrix, runs
  `audit-skill.py --all`, and prints version triangulation. Returns
  exit 0 on a clean library.
- **`scripts/tests/routing-eval.yaml`** — starter set of 31 prompts
  exercising the five lifecycle skills plus negative cases. The full
  routing-eval suite remains deferred per `coverage.md` build trigger;
  this starter exists so the format is locked, the file is in place,
  and `audit-skill.py` reports "eval suite present, runner deferred"
  rather than "no suite at all".
- **Validator hardening** — `scripts/validate-metadata.py` now catches
  four classes of error/warning that were previously silent:
  - Reference chaining (intra-skill `references/A.md` → `references/B.md`):
    error per METADATA-VALIDATION.md.
  - Name segments shaped like version literals (`pdf-v2`, `s3-1`):
    warning per `naming.md`.
  - Required-section title present but empty body: warning.
  - Duplicate H2 sections (same title appearing twice): warning.
- **Fixture matrix expansion** — added 10 new test fixtures, taking
  coverage from 7 to 17 (5 pass + 12 fail):
  - `policy-pass.md` (the missing 5th archetype)
  - `tool-fail-section.md`, `router-fail-section.md`,
    `orchestrator-fail-section.md`, `policy-fail-section.md` —
    section-removal failure paths for non-atom archetypes
  - `atom-fail-name-regex.md`, `atom-fail-long-description.md`,
    `atom-fail-body-cap.md` — universal-rule failures
  - `atom-fail-reference-chain/` and `atom-fail-reference-subdir/` —
    directory-shaped fixtures for the new reference-rule checks

### Changed

- **`skill-audit` v0.1.1 → v0.2.0** — Dependencies and Self-Audit
  sections now point at `scripts/audit-skill.py` (no longer "may add
  in v0.2.0"). The Gate 4 drift formula in `references/health-gates.md`
  was corrected from Jaccard distance (always too eager) to asymmetric
  containment with prefix-based token matching. The earlier formula
  is acknowledged in the doc as superseded.
- **`governance/BREAKING-CHANGE-DETECTION.md` §"Section removal"** —
  rewrote partial enumeration as illustrative-not-exhaustive, with an
  explicit pointer to `METADATA-VALIDATION.md` as the source of truth
  for required-sections lists. Both validators consume that single
  table; the doc now matches the implementation.
- **`family-bootstrap/references/tier-model.md`** — example output
  template now includes `## Tier rationale` matching `taxonomy-template.md`,
  with a note that the template is the source of truth on layout.
- **`coverage.md`** — clarified `skill-evaluate` deferred-row build
  trigger language: distinguished "becomes load-bearing at 50+" from
  "first builds at 25 OR first regression". The two thresholds come
  from different paragraphs of `ARCHITECTURE.md` §"Routing and
  Contention"; the row now points at both.
- **`SNAPSHOT.lock`** — `snapshot_version` bumped to `0.2.0`;
  `skill-audit` to v0.2.0; `depends_on:` pins propagated.

### Health

- All 5 lifecycle skills pass `validate-metadata.py --all` (exit 0).
- All 17 test fixtures behave as expected (5 pass + 12 fail with
  correct error categories).
- `audit-skill.py --all` reports all 5 skills pass implementable
  gates (drift between 0.0% and 9.1%; recency 0.0 months ago).
- `verify.sh` exits 0 with version triangulation consistent.

---

## [0.1.2] - 2026-05-06

Second-pass cross-doc consistency improvements following the v0.1.1
audit. No skill capabilities added or removed; all changes resolve
cross-doc terminology drift or fill in orchestration cases that were
previously implicit.

### Changed

- **`GOVERNANCE.md` §"Dependency Model" + §"Cross-References Between Skills"** —
  unified lockfile terminology. The library has one canonical
  dependency mechanism: `SNAPSHOT.lock` `depends_on:` entries per
  skill. A separate per-skill `lockfile.yaml` or `metadata.lockfile`
  field is named explicitly as a deferred concern, not a current
  feature.
- **`skill-author` v0.1.1 → v0.1.2** — Stage 4 now documents a third
  coverage-update branch: when invoked by `family-bootstrap` Stage 4
  during initial bootstrap of a brand-new family, the per-atom
  coverage update is deferred to the orchestrator's Stage 6 (which
  writes the family `coverage.md` fresh from the woven Stage 5 state).
  Previously Stage 4 had only two branches and the orchestration was
  implicit.
- **`family-bootstrap` v0.1.0 → v0.1.1** — Stage 5 now specifies what
  "audit ritual run across the whole family at once" means concretely:
  N invocations of the per-skill ritual (once per Tier 1 atom, plus
  once for the router) with sibling pool spanning the family, and
  anti-trigger updates batched at end-of-stage. Per-atom dependency
  declarations clarified to reference `SNAPSHOT.lock depends_on:`.
- **`skill-retire` v0.1.0 → v0.1.1** — Stage 2 dependent check
  references the implemented `SNAPSHOT.lock depends_on:` mechanism
  rather than the speculative `metadata.lockfile` field.
- **`skill-refactor` v0.1.0 → v0.1.1** — Stage 2 affected-dependents
  enumeration references `SNAPSHOT.lock depends_on:` rather than
  generic "every lockfile that pins it".
- **`SNAPSHOT.lock`** — `snapshot_version` bumped to `0.1.2`.
  `skill-author` to v0.1.2; `family-bootstrap`, `skill-refactor`,
  `skill-retire` to v0.1.1; `depends_on:` pins updated to track.

### Health

- All five lifecycle skills still pass `validate-metadata.py --all`
  (exit 0). All seven test fixtures still produce expected outcomes.

---

## [0.1.1] - 2026-05-06

Cross-doc consistency pass following an end-to-end audit of the
v0.1.0 release. No skill capabilities were added or removed; all
changes are clarifications, doc fixes, or scaffolding.

### Changed

- **`governance/BREAKING-CHANGE-DETECTION.md` §"Section removal"** —
  router required-section list said `Anti-Triggers` (no such section
  exists; anti-triggers live in the frontmatter `description`).
  Replaced with `Disambiguation Protocol` and added a clarifying
  parenthetical pointing back to the description-level handling.
- **`skill-audit` v0.1.0 → v0.1.1** — Stage 4 renamed to
  "Test-pass-rate & triggering-accuracy probes" so the frontmatter
  description and stage body agree on which gates the stage covers.
  Drift gate (Gate 4) formula pinned in
  `references/health-gates.md` (Jaccard distance with explicit
  set-extraction rules per archetype).
- **`skill-author` v0.1.0 → v0.1.1** — `references/frontmatter-spec.md`
  now documents `metadata.recency_pin: stable` as an optional field
  (already in active use by `skill-audit` Stage 2 but previously
  undocumented). `references/audit-ritual.md` gained a top-of-file
  note clarifying that the `audit-report.md` artifact is ephemeral
  (a planning document, not a committed file).
- **`SNAPSHOT.lock`** — bumped `snapshot_version` to `0.1.1`. Updated
  `skill-author` and `skill-audit` entries to v0.1.1; `depends_on`
  pins in `family-bootstrap` and `skill-refactor` updated to track
  the new `skill-author@0.1.1`.
- **Plugin scaffold** — `agents/`, `commands/`, and `hooks/` now hold
  `.gitkeep` files with one-line "intentionally empty" notes so the
  Claude Code plugin scaffold is self-explanatory.

### Health

- Audit verified all five lifecycle skills pass `validate-metadata.py
  --all` (exit 0). Test fixtures still behave as designed (3 fail with
  the right errors, 4 pass).

---

## [0.1.0] - 2026-05-06

### Added

- **Plugin scaffolding** — converted `library-template/` into a Claude Code plugin (`context-meta-pipeline`) under a new marketplace (`neopolitan-context-meta`).
- **`skill-author` v0.1.0** — Tool. Authors a single SKILL.md (atom, tool, router, or policy overlay) through 4 gated stages: intake, ecosystem audit, drafting, validation & registration. Replaces the conceptual `building-skills` from earlier drafts of the architecture.
- **`family-bootstrap` v0.1.0** — Orchestrator. Creates a complete domain family (router + Tier 1 atoms + per-family `coverage.md`) through 6 gated stages: domain intake, capability indexing, taxonomy design, per-skill authoring, weaving, coverage & registration. Delegates to `skill-author` for each Tier 1 atom. Replaces the conceptual `docs-to-skill-family`.
- **`skill-audit` v0.1.0** — Tool. Runs the four health-gates from `MAINTENANCE.md` (recency, test pass rate, triggering accuracy, description drift) through 5 gated stages.
- **`skill-refactor` v0.1.0** — Tool. Performs split / merge / move / three-way refactor (per `ARCHITECTURE.md` §"Mechanism vs Policy") through 5 gated stages. Delegates to `skill-author` and `skill-retire`.
- **`skill-retire` v0.1.0** — Tool. Archives a skill with redirect note through 4 gated stages. The SKILL.md remains in git history and remains pinnable.
- **`scripts/validate-metadata.py`** — implements `governance/METADATA-VALIDATION.md` (universal + archetype-specific section checks, frontmatter schema, naming, references). PyYAML + stdlib only.
- **`scripts/detect-breaking-changes.py`** — implements `governance/BREAKING-CHANGE-DETECTION.md` (frontmatter / section / capability / routing diffs, dependent lookup via `SNAPSHOT.lock`).
- **`scripts/rollback-skill.py`** — implements Level 1 rollback from `governance/ROLLBACK-PROCEDURE.md`. Levels 2-3 remain procedural.
- **Governance docs ship inside the plugin** — `ARCHITECTURE.md`, `GOVERNANCE.md`, `VERSIONING-POLICY.md`, `MAINTENANCE.md` at plugin root; `governance/INDEX.md`, `governance/METADATA-VALIDATION.md`, `governance/BREAKING-CHANGE-DETECTION.md`, `governance/ROLLBACK-PROCEDURE.md` under `governance/`.
- **`SNAPSHOT.lock`** — initial library snapshot listing the five lifecycle skills at v0.1.0.
- **`coverage.md`** at library root — one domain claimed (skill lifecycle), four deferred entries with build triggers, five out-of-scope entries.

### Changed

- **`ARCHITECTURE.md` §"The Production Pipeline"** — full rewrite. Replaced the three-skill model (`building-skills` + `docs-to-skill-family` + future `library-architect`) with the five-skill lifecycle model. The `library-architect` deferred concern is now resolved through `skill-refactor` plus `family-bootstrap`'s coverage step. Section retitled to "The Lifecycle Pipeline".
- **`README.md` §"Adding to the Library"** — full rewrite. Names the five lifecycle skills explicitly with one-sentence usage and stage counts.
- **`README.md` §"Library Map"** — updated to reflect actual layout (skills under `skills/`, scripts under `scripts/`, plugin manifest under `.claude-plugin/`).
- **`GOVERNANCE.md` §"Adding a New Skill"** — `skill-author` Stage 4 is now the canonical pre-merge checklist; procedural fallback retained for cases where the lifecycle skills are unavailable.
- **`VERSIONING-POLICY.md`** — example pin `docs-to-skill-family@2.0.0` → `family-bootstrap@2.0.0`.
- **`governance/METADATA-VALIDATION.md`, `governance/BREAKING-CHANGE-DETECTION.md`, `governance/ROLLBACK-PROCEDURE.md`** — implementation notes updated from `.sh` to `.py`; status changed from "should be authored when the library reaches the size where this matters" to "Implemented in v0.1.0".
- **`governance/INDEX.md`** — added pointers from each documented procedure to its Python implementation under `/scripts/`.

---

## How to Add Entries

For every PR that ships a notable change:

1. Identify the category (Breaking, Added, Changed, Deprecated, Removed, Health, Rolled back, Security).
2. Add an entry under the current date heading, creating the heading if it does not yet exist.
3. Name the skill, the version transition, and the impact.
4. Link to the migration guide if the change is breaking.
5. Name affected dependents (typically routers) so downstream maintainers see the impact.

### Example entries

```markdown
## 2026-05-06

### Breaking
- `git-history-rewriting` v2.0 — `revert` moved to `git-recovery`
  - Affects: `git` router (anti-trigger updated, routing table updated)
  - Migration guide: /git-history-rewriting/MIGRATION-v2.md

### Added
- `git-hooks` v1.0 — split from `git-config`

### Health
- `building-website-specs` flagged unhealthy (test pass rate 78%, threshold 90%)

### Rolled back
- `git-history-rewriting` v1.5.0 → v1.4.2 (regression in multi-parent merges)
```

The `[Unreleased]` section accumulates entries between releases. When a coordinated release ships, the section is renamed with the date and a new `[Unreleased]` is created.
