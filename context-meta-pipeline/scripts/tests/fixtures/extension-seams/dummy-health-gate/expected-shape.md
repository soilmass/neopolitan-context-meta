# expected-shape.md — extension-seam fixture for §3 (new health gates)

Per `governance/EXTENSION-POINTS.md` §3, new health gates extend
`scripts/audit-skill.py` by adding a `gate_<name>()` function. The
existing four gates (`gate_recency`, `gate_drift`, `gate_test_pass_rate`,
`gate_triggering_accuracy`) take varied arguments depending on what the
gate observes — there is no single fixed signature. The contract is at
the *return-type and naming* level:

| Check | Required |
|-------|----------|
| Function name | matches `^gate_[a-z_]+$` |
| Return annotation | `GateResult` |
| Has a docstring | required |

verify.sh step 9 ast-parses `audit-skill.py` and confirms every
top-level function whose name starts with `gate_` satisfies these three
checks. If any existing `gate_*` function violates them, verify.sh step
9 fails. If a future PR adds a new gate, that PR is responsible for
following the contract — and step 9 confirms it does.

## Why argument shape is NOT in the contract

The four existing gates have these signatures:

| Gate | Signature |
|------|-----------|
| `gate_recency` | `(skill_dir: Path, fm: dict, threshold_months: int)` |
| `gate_drift` | `(fm: dict, body: str, archetype: str \| None = None)` |
| `gate_test_pass_rate` | `()` (no args; reports N/A pending mechanizer) |
| `gate_triggering_accuracy` | `(skill_name: str, eval_path: Path \| None)` |

A 5th gate's input depends on what it observes. Forcing a uniform
signature would either bloat every gate's arg list (so
`gate_test_pass_rate` would have to accept `skill_dir`, `fm`, `body`
even though it ignores them) or hide the gate's data dependency. The
audit-runner's gate-dispatch loop knows each gate's specific call
shape; that knowledge is local to `run_gates()` in `audit-skill.py`.

## Why `GateResult` IS in the contract

Every gate must return a `GateResult` so the per-skill rollup can
iterate over results uniformly. A gate returning `bool` or `int`
breaks the rollup formatter. The seam-test catches this if a future
gate forgets the type.

## What this fixture does NOT prove

- That a new gate's *threshold* is well-chosen. Threshold authoring
  is a `MAINTENANCE.md` discipline, not a code-shape check.
- That a new gate is *implementable*. Gates 2 and 3 are deferred
  per `coverage.md`; the shape contract permits deferred-N/A gates.
- That the gate's `observable` value is well-defined. That's a
  `health-gates.md` discipline.

## What this fixture DOES prove

- A future PR cannot add a `gate_<name>()` returning `bool` and
  expect the audit-rollup to render it.
- A future PR cannot add a `gate_<name>()` without a docstring and
  expect the auto-generated audit-finding ledger to describe it.
- The naming convention `gate_<name>` is enforceable, not aspirational.
