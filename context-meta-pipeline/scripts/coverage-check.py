#!/usr/bin/env python3
"""
coverage-check.py — validates a coverage.md file against the
library-root coverage.md schema.

Per the meta-pipeline's own coverage.md and family-bootstrap's
references/coverage-template.md, every coverage.md must have:
  - Last verification line near the top
  - Domains Claimed table
  - Domains Deferred table (with Build trigger column)
  - Domains Out of Scope table
  - Cross-Domain Orchestrators section
  - Coverage Matrix Status table
  - Out of Scope non-empty

Per-family coverage.md (produced by family-bootstrap Stage 6) has a
slightly different schema — see --schema family. This script enforces
the library-root schema by default.

Exit codes:
  0  coverage.md valid (warnings allowed)
  1  schema violation (blocks merge)
  2  invocation problem (file missing, etc.)

Usage:
  coverage-check.py --file coverage.md
  coverage-check.py --file skills/git/coverage.md --schema family
  coverage-check.py --file coverage.md --format json

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# v0.6.1: shared section splitter lives in _skill_io.
from _skill_io import split_h2_bodies
from typing import Any


LIBRARY_REQUIRED_SECTIONS = [
    "Domains Claimed",
    "Domains Deferred",
    "Domains Out of Scope",
    "Cross-Domain Orchestrators",
    "Coverage Matrix Status",
]

FAMILY_REQUIRED_SECTIONS = [
    "In Scope (Tier 1)",
    "Specced, Not Yet Built (Tier 2)",
    "Deferred (Tier 3)",
    "Policy Overlay",
    "Out of Scope",
    "Coverage Matrix Status",
]


@dataclass
class Finding:
    severity: str  # "error" | "warning"
    message: str

    def render_text(self) -> str:
        prefix = "[X]" if self.severity == "error" else "[!]"
        return f"{prefix} {self.message}"


@dataclass
class Report:
    path: str
    schema: str
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def add(self, f: Finding) -> None:
        (self.errors if f.severity == "error" else self.warnings).append(f)

    def render_text(self) -> str:
        if self.passed and not self.warnings:
            return f"COVERAGE-CHECK PASSED ({self.schema}) for {self.path}\n"
        header = f"COVERAGE-CHECK {'PASSED (with warnings)' if self.passed else 'FAILED'} ({self.schema}) for {self.path}\n\n"
        out = [header]
        if self.errors:
            out.append("Errors (block merge):\n")
            out.extend(f.render_text() + "\n" for f in self.errors)
            out.append("\n")
        if self.warnings:
            out.append("Warnings (do not block):\n")
            out.extend(f.render_text() + "\n" for f in self.warnings)
            out.append("\n")
        return "".join(out)

    def render_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "schema": self.schema,
            "errors": [f.message for f in self.errors],
            "warnings": [f.message for f in self.warnings],
            "passed": self.passed,
        }


# ---------------------------------------------------------------------------
# Section extraction (reused idiom from validate-metadata.py)
# ---------------------------------------------------------------------------


# split_h2_bodies imported from _skill_io at top of file. Removed v0.6.1.


def has_data_rows(section_text: str) -> bool:
    """Return True if the section has at least one markdown-table data row."""
    for line in section_text.splitlines():
        line = line.strip()
        # data row: pipe-bounded, not a separator, has non-trivial content
        if line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            # skip header rows by checking content variety
            non_empty = [c for c in cells if c]
            if non_empty and not all(c.lower() in {"capability", "domain", "atom", "owns", "intent", "target atom", "build trigger", "why deferred", "key concepts", "edge cases", "folds into", "last health check", "skill", "recency", "test pass", "triggering", "drift", "status"} for c in non_empty):
                return True
    return False


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_required_sections(text: str, schema: str) -> list[Finding]:
    findings: list[Finding] = []
    sections = split_h2_bodies(text)
    required = LIBRARY_REQUIRED_SECTIONS if schema == "library" else FAMILY_REQUIRED_SECTIONS
    for name in required:
        if not any(t == name or t.startswith(name) for t in sections):
            findings.append(Finding("error", f"Missing required section: ## {name}"))
    return findings


def check_out_of_scope_non_empty(text: str, schema: str) -> list[Finding]:
    sections = split_h2_bodies(text)
    name = "Domains Out of Scope" if schema == "library" else "Out of Scope"
    body = sections.get(name, "")
    if not body:
        return []  # missing section already reported
    if not has_data_rows(body):
        return [Finding("error", f"Section '## {name}' has no data rows; per the schema it must have ≥1 entry")]
    return []


def check_last_verification(text: str) -> list[Finding]:
    head = "\n".join(text.splitlines()[:30])
    if "Last verification:" not in head:
        return [Finding("warning", "No 'Last verification:' line in the first 30 lines; add a freshness marker")]
    return []


def check_deferred_has_triggers(text: str, schema: str) -> list[Finding]:
    sections = split_h2_bodies(text)
    name = "Domains Deferred" if schema == "library" else "Deferred (Tier 3)"
    body = sections.get(name, "")
    if not body:
        return []
    findings: list[Finding] = []
    # Look for table rows; each row should mention "Build trigger" content
    # (heuristic: contains "trigger" / "fires" / "when" / "if" in a verb-ish position)
    lines = [ln for ln in body.splitlines() if ln.strip().startswith("|") and "---" not in ln]
    if len(lines) < 2:
        return findings  # nothing to check
    # Check the header row references "Build trigger"
    header = lines[0].lower() if lines else ""
    if "build trigger" not in header and "trigger" not in header:
        findings.append(Finding(
            "warning",
            f"'## {name}' table header doesn't mention a 'Build trigger' column; per coverage-template.md "
            f"each Tier 3 / Deferred entry should have an observable build trigger",
        ))
    return findings


def check_coverage_matrix_status(text: str) -> list[Finding]:
    sections = split_h2_bodies(text)
    body = sections.get("Coverage Matrix Status", "")
    if not body:
        return []
    # Freshly-bootstrapped libraries (per library-bootstrap Stage 3) have no
    # skills yet — the section may legitimately say "No skills yet" or
    # equivalent stub. Suppress the verification-marker warning in that case.
    body_lower = body.lower()
    fresh_markers = ("no skills yet", "n/a", "fresh library", "initial bootstrap")
    if any(m in body_lower for m in fresh_markers):
        return []
    if "Last `skill-audit` run" not in body and "Last verification" not in body and "verification" not in body_lower:
        return [Finding(
            "warning",
            "'## Coverage Matrix Status' should include a 'Last skill-audit run' or 'verification' marker",
        )]
    return []


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def validate(path: Path, schema: str) -> Report:
    text = path.read_text(encoding="utf-8")
    report = Report(path=str(path), schema=schema)
    for f in check_required_sections(text, schema):
        report.add(f)
    for f in check_out_of_scope_non_empty(text, schema):
        report.add(f)
    for f in check_last_verification(text):
        report.add(f)
    for f in check_deferred_has_triggers(text, schema):
        report.add(f)
    for f in check_coverage_matrix_status(text):
        report.add(f)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--file", type=Path, required=True, help="path to a coverage.md file")
    parser.add_argument(
        "--schema",
        choices=("library", "family"),
        default="library",
        help="library = library-root coverage.md (default); family = per-family coverage.md (produced by family-bootstrap Stage 6)",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.file.is_file():
        sys.stderr.write(f"error: file not found: {args.file}\n")
        return 2

    report = validate(args.file, args.schema)

    if args.format == "json":
        print(json.dumps(report.render_json(), indent=2))
    else:
        print(report.render_text())

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
