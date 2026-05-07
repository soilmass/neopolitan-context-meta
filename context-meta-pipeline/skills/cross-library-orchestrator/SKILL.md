---
name: cross-library-orchestrator
description: >
  Authors an orchestrator skill that composes skills from two installed
  libraries (e.g., a deploy workflow spanning git + cloud). Produces the
  orchestrator archetype's required sections plus a cross-library
  dependency declaration in SNAPSHOT.lock. Do NOT use for: orchestrators
  within one library spanning two families (use cross-domain-orchestrator-author);
  authoring a single skill (use skill-author); bootstrapping a new
  library (use library-bootstrap).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: orchestrator
  tags: [composition, rare]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/dependency-resolution.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
            Build trigger had not yet fired (no second consumer library exists);
            tool ships ahead of trigger to claim the surface area.
            Per the v0.5.0 risk assessment, this skill is authored against
            speculative use cases — first dogfood will reveal procedural gaps.
---

# cross-library-orchestrator

The Tier 1 orchestrator that composes skills from *two installed
libraries* into a single workflow. Companion to
`cross-domain-orchestrator-author` (which spans two families within
*one* library).

## Purpose

Some workflows naturally span libraries: a deploy spans git
(version control) + cloud (infrastructure); an incident response
spans logs + metrics + tracing + git history. When both libraries
are installed, an orchestrator can compose them.

This tool produces an orchestrator SKILL.md that:
- Names every cross-library skill it composes in `## Skills Coordinated`.
- Declares per-library `depends_on:` pins in `SNAPSHOT.lock`.
- Documents the multi-stage workflow with explicit handoff points
  between libraries.
- Names a fail-loud mode when a required library is uninstalled.

## When to Use

- A real workflow has emerged that spans two installed libraries.
- The workflow is repeated (not a one-off).
- Both libraries' relevant skills already exist (this tool composes;
  it doesn't author the underlying skills).

## When NOT to Use

- For workflows within a single library spanning two families — use
  `cross-domain-orchestrator-author`.
- For a workflow with no clear cross-library handoff (just one
  library's skills in sequence) — use a single-library orchestrator
  authored via `skill-author` archetype=`orchestrator`.
- Speculatively, for "we might want this someday" — author against
  real cases per the architectural discipline. Ship the orchestrator
  the day the second use of the workflow happens.
- For an orchestrator that *would* span libraries but only one is
  currently installed — the second library must exist first.

## The Stages

Five stages.

### Stage 1 — Workflow intake

**Consumes:** the operator's prompt naming the workflow + the two
(or more) libraries involved.

**Produces:** `cross-lib-intake.yaml` with
- `name` — the orchestrator's name (e.g., `deploy-from-git`).
- `libraries` — list of libraries involved with their plugin manifest
  paths and snapshot paths.
- `skills` — for each library, the skills the orchestrator will
  call.
- `workflow` — a sequence of stages, each naming the library + skill
  + handoff condition.

**Gate:** every named library is installed and has a parseable
`SNAPSHOT.lock`; every named skill exists in its library's snapshot;
the workflow has ≥2 stages spanning ≥2 libraries.

### Stage 2 — Composition design

**Consumes:** `cross-lib-intake.yaml`.

**Produces:** `composition.md` documenting
- The handoff points between libraries (what data passes; what
  state changes occur).
- The dependency direction (library A depends on library B's output;
  is the reverse possible?).
- Failure modes when a library's skill errors mid-workflow.

**Gate:** every handoff has a defined data-shape; every failure mode
has a defined recovery path (rollback / retry / escalate).

### Stage 3 — Delegate to skill-author

**Consumes:** Stages 1-2.

**Produces:** the orchestrator SKILL.md authored via `skill-author`
with archetype=`orchestrator`. The required sections (`Purpose`,
`When to Use`, `When NOT to Use`, `The Stages`, `Skills Coordinated`,
`Failure Modes`, `Handoffs`) are pre-filled from the composition.

**Gate:** `validate-metadata.py` exits 0; `## Skills Coordinated`
names every cross-library skill explicitly with library qualifier
(e.g., `context-git/git-collaboration`).

### Stage 4 — Cross-library snapshot pins

**Consumes:** Stage 3's SKILL.md + the involved libraries' snapshots.

**Produces:** an updated entry in *the orchestrator's host library*
`SNAPSHOT.lock` for this orchestrator, with `depends_on:` listing
every cross-library skill at its current version, qualified by
library:

```yaml
deploy-from-git:
  version: "0.1.0"
  archetype: orchestrator
  path: "skills/deploy-from-git/SKILL.md"
  health: "fresh"
  depends_on:
    - context-git/git-collaboration@0.1.0
    - context-cloud/aws-deployments@0.1.0
```

**Gate:** every cross-library pin resolves to an existing skill at
the pinned version in the named library.

### Stage 5 — Verify

**Consumes:** the post-authoring state.

**Produces:** the output of `verify.sh` plus a manual cross-library
check: stop, install only one of the libraries, confirm the
orchestrator fails loudly with a "missing library" message
(not silent substitution).

**Gate:** `verify.sh` exit 0; the fail-loud check passes.

## Skills Coordinated

- **`skill-author`** — Stage 3 delegation.
- **`scripts/validate-metadata.py`** — Stage 3 gate.
- **`scripts/dependency-graph.py`** — useful for visualizing the
  cross-library edges.

## Failure Modes

- **Stage 1 gate fails** (a named library isn't installed). Halt;
  the operator installs the missing library before re-running.
- **Stage 2 gate fails** (handoff data-shapes don't compose). The
  workflow is malformed; either re-design the workflow or refactor
  one of the underlying skills via `skill-refactor`.
- **Stage 4 gate fails** (cross-library pin doesn't resolve). Either
  the named version is wrong or the cross-library snapshot is
  stale.
- **Stage 5 fail-loud check fails** (orchestrator silently
  substitutes when a library is missing). This is a real bug; fix
  the orchestrator's `## Override Behavior` (or equivalent failure
  documentation) to fail loudly.

## Handoffs

- **From the operator** — direct invocation when a real
  cross-library workflow emerges.
- **To `skill-author`** — Stage 3.
- **To `library-audit`** — the new orchestrator is in scope for the
  audit's snapshot-integrity check (Stage 4 verifies cross-library
  pins).
