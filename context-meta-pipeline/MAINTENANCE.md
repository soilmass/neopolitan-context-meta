# Maintenance

How the library handles ownership, health, and unmaintained skills. Specifies the threshold-gate health system, the auto-warn mechanism, and what happens when skills decay.

---

## Implicit Ownership

The library does not maintain a CODEOWNERS file or a maintainers registry. Whoever last touched a skill is implicitly responsible for it.

This is a deliberate simplification. The cost is that long-unmaintained skills have no formal owner. The benefit is no bureaucratic overhead — no maintainer-rotation cycles, no escalation paths, no abandonment notices.

When a skill needs work and no one steps up, the skill becomes unhealthy under the threshold-gate system below. The auto-warn mechanism communicates the staleness; users decide whether to keep using the skill, switch to an alternative, or contribute a fix.

---

## Health Threshold Gates

Every skill is checked against four signals. The skill is healthy only if all four pass.

### Gate 1: Recency

**Threshold:** Last update less than 6 months ago.

A skill that has not been touched in 6 months is flagged. The signal does not distinguish between "stable and complete" and "abandoned" — it cannot, from commit dates alone. A skill that is genuinely complete and stable still flags after 6 months; the auto-warn mechanism allows the maintainer to acknowledge this and pin the recency signal as "stable" for another 6 months.

### Gate 2: Test pass rate

**Threshold:** Test pass rate above 90%.

Every skill has an evaluation suite (per `/ARCHITECTURE.md`). The suite runs on a schedule (typically nightly or weekly) and produces a pass rate. Skills with pass rates below 90% are flagged.

The 90% threshold is calibrated for skills with reasonably-sized test suites (10+ assertions). Skills with very few tests can fail this gate from a single regression; the gate is designed to flag this as a structural problem.

### Gate 3: Triggering accuracy

**Threshold:** Triggering accuracy above 85%.

Routing accuracy is measured by the held-out test selection in the description optimizer (specified in `/governance/INDEX.md` as a deferred document). The measurement asks: when prompts that should hit this skill are presented, how often does the skill actually fire?

Below 85% means the skill is competing with siblings for routing or has a description that doesn't match how users actually phrase prompts. Either is a signal the skill needs description-level work.

### Gate 4: Description drift

**Threshold:** Description drift below 10%.

Description drift is the gap between what the skill's description claims and what the skill actually does. Concretely: the description's stated capabilities versus the capabilities present anywhere in the skill's body.

The exact formula (asymmetric containment with prefix-based token matching) is pinned in `skills/skill-audit/references/health-gates.md` and implemented in `scripts/audit-skill.py` as of v0.2.0. The asymmetric measure asks "does the description claim things the body doesn't deliver?" — a body that goes deeper than the description summarizes does not flag.

The threshold is generous because perfect alignment is impractical — descriptions are compressed; bodies are detailed.

---

## Auto-Warn Mechanism

When a skill fails any threshold gate, its description gets a warning banner that loads with the skill.

```
⚠️ Health Check Failing
Test pass rate: 78% (threshold: >90%)
Last update: 8 months ago (threshold: <6 months)
Triggering accuracy: 91% ✓
Description drift: 4% ✓
```

In v0.2.x, the banner is *generated* by `scripts/audit-skill.py` (or by the `skill-audit` Stage 5 procedure) and the operator applies it to the skill's description on the next release. Auto-prepending at load time is a future enhancement that will require a load-time hook in Claude Code itself; until then, the audit-and-apply loop is a periodic operator action driven by the cadence below.

The banner is not a hard block. The skill still functions. But the warning is visible enough that users have to consciously continue using a flagged skill rather than passively accepting that nothing is wrong.

When the failing signals are corrected (a release fixes the test failures, the description is updated, a touch refreshes the recency clock), the banner disappears on the next health check run.

---

## Unmaintained Skills

A skill that fails health checks and is not addressed remains in the library indefinitely.

The library does not:

- Archive unmaintained skills to a separate folder.
- Remove unmaintained skills from the marketplace.
- Auto-update unmaintained skills via bots.
- Send maintenance reminders to past contributors.
- Issue sunset notices.

A skill that has been failing health checks for two years simply has a banner that has been visible for two years. Users who keep using it have implicitly accepted the staleness. Users who don't, don't.

This is consistent with the latest-only support model. The library does not commit to maintaining anything; it commits to making the state of every skill visible.

---

## When a Skill Needs Work

If a skill is failing health checks and someone wants to fix it, no permission is required. Whoever submits a PR becomes the new implicit owner. The expected workflow:

1. Identify what's failing (one or more of the four gates).
2. Address the failures (update tests, refresh the description, ship a patch).
3. The PR runs metadata validation, breaking-change detection, and the test suite.
4. On merge, the health checks re-run and clear the banner if all gates pass.

There is no formal handoff between owners. The git history records who did what; the implicit-ownership model treats the most recent contributor as the current responsible party.

---

## Health Check Cadence

The health check runs on a schedule. Recommended cadence:

- **Recency gate** *(implementable; mechanized in v0.2.0 via `audit-skill.py`)*: at every CI run on the skill (or on demand via `audit-skill.py`).
- **Test pass rate** *(specified in `governance/INTEGRATION-TESTING.md` from v0.5.0; pre-trigger N/A)*: measured on every test suite run once 10+ skills with cross-deps + 2 cross-skill regressions establish the trigger. The doc specifies the procedure; the runner ships when needed.
- **Triggering accuracy** *(specified in `governance/SKILL-DISCOVERABILITY.md` from v0.5.0; pre-trigger N/A)*: mechanized in v0.5.0 via `scripts/routing-eval-runner.py` + the `skill-evaluate` skill. Real (machine-graded) results require a live routing layer; static / operator / external modes work today but produce approximate numbers.
- **Description drift** *(implementable; mechanized in v0.2.0 via `audit-skill.py`)*: at every PR that modifies a skill, plus a periodic full-library audit. Run via `audit-skill.py --all` or `verify.sh`.

The banner reflects the most recent values from each signal. A skill that just shipped a fix clears the recency banner immediately on the next `audit-skill.py` run; the deferred gates won't refresh until their underlying infrastructure lands.

---

## What This Document Does Not Cover

- Specific evaluation suite formats: see `/ARCHITECTURE.md` and `/governance/INDEX.md` (deferred — INTEGRATION-TESTING.md).
- Routing-eval runner implementation: deferred per `/coverage.md` §"Domains Deferred" under `skill-evaluate`. The starter input format ships at `scripts/tests/routing-eval.yaml`; the runner that scores prompts against the live routing layer is the missing piece.
- Drift formula details: see `/skills/skill-audit/references/health-gates.md` Gate 4 for the asymmetric containment formula.
- Rollback when a "fix" makes things worse: see `/governance/ROLLBACK-PROCEDURE.md`.
- Versioning rules for health-driven changes: see `/VERSIONING-POLICY.md`.
