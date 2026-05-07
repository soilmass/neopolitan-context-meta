#!/usr/bin/env bash
# apply-roundtrip.sh — fixture harness for v0.6.2 --apply-banners + apply_banner_to_skill_md.
#
# Constructs a synthetic skill with a failing drift gate, runs audit-skill.py
# --apply-banners (not dry-run), and asserts:
#   1. The SKILL.md description now contains BANNER_MARKER.
#   2. Re-running --apply-banners is a no-op (idempotency).
#   3. The mutated SKILL.md still parses cleanly via _skill_io.parse_skill.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# Build a fixture library root with one drift-failing skill. Description claims
# capability-X / capability-Y / capability-Z; body mentions only capability-A —
# guaranteed drift > 10%.
mkdir -p "$TMP/skills/drift-fixture"
cat > "$TMP/skills/drift-fixture/SKILL.md" <<'EOF'
---
name: drift-fixture
description: >
  Performs capability-X plus capability-Y plus capability-Z plus
  capability-W. Author-tests-banner-application. Do NOT use for: real work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  changelog: |
    v0.1.0 — fixture-only.
---

# drift-fixture

## When to Use
- Owns capability-A. Used in fixture tests only.

## When NOT to Use
- Outside fixture tests.

## Capabilities Owned
- capability-A — only one.

## Handoffs to Other Skills
- N/A.

## Edge Cases
- N/A.

## References
- N/A.
EOF

# Verify it currently fails the drift gate (sanity check).
actual=0
python3 "$REPO_ROOT/scripts/audit-skill.py" --skill drift-fixture --root "$TMP" >/dev/null 2>&1 || actual=$?
if [ "$actual" -eq 0 ]; then
  echo "FAIL: fixture should fail drift gate but audit returned exit 0"
  exit 1
fi

# Apply banners (real, not dry-run).
python3 "$REPO_ROOT/scripts/audit-skill.py" --skill drift-fixture --root "$TMP" --apply-banners >/dev/null 2>&1 || true

# Confirm BANNER_MARKER is now in the SKILL.md.
if ! grep -q "Health Check Failing" "$TMP/skills/drift-fixture/SKILL.md"; then
  echo "FAIL: banner marker not present after --apply-banners"
  cat "$TMP/skills/drift-fixture/SKILL.md"
  exit 1
fi

# Confirm validate-metadata still parses (frontmatter must remain valid).
python3 "$REPO_ROOT/scripts/validate-metadata.py" --skill "$TMP/skills/drift-fixture" >/dev/null 2>&1 || {
  echo "FAIL: validate-metadata broke after banner application"
  cat "$TMP/skills/drift-fixture/SKILL.md"
  exit 1
}

# Idempotency: second run produces no diff.
md5_before=$(md5sum "$TMP/skills/drift-fixture/SKILL.md" | awk '{print $1}')
python3 "$REPO_ROOT/scripts/audit-skill.py" --skill drift-fixture --root "$TMP" --apply-banners >/dev/null 2>&1 || true
md5_after=$(md5sum "$TMP/skills/drift-fixture/SKILL.md" | awk '{print $1}')
if [ "$md5_before" != "$md5_after" ]; then
  echo "FAIL: --apply-banners not idempotent (md5 changed: $md5_before → $md5_after)"
  exit 1
fi

echo "PASS apply-roundtrip"
exit 0
