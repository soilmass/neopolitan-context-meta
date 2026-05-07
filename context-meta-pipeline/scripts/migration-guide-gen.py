#!/usr/bin/env python3
"""
migration-guide-gen.py — generate a draft MIGRATION-v<NEW>.md from a
structural diff between two versions of a single SKILL.md.

Per VERSIONING-POLICY.md §"Migration Guides", every MAJOR version bump
produces a migration guide. This script implements the auto-generation
half. The author reviews and adds context (rationale, examples, known
incompatibilities) before shipping. The reviewed guide ships at
`<skill-directory>/MIGRATION-v<NEW>.md`.

The diff covers:
  - Frontmatter changes (renamed/removed fields, type changes)
  - Section changes (removed sections, restructured / renamed sections)
  - Capability changes (atoms only): added, removed, moved
  - Routing changes (routers only): added entries, removed entries, target changes

This script is a pure structural diff; it cannot know intent. The output
is always a draft.

Exit codes:
  0  draft produced
  2  invocation problem (file missing, malformed YAML, etc.)

Usage:
  migration-guide-gen.py --old skill-author/SKILL.md@v1 --new skill-author/SKILL.md
  migration-guide-gen.py --old <path> --new <path> --output MIGRATION-v2.md

Dependencies: PyYAML + stdlib.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# v0.6.1: shared parser + section splitter live in _skill_io.
from _skill_io import parse_skill_text, split_h2_bodies


@dataclass
class SkillSnapshot:
    name: str
    version: str
    archetype: str
    description: str
    frontmatter: dict[str, Any]
    sections: dict[str, str]


def parse(text: str) -> SkillSnapshot:
    """Parse a SKILL.md text into a SkillSnapshot. Uses _skill_io shared parser."""
    fm, body = parse_skill_text(text, source="<migration-guide-gen input>")
    sections = split_h2_bodies(body)
    meta = fm.get("metadata") or {}
    return SkillSnapshot(
        name=str(fm.get("name", "?")),
        version=str(meta.get("version", "?")),
        archetype=str(meta.get("archetype", "atom")),
        description=str(fm.get("description", "")).strip(),
        frontmatter=fm,
        sections=sections,
    )


# split_h2_bodies imported from _skill_io at top of file.


def extract_bullets(section_text: str) -> list[str]:
    bullets: list[str] = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            text = line[2:].strip()
            for sep in (":", " — ", " - "):
                if sep in text:
                    text = text.split(sep, 1)[0]
                    break
            bullets.append(text.strip("`* ").strip())
    return [b for b in bullets if b]


def extract_routing_table(section_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in section_text.splitlines():
        line = line.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip(" `*") for c in line.strip("|").split("|") if c.strip()]
        if len(cells) >= 2 and cells[0].lower() not in {"intent", "target atom"}:
            rows[cells[0]] = cells[1]
    return rows


@dataclass
class MigrationDraft:
    name: str
    old_version: str
    new_version: str
    frontmatter_changes: list[str] = field(default_factory=list)
    section_changes: list[str] = field(default_factory=list)
    capability_changes: list[str] = field(default_factory=list)
    routing_changes: list[str] = field(default_factory=list)


def diff(old: SkillSnapshot, new: SkillSnapshot) -> MigrationDraft:
    draft = MigrationDraft(
        name=new.name,
        old_version=old.version,
        new_version=new.version,
    )

    # Frontmatter
    if old.name != new.name:
        draft.frontmatter_changes.append(
            f"`name` changed: `{old.name}` → `{new.name}`. Every skill that referenced "
            f"the old name in routing tables, lockfiles, or handoff prose must update."
        )
    if old.frontmatter.get("license") != new.frontmatter.get("license"):
        draft.frontmatter_changes.append(
            f"`license` changed: {old.frontmatter.get('license')!r} → {new.frontmatter.get('license')!r}."
        )
    if old.frontmatter.get("model") != new.frontmatter.get("model"):
        draft.frontmatter_changes.append(
            f"`model` changed: {old.frontmatter.get('model')!r} → {new.frontmatter.get('model')!r}. "
            f"Downstream skills assuming specific model behavior must verify."
        )
    old_tools = set(_as_list(old.frontmatter.get("allowed-tools")))
    new_tools = set(_as_list(new.frontmatter.get("allowed-tools")))
    removed_tools = old_tools - new_tools
    if removed_tools:
        draft.frontmatter_changes.append(
            f"`allowed-tools` removed: {sorted(removed_tools)}. "
            f"Downstream skills that relied on these tools being available must update."
        )
    # Description rewrite >30%
    if old.description and new.description:
        delta = abs(len(old.description) - len(new.description)) / max(len(old.description), 1)
        if delta > 0.30:
            draft.frontmatter_changes.append(
                f"`description` rewritten by {int(delta*100)}% character delta. Review for breaking shift "
                f"in trigger phrases or anti-trigger surface."
            )

    # Section removal / addition
    old_sections = set(old.sections)
    new_sections = set(new.sections)
    for s in sorted(old_sections - new_sections):
        draft.section_changes.append(f"Removed: `## {s}`. Downstream skills that linked to this section must redirect.")
    for s in sorted(new_sections - old_sections):
        draft.section_changes.append(f"Added: `## {s}` (additive — no migration action required).")

    # Capabilities (atoms)
    if new.archetype == "atom":
        old_caps = set(extract_bullets(old.sections.get("Capabilities Owned", "")))
        new_caps = set(extract_bullets(new.sections.get("Capabilities Owned", "")))
        for cap in sorted(old_caps - new_caps):
            draft.capability_changes.append(
                f"Removed capability: `{cap}`. Operators who relied on this should locate the "
                f"capability in a sibling skill (verify with `audit-skill` or by inspection)."
            )
        for cap in sorted(new_caps - old_caps):
            draft.capability_changes.append(f"Added capability: `{cap}` (additive).")

    # Routing (routers)
    if new.archetype == "router":
        old_table = extract_routing_table(old.sections.get("Routing Table", ""))
        new_table = extract_routing_table(new.sections.get("Routing Table", ""))
        for intent, target in old_table.items():
            if intent not in new_table:
                draft.routing_changes.append(f"Routing entry removed: `{intent}` → `{target}`.")
            elif new_table[intent] != target:
                draft.routing_changes.append(
                    f"Routing target changed: `{intent}` → `{target}` is now `{new_table[intent]}`."
                )
        for intent, target in new_table.items():
            if intent not in old_table:
                draft.routing_changes.append(f"Routing entry added: `{intent}` → `{target}` (additive).")

    return draft


def _as_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


def render(draft: MigrationDraft) -> str:
    out = [
        f"# Migration: {draft.name} v{draft.old_version} → v{draft.new_version}\n",
        "",
        "> **DRAFT** — auto-generated from a structural diff. The author should",
        "> add: rationale (why was this change made?), worked examples, known",
        "> incompatibilities the diff missed, and a suggested timeline for users",
        "> who want to delay migration.",
        "",
    ]
    if draft.frontmatter_changes:
        out.append("## Frontmatter changes\n")
        for c in draft.frontmatter_changes:
            out.append(f"- {c}")
        out.append("")
    if draft.capability_changes:
        out.append("## Capability changes\n")
        for c in draft.capability_changes:
            out.append(f"- {c}")
        out.append("")
    if draft.routing_changes:
        out.append("## Routing changes\n")
        for c in draft.routing_changes:
            out.append(f"- {c}")
        out.append("")
    if draft.section_changes:
        out.append("## Section changes\n")
        for c in draft.section_changes:
            out.append(f"- {c}")
        out.append("")

    if not (draft.frontmatter_changes or draft.capability_changes or draft.routing_changes or draft.section_changes):
        out.append("No structural changes detected. This may not need a MAJOR bump — verify with")
        out.append("`detect-breaking-changes.py` before shipping.")
        out.append("")

    out.append("## Author notes\n")
    out.append("<!-- Add: rationale, worked examples, known incompatibilities, timeline. -->")
    out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--old", type=Path, required=True, help="path to the old SKILL.md")
    parser.add_argument("--new", type=Path, required=True, help="path to the new SKILL.md")
    parser.add_argument("--output", type=Path, help="optional path to write the draft (default: stdout)")
    args = parser.parse_args(argv)

    if not args.old.is_file():
        sys.stderr.write(f"error: --old not found: {args.old}\n")
        return 2
    if not args.new.is_file():
        sys.stderr.write(f"error: --new not found: {args.new}\n")
        return 2

    try:
        old = parse(args.old.read_text(encoding="utf-8"))
        new = parse(args.new.read_text(encoding="utf-8"))
    except ValueError as e:
        # _skill_io.parse_skill_text wraps yaml.YAMLError into ValueError, so
        # ValueError covers both malformed YAML and structural issues.
        sys.stderr.write(f"error parsing: {e}\n")
        return 2

    draft = diff(old, new)
    text = render(draft)

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
