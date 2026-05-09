# Metadata Validation

Every SKILL.md must pass structural validation before merging. Without this gate, frontmatter drift accumulates silently — descriptions get too long, required sections disappear, archetype-specific conventions erode.

This document specifies what gets validated, by archetype, and what happens when validation fails.

---

## Universal Validation (All Skills)

Every skill, regardless of archetype, must satisfy:

### Frontmatter

- **`name`** present, lowercase, kebab-case, ≤ 4 segments separated by hyphens (e.g., `git-history-rewriting`).
- **`description`** present, third-person, under 1024 characters.
- **`description`** contains a `Do NOT use for` block fencing off siblings (anti-triggers, per ARCHITECTURE.md). The validator checks for the literal phrase "Do NOT use for" or close variants.
- **`license`** present (typically `Apache-2.0` or `MIT`).
- **`metadata.version`** present, valid SemVer (MAJOR.MINOR.PATCH).
- **`metadata.changelog`** present, contains at minimum the current version's entry.

### Body structure

- SKILL.md body under 500 lines (counting from the closing `---` of frontmatter).
- All references one level deep (no `references/foo/bar.md`).
- Reference files over 300 lines must open with a table of contents.
- No nested-dash subdomains beyond two segments past the prefix (e.g., `git-history-rewriting` is fine; `git-history-rewriting-conflicts` is not).

### Naming conventions

- Hyphens, not underscores.
- No version numbers in skill names.
- Lowercase only.

These are checked by simple regex and length checks. Failures block merge with a specific error message naming the violation.

---

## Archetype-Specific Required Sections

Each archetype has its own checklist. The validator determines archetype from the skill's location in the directory structure (or from a `metadata.archetype` field if added).

### Atoms

Required sections:

- `## When to Use`
- `## When NOT to Use`
- `## Capabilities Owned` (must contain a list of specific capabilities)
- `## Handoffs to Other Skills` (must name siblings the atom hands off to)
- `## Edge Cases`
- `## References`

Optional but recommended:

- `## Anti-Patterns` (named patterns that should route elsewhere)
- `## Examples`

### Tools

Required sections:

- `## Purpose`
- `## When to Use`
- `## When NOT to Use`
- `## Stage-Gated Procedure` (or equivalent named workflow)
- `## Dependencies`
- `## Evaluation` (how to verify the tool works correctly)
- `## Handoffs`

Optional:

- `## Self-Audit`
- `## Edge Cases`

### Routers

Required sections:

- `## When to Use`
- `## When NOT to Use` (broader scope exclusions; differs from frontmatter `Do NOT use for` which fences siblings at the description level)
- `## Routing Table` (must be a table or structured list mapping intent → atom)
- `## Disambiguation Protocol` (how to handle ambiguous prompts when no single atom is the obvious target)
- `## Atoms in This Family` (the dispatch targets)

Optional:

- `## Non-Negotiable Rules` (when the router has invariants like "do not answer domain questions")
- `## Edge Cases`
- `## Self-Audit`

Note: anti-triggers themselves live in the frontmatter description (the `Do NOT use for` block), not in a separate body section. ARCHITECTURE.md treats anti-triggers as a description-level concern.

### Orchestrators

Required sections:

- `## Purpose`
- `## When to Use`
- `## When NOT to Use`
- `## The Stages` (multi-skill choreography)
- `## Skills Coordinated` (which skills the orchestrator calls)
- `## Failure Modes` (what happens when sub-skills fail)
- `## Handoffs`

### Policy Overlays

Required sections:

- `## Purpose`
- `## Applies On Top Of` (which mechanism skill the policy overlays)
- `## Conventions Enforced`
- `## Override Behavior` (what the policy overrides in the underlying mechanism)

---

## Description Quality Checks

The description field is load-bearing — it's how the LLM decides whether to invoke the skill. Beyond length, the validator checks:

- Description is third-person ("Builds X" not "I build X" or "You can use this to build X").
- Description names what the skill IS for and what it is NOT for.
- Description includes trigger phrases (the kind of language a user would actually use).
- Description does not duplicate the skill name verbatim (it should explain, not restate).

These are heuristic checks — failures produce warnings, not blocks. Reviewer judgment applies.

---

## Reference File Validation

If a skill includes `references/` files:

- Each reference file must be under 1000 lines.
- Files over 300 lines must have a table of contents at the top.
- **References must not chain** (no `references/A.md` linking to `references/B.md` *within the same skill*). If they do, restructure into a single file or split into separate skills. Cross-skill pointers (`other-skill/references/foo.md`) are intentionally allowed; same-skill chaining is not. Surfaced explicitly here per audit finding A61 — operators were violating the rule without realizing it was a rule. The validator catches the violation at PR time with the error: `references must not link to other references in the same skill (per METADATA-VALIDATION.md)`.

---

## What the validator catches at a glance

Single-page summary of every check the validator runs. Errors block merge; warnings inform without blocking. Use this table when authoring a new SKILL.md to know what will get flagged.

| Check | Severity | Source |
|---|---|---|
| `name` present, kebab-case, ≤4 segments | error | Universal §"Frontmatter" |
| `description` present, ≤1024 chars | error | Universal §"Frontmatter" |
| `description` contains "Do NOT use for" anti-trigger block | error | Universal §"Frontmatter" |
| `license` present | error | Universal §"Frontmatter" |
| `metadata.version` valid SemVer | error | Universal §"Frontmatter" |
| `metadata.changelog` present, mentions current version | error | Universal §"Frontmatter" |
| Body ≤500 lines | error | Universal §"Body structure" |
| Required sections present per archetype | error | §"Archetype-Specific Required Sections" |
| Archetype value is one of the canonical 5 | error | Universal §"Frontmatter" (added v0.6.0) |
| References ≤1000 lines each | error | §"Reference File Validation" |
| References over 300 lines have ToC | error | §"Reference File Validation" |
| **Same-skill reference chaining** (`references/A.md` linking to `references/B.md`) | **error** | §"Reference File Validation" — surfaced as A61 |
| `metadata.tags` is kebab-case, ≤5 tags | warning (cap) / error (shape) | §"Optional fields" (added v0.7.0) |
| Description is third-person | warning | §"Description Quality Checks" |
| Description does not duplicate name | warning | §"Description Quality Checks" |
| Name segment shaped like version literal | warning | §"v0.2.0 hardening" |
| Empty required-section content | warning | §"v0.2.0 hardening" |
| Duplicate H2 sections | warning | §"v0.2.0 hardening" |
| `metadata.recency_pin` value is `stable` (or warns on novel value) | warning / error | §"v0.6.2 hardening" (added v0.6.2) |
| Router lists atoms in `## Atoms in This Family` that don't resolve | warning | Router-specific (added v0.4.0) |
| `depends_on:` pin freshness (same-MAJOR window) | warning / error | Library-wide check (added v0.6.1) |

Severity-blocking errors emit the full "Errors (block merge)" report; warnings appear in a "Warnings (do not block)" block in the same report.

---

## Validation Output

When validation fails, the validator produces a structured report:

```
METADATA VALIDATION FAILED for skill: git-history-rewriting

Archetype detected: Atom

Errors (block merge):
[X] Missing required section: ## Capabilities Owned
[X] Description exceeds 1024 characters (currently 1187)
[X] Frontmatter field `metadata.version` not valid SemVer (got "1.4")

Warnings (do not block):
[!] Description does not include trigger phrases ("rebase", "rewrite history", etc.)
[!] No `## Edge Cases` section (recommended for atoms)

Fix the errors and re-run validation.
```

Errors block merge. Warnings are informational and surface for reviewer attention but don't prevent shipping.

---

## When Validation Runs

- **Pre-commit hook** (optional, recommended): catches issues before commit.
- **PR check** (required): runs on every PR that modifies a SKILL.md or its references.
- **Periodic audit** (monthly): runs against all skills in the library to catch drift in skills that haven't been touched.

The periodic audit is the safety net — when a skill hasn't changed but the validation rules have, the audit surfaces the gap.

---

## Adding New Validation Rules

When a new pattern emerges that warrants validation (e.g., a new archetype, a new field, a new convention), add it to this document FIRST, then update the validator script. Skills already in the library are grandfathered until their next version bump, at which point they must comply.

This prevents new rules from invalidating dozens of existing skills on the day they're introduced.

---

## Implementation Notes

Implemented in v0.1.0 as `scripts/validate-metadata.py` (Python 3, PyYAML + stdlib). It needs:

- Read access to the SKILL.md being validated.
- Read access to its `references/` directory.
- Knowledge of the archetype-specific section lists (encoded in the script).
- Output in the structured format above (text or JSON via `--format`).
- Exit codes: 0 all errors pass, 1 any error fails (blocks merge), 2 invocation problem (file not found, malformed YAML).

The Python implementation is the canonical one. Other CI platforms can shell out to it.

### v0.2.0 hardening

In v0.2.0 the validator gained four additional checks on top of the universal + archetype rules:

- **Reference chaining** *(error)*: a `references/X.md` file linking to another `references/Y.md` *within the same skill* fails the gate. Cross-skill pointers (`other-skill/references/foo.md`) are intentionally allowed.
- **Name segment shaped like a version literal** *(warning)*: a name segment matching `v?\d+(\.\d+)*` (e.g., `pdf-v2`, `s3-1`) warns per `naming.md`'s "no version numbers in names" rule.
- **Empty required-section content** *(warning)*: a required H2 title present but with no body underneath warns; this catches copy-paste authoring oversights without blocking.
- **Duplicate H2 sections** *(warning)*: the same H2 title appearing twice warns; usually a copy-paste artifact.

Fixture coverage for the new rules ships under `scripts/tests/fixtures/atom-fail-reference-chain/`, `atom-fail-reference-subdir/`, and the existing flat fixtures.
