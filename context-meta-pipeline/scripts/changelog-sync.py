#!/usr/bin/env python3
"""
changelog-sync.py — cross-references per-skill metadata.changelog entries
against the library CHANGELOG.md.

The discipline (since v0.1.0): every per-skill version bump should produce
both a `metadata.changelog: |` entry in the skill's SKILL.md frontmatter AND
an entry in the library CHANGELOG.md for the release that ships the bump.
This script verifies the cross-reference holds.

Per `governance/GOVERNANCE.md` §"Adding a New Skill" and the v0.x release
ritual, the library CHANGELOG.md per-version blocks (## [X.Y.Z] - YYYY-MM-DD)
should mention any skill that received a content change in that release.
This script reads each skill's `metadata.changelog` entries and looks for
the corresponding skill name in the appropriate library CHANGELOG block.

Out of scope:
  - Auto-generating CHANGELOG entries from skill changelogs (operator-driven).
  - Validating the *content* of CHANGELOG entries against any rubric.
  - Validating CHANGELOG.md `[Unreleased]` block (drift expected there).

Exit codes:
  0  no drift detected
  1  one or more skills have changelog entries not reflected in CHANGELOG.md
  2  invocation problem (file missing, malformed, etc.)

Usage:
  changelog-sync.py
  changelog-sync.py --root /path/to/plugin
  changelog-sync.py --format json

Dependencies: PyYAML (via _skill_io) + stdlib.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# v0.6.1: shared parser + library walker.
from _skill_io import iter_live_skills, parse_skill


@dataclass
class Drift:
    skill: str
    skill_version: str
    skill_changelog_excerpt: str
    library_changelog_versions: list[str] = field(default_factory=list)
    reason: str = ""


# Per-skill `metadata.changelog: |` entries open with `vX.Y.Z — <descriptor>`.
SKILL_CHANGELOG_VERSION = re.compile(r"^v(\d+\.\d+\.\d+)\b", re.MULTILINE)
# Library CHANGELOG.md per-release blocks open with `## [X.Y.Z] - YYYY-MM-DD`.
LIBRARY_BLOCK_VERSION = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def parse_skill_changelog_versions(changelog_text: str) -> list[str]:
    """Extract every `vX.Y.Z` version that begins a skill changelog entry."""
    return list(SKILL_CHANGELOG_VERSION.findall(changelog_text))


def parse_library_block(text: str, version: str) -> str:
    """Return the body of the `## [<version>] - YYYY-MM-DD` block in CHANGELOG.md.

    Returns empty string if the block doesn't exist.
    """
    pattern = re.compile(
        rf'^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)',
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(text)
    return m.group(1) if m else ""


def find_drift(
    skill_dir: Path, skill_name: str, library_changelog: str
) -> list[Drift]:
    """For each skill changelog entry, check if its version is mentioned by
    name in the corresponding library CHANGELOG.md block.

    Heuristic: the library block for version X.Y.Z that ships the skill change
    should mention the skill by name (with or without backticks). We don't try
    to map skill versions to library versions exactly — we just check that for
    *some* recent library block, the skill name appears.

    Returns drift findings (one per skill changelog entry not reflected).
    """
    skill_md = skill_dir / "SKILL.md"
    try:
        doc = parse_skill(skill_md)
    except ValueError:
        return []
    meta = doc.frontmatter.get("metadata") or {}
    if not isinstance(meta, dict):
        return []
    changelog_text = meta.get("changelog") or ""
    if not isinstance(changelog_text, str) or not changelog_text.strip():
        return []
    versions = parse_skill_changelog_versions(changelog_text)
    library_versions = LIBRARY_BLOCK_VERSION.findall(library_changelog)
    drifts: list[Drift] = []
    for sv in versions:
        # Look for the skill name in any library block. If absent everywhere,
        # report drift. Acceptable hits: backtick-wrapped name, plain name in
        # a Health/Changed entry, or the name appearing in any Added/Removed
        # bullet for a release.
        skill_pattern = re.compile(
            rf'(?:`{re.escape(skill_name)}`|\b{re.escape(skill_name)}\b)'
        )
        seen_in: list[str] = []
        for lv in library_versions:
            block = parse_library_block(library_changelog, lv)
            if skill_pattern.search(block):
                seen_in.append(lv)
        if not seen_in:
            # Excerpt the skill changelog line for context.
            excerpt_match = re.search(
                rf'^v{re.escape(sv)}\s*—\s*(.+?)$',
                changelog_text,
                re.MULTILINE,
            )
            excerpt = excerpt_match.group(1).strip() if excerpt_match else "(no descriptor)"
            drifts.append(
                Drift(
                    skill=skill_name,
                    skill_version=sv,
                    skill_changelog_excerpt=excerpt[:120],
                    library_changelog_versions=library_versions,
                    reason=(
                        f"skill changelog has v{sv} but no library "
                        f"CHANGELOG.md block mentions {skill_name!r}"
                    ),
                )
            )
    return drifts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="plugin root (default: cwd)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    changelog_path = args.root / "CHANGELOG.md"
    if not changelog_path.is_file():
        sys.stderr.write(f"error: {changelog_path} not found\n")
        return 2
    library_changelog = changelog_path.read_text(encoding="utf-8")

    all_drifts: list[Drift] = []
    skill_count = 0
    for skill_md in iter_live_skills(args.root):
        skill_count += 1
        skill_name = skill_md.parent.name
        all_drifts.extend(find_drift(skill_md.parent, skill_name, library_changelog))

    if args.format == "json":
        print(json.dumps(
            {
                "skills_checked": skill_count,
                "drift_count": len(all_drifts),
                "drifts": [
                    {
                        "skill": d.skill,
                        "version": d.skill_version,
                        "excerpt": d.skill_changelog_excerpt,
                        "reason": d.reason,
                    }
                    for d in all_drifts
                ],
            },
            indent=2,
        ))
    else:
        if not all_drifts:
            print(f"CHANGELOG-SYNC PASSED: {skill_count} skills checked; no drift.")
        else:
            print(f"CHANGELOG-SYNC FAILED: {skill_count} skills checked; {len(all_drifts)} drift(s):")
            for d in all_drifts:
                print(f"  [{d.skill} v{d.skill_version}] {d.reason}")
                print(f"    excerpt: {d.skill_changelog_excerpt}")

    return 1 if all_drifts else 0


if __name__ == "__main__":
    sys.exit(main())
