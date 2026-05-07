#!/usr/bin/env bash
# verify.sh — one-command self-check for the context-meta-pipeline plugin.
#
# Runs every check the library can actually run on itself:
#   1. validate-metadata.py against every live skill
#   2. validate-metadata.py against every SKILL.md fixture (pass + fail)
#   3. audit-skill.py against every live skill (Gate 1 + Gate 4)
#   4. version triangulation across plugin.json / marketplace.json / SNAPSHOT.lock / per-skill metadata
#   5. coverage-check.py against the library's own coverage.md  (v0.5.0+)
#   6. snapshot-diff.py sanity (against snapshot fixtures, no errors)  (v0.5.0+)
#
# Exit 0 if everything is clean. Exit 1 if any check fails (output names what).

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

green="\033[0;32m"; red="\033[0;31m"; yellow="\033[0;33m"; reset="\033[0m"
ok()   { printf "${green}OK${reset}    %s\n" "$1"; }
warn() { printf "${yellow}WARN${reset}  %s\n" "$1"; }
fail() { printf "${red}FAIL${reset}  %s\n" "$1"; FAILED=1; }

FAILED=0

echo "=== 1. validate-metadata.py against live skills ==="
if python3 scripts/validate-metadata.py --all >/tmp/verify-validate.out 2>&1; then
  ok "all $(grep -c PASSED /tmp/verify-validate.out) skills pass"
else
  fail "validate-metadata.py reported errors"
  cat /tmp/verify-validate.out
fi
echo

echo "=== 2. validate-metadata.py against fixture matrix ==="
# Iterate top-level entries in scripts/tests/fixtures/. Files are SKILL.md
# fixtures; directories are SKILL.md fixtures with references/ (must contain
# SKILL.md). Skip:
#   - Directories that don't contain a SKILL.md (subdirs hold non-SKILL fixtures
#     for other validators, e.g., fixtures/coverage/, fixtures/snapshot/).
#   - Non-.md files at the top level (e.g., .lock files, scratch).
fail_count=0
pass_count=0
for fixture in scripts/tests/fixtures/*; do
  if [ -f "$fixture" ]; then
    [[ "$fixture" == *.md ]] || continue
    name=$(basename "$fixture" .md)
    target="$fixture"
  elif [ -d "$fixture" ]; then
    [ -f "$fixture/SKILL.md" ] || continue
    name=$(basename "$fixture")
    target="$fixture/SKILL.md"
  else
    continue
  fi
  python3 scripts/validate-metadata.py --skill "$target" >/dev/null 2>&1
  exit_code=$?
  expected=0
  case "$name" in
    # Invocation-failure fixtures: malformed YAML, missing frontmatter, empty
    # frontmatter — the validator should report exit 2 (invocation problem)
    # rather than exit 1 (validation problem).
    *fail-empty-frontmatter*|*fail-missing-frontmatter*|*fail-malformed*)
      expected=2 ;;
    *fail*) expected=1 ;;
  esac
  if [ "$exit_code" -eq "$expected" ]; then
    pass_count=$((pass_count + 1))
  else
    fail "fixture $name: expected exit $expected, got $exit_code"
    fail_count=$((fail_count + 1))
  fi
done
if [ "$fail_count" -eq 0 ]; then
  ok "$pass_count SKILL.md fixtures behave correctly"
else
  fail "$fail_count fixture(s) misbehaved"
fi
echo

echo "=== 3. audit-skill.py against live skills ==="
if python3 scripts/audit-skill.py --all >/tmp/verify-audit.out 2>&1; then
  ok "all skills pass implementable health gates (recency + drift)"
else
  warn "audit-skill flagged skills (this is informational, not blocking):"
  grep -E "^FLAGGED|^=== |Description drift" /tmp/verify-audit.out | head -20
fi
echo

echo "=== 4. Version triangulation ==="
plugin_v=$(grep '"version"' .claude-plugin/plugin.json | head -1 | grep -oE '"[0-9.]+"' | tr -d '"')
market_v=$(grep '"version"' ../.claude-plugin/marketplace.json 2>/dev/null | head -1 | grep -oE '"[0-9.]+"' | tr -d '"' || echo "(not found)")
snap_v=$(grep '^snapshot_version' SNAPSHOT.lock | grep -oE '"[0-9.]+"' | tr -d '"')
echo "  plugin.json:        $plugin_v"
echo "  marketplace.json:   $market_v"
echo "  SNAPSHOT.lock:      $snap_v"
if [ "$plugin_v" = "$snap_v" ]; then
  ok "plugin and snapshot versions agree"
else
  fail "plugin.json ($plugin_v) and SNAPSHOT.lock ($snap_v) disagree"
fi
echo "  per-skill versions:"
for d in skills/*/; do
  name=$(basename "$d")
  v=$(awk '/^metadata:/{f=1; next} f && /version:/{print $2; f=0; exit}' "$d/SKILL.md" | tr -d '"')
  snap_skill_v=$(awk -v n="$name" '$0 ~ "^  "n":" {f=1; next} f && /version:/{print $2; f=0; exit}' SNAPSHOT.lock | tr -d '"')
  if [ "$v" = "$snap_skill_v" ]; then
    printf "    %-22s %s ✓\n" "$name" "$v"
  else
    fail "$name: SKILL.md=$v vs SNAPSHOT.lock=$snap_skill_v"
  fi
done
echo

echo "=== 5. coverage-check.py against the library's own coverage.md ==="
if python3 scripts/coverage-check.py --file coverage.md >/tmp/verify-coverage.out 2>&1; then
  ok "coverage.md schema-valid (library schema)"
else
  fail "coverage-check.py reported errors"
  cat /tmp/verify-coverage.out
fi
# Also smoke the coverage fixtures (3 in fixtures/coverage/).
if [ -d scripts/tests/fixtures/coverage ]; then
  cov_pass=0; cov_fail=0
  for cf in scripts/tests/fixtures/coverage/*.md; do
    [ -f "$cf" ] || continue
    name=$(basename "$cf" .md)
    expected=0; case "$name" in *fail*) expected=1 ;; esac
    python3 scripts/coverage-check.py --file "$cf" >/dev/null 2>&1
    actual=$?
    if [ "$actual" -eq "$expected" ]; then cov_pass=$((cov_pass+1)); else cov_fail=$((cov_fail+1)); fi
  done
  if [ "$cov_fail" -eq 0 ]; then
    ok "$cov_pass coverage fixtures behave correctly"
  else
    fail "$cov_fail coverage fixture(s) misbehaved"
  fi
fi
echo

echo "=== 6. snapshot-diff.py sanity (against fixture pair) ==="
if [ -f scripts/tests/fixtures/snapshot/snapshot-a.lock ] && [ -f scripts/tests/fixtures/snapshot/snapshot-b.lock ]; then
  if python3 scripts/snapshot-diff.py \
      --old scripts/tests/fixtures/snapshot/snapshot-a.lock \
      --new scripts/tests/fixtures/snapshot/snapshot-b.lock \
      --format json >/tmp/verify-snapdiff.out 2>&1; then
    if python3 -m json.tool /tmp/verify-snapdiff.out >/dev/null 2>&1; then
      ok "snapshot-diff.py produces valid JSON"
    else
      fail "snapshot-diff.py output is not valid JSON"
    fi
  else
    fail "snapshot-diff.py errored on fixture pair"
    cat /tmp/verify-snapdiff.out
  fi
else
  warn "snapshot fixture pair missing; skipping"
fi
echo

echo "=== 7. Script-script fixtures (breaking-changes / migration / rollback / audit) ==="

# 7a — detect-breaking-changes pair fixtures
bc_pass=0; bc_fail=0
for pair in scripts/tests/fixtures/breaking-changes/pair-*/; do
  [ -d "$pair" ] || continue
  pair_name=$(basename "$pair")
  baseline_rel=$(grep '^baseline:' "$pair/meta.yaml" | sed 's/^baseline: *//')
  expected=$(grep '^expected_exit:' "$pair/meta.yaml" | awk '{print $2}')
  baseline="$pair/$baseline_rel"
  snapshot_arg=""
  if [ -f "$pair/SNAPSHOT.lock" ]; then
    snapshot_arg="--snapshot $pair/SNAPSHOT.lock"
  fi
  python3 scripts/detect-breaking-changes.py --skill "$pair/MODIFIED.md" --baseline "$baseline" $snapshot_arg >/dev/null 2>&1
  actual=$?
  if [ "$actual" -eq "$expected" ]; then
    bc_pass=$((bc_pass + 1))
  else
    fail "BC pair $pair_name: expected exit $expected, got $actual"
    bc_fail=$((bc_fail + 1))
  fi
done
[ "$bc_fail" -eq 0 ] && ok "$bc_pass breaking-changes pairs behave correctly"

# 7b — migration-guide-gen pair fixtures + malformed YAML
mig_pass=0; mig_fail=0
for pair in scripts/tests/fixtures/migration/pair-*/; do
  [ -d "$pair" ] || continue
  pair_name=$(basename "$pair")
  baseline_rel=$(grep '^baseline:' "$pair/meta.yaml" | sed 's/^baseline: *//')
  baseline="$pair/$baseline_rel"
  out=$(python3 scripts/migration-guide-gen.py --old "$baseline" --new "$pair/MODIFIED.md" 2>&1)
  exit_code=$?
  missing=0
  while IFS= read -r fragment; do
    [ -z "$fragment" ] && continue
    echo "$out" | grep -qF "$fragment" || missing=$((missing + 1))
  done < "$pair/expected-fragments.txt"
  if [ "$exit_code" -eq 0 ] && [ "$missing" -eq 0 ]; then
    mig_pass=$((mig_pass + 1))
  else
    fail "migration pair $pair_name: exit $exit_code; missing $missing expected fragments"
    mig_fail=$((mig_fail + 1))
  fi
done
# malformed YAML separately — expect exit 2
python3 scripts/migration-guide-gen.py --old scripts/tests/fixtures/baselines/atom-baseline.md --new scripts/tests/fixtures/migration/fail-malformed-yaml.md >/dev/null 2>&1
malformed_exit=$?
if [ "$malformed_exit" -eq 2 ]; then
  mig_pass=$((mig_pass + 1))
else
  fail "migration fail-malformed-yaml: expected exit 2, got $malformed_exit"
  mig_fail=$((mig_fail + 1))
fi
[ "$mig_fail" -eq 0 ] && ok "$mig_pass migration cases behave correctly"

# 7c — rollback-skill harnesses (skip-with-warn if no git)
if command -v git >/dev/null 2>&1; then
  rb_pass=0; rb_fail=0
  for harness in scripts/tests/fixtures/rollback/*.sh; do
    [ -f "$harness" ] || continue
    if bash "$harness" >/dev/null 2>&1; then
      rb_pass=$((rb_pass + 1))
    else
      fail "rollback harness $(basename $harness) failed"
      rb_fail=$((rb_fail + 1))
    fi
  done
  [ "$rb_fail" -eq 0 ] && ok "$rb_pass rollback harnesses pass"
else
  warn "git not on PATH; skipping rollback harnesses"
fi

# 7d — audit-skill harnesses
au_pass=0; au_fail=0
for harness in scripts/tests/fixtures/audit/*.sh; do
  [ -f "$harness" ] || continue
  if bash "$harness" >/dev/null 2>&1; then
    au_pass=$((au_pass + 1))
  else
    fail "audit harness $(basename $harness) failed"
    au_fail=$((au_fail + 1))
  fi
done
[ "$au_fail" -eq 0 ] && ok "$au_pass audit harnesses pass"

# 7e — cross-skill handoff fixtures (Phase 2.2)
ho_dir="scripts/tests/fixtures/handoffs"
if [ -d "$ho_dir" ]; then
  ho_fail=0
  # family-bootstrap → skill-author: atom-count parity
  fb_intake="$ho_dir/family-bootstrap-to-skill-author/intake.yaml"
  fb_expected="$ho_dir/family-bootstrap-to-skill-author/expected-count.txt"
  if [ -f "$fb_intake" ] && [ -f "$fb_expected" ]; then
    n=$(python3 -c '
import sys, yaml
with open("'"$fb_intake"'") as f:
    data = yaml.safe_load(f) or {}
print(len(data.get("atoms", [])))
' 2>/dev/null) || n=""
    expected=$(tr -d '[:space:]' < "$fb_expected")
    if [ "$n" = "$expected" ] && [ -n "$n" ]; then
      ok "family-bootstrap→skill-author: $n atoms match expected $expected"
    else
      fail "family-bootstrap→skill-author: got '$n', expected '$expected'"
      ho_fail=$((ho_fail + 1))
    fi
  fi
  # skill-refactor → skill-retire: post-refactor sibling count parity
  rr_dir="$ho_dir/skill-refactor-to-skill-retire"
  rr_expected="$rr_dir/expected-count.txt"
  if [ -d "$rr_dir" ] && [ -f "$rr_expected" ]; then
    post=$(ls "$rr_dir"/after-*.md 2>/dev/null | wc -l | tr -d '[:space:]')
    expected=$(tr -d '[:space:]' < "$rr_expected")
    if [ "$post" = "$expected" ]; then
      ok "skill-refactor→skill-retire: $post siblings match expected $expected"
    else
      fail "skill-refactor→skill-retire: got '$post', expected '$expected'"
      ho_fail=$((ho_fail + 1))
    fi
  fi
fi

echo

echo "=== 8. CLI flag exercise (JSON output, alternate formats) ==="
cli_fail=0
# JSON output validates as JSON. We capture stdout (ignoring source exit code,
# which can be nonzero when the script fails its own threshold — e.g.,
# routing-eval-runner exits 1 when any skill is below the accuracy gate, but
# its stdout is still valid JSON).
for cmd in \
  "scripts/validate-metadata.py --all --format json" \
  "scripts/audit-skill.py --all --format json" \
  "scripts/coverage-check.py --file coverage.md --format json" \
  "scripts/snapshot-diff.py --old scripts/tests/fixtures/snapshot/snapshot-a.lock --new scripts/tests/fixtures/snapshot/snapshot-b.lock --format json" \
  "scripts/dependency-graph.py --format json" \
  "scripts/routing-eval-runner.py --mode static --format json"; do
  out=$(python3 $cmd 2>/dev/null || true)
  if ! printf '%s' "$out" | python3 -m json.tool >/dev/null 2>&1; then
    fail "CLI: $cmd → invalid JSON output"
    cli_fail=$((cli_fail + 1))
  fi
done
# repeatable --skill on audit-skill
python3 scripts/audit-skill.py --skill skill-author --skill skill-audit >/dev/null 2>&1 || { fail "audit-skill repeatable --skill failed"; cli_fail=$((cli_fail + 1)); }
# custom threshold path
python3 scripts/audit-skill.py --skill skill-author --recency-months 1 >/dev/null 2>&1 || { fail "audit-skill --recency-months failed"; cli_fail=$((cli_fail + 1)); }
# dependency-graph --format dot
python3 scripts/dependency-graph.py --format dot >/dev/null 2>&1 || { fail "dependency-graph --format dot failed"; cli_fail=$((cli_fail + 1)); }
# release-tag.sh dry-run path (will fail if verify.sh internally fails — we suppress)
# We don't recurse verify.sh from inside verify.sh; just test --help works
./scripts/release-tag.sh --help >/dev/null 2>&1 || { fail "release-tag.sh --help failed"; cli_fail=$((cli_fail + 1)); }
# v0.6.2: routing-eval-runner --mode external with --input fixture
ext_fixture="scripts/tests/fixtures/routing-eval-external/responses.json"
if [ -f "$ext_fixture" ]; then
  # exit 1 is expected (most prompts not in fixture); we just require it RUNS.
  python3 scripts/routing-eval-runner.py --mode external --input "$ext_fixture" >/dev/null 2>&1
  rc=$?
  if [ "$rc" -ne 0 ] && [ "$rc" -ne 1 ]; then
    fail "routing-eval-runner --mode external --input got exit $rc (expected 0 or 1)"
    cli_fail=$((cli_fail + 1))
  fi
fi
# v0.6.2: routing-eval-runner --mode operator with --operator-transcript fixture
op_fixture="scripts/tests/fixtures/routing-eval-operator/transcript.txt"
if [ -f "$op_fixture" ]; then
  python3 scripts/routing-eval-runner.py --mode operator --operator-transcript "$op_fixture" --skill skill-author >/dev/null 2>&1
  rc=$?
  if [ "$rc" -ne 0 ] && [ "$rc" -ne 1 ]; then
    fail "routing-eval-runner --mode operator --operator-transcript got exit $rc (expected 0 or 1)"
    cli_fail=$((cli_fail + 1))
  fi
fi
# v0.6.2: audit-skill --apply-banners --dry-run on live skills (no failures
# means no mutations would occur; this just exercises the code path).
python3 scripts/audit-skill.py --all --apply-banners --dry-run >/dev/null 2>&1 || { fail "audit-skill --apply-banners --dry-run failed"; cli_fail=$((cli_fail + 1)); }
[ "$cli_fail" -eq 0 ] && ok "all CLI invocations succeed; JSON outputs parse"

echo

echo "=== 9. Extension-seam contract checks (governance/EXTENSION-POINTS.md) ==="
seam_fail=0

# 9a — dummy-archetype: validator must reject unknown archetype
arch_fixture="scripts/tests/fixtures/extension-seams/dummy-archetype/SKILL.md"
if [ -f "$arch_fixture" ]; then
  out=$(python3 scripts/validate-metadata.py --skill "$arch_fixture" 2>&1 || true)
  if printf '%s' "$out" | grep -q "Unknown archetype"; then
    ok "dummy-archetype: validator rejects unknown archetype with explicit error"
  else
    fail "dummy-archetype: validator did not surface 'Unknown archetype' error"
    seam_fail=$((seam_fail + 1))
  fi
fi

# 9b — dummy-validator-shape: ast-parse confirms argparse contract surface
shape_fixture="scripts/tests/fixtures/extension-seams/dummy-validator-shape/dummy-validator.py"
if [ -f "$shape_fixture" ]; then
  if python3 -c "
import ast, sys
tree = ast.parse(open('$shape_fixture').read())
src = open('$shape_fixture').read()
required = ('--all', '--skill', '--format', 'json', 'text')
missing = [k for k in required if k not in src]
if missing:
    sys.stderr.write(f'missing keys: {missing}\n')
    sys.exit(1)
# confirm Finding + Report dataclasses present
classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
for c in ('Finding', 'Report'):
    if c not in classes:
        sys.stderr.write(f'missing class: {c}\n')
        sys.exit(1)
" 2>/dev/null; then
    ok "dummy-validator-shape: argparse keys + Finding/Report classes present"
  else
    fail "dummy-validator-shape: contract surface check failed"
    seam_fail=$((seam_fail + 1))
  fi
fi

# 9c — dummy-health-gate: ast-parse audit-skill.py and confirm gate_* shape
if python3 -c "
import ast, sys
tree = ast.parse(open('scripts/audit-skill.py').read())
gate_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('gate_')]
if not gate_funcs:
    sys.stderr.write('no gate_* functions found\n')
    sys.exit(1)
errs = []
for f in gate_funcs:
    if not (f.body and isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant) and isinstance(f.body[0].value.value, str)):
        errs.append(f'{f.name}: missing docstring')
    ann = f.returns
    if ann is None:
        errs.append(f'{f.name}: missing return annotation')
    elif not (isinstance(ann, ast.Name) and ann.id == 'GateResult'):
        errs.append(f'{f.name}: return annotation not GateResult')
if errs:
    for e in errs: sys.stderr.write(e + chr(10))
    sys.exit(1)
" 2>/dev/null; then
  ok "dummy-health-gate: all $(grep -c '^def gate_' scripts/audit-skill.py) gate_* functions match shape contract"
else
  fail "dummy-health-gate: gate_* shape contract violated"
  seam_fail=$((seam_fail + 1))
fi

[ "$seam_fail" -eq 0 ] && ok "all 3 extension seams hold"

echo

echo "=== 10. Synthesis check (taxonomy ↔ coverage sync against fixtures) ==="
syn_fail=0
syn_root="scripts/tests/fixtures/taxonomy-coverage"
if [ -d "$syn_root/matching" ]; then
  if python3 scripts/taxonomy-coverage-sync.py \
       --taxonomy "$syn_root/matching/taxonomy.md" \
       --coverage "$syn_root/matching/coverage.md" >/dev/null 2>&1; then
    ok "taxonomy-coverage matching fixture: aligned"
  else
    fail "taxonomy-coverage matching fixture: unexpected divergence"
    syn_fail=$((syn_fail + 1))
  fi
fi
if [ -d "$syn_root/divergent" ]; then
  # Divergent fixture is *expected* to exit 1 (drift detected). PASS the test
  # only when the script returns exit 1.
  python3 scripts/taxonomy-coverage-sync.py \
    --taxonomy "$syn_root/divergent/taxonomy.md" \
    --coverage "$syn_root/divergent/coverage.md" >/dev/null 2>&1
  rc=$?
  if [ "$rc" -eq 1 ]; then
    ok "taxonomy-coverage divergent fixture: drift correctly detected"
  else
    fail "taxonomy-coverage divergent fixture: expected exit 1, got $rc"
    syn_fail=$((syn_fail + 1))
  fi
fi

# v0.6.1 add-on: depends_on freshness fixtures (under scripts/tests/fixtures/snapshot-pins).
pin_fail=0
for h in scripts/tests/fixtures/snapshot-pins/*.sh; do
  [ -f "$h" ] || continue
  if bash "$h" >/dev/null 2>&1; then
    : # ok
  else
    fail "snapshot-pin harness $(basename "$h") failed"
    pin_fail=$((pin_fail + 1))
  fi
done
[ "$pin_fail" -eq 0 ] && [ -d "scripts/tests/fixtures/snapshot-pins" ] && ok "all $(ls scripts/tests/fixtures/snapshot-pins/*.sh 2>/dev/null | wc -l | tr -d '[:space:]') depends_on freshness harnesses pass"

echo

echo "=== 11. CHANGELOG sync (per-skill metadata.changelog ↔ CHANGELOG.md) ==="
if python3 scripts/changelog-sync.py >/tmp/verify-cs.out 2>&1; then
  ok "$(grep -oE '[0-9]+ skills checked' /tmp/verify-cs.out | head -1); no drift"
else
  fail "changelog-sync reported drift"
  head -20 /tmp/verify-cs.out
fi

# v0.6.2 add-on: audit-banners round-trip fixture.
if [ -f scripts/tests/fixtures/audit-banners/apply-roundtrip.sh ]; then
  if bash scripts/tests/fixtures/audit-banners/apply-roundtrip.sh >/dev/null 2>&1; then
    ok "audit-banners apply-roundtrip fixture: passes (banner + idempotent)"
  else
    fail "audit-banners apply-roundtrip fixture failed"
  fi
fi

echo

echo "=== 12. Snapshot integrity (snapshot-hash --verify) ==="
# v0.7.0 ahead-of-trigger build (governance/SKILL-PROVENANCE.md).
if python3 scripts/snapshot-hash.py --verify >/tmp/verify-hash.out 2>&1; then
  ok "$(grep -oE '[0-9]+ skill' /tmp/verify-hash.out | head -1) match SNAPSHOT.lock sha256"
else
  fail "snapshot-hash --verify reported mismatches"
  head -10 /tmp/verify-hash.out
fi

echo

echo "=== 13. Discoverability (gen-index --check) ==="
# v0.7.0 ahead-of-trigger build (governance/SKILL-DISCOVERABILITY.md).
if python3 scripts/gen-index.py --check >/tmp/verify-index.out 2>&1; then
  ok "INDEX.md is fresh"
else
  fail "INDEX.md is stale; run \`make index\`"
fi

echo

echo "=== 14. Integration scenarios (integration-test-runner.py) ==="
# v0.7.0 ahead-of-trigger build (governance/INTEGRATION-TESTING.md).
if python3 scripts/integration-test-runner.py >/tmp/verify-int.out 2>&1; then
  ok "$(grep -oE '[0-9]+/[0-9]+ scenarios passed' /tmp/verify-int.out)"
else
  fail "integration-test-runner reported failures"
  tail -10 /tmp/verify-int.out
fi

echo

echo "=== 15. Analytics rollup smoke (analytics-rollup.py) ==="
# v0.7.0 ahead-of-trigger build (governance/USAGE-ANALYTICS.md).
if python3 scripts/analytics-rollup.py --input scripts/tests/analytics/synthetic-events.jsonl --format json >/tmp/verify-an.out 2>&1; then
  if python3 -m json.tool </tmp/verify-an.out >/dev/null 2>&1; then
    ok "analytics rollup produces valid JSON ($(grep -oE '"total_events": [0-9]+' /tmp/verify-an.out | head -1))"
  else
    fail "analytics rollup output is not valid JSON"
  fi
else
  fail "analytics-rollup.py exited nonzero on synthetic fixture"
fi

echo

echo "=== Summary ==="
# v0.6.1: unified summary. Reports pass/fail across all steps in one line so
# CI consumers and humans get a single headline; per-step output above is the
# detailed source of truth.
if [ "$FAILED" -eq 0 ]; then
  printf "${green}PASS${reset} all checks clean across 15 steps "
  printf "(metadata + fixtures + audit + version triangulation + coverage + "
  printf "snapshot-diff + script-script fixtures + CLI exercise + extension-seams + "
  printf "synthesis + changelog-sync + snapshot-hash + discoverability + "
  printf "integration + analytics).\n"
  exit 0
else
  printf "${red}FAIL${reset} one or more checks reported errors. See above for which step(s) flagged.\n"
  exit 1
fi
