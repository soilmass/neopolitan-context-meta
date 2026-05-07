#!/usr/bin/env bash
# release-tag.sh — one-command release for the context-meta-pipeline plugin.
#
# Workflow:
#   1. Refuse to run if `verify.sh` exits nonzero (don't tag broken state).
#   2. Read the snapshot_version from SNAPSHOT.lock.
#   3. Verify plugin.json + marketplace.json agree on the same version.
#   4. Verify a git tag for that version doesn't already exist.
#   5. Generate release notes via snapshot-diff.py against the previous tag's
#      SNAPSHOT.lock (if available) and fall back to "first release" notes.
#   6. Print the suggested commands (tag + push); does NOT push without
#      --confirm. Default mode is dry-run-with-instructions.
#
# Per VERSIONING-POLICY.md, this script does not bypass the breaking-change
# detector or any other gate; it composes them into a single entry point.
#
# Exit codes:
#   0  release dry-run produced (with --confirm: tag created)
#   1  refused (verify.sh failed, version mismatch, tag exists, etc.)
#   2  invocation problem (not in plugin root, missing files)
#
# Usage:
#   ./scripts/release-tag.sh                  # dry-run; print plan
#   ./scripts/release-tag.sh --confirm        # actually create the tag
#   ./scripts/release-tag.sh --output NOTES.md  # write notes to file

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || { echo "error: cd $ROOT failed" >&2; exit 2; }

CONFIRM=0
NOTES_OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --confirm) CONFIRM=1; shift ;;
    --output) NOTES_OUT="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^$/p' "$0" | sed 's/^# //;s/^#//'
      exit 0 ;;
    *) echo "error: unknown arg: $1" >&2; exit 2 ;;
  esac
done

red()    { printf "\033[0;31m%s\033[0m\n" "$1"; }
green()  { printf "\033[0;32m%s\033[0m\n" "$1"; }
yellow() { printf "\033[0;33m%s\033[0m\n" "$1"; }

# 1. Refuse if verify.sh fails
echo "=== Step 1: verify.sh ==="
if ! ./verify.sh > /tmp/release-verify.log 2>&1; then
  red "  verify.sh exited nonzero — refusing to tag a broken state."
  echo "  Last 20 lines of output:"
  tail -20 /tmp/release-verify.log | sed 's/^/    /'
  exit 1
fi
green "  verify.sh exit 0"

# 1.5 (v0.6.2): health audits + library-audit checklist.
# verify.sh covers structural checks; library-shape and per-skill health are
# advisory pre-release gates. Per the v0.6.2 wiring, audit-skill --write-health
# updates SNAPSHOT.lock. Refuse if any skill is "unhealthy". --allow-unhealthy
# bypasses for emergency CI tagging.
echo
echo "=== Step 1.5: health audits ==="
ALLOW_UNHEALTHY=0
for arg in "$@"; do
  if [ "$arg" = "--allow-unhealthy" ]; then
    ALLOW_UNHEALTHY=1
  fi
done

# Run audit-skill with --write-health (idempotent; only mutates if status changes).
audit_rc=0
python3 scripts/audit-skill.py --all --write-health > /tmp/release-audit.log 2>&1 || audit_rc=$?
if [ "$audit_rc" -ne 0 ]; then
  if [ "$ALLOW_UNHEALTHY" -eq 1 ]; then
    yellow "  audit-skill flagged skills (bypassed via --allow-unhealthy)"
  else
    red "  audit-skill flagged skills — refusing to tag. Pass --allow-unhealthy to bypass."
    echo "  Last 15 lines of audit output:"
    tail -15 /tmp/release-audit.log | sed 's/^/    /'
    exit 1
  fi
else
  green "  audit-skill --all --write-health: clean"
fi

# v0.7.0: snapshot-hash --verify + gen-index --check (ahead-of-trigger
# governance/SKILL-PROVENANCE.md + governance/SKILL-DISCOVERABILITY.md).
if python3 scripts/snapshot-hash.py --verify > /tmp/release-hash.log 2>&1; then
  green "  snapshot-hash --verify: clean"
else
  red "  snapshot-hash --verify: SKILL.md hashes don't match SNAPSHOT.lock — refuse."
  cat /tmp/release-hash.log | sed 's/^/    /'
  exit 1
fi
if python3 scripts/gen-index.py --check > /tmp/release-index.log 2>&1; then
  green "  gen-index --check: INDEX.md fresh"
else
  red "  gen-index --check: INDEX.md stale. Run \`make index\` and re-tag."
  exit 1
fi

# Refuse if SNAPSHOT.lock now has any "unhealthy" skill (write-health may have
# transitioned a skill from flagged → unhealthy). grep returns nonzero when
# nothing matches; `|| true` and `wc -l` pattern gives a clean integer.
unhealthy_count=$(grep 'health: "unhealthy"' SNAPSHOT.lock 2>/dev/null | wc -l | tr -d '[:space:]')
unhealthy_count=${unhealthy_count:-0}
if [ "$unhealthy_count" -gt 0 ]; then
  if [ "$ALLOW_UNHEALTHY" -eq 1 ]; then
    yellow "  SNAPSHOT.lock has $unhealthy_count unhealthy skill(s) (bypassed)"
  else
    red "  SNAPSHOT.lock has $unhealthy_count unhealthy skill(s) — refusing to tag."
    grep -B1 'health: "unhealthy"' SNAPSHOT.lock | sed 's/^/    /'
    exit 1
  fi
fi

# library-audit is procedural (a SKILL.md, not a script). Print a checklist
# the operator must mentally walk before --confirm. release-tag.sh does NOT
# mechanize library-audit because procedural skills are operator-driven by
# design (M4 antipattern from v0.5.0 audit; reaffirmed v0.6.x).
yellow "  library-audit reminder (procedural — operator must walk):"
yellow "    - skills/library-audit/SKILL.md Stage 1: scope selection"
yellow "    - Stage 2: per-skill audit (delegated to audit-skill — done above)"
yellow "    - Stage 3: coverage schema check (delegated to coverage-check — verify.sh covers)"
yellow "    - Stage 4: snapshot integrity (delegated to dependency-graph — verify.sh covers)"
yellow "    - Stage 5: synthesis — operator drafts library-audit-report.md"
yellow "  Confirm operator walked Stage 5 before passing --confirm."

# 2. Read snapshot version
echo
echo "=== Step 2: extract version ==="
SNAP_V=$(python3 -c "import yaml; print(yaml.safe_load(open('SNAPSHOT.lock'))['snapshot_version'])")
PLUGIN_V=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
echo "  SNAPSHOT.lock snapshot_version: $SNAP_V"
echo "  plugin.json version:            $PLUGIN_V"
if [ "$SNAP_V" != "$PLUGIN_V" ]; then
  red "  SNAPSHOT.lock and plugin.json disagree — refuse."
  exit 1
fi
TAG="v$SNAP_V"
green "  release tag will be: $TAG"

# 3. Tag must not already exist
echo
echo "=== Step 3: tag uniqueness ==="
if git rev-parse "$TAG" >/dev/null 2>&1; then
  red "  Tag $TAG already exists — refuse. Bump snapshot_version first."
  exit 1
fi
green "  $TAG does not yet exist; OK to create"

# 4. Find the previous tag for diffing
echo
echo "=== Step 4: previous tag ==="
PREV_TAG=$(git tag --sort=-v:refname 2>/dev/null | head -1 || true)
if [ -n "$PREV_TAG" ]; then
  green "  previous tag: $PREV_TAG"
else
  yellow "  no previous tag — will produce first-release notes"
fi

# 5. Generate release notes via snapshot-diff (if prev tag exists)
echo
echo "=== Step 5: release notes ==="
NOTES_TMP="$(mktemp)"
{
  echo "# Release: $TAG"
  echo
  if [ -n "$PREV_TAG" ]; then
    PREV_SNAP=$(mktemp)
    if git show "$PREV_TAG:SNAPSHOT.lock" > "$PREV_SNAP" 2>/dev/null; then
      python3 scripts/snapshot-diff.py --old "$PREV_SNAP" --new SNAPSHOT.lock 2>&1 | tail -n +2
    else
      yellow "  (could not fetch SNAPSHOT.lock from $PREV_TAG; skipping diff)"
    fi
    rm -f "$PREV_SNAP"
  else
    echo "## First release"
    echo
    python3 -c "
import yaml
data = yaml.safe_load(open('SNAPSHOT.lock'))
print(f'Skills shipped:')
for n, e in sorted(data['skills'].items()):
    print(f'  - {n} v{e[\"version\"]} ({e[\"archetype\"]})')
"
  fi
  echo
  echo "## Verification"
  echo
  echo "- verify.sh exit 0"
  echo "- ruff: clean"
  echo "- mypy --strict: zero issues"
  echo
  echo "## Authority"
  echo
  echo "Per CHANGELOG.md and SNAPSHOT.lock; see those files for the full record."
} > "$NOTES_TMP"

if [ -n "$NOTES_OUT" ]; then
  cp "$NOTES_TMP" "$NOTES_OUT"
  green "  release notes written to $NOTES_OUT"
else
  echo
  cat "$NOTES_TMP" | sed 's/^/    /'
fi

# 6. Tag (or print instructions)
echo
echo "=== Step 6: tag ==="
# v0.7.0: signed-tag enforcement (-as instead of -a) per
# governance/SKILL-PROVENANCE.md. --allow-unsigned bypasses for CI without GPG.
ALLOW_UNSIGNED=0
for arg in "$@"; do
  if [ "$arg" = "--allow-unsigned" ]; then
    ALLOW_UNSIGNED=1
  fi
done
TAG_FLAGS="-as"
if [ "$ALLOW_UNSIGNED" -eq 1 ]; then
  TAG_FLAGS="-a"
  yellow "  --allow-unsigned: tag will NOT be GPG-signed (CI bypass)"
fi
if [ "$CONFIRM" -eq 1 ]; then
  if ! git tag $TAG_FLAGS "$TAG" -F "$NOTES_TMP" 2>/tmp/release-tag-err.log; then
    red "  git tag failed:"
    cat /tmp/release-tag-err.log | sed 's/^/    /'
    if grep -qi "gpg\|sign" /tmp/release-tag-err.log; then
      yellow "  Hint: pass --allow-unsigned to bypass GPG signing (CI environments)."
    fi
    rm -f "$NOTES_TMP"
    exit 1
  fi
  green "  created tag $TAG ($([ "$ALLOW_UNSIGNED" -eq 1 ] && echo unsigned || echo signed))"
  echo "  push with: git push origin $TAG"
else
  yellow "  dry-run (use --confirm to create the tag)"
  echo "  command would be: git tag $TAG_FLAGS $TAG -F <notes>"
fi

rm -f "$NOTES_TMP" /tmp/release-verify.log /tmp/release-hash.log /tmp/release-index.log /tmp/release-audit.log /tmp/release-tag-err.log
exit 0
