#!/usr/bin/env bash
# verify.sh — minimal self-check for context-site-build.
#
# Inherits scripts from the sibling context-meta-pipeline plugin.
# Per skills/library-bootstrap/references/library-skeleton.md.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
green="\033[0;32m"; red="\033[0;31m"; reset="\033[0m"
ok()   { printf "${green}OK${reset}    %s\n" "$1"; }
fail() { printf "${red}FAIL${reset}  %s\n" "$1"; FAILED=1; }
FAILED=0

META=../context-meta-pipeline

echo "=== 1. validate-metadata against live skills ==="
if python3 $META/scripts/validate-metadata.py --all --allow-empty >/tmp/csb-validate.log 2>&1; then
  count=$(grep -c "PASSED" /tmp/csb-validate.log || true)
  if [ -z "$count" ] || [ "$count" -eq 0 ]; then
    ok "no skills yet (vacuously OK; --allow-empty)"
  else
    ok "$count skills pass"
  fi
else
  fail "validate-metadata reported errors"
  cat /tmp/csb-validate.log
fi

echo
echo "=== 2. coverage-check ==="
if python3 $META/scripts/coverage-check.py --file coverage.md >/tmp/csb-coverage.log 2>&1; then
  ok "coverage.md schema-valid"
else
  fail "coverage-check failed"
  cat /tmp/csb-coverage.log
fi

echo
echo "=== 3. plugin.json + SNAPSHOT.lock parse cleanly ==="
if python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))" 2>/dev/null; then
  ok "plugin.json parses"
else
  fail "plugin.json malformed"
fi
if python3 -c "import yaml; yaml.safe_load(open('SNAPSHOT.lock'))" 2>/dev/null; then
  ok "SNAPSHOT.lock parses"
else
  fail "SNAPSHOT.lock malformed"
fi

echo
echo "=== 4. version triangulation (plugin.json ↔ SNAPSHOT.lock) ==="
plugin_v=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
snap_v=$(python3 -c "import yaml; print(yaml.safe_load(open('SNAPSHOT.lock'))['snapshot_version'])")
if [ "$plugin_v" = "$snap_v" ]; then
  ok "versions agree ($plugin_v)"
else
  fail "plugin.json=$plugin_v vs SNAPSHOT.lock=$snap_v"
fi

echo
echo "=== Summary ==="
if [ "$FAILED" -eq 0 ]; then
  printf "${green}PASS${reset} all checks clean across 4 steps.\n"
  exit 0
else
  printf "${red}FAIL${reset}\n"
  exit 1
fi
