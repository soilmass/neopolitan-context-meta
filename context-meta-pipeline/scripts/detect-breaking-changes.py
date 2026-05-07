#!/usr/bin/env python3
"""
detect-breaking-changes.py — implements governance/BREAKING-CHANGE-DETECTION.md.

Compares a modified SKILL.md against a baseline (file or git ref) and flags
breaking changes per the four detection passes:

  1. Frontmatter changes (name, allowed-tools removal, description >30%, model)
  2. Section removal (any required section for the archetype)
  3. Capability changes (atoms: removal/move from `Capabilities Owned`)
  4. Routing changes (routers: removal/target-change in `Routing Table`)

Exit codes:
  0  no breaking change detected
  1  breaking change detected without proper handling (blocks merge)
  2  breaking change detected with proper handling (informational only)

Usage:
  detect-breaking-changes.py --skill <path> --baseline <path>
  detect-breaking-changes.py --skill <path> --baseline-ref HEAD~1
  detect-breaking-changes.py --skill <path> --baseline-ref HEAD~1 --snapshot SNAPSHOT.lock
  detect-breaking-changes.py --skill <path> --baseline <path> --format json

Dependencies: PyYAML + stdlib + subprocess (git).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# SNAPSHOT.lock parsing uses yaml directly; SKILL.md parsing goes through _skill_io.
try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    sys.stderr.write("error: PyYAML not installed. `pip install pyyaml`\n")
    sys.exit(2)

# v0.6.1: shared parser + section splitter live in _skill_io.
from _skill_io import parse_skill_text, split_h2_bodies as split_sections


# Same archetype-required-sections table as validate-metadata.py
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

DESCRIPTION_REWRITE_THRESHOLD = 0.30  # >30% character-count change is breaking


@dataclass
class BreakingFinding:
    category: str  # "Frontmatter" | "Section removal" | "Capability removal" | "Routing change"
    detail: str

    def render(self) -> str:
        return f"Category: {self.category}\nDetail: {self.detail}"


@dataclass
class Doc:
    frontmatter: dict[str, Any]
    body: str
    sections: dict[str, str]  # section title → body text under it (until next H2)


def parse(text: str) -> Doc:
    """Parse a SKILL.md text into a Doc. Uses _skill_io's shared parser."""
    fm, body = parse_skill_text(text, source="<detect-breaking-changes input>")
    sections = split_sections(body)
    return Doc(frontmatter=fm, body=body, sections=sections)


# split_sections is imported from _skill_io as the canonical split_h2_bodies.
# The local name `split_sections` is preserved as an alias to keep the rest
# of detect-breaking-changes.py untouched.


def read_text_or_git(path_or_ref: str | None, ref_arg: str | None, file_path: Path | None) -> str:
    """Resolve baseline content from --baseline or --baseline-ref."""
    if path_or_ref is not None:
        p = Path(path_or_ref)
        if not p.is_file():
            raise FileNotFoundError(f"baseline file not found: {p}")
        return p.read_text(encoding="utf-8")
    assert ref_arg is not None and file_path is not None
    # `git show <ref>:<path>` requires the path relative to the repo root.
    try:
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=file_path.parent,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("--baseline-ref requires a git repo")
    rel = file_path.resolve().relative_to(repo_root)
    out = subprocess.check_output(
        ["git", "show", f"{ref_arg}:{rel}"],
        cwd=repo_root,
        stderr=subprocess.DEVNULL,
    )
    return out.decode("utf-8")


# ---------------------------------------------------------------------------
# Detection passes
# ---------------------------------------------------------------------------


def diff_frontmatter(old: dict[str, Any], new: dict[str, Any]) -> list[BreakingFinding]:
    findings: list[BreakingFinding] = []
    if old.get("name") != new.get("name"):
        findings.append(
            BreakingFinding(
                "Frontmatter",
                f"`name` changed: {old.get('name')!r} -> {new.get('name')!r}",
            )
        )
    old_tools = set(_as_list(old.get("allowed-tools")))
    new_tools = set(_as_list(new.get("allowed-tools")))
    removed = old_tools - new_tools
    if removed:
        findings.append(
            BreakingFinding(
                "Frontmatter",
                f"`allowed-tools` removed: {sorted(removed)!r}",
            )
        )
    if old.get("model") != new.get("model"):
        findings.append(
            BreakingFinding(
                "Frontmatter",
                f"`model` changed: {old.get('model')!r} -> {new.get('model')!r}",
            )
        )
    old_desc = (old.get("description") or "").strip()
    new_desc = (new.get("description") or "").strip()
    if old_desc and new_desc:
        delta = abs(len(old_desc) - len(new_desc)) / max(len(old_desc), 1)
        if delta > DESCRIPTION_REWRITE_THRESHOLD:
            findings.append(
                BreakingFinding(
                    "Frontmatter",
                    f"`description` rewritten >{int(DESCRIPTION_REWRITE_THRESHOLD*100)}% by character count "
                    f"({int(delta*100)}% change); review for breaking shift",
                )
            )
    return findings


def _as_list(v: Any) -> list[Any]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        return [s.strip() for s in v.split(",") if s.strip()]
    return [v]


def diff_sections(old: Doc, new: Doc, archetype: str) -> list[BreakingFinding]:
    findings: list[BreakingFinding] = []
    required = ARCHETYPE_REQUIRED_SECTIONS.get(archetype, [])
    for section in required:
        old_has = section in old.sections
        new_has = section in new.sections
        if old_has and not new_has:
            findings.append(
                BreakingFinding("Section removal", f"required section '## {section}' removed")
            )
    return findings


def diff_capabilities(old: Doc, new: Doc) -> list[BreakingFinding]:
    findings: list[BreakingFinding] = []
    old_caps = extract_capabilities(old)
    new_caps = extract_capabilities(new)
    removed = old_caps - new_caps
    for cap in sorted(removed):
        findings.append(
            BreakingFinding("Capability removal", f"`{cap}` removed from Capabilities Owned")
        )
    return findings


def extract_capabilities(doc: Doc) -> set[str]:
    """Capabilities are bullet entries under `## Capabilities Owned`."""
    section = doc.sections.get("Capabilities Owned", "")
    caps: set[str] = set()
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            # strip leading marker, then split on first ':' or ' —' to get the cap name
            text = line[2:].strip()
            for sep in (":", " — ", " - "):
                if sep in text:
                    text = text.split(sep, 1)[0]
                    break
            text = text.strip("`* ").strip()
            if text:
                caps.add(text)
    return caps


def diff_routing(old: Doc, new: Doc) -> list[BreakingFinding]:
    findings: list[BreakingFinding] = []
    old_table = parse_routing_table(old.sections.get("Routing Table", ""))
    new_table = parse_routing_table(new.sections.get("Routing Table", ""))
    for intent, target in old_table.items():
        if intent not in new_table:
            findings.append(
                BreakingFinding("Routing change", f"routing entry removed: {intent!r} -> {target!r}")
            )
        elif new_table[intent] != target:
            findings.append(
                BreakingFinding(
                    "Routing change",
                    f"routing target changed for {intent!r}: {target!r} -> {new_table[intent]!r}",
                )
            )
    return findings


ROUTING_ROW_RE = re.compile(r"^\|\s*(?P<intent>[^|]+?)\s*\|\s*(?P<target>[^|]+?)\s*\|")


def parse_routing_table(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        m = ROUTING_ROW_RE.match(line.strip())
        if not m:
            continue
        intent = m.group("intent").strip("`* ").strip()
        target = m.group("target").strip("`* ").strip()
        if not intent or intent.lower() in {"intent", ":---", "---"} or set(intent) <= {"-", ":"}:
            continue
        rows[intent] = target
    return rows


# ---------------------------------------------------------------------------
# Required-actions check (handling)
# ---------------------------------------------------------------------------


def required_actions(
    new: Doc, baseline: Doc, snapshot_path: Path | None, skill_name: str
) -> tuple[list[str], list[str]]:
    """Return (blocking_gaps, reminders).

    Blocking gaps are auto-checkable from the diff — failing them returns exit 1.
    Reminders are procedural — they list actions the operator must perform but
    that this script can't verify from the skill diff alone.
    """
    blocking: list[str] = []
    reminders: list[str] = []

    new_v = (new.frontmatter.get("metadata") or {}).get("version", "")
    old_v = (baseline.frontmatter.get("metadata") or {}).get("version", "")
    new_major = _major(new_v)
    old_major = _major(old_v)
    if new_major is None or old_major is None or new_major <= old_major:
        blocking.append(f"Bump version to {(old_major or 0) + 1}.0.0 (currently {new_v or 'unknown'})")

    changelog = (new.frontmatter.get("metadata") or {}).get("changelog") or ""
    if isinstance(changelog, str) and "migration" not in changelog.lower():
        blocking.append("Add migration guide entry (skill `metadata.changelog` mentions no migration)")

    if snapshot_path and snapshot_path.is_file():
        try:
            snap = yaml.safe_load(snapshot_path.read_text(encoding="utf-8")) or {}
            skills = snap.get("skills", {})
            entry = skills.get(skill_name, {})
            if entry.get("version") != new_v:
                blocking.append(
                    f"Update library snapshot ({snapshot_path.name}) to record {skill_name}@{new_v}"
                )
        except yaml.YAMLError:
            blocking.append("Update library snapshot (snapshot unparseable)")
    else:
        reminders.append("Update library snapshot (no SNAPSHOT.lock provided to verify)")

    # Library CHANGELOG and lock-step coordination are not verifiable from a
    # single-skill diff. They're procedural reminders.
    reminders.append("Add entry to library CHANGELOG.md under today's date")
    reminders.append("Update routers that dispatch to this skill (lock-step coordination)")

    return blocking, reminders


def _major(version: str) -> int | None:
    if not version:
        return None
    m = re.match(r"^(\d+)\.", version)
    return int(m.group(1)) if m else None


def find_dependents(skill_name: str, snapshot_path: Path | None) -> list[str]:
    if not snapshot_path or not snapshot_path.is_file():
        return []
    try:
        snap = yaml.safe_load(snapshot_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []
    deps: list[str] = []
    skills = snap.get("skills", {})
    target = f"{skill_name}@"
    for other, entry in skills.items():
        if other == skill_name:
            continue
        for dep in entry.get("depends_on", []) or []:
            if isinstance(dep, str) and dep.startswith(target):
                deps.append(other)
                break
    return deps


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


@dataclass
class DetectorReport:
    skill: str
    findings: list[BreakingFinding] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    blocking_gaps: list[str] = field(default_factory=list)
    reminders: list[str] = field(default_factory=list)

    @property
    def is_breaking(self) -> bool:
        return bool(self.findings)

    @property
    def properly_handled(self) -> bool:
        return self.is_breaking and not self.blocking_gaps

    def render_text(self) -> str:
        if not self.is_breaking:
            return f"NO BREAKING CHANGE detected in skill: {self.skill}\n"
        out = [f"BREAKING CHANGE DETECTED in skill: {self.skill}\n\n"]
        for f in self.findings:
            out.append(f.render() + "\n")
        impact = (
            f"{len(self.dependents)} dependents: " + ", ".join(self.dependents)
            if self.dependents
            else "no recorded dependents in snapshot"
        )
        out.append(f"Impact: {impact}\n\n")
        if self.blocking_gaps:
            out.append("Blocking gaps (must fix before merge):\n")
            for g in self.blocking_gaps:
                out.append(f"[X] {g}\n")
            out.append("\n")
        if self.reminders:
            out.append("Procedural reminders (verify manually):\n")
            for r in self.reminders:
                out.append(f"[ ] {r}\n")
            out.append("\n")
        if self.properly_handled:
            out.append("Auto-checkable handling complete (informational — does not block merge).\n")
        return "".join(out)

    def render_json(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "is_breaking": self.is_breaking,
            "properly_handled": self.properly_handled,
            "findings": [{"category": f.category, "detail": f.detail} for f in self.findings],
            "dependents": self.dependents,
            "blocking_gaps": self.blocking_gaps,
            "reminders": self.reminders,
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def detect_archetype(doc: Doc) -> str:
    meta = doc.frontmatter.get("metadata") or {}
    a = meta.get("archetype") if isinstance(meta, dict) else None
    if isinstance(a, str) and a.lower() in ARCHETYPE_REQUIRED_SECTIONS:
        return a.lower()
    return "atom"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--skill", type=Path, required=True)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--baseline", type=str, help="path to baseline SKILL.md")
    g.add_argument("--baseline-ref", type=str, help="git ref to fetch baseline from (e.g., HEAD~1)")
    parser.add_argument("--snapshot", type=Path, default=Path("SNAPSHOT.lock"))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    try:
        new_text = args.skill.read_text(encoding="utf-8")
        baseline_text = read_text_or_git(args.baseline, args.baseline_ref, args.skill)
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write(f"error: {e}\n")
        return 2

    try:
        new = parse(new_text)
        baseline = parse(baseline_text)
    except (ValueError, yaml.YAMLError) as e:
        sys.stderr.write(f"error parsing: {e}\n")
        return 2

    archetype = detect_archetype(new)
    skill_name = new.frontmatter.get("name") or args.skill.parent.name

    findings: list[BreakingFinding] = []
    findings.extend(diff_frontmatter(baseline.frontmatter, new.frontmatter))
    findings.extend(diff_sections(baseline, new, archetype))
    if archetype == "atom":
        findings.extend(diff_capabilities(baseline, new))
    if archetype == "router":
        findings.extend(diff_routing(baseline, new))

    snapshot_path = args.snapshot if args.snapshot and args.snapshot.is_file() else None
    dependents = find_dependents(skill_name, snapshot_path) if findings else []
    if findings:
        blocking, reminders = required_actions(new, baseline, snapshot_path, skill_name)
    else:
        blocking, reminders = [], []

    report = DetectorReport(
        skill=skill_name,
        findings=findings,
        dependents=dependents,
        blocking_gaps=blocking,
        reminders=reminders,
    )

    if args.format == "json":
        print(json.dumps(report.render_json(), indent=2))
    else:
        print(report.render_text())

    if not report.is_breaking:
        return 0
    return 2 if report.properly_handled else 1


if __name__ == "__main__":
    sys.exit(main())
