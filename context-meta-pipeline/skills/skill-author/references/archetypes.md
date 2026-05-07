# Archetype Rubrics

Required sections per archetype. The `validate-metadata.py` script enforces
these literally; this document explains the *intent* of each section so
authors know what to put in them.

The five archetypes (per `ARCHITECTURE.md` §"Skill Archetypes") are:
**Atom**, **Tool**, **Router**, **Orchestrator**, **Policy**.

A skill is exactly one archetype. If it feels like two, it's two skills.

> **Source of truth.** When this document and `governance/METADATA-VALIDATION.md`
> disagree, **`METADATA-VALIDATION.md` is canonical** — it is the document
> the validators are written against and the document `BREAKING-CHANGE-DETECTION.md`
> cross-references. This rubric is illustrative: it explains the intent of
> each required section so an author can write substantive content, but the
> definitive list of required sections per archetype lives in
> `METADATA-VALIDATION.md` §"Archetype-Specific Required Sections". (Audit
> finding A12 from the v0.4.0 dogfood.)

---

## Atom

A single capability in a narrow domain. Unix analog: `cat`, `wc`, `grep`.

### Required sections

| Section | Intent |
|---|---|
| `## When to Use` | Concrete conditions that should trigger this atom. |
| `## When NOT to Use` | Sibling fences — name skills that are NOT this one. |
| `## Capabilities Owned` | Bullet list of the specific operations this atom performs. The breaking-change detector compares this list across versions. |
| `## Handoffs to Other Skills` | Names the siblings this atom delegates to. |
| `## Edge Cases` | Hostile inputs, empty inputs, and failure modes. |
| `## References` | Pointers to the atom's `references/*.md`. |

### Recommended (warnings only)

- `## Anti-Patterns` — named patterns that should route elsewhere.
- `## Examples` — worked examples for the most common usage.

---

## Tool

One workflow producing one named output. Unix analog: shell utilities,
language compilers.

### Required sections

| Section | Intent |
|---|---|
| `## Purpose` | One-paragraph statement of what the tool produces. |
| `## When to Use` | Triggers. |
| `## When NOT to Use` | What this tool will not do. |
| `## Stage-Gated Procedure` | The named stages, what each consumes and produces, and the gate before the next stage. |
| `## Dependencies` | What other skills, scripts, or files this tool reads or invokes. |
| `## Evaluation` | How to verify the tool is working — typically a list of properties the output must satisfy across N worked examples. |
| `## Handoffs` | Where the output flows to next. |

### Recommended (warnings only)

- `## Self-Audit` — checks the tool runs against itself.
- `## Edge Cases`.

---

## Router

Dispatches to other skills. No domain knowledge of its own. Bare-domain
mental-model name (`git`, `kubectl`, `postgres`, never suffixed).

### Required sections

| Section | Intent |
|---|---|
| `## When to Use` | When the prompt names the domain but no specific atom. |
| `## When NOT to Use` | Out-of-scope prompts; sibling-router boundaries. |
| `## Routing Table` | Markdown table: `Intent → Target atom`. The breaking-change detector compares this table across versions. |
| `## Disambiguation Protocol` | How to handle ambiguous prompts that could match two atoms. |
| `## Atoms in This Family` | The dispatch targets, named explicitly. |

### Recommended (warnings only)

- `## Non-Negotiable Rules` — when the router has invariants like "do not answer domain questions yourself."
- `## Edge Cases`.
- `## Self-Audit`.

Note: anti-triggers live in the frontmatter `description` (per
`METADATA-VALIDATION.md`), not in a separate body section.

---

## Orchestrator

Coordinates multiple skills through a multi-stage workflow. Unix analog:
shell scripts, `make`.

### Required sections

| Section | Intent |
|---|---|
| `## Purpose` | One paragraph — the multi-skill workflow this orchestrates. |
| `## When to Use` | Triggers. |
| `## When NOT to Use` | When a single skill suffices. |
| `## The Stages` | The named stages, what each consumes and produces, gate per stage, and which sub-skill is invoked. |
| `## Skills Coordinated` | The skills this orchestrator calls, by name. |
| `## Failure Modes` | What happens when a sub-skill fails — halt? rollback? retry? |
| `## Handoffs` | Where the orchestrator's output flows to next. |

---

## Policy

Conventions and team-specific opinions overlaid on a mechanism skill.
Three-segment name: `<context>-<domain>-<aspect>` (e.g., `house-git-conventions`).

### Required sections

| Section | Intent |
|---|---|
| `## Purpose` | What the overlay enforces. |
| `## Applies On Top Of` | Which mechanism skill this overlays. If that skill is uninstalled, this overlay should fail loudly. |
| `## Conventions Enforced` | The team-specific rules. |
| `## Override Behavior` | What the policy overrides in the underlying mechanism. |

---

## Choosing the right archetype

Per `ARCHITECTURE.md` §"Skill Archetypes", a skill is *exactly one* of
these. The diagnostic test: write the skill's purpose as a sentence with
verbs. If you write "X **and** Y" with two distinct verbs, the skill is
two skills.

Common confusions:

- **Tool vs Atom.** Atoms are domain capabilities; tools are workflows
  that may compose atoms. If your skill has stages, it's a tool. If it
  performs one operation, it's an atom.
- **Tool vs Orchestrator.** Tools call atoms (one or many) within a single
  workflow producing one output. Orchestrators call multiple *tools* or
  multiple skills across stages where the output is multi-artifact.
- **Atom vs Router.** Atoms perform; routers dispatch. A router is named
  for the domain (`git`); atoms are named for the failure mode within the
  domain (`git-history-rewriting`).
- **Mechanism atom vs Policy overlay.** A mechanism atom describes domain
  reality and ports across teams unchanged. A policy overlay carries
  team-specific opinions and references the mechanism. If the skill makes
  best-practice claims, it's a policy.
