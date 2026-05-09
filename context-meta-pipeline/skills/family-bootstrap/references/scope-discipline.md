# Scope discipline — distinguishing in-family-deferred from out-of-scope

Surfaced by audit finding A63 (2026-05-08 first real-consumer
dogfood of `context-site-build` v0.1.x — atoms in family A
referenced siblings in family B using "(deferred)" qualifiers,
conflating two genuinely different cases).

When an atom in your family references a sibling that **doesn't
exist yet**, the operator's mental state needs to know which of
two cases applies. The vocabulary matters.

## The two cases

### Case 1 — In-family-deferred (Specced, Not Yet Built)

The sibling is **listed in this family's `taxonomy.md`** as Tier 2
or Tier 3, with a build trigger that hasn't fired. The family's
`coverage.md` has a "Specced, Not Yet Built" or "Deferred" row for
it. The atom *will* exist in this family eventually.

**Vocabulary**: `(use X-author once built)` or `(deferred Tier 3
atom)`.

**Operator action when triggered**: invoke `skill-author` to add
the atom to *this* family. The taxonomy already approved its scope.

### Case 2 — Out-of-scope (different family)

The sibling **belongs to a different family** — typically a future
family that doesn't exist yet. The atom won't ever be built in
*this* family. The family's `coverage.md` has an "Out of Scope" row
documenting where it lives instead (or will live).

**Vocabulary**: `(handled by the future <family-name> family;
user-invocable peer Y covers it now)` or
`(out of scope for this family per coverage.md)`.

**Operator action when triggered**: bootstrap the future family via
`family-bootstrap`, OR use the user-invocable peer if one exists,
OR author the atom via `skill-author` outside any family if it's a
free-standing tool.

## Why the distinction matters

Conflating the two cases produces three real failures the
context-site-build v0.1.x dogfood surfaced:

1. **Operator confusion**: "(deferred)" reads as "coming soon to this
   family" — but if the sibling is actually in a future *different*
   family, building it inside the current family creates a wrong-
   tier atom that later needs `skill-refactor` to move.

2. **Family scope erosion**: out-of-scope siblings get silently
   absorbed when their `(deferred)` framing makes them feel
   in-scope. The family's coverage.md grows beyond its honest
   bound.

3. **Missing user-invocable fallback**: the fallback path differs.
   In-family-deferred siblings will eventually have a meta-pipeline-
   conformant peer; out-of-scope siblings often have a *different*
   home (a future family OR a user-invocable peer in the operator's
   existing environment OR a stack-specific overlay). The anti-
   trigger needs to name the right home.

## Authoring guidance

When writing an atom's `When NOT to Use` block or its description's
`Do NOT use for` anti-triggers:

1. **Determine which case applies** by checking the family's
   `coverage.md`:
   - If the sibling is in `Specced, Not Yet Built` — Case 1.
   - If the sibling is in `Out of Scope` (with a "where it lives
     instead" pointer) — Case 2.
   - If the sibling is *missing* from coverage.md entirely — surface
     as a coverage-discipline gap; either add to one of the two
     sections or remove the anti-trigger reference.

2. **Use the case-appropriate vocabulary**:
   - Case 1: `(use X-author once built; user-invocable draft-X
     covers it now if applicable)`
   - Case 2: `(handled by the future <family> family; user-invocable
     peer Y covers it now)`

3. **Cross-link to the user-invocable peer** when one exists in the
   operator's environment. The `draft-*` skills are typically the
   peer skills for site-build SOP deliverables; check the operator's
   skill set for matching names.

## Examples from context-site-build v0.1.x

### Case 1 (in-family-deferred) — pattern that worked

`vision-author` Tier 1 in `site-build` family. KPI is a `Tier 2
specialist atom in the same family but not yet authored. Anti-
trigger:

> Do NOT use for: ... measurement and KPI work (use kpi-author once
> built; the user-invocable draft-kpi-doc covers it now); ...

When `kpi-author` was authored in v0.2.0, the qualifier was dropped
in a PATCH bump.

### Case 2 (out-of-scope) — pattern that worked

`runbook-author` Tier 1 in `site-build` family. Launch-comms is in
a future `site-operate` family (out-of-scope for site-build).
Anti-trigger:

> Do NOT use for: ... writing the launch communications (handled by
> the future site-operate family; the user-invocable
> draft-launch-comms covers it now); ...

When `launch-comms-author` shipped in v0.4.0 (site-operate family
bootstrap), `runbook-author`'s anti-trigger was updated in a PATCH
bump to point at the live atom.

### The anti-pattern this prevents

Before v0.1.2 self-review, several v0.1.0 atoms used `(deferred)` for
both cases indiscriminately:

> Do NOT use for: ... writing the launch communications (use
> launch-comms-author when built); ...

This reads as Case 1 (in-family-deferred), but `launch-comms-author`
was actually Case 2 (out-of-scope, future site-operate family). An
operator who tried to invoke `skill-author` to add `launch-comms-
author` to the `site-build` family would have been stopped at the
taxonomy.md gate — but only after wasted intake work.

## See also

- The family coverage.md schema lives in this skill's
  coverage-template reference (the `Specced, Not Yet Built` and
  `Out of Scope` sections).
- The anti-trigger text discipline lives in `skill-author`'s
  audit-ritual reference under "Anti-trigger fallback discipline".
- The library-root coverage.md schema (with `Domains Deferred` and
  `Domains Out of Scope` rows) lives in `library-bootstrap`'s
  library-skeleton reference.
