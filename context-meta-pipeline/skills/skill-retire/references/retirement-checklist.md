# Retirement Checklist

The Stage 4 gate fires only when this entire checklist is satisfied.
This document is the operator's reference for the lock-step PR.

## The single change set

A retirement PR contains exactly these modifications:

- [ ] `skills/<name>/SKILL.md` — frontmatter `archived: true` added;
      `metadata.changelog` prepended with retirement entry; redirect
      block prepended to body.
- [ ] `SNAPSHOT.lock` — entry for the skill removed from `skills:` (or
      moved to a `retired:` block; see snapshot format below).
- [ ] Family `coverage.md` (the family containing the retired skill) —
      atom moved from "In Scope (Tier 1)" or wherever it lived, to a
      new section titled `## Retired`.
- [ ] Library-root `coverage.md` — only updated if the retirement
      affects a domain claim (e.g., the retired skill was the last
      atom in a family — domain itself moves to "Out of Scope").
- [ ] `CHANGELOG.md` — single new entry under today's date, in
      `### Removed` or `### Deprecated` category.
- [ ] Each dependent (router, lockfile-pinning skill) — updated to
      route or pin elsewhere. May be a no-op if the only dependent
      relationship was the family's router and the redirect can stand
      in.

## SNAPSHOT.lock format for retired skills

Two acceptable patterns:

### Pattern A: removal

The retired skill is simply not listed under `skills:`. The git history
of `SNAPSHOT.lock` itself records when it was removed.

```yaml
skills:
  skill-author:
    version: "0.1.0"
    archetype: tool
    path: "skills/skill-author/SKILL.md"
    health: "fresh"
  # skill-old removed in 2026-09-01 retirement
```

### Pattern B: explicit retired block

The retired skill moves to a separate top-level key:

```yaml
skills:
  skill-author:
    version: "0.1.0"
    archetype: tool
    path: "skills/skill-author/SKILL.md"
    health: "fresh"

retired:
  skill-old:
    last_canonical: "1.4.2"
    retired: "2026-09-01"
    reason: replaced
    replacement: skill-new
    path: "skills/skill-old/SKILL.md"
```

Pattern B is preferred — it keeps retirement information first-class
and queryable. Pattern A loses information unless the operator pulls
git history.

## CHANGELOG entry format

```markdown
## <YYYY-MM-DD>

### Removed
- `<skill-name>` v<final-version> — retired (<reason>).
  - Replacement: `<replacement>` (or: none — see <pointer>)
  - Affects: <list of routers / lockfiles updated>
  - Migration: <skill-name>/MIGRATION-retire.md (if non-trivial)
```

Use `### Removed` when a replacement exists or when the absorption is
clean. Use `### Deprecated` when the retirement is health-failure-driven
and no replacement exists — the skill is *still installable* via
explicit pin, but unrecommended.

## Family coverage.md — Retired section

Add at the bottom of the family's `coverage.md`, after "Coverage Matrix
Status":

```markdown
## Retired

| Atom | Last canonical version | Retired | Reason | Replacement |
|---|---|---|---|---|
| `<atom>` | v<final> | <YYYY-MM-DD> | <reason> | `<replacement>` or "—" |
```

If the family has no retired skills yet, the section doesn't need to
exist. The first retirement creates it.

## Dependent updates

For each dependent identified in Stage 2:

### If the dependent is a router

- Update its `## Routing Table`: replace the entry pointing at the
  retired skill with one pointing at the replacement. If no replacement
  exists, remove the row and add an anti-trigger to the router's
  description for the routing intent.
- Bump the router's `metadata.version` (typically MAJOR — a routing
  table change is usually breaking).
- Add to its `metadata.changelog`.

### If the dependent has a lockfile pin

- Update the pin to point at the replacement at its current version.
- If no replacement exists and the dependent genuinely needed the
  retired skill, the dependent is now broken — escalate to retiring
  the dependent, or to writing a new skill that fills the gap.

### If a `coverage.md` cross-references the retired skill

- Replace the cross-reference with the redirect pointer.

## Verification (post-Stage-4)

- [ ] `git status` shows exactly the files in this checklist (no
      stray modifications).
- [ ] `validate-metadata.py --all` exits 0 (the archived skill still
      passes; warnings ok).
- [ ] `git checkout <pre-retire-ref> -- skills/<name>/` restores the
      pre-retirement content cleanly. Pinning works.
- [ ] No router dispatches to the retired skill in its current
      `## Routing Table`.
- [ ] `SNAPSHOT.lock` `skills:` does not list the retired skill (it's
      under `retired:` if Pattern B is used).
- [ ] Library `CHANGELOG.md` has the new entry under today's date.

## What this checklist does NOT cover

- The decision to retire. Upstream — `skill-audit` flags, `skill-refactor`
  decides, the operator confirms.
- Communication to external users. v0.1.0 has no external users; when
  the deferred `DEPRECATION-COMMUNICATION.md` is authored (per
  `governance/INDEX.md`), this checklist will gain a "notify external
  consumers" item.
- Forensics on why the retirement was needed. That's a `skill-audit`
  artifact (its synthesis report), not a retirement artifact.
