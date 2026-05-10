# Troubleshooting `context-site-build`

Common errors per atom + per-stack-overlay + drift-gate guidance.
For library-architecture questions, see `LIBRARY-MAP.md`. For
versioning, see `VERSIONING-POLICY.md`.

---

## Validation errors

### "Description exceeds 1024 characters"

The frontmatter `description` field has a hard 1024-char cap.
Trim:

1. Drop trailing "… or X" enumeration suffixes.
2. Compress "Do NOT use for: A; B; C; D" to fewer (most-load-
   bearing) items.
3. Compact "(use the user-invocable draft-X covers it now)" to
   "(user-invocable draft-X)".

Common causes:
- Long anti-trigger lists (5+ siblings).
- Verbose first-sentence purpose statement.
- Marketing-copy adjectives ("comprehensive", "robust",
  "best-in-class").

### "Skill name fails the regex"

The regex is `^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$` (≤ 4 hyphen-
separated kebab-case segments). Common mistakes:

- 5+ segments — collapse compound nouns or rename.
- Underscores — replace with hyphens.
- CamelCase — kebab-case.
- Trailing hyphens.
- Numbers as first character.

### "Required section missing for archetype X"

Each archetype has required sections enforced by
`validate-metadata.py`. See
`context-meta-pipeline/skills/skill-author/references/archetypes.md`
for the per-archetype rubric. Most common:

- `atom` missing `Capabilities Owned` / `Handoffs to Other Skills`
  / `Edge Cases` / `References`.
- `tool` missing `Stage-Gated Procedure` / `Dependencies` /
  `Evaluation` / `Handoffs`.
- `policy` missing `Applies On Top Of` / `Conventions Enforced` /
  `Override Behavior`.
- `router` missing `Routing Table` / `Disambiguation Protocol` /
  `Atoms in This Family`.

---

## Drift-gate failures (skill-audit)

**Description-drift** = description tokens that don't appear in the
body. Threshold: < 10%. Per `context-meta-pipeline/skills/skill-
author/references/audit-ritual.md` "Common drift signals on fresh
atoms":

| Drift cause | Fix |
|---|---|
| Phase-name suffixes ("kickoff", "during Phase X start") | Use the body's exact phrase ("Phase 1 Discovery") |
| Temporal hedges ("around T+8 weeks") | Use precise form ("at T+8 weeks") |
| Verb form mismatches ("Writes" vs "Write" / "writes the …") | Match body exactly |
| Abstract framing ("the artifact that **sets** why") | Use body's concrete operation ("compose a one-paragraph statement") |
| Filler structure words ("structured", "around", "during") | Drop them; rare in body |

**Fix discipline**: tighten the **description**, not the body.

---

## Anti-trigger fallback failures

**Anti-pattern**: `(use X-author when authored)` — unactionable for
the LLM router because the skill doesn't exist.

**Pattern that works** (per `context-meta-pipeline/skills/skill-
author/references/audit-ritual.md` "Anti-trigger fallback
discipline"):

```
Do NOT use for: <topic> (use X-author once built; the user-invocable
draft-X covers it now).
```

OR for cross-family deferred siblings:

```
Do NOT use for: <topic> (handled by the future <family> family;
the user-invocable draft-<topic> covers it now).
```

OR if no peer exists:

```
Do NOT use for: <topic> (use X-author once built; no user-invocable
peer exists for this Awwwards-tier addition).
```

---

## Coverage.md gaps

### "atom referenced but not in coverage"

If an atom's anti-trigger references a sibling that's not in the
family's `coverage.md`, surface as a `B`-series finding. Decide:

1. Is it **in-family-deferred** (Specced, Not Yet Built)? Add row
   to that section.
2. Is it **out-of-scope** (different family / not in this library)?
   Add row to "Out of Scope" with a "where it lives instead"
   pointer.

Per `context-meta-pipeline/skills/family-bootstrap/references/scope-
discipline.md`, the distinction matters — vocabulary differs.

### "v0.5.0–v1.0.0 Ahead-of-Trigger Note absent"

If `coverage.md` has skills from the v0.5.0+ ahead-of-trigger
window without the disclosure section, the operator added skills
without honoring the A56 commitment. Restore by adding the section
+ the per-skill top-of-body markers per the v0.5.0 pattern.

---

## Stack-overlay specific issues

### "house-site-build-X applies but I'm on stack Y"

The mechanism atoms work stack-agnostic. Stack overlays specialize
mechanism for one stack. If you're on Y and citing the X overlay,
the citation is wrong:

1. Switch to `house-site-build-Y` (if Y is one of the supported
   stacks: nextjs / nuxt / astro / sveltekit / webflow).
2. If Y is unsupported, mechanism atoms apply directly without an
   overlay; the SRS NFRs become advisory rather than enforced.

### "depends_on resolves to skill-author@X.Y but X.Y doesn't exist"

The `depends_on:` pin is stale. SNAPSHOT.lock `depends_on` should
reflect current versions. Run:

```bash
grep -n "depends_on" SNAPSHOT.lock
```

Update each pin to the current version. The meta-pipeline's
A65 fix (`release-tag.sh --allow-unsigned`) won't help here — this
is a content-edit, not a script-flag fix.

### "Multiple stack overlays apply"

A project can pick exactly **one** per family per consumer surface:
either `house-site-build-nextjs` OR `house-site-build-nuxt`, not
both. Cross-stack overlays (motion / a11y / figma) compose ON TOP of
the per-stack overlay; hosting overlays compose under it.

---

## Cross-cutting tool atom issues

### "performance-budget.md cites a stack overlay's bundle table — different"

Each stack overlay's bundle table specializes (Astro is tighter than
Combo A; SvelteKit is the strictest). The per-stack overlay's
table OVERRIDES `performance-budget.md`'s general table when
applicable. CI gates use the more-specific (smaller) of the two.

### "motion-conformance-author + house-site-design-a11y feel duplicative"

They're not. `motion-conformance-author` is the **cross-cutting
tool atom** (free-standing; produces docs). `house-site-design-a11y`
is the **policy overlay** (overlays mechanism atoms; CSS-cascade
override semantics). The atom defines the patterns; the overlay
applies them per-component. Both are needed for full coverage.

### "Cross-PR fallback qualifier still in overlay description"

The 21 stack overlays (v0.5.0) cite the 7 cross-cutting atoms
(v0.6.0) via the A62 anti-trigger fallback pattern: `(use X-author
once built; the user-invocable draft-X covers it now)`. With the
atoms now built, the qualifier should drop. The cleanup landed in
PR #8 (the v1.0-readiness docs PR); if your branch predates that
merge, rebase + the cleanup will apply.

---

## Verify.sh failures

### "INDEX.md is stale"

Only applies to `context-meta-pipeline` (which uses `gen-index.py`).
This library doesn't ship an `INDEX.md`; `verify.sh` here doesn't
include the discoverability step.

### "validate-metadata --all errors with exit 2 on empty skills/"

If you bootstrap a fresh library and `verify.sh` errors, the
`validate-metadata.py --allow-empty` flag exists per A57. Add to
your library's `verify.sh`:

```bash
python3 ../context-meta-pipeline/scripts/validate-metadata.py --all --allow-empty
```

### "snapshot-hash.py --verify fails"

Only applies to `context-meta-pipeline`. This library's
SNAPSHOT.lock doesn't ship sha256 fields per its simpler schema.

---

## Library-versus-library issues

### "context-site-build cites context-meta-pipeline atom that doesn't exist"

The meta-pipeline's `skill-author`, `family-bootstrap`,
`skill-policy-overlay`, `skill-migrate` etc. should be installed
alongside this library for the authoring procedures to work. If
you cited e.g. `library-bootstrap` in a context-site-build artifact
and the atom isn't installed, install context-meta-pipeline OR
swap the citation to a user-invocable peer (less common).

### "marketplace.json + plugin.json + SNAPSHOT.lock disagree"

Run `verify.sh` step 4 (version triangulation). All three should
agree on the library version (e.g., `0.6.0`). The `release-tag.sh`
script (in context-meta-pipeline) gates on this.

---

## Audit findings (B-series)

The library's audit-finding ledger lives in `coverage.md`
"Audit-finding ledger" section. New findings get a sequential
`B` number (B1, B2, …); cross-reference to meta-pipeline `A` series
when relevant.

| If you find | File as |
|---|---|
| validate-metadata bug | New B (cross-ref to A if also a meta-pipeline issue) |
| Drift-gate failure on fresh atom | New B (referencing A60 / B4 pattern) |
| Coverage discipline gap | New B (referencing A63 / B7 if scope-discipline) |
| Anti-trigger fallback issue | New B (referencing A62 / B6) |
| Routing-table includes unbuilt atom | New B (referencing A64 / B8) |

---

## When all else fails

1. Check `coverage.md` audit-finding ledger for prior occurrences.
2. Check `context-meta-pipeline/CHANGELOG.md` for the most-recent
   meta-pipeline patches that may have addressed the issue.
3. Cross-reference your finding against the meta-pipeline's `A`
   series to see if it's a known issue.
4. File a B-series finding in `coverage.md` with the failure mode +
   reproduction steps + suggested remediation.

---

## See also

- `LIBRARY-MAP.md` — dependency graph for atom-citation reasoning.
- `VERSIONING-POLICY.md` — for SemVer-bump-decision questions.
- `coverage.md` — for the audit-finding ledger + the cumulative
  discipline shifts (A56 + B9).
- `context-meta-pipeline/governance/METADATA-VALIDATION.md` — the
  validator's source of truth for the rules this library enforces.
