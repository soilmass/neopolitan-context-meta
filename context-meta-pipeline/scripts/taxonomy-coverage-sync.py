#!/usr/bin/env python3
"""
taxonomy-coverage-sync.py — verify that a family's `taxonomy.md`
(Stage 3 planning artifact) and `coverage.md` (Stage 6 ledger) agree
on which atoms are in which tier.

Per family-bootstrap/references/tier-model.md §"Artifact conventions"
(audit finding A9):
  - coverage.md = current state (source of truth for *now*)
  - taxonomy.md = original intent (source of truth for *why*)

Divergence is expected over time as `skill-author`, `skill-refactor`,
and `skill-retire` update coverage.md but not taxonomy.md. This script
surfaces divergence so the operator can decide:
  - The divergence is intentional (note it in taxonomy.md changelog).
  - The divergence is drift (re-align coverage.md or taxonomy.md).
  - The taxonomy needs to be regenerated (rare — Stage 3 of family-bootstrap).

Exit codes:
  0  taxonomy and coverage are aligned
  1  divergence detected (atoms in one but not the other; tier mismatches)
  2  invocation problem (file missing, malformed)

Usage:
  taxonomy-coverage-sync.py --taxonomy <family>/taxonomy.md --coverage <family>/coverage.md
  taxonomy-coverage-sync.py --taxonomy taxonomy.md --coverage coverage.md --format json

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# v0.6.1: shared section splitter lives in _skill_io.
from _skill_io import split_h2_bodies


@dataclass
class TierAtoms:
    tier_1: set[str] = field(default_factory=set)
    tier_2: set[str] = field(default_factory=set)
    tier_3: set[str] = field(default_factory=set)


@dataclass
class Diff:
    in_taxonomy_only: dict[str, set[str]] = field(default_factory=dict)
    in_coverage_only: dict[str, set[str]] = field(default_factory=dict)
    tier_mismatch: list[tuple[str, str, str]] = field(default_factory=list)  # (atom, taxonomy_tier, coverage_tier)

    @property
    def aligned(self) -> bool:
        return not (any(self.in_taxonomy_only.values()) or any(self.in_coverage_only.values()) or self.tier_mismatch)


# ---------------------------------------------------------------------------
# Section + atom-name extraction
# ---------------------------------------------------------------------------


# split_h2_bodies imported from _skill_io at top of file. Removed v0.6.1.


_ATOM_REGEX = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+){0,3})`")


def extract_atoms(section_text: str) -> set[str]:
    """Pull every backticked kebab-case identifier from a section's table."""
    atoms: set[str] = set()
    for line in section_text.splitlines():
        if not line.strip().startswith("|") or "---" in line:
            continue
        # Each row may have multiple atoms; we take the FIRST one (the row's primary atom).
        # This is a heuristic; see below.
        matches = _ATOM_REGEX.findall(line)
        if matches:
            atoms.add(matches[0])
    return atoms


def extract_taxonomy_tiers(text: str) -> TierAtoms:
    sections = split_h2_bodies(text)
    return TierAtoms(
        tier_1=extract_atoms(sections.get("Tier 1 — Essential", "")),
        tier_2=extract_atoms(sections.get("Tier 2 — Specced, Not Yet Built", "")),
        tier_3=extract_atoms(sections.get("Tier 3 — Deferred", "")),
    )


def extract_coverage_tiers(text: str) -> TierAtoms:
    sections = split_h2_bodies(text)
    return TierAtoms(
        tier_1=extract_atoms(sections.get("In Scope (Tier 1)", "")),
        tier_2=extract_atoms(sections.get("Specced, Not Yet Built (Tier 2)", "")),
        tier_3=extract_atoms(sections.get("Deferred (Tier 3)", "")),
    )


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------


def compute_diff(tax: TierAtoms, cov: TierAtoms) -> Diff:
    diff = Diff()
    for tier_name, tax_atoms, cov_atoms in [
        ("Tier 1", tax.tier_1, cov.tier_1),
        ("Tier 2", tax.tier_2, cov.tier_2),
        ("Tier 3", tax.tier_3, cov.tier_3),
    ]:
        only_tax = tax_atoms - cov_atoms
        only_cov = cov_atoms - tax_atoms
        if only_tax:
            diff.in_taxonomy_only[tier_name] = only_tax
        if only_cov:
            diff.in_coverage_only[tier_name] = only_cov

    # Tier mismatch: an atom that's in both but on different tiers
    tax_to_tier = {}
    for tier_name, atoms in [("Tier 1", tax.tier_1), ("Tier 2", tax.tier_2), ("Tier 3", tax.tier_3)]:
        for a in atoms:
            tax_to_tier[a] = tier_name
    cov_to_tier = {}
    for tier_name, atoms in [("Tier 1", cov.tier_1), ("Tier 2", cov.tier_2), ("Tier 3", cov.tier_3)]:
        for a in atoms:
            cov_to_tier[a] = tier_name
    for atom in sorted(set(tax_to_tier) & set(cov_to_tier)):
        if tax_to_tier[atom] != cov_to_tier[atom]:
            diff.tier_mismatch.append((atom, tax_to_tier[atom], cov_to_tier[atom]))
    return diff


def render_text(diff: Diff, taxonomy_path: Path, coverage_path: Path) -> str:
    out = [f"# Taxonomy ↔ Coverage sync: {taxonomy_path} vs {coverage_path}\n"]
    if diff.aligned:
        out.append("\nAligned. Every atom appears in both files at the same tier.\n")
        return "".join(out)
    if diff.in_taxonomy_only:
        out.append("\n## In taxonomy.md but missing from coverage.md\n")
        out.append("These atoms were planned at bootstrap but the family's coverage.md doesn't list them.\n")
        out.append("Either (a) authoring deferred them, (b) they were retired (move to coverage.md Retired section),\n")
        out.append("or (c) coverage.md drifted and needs the row back.\n")
        for tier, atoms in sorted(diff.in_taxonomy_only.items()):
            out.append(f"\n### {tier}\n")
            for a in sorted(atoms):
                out.append(f"  - `{a}`")
    if diff.in_coverage_only:
        out.append("\n\n## In coverage.md but missing from taxonomy.md\n")
        out.append("These atoms were added after bootstrap (via skill-author or skill-refactor).\n")
        out.append("Per the convention: coverage.md is current state; taxonomy.md is original intent.\n")
        out.append("Update taxonomy.md only if the change represents a meaningful rescoping.\n")
        for tier, atoms in sorted(diff.in_coverage_only.items()):
            out.append(f"\n### {tier}\n")
            for a in sorted(atoms):
                out.append(f"  - `{a}`")
    if diff.tier_mismatch:
        out.append("\n\n## Tier mismatch (atom present in both files but at different tiers)\n")
        for atom, tax_tier, cov_tier in diff.tier_mismatch:
            out.append(f"  - `{atom}`: taxonomy.md says {tax_tier}; coverage.md says {cov_tier}")
            out.append("    (likely a tier transition that taxonomy.md hasn't recorded; OK if intentional)")
    return "".join(out) + "\n"


def render_json(diff: Diff) -> str:
    return json.dumps({
        "aligned": diff.aligned,
        "in_taxonomy_only": {k: sorted(v) for k, v in diff.in_taxonomy_only.items()},
        "in_coverage_only": {k: sorted(v) for k, v in diff.in_coverage_only.items()},
        "tier_mismatch": [
            {"atom": a, "taxonomy_tier": t, "coverage_tier": c}
            for a, t, c in diff.tier_mismatch
        ],
    }, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--taxonomy", type=Path, required=True)
    parser.add_argument("--coverage", type=Path, required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.taxonomy.is_file():
        sys.stderr.write(f"error: taxonomy not found: {args.taxonomy}\n")
        return 2
    if not args.coverage.is_file():
        sys.stderr.write(f"error: coverage not found: {args.coverage}\n")
        return 2

    try:
        tax = extract_taxonomy_tiers(args.taxonomy.read_text(encoding="utf-8"))
        cov = extract_coverage_tiers(args.coverage.read_text(encoding="utf-8"))
    except OSError as e:
        sys.stderr.write(f"error reading: {e}\n")
        return 2

    diff = compute_diff(tax, cov)

    if args.format == "json":
        print(render_json(diff))
    else:
        print(render_text(diff, args.taxonomy, args.coverage))

    return 0 if diff.aligned else 1


if __name__ == "__main__":
    sys.exit(main())
