# Path to v1.0

The library is at v0.6.0 — feature-complete for skill-governance
self-administration but not yet at a 1.0 promise. This doc names the
**seven prerequisites** for v1.0, each with a build trigger that
indicates the work is ready to start.

**Why v1.0 matters.** The v0.x series allows MINOR bumps to break
*interpretation* (e.g., what a gate threshold means), even if the
schema stays the same. v1.0 locks the interpretation. Consumers
authoring against v1.0 know that the meta-pipeline will not silently
shift the meaning of a `depends_on:` pin or a `recency_pin: stable`
marker between MINOR releases.

**Format.** Each prerequisite has:
- **Trigger** — observable signal that the work is ready to start
- **Current state** — what exists today
- **Blocking item** — what's missing
- **Exit criterion** — how we know the prerequisite is satisfied

---

## P1. Gate 2 mechanizer (test pass rate)

The fourth health gate's *test pass rate* check is currently explicit
N/A pending `governance/INTEGRATION-TESTING.md` →
`scripts/integration-test.py`.

**Trigger.** ≥10 skills declare `depends_on:` in `SNAPSHOT.lock`
(cross-skill dependency density passes the threshold) **OR** two
regressions in three months slip through because tests don't exist.
Per `governance/INDEX.md` →`INTEGRATION-TESTING.md` row.

**Current state.** Doc shipped in v0.5.0; mechanizer not authored.
Audit reports `test_pass_rate: "N/A — INTEGRATION-TESTING.md
deferred"`.

**Blocking item.** Authoring a runner that takes a SKILL.md +
test-suite-path and emits pass-rate. Format and discipline questions
mostly settled in `INTEGRATION-TESTING.md`; runner authoring deferred.

**Exit criterion.** `gate_test_pass_rate()` in `audit-skill.py` reports
a real percentage. The threshold (probably ≥85%) is committed in
`governance/MAINTENANCE.md`.

---

## P2. Gate 3 mechanizer with real routing layer

The fourth health gate's *triggering accuracy* check is currently
deferred pending the routing layer being addressable from outside Claude
Code's normal load path.

**Trigger.** ≥25 skills exist in the library **OR** first description-
change regression slips through. (Per `coverage.md` `skill-evaluate`
deferred row.)

**Current state.** A starter `routing-eval.yaml` ships in v0.2.0;
extended in v0.5.2 to cover the v0.5.0 cluster. Static keyword-overlap
heuristic exists as a coarse pre-screen.

**Blocking item.** Real routing layer (LLM-based) requires either:
- Claude Code load-time hooks that expose "which skill fired" per
  prompt, or
- An external runner that issues sub-Claude requests and parses the
  routed-skill name from the response.

The static heuristic is not the production path; it surfaces gross
mis-routing only.

**Exit criterion.** `routing-eval-runner.py --mode external` consumes
real routing-layer responses and `gate_triggering_accuracy()` reports
a real percentage per skill. The threshold (probably ≥85%) committed.

---

## P3. ≥50 skills — meta-router threshold

ARCHITECTURE.md §"Cross-Cluster Meta-Router" notes that at sufficient
library scale, the single-tier router pattern starts to fail (a router
that lists all skills is just a flat list). The meta-router pattern
adds a second tier.

**Trigger.** Library reaches ≥50 skills total (across all consumer
libraries) **OR** the static-routing heuristic accuracy drops below
60% on the held-out suite.

**Current state.** 14 skills (this library is the 1st). The
meta-pipeline itself isn't a "consumer library"; it's the lifecycle
substrate. Real consumer libraries (the 2nd, 3rd, …) bring the count
up.

**Blocking item.** No real consumer library exists yet.

**Exit criterion.** ≥1 cross-cluster meta-router authored against a
documented procedure. v0.5.0 introduced the `meta` per-cluster router;
v1.0 needs at least one *cross*-cluster instance.

---

## P4. Multi-tier policy composition

`ARCHITECTURE.md` §"Policy Overlay Composition" specs single-tier
overlays (`house-postgres-conventions` over `postgres-history-rewriting`).
Multi-tier (`acme-base` + `acme-frontend` overrides on the same
mechanism) is documented as deferred.

**Trigger.** ≥2 tiers of `house-*` overlays exist on the same
mechanism atom in any consumer library.

**Current state.** Zero policy overlays exist (the v0.5.2 dogfood
walkthrough used an *invented* overlay; nothing real shipped).

**Blocking item.** Real consumer library authoring policy overlays.

**Exit criterion.** `skill-policy-overlay` Stage 6 (or new) handles the
multi-tier merge order; `MAINTENANCE.md` documents the composition rule.

---

## P5. Provenance layer

`governance/SKILL-PROVENANCE.md` is shipped with explicit pre-trigger
N/A. Skills are not currently signed; consumers cannot verify
authorship.

**Trigger.** External distribution begins (the marketplace serves
skills to people who didn't author them) **OR** the first reproducible-
behavior bug requires provenance to triage.

**Current state.** Doc shipped in v0.5.0; no signing infrastructure.

**Blocking item.** Decision on signing scheme (sigstore? plain GPG?
content-addressed?). Once decided, mechanizer in `scripts/`.

**Exit criterion.** `validate-metadata.py` checks provenance signatures
when present; `coverage.md` consumer-library row records provenance
posture.

---

## P6. First real consumer library completes a full lifecycle

The meta-pipeline has been validated against itself (every lifecycle
skill walked end-to-end as in-memory dogfood at v0.5.2). It has not yet
been validated against an *external* library that exercises every
lifecycle stage.

**Trigger.** ≥1 consumer library exists, has authored ≥3 skills, has
audited the library, has refactored at least one skill, and has retired
at least one skill.

**Current state.** Zero consumer libraries.

**Blocking item.** No real consumer.

**Exit criterion.** A full lifecycle pass — `library-bootstrap` →
`family-bootstrap` → `skill-author` × N → `skill-audit` →
`skill-refactor` → `skill-retire` — completes without surfacing a
structural bug. Findings beyond doc clarifications are PATCH bumps in
the meta-pipeline; if any require a MAJOR bump in the meta-pipeline,
v1.0 is held until that lands.

---

## P7. v1.0 lock-in

When P1-P6 are satisfied, the v1.0 release **freezes** the load-bearing
schemas:

- `ARCHITECTURE.md` §"The Five Archetypes" — exact archetype names + counts
- Frontmatter schema — exact required-key list
- `SNAPSHOT.lock` schema — exact key set
- Naming conventions — exact regex
- The six artifact contracts in `governance/EXTENSION-POINTS.md` §5

**Exit criterion.** The library MAJOR-bumps to v1.0.0 and ships a
`MIGRATION-v1.md` authored via `skill-migrate` documenting every change
since v0.6.0. After v1.0, schema changes are MAJOR-bump library
changes (v2.0); field additions are MINOR; field clarifications are
PATCH.

---

## What's intentionally NOT a v1.0 prerequisite

- **A 6th archetype.** Per `governance/EXTENSION-POINTS.md` §4, this is
  out-of-scope and would itself be a MAJOR-bump library change. Adding
  one *during* the v1.0 path makes the lock-in moot.
- **Performance / latency targets.** No signal that's load-bearing.
- **A formal grammar for SKILL.md descriptions.** The 1024-char +
  third-person + `Do NOT use for` discipline has worked through 14
  skills + 21 + 13 audit findings; the description format is healthy
  without a formal grammar.
- **A second consumer library beyond P6.** P6 only requires *one*; the
  Nth-consumer-library threshold is a separate growth signal, not a
  v1.0 prerequisite.
- **Multi-marketplace federation.** Out of scope per `coverage.md`.

---

## Estimated timeline

Each prerequisite gates on real-world signal, not calendar time. The
build triggers are observable. v1.0 ships when:
- All seven exits are reached, AND
- A 30-day stability window has passed with no MAJOR bumps, AND
- The audit ritual against the meta-pipeline returns zero findings
  for three consecutive runs.

Probable shape: P1, P2, P5 are mostly authoring work that lands
incrementally as consumer libraries push for them. P3, P4, P6 wait
on consumer libraries to exist. P7 is the closing ritual.

**Best case:** v1.0 in 6 months if a real consumer dogfood starts now.
**Worst case:** v1.0 in 18+ months if the meta-pipeline only ever has
one consumer (itself).
