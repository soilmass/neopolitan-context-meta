#!/usr/bin/env python3
# pre-trigger build (v0.7.0); reassess when trigger fires per
# governance/INTEGRATION-TESTING.md (10+ skills with cross-deps + 2 regressions).
"""
integration-test-runner.py — execute YAML scenarios that compose existing
scripts and assert their exit codes / artifacts.

Per governance/INTEGRATION-TESTING.md. Mechanizes Health Gate 2 (test pass
rate) WHEN the trigger fires; until then, runs against synthetic scenarios
under scripts/tests/fixtures/integration/ for shape-validation only.

OUT OF SCOPE (M4 antipattern from v0.5.0 audit):
  - Mechanizing procedural skills (skill-author, skill-audit, etc.).
    Those skills are operator-driven by design. This runner only invokes
    *scripts*, never walks SKILL.md stages.

Scenario format:
```yaml
name: <scenario-name>
description: <one-line>
steps:
  - run: <shell command>
    expected_exit: 0   # optional, default 0
    expects_file: <path>  # optional; assert file exists after step
    expects_pattern: <regex>  # optional; assert stdout matches
```

Exit codes:
  0  all scenarios passed
  1  one or more scenarios failed (gate signal)
  2  invocation problem (no scenarios, malformed YAML, etc.)

Usage:
  integration-test-runner.py --suite scripts/tests/fixtures/integration/
  integration-test-runner.py --suite <dir> --format json

Dependencies: PyYAML (via _skill_io) + stdlib + subprocess.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    sys.stderr.write("error: PyYAML not installed.\n")
    sys.exit(2)


@dataclass
class StepResult:
    cmd: str
    expected_exit: int
    actual_exit: int
    passed: bool
    reason: str = ""


@dataclass
class ScenarioResult:
    name: str
    description: str
    steps: list[StepResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(s.passed for s in self.steps)


def run_scenario(scenario_path: Path, root: Path) -> ScenarioResult:
    text = scenario_path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        return ScenarioResult(
            name=str(scenario_path),
            description="(malformed scenario)",
            steps=[StepResult(cmd="", expected_exit=0, actual_exit=2, passed=False, reason="not a YAML mapping")],
        )
    name = str(data.get("name") or scenario_path.stem)
    description = str(data.get("description") or "")
    result = ScenarioResult(name=name, description=description)
    steps = data.get("steps") or []
    if not isinstance(steps, list):
        result.steps.append(
            StepResult(cmd="", expected_exit=0, actual_exit=2, passed=False,
                       reason="steps: must be a list")
        )
        return result
    for raw_step in steps:
        if not isinstance(raw_step, dict):
            continue
        cmd = str(raw_step.get("run") or "")
        expected_exit = int(raw_step.get("expected_exit", 0))
        expects_file = raw_step.get("expects_file")
        expects_pattern = raw_step.get("expects_pattern")

        # Run the command from the plugin root.
        proc = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=root,
        )
        actual_exit = proc.returncode
        passed = (actual_exit == expected_exit)
        reason = ""
        if not passed:
            reason = f"exit {actual_exit}, expected {expected_exit}"

        if passed and expects_file is not None:
            file_path = root / str(expects_file)
            if not file_path.exists():
                passed = False
                reason = f"expected_file {expects_file} not present"

        if passed and expects_pattern is not None:
            if not re.search(str(expects_pattern), proc.stdout):
                passed = False
                reason = f"stdout did not match pattern {expects_pattern!r}"

        result.steps.append(
            StepResult(
                cmd=cmd,
                expected_exit=expected_exit,
                actual_exit=actual_exit,
                passed=passed,
                reason=reason,
            )
        )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--suite", type=Path,
                        default=Path("scripts/tests/fixtures/integration"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.suite.is_dir():
        sys.stderr.write(f"error: suite directory {args.suite} not found\n")
        return 2

    scenarios = sorted(args.suite.glob("scenario-*.yaml"))
    if not scenarios:
        sys.stderr.write(f"error: no scenario-*.yaml under {args.suite}\n")
        return 2

    results: list[ScenarioResult] = []
    for s in scenarios:
        results.append(run_scenario(s, args.root))

    n_pass = sum(1 for r in results if r.passed)
    n_fail = len(results) - n_pass

    if args.format == "json":
        print(json.dumps(
            {
                "total": len(results),
                "passed": n_pass,
                "failed": n_fail,
                "scenarios": [
                    {
                        "name": r.name,
                        "description": r.description,
                        "passed": r.passed,
                        "steps": [
                            {
                                "cmd": s.cmd,
                                "expected_exit": s.expected_exit,
                                "actual_exit": s.actual_exit,
                                "passed": s.passed,
                                "reason": s.reason,
                            }
                            for s in r.steps
                        ],
                    }
                    for r in results
                ],
            },
            indent=2,
        ))
    else:
        for r in results:
            mark = "✓" if r.passed else "✗"
            print(f"{mark} {r.name}: {r.description}")
            for s in r.steps:
                step_mark = "✓" if s.passed else "✗"
                line = f"  {step_mark} {s.cmd}"
                if s.reason:
                    line += f"  | {s.reason}"
                print(line)
        print()
        print(f"INTEGRATION-TEST: {n_pass}/{len(results)} scenarios passed.")

    return 1 if n_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
