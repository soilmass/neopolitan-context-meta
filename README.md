# neopolitan-context-meta

Claude Code marketplace hosting the `context-meta-pipeline` plugin — the
skill-lifecycle meta-pipeline (skills that govern other skills).

## Layout

```
.claude-plugin/
  marketplace.json          ← marketplace manifest

context-meta-pipeline/
  .claude-plugin/
    plugin.json             ← plugin manifest
  ARCHITECTURE.md           ← system design + extension points
  CHANGELOG.md              ← cross-skill changelog
  GOVERNANCE.md             ← ownership, dependencies, lock-step upgrades
  INDEX.md                  ← generated index of all skills (v0.7.0+)
  MAINTENANCE.md            ← health gates, audit cadence
  SNAPSHOT.lock             ← canonical skill register
  VERSIONING-POLICY.md      ← SemVer rules
  coverage.md               ← in-scope / specced / deferred / out-of-scope
  docs/PATH-TO-V1.md        ← prerequisites for v1.0
  governance/               ← 11 governance docs (3 load-bearing + 8 specified)
  scripts/                  ← 18 Python validators + 1 shared helper
  skills/                   ← 14 skills across lifecycle / library / composition
  verify.sh                 ← one-command self-check (15 steps)
  Makefile                  ← convenience wrappers
```

## What it does

The plugin contains 14 skills that *govern* other skills:

- **Per-skill lifecycle** (8): `skill-author`, `skill-audit`, `skill-refactor`,
  `skill-retire`, `skill-migrate`, `skill-evaluate`, `skill-policy-overlay`,
  `skill-snapshot-diff`
- **Library lifecycle** (2): `library-audit`, `library-bootstrap`
- **Composition** (3): `family-bootstrap`, `cross-domain-orchestrator-author`,
  `cross-library-orchestrator`
- **Routing** (1): `meta` (per-cluster router)

Each skill has been walked end-to-end as in-memory dogfood. Findings are
captured in `context-meta-pipeline/coverage.md` audit-finding ledger
(currently A1-A56).

## Self-check

```bash
cd context-meta-pipeline
./verify.sh    # 15 steps, all green at v0.7.0
make verify    # same via Make
make lint      # ruff (informational)
make typecheck # mypy --strict (informational)
```

## Discipline

Per `context-meta-pipeline/ARCHITECTURE.md`:
- PyYAML + stdlib only (load-bearing since v0.1.0)
- Lifecycle skills are procedural by design (operator-driven, not
  script-mechanized)
- Coverage matrix forbids silent gaps (everything is in-scope, specced,
  deferred, or explicitly out-of-scope)

v0.7.0 ships five pre-trigger build-outs (integration-test-runner,
search-skills + gen-index, snapshot-hash, notify-dependents, analytics-
rollup) ahead of their formal triggers per operator choice — disclosed
explicitly in `ARCHITECTURE.md` §"v0.7.0 Ahead-of-Trigger Note".

## License

Apache-2.0 (per `context-meta-pipeline/LICENSE`).
