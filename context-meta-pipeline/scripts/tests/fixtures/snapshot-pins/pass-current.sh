#!/usr/bin/env bash
# pass-current.sh — fixture harness for v0.6.1 check_depends_on_freshness.
#
# Constructs an in-memory snapshot dict with depends_on pins that match
# the targets' current versions, then asserts check_depends_on_freshness
# emits zero error findings.
#
# Pattern: capture exit under set -e via `actual=0; <cmd> || actual=$?`
# (mirrors rollback-skill fixture harnesses from v0.5.1).

set -e

cd "$(dirname "$0")/../../../.."

actual=0
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from importlib import import_module
mod = import_module('validate-metadata'.replace('-', '_'))
" 2>/dev/null || {
  # validate-metadata.py has a hyphen so it can't be imported by the standard
  # import machinery. Inline the function instead — keeps the fixture
  # self-contained and avoids hyphen-to-underscore aliasing tricks.
  python3 -c "
import sys
sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('vm', 'scripts/validate-metadata.py')
vm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vm)

snap = {
    'skills': {
        'skill-a': {'version': '0.1.5', 'archetype': 'tool'},
        'skill-b': {
            'version': '0.2.0',
            'archetype': 'tool',
            'depends_on': ['skill-a@0.1.5'],
        },
    },
}
findings = list(vm.check_depends_on_freshness(snap))
errors = [f for f in findings if f.severity == 'error']
warnings = [f for f in findings if f.severity == 'warning']
if errors or warnings:
    print(f'unexpected findings: {len(errors)} errors, {len(warnings)} warnings')
    for f in findings:
        print(f'  [{f.severity}] {f.message}')
    sys.exit(1)
print('pass-current: clean (no findings)')
" || actual=$?
}

if [ "$actual" -eq 0 ]; then
  echo "PASS pass-current"
  exit 0
else
  echo "FAIL pass-current (exit $actual)"
  exit 1
fi
