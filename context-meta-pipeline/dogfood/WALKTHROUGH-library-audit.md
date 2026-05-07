# Walkthrough: library-audit

Phase 2 dogfood walkthrough #5.

## Procedure walked

5 stages end-to-end against the live v0.5.1 library.

- **Stage 1 (scope selection)** → root = plugin root, fixtures excluded
- **Stage 2 (per-skill audit, delegated)** → audit-skill --all → 14/14 pass
- **Stage 3 (coverage schema check, delegated)** → coverage-check.py exit 0
- **Stage 4 (snapshot integrity)** → 14 nodes, 9 edges, 0 cycles, 0 unresolved
- **Stage 5 (synthesis)** → PASS — no flagged items

## Result

Library-audit's output: PASS clean. Composes audit-skill +
coverage-check + dependency-graph correctly. The skill works as a
true rollup of the existing scripts.

## Findings

### A27 — library-audit doesn't actually invoke verify.sh

The skill SKILL.md mentions `verify.sh` as a Stage 4 component, but
the procedure as walked uses `dependency-graph.py --format json` for
snapshot integrity, not `verify.sh` itself. This is fine in practice
(verify.sh's own version-triangulation logic is duplicated in
library-audit's interpretation of the dep graph), but the SKILL.md
should be precise: Stage 4 either *invokes* verify.sh OR composes
the same checks separately, not both.

**Remedy** (minor doc clarification, queued for v0.5.2): tighten the
`library-audit` SKILL.md Stage 4 description to say "snapshot
integrity check via dependency-graph.py + a manual cross-check that
plugin.json / marketplace.json / SNAPSHOT.lock versions agree (the
same triangulation verify.sh step 4 performs)." Avoid implying
this stage shells out to verify.sh.

### A28 — no `library-audit-report.md` artifact format pinned

Stage 5 says "Produces: `library-audit-report.md` with one-line
headline + per-stage rollup + recommended remedies + CHANGELOG
suggestion." But the format is described, not specified. Different
operators will produce different shapes.

**Remedy** (minor; queued for v0.5.2 if other walkthroughs add to
the queue, otherwise v0.6.0): add a `references/rollup-template.md`
under `skills/library-audit/references/` with the canonical
report shape (it was named in the SKILL.md's Dependencies but the
file doesn't exist yet — see also A29).

### A29 — referenced `references/rollup-template.md` doesn't exist

`library-audit/SKILL.md` Dependencies section names
`references/library-gates.md` and `references/rollup-template.md`,
but neither file exists. The `references/` directory under
`skills/library-audit/` was created in v0.5.0 but never populated.

**Remedy** (queued for v0.5.2): author both reference files. Each is
a short doc explaining what it claims to.

## Bug status

No load-bearing bugs. A27/A28/A29 are doc-precision findings. The
skill works in practice (the walkthrough completed successfully).

## Walkthrough verdict

PASS with 3 minor doc findings (A27/A28/A29 all queued for v0.5.2).
