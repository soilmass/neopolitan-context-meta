# Expected per-family coverage.md skeleton (Stage 6 output)
#
# Per family-bootstrap/references/coverage-template.md, the output
# coverage.md should have all six required sections. Section *names*
# are fixed; section *contents* depend on authoring choices.
#
# Tier sizes from the dogfood input (expected_size=8):
#   Tier 1: 8 atoms
#   Tier 2: 5 atoms (specced, not built)
#   Tier 3: 4 atoms (deferred with observable build triggers)
#
# Out-of-Scope rows: ≥1 (gate); the dogfood produced 5.

## Required sections (6, all present, all non-empty)

- In Scope (Tier 1)
- Specced, Not Yet Built (Tier 2)
- Deferred (Tier 3)
- Policy Overlay
- Out of Scope
- Coverage Matrix Status

## Tier-1 atoms expected (per dogfood)

git-basics, git-branching, git-history-rewriting, git-recovery,
git-collaboration, git-inspection, git-config, git-hooks

## Tier-2 atoms expected (specced)

git-stash, git-tags, git-submodules, git-worktrees, git-rerere

## Tier-3 atoms expected (deferred)

git-plumbing, git-large-repo, git-credentials, git-server

## Out of Scope rows expected (≥1; dogfood had 5)

- Workflows (gitflow, trunk-based) — policy not mechanism
- GitHub-specific operations — different domain
- GUI clients — not git-the-tool
- git filter-branch — deprecated by Pro Git in favor of filter-repo
- Pre-commit-the-framework — wraps hooks; one layer above
