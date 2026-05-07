#!/usr/bin/env python3
"""
dummy-validator.py — extension-seam fixture exercising the validator
interface contract documented in governance/EXTENSION-POINTS.md §2.

This is NOT a runnable validator. It is a 30-line stub matching the
interface every script under scripts/*.py must follow:

  - argparse signature with --all, --skill (repeatable), --format json|text
  - exit codes 0 (clean) / 1 (findings) / 2 (invocation problem)
  - Finding(severity, message) dataclass
  - Report dataclass with to_text() / to_json() methods
  - PyYAML-only third-party dependency

verify.sh step 9 ast-parses this file and confirms the contract surface
is present. If a future PR adds a new validator that omits any of these,
the existing six validators in scripts/ would still pass step 9 — but
the new validator's existence implies the contract was understood. This
fixture stays self-documenting through that growth.

If the contract changes (e.g., --format gains a yaml option), this
fixture is updated alongside the validator that introduces the change.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class Finding:
    severity: str
    message: str


@dataclass
class Report:
    skill: str
    findings: list[Finding]

    def to_text(self) -> str:
        if not self.findings:
            return f"DUMMY VALIDATION PASSED for skill: {self.skill}\n"
        lines = [f"DUMMY VALIDATION FAILED for skill: {self.skill}\n"]
        for f in self.findings:
            lines.append(f"[{f.severity}] {f.message}\n")
        return "".join(lines)

    def to_json(self) -> str:
        return json.dumps({
            "skill": self.skill,
            "findings": [{"severity": f.severity, "message": f.message} for f in self.findings],
        })


def main() -> int:
    parser = argparse.ArgumentParser(description="dummy-validator (extension-seam fixture)")
    parser.add_argument("--all", action="store_true", help="validate all skills")
    parser.add_argument("--skill", action="append", default=[], help="validate one skill (repeatable)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    if not args.all and not args.skill:
        sys.stderr.write("error: --all or --skill required\n")
        return 2

    # This fixture never actually validates anything. It returns clean.
    report = Report(skill="dummy", findings=[])
    sys.stdout.write(report.to_json() if args.format == "json" else report.to_text())
    return 0 if not report.findings else 1


if __name__ == "__main__":
    sys.exit(main())
