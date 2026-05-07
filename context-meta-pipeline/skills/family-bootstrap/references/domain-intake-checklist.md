# Domain Intake Checklist

Stage 1 of `family-bootstrap`. Catches scope problems before they
become Stage 6 problems.

## The five intake questions

1. **What is the domain's bare-domain mental-model name?** This becomes
   the router's name (`git`, `postgres`, `kubectl`). Not the binary
   (`psql`, `awscli`); the user's mental model.

2. **What is the canonical authority?** A URL, a named author, and the
   work's title. "The official `git` documentation, by the Git
   maintainers, https://git-scm.com/docs". *Not* "general consensus" or
   "Stack Overflow answers."

3. **What is in scope?** One paragraph. Concrete enough that a reader
   can predict whether a given capability is covered.

4. **What is out of scope?** At least one bullet. The family's
   `coverage.md` will require a non-empty Out of Scope section in
   Stage 6 — start populating it now.

5. **What is the expected Tier 1 size?** A number 6-9. Below 6 means
   author a single atom instead of a family. Above 9 means split, or
   accept that some capabilities will be Tier 2.

## Output: domain-intake.yaml

```yaml
domain: <bare-domain-name>
authority:
  url: <https://...>
  author: <named author or maintainer>
  title: <document title>
scope:
  in: |
    <one paragraph>
  out:
    - <bullet>
    - <bullet>
expected_size: <int between 6 and 9>
adjacent_families:
  - <family that may interact>
  - ...
existing_overlap:
  - skill: <existing-skill-name>
    overlap: <one-line>
    resolution: <anti-trigger to add | rename proposed | escalate to skill-refactor>
```

## Stage 1 gate

Pass requires:

- [ ] `domain` matches the naming regex (`^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$`).
- [ ] `domain` is not already a family in **the consuming library's**
      `SNAPSHOT.lock` (audit finding A2). The meta-pipeline's own
      `SNAPSHOT.lock` is irrelevant here — domain skills are out of
      scope for the meta-pipeline; the orchestrator produces them
      *into* a separate consuming library, and that library's
      snapshot is what to check.
- [ ] `authority.url` resolves. v0.1.x–v0.2.x rely on the **operator
      to confirm** reachability (e.g., `curl --head <url>`); the
      orchestrator does not auto-fetch. If a `family-bootstrap`
      runner is built (deferred per coverage.md), the runner should
      do this automatically. Audit finding A1.
- [ ] `authority.author` is named (not blank, not "general").
- [ ] `scope.in` is one paragraph (≤500 chars; non-empty).
- [ ] `scope.out` has ≥1 entry.
- [ ] `expected_size` is between 6 and 9 inclusive.
- [ ] `existing_overlap` lists every Tier 1 skill in adjacent families
      with overlap >0.

If any of these fail, halt and re-do Stage 1. Do not proceed to Stage 2.

## Common intake failures

- **Authority is a forum thread or a chatbot transcript.** These aren't
  citable. Find the canonical docs.
- **Domain name conflicts with an existing family.** Either rename, or
  the operator is actually trying to extend the existing family — use
  `skill-author` with that family's `coverage.md`.
- **Scope is too broad.** "Everything about databases" is not a domain.
  Pick `postgres` or `mysql` or `sqlite`; the family is named for the
  tool, not the concept.
- **Out of Scope is empty.** Force at least one bullet. If the operator
  truly believes nothing is out of scope, the family's scope is too
  broad — see previous bullet.

## Why this much intake discipline

Most family-quality problems trace back to fuzzy intake. A domain that
isn't crisply defined produces atoms with overlapping responsibilities,
a router whose Routing Table competes with sibling routers, and a
`coverage.md` that can't honestly say what it doesn't cover.

The intake stage is the cheapest place to fix these problems. By
Stage 4 they require restarting; by Stage 6 they require
`skill-refactor`.
