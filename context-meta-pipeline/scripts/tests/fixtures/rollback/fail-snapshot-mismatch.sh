#!/usr/bin/env bash
# fail-snapshot-mismatch.sh — SNAPSHOT.lock has no entry for the skill being
# rolled back. rollback-skill.py's update_snapshot() raises ValueError →
# exit 1.

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
correct.

## Handoffs
none.
EOF

# SNAPSHOT.lock has NO entry for skill-foo (only some other skill).
cat > SNAPSHOT.lock <<EOF
snapshot_version: "0.1.0"
plugin: "fixture"
skills:
  some-other-skill:
    version: "0.1.0"
    archetype: tool
    path: "skills/some-other-skill/SKILL.md"
    health: "fresh"
EOF

cat > CHANGELOG.md <<EOF
# Changelog
## [0.1.0]
EOF

git add -A
git commit -q -m "v0.1.0"

# Add another commit at v0.1.1 so find_ref_for_version succeeds; the
# subsequent snapshot update is what should fail.
sed -i 's/version: "0.1.0"/version: "0.1.1"/' skills/skill-foo/SKILL.md
git add -A
git commit -q -m "v0.1.1"

actual=0
python3 "$ROLLBACK_SCRIPT" --skill skill-foo --to 0.1.0 --reason "fixture test" --dry-run >/dev/null 2>&1 || actual=$?

# A snapshot mismatch raises in update_snapshot() — but with --dry-run that
# update is skipped, so the harness checks the non-dry-run path by removing
# --dry-run. But non-dry-run modifies files, so we want the dry-run path.
# Actually: dry-run still calls find_ref_for_version (succeeds), then the
# update_snapshot is the *next* step which is also skipped. So in dry-run
# this test won't surface the mismatch. The script returns exit 2 (dry-run
# completed) even though the real run would fail.
#
# To actually test snapshot-mismatch, we need to NOT use --dry-run. But that
# also writes files. Compromise: run without --dry-run inside the disposable
# temp repo and verify exit 1.

actual=0
python3 "$ROLLBACK_SCRIPT" --skill skill-foo --to 0.1.0 --reason "fixture test" >/dev/null 2>&1 || actual=$?

if [ "$actual" -eq 1 ]; then
  echo "PASS fail-snapshot-mismatch.sh (exit $actual = expected 1 for missing snapshot entry)"
  exit 0
else
  echo "FAIL fail-snapshot-mismatch.sh (exit $actual; expected 1)"
  exit 1
fi
