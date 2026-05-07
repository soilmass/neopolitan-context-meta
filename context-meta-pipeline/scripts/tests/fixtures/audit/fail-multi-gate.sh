#!/usr/bin/env bash
# fail-multi-gate.sh — Gates 1 (recency) AND 4 (drift) both fail. Expects exit 1.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/scripts/audit-skill.py"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

mkdir -p "$TMP/skills/multi-fail"
cat > "$TMP/skills/multi-fail/SKILL.md" <<'EOF'
---
name: multi-fail
description: >
  Performs revolutionary cryptographic synthesis with quantum entanglement.
  Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# multi-fail

## When to Use
in fixture tests only.

## When NOT to Use
in real work.

## Capabilities Owned
- A: a tiny operation.

## Handoffs to Other Skills
- to a sibling.

## Edge Cases
- empty input.

## References
- (none).
EOF

# Backdate so Gate 1 also fails.
touch -d "12 months ago" "$TMP/skills/multi-fail"

actual=0
out=$(python3 "$AUDIT_SCRIPT" --skill multi-fail --root "$TMP" 2>&1) || actual=$?

# Verify exit AND that both gates flagged
gate1_failed=$(echo "$out" | grep -c "Last update.*month" || true)
gate4_failed=$(echo "$out" | grep -c "Description drift.*%" || true)

if [ "$actual" -eq 1 ] && [ "$gate1_failed" -ge 1 ] && [ "$gate4_failed" -ge 1 ]; then
  echo "PASS fail-multi-gate.sh (exit $actual; both Gate 1 and Gate 4 surfaced)"
  exit 0
else
  echo "FAIL fail-multi-gate.sh (exit $actual; gate1=$gate1_failed gate4=$gate4_failed)"
  echo "$out" | head -10
  exit 1
fi
