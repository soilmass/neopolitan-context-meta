# Skill Discoverability

**Build trigger:** library has 50+ skills and description-matching
alone can't reliably surface the right skill for a given prompt. Per
`ARCHITECTURE.md` §"Routing and Contention" scaling table, this is
the same threshold where the routing eval suite becomes load-bearing.

**Pre-trigger applicability:** *None.* The library has 14 skills as
of v0.5.0. The routing-contention discipline (anti-triggers + audit
ritual + per-domain routers) handles discovery at this scale.
Description-matching plus the `meta` router carries the load until
the threshold fires.

---

## What discoverability covers beyond description-matching

Once a library exceeds 50 skills, the LLM's natural-language
match-on-description starts producing routing errors that no amount
of anti-trigger discipline can fix. Discoverability adds:

- **Tags** — explicit category labels per skill (`category: vcs`,
  `category: ops`, `category: data`).
- **Domain hierarchy** — explicit parent/child relationships (e.g.,
  `git-collaboration` is a *child of* `git`).
- **Search** — keyword search over descriptions + capabilities (not
  LLM-mediated; mechanical).
- **Skill index** — a generated `INDEX.md` listing every skill with
  category + one-line description.

## Tags

Per skill, in `metadata.tags:` (a new optional frontmatter field):

```yaml
metadata:
  version: "1.0.0"
  archetype: atom
  tags:
    - git
    - vcs
    - daily-use
```

Tags are free-form but conventions emerge: `<domain>`, `<archetype-aspect>`,
`<usage-tier>` (e.g., `daily-use` / `weekly` / `rare`). The
`meta` router uses tags to prefilter the candidate set before
description-matching.

## Domain hierarchy

Per family, in the family's `coverage.md`:

```markdown
## Domain hierarchy

This family is a child of: (none — root family)
This family parents: (none currently)
This family is sibling to: docker, podman (container runtimes)
```

The hierarchy is informational (helps operators discover related
families) and feeds the cross-domain orchestrator pattern from
`ARCHITECTURE.md`.

## Search

A `scripts/search-skills.py` (deferred) takes a query string and:
- Searches skill descriptions by token overlap.
- Searches `## Capabilities Owned` body content.
- Searches tags.
- Returns a ranked list with relevance scores.

This is mechanical (TF-IDF or similar), not LLM-mediated. It exists
specifically because LLM matching fails at scale.

## Skill index

`scripts/gen-index.py` (deferred) produces `INDEX.md` at the library
root listing every skill with:
- name + version
- archetype
- category tags
- one-line description (first sentence of frontmatter description)
- path

The index updates automatically on every release via
`release-tag.sh` (when extended).

## Implementation

When the trigger fires:

1. `metadata.tags` is added to the frontmatter spec
   (`skills/skill-author/references/frontmatter-spec.md`) as an
   optional field.
2. `scripts/search-skills.py` is authored.
3. `scripts/gen-index.py` is authored.
4. `coverage.md` schema gains an optional `## Domain Hierarchy`
   per-family section.
5. The `meta` router (this library's per-cluster router) gains a
   tag-prefilter step before its disambiguation protocol.

## Cross-references

- `MAINTENANCE.md` §Gate 3 (triggering accuracy) — companion gate.
- `skills/skill-evaluate/SKILL.md` — Gate 3's mechanizer; tags feed
  its `--skill <tag>` filtering.
- `coverage.md` Domains Deferred — gates the trigger.
- `ARCHITECTURE.md` §"Routing and Contention" scaling table — the
  50-skill threshold.

## Out of scope

- Visual / GUI search interfaces.
- LLM-mediated semantic search beyond what description-matching
  already does.
- Marketplace-level discoverability (cross-library — out of scope
  per `governance/INDEX.md` §Out of Scope §"Skill marketplace
  mechanics").
