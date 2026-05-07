#!/usr/bin/env python3
# pre-trigger build (v0.7.0); STUB only — real load-time hooking blocked
# on Claude Code core support per governance/USAGE-ANALYTICS.md.
"""
telemetry-hook.py — STUB. Documents the JSONL event schema that
governance/USAGE-ANALYTICS.md specifies, but does NOT actually hook into
Claude Code's load-time mechanism (that mechanism does not exist outside
the plugin's process).

When invoked directly, prints the schema to stdout and exits 0. When
sourced/imported by a future Claude Code core load-time hook, it would
write to scripts/tests/analytics/<date>.jsonl. That hook does not exist
at v0.7.0; this stub exists so:

  1. Consumer libraries see what telemetry-format the meta-pipeline
     would consume if telemetry were available.
  2. analytics-rollup.py (sibling script) has a documented format to
     consume from real OR synthetic JSONL files.
  3. When Claude Code core gains the load-time hook, the contract is
     pre-defined and stable.

Schema (one event per JSONL line):

    {
      "ts": "2026-05-06T14:32:01Z",
      "event": "skill_fired" | "skill_loaded" | "skill_completed",
      "skill": "<skill-name>",
      "session_id": "<opaque>",
      "prompt_hash": "<sha256 of prompt; NEVER the prompt itself>",
      "co_invoked": ["<other skills fired in same session>"],
      "outcome": "success" | "error" | "partial"
    }

Privacy: per USAGE-ANALYTICS.md, prompt content is NEVER logged. Only the
hash. Session IDs are opaque.

Exit codes:
  0  schema printed (the only mode this stub supports)
  2  invocation problem (e.g., --record without a hook, which is impossible)

Usage:
  telemetry-hook.py                # print schema documentation
  telemetry-hook.py --schema-json  # print schema as JSON

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SCHEMA: dict[str, Any] = {
    "$comment": (
        "Event schema for governance/USAGE-ANALYTICS.md telemetry. "
        "One event per JSONL line. Privacy: prompt content NEVER logged."
    ),
    "fields": {
        "ts": {"type": "string", "format": "ISO 8601", "required": True},
        "event": {
            "type": "string",
            "enum": ["skill_fired", "skill_loaded", "skill_completed"],
            "required": True,
        },
        "skill": {"type": "string", "required": True},
        "session_id": {"type": "string", "required": True, "note": "opaque"},
        "prompt_hash": {"type": "string", "format": "sha256-hex", "required": True},
        "co_invoked": {"type": "array", "items": "string", "required": False},
        "outcome": {
            "type": "string",
            "enum": ["success", "error", "partial"],
            "required": False,
        },
    },
    "stub_status": "v0.7.0 ahead-of-trigger; real hook depends on Claude Code core",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--schema-json", action="store_true",
                        help="emit schema as JSON (for tooling)")
    args = parser.parse_args(argv)

    if args.schema_json:
        print(json.dumps(SCHEMA, indent=2))
    else:
        print("telemetry-hook.py — STUB (v0.7.0 ahead-of-trigger).")
        print()
        print("Real load-time hooking blocked on Claude Code core. This stub")
        print("documents the JSONL event schema that analytics-rollup.py would")
        print("consume from real OR synthetic JSONL fixtures.")
        print()
        print("Schema:")
        for field_name, spec in SCHEMA["fields"].items():
            req = "required" if spec.get("required") else "optional"
            print(f"  {field_name} ({spec['type']}, {req})")
        print()
        print("Run with --schema-json to emit machine-readable schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
