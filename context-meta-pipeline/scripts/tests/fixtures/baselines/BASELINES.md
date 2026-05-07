# Shared baseline fixtures

Per-archetype "known-good" SKILL.md files used as the *baseline* side of
fixture pairs in:

- `scripts/tests/fixtures/breaking-changes/` — paired with a
  modified SKILL.md to exercise `detect-breaking-changes.py`.
- `scripts/tests/fixtures/migration/` — paired with a modified
  SKILL.md to exercise `migration-guide-gen.py`.

This directory exists so the same baseline isn't duplicated across
fixture trees. Each baseline is referenced by relative path from
the consuming pair's harness.

## Files

| Baseline | Archetype | Purpose |
|---|---|---|
| `atom-baseline.md` | atom | atom with 2 capabilities (A, B), valid frontmatter, all 6 required sections |
| `tool-baseline.md` | tool | tool with 3 stages, valid frontmatter, all 7 required sections |
| `router-baseline.md` | router | router with 3 routing-table entries, all 5 required sections |
| `orchestrator-baseline.md` | orchestrator | orchestrator with 3 stages + 2 skills coordinated |
| `policy-baseline.md` | policy | policy with 2 conventions + override-behavior |

## Convention

Baselines are *minimal, valid, well-formed* SKILL.md files. They pass
`validate-metadata.py` clean (exit 0, no warnings). They do NOT
attempt to be realistic skills — they're test inputs. Names use the
prefix `bl-` (short for baseline) to make their fixture-only role
obvious in any error output.

## Versioning

Baselines do not appear in `SNAPSHOT.lock`. They're test material,
not skills. The naming regex still applies (kebab-case, ≤4 segments)
because validate-metadata.py validates them as SKILL.md.
