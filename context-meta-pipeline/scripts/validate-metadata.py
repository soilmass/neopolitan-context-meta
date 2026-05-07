#!/usr/bin/env python3
"""
validate-metadata.py — implements governance/METADATA-VALIDATION.md.

Validates a SKILL.md against the universal frontmatter rules, archetype-
specific required-section lists, and reference-file constraints.

Exit codes:
  0  all checks passed (warnings allowed)
  1  at least one error (blocks merge)
  2  invocation problem (file missing, malformed YAML, etc.)

Usage:
  validate-metadata.py --skill <path-to-SKILL.md-or-skill-dir>
  validate-metadata.py --all                 # all skills under ./skills/
  validate-metadata.py --skill <path> --archetype atom
  validate-metadata.py --all --format json

Dependencies: PyYAML + stdlib.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


# v0.6.1: shared parser + Finding/Report dataclasses live in _skill_io.
# Finding and Report are *re-exported* here at module top-level via PEP 484
# `import as` to preserve the dummy-validator-shape extension-seam fixture
# (verify.sh §9b ast-walks this file for ClassDef nodes named "Finding" and
# "Report"). The classes themselves live in _skill_io; this module imports
# them and exposes them under the same names.
from _skill_io import (
    ARCHETYPES as ARCHETYPES,
    Finding as Finding,
    Report as Report,
    SkillDoc as SkillDoc,
    detect_archetype as _detect_archetype_shared,
    parse_skill as _parse_skill_shared,
    parse_skill_text as parse_skill_text,
    split_h2_bodies as _split_h2_bodies,
)

ARCHETYPE_REQUIRED_SECTIONS: dict[str, list[str]] = {
    "atom": [
        "When to Use",
        "When NOT to Use",
        "Capabilities Owned",
        "Handoffs to Other Skills",
        "Edge Cases",
        "References",
    ],
    "tool": [
        "Purpose",
        "When to Use",
        "When NOT to Use",
        "Stage-Gated Procedure",
        "Dependencies",
        "Evaluation",
        "Handoffs",
    ],
    "router": [
        "When to Use",
        "When NOT to Use",
        "Routing Table",
        "Disambiguation Protocol",
        "Atoms in This Family",
    ],
    "orchestrator": [
        "Purpose",
        "When to Use",
        "When NOT to Use",
        "The Stages",
        "Skills Coordinated",
        "Failure Modes",
        "Handoffs",
    ],
    "policy": [
        "Purpose",
        "Applies On Top Of",
        "Conventions Enforced",
        "Override Behavior",
    ],
}

# Universal frontmatter rules
NAME_REGEX = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$")  # ≤4 segments
# Heuristic for "no version numbers in skill names" (naming.md):
# matches any name segment shaped like a version literal (`v2`, `2`, `v1.0`).
NAME_VERSION_SEGMENT_REGEX = re.compile(r"(?:^|-)v?\d+(?:\.\d+)*(?:-|$)")
# SemVer 2.0 (semver.org): MAJOR.MINOR.PATCH with optional `-pre.release` and
# optional `+build.metadata`, in either order on the spec but pre-release
# always precedes build when both present. Allow combined `-pre+build`.
SEMVER_REGEX = re.compile(r"^\d+\.\d+\.\d+(?:-[\w.-]+)?(?:\+[\w.-]+)?$")
DESCRIPTION_MAX = 1024
ANTI_TRIGGER_PHRASES = ("Do NOT use for", "Do not use for", "do NOT use for")
BODY_MAX_LINES = 500
REFERENCE_MAX_LINES = 1000
REFERENCE_TOC_THRESHOLD = 300
# Reference chaining: any references/X.md link inside a references/*.md file
# violates METADATA-VALIDATION.md "References must not chain".
REFERENCE_CHAIN_REGEX = re.compile(r"references/[a-zA-Z0-9_.-]+\.md")
# Match any-level markdown heading containing "table of contents", "contents", or "toc".
_TOC_HEADING_REGEX = re.compile(r"^#{1,6}\s+(table of contents|contents|toc)\b", re.MULTILINE)


# Finding, Report, SkillDoc, parse_skill, parse_skill_text, ARCHETYPES are
# imported from _skill_io at the top of this file. Local thin wrappers preserve
# the existing call shape (validate-metadata's detect_archetype takes a SkillDoc;
# _skill_io's takes a frontmatter dict — translate at the boundary).


def parse_skill(path: Path) -> SkillDoc:
    """Parse a SKILL.md from a path. Thin wrapper over _skill_io.parse_skill
    that keeps validate-metadata's existing API stable."""
    return _parse_skill_shared(path)


def detect_archetype(doc: SkillDoc, override: str | None) -> str:
    """Wrapper accepting a SkillDoc (validate-metadata's existing API)."""
    return _detect_archetype_shared(doc.frontmatter, override)


def check_tags(doc: SkillDoc) -> Iterable[Finding]:
    """v0.7.0: validate `metadata.tags` if present.

    Optional field. When present, must be a list of kebab-case strings
    matching `^[a-z][a-z0-9-]*$`. Cap at 5 tags. The canonical tag taxonomy
    is documented in skills/skill-author/references/frontmatter-spec.md
    §"metadata.tags". This validator is *shape-only*: it doesn't enforce
    that tags come from the canonical list (consumer libraries may extend
    the taxonomy), only that they're well-formed strings.

    Pre-trigger discipline: `search-skills.py` and `gen-index.py` ship as
    part of v0.7.0 ahead of the formal SKILL-DISCOVERABILITY.md trigger
    (50+ skills). The `metadata.tags` field is the input both consume.
    """
    meta = doc.frontmatter.get("metadata", {})
    if not isinstance(meta, dict):
        return
    tags = meta.get("tags")
    if tags is None:
        return  # absent is fine
    if not isinstance(tags, list):
        yield Finding(
            "error",
            f"metadata.tags must be a list, got {type(tags).__name__}",
        )
        return
    if len(tags) > 5:
        yield Finding(
            "warning",
            f"metadata.tags has {len(tags)} entries; cap is 5 (see "
            f"skills/skill-author/references/frontmatter-spec.md).",
        )
    tag_pattern = re.compile(r"^[a-z][a-z0-9-]*$")
    for tag in tags:
        if not isinstance(tag, str):
            yield Finding(
                "error",
                f"metadata.tags entry must be a string, got {type(tag).__name__}: {tag!r}",
            )
            continue
        if not tag_pattern.match(tag):
            yield Finding(
                "error",
                f"metadata.tags entry {tag!r} is not kebab-case "
                f"(must match ^[a-z][a-z0-9-]*$).",
            )


def check_recency_pin_value(doc: SkillDoc) -> Iterable[Finding]:
    """v0.6.2: warn if `metadata.recency_pin` is present but not the only
    documented value (`stable`).

    Per `skills/skill-author/references/frontmatter-spec.md`, recency_pin is an
    optional escape hatch for skills whose authors consider them complete. The
    only documented value is `stable`. Future values may be added (e.g.,
    `legacy`, `frozen`), but for v0.6.2 the field is single-valued.
    `audit-skill.py:gate_recency` only acts on `stable`; any other value is
    silently ignored, which is exactly the kind of write-only field the v0.6.1
    inventory flagged. This check surfaces the case at validation time.
    """
    meta = doc.frontmatter.get("metadata", {})
    if not isinstance(meta, dict):
        return
    pin = meta.get("recency_pin")
    if pin is None:
        return
    if not isinstance(pin, str):
        yield Finding(
            "error",
            f"metadata.recency_pin must be a string, got {type(pin).__name__}",
        )
        return
    if pin != "stable":
        yield Finding(
            "warning",
            f"metadata.recency_pin: {pin!r} is not a documented value. The "
            f"only value gate_recency acts on is 'stable'. See "
            f"skills/skill-author/references/frontmatter-spec.md.",
        )


def check_archetype_known(doc: SkillDoc) -> Iterable[Finding]:
    """v0.6.0 (extension-seam #1): the archetype enumeration is closed at five.
    Authoring a 6th archetype is OUT OF SCOPE per governance/EXTENSION-POINTS.md
    §4 — it would be a MAJOR refactor. An unknown `archetype:` value silently
    falling through to `atom` is exactly the kind of seam slip this check
    prevents."""
    meta = doc.frontmatter.get("metadata", {})
    if not isinstance(meta, dict):
        return
    archetype_value = meta.get("archetype")
    if not isinstance(archetype_value, str):
        return
    a = archetype_value.lower()
    if a not in ARCHETYPES:
        yield Finding(
            "error",
            f"Unknown archetype {archetype_value!r}; "
            f"expected one of {ARCHETYPES}. Per governance/EXTENSION-POINTS.md §4, "
            f"adding a 6th archetype is OUT OF SCOPE at v0.6.0 — it would be a "
            f"MAJOR refactor. If you intended one of the five canonical archetypes, "
            f"check spelling.",
        )


# ---------------------------------------------------------------------------
# Library-wide checks (require --all because they need cross-skill context)
# ---------------------------------------------------------------------------


def _parse_pin(pin: str) -> tuple[str, str] | None:
    """Parse a depends_on pin like 'skill-author@0.1.5' into (name, version).
    Returns None if the pin doesn't have an `@` separator."""
    if "@" not in pin:
        return None
    name, _, version = pin.partition("@")
    return name.strip(), version.strip()


def _parse_semver(v: str) -> tuple[int, int, int] | None:
    """Parse 'X.Y.Z' (or 'X.Y.Z-suffix') into a tuple of ints. Returns None
    if it doesn't look like a SemVer prefix."""
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-.*)?$", v.strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def check_depends_on_freshness(snapshot: dict[str, Any]) -> Iterable[Finding]:
    """v0.6.1: catch stale `depends_on:` pins.

    A pin like `skill-author@0.1.5` records that the dependent expected
    skill-author at version 0.1.5 (or compatible) when authored. Per
    library-audit's v0.5.2 pinned-version semantics: a pin is satisfied
    when the target's current version is >= pinned AND the leading
    SemVer segment matches (no MAJOR boundary crossed).

    This check flags pins that have drifted: the pinned version is older
    than the target's current version AND a MAJOR boundary has been
    crossed. The dependent's metadata.changelog likely needs an entry
    acknowledging the new MAJOR version of the dependency.

    A drift within the same MAJOR is a warning (potentially OK; floor
    semantics). A MAJOR jump is an error (depends_on is now stale).
    """
    skills = snapshot.get("skills") or {}
    if not isinstance(skills, dict):
        return
    # Build a name → current-version map.
    current: dict[str, str] = {}
    for name, spec in skills.items():
        if isinstance(spec, dict):
            v = spec.get("version")
            if isinstance(v, str):
                current[name] = v

    for dependent_name, spec in skills.items():
        if not isinstance(spec, dict):
            continue
        deps = spec.get("depends_on") or []
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if not isinstance(dep, str):
                continue
            parsed = _parse_pin(dep)
            if parsed is None:
                continue
            target_name, pinned_version = parsed
            target_current = current.get(target_name)
            if target_current is None:
                yield Finding(
                    "error",
                    f"depends_on freshness: {dependent_name}'s pin "
                    f"`{target_name}@{pinned_version}` references a skill not "
                    f"present in SNAPSHOT.lock.",
                )
                continue
            pin_sv = _parse_semver(pinned_version)
            cur_sv = _parse_semver(target_current)
            if pin_sv is None or cur_sv is None:
                # Non-SemVer; can't compare. Skip.
                continue
            if pin_sv == cur_sv:
                continue  # Pin is current.
            if pin_sv > cur_sv:
                yield Finding(
                    "error",
                    f"depends_on freshness: {dependent_name}'s pin "
                    f"`{target_name}@{pinned_version}` is NEWER than current "
                    f"`{target_name}@{target_current}` — pin from the future is "
                    f"a SNAPSHOT.lock authoring error.",
                )
                continue
            # pin_sv < cur_sv. Same MAJOR is warning; MAJOR jump is error.
            if pin_sv[0] != cur_sv[0]:
                yield Finding(
                    "error",
                    f"depends_on freshness: {dependent_name}'s pin "
                    f"`{target_name}@{pinned_version}` crosses a MAJOR boundary "
                    f"vs current `{target_name}@{target_current}`. Dependent "
                    f"must update the pin and acknowledge the breaking change "
                    f"in its metadata.changelog.",
                )
            else:
                yield Finding(
                    "warning",
                    f"depends_on freshness: {dependent_name}'s pin "
                    f"`{target_name}@{pinned_version}` lags current "
                    f"`{target_name}@{target_current}` (same MAJOR; floor-"
                    f"semantics OK but consider refreshing the pin).",
                )


# ---------------------------------------------------------------------------
# Per-skill checks
# ---------------------------------------------------------------------------


def check_frontmatter(doc: SkillDoc) -> Iterable[Finding]:
    fm = doc.frontmatter
    name = fm.get("name")
    if not isinstance(name, str):
        yield Finding("error", "Frontmatter `name` missing or not a string")
    elif not NAME_REGEX.match(name):
        yield Finding(
            "error",
            f"Frontmatter `name` {name!r} fails naming regex "
            f"(lowercase, kebab-case, ≤4 segments)",
        )
    elif NAME_VERSION_SEGMENT_REGEX.search(f"-{name}-"):
        # Heuristic: catch name segments shaped like version literals.
        # naming.md forbids version numbers in skill names.
        yield Finding(
            "warning",
            f"Frontmatter `name` {name!r} contains a segment that looks like "
            f"a version literal (e.g., 'v2', '1.0'); per naming.md, version "
            f"numbers belong in `metadata.version`, not the name",
        )

    desc = fm.get("description")
    if not isinstance(desc, str):
        yield Finding("error", "Frontmatter `description` missing or not a string")
    else:
        if len(desc) > DESCRIPTION_MAX:
            yield Finding(
                "error",
                f"Description exceeds {DESCRIPTION_MAX} characters (currently {len(desc)})",
            )
        if not any(p in desc for p in ANTI_TRIGGER_PHRASES):
            yield Finding(
                "error",
                "Description missing 'Do NOT use for' anti-trigger block",
            )
        # Description quality warnings
        first_word = desc.strip().split(" ", 1)[0].lower() if desc.strip() else ""
        if first_word in {"i", "you", "we"}:
            yield Finding(
                "warning",
                f"Description starts with first/second-person pronoun ({first_word!r}); prefer third-person",
            )
        if isinstance(name, str) and name and name.lower() == desc.strip().lower()[: len(name)]:
            yield Finding(
                "warning",
                "Description appears to start with the skill name verbatim; explain rather than restate",
            )

    if "license" not in fm:
        yield Finding("error", "Frontmatter `license` missing")

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        yield Finding("error", "Frontmatter `metadata` missing or not a mapping")
        return  # downstream metadata checks meaningless
    version = meta.get("version")
    if not isinstance(version, str):
        yield Finding("error", "Frontmatter `metadata.version` missing or not a string")
    elif not SEMVER_REGEX.match(version):
        yield Finding(
            "error",
            f"Frontmatter `metadata.version` not valid SemVer (got {version!r})",
        )
    changelog = meta.get("changelog")
    if not changelog:
        yield Finding("error", "Frontmatter `metadata.changelog` missing or empty")
    elif isinstance(changelog, str) and isinstance(version, str) and version not in changelog:
        yield Finding(
            "warning",
            f"Frontmatter `metadata.changelog` does not mention current version {version!r}",
        )


def check_body(doc: SkillDoc) -> Iterable[Finding]:
    if doc.body_lines > BODY_MAX_LINES:
        yield Finding(
            "error",
            f"Body exceeds {BODY_MAX_LINES} lines (currently {doc.body_lines}); "
            f"push detail into references/",
        )


def check_router_atoms_resolve(doc: SkillDoc, archetype: str, plugin_root: Path) -> Iterable[Finding]:
    """Routers list their family's atoms in `## Atoms in This Family`. Each
    backticked entry should resolve to an existing skill directory under
    `<plugin_root>/skills/<name>/`. Tier 2/3 atoms that are specced-but-not-
    built will not resolve — that's expected; we warn (not error) so the
    operator can confirm. Per audit finding A21 from the family-bootstrap
    dogfood (v0.4.0 release)."""
    if archetype != "router":
        return
    section_bodies = _split_h2_bodies(doc.body)
    family_section = section_bodies.get("Atoms in This Family", "")
    if not family_section:
        return
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return  # no plugin skills/ to resolve against; skip silently
    listed = set()
    for match in re.finditer(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+){0,3})`", family_section):
        listed.add(match.group(1))
    if not listed:
        return
    missing = []
    for name in sorted(listed):
        if name == doc.frontmatter.get("name"):
            continue  # router can self-reference; skip
        if not (skills_dir / name).is_dir():
            missing.append(name)
    if missing:
        yield Finding(
            "warning",
            f"Router lists {len(missing)} atom(s) in `## Atoms in This Family` that "
            f"don't resolve to a skill directory: {missing}. If they are Tier 2/3 "
            f"atoms (specced/deferred per the family's coverage.md), this is "
            f"expected; otherwise the router and family are out of sync.",
        )


def check_required_sections(doc: SkillDoc, archetype: str) -> Iterable[Finding]:
    required = ARCHETYPE_REQUIRED_SECTIONS.get(archetype, [])
    titles = doc.section_titles
    for section in required:
        if not any(t == section or t.startswith(section) for t in titles):
            yield Finding(
                "error",
                f"Missing required section for archetype {archetype!r}: ## {section}",
            )

    # Duplicate H2 — same title appearing more than once is usually an
    # authoring error (a copy-paste artifact). Warn rather than block.
    seen: dict[str, int] = {}
    for t in titles:
        seen[t] = seen.get(t, 0) + 1
    for title, count in seen.items():
        if count > 1:
            yield Finding(
                "warning",
                f"Duplicate H2 section '## {title}' appears {count}× — usually an authoring error",
            )

    # Empty required-section content — the title is present but no body
    # follows. Common authoring oversight; warn so it surfaces in review.
    section_bodies = _split_h2_bodies(doc.body)
    for section in required:
        body = section_bodies.get(section, None)
        if body is not None and not body.strip():
            yield Finding(
                "warning",
                f"Required section '## {section}' is present but empty",
            )


# _split_h2_bodies is imported from _skill_io as a top-level alias; leaving
# this comment as a marker that the prior inline definition (v0.6.0) is
# intentionally gone in v0.6.1.


def check_references(skill_dir: Path) -> Iterable[Finding]:
    refs = skill_dir / "references"
    if not refs.is_dir():
        return
    for ref in refs.iterdir():
        if ref.is_dir():
            yield Finding(
                "error",
                f"Reference subdirectory not allowed: {ref.relative_to(skill_dir)} "
                f"(references must be one level deep)",
            )
            continue
        if ref.suffix != ".md":
            continue
        try:
            text = ref.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            yield Finding("error", f"Reference {ref.name} unreadable: {e}")
            continue
        line_count = text.count("\n")
        if line_count > REFERENCE_MAX_LINES:
            yield Finding(
                "error",
                f"Reference {ref.name} exceeds {REFERENCE_MAX_LINES} lines "
                f"(currently {line_count})",
            )
        if line_count > REFERENCE_TOC_THRESHOLD:
            # Check first 30 lines for any-level Table of Contents heading.
            # Spec says "table of contents at the top" without specifying H1/H2/H3,
            # so accept any heading level.
            head = "\n".join(text.splitlines()[:30]).lower()
            if not _TOC_HEADING_REGEX.search(head):
                yield Finding(
                    "warning",
                    f"Reference {ref.name} >300 lines but lacks a Table of Contents",
                )
        # Reference chaining: per METADATA-VALIDATION.md, a `references/*.md`
        # file must not link to another `references/*.md` *within the same
        # skill*. Cross-skill pointers (e.g., `skill-audit/references/foo.md`
        # appearing inside skill-author's frontmatter-spec.md) are fine — the
        # rule is about intra-skill navigation chains, not the meta-pipeline's
        # cross-skill cross-references.
        sibling_refs = {p.name for p in refs.iterdir() if p.is_file() and p.suffix == ".md"}
        for match in REFERENCE_CHAIN_REGEX.finditer(text):
            referenced = match.group(0)  # e.g., "references/foo.md"
            # Skip if it has a path prefix (cross-skill pointer like
            # `skill-audit/references/foo.md` — the regex match is `references/foo.md`
            # but the surrounding context names a different skill).
            start = match.start()
            preceding = text[max(0, start - 32) : start]
            if "/" in preceding.rsplit(" ", 1)[-1].rsplit("(", 1)[-1].rsplit("`", 1)[-1]:
                # Looks like the match is inside a longer path expression;
                # cross-skill or otherwise non-local. Skip.
                continue
            referenced_name = referenced.split("/", 1)[1]
            if referenced_name == ref.name:
                continue  # self-reference is harmless
            if referenced_name not in sibling_refs:
                continue  # not pointing at a sibling reference; not a chain
            yield Finding(
                "error",
                f"Reference {ref.name} chains to {referenced} — references must "
                f"not link to other references in the same skill "
                f"(per METADATA-VALIDATION.md)",
            )
            break  # one finding per file is enough; don't spam


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def find_skill_md(target: Path) -> Path:
    """Resolve a path to a SKILL.md. Accepts a file or a directory containing one."""
    if target.is_file():
        return target
    if target.is_dir():
        candidate = target / "SKILL.md"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"no SKILL.md at {target}")


def discover_all(plugin_root: Path) -> list[Path]:
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(skills_dir.glob("*/SKILL.md"))


def validate_one(skill_md: Path, override: str | None, plugin_root: Path | None = None) -> Report:
    doc = parse_skill(skill_md)
    archetype = detect_archetype(doc, override)
    name = doc.frontmatter.get("name") or skill_md.parent.name
    report = Report(skill=str(name), archetype=archetype)

    for finding in check_frontmatter(doc):
        report.add(finding)
    for finding in check_archetype_known(doc):
        report.add(finding)
    for finding in check_recency_pin_value(doc):
        report.add(finding)
    for finding in check_tags(doc):
        report.add(finding)
    for finding in check_body(doc):
        report.add(finding)
    for finding in check_required_sections(doc, archetype):
        report.add(finding)
    for finding in check_references(skill_md.parent):
        report.add(finding)
    # Router-specific cross-check: each entry in `## Atoms in This Family`
    # should resolve to an existing skill directory. Plugin root defaults to
    # two levels up from the SKILL.md (`<plugin>/skills/<name>/SKILL.md`).
    effective_root = plugin_root or skill_md.parent.parent.parent
    for finding in check_router_atoms_resolve(doc, archetype, effective_root):
        report.add(finding)

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--skill", type=Path, help="path to SKILL.md or skill directory")
    g.add_argument("--all", action="store_true", help="validate all skills under ./skills/")
    parser.add_argument("--archetype", choices=ARCHETYPES, help="override archetype detection")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="plugin root (default: cwd)")
    args = parser.parse_args(argv)

    try:
        targets: list[Path]
        if args.all:
            targets = discover_all(args.root)
            if not targets:
                sys.stderr.write(f"error: no SKILL.md files found under {args.root}/skills/\n")
                return 2
        else:
            targets = [find_skill_md(args.skill)]
    except FileNotFoundError as e:
        sys.stderr.write(f"error: {e}\n")
        return 2

    reports = []
    for skill_md in targets:
        try:
            reports.append(validate_one(skill_md, args.archetype, args.root))
        except (ValueError, FileNotFoundError) as e:
            sys.stderr.write(f"error: {e}\n")
            return 2

    # v0.6.1: library-wide depends_on freshness check (only on --all because
    # it requires the full skill set to compare pins against current versions).
    library_findings: list[Finding] = []
    if args.all:
        snapshot_path = args.root / "SNAPSHOT.lock"
        if snapshot_path.is_file():
            try:
                from _skill_io import load_snapshot
                snap = load_snapshot(snapshot_path)
                library_findings = list(check_depends_on_freshness(snap))
            except (ValueError, FileNotFoundError) as e:
                sys.stderr.write(f"warning: depends_on freshness skipped: {e}\n")

    any_errors = any(not r.passed for r in reports) or any(
        f.severity == "error" for f in library_findings
    )

    if args.format == "json":
        out: dict[str, Any] = {
            "skills": [r.render_json() for r in reports],
            "library": {
                "depends_on_freshness": [
                    {"severity": f.severity, "message": f.message}
                    for f in library_findings
                ],
            },
        }
        print(json.dumps(out, indent=2))
    else:
        for r in reports:
            print(r.render_text())
        if library_findings:
            print("Library-wide checks:")
            for f in library_findings:
                print(f"  {f.render_text()}")
            print()

    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main())
