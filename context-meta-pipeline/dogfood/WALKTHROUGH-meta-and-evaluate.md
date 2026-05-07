# Walkthrough: meta router + skill-evaluate

Phase 2 dogfood walkthrough #1 + #2 (paired — skill-evaluate Stage 3 invokes
the runner which validates the meta router's dispatch decisions over
the routing-eval suite).

## Procedure walked

`skill-evaluate` 5 stages, end-to-end:

- **Stage 1 (mode selection)** → static (no real routing layer in v0.5.x)
- **Stage 2 (prompt suite scope)** → loaded `scripts/tests/routing-eval.yaml`
  (31 prompts: 28 across 5 skills + 3 negatives)
- **Stage 3 (run runner)** → `routing-eval-runner.py --mode static`
- **Stage 4 (synthesis)** → see Findings below
- **Stage 5 (CHANGELOG suggestion)** → captured as A22+ entries

## Result

```
mode=static, threshold=85%
✗ family-bootstrap: 4/6 = 66.7%   (was ~83% pre-v0.5.0)
✓ none:             3/3 = 100.0%
✗ skill-audit:      1/6 = 16.7%   (was ~50%)
✗ skill-author:     0/6 = 0.0%    (was ~33%)
✗ skill-refactor:   1/6 = 16.7%   (was ~33%)
✗ skill-retire:     1/4 = 25.0%   (was ~50%)
```

Five of six skills fail the 85% threshold; four catastrophically.

## Findings

### A22 — routing-eval suite is stale relative to the v0.5.0 cluster

The 31 prompts were authored against the v0.2.0 5-skill cluster.
After v0.5.0 added 8 lifecycle skills + a router, many prompts that
were previously unambiguous are now genuinely contended:

- "Run the health checks on all skills in the library" — could be
  `skill-audit --all` OR the new `library-audit` (which composes
  audit-skill + coverage-check + verify.sh + snapshot integrity).
  In context, `library-audit` is arguably the better target.
- "Check description drift across the library" — same situation;
  `library-audit` wraps the cross-skill view.
- "Help me draft a tool skill that orchestrates a deploy workflow" —
  could be `skill-author` (single tool) OR
  `cross-domain-orchestrator-author` (the new orchestrator-spanning-
  families skill) OR `cross-library-orchestrator`.

**Remedy** (queued for v0.5.2): update routing-eval.yaml's prompts
for the 14-skill cluster. Some prompts move to new expected skills;
some are removed (genuinely ambiguous post-v0.5.0); new prompts are
added covering the 8 new skills and the meta router.

### A23 — static-mode heuristic over-weights routers

The `meta` router lists every atom in its `## Routing Table` and
`## Atoms in This Family` sections. The static heuristic's
keyword-overlap metric therefore scores `meta` highly on most
prompts containing any atom-related keyword. Concrete misses:

- "We need a postgres family" → got `meta` (expected `family-bootstrap`)
- "Add a router for our git family" → got `meta` (expected `skill-author`)
- "Split git-history-rewriting into two atoms" → got `meta`
  (expected `skill-refactor`)

This is structurally inevitable for static keyword-overlap because
routers are *designed* to mention every dispatch target. The static
heuristic should de-rank routers (treat them as low-priority unless
the prompt explicitly asks for routing).

**Remedy** (queued for v0.5.2 or v0.6.0): in
`routing-eval-runner.py:static_routing()`, when computing the
overlap score, multiply router-archetype skills by 0.5 (or skip
them entirely unless no atom matched). Document the bias explicitly
in `routing-eval-protocol.md`.

### A24 — new sibling siblings displace original skills

Pre-v0.5.0: "Run the health checks" → `skill-audit`. Post-v0.5.0:
the same prompt routes to `library-audit` because `library-audit`'s
description includes "library-shape health check" — a stronger
keyword match for "health checks all skills" than `skill-audit`'s
"per-skill health-gates" framing.

**Remedy** (queued for v0.5.2): the original 5 lifecycle skills
need anti-trigger updates fencing off the new siblings. This is the
"v0.5.1-deferred routing-contention audit" called out in the v0.5.0
CHANGELOG — confirmed urgent by this walkthrough. Each of:
`skill-author`, `skill-audit`, `skill-refactor`, `skill-retire`,
`family-bootstrap` gets a description revision adding `Do NOT use
for: <new sibling>` clauses. Bumps each to PATCH per
VERSIONING-POLICY.md "clarification" rule.

### A25 — `meta` router as itself a routing target

Several prompts route to `meta`. By the architecture's atom-
precedence rule, the router should NEVER be the dispatch target;
it should always defer to a more-specific atom. Yet the static
heuristic doesn't model atom-precedence. The real (LLM-based)
routing layer presumably DOES — atom-precedence is a description-
level rule the LLM reads. But the static heuristic is a poor
proxy for routing here.

**Remedy**: tighten static-routing's atom-precedence emulation:
if any atom skill scores within 20% of the router's score, prefer
the atom. Documented in routing-eval-protocol.md.

## Bug status

No structural bugs in `meta` SKILL.md, `skill-evaluate` SKILL.md,
or `routing-eval-runner.py` itself. The findings are about (a) the
suite being stale for the new cluster, and (b) the static
heuristic being too coarse for the v0.5.0 surface area. Both are
addressable in v0.5.2 without changing the procedural skills.

## Walkthrough verdict

PASS — the procedure flows end-to-end; 5 stages all execute; the
output is the expected per-skill report. The accuracy numbers
themselves are bad, but that's a *finding* about the input data
(routing-eval.yaml), not a finding about the procedure. The skill
correctly identified that the library has a routing-contention
problem at v0.5.0.
