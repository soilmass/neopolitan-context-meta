#!/usr/bin/env python3
# pre-trigger build (v0.7.0); reassess when trigger fires per
# governance/USAGE-ANALYTICS.md (25+ skills, real telemetry hook).
"""
analytics-rollup.py — consume JSONL events emitted by telemetry-hook.py
(or a future real Claude Code load-time hook) and produce per-skill
activation count, co-invocation matrix, trend lines.

Per governance/USAGE-ANALYTICS.md. v0.7.0 ahead-of-trigger build:
operates on synthetic JSONL fixtures today; consumes real events when
Claude Code core gains the load-time hook.

Exit codes:
  0  rollup produced
  2  invocation problem (no input, malformed JSONL)

Usage:
  analytics-rollup.py --input scripts/tests/analytics/synthetic-events.jsonl
  analytics-rollup.py --input <path> --format json

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"warning: line {i} skipped (malformed JSON): {e}\n")
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.input.is_file():
        sys.stderr.write(f"error: {args.input} not found\n")
        return 2

    events = load_events(args.input)
    if not events:
        sys.stderr.write(f"warning: no events in {args.input}\n")

    # Per-skill activation count (event == "skill_fired").
    activations: Counter[str] = Counter()
    # Co-invocation: pairs of skills firing in the same session.
    sessions: dict[str, set[str]] = defaultdict(set)
    outcomes: Counter[str] = Counter()

    for ev in events:
        ev_type = ev.get("event")
        skill = ev.get("skill", "")
        session = ev.get("session_id", "")
        outcome = ev.get("outcome", "")
        if ev_type == "skill_fired" and skill:
            activations[skill] += 1
            if session:
                sessions[session].add(skill)
        if outcome:
            outcomes[outcome] += 1

    # Co-invocation matrix (sparse): {(skill_a, skill_b): count}
    co_invoke: Counter[tuple[str, str]] = Counter()
    for skills_in_session in sessions.values():
        skill_list = sorted(skills_in_session)
        for i in range(len(skill_list)):
            for j in range(i + 1, len(skill_list)):
                co_invoke[(skill_list[i], skill_list[j])] += 1

    if args.format == "json":
        print(json.dumps(
            {
                "total_events": len(events),
                "activations": dict(activations),
                "outcomes": dict(outcomes),
                "co_invoke": [
                    {"a": a, "b": b, "count": n} for (a, b), n in co_invoke.most_common()
                ],
            },
            indent=2,
        ))
    else:
        print(f"analytics-rollup: {len(events)} events from {args.input}")
        print()
        print("Per-skill activations:")
        for skill, n in activations.most_common():
            print(f"  {skill}: {n}")
        print()
        print("Outcomes:")
        for outcome, n in outcomes.most_common():
            print(f"  {outcome}: {n}")
        print()
        print(f"Co-invocation pairs: {len(co_invoke)}")
        for (a, b), n in co_invoke.most_common(5):
            print(f"  {a} ↔ {b}: {n}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
