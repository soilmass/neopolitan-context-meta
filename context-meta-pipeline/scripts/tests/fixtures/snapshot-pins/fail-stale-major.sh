#!/usr/bin/env bash
# fail-stale-major.sh — fixture harness for v0.6.1 check_depends_on_freshness.
#
# Constructs an in-memory snapshot where skill-b depends_on skill-a@0.1.5
# but skill-a is at 1.0.0 in the same snapshot. Should emit an error
# finding (MAJOR boundary crossed; pin is stale).

set -e

cd "$(dirname "$0")/../../../.."

actual=0
python3 -c "
import sys
sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('vm', 'scripts/validate-metadata.py')
vm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vm)

snap = {
    'skills': {
        'skill-a': {'version': '1.0.0', 'archetype': 'tool'},
        'skill-b': {
            'version': '0.2.0',
            'archetype': 'tool',
            'depends_on': ['skill-a@0.1.5'],
        },
    },
}
findings = list(vm.check_depends_on_freshness(snap))
errors = [f for f in findings if f.severity == 'error']
if not errors:
    print('expected at least one error finding for MAJOR-boundary pin drift')
    print(f'got {len(findings)} findings:')
    for f in findings:
        print(f'  [{f.severity}] {f.message}')
    sys.exit(1)
# Confirm the error message names the MAJOR boundary
matched = [e for e in errors if 'MAJOR' in e.message]
if not matched:
    print('error finding did not mention MAJOR boundary')
    for f in errors:
        print(f'  [{f.severity}] {f.message}')
    sys.exit(1)
print(f'fail-stale-major: error correctly emitted ({len(errors)} errors)')
" || actual=$?

if [ "$actual" -eq 0 ]; then
  echo "PASS fail-stale-major"
  exit 0
else
  echo "FAIL fail-stale-major (exit $actual)"
  exit 1
fi
