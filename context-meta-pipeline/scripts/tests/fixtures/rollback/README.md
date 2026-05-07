# Rollback-skill fixture harnesses

Each harness is a self-contained shell script that:

1. Creates a temporary directory under `/tmp/`.
2. Initializes a git repo there.
3. Commits a synthetic plugin layout (`skills/<name>/SKILL.md`,
   `SNAPSHOT.lock`, `CHANGELOG.md`) at one or more versions.
4. Invokes `rollback-skill.py --dry-run` against the temp repo.
5. Compares the actual exit code to the expected.
6. Cleans up the temp directory.

The harnesses use `--dry-run` exclusively — no actual writes to git.
This keeps fixtures safe and idempotent.

## Skip-if-no-git

verify.sh step 7 invokes each harness with:

```bash
if command -v git >/dev/null 2>&1; then
  bash <harness>
else
  echo "WARN  git not on PATH — skipping rollback fixtures"
fi
```

Mirrors the ruff/mypy "skip if not installed" pattern in the Makefile.

## Harnesses

- `pass-dry-run.sh` — successful rollback dry-run; exit 0
- `fail-version-not-in-history.sh` — target version never committed; exit 1
- `fail-snapshot-mismatch.sh` — SNAPSHOT.lock has no entry for the skill; exit 1

Each harness echoes a single PASS/FAIL line that verify.sh greps.
