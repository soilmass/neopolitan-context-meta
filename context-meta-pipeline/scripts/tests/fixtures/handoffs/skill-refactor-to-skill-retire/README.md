# skill-refactor → skill-retire handoff fixture

**Edge tested:** skill-refactor SKILL.md §"Stage 4 — Retire source +
redirect" delegates to skill-retire for the source skill, then the new
post-refactor siblings live alongside. The contract is: *capability
preservation* — every capability owned by the source must be owned by
exactly one of the post-refactor siblings.

The before/after pair here is contrived: `bl-monolith-tool` owns
capability-A and capability-B; the refactor produces `bl-tool-cap-a`
and `bl-tool-cap-b`. The handoff is correct when:

1. `expected-count.txt` (= 2) matches the count of post-refactor SKILL.md
   files (`after-*.md` in this dir).
2. The union of capabilities mentioned in the post-refactor When-to-Use
   sections covers every capability mentioned in the before When-to-Use
   section.

**verify.sh step 7 invocation:**
```bash
post=$(ls scripts/tests/fixtures/handoffs/skill-refactor-to-skill-retire/after-*.md 2>/dev/null | wc -l)
expected=$(cat scripts/tests/fixtures/handoffs/skill-refactor-to-skill-retire/expected-count.txt)
[[ "$post" == "$expected" ]] || exit 1
```

A capability-coverage check (the second invariant) requires more
parsing than is appropriate for verify.sh; that check is the
skill-refactor Stage 5 verification step (capability-coverage in
`refactor-verification.md`) and is exercised by skill-refactor itself,
not by this fixture.

**Why the fixture lives at the source/sibling edge:** the failure mode
this catches is a refactor that drops a capability silently because the
operator only authored one of the two intended siblings. The count check
won't catch dropped capabilities directly, but it does catch the
upstream "we forgot to author the second sibling" case.
