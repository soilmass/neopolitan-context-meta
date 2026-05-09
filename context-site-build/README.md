# context-site-build

Site-build methodology library — skills that draft, audit, and
synthesize the deliverables of a 7-phase site/web-app build
(discovery → requirements → design → build → hardening → launch →
post-launch). Produces opinionated documentation artifacts per a
documented SOP.

Scaffolded via `library-bootstrap` from the
[`context-meta-pipeline`](../context-meta-pipeline/) plugin.

---

## Where to Start

| You are... | Read this |
|---|---|
| New to this library | this README, then `coverage.md` |
| Authoring a new skill | `../context-meta-pipeline/skills/skill-author/SKILL.md` |
| Bootstrapping a new family | `../context-meta-pipeline/skills/family-bootstrap/SKILL.md` |
| Reviewing a skill PR | `../context-meta-pipeline/governance/INDEX.md` |
| Looking for operational rules | `../context-meta-pipeline/GOVERNANCE.md` |

---

## Library Map

```
/
├── .claude-plugin/plugin.json   ← plugin manifest
├── README.md                    ← entry point (this file)
├── CHANGELOG.md                 ← cross-skill change log
├── SNAPSHOT.lock                ← last known-good library state
├── coverage.md                  ← coverage map + audit-finding ledger
├── governance/INDEX.md          ← inherits meta-pipeline governance
├── verify.sh                    ← one-command self-check
├── Makefile                     ← `make verify`, `make audit`, …
├── requirements.txt             ← runtime deps (PyYAML)
├── .github/workflows/verify.yml ← CI
└── skills/                      ← every SKILL.md lives here (currently empty)
```

The library inherits its scripts from the meta-pipeline (no
duplication). `make audit` invokes
`../context-meta-pipeline/scripts/audit-skill.py` etc.

---

## Current State

Fresh library, v0.1.0. Zero skills authored. Seven domain families
queued in `coverage.md` Domains Deferred — each will be bootstrapped
via `family-bootstrap` when its first deliverable needs a conformant
skill.

For the per-skill state, consult `CHANGELOG.md` and (eventually)
per-family `coverage.md` files.

---

## Operational Model

This library inherits the meta-pipeline's three commitments:

- **Latest-only support.** Older versions are not maintained.
- **Lock-step upgrades.** Breaking changes touching multiple skills
  release together.
- **Self-contained per library.** No cross-library skill
  dependencies in this library's MAJOR-version contract.

---

## Adding to the Library

Use the meta-pipeline's lifecycle skills:

- **New skill family** → `family-bootstrap`
- **Single skill** → `skill-author`
- **Audit health** → `skill-audit`
- **Restructure** → `skill-refactor`
- **Retire** → `skill-retire`

Always run `make verify` from this library's root before submitting.
