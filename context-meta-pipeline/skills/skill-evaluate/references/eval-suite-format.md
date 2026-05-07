# eval-suite-format.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

The eval suite at `scripts/tests/routing-eval.yaml` is the input
`skill-evaluate` consumes. Format documented here so consumer libraries
authoring their own `routing-eval.yaml` files can mirror it.

## Top-level shape

```yaml
version: 1
generated: "YYYY-MM-DD"
prompts:
  - prompt: "<natural-language input>"
    expected: <skill-name | none>
    source: held_out | in_distribution
    rationale: "<one-line: why this prompt should fire that skill>"
```

## Per-prompt fields

| Field | Required | Notes |
|---|---|---|
| `prompt` | yes | The exact text an operator might type. Not a paraphrase. |
| `expected` | yes | The skill that *should* fire. `none` is valid (true negative). |
| `source` | yes | `held_out` for never-seen-by-author prompts; `in_distribution` for prompts derived from existing test cases. |
| `rationale` | yes | One line explaining why this prompt was authored. Surfaced by `routing-eval-runner.py --verbose` on misses. |

## Coverage threshold

`audit-skill.py:gate_eval_coverage` (added v0.6.1) requires ≥3 positive
prompts per skill (configurable via `--eval-coverage-threshold`). If a skill
ships in SNAPSHOT.lock but has fewer than 3 positive prompts in
`routing-eval.yaml`, the gate fails.

A "positive prompt" is one where `expected: <skill-name>` (i.e., the prompt
is supposed to fire that skill). Prompts with `expected: none` are negative
prompts — they should NOT fire any skill — and don't count toward coverage.

## Author conventions

- Each skill should have ≥3 positive (held-out) prompts plus ≥2 negative
  prompts that nearly fire it.
- Negative prompts test anti-triggers: phrasings that *should not* fire the
  skill but might be misread.
- Rationale is for the audit operator, not the routing layer. Be specific:
  "Drift-gate language; should NOT fire skill-refactor" beats "negative case."

## Mode invariants

`routing-eval-runner.py` consumes this file in three modes:

- **static** — keyword-overlap heuristic over skill descriptions. v0.5.2
  added a 0.7× de-rank for routers; consumer libraries should preserve
  similar de-ranking when relevant.
- **operator** — interactive scoring. `--operator-transcript <path>` replays
  pre-canned answers (one line per prompt, in order).
- **external** — reads JSON list of `{prompt, actual}` from stdin or
  `--input <path>`. The production mode for real LLM-routing layers.

## What this skill does NOT validate

- Whether `description` text drifts from `body` content. That's
  `audit-skill.py` Gate 4 (drift), not eval-suite shape.
- Whether the eval-suite covers archetype-specific patterns (e.g., a
  router's ambiguous prompts). Coverage is per-skill, not per-archetype.
