#!/usr/bin/env bash
# warn-stale-minor.sh — fixture harness for v0.6.1 check_depends_on_freshness.
#
# skill-b depends_on skill-a@0.1.5; skill-a is at 0.2.0 (same MAJOR).
# Should emit a warning (floor-semantics OK; consider refreshing).

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
        'skill-a': {'version': '0.2.0', 'archetype': 'tool'},
        'skill-b': {
            'version': '0.1.0',
            'archetype': 'tool',
            'depends_on': ['skill-a@0.1.5'],
        },
    },
}
findings = list(vm.check_depends_on_freshness(snap))
warnings = [f for f in findings if f.severity == 'warning']
errors = [f for f in findings if f.severity == 'error']
if errors:
    print(f'unexpected error findings: {len(errors)}')
    for f in errors:
        print(f'  [error] {f.message}')
    sys.exit(1)
if not warnings:
    print('expected at least one warning for same-MAJOR pin lag')
    sys.exit(1)
print(f'warn-stale-minor: warning correctly emitted ({len(warnings)} warnings, 0 errors)')
" || actual=$?

if [ "$actual" -eq 0 ]; then
  echo "PASS warn-stale-minor"
  exit 0
else
  echo "FAIL warn-stale-minor (exit $actual)"
  exit 1
fi
