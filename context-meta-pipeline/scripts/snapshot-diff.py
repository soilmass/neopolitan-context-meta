#!/usr/bin/env python3
"""
snapshot-diff.py — diff two SNAPSHOT.lock files and emit a structured
report suitable for CHANGELOG and GitHub release notes.

Categorizes changes into:
  - Added:    skills present in the new snapshot but not the old
  - Removed:  skills present in the old snapshot but not the new
              (per GOVERNANCE.md, "removed" means "no longer canonical";
              the SKILL.md remains in git history per skill-retire)
  - Bumped:   skills with version increase
  - Health:   skills with health-state transition (fresh → healthy → flagged → ...)
  - Deps:     skills whose `depends_on` set changed (added / removed / version-bumped)

Exit codes:
  0  diff produced (whether changes or none)
  2  invocation problem

Usage:
  snapshot-diff.py --old SNAPSHOT.old.lock --new SNAPSHOT.lock
  snapshot-diff.py --old <ref> --new SNAPSHOT.lock --format json

Dependencies: PyYAML + stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("error: PyYAML not installed. `pip install pyyaml`\n")
    sys.exit(2)


@dataclass
class SnapshotDiff:
    old_version: str
    new_version: str
    added: list[dict[str, Any]] = field(default_factory=list)
    removed: list[dict[str, Any]] = field(default_factory=list)
    bumped: list[dict[str, Any]] = field(default_factory=list)
    health_changed: list[dict[str, Any]] = field(default_factory=list)
    deps_changed: list[dict[str, Any]] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return any([self.added, self.removed, self.bumped, self.health_changed, self.deps_changed])


def load_snapshot(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: snapshot must be a YAML mapping")
    return data


def diff_snapshots(old: dict[str, Any], new: dict[str, Any]) -> SnapshotDiff:
    diff = SnapshotDiff(
        old_version=str(old.get("snapshot_version", "?")),
        new_version=str(new.get("snapshot_version", "?")),
    )

    old_skills: dict[str, dict[str, Any]] = old.get("skills", {}) or {}
    new_skills: dict[str, dict[str, Any]] = new.get("skills", {}) or {}

    old_names = set(old_skills)
    new_names = set(new_skills)

    for name in sorted(new_names - old_names):
        entry = new_skills[name]
        diff.added.append({
            "name": name,
            "version": entry.get("version", "?"),
            "archetype": entry.get("archetype", "?"),
            "path": entry.get("path", ""),
        })

    for name in sorted(old_names - new_names):
        entry = old_skills[name]
        diff.removed.append({
            "name": name,
            "last_canonical": entry.get("version", "?"),
            "archetype": entry.get("archetype", "?"),
        })

    for name in sorted(old_names & new_names):
        old_e, new_e = old_skills[name], new_skills[name]
        old_v = str(old_e.get("version", ""))
        new_v = str(new_e.get("version", ""))
        if old_v != new_v:
            diff.bumped.append({
                "name": name,
                "old_version": old_v,
                "new_version": new_v,
                "archetype": new_e.get("archetype", "?"),
            })
        old_h = old_e.get("health", "")
        new_h = new_e.get("health", "")
        if old_h != new_h:
            diff.health_changed.append({
                "name": name,
                "old_health": old_h,
                "new_health": new_h,
            })
        old_deps = sorted(_as_list(old_e.get("depends_on")))
        new_deps = sorted(_as_list(new_e.get("depends_on")))
        if old_deps != new_deps:
            diff.deps_changed.append({
                "name": name,
                "old_deps": old_deps,
                "new_deps": new_deps,
                "added": [d for d in new_deps if d not in old_deps],
                "removed": [d for d in old_deps if d not in new_deps],
            })

    return diff


def _as_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


def render_text(diff: SnapshotDiff) -> str:
    out = [f"# Snapshot diff: v{diff.old_version} → v{diff.new_version}\n"]
    if not diff.has_changes:
        out.append("\nNo changes.\n")
        return "".join(out)
    if diff.added:
        out.append("\n## Added\n\n")
        for s in diff.added:
            out.append(f"- **`{s['name']}`** v{s['version']} ({s['archetype']})\n")
    if diff.removed:
        out.append("\n## Removed (no longer canonical; remains pinnable in git)\n\n")
        for s in diff.removed:
            out.append(f"- `{s['name']}` (last canonical: v{s['last_canonical']}, archetype: {s['archetype']})\n")
    if diff.bumped:
        out.append("\n## Version bumps\n\n")
        for s in diff.bumped:
            out.append(f"- `{s['name']}` v{s['old_version']} → v{s['new_version']} ({s['archetype']})\n")
    if diff.health_changed:
        out.append("\n## Health transitions\n\n")
        for s in diff.health_changed:
            out.append(f"- `{s['name']}`: {s['old_health'] or '(none)'} → {s['new_health'] or '(none)'}\n")
    if diff.deps_changed:
        out.append("\n## Dependency changes\n\n")
        for s in diff.deps_changed:
            out.append(f"- `{s['name']}`:")
            if s["added"]:
                out.append(f" added {s['added']}")
            if s["removed"]:
                out.append(f" removed {s['removed']}")
            out.append("\n")
    return "".join(out)


def render_json(diff: SnapshotDiff) -> str:
    return json.dumps({
        "old_version": diff.old_version,
        "new_version": diff.new_version,
        "added": diff.added,
        "removed": diff.removed,
        "bumped": diff.bumped,
        "health_changed": diff.health_changed,
        "deps_changed": diff.deps_changed,
        "has_changes": diff.has_changes,
    }, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--old", type=Path, required=True, help="path to the older SNAPSHOT.lock")
    parser.add_argument("--new", type=Path, required=True, help="path to the newer SNAPSHOT.lock")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.old.is_file():
        sys.stderr.write(f"error: --old not found: {args.old}\n")
        return 2
    if not args.new.is_file():
        sys.stderr.write(f"error: --new not found: {args.new}\n")
        return 2

    try:
        old = load_snapshot(args.old)
        new = load_snapshot(args.new)
    except (ValueError, yaml.YAMLError) as e:
        sys.stderr.write(f"error: {e}\n")
        return 2

    diff = diff_snapshots(old, new)
    if args.format == "json":
        print(render_json(diff))
    else:
        print(render_text(diff))
    return 0


if __name__ == "__main__":
    sys.exit(main())
