#!/usr/bin/env bash
# fail-stale-recency.sh — skill dir mtime backdated 12 months → Gate 1 fail.
# (audit-skill.py uses git log when available; falls back to mtime when not.
# The fixture sets up a non-git temp dir, so audit-skill uses mtime.)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/scripts/audit-skill.py"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

mkdir -p "$TMP/skills/stale-skill"
cat > "$TMP/skills/stale-skill/SKILL.md" <<'EOF'
---
name: stale-skill
description: >
  Owns capability-a. Used in fixture tests only. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# stale-skill

## When to Use
in fixture tests only.

## When NOT to Use
in real work.

## Capabilities Owned
- capability-a — narrow fixture capability.

## Handoffs to Other Skills
- to bl-router for dispatch.

## Edge Cases
- empty input — no-op.

## References
- (none).
EOF

# Backdate the skill dir so Gate 1 fails (no git in this temp dir, so
# audit-skill uses working-tree mtime per its Stage 2 fallback).
touch -d "12 months ago" "$TMP/skills/stale-skill"

actual=0
python3 "$AUDIT_SCRIPT" --skill stale-skill --root "$TMP" >/dev/null 2>&1 || actual=$?

if [ "$actual" -eq 1 ]; then
  echo "PASS fail-stale-recency.sh (exit $actual = expected 1 for Gate 1 fail)"
  exit 0
else
  echo "FAIL fail-stale-recency.sh (exit $actual; expected 1)"
  python3 "$AUDIT_SCRIPT" --skill stale-skill --root "$TMP" 2>&1 | head -10
  exit 1
fi
