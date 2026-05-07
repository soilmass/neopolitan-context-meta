---
name: meta
description: >
  Per-domain router for the meta-pipeline cluster. Dispatches operator
  prompts to one of 13 lifecycle / library / cross-* / family / skill
  atoms by intent. Intent classification only — no authoring, audit,
  refactor, or retire operations happen in this skill. Do NOT use for:
  any actual lifecycle operation (the routing table names the right
  skill); domain-content questions (use the matching atom or
  ARCHITECTURE.md); routing across families (deferred per ARCHITECTURE.md
  §"Library-level routing meta-router"); routing across libraries
  (deferred until multiple libraries exist).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: router
  tags: [router, discoverability, daily-use]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/router-disambiguation.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 to claim the per-cluster router.
            The 14-skill lifecycle cluster passed the 5+ atoms threshold from
            ARCHITECTURE.md §"Routing and Contention" / §"Per-domain routers".
---

# meta

The bare-domain router for the meta-pipeline cluster. Dispatches
across 13 atoms (skill-* / library-* / family-* / cross-*).

Per `naming.md`, routers are named for the user mental model. The
mental model for this cluster is "meta-tooling about skills", so the
router is `meta` rather than `skill` (which would collide with the
`skill-*` prefix all but five of the atoms use).

## When to Use

- The operator's prompt is meta-pipeline domain but doesn't name a
  specific atom or failure mode.
- The operator names a verb that could route to two or more atoms
  (e.g., "audit my library" — `library-audit` vs `skill-audit`?).
- The operator asks a meta-question about authoring, refactoring, or
  releasing that involves multiple lifecycle skills.

## When NOT to Use

- When the prompt names a specific atom by name (`skill-author`,
  `family-bootstrap`, `library-audit`, etc.) — atom-precedence per
  `ARCHITECTURE.md` §"Per-domain routers".
- For domain-content questions ("explain how skill-audit's drift
  formula works") — use the matching atom or its references.
- For routing across families *within a consuming library* — that's
  the consuming library's router(s), not this one.
- For routing across libraries — deferred per `ARCHITECTURE.md`
  §"Open Questions / Library-level routing meta-router".

## Routing Table

| Intent | Target atom |
|---|---|
| Author a single new skill (atom / tool / router / orchestrator / policy) | `skill-author` |
| Bootstrap a new domain family (router + 6-9 atoms) | `family-bootstrap` |
| Bootstrap a brand-new consuming library | `library-bootstrap` |
| Author an orchestrator spanning two families in one library | `cross-domain-orchestrator-author` |
| Author an orchestrator spanning two installed libraries | `cross-library-orchestrator` |
| Author a `house-*-conventions` policy overlay on top of a mechanism atom | `skill-policy-overlay` |
| Health-check a single skill (recency / drift / gates) | `skill-audit` |
| Library-shape health check (coverage.md, snapshot, cross-skill consistency) | `library-audit` |
| Run held-out routing-eval prompts (Health Gate 3 — triggering accuracy) | `skill-evaluate` |
| Restructure an existing skill (split / merge / move / three-way refactor) | `skill-refactor` |
| Author a MIGRATION-v\<N\>.md guide for a MAJOR version bump | `skill-migrate` |
| Diff two SNAPSHOT.lock states for release notes | `skill-snapshot-diff` |
| Archive a skill with redirect (no delete; remains pinnable) | `skill-retire` |

## Disambiguation Protocol

When a prompt could match two or more atoms, ask one clarifying
question:

- "audit my X" → ask "the *whole library* (library-audit) or *one
  skill* (skill-audit)?"
- "rewrite history" → ask "*one skill's body / capabilities*
  (skill-refactor) or *write a migration guide for a MAJOR bump*
  (skill-migrate)?"
- "release" → ask "*the diff for release notes* (skill-snapshot-diff),
  the *health audit before tagging* (library-audit), or the
  *actual tag* (release-tag.sh script — not a skill)?"
- "deprecate / retire" → "*just archive* (skill-retire) or *split into
  new skills first* (skill-refactor) and then archive the source?"
- "set up a library" → "*from scratch* (library-bootstrap) or *a
  family within an existing library* (family-bootstrap)?"
- "evaluate" → "*triggering accuracy* (skill-evaluate) or
  *full health* (library-audit composes everything)?"

If the operator's prompt names a specific verb belonging to one
atom, atom-precedence applies — skip disambiguation. The router
activates only on genuinely ambiguous prompts.

## Atoms in This Family

Tier 1 (all 13 lifecycle / library / cross-* / family / skill atoms):

- `skill-author`
- `skill-audit`
- `skill-evaluate`
- `skill-migrate`
- `skill-policy-overlay`
- `skill-refactor`
- `skill-retire`
- `skill-snapshot-diff`
- `family-bootstrap`
- `library-audit`
- `library-bootstrap`
- `cross-domain-orchestrator-author`
- `cross-library-orchestrator`

Tier 2 (specced, not yet built; folded into Tier 1 mentions until
built — none currently):

- (none — the cluster's surface area is fully covered at v0.5.0)

Tier 3 (deferred with observable build triggers; see library-root
`coverage.md`):

- `skill-discoverability` (tagging / search beyond LLM matching;
  trigger: 50+ skills in a single library)
- `usage-analytics` (telemetry; trigger: 25+ skills + can't tell
  what's load-bearing)
- (additional Tier 3 atoms surface as `coverage.md` deferred rows
  fire — not enumerated here to avoid ledger drift)

## Non-Negotiable Rules

The router does not perform any operation. It dispatches. If a
prompt actively requests an operation (not a routing question), the
router hands off to the matching atom and does NOT begin the
operation itself. This preserves the architecture's invariant that
routers are dispatch-only.

The router does not answer domain questions about *what skills are*
or *how the meta-pipeline works*. Those are documentation questions
(`ARCHITECTURE.md`, `governance/INDEX.md`, `MAINTENANCE.md`,
`README.md`). The router activates on operational prompts.
