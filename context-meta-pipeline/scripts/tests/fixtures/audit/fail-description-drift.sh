#!/usr/bin/env bash
# fail-description-drift.sh — description claims things absent from body.
# Expects Gate 4 fail → exit 1.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/scripts/audit-skill.py"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

mkdir -p "$TMP/skills/drifted-skill"
cat > "$TMP/skills/drifted-skill/SKILL.md" <<'EOF'
---
name: drifted-skill
description: >
  Performs revolutionary cryptographic synthesis with quantum entanglement
  in distributed monorepos via blockchain. Pioneers satellite reconciliation
  protocols. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — initial.
---

# drifted-skill

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

actual=0
python3 "$AUDIT_SCRIPT" --skill drifted-skill --root "$TMP" >/dev/null 2>&1 || actual=$?

if [ "$actual" -eq 1 ]; then
  echo "PASS fail-description-drift.sh (exit $actual = expected 1 for Gate 4 fail)"
  exit 0
else
  echo "FAIL fail-description-drift.sh (exit $actual; expected 1)"
  exit 1
fi
