# Library skeleton

Stage 4 of `library-bootstrap` produces a complete operational
scaffold. This reference defines the *content* of each file (Stage
4's named outputs were missing from the SKILL.md until this v0.5.2
addition — audit findings A32 / A33).

Substitutions throughout: `<NAME>` is the library name (e.g.,
`context-postgres`). `<DESCRIPTION>` is the one-paragraph from
Stage 1's library-intake.yaml. `<DOMAIN1>` etc. are first_domains.

## SNAPSHOT.lock (root)

```yaml
snapshot_version: "0.1.0"
generated: "<YYYY-MM-DD>"
plugin: "<NAME>"
skills: {}
```

## coverage.md (root) — empty-library schema

```markdown
# <NAME> Coverage

Last verification: <YYYY-MM-DD> (initial bootstrap; no skills yet).

## Domains Claimed

| Domain | Family | Coverage |
|---|---|---|
| (none yet) | — | bootstrap a family via family-bootstrap |

## Domains Deferred

| Domain | Why deferred | Build trigger |
|---|---|---|
| `<DOMAIN1>` | Not yet bootstrapped | When first <DOMAIN1> family is needed |
| `<DOMAIN2>` | Not yet bootstrapped | When first <DOMAIN2> family is needed |

## Domains Out of Scope

| Domain | Why out of scope | Where to look instead |
|---|---|---|
| Lifecycle skills | Belong to the meta-pipeline | context-meta-pipeline plugin |

## Cross-Domain Orchestrators

None at v0.1.0.

## Coverage Matrix Status

No skills yet — fresh library (will populate after first
family-bootstrap run).
```

(The "No skills yet" stub triggers the Coverage Matrix Status
warning suppression in `coverage-check.py` — see A31 fix in
v0.5.2.)

## governance/INDEX.md (root)

```markdown
# Governance Index — <NAME>

This library inherits the meta-pipeline's three load-bearing
governance docs (METADATA-VALIDATION, BREAKING-CHANGE-DETECTION,
ROLLBACK-PROCEDURE) by reference. Authoring local versions is
unnecessary; the meta-pipeline is the canonical source.

## Currently Documented

(inherited from context-meta-pipeline)

## Deferred

(inherited; first build trigger to fire on this library will be
the trigger for the relevant deferred doc)
```

## CHANGELOG.md (root)

```markdown
# Changelog

## [Unreleased]
(Pending the next release.)

## [0.1.0] - <YYYY-MM-DD>
### Added
- Library scaffolded via library-bootstrap.
```

## README.md (root)

```markdown
# <NAME>

<DESCRIPTION>

Scaffolded via library-bootstrap.

See `coverage.md` for the domain claim list, `governance/INDEX.md`
for the inherited governance layer.
```

## Makefile (root)

```makefile
PYTHON ?= python3
SCRIPTS := scripts

.PHONY: help verify validate audit lint typecheck install-deps clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk -F':.*?##' '{printf "  %-22s %s\n", $$1, $$2}'

verify: ## Run verify.sh — full self-check
	@./verify.sh

validate: ## Validate every live SKILL.md
	@$(PYTHON) ../context-meta-pipeline/scripts/validate-metadata.py --all

audit: ## Run audit-skill on every live skill
	@$(PYTHON) ../context-meta-pipeline/scripts/audit-skill.py --all

install-deps: ## Install runtime dependencies
	@$(PYTHON) -m pip install -r requirements.txt

clean: ## Remove generated artifacts
	@find . -type d \( -name '__pycache__' -o -name '.mypy_cache' -o -name '.ruff_cache' \) -exec rm -rf {} + 2>/dev/null || true
```

(Note the `../context-meta-pipeline/scripts/` references — the new
library re-uses the meta-pipeline's scripts rather than duplicating.)

## verify.sh (root)

```bash
#!/usr/bin/env bash
# verify.sh — minimal self-check for <NAME>.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
green="\033[0;32m"; red="\033[0;31m"; reset="\033[0m"
ok() { printf "${green}OK${reset}    %s\n" "$1"; }
fail() { printf "${red}FAIL${reset}  %s\n" "$1"; FAILED=1; }
FAILED=0

META=../context-meta-pipeline

echo "=== 1. validate-metadata against live skills ==="
if python3 $META/scripts/validate-metadata.py --all >/tmp/v.log 2>&1; then
  count=$(grep -c PASSED /tmp/v.log)
  ok "$count skills pass"
else
  fail "validate-metadata reported errors"
  cat /tmp/v.log
fi

echo
echo "=== 2. coverage-check ==="
if python3 $META/scripts/coverage-check.py --file coverage.md >/dev/null 2>&1; then
  ok "coverage.md schema-valid"
else
  fail "coverage-check failed"
fi

echo
if [ "$FAILED" -eq 0 ]; then
  printf "${green}PASS${reset} all checks clean.\n"
  exit 0
else
  printf "${red}FAIL${reset}\n"
  exit 1
fi
```

(Mark executable: `chmod +x verify.sh`.)

## requirements.txt (root)

```
PyYAML>=6.0,<7
```

## .gitignore (root)

```
__pycache__/
*.py[cod]
.mypy_cache/
.ruff_cache/
.venv/
.idea/
.vscode/
.DS_Store
```

## CONTRIBUTING.md (root)

```markdown
# Contributing to <NAME>

This library was scaffolded via the meta-pipeline's `library-bootstrap`.
It inherits the meta-pipeline's authoring conventions, validators,
versioning policy, and naming rules.

For any contribution shape:
1. Read the meta-pipeline's CONTRIBUTING.md (parent doc).
2. Run `make verify` from this library's root before submitting.
3. Skill-authoring uses `skill-author` from the meta-pipeline.
4. Family-bootstrap for whole new domains uses `family-bootstrap`.
```

## LICENSE (root)

Apache-2.0 standard text. Copy from the meta-pipeline's LICENSE
file verbatim, with the copyright line updated.

## .github/workflows/verify.yml (root)

```yaml
name: verify

on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: ./verify.sh
```

## What's NOT scaffolded

- Per-skill SKILL.md files — authored via `skill-author` after
  bootstrap completes.
- Domain families — authored via `family-bootstrap` after bootstrap
  completes.
- governance/<NAME>.md docs beyond INDEX.md — inherited.
- ARCHITECTURE.md / GOVERNANCE.md / VERSIONING-POLICY.md /
  MAINTENANCE.md — inherited from the meta-pipeline; no local
  authoring needed.
