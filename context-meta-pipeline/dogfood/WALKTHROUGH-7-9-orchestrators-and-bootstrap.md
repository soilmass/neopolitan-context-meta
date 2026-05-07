# Walkthroughs 7–9: cross-domain-orchestrator-author, cross-library-orchestrator, library-bootstrap

Phase 2 dogfood walkthroughs of the three most-speculative v0.5.0 skills.

## Walkthrough 7: cross-domain-orchestrator-author

**Synthetic input:** `deploy-from-git-and-test` orchestrator spanning
hypothetical `git` + `test` families (neither exists in any
real library).

**Procedure walked:**
- Stage 1 (workflow intake) — produced cross-domain-intake.yaml with
  families = [git, test]; skills = [git-collaboration, test-runner]
- Stage 2 (handoff design) — handoff doc: git pushes → test-runner
  picks up the new commit
- Stage 3 (delegate to skill-author) — would produce SKILL.md
  referencing hypothetical atoms
- Stage 4 (family handoff weave-back) — would update each
  involved atom's `## Handoffs to Other Skills` (atoms don't exist)
- Stage 5 (verify + coverage row) — coverage.md gains a Cross-Domain
  Orchestrators row

**Verdict:** procedure walks. Same speculative-skill caveat as
walkthrough 6 — the Stage 1 gate ("every named family has a router
in the consuming library") is operator-confirmed for hypothetical
families.

**No findings.** Skill works as designed for the speculative-input
case.

---

## Walkthrough 8: cross-library-orchestrator

**Synthetic input:** `deploy-from-git` spanning hypothetical
`context-git` + `context-cloud` libraries.

**Procedure walked:**
- Stage 1 (workflow intake) — Gate fires immediately: "every named
  library is installed and has a parseable SNAPSHOT.lock". No second
  library is installed. **Gate fails as designed.**

The skill correctly halts at Stage 1 when no second library exists.
This confirms the gate machinery — speculation-by-default behavior
is the right default.

**Verdict:** PASS — skill correctly refuses to proceed against
nonexistent libraries. The build-trigger discipline holds at the
gate level.

**No findings.**

---

## Walkthrough 9: library-bootstrap

**Synthetic input:** `context-test` library with first-domains
`[test, example]`.

**Procedure walked end-to-end (in /tmp/context-test/):**

- Stage 1 (library intake) → library-intake.yaml ✓
- Stage 2 (plugin manifest) → `.claude-plugin/plugin.json` ✓
- Stage 3 (governance + ledger scaffolding) → SNAPSHOT.lock,
  coverage.md, governance/INDEX.md, CHANGELOG.md, README.md
- Stage 4 (operational scaffolding) → **gap surfaced** (see findings)
- Stage 5 (marketplace registration) → would update parent's
  marketplace.json
- Stage 6 (reference the meta-pipeline) → governance/INDEX.md
  references the meta-pipeline's three load-bearing docs
- Stage 7 (verify) → **gap surfaced** (see findings)

## Findings (across all three speculative walkthroughs)

### A31 — coverage-check.py warns on freshly-bootstrapped library's coverage.md

The Coverage Matrix Status section warning fires because there's no
"Last skill-audit run" marker yet (the new library has zero skills).
This is the default state for a freshly-bootstrapped library —
expected, but the warning fires anyway.

**Remedy** (queued for v0.5.2): in `coverage-check.py`, suppress
the Coverage Matrix Status warning when the section text contains
"No skills yet" or equivalent stub markers. Or: library-bootstrap
Stage 3 produces a coverage.md with "Last skill-audit run: N/A
(library has no skills yet — re-run after first family bootstrap)"
which the warning regex would tolerate.

### A32 — library-bootstrap Stage 4 names files but doesn't specify their content

Stage 4 says "Produces: Makefile, verify.sh, requirements.txt,
.gitignore, CONTRIBUTING.md, LICENSE, .github/workflows/verify.yml".
But the SKILL.md doesn't specify the CONTENT of these scaffolded
files. The procedure can't be walked end-to-end without authoring
templates.

**Remedy** (queued for v0.5.2): author the named-but-missing
references for `library-bootstrap`:
- `references/library-skeleton.md` — the seven files Stage 4
  produces, with content templates (parameterized by library name).
- `references/plugin-manifest.md` — plugin.json schema reference.
- `references/marketplace-row.md` — Stage 5's marketplace.json edit.

These files were named in the critical-files list of the v0.5.0
plan but never authored.

### A33 — library-bootstrap has a circular Stage 4 → Stage 7 dependency

Stage 7's gate is "verify.sh exit 0". But Stage 4 produces verify.sh.
If Stage 4's verify.sh template is broken, Stage 7 can't validate.
The procedure works only when Stage 4 produces a known-good template.

**Remedy** (queued for v0.5.2): the `references/library-skeleton.md`
template (per A32) ships with a verified-clean `verify.sh` skeleton.
Adding it to library-bootstrap's references closes both findings.

### A34 — Stage 3's coverage.md template undefined for empty libraries

The coverage-template.md in family-bootstrap/references is for
**family** coverage.md, not library-root coverage.md. Library-root
schema is defined in coverage-check.py but no canonical empty-library
template exists. My walkthrough invented one.

**Remedy** (queued for v0.5.2): library-bootstrap Stage 3 references
a `references/library-skeleton.md` (per A32 / A33) which includes
the canonical empty-library coverage.md.

## Summary across walkthroughs 7–9

| Walkthrough | Findings | Verdict |
|---|---|---|
| 7 — cross-domain-orchestrator-author | 0 | PASS (speculative-input caveat) |
| 8 — cross-library-orchestrator | 0 | PASS (gate halts as designed) |
| 9 — library-bootstrap | 4 (A31, A32, A33, A34) | needs reference files in v0.5.2 |

A31 fixes coverage-check.py; A32–A34 are addressed by authoring
3 reference files for library-bootstrap. All are PATCH-bump scope.

## Bug status

- A31 → script bug, fix in coverage-check.py (PATCH bump on script)
- A32–A34 → missing reference files, fix in skills/library-bootstrap/references/ (PATCH bump on library-bootstrap)
- All others (A26 from walkthrough 4, A27/A28/A29 from walkthrough 5, A30 from walkthrough 6) → doc precision, also addressable in v0.5.2

Total Phase 2 findings: A22–A34 (13 entries).
