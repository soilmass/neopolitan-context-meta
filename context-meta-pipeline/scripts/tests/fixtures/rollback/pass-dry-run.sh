#!/usr/bin/env bash
# pass-dry-run.sh — rollback-skill fixture: successful dry-run.
#
# Creates a temp git repo with skill-foo at v0.1.0 and v0.1.1,
# then invokes rollback-skill.py --dry-run --to 0.1.0.
# Expects exit 2 (rollback-skill.py's dry-run exit code per docstring).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
ROLLBACK_SCRIPT="$REPO_ROOT/scripts/rollback-skill.py"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

cd "$TMP"
git init -q
git config user.email "fixture@test"
git config user.name "fixture"

mkdir -p skills/skill-foo .claude-plugin
cat > .claude-plugin/plugin.json <<EOF
{"name":"fixture","version":"0.1.1"}
EOF

# v0.1.0 commit
cat > skills/skill-foo/SKILL.md <<EOF
---
name: skill-foo
description: >
  Fixture skill for rollback testing. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: tool
  changelog: |
    v0.1.0 — initial.
---

# skill-foo

## Purpose
fixture.

## When to Use
in tests.

## When NOT to Use
in prod.

## Stage-Gated Procedure
### Stage 1
do thing.

## Dependencies
none.

## Evaluation
correct when stage runs.

## Handoffs
none.
EOF

cat > SNAPSHOT.lock <<EOF
snapshot_version: "0.1.0"
plugin: "fixture"
skills:
  skill-foo:
    version: "0.1.0"
    archetype: tool
    path: "skills/skill-foo/SKILL.md"
    health: "fresh"
EOF

cat > CHANGELOG.md <<EOF
# Changelog
## [0.1.0] - 2026-01-01
### Added
- skill-foo v0.1.0
EOF

git add -A
git commit -q -m "v0.1.0"

# v0.1.1 commit
sed -i 's/version: "0.1.0"/version: "0.1.1"/' skills/skill-foo/SKILL.md
sed -i '0,/v0.1.0 — initial./{s/v0.1.0 — initial./v0.1.1 — patch.\n    v0.1.0 — initial./}' skills/skill-foo/SKILL.md
sed -i 's/version: "0.1.0"/version: "0.1.1"/' SNAPSHOT.lock
sed -i 's/snapshot_version: "0.1.0"/snapshot_version: "0.1.1"/' SNAPSHOT.lock
git add -A
git commit -q -m "v0.1.1"

# Rollback dry-run from current 0.1.1 → 0.1.0
# `|| actual=$?` captures the exit without aborting under `set -e`.
actual=0
python3 "$ROLLBACK_SCRIPT" --skill skill-foo --to 0.1.0 --reason "fixture test" --dry-run >/dev/null 2>&1 || actual=$?

# rollback-skill.py returns 2 for dry-run per its docstring
if [ "$actual" -eq 2 ]; then
  echo "PASS pass-dry-run.sh (exit $actual = expected 2 for --dry-run)"
  exit 0
else
  echo "FAIL pass-dry-run.sh (exit $actual; expected 2)"
  exit 1
fi
