# Library-shape gates

The four cross-skill consistency checks `library-audit` runs at
Stages 2–4. Each gate produces a pass/fail/N-A rollup that Stage 5
synthesizes.

## Gate L1 — per-skill health (delegated)

`audit-skill.py --all` runs Gates 1 (recency), 2 (test pass rate
— deferred), 3 (triggering accuracy — deferred), 4 (drift) per
`MAINTENANCE.md`. Library-audit's contribution: aggregate the
per-skill rollup into a per-library "all skills pass" / "N
skills flagged" headline.

## Gate L2 — coverage.md schema compliance

`coverage-check.py --file coverage.md --schema library` validates
the library-root coverage.md. Per-family coverage.md files (if
any) get the `--schema family` variant.

## Gate L3 — snapshot integrity

Three sub-checks on `SNAPSHOT.lock`:

- **Skill files exist**: every `path:` in the snapshot resolves
  to an actual SKILL.md.
- **`depends_on` resolves**: every `<skill>@<version>` pin
  references an existing skill at the pinned version.
- **No cycles**: the `depends_on` graph is a DAG.

`dependency-graph.py --format json` produces the input data;
library-audit interprets it.

## Gate L4 — version triangulation

Cross-check that `plugin.json` / `marketplace.json` (the
parent's relevant row) / `SNAPSHOT.lock snapshot_version` agree.
The same triangulation `verify.sh` step 4 does — library-audit
performs the same check independently rather than shelling
out to verify.sh.

## What gates DON'T do

- Don't *fix* anything — gates surface state. Fixes happen in
  `skill-author` / `skill-refactor` / `skill-retire` / direct edits.
- Don't enforce per-skill content rules beyond what audit-skill
  delegates — content validation is `validate-metadata.py`'s job.
- Don't run integration tests (Gate 2 is deferred per
  `governance/INTEGRATION-TESTING.md` until 10+ cross-dep skills exist).
