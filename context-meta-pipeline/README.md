# Skill Library

A modular, composable system of Claude skills built on Unix-philosophy principles. Each skill does one thing. Skills compose through explicit handoffs rather than absorption. New domains enter the library through a stage-gated converter that produces tiered families of cross-referencing skills with documented coverage boundaries.

The library is designed to be encompassing — every claimed domain has its capabilities either covered, queued, or named-and-deferred. Silent gaps are the failure mode the architecture exists to prevent.

---

## Where to Start

| You are... | Read this |
|---|---|
| New to the library | `ARCHITECTURE.md` |
| Authoring a new skill | `governance/METADATA-VALIDATION.md` |
| Reviewing a skill PR | `governance/INDEX.md`, then the three current governance docs |
| Responding to a broken skill | `governance/ROLLBACK-PROCEDURE.md` |
| Building a new skill family | `skills/family-bootstrap/SKILL.md` |
| Looking for the operational rules | `GOVERNANCE.md`, `VERSIONING-POLICY.md`, `MAINTENANCE.md` |

For a complete reading order, see the "Reading Order" section in `governance/INDEX.md`.

---

## Library Map

```
/
├── .claude-plugin/plugin.json         ← plugin manifest
├── README.md                          ← entry point (this file)
├── ARCHITECTURE.md                    ← system design, archetypes, layering
├── CHANGELOG.md                       ← cross-skill change log (canonical)
├── SNAPSHOT.lock                      ← last known-good library state
├── coverage.md                        ← library-root coverage map
├── GOVERNANCE.md                      ← operational rules
├── VERSIONING-POLICY.md               ← SemVer application, user pins, migration
├── MAINTENANCE.md                     ← ownership, health checks, decay
├── CONTRIBUTING.md                    ← contributor guide (entry point)
├── LICENSE                            ← Apache-2.0
├── verify.sh                          ← one-command self-check runner
├── Makefile                           ← `make verify`, `make audit`, `make lint`, …
├── requirements.txt                   ← runtime deps (PyYAML)
├── .gitignore                         ← Python build artifacts, caches
├── .github/workflows/verify.yml       ← CI: verify.sh + lint + breaking-change detector
├── agents/, commands/, hooks/         ← reserved Claude Code plugin slots (empty in v0.2.x)
├── governance/                        ← specific operational procedures
│   ├── INDEX.md                       ← maps the governance layer
│   ├── BREAKING-CHANGE-DETECTION.md   ← load-bearing
│   ├── METADATA-VALIDATION.md         ← load-bearing
│   ├── ROLLBACK-PROCEDURE.md          ← load-bearing
│   ├── INTEGRATION-TESTING.md         ← v0.5.0; pre-trigger N/A
│   ├── SKILL-DISCOVERABILITY.md       ← v0.5.0; pre-trigger N/A
│   ├── SKILL-PROVENANCE.md            ← v0.5.0; pre-trigger N/A
│   ├── SECURITY-AUDIT.md              ← v0.5.0; pre-trigger N/A
│   ├── EMERGENCY-HOTFIX.md            ← v0.5.0; placeholder skeleton
│   ├── DEPRECATION-COMMUNICATION.md   ← v0.5.0; pre-trigger N/A
│   └── USAGE-ANALYTICS.md             ← v0.5.0; pre-trigger N/A
├── scripts/                           ← Python automation + tests
│   ├── validate-metadata.py           ← structural + heuristic checks (METADATA-VALIDATION.md)
│   ├── detect-breaking-changes.py     ← BREAKING-CHANGE-DETECTION.md
│   ├── rollback-skill.py              ← ROLLBACK-PROCEDURE.md Level 1
│   ├── audit-skill.py                 ← MAINTENANCE.md Gates 1 + 4 (v0.2.0+)
│   ├── coverage-check.py              ← v0.5.0 — coverage.md schema validator
│   ├── snapshot-diff.py               ← v0.5.0 — release-note generator
│   ├── migration-guide-gen.py         ← v0.5.0 — MIGRATION-v<N>.md drafter
│   ├── dependency-graph.py            ← v0.5.0 — SNAPSHOT.lock depends_on visualizer
│   ├── routing-eval-runner.py         ← v0.5.0 — Gate 3 mechanizer
│   ├── taxonomy-coverage-sync.py      ← v0.5.0 — taxonomy.md ↔ coverage.md alignment
│   ├── release-tag.sh                 ← v0.5.0 — one-command release flow
│   └── tests/
│       ├── fixtures/                  ← 17 SKILL.md fixtures + coverage/ + snapshot/
│       ├── routing-eval.yaml          ← starter routing-eval prompts
│       └── smoke/bootstrap-git-family/ ← v0.5.0 family-bootstrap regression fixture
└── skills/                            ← every SKILL.md lives here, auto-discovered
    ├── meta/                          ← v0.5.0 — per-cluster router for the lifecycle cluster
    ├── skill-author/                  ← lifecycle: create
    ├── skill-audit/                   ← lifecycle: per-skill health
    ├── skill-refactor/                ← lifecycle: restructure
    ├── skill-retire/                  ← lifecycle: archive + redirect
    ├── skill-migrate/                 ← v0.5.0 — author MIGRATION-v<N>.md
    ├── skill-evaluate/                ← v0.5.0 — Gate 3 mechanizer (procedural)
    ├── skill-policy-overlay/          ← v0.5.0 — author house-* overlays
    ├── skill-snapshot-diff/           ← v0.5.0 — release-note composition
    ├── library-audit/                 ← v0.5.0 — library-shape health
    ├── library-bootstrap/             ← v0.5.0 — scaffold a new library
    ├── family-bootstrap/              ← lifecycle: bootstrap a family within a library
    ├── cross-domain-orchestrator-author/ ← v0.5.0 — cross-family orchestrators
    ├── cross-library-orchestrator/    ← v0.5.0 — cross-library orchestrators
    └── <consumer-family>/             ← future: domain families produced by family-bootstrap
        └── (per-family SKILL.md + coverage.md + atoms)
```

Concrete contents depend on which families and skills are present. The structure above shows the shape; what populates it is determined by the architecture (see `ARCHITECTURE.md`) and the families currently active in the library (see `CHANGELOG.md`).

---

## Current State

System-level state. For specific skills and families, see `CHANGELOG.md` and individual family `coverage.md` files.

### Stable

- **Architecture** is documented. Five archetypes, layering rules, naming conventions, tier model, coverage discipline, routing-contention discipline.
- **Governance** has three load-bearing documents (breaking-change detection, metadata validation, rollback) plus the index that maps deferred concerns.
- **Operational rules** are documented at the root (`GOVERNANCE.md`, `VERSIONING-POLICY.md`, `MAINTENANCE.md`).
- **Lifecycle pipeline** ships 13 atoms + 1 router (`meta`) clustered around per-skill / library / composition concerns:
  - **Per-skill**: `skill-author`, `skill-audit`, `skill-refactor`, `skill-retire`, `skill-migrate`, `skill-evaluate`, `skill-policy-overlay`, `skill-snapshot-diff`
  - **Library**: `library-audit`, `library-bootstrap`
  - **Composition**: `family-bootstrap`, `cross-domain-orchestrator-author`, `cross-library-orchestrator`
  - **Router**: `meta`
- **11 Python scripts** under `scripts/`:
  - `validate-metadata.py` / `detect-breaking-changes.py` / `rollback-skill.py` / `audit-skill.py` (v0.1.0–v0.2.0)
  - `coverage-check.py` / `snapshot-diff.py` / `migration-guide-gen.py` / `dependency-graph.py` / `routing-eval-runner.py` / `taxonomy-coverage-sync.py` / `release-tag.sh` (v0.5.0)
- **`verify.sh`** at plugin root runs every check end-to-end (validators + fixture matrix + audit + version triangulation + coverage-check + snapshot-diff sanity) and exits 0 when the library is clean.
- **17-fixture matrix + 3 coverage fixtures + 2 snapshot fixtures** under `scripts/tests/fixtures/` exercises every validator rule across all five archetypes plus coverage.md schema and snapshot-diff parsing.
- **10 governance docs** under `governance/`: 3 load-bearing (METADATA-VALIDATION, BREAKING-CHANGE-DETECTION, ROLLBACK-PROCEDURE) + 7 specified-but-pre-trigger-N/A (INTEGRATION-TESTING, SKILL-DISCOVERABILITY, SKILL-PROVENANCE, SECURITY-AUDIT, EMERGENCY-HOTFIX, DEPRECATION-COMMUNICATION, USAGE-ANALYTICS).

### Deferred

The governance `INDEX.md` names seven deferred documents with explicit build triggers (security audit, integration testing, emergency hotfix, deprecation communication, provenance, analytics, discoverability). Each is documented as a future need, not a silent gap.

For the current inventory of skills, families, and queued work, consult `CHANGELOG.md`. The README does not track per-skill state because that information goes stale faster than the README is updated.

---

## Core Principles

These are the non-negotiable rules. Detail in `ARCHITECTURE.md`.

**One responsibility per skill.** If a description has "and" between two distinct verbs, it's two skills.

**Compose via handoff, not absorption.** Skills name the next skill rather than reimplementing.

**Anti-triggers are first-class.** Every skill description has a `Do NOT use for` block.

**Read/write separation.** Reading and writing operations on the same domain are different skills.

**Mechanism vs policy.** Domain reality and team conventions live in different skills.

**Stable interfaces between skills.** `taxonomy.md`, `capabilities.json`, `patterns.json`, `coverage.md` are the text streams between cooperating skills.

**Worse-is-better triggers.** Short descriptions plus disciplined anti-triggers beat elaborate trigger logic.

---

## Operational Model

The library runs on three commitments. Detail in `GOVERNANCE.md`.

**Latest-only support.** Older versions are not maintained. Users who need an older version pin explicitly and accept the risks.

**Lock-step upgrades.** When a breaking change touches multiple skills, all affected skills release together.

**Self-contained.** No external skill dependencies. If an external capability is needed, an internal atom is authored.

---

## Adding to the Library

The library uses a five-skill **lifecycle pipeline**. Each skill has heavyweight, gated stages.

**To add a new skill family:** invoke `family-bootstrap` (Orchestrator, 6 stages). Produces a router, Tier 1 atoms, a per-family `coverage.md`, and entries in `SNAPSHOT.lock` and `CHANGELOG.md`. Delegates to `skill-author` per atom.

**To add a single skill** (atom into an existing family, or a tool, router, or policy overlay): invoke `skill-author` (Tool, 4 stages). Produces the SKILL.md and any references; runs `validate-metadata.py` at the validation gate; updates the family's `coverage.md`.

**To audit health** of one or more skills: invoke `skill-audit` (Tool, 5 stages). Runs the four gates from `MAINTENANCE.md` and emits per-failing-skill banner blocks plus a `CHANGELOG` `Health` suggestion.

**To restructure** a skill that's mixing archetypes (or to perform the three-way refactor in `ARCHITECTURE.md` §"Mechanism vs Policy"): invoke `skill-refactor` (Tool, 5 stages). Delegates to `skill-author` for new skills and to `skill-retire` for the source.

**To retire a skill:** invoke `skill-retire` (Tool, 4 stages). Archives with a redirect note; the SKILL.md remains in git history and remains pinnable.

**To modify an existing skill:** open a PR. `validate-metadata.py` runs at PR time. Breaking changes require a MAJOR bump per `VERSIONING-POLICY.md`, a migration guide, and lock-step updates to dependents — `detect-breaking-changes.py` enforces this.

The audit ritual (per `ARCHITECTURE.md` §"Routing and Contention") runs in `skill-author` Stage 2 and `family-bootstrap` Stage 5 to catch routing contention before merge.
