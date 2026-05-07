---
name: skill-policy-overlay
description: >
  Authors a `house-<domain>-conventions` policy overlay on top of an
  existing mechanism atom. Produces the policy archetype's four
  required sections (Purpose, Applies On Top Of, Conventions Enforced,
  Override Behavior) following the CSS-cascade composition rule from
  ARCHITECTURE.md. Do NOT use for: authoring mechanism atoms (use
  skill-author with archetype=atom); authoring tools (use skill-author
  with archetype=tool); composing multi-tier policy (acme-base +
  acme-frontend) — that's deferred per ARCHITECTURE.md.
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: tool
  tags: [lifecycle, composition]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/composition-rules.md`, `references/precedence-table.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
            Build trigger had not yet fired (zero house-* skills exist);
            tool ships ahead of trigger to claim the surface area.
---

# skill-policy-overlay

Tier 1 tool for authoring a single policy overlay. Per
`ARCHITECTURE.md` §"Mechanism vs Policy", policy overlays apply
team-specific conventions on top of mechanism atoms via a
CSS-cascade-style composition rule: mechanism is the default; policy
overrides.

## Purpose

Author the four-section policy SKILL.md (Purpose / Applies On Top
Of / Conventions Enforced / Override Behavior) in a way that:

1. The naming convention `<context>-<domain>-<aspect>` is followed
   (`house-git-conventions`, `acme-postgres-rules`, etc.).
2. The mechanism atom(s) being overlaid are explicitly named in
   `## Applies On Top Of` and pinned in `SNAPSHOT.lock` `depends_on:`.
3. The conventions section is opinionated and team-specific (not a
   re-explanation of mechanism).
4. The override behavior is fail-loud when the mechanism atom is
   missing, not silent-substitution.

The tool delegates the actual SKILL.md authoring to `skill-author`
with archetype=`policy`; this tool's contribution is the policy-
specific intake (which mechanism atom, what conventions, what
override semantics).

## When to Use

- A team has stable conventions for a domain (git workflow rules,
  postgres connection-string conventions, kubectl namespace
  policies) that are stable enough to encode.
- A `skill-refactor` three-way refactor produces a policy overlay
  as part of the split.
- A consumer library wants to ship its own house conventions on top
  of a mechanism family bootstrapped via `family-bootstrap`.

## When NOT to Use

- For authoring the mechanism atom itself — use `skill-author` with
  archetype=`atom`. Conventions live in policy; mechanism is
  team-neutral.
- For authoring a tool (workflow orchestrating mechanism for a
  specific use case) — use `skill-author` with archetype=`tool`. A
  tool is procedural; a policy is declarative.
- For composing multi-tier policy (e.g., `acme-base` + per-team
  overrides) — that's deferred per `ARCHITECTURE.md` §"Policy overlay
  composition" until 2+ tiers exist.
- For one-off "do X this way" rules embedded in a single skill —
  fold into the existing skill's body; don't extract.

## Stage-Gated Procedure

Four stages.

### Stage 1 — Policy intake

**Consumes:** the operator's prompt naming the mechanism atom + the
conventions to encode.

**Produces:** `policy-intake.yaml` with
- `name` — `<context>-<domain>-<aspect>` (kebab-case, 3 segments)
- `applies_on_top_of` — list of mechanism skills this overlays
- `conventions` — list of bullet-shaped declarative rules
- `override_behavior` — text describing what happens when the
  mechanism is absent / substituted / disagrees

**Gate:** name matches the 3-segment policy regex; every entry in
`applies_on_top_of` resolves to an existing skill in the consuming
library's `SNAPSHOT.lock`; `conventions` has ≥1 entry that's clearly
opinionated (the three diagnostic tests from `ARCHITECTURE.md`
§"Mechanism vs Policy" identify what's policy vs mechanism).

### Stage 2 — Delegate to skill-author

**Consumes:** `policy-intake.yaml`.

**Produces:** the policy SKILL.md authored via `skill-author` with a
pre-filled `intake.yaml` (archetype=`policy`, name from Stage 1,
purpose derived from conventions).

**Gate:** `validate-metadata.py` exits 0; the four required sections
for archetype=`policy` are present (Purpose, Applies On Top Of,
Conventions Enforced, Override Behavior).

### Stage 3 — Wire dependency

**Consumes:** the new SKILL.md + `SNAPSHOT.lock`.

**Produces:** an updated `SNAPSHOT.lock` entry for the policy with
`depends_on:` listing every mechanism skill from Stage 1 at its
current version.

**Gate:** the policy's `depends_on:` resolves; the consuming library's
`scripts/dependency-graph.py` shows the policy depending on the
named mechanisms (no orphans).

### Stage 4 — Override semantics check

**Consumes:** the new SKILL.md.

**Produces:** a verification that `## Override Behavior` names the
fail-loud mode explicitly. Per `ARCHITECTURE.md`: "if the mechanism
skill is uninstalled, the policy skill should fail loudly, not
silently substitute."

**Gate:** the section contains a fail-loud commitment (substring
match: "fail loudly", "fail loud", "raise an error", or equivalent).
If silent-substitution is intended (rare), the operator documents
the rationale explicitly.

## Dependencies

- `skill-author` — Stage 2 delegation.
- `scripts/validate-metadata.py` — Stage 2 gate.
- `scripts/dependency-graph.py` — Stage 3 verification.
- `ARCHITECTURE.md` §"Mechanism vs Policy" — the canonical
  composition rule.
- The consuming library's `SNAPSHOT.lock` — Stage 1 + Stage 3.

## Evaluation

`skill-policy-overlay` is correct when, run against a synthetic
intake (e.g., `house-git-conventions` overlaying `git-history-rewriting`
+ `git-collaboration`), the produced SKILL.md:

1. Passes `validate-metadata.py` exit 0.
2. Has the four policy archetype sections with substantive content.
3. Has a `depends_on:` in `SNAPSHOT.lock` listing both mechanism
   skills.
4. Names a fail-loud override behavior.
5. Does not re-explain mechanism (the conventions section is
   policy-only).

The first dogfood is whenever a consumer team authors their first
`house-*-conventions` skill. Until then, the tool is exercised
against synthetic fixtures.

## Handoffs

- **From `skill-refactor` Stage 4** — three-way refactor produces a
  policy slice; this tool authors it.
- **From the operator** — direct invocation when a team wants to
  encode conventions.
- **To `skill-author`** — Stage 2 delegates here.
- **To `skill-audit`** — the new policy is in scope for the next
  audit run.
