# Naming Conventions

Locked. Generated atoms inherit these automatically through `family-bootstrap`.

## Scope: this regex applies to SKILL.md `name` only

The conventions in this file govern the `name:` field in a SKILL.md's
frontmatter — i.e., **the skill itself**, the directory it lives in,
and the way it's referenced from routers and other skills.

They do **NOT** govern:

- **Capability names** in body bullets (e.g., `## Capabilities Owned`
  entries like "fixup / autosquash" or "log (filtered)"). These are
  human-readable prose lifted from the domain authority's vocabulary.
  See `family-bootstrap/references/tier-model.md` §"Capability-to-tier
  mapping convention" for capability-name conventions.
- **Citation strings** in `capabilities.json` (e.g.,
  "Pro Git §7.6 'Rewriting History'"). These are unconstrained
  natural-language references.
- **Free-text descriptions** anywhere.

The naming regex below is for the SKILL.md `name` field exclusively.

## The naming regex

```
^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$
```

In words: lowercase, kebab-case, **≤4 segments** separated by hyphens.
Underscores not allowed. Version numbers not allowed in names (use
`metadata.version` in frontmatter instead).

`validate-metadata.py` enforces this regex. A name that fails the regex
blocks merge.

## Domain prefix

The user's mental-model name for the tool, not the binary:

| Binary | Mental model | Skill prefix |
|---|---|---|
| `psql` | postgres | `postgres-*` |
| `awscli` | aws | `aws-*` |
| `kubectl` | kubectl | `kubectl-*` |
| `git` | git | `git-*` |

## Scope segment

Use the domain's own canonical vocabulary:

- Git's docs say "history rewriting" → `git-history-rewriting`
- Kubectl's docs say "cluster state" → `kubectl-cluster-state-mutations`
- Postgres's docs say "transaction isolation" → `postgres-transaction-isolation`

The scope name should describe the failure mode using the domain's own
term. Official docs usually name dangerous areas explicitly.

## Universal suffixes

Three categories override domain vocabulary because they recur across
every domain. Predictability beats native vocabulary here:

- `-inspection` for read-only operations
- `-recovery` for repair and restoration
- `-config` for configuration and setup

## Plumbing vs porcelain

Default is porcelain (user-facing capabilities). Plumbing skills get the
explicit `-plumbing` suffix. Most domains do not need plumbing atoms.

## Routers

Bare domain mental-model name. `git`, `postgres`, `kubectl`, `aws`.
Never suffixed.

## Policy overlays

Three-segment form `<context>-<domain>-<aspect>`:

- `house-git-conventions`
- `acme-postgres-rules`
- `house-test-style`

Three segments signal that the skill modifies a domain rather than being
one.

## Forbidden patterns

- Underscores: `git_history` ✗ (should be `git-history`)
- Version numbers: `pdf-v2` ✗ (use `metadata.version`)
- More than 4 segments: `kubectl-cluster-state-mutations-advanced` ✗
- Mixed case: `gitHistoryRewriting` ✗
- Spaces: `git history` ✗

## Examples that pass

- `pdf-reading`
- `git-history-rewriting`
- `kubectl-cluster-state-mutations` (4 segments — the cap)
- `house-git-conventions`
- `skill-author`
- `family-bootstrap`

## Examples that fail

- `Git-Rewrite` (uppercase)
- `pdf_reading` (underscore)
- `git-history-rewriting-conflicts` (5 segments)
- `pdf-2.0` (version in name)
