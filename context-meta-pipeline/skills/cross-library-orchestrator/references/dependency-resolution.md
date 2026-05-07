# dependency-resolution.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library
> (specifically: when ≥2 libraries are simultaneously installed).

How orchestrators that span library boundaries resolve dependencies. This
is the hardest case — different libraries have independent SNAPSHOT.locks,
independent versioning, and may pin to different versions of the same
external dependency.

## Why cross-library is different

Within one library:
- single `SNAPSHOT.lock` is the source of truth for which skills exist;
- single CHANGELOG; single coverage.md;
- `depends_on:` pins resolve trivially against the same snapshot.

Across libraries:
- two SNAPSHOT.locks; the orchestrator might pin different versions of the
  same skill in each library;
- CHANGELOGs are independent; release cadences differ;
- `depends_on:` resolution requires looking up which library exposes which
  skill, then resolving against THAT library's snapshot.

## The pinning model

A cross-library orchestrator's `depends_on:` uses an extended syntax:

```yaml
depends_on:
  - context-git/git-history-rewriting@1.2.0
  - context-cloud/deploy-blue-green@0.3.1
```

Format: `<library-name>/<skill-name>@<version>`. The library name is the
plugin name from `.claude-plugin/plugin.json`, not a path.

Resolution rules:
1. The orchestrator must declare both libraries it depends on in its own
   library's `governance/INDEX.md` (so the operator knows which to install).
2. Each pinned skill's version is checked against the named library's
   SNAPSHOT.lock at install time, not authoring time.
3. If a library is installed but at the wrong version, the orchestrator
   refuses to fire and surfaces the mismatch.

## When NOT to use cross-library orchestrator

- The "cross-library" is actually one library that hasn't been split yet.
  Author a regular `cross-domain-orchestrator-author` instead, then refactor
  the library if/when the split is justified.
- The orchestrator only references one library, with a single skill from
  another library as a "would be nice." Just author against the single
  library; don't introduce cross-library complexity.
- The two libraries have wildly different release cadences and the
  orchestrator's pin would constantly drift. That's a design smell —
  consolidate or accept the drift discipline cost.

## Author conventions

When authoring a cross-library orchestrator:

1. Declare both libraries as required in the orchestrator's library's
   `coverage.md` "Out of Scope" or a new "External Dependencies" section.
2. Pin skills using the extended `<library>/<skill>@<version>` syntax.
3. Document the version-resolution behavior (refuse-on-mismatch) in the
   orchestrator's "Edge Cases" section.
4. Author `## Refresh procedure` describing what the operator does when
   either library publishes a new version.

## Audit ritual

The audit ritual for cross-library orchestrators must check:

- both libraries are installed at the pinned versions
- the orchestrator's description doesn't conflict with any in-library
  skill's description (cross-library contention is harder to spot)
- the cross-library `depends_on:` syntax parses correctly via
  `validate-metadata.py:check_depends_on_freshness` (extension pending —
  v0.6.1's check assumes intra-library only)

## Open question

How does `validate-metadata.py:check_depends_on_freshness` (v0.6.1)
interact with cross-library pins? Today it assumes the pinned skill is in
the same SNAPSHOT.lock; cross-library pins would need an additional
`<library>/` prefix in the parser. Deferred until first real consumer
library exists.
