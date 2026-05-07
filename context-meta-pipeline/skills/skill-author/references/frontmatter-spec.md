# Frontmatter Specification

Every SKILL.md begins with YAML frontmatter delimited by `---` lines.
This is the contract `validate-metadata.py` enforces.

## Required fields

```yaml
---
name: <kebab-case, ≤4 segments>
description: >
  <Third-person, ≤1024 characters, includes a "Do NOT use for" block.>
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom | tool | router | orchestrator | policy
  changelog: |
    v0.1.0 — initial.
---
```

## Field details

### `name`

Required. String. Must match the naming regex (see `naming.md`).

The validator compares this against the regex. The breaking-change
detector treats any change to `name` as breaking.

### `description`

Required. String. Third-person prose, ≤1024 characters total.

Must contain a literal "Do NOT use for" block (or close variants:
"Do not use for", "do NOT use for"). The block names siblings or
out-of-scope cases that should NOT route here. Without this block, every
adjacent skill on natural-language matching becomes a routing competitor.

Should:
- Start with a verb in third person ("Authors…", "Validates…", "Routes…").
- Include trigger phrases the operator would naturally use.
- Not begin with the skill name verbatim — the description should
  *explain*, not *restate*.

Should not:
- Use first/second-person pronouns ("I…", "You can…").
- Exceed 1024 characters.
- Skip the anti-trigger block.

### `license`

Required. String. Typically `Apache-2.0` or `MIT`. Whatever applies.

### `metadata.version`

Required. String. Valid SemVer (`MAJOR.MINOR.PATCH`).

The breaking-change detector enforces MAJOR-bumps when capabilities are
removed, sections disappear, etc. See `governance/BREAKING-CHANGE-DETECTION.md`.

### `metadata.archetype`

Optional but strongly recommended. Lowercase string from:
`atom`, `tool`, `router`, `orchestrator`, `policy`.

If absent, the validator infers `atom` (and may issue a warning). Setting
it explicitly disambiguates.

### `metadata.changelog`

Required. String (block-scalar). Must mention at least the current
version. Per-skill changelog format is human-readable prose, one line
per version, newest first:

```yaml
changelog: |
  v1.4.2 — patch: clarified disambiguation protocol example.
  v1.4.0 — minor: added bisect routing entry.
  v1.0.0 — initial.
```

The `metadata.changelog` field is *not* machine-parsed for the library
`CHANGELOG.md`. The library CHANGELOG is authored separately.

## Optional fields

### `allowed-tools`

Optional. List of tool names the skill needs (`Read, Write, Edit`, etc.).
Removing a tool from this list is breaking — downstream skills may have
relied on the tool being available.

### `model`

Optional. Required model name when the skill assumes specific model
behavior. Changing this is breaking.

### `archived: true`

Optional. Set by `skill-retire` Stage 3. The skill remains pinnable but
the SNAPSHOT.lock no longer lists it as canonical.

### `metadata.recency_pin: stable`

Optional. Acknowledged-as-complete marker. When set, `skill-audit` Stage 2
treats the recency gate as passing even if the skill's last commit is
older than the 6-month threshold. Intended for genuinely stable, complete
skills where age is not a staleness signal.

Set this only after deliberation — the recency gate exists to surface
abandonment, and pinning bypasses that signal. Re-evaluate at every audit
run; remove the pin if the underlying domain or authority docs change.

See `skill-audit/references/health-gates.md` Gate 1 for the semantics.

### `metadata.tags`

Optional list of kebab-case tags for skill discovery. Added in v0.7.0 to
support `scripts/search-skills.py` token-overlap search and `INDEX.md`
generation via `scripts/gen-index.py`. The canonical tag taxonomy is small
by intent — editorial drift is the failure mode this list prevents.

Canonical tag set (v0.7.0):

| Tag | When to apply |
|---|---|
| `lifecycle` | Skill operates on the lifecycle of other skills (skill-author / skill-audit / skill-refactor / skill-retire / skill-migrate). |
| `composition` | Skill builds new structure by composing existing skills (family-bootstrap, library-bootstrap, cross-domain-orchestrator-author, cross-library-orchestrator). |
| `health` | Skill assesses or surfaces health (skill-audit, library-audit, skill-evaluate). |
| `provenance` | Skill addresses authenticity, signing, hashing (provenance-related). |
| `router` | Archetype is `router`. The tag is redundant with archetype but lets search-skills filter on dispatching skills. |
| `discoverability` | Skill produces an index, search, or tag artifact. |
| `daily-use` | Operator likely invokes this multiple times per week. |
| `weekly` | Operator invokes ~weekly (audit cadence; release-prep). |
| `rare` | Operator invokes infrequently (skill-retire, library-bootstrap, skill-migrate when MAJOR bumps fire). |

Format: YAML list of strings. Each value must match the naming regex
`^[a-z][a-z0-9-]*$` (kebab-case, no leading digits). 2-3 tags per skill is
the convention; ≤5 is the cap. Tags are *not* required (validate-metadata
treats empty/absent as fine), but `search-skills.py` ranking weights tags
heavily, so unannotated skills surface below their tagged peers.

Adding a new tag is a v0.7.x discipline question — do not introduce
single-skill tags. If the use case isn't represented in the table above,
either pick the closest existing tag, propose a new tag in a CHANGELOG
entry, or omit the tag entirely.

See `scripts/search-skills.py` for the tokenization and ranking logic.

## What the validator checks

| Check | Severity | Source |
|---|---|---|
| `name` present, kebab-case, ≤4 segments | error | naming regex |
| `description` ≤1024 chars | error | METADATA-VALIDATION.md |
| `description` contains "Do NOT use for" | error | METADATA-VALIDATION.md |
| `license` present | error | METADATA-VALIDATION.md |
| `metadata.version` valid SemVer | error | METADATA-VALIDATION.md |
| `metadata.changelog` present, mentions current version | error / warning | METADATA-VALIDATION.md |
| Description is third-person | warning | description-quality |
| Description does not duplicate name | warning | description-quality |

## What the breaking-change detector checks

| Change | Breaking? |
|---|---|
| `name` changed | yes |
| `description` rewritten >30% | flagged for review |
| `allowed-tools` entry removed | yes |
| `model` changed | yes |
| Required section removed | yes |
| `Capabilities Owned` entry removed (atoms) | yes |
| `Routing Table` entry removed or target changed (routers) | yes |
| New section added | no |
| New capability added (atoms) | no |
| New routing entry added (routers) | no |

See `governance/BREAKING-CHANGE-DETECTION.md` for the full catalog.
