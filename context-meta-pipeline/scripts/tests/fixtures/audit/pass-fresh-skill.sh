#!/usr/bin/env bash
# pass-fresh-skill.sh — fresh SKILL.md; expect audit-skill --skill ... exit 0.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/scripts/audit-skill.py"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

mkdir -p "$TMP/skills/fixture-skill"
cat > "$TMP/skills/fixture-skill/SKILL.md" <<'EOF'
---
name: fixture-skill
description: >
  Owns capability-a. Used in fixture tests only. Do NOT use for: real
  work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# fixture-skill

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

actual=0
python3 "$AUDIT_SCRIPT" --skill fixture-skill --root "$TMP" >/dev/null 2>&1 || actual=$?

if [ "$actual" -eq 0 ]; then
  echo "PASS pass-fresh-skill.sh (exit $actual)"
  exit 0
else
  echo "FAIL pass-fresh-skill.sh (exit $actual; expected 0)"
  python3 "$AUDIT_SCRIPT" --skill fixture-skill --root "$TMP" 2>&1 | head -20
  exit 1
fi
