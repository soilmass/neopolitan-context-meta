# Redirect Note Template

Stage 3 of `skill-retire` prepends a redirect block to the target's
SKILL.md body, immediately after the H1 heading.

## The block

```markdown
> **⚠️ This skill is retired.**
>
> <One-paragraph reason from retirement-justification.md.>
>
> **Replacement:** `<replacement-skill>`
> (or: "no direct replacement — see [pointer]")
>
> Last canonical version: v<current>.
> Retired: <YYYY-MM-DD>.
```

## Per-reason variants

### Absorbed

```markdown
> **⚠️ This skill is retired.**
>
> Absorbed into `<absorbing-skill>` as part of a refactor that consolidated
> overlapping responsibilities.
>
> **Replacement:** `<absorbing-skill>` — covers all capabilities
> previously owned by this skill.
>
> Last canonical version: v<current>.
> Retired: <YYYY-MM-DD>.
```

### Replaced

```markdown
> **⚠️ This skill is retired.**
>
> Replaced by `<replacement-skill>`, which covers the same scope with
> [improved approach / corrected design / additional capabilities].
>
> **Replacement:** `<replacement-skill>` (see migration guide at
> `<path-to-migration>`).
>
> Last canonical version: v<current>.
> Retired: <YYYY-MM-DD>.
```

### Domain-gone

```markdown
> **⚠️ This skill is retired.**
>
> The underlying domain (`<domain-name>`) has been deprecated by its
> upstream maintainers — see [deprecation announcement](<URL>).
> No replacement is appropriate because the domain itself is gone.
>
> **Replacement:** none.
>
> Last canonical version: v<current>.
> Retired: <YYYY-MM-DD>.
```

### Health-failure

```markdown
> **⚠️ This skill is retired.**
>
> This skill failed health gates for ≥12 months and was not maintained.
> Per `MAINTENANCE.md`, an unmaintained skill remains installable but
> the library snapshot no longer lists it as canonical.
>
> **Replacement:** none in the canonical library. If you need this
> skill, you may pin to v<current> in your own lockfile, with the
> understanding that it is unmaintained.
>
> Last canonical version: v<current>.
> Retired: <YYYY-MM-DD>.
```

## Frontmatter additions

Stage 3 also adds `archived: true` to the frontmatter and prepends to
`metadata.changelog`:

```yaml
---
name: <skill-name>
description: <unchanged>
license: <unchanged>
archived: true
metadata:
  version: "<current>"
  archetype: <unchanged>
  changelog: |
    v<current> (retired, <YYYY-MM-DD>) — <reason>. <pointer>.
    v<previous> — <previous changelog entries preserved>.
---
```

The description is **not modified** in Stage 3. The redirect block in
the body is the user-visible signal. The description stays so that any
remaining LLM-routing match against the description still produces a
reasonable answer (the LLM reads the redirect block on first use).

## What the block must contain

- The literal warning marker `⚠️ This skill is retired.`
- The reason (one of four).
- Either a named replacement OR an explicit "no replacement" with rationale.
- The last canonical version.
- The retirement date.

## What the block must NOT contain

- A claim that the skill still works as-is. Pinned users get the
  pre-retirement content; new users see this block.
- Editorial commentary on why the skill was bad. Be factual.
- Promises about future replacements that aren't already in the library.

## Validation

The redirect block must not break the structural validators:

- `validate-metadata.py` continues to pass on the archived skill — the
  redirect block is *prepended* to the body, the required sections
  remain, and all universal frontmatter rules continue to apply.
- The `archived: true` field is a marker for tooling (and for human
  readers reading the SKILL.md). The validator does not currently
  treat it specially; it just preserves the spec invariant that all
  required sections remain present.

A future relaxed-rules path (e.g., letting an archived skill drop
its required sections so the SKILL.md becomes "redirect note only")
is **not** in v0.2.x. If that becomes worth doing, it requires:

1. A `--allow-archived` flag (or equivalent) on `validate-metadata.py`,
2. An update to `governance/METADATA-VALIDATION.md` documenting the
   relaxed checklist for archived skills,
3. A migration path for any skills that retired before the relaxation.

Until then, the explicit choice is: archived skills keep their full
structure; the redirect block is the user-visible change.
