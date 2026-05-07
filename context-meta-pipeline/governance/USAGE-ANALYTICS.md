# Usage Analytics

**Build trigger:** library has 25+ skills and you can't tell from
inspection which are load-bearing versus which are unused.

**Pre-trigger applicability:** *None.* The library has 14 skills as
of v0.5.0 — every one is identifiable by inspection. Telemetry isn't
needed at this scale and would be expensive to build.

---

## What usage analytics covers

Three questions:

1. **Which skills are actually invoked?** (Activation rate.)
2. **Which skills have never been invoked?** (Dead code.)
3. **Which skills are invoked together?** (Composition / handoff
   patterns the architecture didn't predict.)

Analytics produce data; humans interpret. Dead code may or may not
mean "retire"; co-invocation may or may not suggest a new
orchestrator. The data feeds judgment, not automated retirement.

## Mechanism (when implemented)

Per-skill telemetry hooks at three points:

1. **Skill load** — record `(skill_name, version, timestamp)`.
2. **Skill activation** — record `(skill_name, prompt_hash,
   timestamp)`. Prompt content is NOT recorded (privacy +
   compliance); the hash identifies "same prompt routed twice"
   without preserving content.
3. **Skill handoff** — when one skill names another in its
   `## Handoffs` and the operator follows the handoff, record
   `(from, to, timestamp)`.

Data lands in append-only logs at
`scripts/tests/analytics/<date>.jsonl` (deferred path; not yet
defined). A `scripts/analytics-rollup.py` (deferred) aggregates
into:

- Per-skill activation count over the last 30 / 90 / 365 days
- Co-invocation matrix (which skills fire in the same operator
  session)
- Trend lines (rising / falling activation per skill)

## What the rollup informs

- **Retire candidates** — skills with zero activations over 12
  months. Hand off to `skill-retire` with reason `domain-gone` or
  `health-failure`.
- **Refactor candidates** — skills with consistent co-invocation
  but separate identities. Hand off to `skill-refactor` for a
  potential merge or new orchestrator.
- **Investment candidates** — skills with high activation but
  failing health gates. Prioritize for hand-authored fixes.
- **Coverage gaps** — prompt-hashes that hit no skill (the
  `meta` router fell back to `none`). Suggest a new family or a
  description-tightening pass.

## Privacy + scope

- Prompt content is never recorded. Only hashes (collision
  acceptance: SHA-256 truncated to 64 bits is fine for
  aggregation purposes).
- Per-operator identity is not recorded (the meta-pipeline is
  internal; cross-operator deduplication is not a goal).
- Telemetry is opt-in per operator via a `~/.claude/analytics.yaml`
  configuration (deferred). Default: off.

When the library has external consumers, the privacy posture
tightens further — see `governance/SECURITY-AUDIT.md` for the
overlap.

## Pre-trigger alternative

Until 25+ skills exist, "which are load-bearing?" is answerable by
inspection:

- Read `SNAPSHOT.lock` `depends_on:` — load-bearing skills are
  named there.
- Read `coverage.md` "Coverage Matrix Status" — skills not flagged
  Health are presumed used.
- Read `CHANGELOG.md` — skills mentioned in Changed / Health
  entries are active.
- Run `audit-skill.py --all` — recency gate identifies abandoned
  skills.

These cover the pre-trigger case adequately.

## Implementation

When the trigger fires:

1. `scripts/telemetry-hook.py` is authored — writes JSONL events.
2. Skill load / activation / handoff events get hooks (probably
   via Claude Code's load-time mechanism — this is partly
   blocked on Claude Code core support).
3. `scripts/analytics-rollup.py` consumes the JSONL and produces
   per-skill summaries.
4. The output integrates with `library-audit` Stage 5 as a
   secondary signal alongside the four health gates.

## Cross-references

- `MAINTENANCE.md` §"Health Threshold Gates" — analytics is a
  *fifth* signal beyond the four gates, not a replacement.
- `coverage.md` Domains Deferred — currently lists this as a
  deferred concern.
- `governance/SECURITY-AUDIT.md` — analytics intersects with audit
  trails (when consumer libraries care about both).
- `skills/skill-retire/SKILL.md` — analytics-driven retirement
  flows through this skill.

## Out of scope

- Public-facing usage dashboards (operator-side concern).
- Performance / latency telemetry (separate from "which skills
  fire").
- Cross-library analytics (depends on a marketplace that
  aggregates — out of scope per
  `governance/INDEX.md` §"Skill marketplace mechanics").
