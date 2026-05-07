# migration-checklist.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library
> (specifically: when the first MAJOR bump on any meta-pipeline skill ships).

What every `MIGRATION-v<N>.md` file must contain. `skill-migrate` Stage 3
adds these sections to the auto-generated structural diff from Stage 2.

## Required sections

Per `governance/VERSIONING-POLICY.md` §"Migration Guides" + this skill's
Stage 3:

1. **Why this change** — one paragraph rationale. What problem does the
   MAJOR bump solve? Why couldn't it have been a MINOR? Operator-facing
   prose, not internal "we needed to refactor."
2. **What changed structurally** — the auto-generated content from Stage
   2's `migration-guide-gen.py` output. Frontmatter / Capability / Routing /
   Section change tables.
3. **Worked examples** — at least one before-and-after code or prompt
   snippet showing user-visible impact.
4. **Known incompatibilities** — anything not captured by the structural
   diff (behavioral changes, performance shifts, output-format drifts).
5. **Suggested timeline** — for users who want to delay. Per
   `GOVERNANCE.md`'s latest-only support model, delaying means pinning to
   the prior version; document how.

## Optional sections (operator judgment)

- **Rollback procedure** — only if the migration includes irreversible
  operations (rare for SKILL.md changes; common for data migrations).
- **Tooling support** — link to any helper scripts that automate parts
  of the migration on the user's side.
- **Acknowledgments** — credit reviewers or external contributors.

## Stage 3 author checklist

Before passing the Stage 3 gate ("every section has substantive content"),
walk this list:

- [ ] Why-this-change paragraph names the problem in user terms (not
  internal team terms)
- [ ] Each capability change has a before-snippet AND after-snippet
- [ ] Routing changes (for routers) include the old and new dispatch
  decision in plain language
- [ ] Worked example is *minimum* viable (not a full feature demo)
- [ ] Known incompatibilities lists at least one item, even if it's
  "no behavioral changes beyond the structural diff" (forces you to
  consider non-structural drifts)
- [ ] Suggested timeline gives a concrete date (or "as soon as you can
  re-validate" if no calendar concerns apply)

## Stage 4 ship checklist

Before passing the Stage 4 gate (`detect-breaking-changes.py` exit 2):

- [ ] `MIGRATION-v<NEW>.md` exists at `<skill-dir>/MIGRATION-v<NEW>.md`
- [ ] Skill's `metadata.changelog` references the migration guide path
- [ ] Library `CHANGELOG.md` `[<release>]` Breaking section references
  the same path
- [ ] Round-trip: `detect-breaking-changes.py` exits 2 (breaking detected
  with proper handling), not 1 (breaking detected without handling)

## Anti-patterns

These are the failure modes Stage 3 catches:

- **All-empty migration guide** — every section is template prose with
  no specifics. Per the v0.5.2 A26 fix, Stage 2 halts before reaching
  Stage 3 if the structural diff is empty (suggesting the bump shouldn't
  be MAJOR).
- **Internal-team prose** — "we needed to refactor for cleanliness" is
  not a user-facing reason. Rewrite to: "we corrected an output-format
  ambiguity that broke X downstream consumer".
- **No worked examples** — abstract description without code or prompts.
  Every section after Why-this-change must include at least one concrete
  artifact.
