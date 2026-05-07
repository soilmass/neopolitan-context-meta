# The Three-Way Refactor

The most important refactor pattern, from `ARCHITECTURE.md` §"Mechanism
vs Policy". When a single skill mixes mechanism (domain reality) with
policy (team conventions), the refactor produces *three* skills:

1. A **mechanism atom** (or atoms) that holds the domain reality.
2. A **tool** that orchestrates the mechanism for a workflow.
3. A **policy overlay** that captures team-specific opinions.

Three skills replacing one, each independently maintainable.

## When the three-way is right

Run the three diagnostic tests from `ARCHITECTURE.md`:

1. **Could this skill ship to another team unchanged?** If no, policy is
   embedded.
2. **Does this make sense without the underlying tool's mechanics?** If
   no, mechanism is embedded.
3. **If team conventions changed tomorrow, what would change in this
   skill?** Only the policy skill should change.

If tests 1 and 2 *both* fail (or test 3 reveals significant changes
across the whole skill), the three-way refactor applies.

## Worked example

### Before (the mixed skill)

```
git-rebase-discipline (Tool)
─ Description: "Rebase with our conventions: never on shared branches,
  always with --autosquash, fixup messages start with 'fixup!:'..."
─ Body:
  ## Stage 1 — Identify rebase target
  ## Stage 2 — Verify branch is private
  ## Stage 3 — Run rebase
  ## Stage 4 — Force-push with conventions
  ## Conventions: never on shared, always autosquash, ...
```

This skill fails:
- Test 1: another team with different conventions can't use it.
- Test 2: stripping the conventions leaves "run a rebase" — not enough
  to be useful.
- Test 3: if conventions changed, half the skill changes.

### After (three skills)

```
git-history-rewriting (Atom — mechanism)
─ Description: "Rewrites git history (rebase, amend, fixup, etc.) and
  the failure modes for each. Do NOT use for: branching strategy or
  team conventions (use house-git-conventions)."
─ Body:
  ## When to Use
  ## When NOT to Use
  ## Capabilities Owned
    - rebase
    - amend
    - fixup
    - autosquash
    - filter-repo
  ## Handoffs to Other Skills
  ## Edge Cases
  ## References
```

```
git-rebase-tool (Tool — workflow)
─ Description: "Walks through a rebase operation: identify target,
  resolve conflicts, force-push. Calls git-history-rewriting for
  mechanics. Do NOT use for: deciding branching policy (use
  house-git-conventions)."
─ Body:
  ## Purpose
  ## When to Use
  ## When NOT to Use
  ## Stage-Gated Procedure
    1. Identify target
    2. Detect conflicts (delegates to git-history-rewriting)
    3. Resolve conflicts
    4. Push (delegates to git-history-rewriting)
  ## Dependencies
    - git-history-rewriting (mechanism)
    - house-git-conventions (policy, optional)
  ## Evaluation
  ## Handoffs
```

```
house-git-conventions (Policy — overlay)
─ Description: "Overlays the team's git conventions on top of
  git-history-rewriting and git-rebase-tool: never rebase shared
  branches, always autosquash, fixup-message format. Do NOT use for:
  domain mechanics (use git-history-rewriting) or generic rebase
  workflow (use git-rebase-tool)."
─ Body:
  ## Purpose
  ## Applies On Top Of
    - git-history-rewriting
    - git-rebase-tool
  ## Conventions Enforced
    - Never rebase on shared branches.
    - Always run with --autosquash.
    - Fixup-message format: 'fixup!: <subject>'.
  ## Override Behavior
    - If invoked without git-history-rewriting installed, fail loudly.
```

Each skill independently maintainable:
- `git-history-rewriting` ships to any team unchanged.
- `git-rebase-tool` orchestrates the mechanism — also team-neutral.
- `house-git-conventions` is the team-specific overlay; another team
  can ship `acme-git-conventions` instead and use the same mechanism +
  tool.

## How `skill-refactor` orchestrates this

| Refactor Stage | Three-way action |
|---|---|
| 1 Diagnosis | Identify which sections of the source are mechanism, which are tool, which are policy. |
| 2 Plan | Map each capability/section to one of the three new skills. Compute redirects. |
| 3 Execute | Invoke `skill-author` three times: mechanism atom, tool, policy. |
| 4 Retire source | Mark source archived; redirect note names all three. |
| 5 Verification | Confirm every capability of the original is reachable through one of the three. |

## Common three-way mistakes

- **Forgetting the policy.** If you only split mechanism from tool, you
  end up with two skills that still embed the conventions. Test 3 will
  reveal this.
- **Conflating mechanism and policy in the tool.** The tool calls the
  mechanism atom; it does NOT re-explain mechanism. The tool is
  workflow-shaped, not knowledge-shaped.
- **Making the policy too thin.** If the policy overlay is one
  paragraph, it probably doesn't deserve its own skill — fold the
  rule into the tool's `## When to Use` instead.
- **Making the mechanism too broad.** The mechanism atom covers domain
  reality; if it covers two domains, split further.

## When NOT to do a three-way

- The skill is already a clean atom (passes all three diagnostic tests).
- The "policy" component is just a single best-practice mention — fold
  into the tool's body, don't extract.
- The mechanism is already covered by an existing skill — only the
  tool and policy need authoring.
- The team operating the library is *the only consumer* and will never
  ship to another team. Policy and mechanism don't need to separate
  if portability isn't a goal.

## Composition rule

Per `ARCHITECTURE.md`, the composition rule is borrowed from CSS:

> Policy *overrides or constrains* mechanism. Mechanism is the cascade
> default; policy is the override.

The mechanism skill ships unchanged across teams. Each team's policy
overlay overrides what the mechanism allows but never re-explains how
the mechanism works.
