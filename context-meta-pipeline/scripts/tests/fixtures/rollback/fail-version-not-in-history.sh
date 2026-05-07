#!/usr/bin/env bash
# fail-version-not-in-history.sh — rollback target version was never committed.
# Expects exit 1 (could not find ref for version).

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

cat > skills/skill-foo/SKILL.md <<EOF
---
name: skill-foo
description: >
  Fixture skill. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.2.0"
  archetype: tool
  changelog: |
    v0.2.0 — only version ever committed.
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
correct.

## Handoffs
none.
EOF

cat > SNAPSHOT.lock <<EOF
snapshot_version: "0.2.0"
plugin: "fixture"
skills:
  skill-foo:
    version: "0.2.0"
    archetype: tool
    path: "skills/skill-foo/SKILL.md"
    health: "fresh"
EOF

cat > CHANGELOG.md <<EOF
# Changelog
## [0.2.0]
EOF

git add -A
git commit -q -m "v0.2.0 only"

# Try to roll back to v0.1.0 (never committed)
actual=0
python3 "$ROLLBACK_SCRIPT" --skill skill-foo --to 0.1.0 --reason "fixture test" --dry-run >/dev/null 2>&1 || actual=$?

if [ "$actual" -eq 1 ]; then
  echo "PASS fail-version-not-in-history.sh (exit $actual = expected 1 for missing version)"
  exit 0
else
  echo "FAIL fail-version-not-in-history.sh (exit $actual; expected 1)"
  exit 1
fi
