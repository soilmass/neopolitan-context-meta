# threshold-rationale.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

`skill-evaluate` reports per-skill triggering accuracy and compares against
a threshold. This document explains where the thresholds come from and when
to adjust them.

## Default thresholds

| Threshold | Default | Source |
|---|---|---|
| Triggering accuracy gate (Gate 3) | ≥85% | `governance/MAINTENANCE.md` §"Health Threshold Gates" |
| Eval-suite coverage gate (Gate 5, v0.6.1) | ≥3 positive prompts per skill | `scripts/audit-skill.py:gate_eval_coverage` default |

## Why 85% for triggering accuracy

The 85% bar comes from `MAINTENANCE.md` and is calibrated for the static
keyword-overlap heuristic in `routing-eval-runner.py --mode static`. Real
LLM-routing layers (when they exist) typically score higher; treat 85% as a
floor, not a target.

If a consumer library's static-mode accuracy drops below 85%:
- (most common) anti-triggers are missing from one or more skills'
  descriptions. Run `skill-audit` Stage 4 and look for drift.
- (less common) the eval suite has prompts that the static heuristic
  *cannot* solve (e.g., they require semantic context the keyword overlap
  doesn't capture). Either add anti-triggers to make the static path work,
  or accept that static mode is approximate.

If a consumer library's external-mode (real-routing) accuracy drops below
85%:
- this is a real signal; investigate per skill.

## Why 3 prompts for eval-coverage

The 3-prompt minimum is a v0.6.1 design decision based on 14 skills × the
desire for ≥30 prompts in the suite at all times. Consumer libraries with
larger skill sets may want to raise this — `--eval-coverage-threshold 5`
is a reasonable target for libraries with 25+ skills.

3 prompts is the minimum to surface description drift: with 1-2 prompts a
skill could pass triggering accuracy by accident. 3+ prompts means the
heuristic has to actually understand the description's anti-trigger
discipline.

## When to override thresholds

- **Lower (e.g., 70%)**: during a known-bad period (just after a major
  refactor; before anti-triggers have been re-added). Document why the
  threshold is temporarily lower in the next CHANGELOG entry.
- **Higher (e.g., 95%)**: when the consumer library has shipped its second
  or third release without any routing regression. Demonstrate stability,
  then raise the bar.

Both adjustments go through the same channel: edit
`scripts/tests/routing-eval.yaml`'s `version:` field and document the
rationale in CHANGELOG.md.
