#!/usr/bin/env python3
"""
rollback-skill.py — automates Level 1 (single-skill) rollback per
governance/ROLLBACK-PROCEDURE.md.

Levels 2 (coordinated multi-skill) and 3 (full library snapshot) remain
procedural — their blast radius and forensic requirements are too case-
specific to safely automate.

Actions performed (in order):
  1. Find the git ref where the target version was canonical (parses
     metadata.version per commit on the skill's directory).
  2. Restore SKILL.md, references/, and any scripts/ via `git checkout`.
  3. Prepend a rollback entry to the skill's metadata.changelog.
  4. Update SNAPSHOT.lock to record the rolled-back version.
  5. Append a rollback entry to the library CHANGELOG.md.

Exit codes:
  0  rollback applied successfully (or dry-run completed)
  1  rollback failed (target version not in git history, snapshot mismatch, etc.)
  2  --dry-run was set; would-have-written actions printed but no writes performed

Usage:
  rollback-skill.py --skill skill-author --to 0.1.0 --reason "regression in stage 4"
  rollback-skill.py --skill skill-author --to 0.1.0 --reason "smoke" --dry-run

Dependencies: PyYAML + stdlib + subprocess (git).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    sys.stderr.write("error: PyYAML not installed. `pip install pyyaml`\n")
    sys.exit(1)

# v0.6.1: shared parser for SKILL.md frontmatter+body. SNAPSHOT.lock parsing
# stays on direct yaml usage (round-trip writes need yaml.safe_dump).
from _skill_io import parse_skill_text


@dataclass
class ActionLog:
    actions: list[tuple[str, str]] = field(default_factory=list)  # (status, message)

    def ok(self, msg: str) -> None:
        self.actions.append(("OK", msg))

    def skip(self, msg: str) -> None:
        self.actions.append(("--", msg))

    def fail(self, msg: str) -> None:
        self.actions.append(("FAIL", msg))

    def render(self, header: str) -> str:
        out = [header, "\n"]
        for status, msg in self.actions:
            out.append(f"[{status}] {msg}\n")
        return "".join(out)


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def git(args: list[str], cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.PIPE).decode("utf-8")


def find_ref_for_version(skill_dir: Path, target_version: str) -> str:
    """Walk git log on the skill's directory; return the first commit where
    the SKILL.md's metadata.version matches `target_version`.

    Runs git from the repo root so the repo-relative path resolves correctly.
    Earlier versions ran git from `skill_dir`, where a repo-relative path
    silently resolved to a nonexistent location and the loop never found
    any commits — surfaced by the v0.5.1 rollback fixture.
    """
    repo_root = _repo_root(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    rel = skill_md.resolve().relative_to(repo_root)
    log = git(["log", "--format=%H", "--", str(rel)], repo_root)
    for ref in log.strip().splitlines():
        try:
            text = git(["show", f"{ref}:{rel}"], repo_root)
        except subprocess.CalledProcessError:
            continue
        m = re.search(r"^\s*version:\s*['\"]?([\d.]+(?:-[\w.]+)?)['\"]?", text, re.MULTILINE)
        if m and m.group(1) == target_version:
            return ref
    raise ValueError(f"target version {target_version} not found in git history of {skill_md}")


def _repo_root(any_path: Path) -> Path:
    return Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=any_path
        ).decode().strip()
    )


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------


def parse_skill_md(path: Path) -> tuple[dict[str, Any], str]:
    """Parse a SKILL.md from a path. v0.6.1: thin wrapper over _skill_io."""
    return parse_skill_text(path.read_text(encoding="utf-8"), source=str(path))


def render_skill_md(fm: dict[str, Any], body: str) -> str:
    dumped: str = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    return "---\n" + dumped.rstrip() + "\n---\n" + body


# ---------------------------------------------------------------------------
# Snapshot + library CHANGELOG helpers
# ---------------------------------------------------------------------------


def update_snapshot(snapshot_path: Path, skill_name: str, target_version: str) -> bool:
    """Update SNAPSHOT.lock's skill entry to target_version. Returns True if changed."""
    snap = yaml.safe_load(snapshot_path.read_text(encoding="utf-8")) or {}
    skills = snap.setdefault("skills", {})
    entry = skills.get(skill_name)
    if not entry:
        raise ValueError(f"snapshot has no entry for skill {skill_name!r}")
    if entry.get("version") == target_version:
        return False
    entry["version"] = target_version
    entry["health"] = "rolled-back"
    snapshot_path.write_text(yaml.safe_dump(snap, sort_keys=False), encoding="utf-8")
    return True


def append_library_changelog(
    changelog_path: Path, skill_name: str, from_version: str, to_version: str, reason: str
) -> None:
    today = _dt.date.today().isoformat()
    entry = (
        f"\n## {today}\n\n"
        f"### Rolled back\n"
        f"- `{skill_name}` v{from_version} → v{to_version} ({reason})\n"
        f"  - Affects: routers that dispatch to this skill (verify and update)\n"
        f"  - Users with explicit pins to v{from_version}: investigate before updating\n"
    )
    text = changelog_path.read_text(encoding="utf-8")
    # Insert under [Unreleased] block if present, else append.
    marker = "## [Unreleased]"
    if marker in text:
        idx = text.index(marker) + len(marker)
        nl = text.find("\n", idx)
        text = text[: nl + 1] + entry + text[nl + 1 :]
    else:
        text = text.rstrip() + "\n" + entry
    changelog_path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--skill", required=True, help="skill name (looked up under ./skills/)")
    parser.add_argument("--to", required=True, help="target SemVer to roll back to")
    parser.add_argument("--reason", required=True, help="rollback reason (embedded in changelogs)")
    parser.add_argument("--snapshot", type=Path, default=Path("SNAPSHOT.lock"))
    parser.add_argument("--changelog", type=Path, default=Path("CHANGELOG.md"))
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="plugin root (default: cwd)")
    parser.add_argument("--dry-run", action="store_true", help="print intended actions; do not write")
    args = parser.parse_args(argv)

    skill_dir = args.root / "skills" / args.skill
    skill_md = skill_dir / "SKILL.md"
    log = ActionLog()

    if not skill_md.is_file():
        sys.stderr.write(f"error: {skill_md} not found\n")
        return 1
    if not args.snapshot.is_file():
        sys.stderr.write(f"error: snapshot {args.snapshot} not found\n")
        return 1
    if not args.changelog.is_file():
        sys.stderr.write(f"error: changelog {args.changelog} not found\n")
        return 1

    # Capture current version
    try:
        fm, _ = parse_skill_md(skill_md)
    except ValueError as e:
        sys.stderr.write(f"error: {e}\n")
        return 1
    current_version = (fm.get("metadata") or {}).get("version", "unknown")

    header = f"ROLLBACK: {args.skill} {current_version} -> {args.to}\nReason: {args.reason}\n"

    # Step 1: locate the git ref for the target version
    try:
        ref = find_ref_for_version(skill_dir, args.to)
        log.ok(f"found git ref {ref[:12]} for version {args.to}")
    except (ValueError, subprocess.CalledProcessError) as e:
        log.fail(f"could not find ref for version {args.to}: {e}")
        sys.stderr.write(log.render(header))
        return 1

    # Step 2: restore skill files
    if args.dry_run:
        log.skip(f"would `git checkout {ref[:12]} -- {skill_dir}/` (dry-run)")
    else:
        try:
            git(["checkout", ref, "--", str(skill_dir)], cwd=args.root)
            log.ok(f"restored {skill_dir} from {ref[:12]}")
        except subprocess.CalledProcessError as e:
            log.fail(f"git checkout failed: {e.stderr.decode() if e.stderr else e}")
            sys.stderr.write(log.render(header))
            return 1

    # Step 3: prepend rollback entry to metadata.changelog
    rollback_changelog_entry = (
        f"v{current_version} (rolled back, {_dt.date.today().isoformat()}) — {args.reason}.\n"
        f"v{args.to} (current) — restored as canonical version pending investigation.\n"
    )
    if args.dry_run:
        log.skip("would prepend rollback entry to skill metadata.changelog (dry-run)")
    else:
        try:
            fm2, body2 = parse_skill_md(skill_md)
            existing = (fm2.get("metadata") or {}).get("changelog", "") or ""
            fm2.setdefault("metadata", {})["changelog"] = rollback_changelog_entry + str(existing)
            skill_md.write_text(render_skill_md(fm2, body2), encoding="utf-8")
            log.ok("prepended rollback entry to skill metadata.changelog")
        except (ValueError, OSError) as e:
            log.fail(f"failed to update metadata.changelog: {e}")
            return 1

    # Step 4: update SNAPSHOT.lock
    if args.dry_run:
        log.skip(f"would update {args.snapshot.name}: {args.skill}@{args.to}, health=rolled-back (dry-run)")
    else:
        try:
            changed = update_snapshot(args.snapshot, args.skill, args.to)
            log.ok(f"{args.snapshot.name} updated" if changed else f"{args.snapshot.name} already at {args.to}")
        except (ValueError, OSError, yaml.YAMLError) as e:
            log.fail(f"snapshot update failed: {e}")
            return 1

    # Step 5: append library CHANGELOG entry
    if args.dry_run:
        log.skip(f"would append rollback entry to {args.changelog.name} under today's date (dry-run)")
    else:
        try:
            append_library_changelog(args.changelog, args.skill, current_version, args.to, args.reason)
            log.ok(f"{args.changelog.name} updated with rollback entry")
        except OSError as e:
            log.fail(f"changelog update failed: {e}")
            return 1

    # Manual remaining steps (always reminded)
    log.skip("manual: notify dependents (routers) — see GOVERNANCE.md §Change Notifications")
    log.skip("manual: open PR titled \"rollback: {} -> {}\"".format(args.skill, args.to))

    print(log.render(header))
    return 2 if args.dry_run else 0


if __name__ == "__main__":
    sys.exit(main())
