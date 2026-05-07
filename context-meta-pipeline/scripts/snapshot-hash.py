#!/usr/bin/env python3
# pre-trigger build (v0.7.0); reassess when trigger fires per
# governance/SKILL-PROVENANCE.md (external publishing).
"""
snapshot-hash.py — compute SHA-256 hashes of every SKILL.md and write them to
SNAPSHOT.lock per skill. Per governance/SKILL-PROVENANCE.md.

Two modes:
  (default) — compute and write hashes. First run: populates `sha256:` field on
              every skill. Subsequent runs: refreshes hashes for changed
              SKILL.md files. Idempotent.
  --verify  — recompute hashes and compare against stored values. Exit 1 on
              mismatch. Used by release-tag.sh and CI to confirm SKILL.md
              integrity matches snapshot.

The hash uses a canonical input: the raw SKILL.md bytes, no normalization.
This couples the hash to file content exactly — any whitespace edit changes
the hash. Per SKILL-PROVENANCE.md, the hash is meant for tampering detection
across distribution boundaries (consumer libraries / marketplace), not for
ignoring trivial diffs.

First-run init behavior: when no `sha256:` fields exist, treat as init and
populate. Subsequent runs treat missing-field as an error (a skill was added
after init but its hash wasn't written).

Exit codes:
  0  hashes written (or all match in --verify mode)
  1  --verify found a hash mismatch OR a skill missing sha256: in non-init state
  2  invocation problem (no skills, malformed SNAPSHOT.lock, etc.)

Usage:
  snapshot-hash.py
  snapshot-hash.py --verify

Dependencies: stdlib (no PyYAML — string-replace surgery on SNAPSHOT.lock).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from _skill_io import iter_live_skills


def compute_hash(skill_md: Path) -> str:
    """SHA-256 of raw SKILL.md bytes."""
    return hashlib.sha256(skill_md.read_bytes()).hexdigest()


def find_skill_block_range(snapshot_text: str, skill_name: str) -> tuple[int, int] | None:
    """Locate the byte range of a skill's block in SNAPSHOT.lock — same logic
    as audit-skill.py's _find_skill_block."""
    head_pattern = re.compile(
        rf'^(  {re.escape(skill_name)}:\s*)$\n', re.MULTILINE
    )
    m = head_pattern.search(snapshot_text)
    if not m:
        return None
    block_start = m.start()
    pos = m.end()
    while pos < len(snapshot_text):
        eol = snapshot_text.find("\n", pos)
        if eol == -1:
            pos = len(snapshot_text)
            break
        line = snapshot_text[pos:eol]
        if line.startswith("    ") or line.strip() == "":
            pos = eol + 1
            continue
        break
    return (block_start, pos)


def extract_sha256(snapshot_text: str, skill_name: str) -> str | None:
    span = find_skill_block_range(snapshot_text, skill_name)
    if span is None:
        return None
    block = snapshot_text[span[0]:span[1]]
    m = re.search(r'^\s+sha256:\s*["\']?([a-f0-9]+)["\']?\s*$', block, re.MULTILINE)
    return m.group(1) if m else None


def upsert_sha256(snapshot_text: str, skill_name: str, sha: str) -> str:
    """Insert or replace `sha256:` in a skill's block."""
    span = find_skill_block_range(snapshot_text, skill_name)
    if span is None:
        return snapshot_text
    block = snapshot_text[span[0]:span[1]]
    if re.search(r'^\s+sha256:', block, re.MULTILINE):
        # Replace existing.
        new_block = re.sub(
            r'(^\s+sha256:\s*)["\']?[a-f0-9]+["\']?(\s*)$',
            rf'\1"{sha}"\2',
            block,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        # Insert. Add as the last line of the block (before any trailing
        # blank lines that mark block boundary).
        # Find the indentation level of the existing content lines.
        body_lines = block.splitlines(keepends=True)
        # Remove trailing blank lines to find the insert point.
        while body_lines and body_lines[-1].strip() == "":
            body_lines.pop()
        # Insert sha256 line with 4-space indent matching siblings.
        body_lines.append(f'    sha256: "{sha}"\n')
        new_block = "".join(body_lines)
        # Restore trailing newline if the original had one.
        if not new_block.endswith("\n"):
            new_block += "\n"
    return snapshot_text[: span[0]] + new_block + snapshot_text[span[1]:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--verify", action="store_true",
                        help="recompute hashes and compare against stored; exit 1 on mismatch")
    args = parser.parse_args(argv)

    snap_path = args.root / "SNAPSHOT.lock"
    if not snap_path.is_file():
        sys.stderr.write(f"error: {snap_path} not found\n")
        return 2
    text = snap_path.read_text(encoding="utf-8")

    # Detect init state: if NO skill has sha256, this is the first run.
    has_any_hash = bool(re.search(r'^\s+sha256:', text, re.MULTILINE))

    skills_seen = list(iter_live_skills(args.root))

    if args.verify:
        mismatches: list[tuple[str, str | None, str]] = []
        missing: list[str] = []
        for skill_md in skills_seen:
            name = skill_md.parent.name
            stored = extract_sha256(text, name)
            actual = compute_hash(skill_md)
            if stored is None:
                if has_any_hash:
                    missing.append(name)
                # First-run state: skip; the operator should run without --verify
                # to populate.
                continue
            if stored != actual:
                mismatches.append((name, stored, actual))
        if missing:
            print(f"--verify: {len(missing)} skill(s) missing sha256: {', '.join(missing)}")
        if mismatches:
            print(f"--verify: {len(mismatches)} hash mismatch(es):")
            for name, stored, actual in mismatches:
                stored_short = (stored or "<none>")[:12]
                print(f"  {name}: stored={stored_short}...  actual={actual[:12]}...")
        if not has_any_hash:
            print("--verify: no sha256 fields populated; run snapshot-hash.py to init.")
            return 0
        if missing or mismatches:
            return 1
        print(f"--verify: {len(skills_seen)} skill(s) match.")
        return 0

    # Write/update mode.
    n_changed = 0
    for skill_md in skills_seen:
        name = skill_md.parent.name
        actual = compute_hash(skill_md)
        stored = extract_sha256(text, name)
        if stored == actual:
            continue
        text = upsert_sha256(text, name, actual)
        n_changed += 1

    if n_changed > 0:
        snap_path.write_text(text, encoding="utf-8")
    print(f"snapshot-hash: {len(skills_seen)} skill(s) checked; {n_changed} hash(es) written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
