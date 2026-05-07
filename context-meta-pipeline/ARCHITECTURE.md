# Skill Library Architecture

## Purpose

A modular, composable system of Claude skills built on Unix-philosophy principles. Each skill does one thing. Skills compose through explicit handoffs rather than absorption. New domains enter the library through a stage-gated converter that produces tiered families of cross-referencing skills with documented coverage boundaries.

The library is designed to be encompassing — every claimed domain has its capabilities either covered, queued, or named-and-deferred. Silent gaps are the failure mode the architecture exists to prevent.

---

## Design Philosophy

The library inherits five tenets from Unix's design tradition.

**One responsibility per skill.** If a description has "and" between two distinct verbs, the skill is two skills. Internal modes become silent capability creep — users discover them by accident, not by reading the skill description.

**Compose via handoff, not absorption.** Skills name the next skill rather than reimplementing its capability. `skill-author` hands off to a sibling-discovery routine; `family-bootstrap` hands off to `skill-author` for each Tier 1 atom. Neither absorbs.

**Stable interfaces between skills.** The artifacts that move between skills (`taxonomy.md`, `capabilities.json`, `patterns.json`, `coverage.md`) are named and consistent. They are not internal implementation details; they are the contract between cooperating skills.

**Mechanism separated from policy.** Domain reality is one skill; opinions about how to use it are another. Mechanism atoms ship to any team unchanged; policy overlays carry the team-specific conventions.

**Worse-is-better triggers.** Skill descriptions are matched against natural language by an LLM. Trust short descriptions and disciplined anti-triggers over elaborate trigger logic.

These rules are observable in Anthropic's public skills (`pdf` and `pdf-reading` are separate skills; `file-reading` is explicitly framed as a router) and in the library's own conventions documented below.

The alternative — monolithic frameworks that try to handle a whole domain in one skill — produces routing brittleness, internal mode-switching, and silent capability gaps. The library trades a higher skill count for clean boundaries.

---

## Skill Archetypes

Every skill in the library is exactly one of these five types. A skill that combines two archetypes is two skills.

| Archetype | Unix analog | What it does | Examples |
|---|---|---|---|
| **Atom** | `cat`, `wc`, `grep` | Single capability, narrow domain | `pdf-reading`, `git-history-rewriting`, `kubectl-cluster-state-mutations` |
| **Tool** | shell utilities, language compilers | One workflow, single output | `skill-author`, `skill-audit`, `skill-refactor` |
| **Router** | `xargs`, `find -exec` | Dispatches to other skills, no domain knowledge | `file-reading`, `git` |
| **Orchestrator** | shell scripts, `make` | Coordinates multiple skills | `family-bootstrap` |
| **Policy** | dotfiles, aliases, project conventions | Conventions and style overlay | `voice-profile`, `house-<domain>-conventions` |

Archetype determines layering, not naming. A router named `git` lives in the Tools layer of the library map below; the bare-domain name reflects user mental model, not archetype.

---

## The Layered Map

Composition is upward-only. Atoms never call up.

```
┌──────────────────────────────────────────────────────────┐
│ POLICY                                                   │
│   Conventions, opinions, team-specific overlays.         │
│   voice-profile · house-<domain>-conventions             │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ ORCHESTRATORS                                            │
│   Multi-skill choreography.                              │
│   family-bootstrap · cross-domain orchestrators          │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ ROUTERS                                                  │
│   Dispatch only. Per-domain entry points.                │
│   file-reading · git · <domain> per family               │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ TOOLS                                                    │
│   Single workflows that produce one kind of output.      │
│   skill-author · skill-audit · skill-refactor            │
│   skill-retire                                           │
└──────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────┐
│ ATOMS                                                    │
│   Single capabilities, narrow domain. The bulk of the    │
│   library lives here.                                    │
│   docx · pdf · pdf-reading · xlsx · pptx                 │
│   git-* (basics, branching, history-rewriting, etc.)     │
└──────────────────────────────────────────────────────────┘
```

Tools call atoms. Orchestrators call tools and atoms. Policy flavors any of them. Routers are dispatch-only — they live in Tools by archetype but exist to hand off, not to perform.

---

## Composition Principles

Seven rules. Each carries a rationale because bare rules invite rationalization.

**1. One responsibility per skill.** Two skills with clean boundaries beat one skill with internal modes. Internal modes become silent capability creep.

**2. Compose via handoff, not absorption.** When a skill needs another's capability, it names the other skill and hands off. Reimplementing creates duplication that drifts.

**3. Anti-triggers are first-class.** Every skill description has a `Do NOT use for` block that fences off siblings. A description that only says what a skill is *for* will compete with every adjacent skill on natural-language matching. Anti-triggers are how routing accuracy holds at scale.

**4. Read/write separation.** Reading and writing operations on the same domain are different skills. They have different risk profiles, different mental models, and different edge cases. `pdf` (creation) and `pdf-reading` (extraction) live separately. The convention extends to every domain.

**5. Mechanism vs policy.** Domain reality is mechanism — stable, objective, ports across teams. Conventions are policy — opinionated, team-specific, evolves. Mechanism atoms never embed team conventions; policy overlays never re-explain mechanism.

**6. Stable interfaces between skills.** The artifacts that move between skills are named and consistent. `capabilities.json`, `patterns.json`, `taxonomy.md`, `coverage.md` are the text streams of the ecosystem.

**7. Worse-is-better triggers.** Over-specification creates routing brittleness. Descriptions that pattern-match too narrowly miss real prompts; descriptions that pattern-match too widely compete with siblings. Short descriptions plus disciplined anti-triggers beat elaborate trigger logic.

---

## Naming Conventions

Locked. Generated atoms inherit these automatically through the converter.

**Lexical conventions** (per clig.dev and observed kubectl/docker/git/aws patterns):

- Lowercase, kebab-case (hyphens, not underscores).
- ≤4 segments total: `<domain>-<scope>` or `<domain>-<scope>-<modifier>`.
- No version numbers in names; use `metadata.version` in frontmatter.

**Domain prefix** = the user's mental-model name for the tool, not the binary:

- Binary `psql`, mental model `postgres` → `postgres`
- Binary `awscli`, mental model `aws` → `aws`
- Binary `kubectl`, mental model `kubectl` → `kubectl`

**Scope segment** uses the domain's own canonical vocabulary:

- Git's docs say "history rewriting" → `git-history-rewriting`
- Kubectl's docs say "cluster state" → `kubectl-cluster-state-mutations`
- Postgres's docs say "transaction isolation" → `postgres-transaction-isolation`

The scope name should describe the failure mode using the domain's own term. The two usually align — official docs name dangerous areas explicitly.

**Universal suffixes** override domain vocabulary for three categories that recur across every domain:

- `-inspection` for read-only operations
- `-recovery` for repair and restoration
- `-config` for configuration and setup

Predictability across domains beats native vocabulary for these three.

**Plumbing vs porcelain** (git's own term, generalized):

- Default is porcelain (user-facing capabilities).
- Plumbing skills get the explicit `-plumbing` suffix.
- Most domains do not need plumbing atoms; build only on documented demand.

**Routers** = bare domain mental-model name. `git`, `postgres`, `kubectl`, `aws`. Never suffixed.

**Policy overlays** follow `<context>-<domain>-<aspect>`:

- `house-git-conventions`
- `acme-postgres-rules`
- `house-test-style`

Three segments signal that the skill modifies a domain rather than being one.

---

## The Tier Model

Every domain claimed by the library produces three tiers of atoms.

**Tier 1 — essential.** Every user touches these regularly. ~70-80% of common usage. 6-9 atoms typical. Always shipped.

**Tier 2 — encompassing.** Common specialist needs — subdomains with their own complexity (hooks, submodules, large-repo handling, debugging workflows). 4-7 atoms typical. Shipped to claim the encompassing property; until then, folded into Tier 1 atoms with the split flagged in `coverage.md`.

**Tier 3 — advanced.** Long tail (plumbing, niche workflows, external bridges). 2-5 atoms typical. Documented as deferred with explicit build triggers; authored only when the trigger fires.

The tier model exists to enforce the encompassing property. A flat list of skills lets long-tail capabilities silently disappear ("we never built it, nobody asked"). Tiers force the deferral into writing. Tier 3 documented-as-deferred is the encompassing property.

**Build triggers must be observable, not aspirational.** "Build when needed" is not a trigger. "Build when a contributor to a kernel-style project joins the cohort" is. "Build when repo size crosses 5 GB" is. The trigger has to be something you would notice; otherwise deferral becomes permanent abandonment.

---

## Coverage Discipline

The encompassing property is structurally enforced by `coverage.md` documents at two levels.

### Per-family coverage.md

Every skill family produced by the converter ships with `coverage.md` at the family root. Six sections:

1. **In Scope (Tier 1)** — atoms shipped, with one-line ownership statements.
2. **Specced, Not Yet Built (Tier 2)** — queued atoms with key concepts and edge cases named.
3. **Deferred (Tier 3)** — named atoms with observable build triggers.
4. **Policy Overlay** — the `house-<domain>-conventions` skill if one exists.
5. **Out of Scope** — capabilities the family explicitly does not cover, with rationale and pointer.
6. **Coverage Matrix Status** — last verification run results.

The Out of Scope section is load-bearing. Most coverage docs focus on what is covered. This template gives equal weight to what is not, because *silent gaps are where encompassing claims actually fail*. A documented gap is a covered gap.

### Library-root coverage.md

The library as a whole maintains its own `coverage.md` documenting:

- Domains claimed (one row per family with link to the family's own coverage.md).
- Domains deferred (named with build triggers).
- Domains explicitly out of scope.
- Cross-domain orchestrators (skills that compose multiple families).

Library-level coverage is maintained by hand. The converter handles per-family; library-level is a separate discipline.

---

## Routing and Contention

Routing accuracy degrades at predictable scale points. Calibrate effort to where the library is.

| Skills | Pattern | Cost |
|---|---|---|
| 0–10 | Disjoint descriptions + anti-triggers | Maintenance only |
| 10–25 | + Audit ritual on every new skill | O(N) audit per addition |
| 25–50 | + Per-domain routers for clusters of 5+ | One new skill per dense domain |
| 50+ | + Held-out routing eval suite | Real infrastructure |

### The audit ritual

Before merging any new skill:

1. List the 3 skills with most-overlapping description keywords.
2. Generate 5 ambiguous prompts that could hit any of them.
3. Run each — does the right skill win?
4. If contention exists, add anti-triggers to non-primary skills naming the new sibling by name.

Catches roughly 80% of routing problems pre-merge for nearly zero cost.

### Per-domain routers

When a domain reaches 5+ atoms, add a router named after the bare domain (`git`, `kubectl`, `postgres`). The router does intent classification only — no domain knowledge.

The atom-precedence rule keeps routers from competing with their own atoms: when a prompt names a specific failure mode by name ("rebase", "reflog"), the matching atom wins on specificity. The router activates only on ambiguous domain prompts.

### Routing eval suite

At ~25+ skills, descriptions become unverifiable by inspection. Build a YAML of `(prompt, expected_skill)` pairs (~100-200 entries), a runner that takes each prompt against current skill descriptions and records actual vs expected, a grader, and a gate that blocks description changes that regress accuracy.

Same machinery as Anthropic's `skill-creator` description optimizer (`run_loop.py`), applied at the library level.

---

## Mechanism vs Policy

The most important architectural split. Most refactor work in the library involves pulling policy out of mechanism.

**Mechanism** is domain reality. Stable, objective, ports across teams. "What `git rebase` does and when it can corrupt history."

**Policy** is conventions. Opinionated, team-specific, evolves. "Our rule: never rebase shared branches."

The composition rule is borrowed from CSS: policy *overrides or constrains* mechanism. Mechanism is the cascade default; policy is the override.

### Three diagnostic tests

1. Could this skill ship to another team unchanged? If no, policy is embedded.
2. Does this make sense without the underlying tool's mechanics? If no, mechanism is embedded.
3. If team conventions changed tomorrow, what would change in this skill? Only the policy skill should change.

### Mechanism-skill rules

No team conventions. No "best practice" claims. Where defaults are unavoidable (a tutorial example, an order in a list), label them as defaults explicitly meant to be overridden.

### Policy-skill rules

Reference the mechanism skill rather than re-explaining commands. The description names the mechanism overridden ("Applies on top of `git-history-rewriting`"). If the mechanism skill is uninstalled, the policy skill should fail loudly, not silently substitute.

### The three-way refactor

When a tool skill mixes mechanism and policy, the refactor produces three skills:

- A mechanism atom (or atoms) that holds the domain reality.
- A tool that orchestrates the mechanism for a workflow.
- A policy overlay that captures team-specific opinions.

Three skills replacing one, each independently maintainable.

---

## The Lifecycle Pipeline

Five skills cover the full lifecycle of every other skill in the library: authoring, family bootstrap, audit, refactor, and retire. Maintenance is first-class — not a procedure tacked onto authoring.

**`skill-author`** (Tool, 4 gated stages: intake → ecosystem audit → drafting → validation & registration) authors a single SKILL.md (atom, tool, router, or policy overlay). Stage 4 runs `validate-metadata.py`, updates the library `CHANGELOG.md`, the `SNAPSHOT.lock`, and the relevant `coverage.md`. Used directly for tools and routers; called by `family-bootstrap` for atoms within a family.

**`family-bootstrap`** (Orchestrator, 6 gated stages: domain intake → capability indexing → taxonomy design → per-skill authoring → weaving → coverage & registration) produces a tiered family from a documented domain. Stage 4 delegates to `skill-author` for each Tier 1 atom. Output: a router, a Tier 1 atom set, a `taxonomy.md`, a per-family `coverage.md`, and a row in the library-root `coverage.md`.

**`skill-audit`** (Tool, 5 gated stages: scope selection → recency scan → drift scan → triggering accuracy probe → synthesis & banner emit) runs the four health-gates from `MAINTENANCE.md` (recency, test pass rate, triggering accuracy, description drift) against existing skills. Emits a per-failing-skill banner block and CHANGELOG `Health` suggestions.

**`skill-refactor`** (Tool, 5 gated stages: diagnosis → plan → execute new skills → retire source + redirect → verification) performs the three-way refactor named in §"Mechanism vs Policy" plus split / merge / move when archetype-mixing is detected. Delegates to `skill-author` (Stage 3) and `skill-retire` (Stage 4).

**`skill-retire`** (Tool, 4 gated stages: justification → dependent check → archive & redirect → snapshot & coverage update) archives a skill with a redirect note, updates the family `coverage.md` and `SNAPSHOT.lock`, and emits a `CHANGELOG` `Removed` or `Deprecated` entry. Per `GOVERNANCE.md` §"Removing a Skill", the SKILL.md remains in git history and remains pinnable.

The deferred `library-architect` concern from earlier drafts is superseded: `skill-refactor` handles the cross-skill restructuring it would have done; `family-bootstrap`'s Stage 6 handles the library-root `coverage.md` updates.

---

## Library-Level Concerns

Three concerns operate above any single family.

### Cross-domain workflows

Some workflows span families: deploying code spans git + CI + cloud; investigating an incident spans logs + metrics + tracing + git history. These workflows need owners. Either:

- An orchestrator skill that composes the families explicitly, or
- An "out of scope" entry in the library-root `coverage.md` with a pointer to the right combination of skills.

Silent ownership of cross-domain workflows is the library-level version of the silent-gap failure mode.

### The library's own scope

The library claims certain domains and explicitly does not claim others. The library-root `coverage.md` documents both. Domains the library will never claim get explicit out-of-scope entries with rationale.

This matters because a request for an unclaimed domain has to land somewhere. Either the user installs a third-party skill, builds a new one, or accepts that the request is out of bounds. Without documentation, every unclaimed-domain request becomes a one-off decision.

### Skill retirement

Skills are retired when:

- The domain they cover stops existing (rare).
- They are absorbed into a more comprehensive skill (refactor outcome).
- The trigger for their existence stops firing — though this usually means the skill stays in deferred state, not actively retired.

Retirement is a deliberate operation: archive the SKILL.md with a final changelog entry, update the family's `coverage.md`, and audit downstream skills that referenced it.

---

## Maintenance

Three rituals keep the library healthy.

### When adding a skill

1. Decide the archetype. If two archetypes fit, the skill is two skills.
2. Run the audit ritual against existing skills. Add anti-triggers to siblings.
3. Update the relevant `coverage.md` (per-family or library-root).
4. If adding an atom to an existing family, regenerate the family's `coverage.md` via the converter's Stage 6.

### When adding a domain

1. Run `family-bootstrap` from Stage 1.
2. Ship Tier 1 atoms only at first. Spec Tier 2; defer Tier 3 with build triggers.
3. Add the domain to the library-root `coverage.md`.
4. Audit existing routers and orchestrators for new cross-domain interactions.

### Periodic audits

Every ~6 months or every 10 new skills, whichever comes first:

1. Re-run Stage 6 coverage verification on each family.
2. Audit Tier 3 build triggers — have any fired without anyone noticing?
3. Re-check anti-triggers across siblings; description drift is silent.
4. Confirm `coverage.md` files are current.

---

## Library-Level Routing

The library has two distinct routing layers, separated by scope:

**Per-cluster routers** — each cluster of 5+ atoms (the meta-pipeline's lifecycle skills, a domain family like `git`, etc.) gets a bare-domain router (`meta`, `git`, `kubectl`, `postgres`). The router does intent classification only; per the atom-precedence rule, atoms named explicitly in a prompt take priority. The meta-pipeline's own cluster has its router at `skills/meta/SKILL.md` from v0.5.0 onward (added when the cluster crossed the 5+-atom threshold via the v0.5.0 build-out).

**Cross-cluster meta-router** *(deferred — see Open Questions below)* — would dispatch across families when the library hosts 5–10+ families and prompts naturally span clusters. This layer does not exist at v0.5.0.

The two layers compose: a prompt enters the cross-cluster meta-router (when it exists), gets classified to a cluster, the cluster's per-cluster router dispatches to an atom. Per-cluster routers do not depend on the cross-cluster meta-router; they work standalone, which is why each per-cluster router can be authored when its cluster reaches the 5-atom threshold without waiting for the meta-router infrastructure.

**Why the threshold differs.** A per-cluster router becomes useful at 5+ atoms because the cluster's atoms compete for prompts that name shared verbs ("audit my X" — which audit?). A cross-cluster meta-router becomes useful at 5–10+ *families* because cross-family prompts are categorically different (they span domains; description-matching alone is too coarse). The cross-cluster threshold is ~50+ skills, equivalent to the routing-eval threshold from §"Routing and Contention".

**The `meta` router naming choice.** The meta-pipeline's per-cluster router is `meta`, not `skill`. The mental model for the cluster is "meta-tooling about skills"; the prefix `skill-*` (8 of 13 atoms) collides with what `skill` would route to. `meta` is the bare-domain mental-model name per `naming.md`.

---

## Cross-Domain Orchestrator Pattern

A cross-domain orchestrator composes atoms from two or more families *within the same library*. The pattern emerges when a real workflow spans domains — a deploy spans `build` + `test` + `deploy`; an incident response spans `logs` + `metrics` + `git-inspection`.

**Authoring**: handed by `cross-domain-orchestrator-author` (Tier 1 tool, v0.5.0+). The tool produces an orchestrator SKILL.md with explicit per-family handoff documentation: data-shapes, state changes, failure modes per family. Cross-family handoffs are *first-class*, not buried in prose.

**Difference from per-cluster routers**: a router *dispatches* (no domain knowledge); an orchestrator *composes* (full multi-step workflow). Routers are dispatch-only; orchestrators choreograph multiple skills.

**Difference from `cross-library-orchestrator`**: the cross-library variant spans skills from *separate* libraries (e.g., `context-git` + `context-cloud`); the cross-domain variant spans *families within one library*. They have separate authoring tools because the snapshot-pinning patterns differ — cross-library declares qualified pins (`context-git/git-collaboration@0.1.0`), cross-domain declares unqualified pins.

**Pattern extraction**: per `cross-domain-orchestrator-author` Stage 5, the second and third cross-domain orchestrators in any library generate evidence for whether the pattern is genuinely extractable into a meta-template. Until 2–3 examples exist, each orchestrator is hand-authored; the *pattern* of what they share is what gets extracted later.

---

## Policy Overlay Composition

A single `house-<domain>-conventions` policy overlay is documented in §"Mechanism vs Policy" and authored via `skill-policy-overlay` (v0.5.0+). The composition question — what happens when multiple policy overlays apply to the same mechanism atom — is more subtle.

**Single-tier composition** (v0.5.0+, supported): one mechanism atom + one policy overlay. The overlay names what it overrides in `## Override Behavior`. Mechanism is the cascade default; policy overrides. Per CSS-cascade analogy: mechanism is browser-default, policy is user-stylesheet.

**Multi-tier composition** *(deferred — see Open Questions below)*: an organization with multiple teams might want a hierarchy — a base `acme-postgres-rules` plus per-team overrides like `acme-frontend-postgres-rules` that further refine. The composition rule for multi-tier is the same CSS cascade, applied recursively: more-specific overrides apply on top of less-specific. The deferred question is *which mechanism resolves the ordering* — an overlay's `## Applies On Top Of` list, or a separate `## Composition Order` section, or a manifest at the library level.

**Pre-trigger discipline**: until 2+ tiers of `house-*` overlays exist on the same mechanism atom, no composition mechanism is built. The single-tier case via `skill-policy-overlay` covers everything that exists today.

---

## Extension Points

The library has stable seams. New skills, new validators, new health
gates, and new archetypes go *through* these seams without architectural
changes. The seams predate the explicit documentation; v0.6.0 adds the
documentation so consumers can extend without re-discovering them.

The five extension categories are:

1. **Adding a new skill** — through `skill-author` / `family-bootstrap`
   / `library-bootstrap` against the stable SKILL.md frontmatter +
   body schema.
2. **Adding a new validator / script** — by matching the validator
   interface contract (argparse + exit codes 0/1/2 + JSON output +
   PyYAML-only dependency).
3. **Adding a new health gate** — by adding a `gate_<name>()` function
   to `audit-skill.py` matching the documented signature.
4. **Adding a new archetype** — explicitly out-of-scope at v0.6.0.
   The seam exists (the `archetype:` enumeration) but authoring a 6th
   archetype is a MAJOR refactor.
5. **Stable interfaces (the six artifacts)** — `SNAPSHOT.lock` /
   `coverage.md` / `SKILL.md` / `MIGRATION-v<N>.md` / `routing-eval.yaml`
   / `CHANGELOG.md`, each with documented schema-stability promises.

Detail per category lives in `governance/EXTENSION-POINTS.md`. The
extension-seam fixtures under `scripts/tests/fixtures/extension-seams/`
prove each seam still holds.

For when these seams become *immutable*, see `docs/PATH-TO-V1.md` —
v1.0 freezes the schemas; v0.x allows interpretation drift between
MINORs.

---

## v0.7.0 Ahead-of-Trigger Note

⚠ **Discipline shift, deliberately taken.** The v0.1.0+ rule was "do not build ahead of trigger." v0.7.0 breaks the rule consciously by building five pieces of deferred infrastructure before their build triggers fired:

1. `scripts/integration-test-runner.py` (per `governance/INTEGRATION-TESTING.md` — trigger: 10+ skills with cross-deps + 2 regressions; 14 skills exist, 0 regressions seen)
2. `scripts/search-skills.py` + `scripts/gen-index.py` + `INDEX.md` (per `governance/SKILL-DISCOVERABILITY.md` — trigger: 50+ skills; 14 exist)
3. `scripts/snapshot-hash.py` + signed-tag enforcement (per `governance/SKILL-PROVENANCE.md` — trigger: external publishing; not yet)
4. `scripts/notify-dependents.py` + `governance/notification-channels.yaml` (per `governance/DEPRECATION-COMMUNICATION.md` — trigger: external consumers; not yet)
5. `scripts/analytics-rollup.py` + `scripts/telemetry-hook.py` (the latter is a stub — real load-time hook blocked on Claude Code core)

Each ahead-of-trigger artifact is marked with a top-of-file comment: `# pre-trigger build (v0.7.0); reassess when trigger fires per governance/<doc>.md`. The discipline existed for two reasons:

1. **Speculative builds bake in wrong assumptions.** Building integration-test-runner.py before any cross-skill regression has actually broken something means we're guessing at failure modes.
2. **Each new script adds maintenance carry** (verify.sh step, fixtures, ruff/mypy budget, future deprecation cost).

Mitigation is *minimum-viable-shell* discipline: each script is the shortest-possible runnable thing that satisfies the docs. When triggers fire, expect re-design — that's the cost of building ahead.

Discipline restored: any future v0.7.x or v0.8.0 work that proposes building further ahead-of-trigger items must include explicit operator approval, the same way v0.7.0 did. No silent ahead-of-trigger drift.

---

## Open Questions

Things deliberately unresolved at v0.5.0.

**Cross-cluster meta-router threshold.** The `meta` router (per-cluster) ships in v0.5.0. A cross-cluster meta-router that dispatches *across families* in a consuming library has no concrete threshold yet — `ARCHITECTURE.md` previously named "5–10 families" but consumers haven't yet hit even one family. The threshold is reaffirmed as "when the consuming library has 10+ families across the library OR when prompts spanning ≥3 families become common enough to warrant a higher-level router". This question stays open until the *first consumer library* exists.

**Eval-suite scaffolding.** The routing-eval starter at `scripts/tests/routing-eval.yaml` exists from v0.2.0; the runner at `scripts/routing-eval-runner.py` exists from v0.5.0. What's still missing is *the routing layer itself* — a real LLM-based classifier that, given a prompt, returns the skill that fires. Without it, `skill-evaluate` operates in static-heuristic / operator-scored / external-pipe modes only. Building the routing layer requires Claude Code-side load-time hooks and is partly outside this plugin's scope.

**Multi-tier policy composition.** Documented in §"Policy Overlay Composition" above as deferred. Trigger: 2+ `house-*` overlays on the same mechanism atom.

These are flagged here so they do not become silent debt.

---

## Where to Go Next

This document covers the system design. The operational layer that sits on top of it lives in separate documents.

- **`GOVERNANCE.md`** — operational rules (dependency model, lock-step upgrades, change notifications, audit trail).
- **`VERSIONING-POLICY.md`** — SemVer application, latest-only support, user pins, migration guides.
- **`MAINTENANCE.md`** — implicit ownership, health threshold gates, auto-warn mechanism, unmaintained skills.
- **`governance/INDEX.md`** — maps the specific operational procedures (breaking-change detection, metadata validation, rollback) and names what is deferred with build triggers.

When in doubt: architecture answers "how is the system designed?" Governance answers "how does the system run?"
