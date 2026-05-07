# EXTENSION-POINTS.md

The library has stable seams. New skills, new validators, new health
gates, and new archetypes go *through* these seams without architectural
changes. The seams exist whether they're documented or not — this doc
makes them explicit so consumers and contributors can extend the library
without re-discovering them.

**Audience.** Library contributors and operators authoring new
validators, health gates, or archetypes against the meta-pipeline.

**Cross-references.**
- `ARCHITECTURE.md` §"Extension Points" — orientation pointer to this
  doc.
- `governance/INDEX.md` — names this doc among load-bearing governance.
- `docs/PATH-TO-V1.md` — names which seams become immutable at v1.0.

---

## 1. Adding a new skill

The single most-traveled extension. Five steps as documented in
`GOVERNANCE.md` §"Adding a New Skill"; this section names the seam,
not the procedure.

**Seam:** `skills/<name>/SKILL.md` + entry in `SNAPSHOT.lock` +
row in the relevant `coverage.md`.

**Canonical procedure:** `skill-author` Stages 1-4 (intake → audit →
draft → validate). For whole-family scaffolding: `family-bootstrap`
delegates to `skill-author` per atom. For whole-library scaffolding:
`library-bootstrap` delegates to `family-bootstrap` per family.

**Stable invariants** (do not break these without a MAJOR bump on the
library):
- Naming: `^[a-z][a-z0-9-]{2,63}$`, ≤4 segments, kebab-case.
- Required frontmatter keys: `name`, `description` (≤1024 chars,
  third-person, includes `Do NOT use for`), `license`,
  `metadata.version`, `metadata.archetype`, `metadata.changelog`.
- Body ≤500 lines; detail in references.
- One H1 matching the `name`.
- Archetype-specific required sections per
  `governance/METADATA-VALIDATION.md`.

**Validation:** `python3 scripts/validate-metadata.py --skill
skills/<name>/SKILL.md` exits 0.

**What this seam does NOT extend:** authoring a new *archetype* (see §4
below — explicitly out of scope at v0.6.0).

---

## 2. Adding a new validator / script

The Python validators under `scripts/` are independently composable.
Each is a single-purpose CLI that reads SKILL.md / coverage.md /
SNAPSHOT.lock files and emits findings.

**Seam:** `scripts/<name>.py` matching the validator interface
contract.

**Validator interface contract** (the shape every script in
`scripts/*.py` follows):

| Surface | Convention |
|---------|------------|
| Argparse signature | `--all`, `--skill <path>` (repeatable), `--format text\|json`, plus script-specific flags |
| Exit codes | `0` clean / `1` findings present / `2` invocation problem (no input, malformed, missing dependency) |
| Findings shape | `Finding(severity, message)` dataclass — see `validate-metadata.py:91-129` for the canonical shape |
| Report shape | `Report` dataclass with `findings: list[Finding]` and `to_text()` / `to_json()` methods |
| Stdout | text or JSON depending on `--format`; **never** mix both |
| Stderr | only for invocation errors (exit 2) and progress when `--verbose` is passed |
| PyYAML | only third-party dependency; see `requirements.txt` |
| Type hints | `mypy --strict` clean |

**Five steps to add one:**
1. Author `scripts/<name>.py` matching the contract above.
2. Add a `Makefile` target (`make <name>`) that runs it.
3. Add a `verify.sh` step that exercises it against fixtures and
   asserts an expected exit code.
4. Add fixtures under `scripts/tests/fixtures/<name>/` — at least
   one pass and two fails covering exit codes 1 and 2.
5. Register the script in `governance/INDEX.md` (under the load-bearing
   list if it's hard-required; under the operator-tooling list
   otherwise).

**What this seam does NOT extend:** running a script as part of CI for
mandatory pre-merge enforcement. That's a separate decision per
`governance/INDEX.md` and may require lifting the script from
"informational" to "load-bearing." Done explicitly, not by accident.

---

## 3. Adding a new health gate

The four gates from `governance/MAINTENANCE.md` (recency / test pass
rate / triggering accuracy / description drift) are the canonical health
surface. New gates extend `audit-skill.py`.

**Seam:** a new `gate_<name>()` function in `scripts/audit-skill.py`
plus a threshold in `governance/MAINTENANCE.md` plus mechanizer link in
`skills/skill-audit/references/health-gates.md`.

**Gate signature contract:**

```python
def gate_<name>(skill_dir: Path, *, threshold: float | int | None = None) -> GateResult:
    """One-line description of what this gate checks.

    Returns GateResult(name="<name>", passed=bool, value=<observable>,
                       threshold=<threshold>, reason=<short>)
    """
```

The `GateResult` dataclass already exists in `audit-skill.py`. New gates
add a single `gate_<name>` function and wire it into the gate-runner
loop.

**Five steps to add one:**
1. Author `gate_<name>()` in `audit-skill.py` matching the signature.
2. Document the threshold in `governance/MAINTENANCE.md`.
3. Add a "what this gate observes" subsection in
   `skills/skill-audit/references/health-gates.md`.
4. Add a fixture under `scripts/tests/fixtures/audit/` exercising the
   gate's pass and fail paths.
5. Bump `skill-audit`'s version (MINOR — adding a gate is a new
   capability) with a changelog entry.

**Implementable vs deferred.** Gates 2 and 3 currently report explicit
N/A pending build triggers (`INTEGRATION-TESTING.md` for Gate 2;
`skill-evaluate` build trigger for Gate 3). New gates SHOULD be
implementable at the time they ship — deferred gates get added to
`coverage.md` Deferred row instead of `audit-skill.py`.

---

## 4. Adding a new archetype — **OUT OF SCOPE AT v0.6.0**

The five archetypes (atom / tool / router / orchestrator / policy) are
the load-bearing categorization of every skill. Adding a sixth would
touch `ARCHITECTURE.md`, every validator's archetype-aware logic, the
audit ritual, the routing-eval suite, and the shape of every existing
SKILL.md.

**This is a MAJOR refactor and is explicitly not a documented extension
seam at v0.6.0.**

The seam *exists* — it's the archetype table in
`governance/METADATA-VALIDATION.md` and the `archetype: ` enumeration
in every validator. But authoring a sixth archetype requires:

- Restructuring `ARCHITECTURE.md` §"The Five Archetypes" → "The N
  Archetypes."
- Adding archetype-specific required-section rules in three places
  (`validate-metadata.py`, `detect-breaking-changes.py`,
  `migration-guide-gen.py`) and keeping them triple-consistent.
- Authoring a new "audit ritual" rule for how the new archetype's
  description should anti-trigger against existing archetypes.
- Updating the routing-eval suite to cover the new archetype's
  expected fire patterns.
- A library MAJOR bump with a `MIGRATION-v<N>.md` authored via
  `skill-migrate`.

The explicit barrier is intentional. If a future PR proposes a 6th
archetype, the proposer reads this section first and authors the MAJOR
bump consciously. The extension-seam fixture
(`scripts/tests/fixtures/extension-seams/dummy-archetype/`) is designed
to *fail-as-expected* — it tries to validate a SKILL.md with
`archetype: connector` and the validator must reject it. If a future PR
adds the archetype, the fixture flips to pass, and that's the signal
that the MAJOR refactor has been done.

---

## 5. Stable interfaces — the six artifacts

These are the file-format contracts the library promises to consumers.
Schema changes are MAJOR-bump library changes; field additions are
MINOR; field clarifications are PATCH.

| Artifact | Schema-stability promise |
|----------|-------------------------|
| `SNAPSHOT.lock` | Top-level keys (`snapshot_version`, `generated`, `plugin`, `skills`) and per-skill keys (`version`, `archetype`, `path`, `health`, optional `depends_on`) are stable. New optional keys are MINOR. Removing or renaming any existing key is MAJOR. |
| `coverage.md` | Required H2 sections (`## In Scope (Tier 1)`, `## Specced, Not Yet Built`, `## Deferred`, `## Out of Scope`) are stable. The schema-check in `coverage-check.py` enforces them. New optional sections are MINOR. |
| `SKILL.md` | Frontmatter keys + body required-sections-by-archetype as documented in `governance/METADATA-VALIDATION.md`. Naming regex is stable. New optional frontmatter keys are MINOR. |
| `MIGRATION-v<N>.md` | Generated by `migration-guide-gen.py` with four sections (Frontmatter / Capability / Routing / Section changes) plus author context. Section names stable. |
| `routing-eval.yaml` | Top-level `version`, `generated`, `prompts:` list. Per-prompt fields `prompt`, `expected`, `source`, `rationale` stable. |
| `CHANGELOG.md` | Per-release block: `## [<version>] - <YYYY-MM-DD>` heading + categorized `### <Category>` H3s using the `GOVERNANCE.md` category set. |

**v0.6.0 lock-in status.** The six artifacts have been stable since
v0.3.0 (when boundary-condition sweep + triple-consistency checks
landed). They are *de facto* immutable. Per `docs/PATH-TO-V1.md`,
they become *de jure* immutable at v1.0.

---

## What this doc is NOT

- A complete tutorial for *how* to author a new skill / validator /
  gate / archetype. The procedural detail lives in skill SKILL.md
  files. This doc names the seams and the contracts.
- A roadmap. New skills do not require entries here unless they
  introduce a new extension category. The existing five sections
  cover the v0.6.0 surface area.
- A protected list. New extension categories can be added with a
  PATCH bump on this doc, as long as they describe a seam that
  already exists in the code. They cannot *create* seams; they
  document existing ones.
