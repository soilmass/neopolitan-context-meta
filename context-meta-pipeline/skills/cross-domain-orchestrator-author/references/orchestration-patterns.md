# orchestration-patterns.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

Common patterns for orchestrators that span 2+ families within a single
library. Cross-library orchestrators (across libraries) use a different
skill — see `skills/cross-library-orchestrator/`.

## The four canonical patterns

### Pattern 1: Sequential delegation

```
operator prompt → orchestrator
   → family-A skill (stage 1 of orchestrator)
   → family-B skill (stage 2)
   → orchestrator synthesizes results (stage 3)
```

Use when each family is self-contained and the orchestrator is a thin
shell. Most common pattern. Example: a deploy orchestrator that
delegates to git-collaboration (commit) → test-validation (run tests).

### Pattern 2: Conditional dispatch

```
operator prompt → orchestrator
   → check condition (stage 1)
   → branch:
       if condition_a → family-A skill
       else          → family-B skill
   → orchestrator synthesizes (final stage)
```

Use when the orchestrator's value is the decision logic, not the chaining.
Anti-pattern when the decision is trivial — that should be in the routing
layer, not the orchestrator.

### Pattern 3: Parallel composition

```
operator prompt → orchestrator
   → family-A skill   ┐
   → family-B skill   ├ run in parallel (operator-driven)
   → family-C skill   ┘
   → orchestrator synthesizes (final stage)
```

Use when the families are independent and the orchestrator's value is
preventing the operator from forgetting one. Note: "parallel" here means
the operator can run them in any order; this is NOT script-driven
parallelism (which would violate the procedural-skill discipline per the
v0.5.0 M4 antipattern).

### Pattern 4: Refinement loop

```
operator prompt → orchestrator
   → family-A skill (initial pass)
   → family-B skill (assess)
   → if not converged: back to family-A
   → orchestrator synthesizes
```

Use sparingly. Loops easily become unbounded. Cap at 3 iterations
explicitly in the orchestrator's stage description.

## When NOT to use cross-domain orchestrator

- The "orchestration" is really sequential one-skill-after-another with
  no synthesis. Document the sequence in a runbook, not a skill.
- The orchestration spans libraries (use `cross-library-orchestrator`
  instead — different concerns: dependency resolution, version pinning).
- The orchestration is operator-judgment-heavy at every step. That's a
  procedural skill, not an orchestrator. Author per `skill-author`'s tool
  archetype.

## Stage discipline

Per `family-bootstrap` and `library-bootstrap`'s archetype rules,
`orchestrator` archetype skills:

- have ≥3 stages, ≤8 stages
- each stage produces a named artifact the next stage consumes
- transitions are gated on artifact-presence checks
- the orchestrator's description names which families it composes

Cross-domain orchestrators specifically:

- name BOTH families in the description's "composes" sentence
- declare `depends_on:` entries for one representative skill from each
  family (not every skill — that creates depends_on bloat)
- include an `## Affected families` section listing every family touched

## Audit ritual

When authoring a cross-domain orchestrator, the audit ritual (per
`skill-author/references/audit-ritual.md`) should run against:

- every router whose family the orchestrator touches (typically 2);
- every existing orchestrator that touches ≥1 of the same families;
- the cross-cluster meta-router (when one exists; deferred at v0.7.0).

If the audit surfaces routing contention with another orchestrator, the
fix is sharpening anti-triggers in the cross-domain orchestrator's
description, not the existing one.
