# Audit-skill fixture harnesses

Each harness sets up a temp `--root` containing a `skills/<name>/SKILL.md`
fixture, then invokes `audit-skill.py --skill <name> --root <tmp>` and
checks the exit code + relevant gate output.

## Why harnesses, not raw .md files

`audit-skill.py` requires a `--root` containing a `skills/` directory.
A bare `.md` fixture isn't enough — the script needs the directory
shape. Harnesses create that shape in a temp dir, run the audit, and
clean up.

## Harnesses

- `pass-fresh-skill.sh` — clean SKILL.md, recent mtime; expect exit 0
- `fail-stale-recency.sh` — mtime backdated >6 months; expect exit 1 (Gate 1)
- `fail-description-drift.sh` — description claims things absent from body; expect exit 1 (Gate 4)
- `fail-multi-gate.sh` — Gates 1 and 4 both fail; expect exit 1

Each harness echoes a single PASS/FAIL line for verify.sh to grep.
