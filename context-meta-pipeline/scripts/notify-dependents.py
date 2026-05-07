#!/usr/bin/env python3
# pre-trigger build (v0.7.0); reassess when trigger fires per
# governance/DEPRECATION-COMMUNICATION.md (external consumers exist).
"""
notify-dependents.py — emit per-channel JSON notifications when a skill is
retired or deprecated. Per governance/DEPRECATION-COMMUNICATION.md.

Reads SNAPSHOT.lock to find dependents (skills with `depends_on:` pointing
at the target) and `governance/notification-channels.yaml` for the channel
list. Emits one JSON record per channel × dependent. Does NOT actually
send — channel-wiring (webhook URL, email server, etc.) is per consumer
team's setup.

Exit codes:
  0  notifications produced
  1  no dependents found (informational; not an error in DEPRECATION-COMM
     terms but flagged so the operator notices)
  2  invocation problem (skill not found, no channels.yaml, malformed)

Usage:
  notify-dependents.py --skill skill-X
  notify-dependents.py --skill skill-X --reason "absorbed into skill-Y"
  notify-dependents.py --skill skill-X --format json

Dependencies: PyYAML (via _skill_io) + stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from _skill_io import load_snapshot


@dataclass
class Notification:
    channel: str
    type: str
    target: str
    skill: str
    reason: str
    dependents: list[str] = field(default_factory=list)


def find_dependents(snapshot: dict[str, Any], target_skill: str) -> list[str]:
    """List every skill whose depends_on: includes target_skill@<any>."""
    skills = snapshot.get("skills") or {}
    if not isinstance(skills, dict):
        return []
    deps: list[str] = []
    for name, spec in skills.items():
        if not isinstance(spec, dict):
            continue
        for d in spec.get("depends_on") or []:
            if isinstance(d, str) and d.startswith(f"{target_skill}@"):
                deps.append(name)
                break
    return sorted(deps)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--skill", required=True,
                        help="skill being retired/deprecated")
    parser.add_argument("--reason", default="(unspecified)",
                        help="one-line reason; lands in the notification payload")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    snap_path = args.root / "SNAPSHOT.lock"
    channels_path = args.root / "governance" / "notification-channels.yaml"
    if not snap_path.is_file():
        sys.stderr.write(f"error: {snap_path} not found\n")
        return 2
    if not channels_path.is_file():
        sys.stderr.write(f"error: {channels_path} not found\n")
        return 2

    try:
        snap = load_snapshot(snap_path)
    except ValueError as e:
        sys.stderr.write(f"error: {e}\n")
        return 2

    skills = snap.get("skills") or {}
    if not isinstance(skills, dict) or args.skill not in skills:
        sys.stderr.write(f"error: skill {args.skill!r} not in SNAPSHOT.lock\n")
        return 2

    try:
        import yaml  # type: ignore[import-untyped]
        channels_data = yaml.safe_load(channels_path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError) as e:
        sys.stderr.write(f"error parsing {channels_path}: {e}\n")
        return 2
    channels = channels_data.get("channels") or []
    if not isinstance(channels, list):
        sys.stderr.write(f"error: channels in {channels_path} must be a list\n")
        return 2

    dependents = find_dependents(snap, args.skill)

    notifications: list[Notification] = []
    for ch in channels:
        if not isinstance(ch, dict):
            continue
        if not ch.get("enabled", True):
            continue
        notifications.append(
            Notification(
                channel=str(ch.get("name", "")),
                type=str(ch.get("type", "")),
                target=str(ch.get("target", "")),
                skill=args.skill,
                reason=args.reason,
                dependents=dependents,
            )
        )

    if args.format == "json":
        print(json.dumps(
            {
                "skill": args.skill,
                "reason": args.reason,
                "dependent_count": len(dependents),
                "dependents": dependents,
                "notification_count": len(notifications),
                "notifications": [
                    {
                        "channel": n.channel,
                        "type": n.type,
                        "target": n.target,
                        "skill": n.skill,
                        "reason": n.reason,
                        "dependents": n.dependents,
                    }
                    for n in notifications
                ],
            },
            indent=2,
        ))
    else:
        print(f"notify-dependents: skill={args.skill}; reason={args.reason!r}")
        print(f"  dependents: {len(dependents)} ({', '.join(dependents) if dependents else 'none'})")
        print(f"  channels enabled: {len(notifications)}")
        if not notifications:
            print("  (no enabled channels in governance/notification-channels.yaml; "
                  "notification dry-run only)")
        else:
            for n in notifications:
                print(f"  → channel={n.channel!r} type={n.type} target={n.target}")

    return 1 if not dependents else 0


if __name__ == "__main__":
    sys.exit(main())
