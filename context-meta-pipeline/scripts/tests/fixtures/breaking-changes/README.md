# Breaking-changes fixture pairs

Each subdirectory is a *pair fixture* — a `MODIFIED.md` (the changed
version) plus a `meta.yaml` recording:

- `baseline:` — relative path to the baseline SKILL.md under
  `../../baselines/`
- `expected_exit:` — 0 (no breaking change), 1 (breaking + improperly
  handled, blocks merge), or 2 (breaking + properly handled,
  informational)
- `pass_exercised:` — which detector pass(es) the modification
  triggers (frontmatter / section removal / capability change /
  routing change)

verify.sh step 7 iterates these directories, invokes
`detect-breaking-changes.py --baseline <baseline> --skill MODIFIED.md`,
and compares the actual exit code to expected_exit.

## Pairs

- `pair-no-change/` — exit 0; identical files (atom)
- `pair-capability-removed-no-bump/` — exit 1; capability removed without MAJOR bump
- `pair-capability-removed-major-bumped/` — exit 2; capability removed AND version bumped to MAJOR
- `pair-section-removed/` — exit 1; required section gone
- `pair-description-30pct-rewrite/` — exit 1; description >30% character delta
- `pair-router-target-changed/` — exit 1; router routing-table target change
- `pair-router-entry-added/` — exit 0; new routing entry is MINOR (additive)
- `pair-tool-allowed-tools-removed/` — exit 1; allowed-tools entry removed
