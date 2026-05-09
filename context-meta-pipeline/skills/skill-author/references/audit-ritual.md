# The Audit Ritual

Stage 2 of `skill-author` (and Stage 5 of `family-bootstrap`) implements
this procedure from `ARCHITECTURE.md` §"Routing and Contention".

It catches roughly 80% of routing-contention problems pre-merge for
near-zero cost.

> **Note on the `audit-report.md` artifact.** It is ephemeral — a
> planning document the operator works through during Stage 2. It is
> not committed to the repo; the only persistent outputs of the ritual
> are anti-trigger updates applied to sibling skills' descriptions
> (which land via the normal Stage 4 commit) and any "no contention"
> notes that the operator chooses to keep in their PR description.

## Procedure

### Step 1: List the three nearest siblings

Take the proposed skill's name and one-sentence purpose. Read the
`description` field of every existing skill in `SNAPSHOT.lock`. Rank by
description-keyword overlap. Pick the top three.

If fewer than three skills overlap meaningfully, the proposed skill is
in a clean corner of the description space — record this and continue.

### Step 2: Generate five ambiguous prompts

Write five prompts that *could plausibly* hit either the new skill or any
of the top-three siblings. Aim for prompts the operator would actually
say, not synthetic ones. Avoid prompts that are obviously about one
specific skill — those don't test routing.

Examples for `skill-author` against `family-bootstrap`:

> "I want to add a new skill for parsing HTML metadata."
>
> *(Could route to skill-author or family-bootstrap; the prompt
> doesn't say whether HTML metadata is one skill or a whole family.)*

> "Make a new skill that wraps git rebase."
>
> *(Should route to skill-author — it's one skill, not a family.)*

### Step 3: Predict and verify

For each prompt, predict which skill the LLM should route to. The
prediction is yours; the LLM may disagree.

Then run the prompts (or simulate by reading descriptions and judging).
Note where actual routing diverges from your prediction.

For routing failures: the cause is one of three:
- The new skill's description matches too widely (narrow it).
- A sibling's description is too broad (sibling needs an anti-trigger).
- The prompts are genuinely ambiguous (clarify the domain split or
  combine the skills).

### Step 4: Add anti-triggers to siblings

For each sibling that competed for any of the five prompts, add a
specific anti-trigger to that sibling's `description` field naming the
new skill. Example:

> "…[existing description]… Do NOT use for: authoring a single new
> SKILL.md (use `skill-author`)…"

The anti-trigger:
- Names the new skill explicitly.
- Says what the new skill does, not what this skill doesn't do.
- Is short — one phrase, not a paragraph.

These edits to siblings are part of the lock-step changes for the new
skill's PR. They go into the same change set.

### Step 5: Document no-contention cases

For siblings that did NOT compete on any of the five prompts, write a
one-line "no contention" note in `audit-report.md` explaining why. The
goal is to make the audit *legible* — a future reader of the PR should
see what was checked, not just what was changed.

## Output: audit-report.md

```markdown
# Audit Report — <new-skill-name>

## Top 3 Siblings by Description Overlap

1. `<sibling-1>` — overlaps on "<keywords>"
2. `<sibling-2>` — overlaps on "<keywords>"
3. `<sibling-3>` — overlaps on "<keywords>"

## Ambiguous Prompts

| # | Prompt | Predicted target | Actual / inspected |
|---|---|---|---|
| 1 | "..." | `<new-skill>` | `<actual>` |
| 2 | "..." | `<sibling-1>` | `<actual>` |
| ... | | | |

## Resolution Per Sibling

- `<sibling-1>` — Anti-trigger to add: "Do NOT use for: …"
- `<sibling-2>` — No contention (descriptions are already disjoint
  because…)
- `<sibling-3>` — Anti-trigger to add: …

## Sibling Anti-Trigger Updates Queued for This PR

(Listed for the operator to apply in Stage 4 alongside the new skill.)
```

## Gate

Stage 2 passes only when every contended sibling has either:
1. A queued anti-trigger update *applied* in Stage 4, OR
2. A written no-contention justification in this report.

No sibling is silently left as a routing competitor. That's the whole
point of the ritual.

## Common drift signals on fresh atoms

Surfaced by audit finding A60 (2026-05-08 first real-consumer dogfood
of `family-bootstrap` against the `context-site-build` library — 4 of
7 freshly-authored atoms failed the description-drift gate on first
audit).

Drift = description tokens that don't appear in the body. Common
offenders on fresh atoms:

- **Phase-name suffixes** ("kickoff", "during Phase X start"). The
  body usually says "Phase 1 Discovery" or "the project starts"; the
  description grabs a more colloquial form.
- **Temporal hedges** ("around T+8 weeks", "after stabilization
  completes"). Bodies use precise forms; descriptions use approximate
  ones.
- **Verb form mismatches** ("Writes" in description / "Write" or
  "writes the artifact" in body). Tokenizer treats different forms
  as different stems.
- **Abstract framing** ("the artifact that **sets** why the project
  exists, **who** it serves"). Bodies use concrete operations
  ("compose a one-paragraph statement"). Description's "set / who /
  why / how" become drift tokens.
- **Filler structure words** ("structured", "around", "during"). They
  read smoothly in descriptions but rarely echo in bodies.

**The fix is almost always to tighten the description**, not to
inflate the body. Descriptions should use the same vocabulary as the
body (`compose`, `assign`, `aggregate`, `cite`) rather than abstract
synonyms (`set`, `make`, `cover`, `handle`).

If a fresh family produces N atoms and >50% fail the drift gate, the
issue is usually a shared abstract-description-template that diverges
from each atom's concrete body. Iterate on descriptions individually;
the gate will pass after one or two passes.

This pattern was first observed in the v0.4.0 family-bootstrap
dogfood ("8 of 9 freshly-bootstrapped skills failed the drift gate
immediately"), motivating the Stage 6 advisory audit. The v0.7.x
context-site-build dogfood reproduced it. The audit-at-Stage-6
design is correct; this subsection is the operator's first-aid kit.

## Scaling notes

Per `ARCHITECTURE.md` §"Routing and Contention":

- 0–10 skills in the library: this ritual is the only routing safeguard.
- 10–25 skills: this ritual remains the safeguard. Run on every new skill.
- 25–50 skills: add per-domain routers for clusters of 5+ atoms.
- 50+ skills: build a held-out routing eval suite (the deferred
  `skill-evaluate` skill — see library-root `coverage.md`).

The ritual continues to apply at every scale. The eval suite supplements
it; it does not replace it.
