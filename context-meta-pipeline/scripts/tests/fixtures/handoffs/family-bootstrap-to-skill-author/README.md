# family-bootstrap → skill-author handoff fixture

**Edge tested:** family-bootstrap SKILL.md §"Stage 4 — Atom authoring
(delegated)" — for each Tier 1 atom in the family taxonomy, the
orchestrator invokes `skill-author` Stage 1 with a pre-filled
`intake.yaml`. The contract is: *N atoms in the taxonomy ↔ N
skill-author invocations*.

**Test:** count records under `atoms:` in `intake.yaml`, compare to
the integer in `expected-count.txt`. They must match. Failure means
the orchestrator could over- or under-invoke skill-author.

**verify.sh step 7 invocation:**
```bash
n=$(python3 -c '
import yaml, sys
data = yaml.safe_load(open("scripts/tests/fixtures/handoffs/family-bootstrap-to-skill-author/intake.yaml"))
print(len(data["atoms"]))')
expected=$(cat scripts/tests/fixtures/handoffs/family-bootstrap-to-skill-author/expected-count.txt)
[[ "$n" == "$expected" ]] || exit 1
```

**Why the fixture lives at the orchestrator/atom edge:** this is the
single most-load-bearing handoff in the library. Every new family
authored by a consumer will exercise it 4-7 times (Tier 1 atom count).
A drift between orchestrator iteration and skill-author Stage 1
expectation is the kind of bug that lands silently and shows up as
"the second atom got skipped" in someone else's library months later.
