---
name: family-bootstrap
description: >
  Orchestrates the creation of a complete domain family — router plus
  Tier 1 atoms plus a per-family coverage.md — through six gated stages:
  domain intake, capability indexing, taxonomy design, per-skill authoring,
  weaving, and coverage & registration. Delegates to skill-author for each
  Tier 1 atom. Do NOT use for: authoring a single skill (use skill-author);
  scaffolding an entire new library (use library-bootstrap — handles the
  layer above family-bootstrap); composing an orchestrator across two
  families (use cross-domain-orchestrator-author); composing across two
  libraries (use cross-library-orchestrator); splitting an existing skill
  (use skill-refactor); running health checks (use skill-audit / library-audit);
  archiving skills (use skill-retire).
license: Apache-2.0
metadata:
  version: "0.2.5"
  archetype: orchestrator
  tags: [composition, rare]
  recency_pin: stable
  changelog: |
    v0.2.5 — patch: Stage 4 procedure prose clarifies that routers'
            Routing Tables list only built atoms; deferred Tier 2/3
            atoms appear in the "Atoms in This Family" section only
            (audit finding A64 from context-site-build first-real-
            consumer dogfood). Added new reference doc
            `references/scope-discipline.md` distinguishing
            in-family-deferred (Specced, Not Yet Built) from
            out-of-scope (handled by future or different family)
            (audit finding A63).
    v0.2.4 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.2.3 — patch: metadata.recency_pin: stable declared (v0.6.2 wiring).
    v0.2.2 — patch: description anti-triggers extended (A24/A25 from v0.5.2
            dogfood) — `Do NOT use for` block now names library-bootstrap
            (the layer above family-bootstrap), cross-domain-orchestrator-author
            (across two families), cross-library-orchestrator (across two
            libraries), and skill-audit/library-audit (health checks). Prevents
            static-routing contention against the v0.5.0 composition cluster.
    v0.2.1 — patch: applied the remaining 18 dogfood audit findings.
            Stage 3 gate now enforces all-tier size caps (A6/A7).
            Stage 5 reworded "per-atom dependency declarations" to flag
            it as rare-for-atoms (A15); added connectedness recommendation
            for cross-handoffs (A17); added router-routing-table
            cross-check (A14); added cross-reference to
            audit-ritual.md's ephemeral-artifact note (A18). Stage 6
            now states explicitly that the new family lands in a
            *consuming library*, not the meta-pipeline itself (A20).
            Coordinated with reference updates (A1/A2/A3/A4/A5/A8/A9/A12).
    v0.2.0 — minor: Stage 6 gate now has three checks (structural validation,
            coverage discipline, advisory health audit via audit-skill.py).
            Stage 4 now spells out the intake.yaml schema the orchestrator
            pre-fills per atom and points operators to skill-author Stage 2's
            "when delegated from family-bootstrap" note. Surfaced by the
            v0.4.0 dogfood (8 of 9 freshly-bootstrapped skills failed the
            drift gate immediately under the prior procedure — audit
            finding A19).
    v0.1.1 — patch: Stage 5 now specifies what "audit ritual across the whole
            family" means concretely (N invocations of the per-skill ritual
            with cross-family sibling pool, batched anti-trigger updates).
            Lockfile terminology unified — per-atom dependencies are
            recorded as `depends_on:` in `SNAPSHOT.lock`.
    v0.1.0 — initial. Authored via skill-author 4-stage procedure.
---

# family-bootstrap

The lifecycle skill that scaffolds a brand-new domain family. Replaces the
conceptual `docs-to-skill-family` from earlier drafts of the architecture.

## Purpose

Produce a working skill family from a documented domain:

- A router named for the bare domain (`git`, `kubectl`, `postgres`).
- A Tier 1 set of atoms (typically 6-9), each authored via `skill-author`.
- A `taxonomy.md` documenting the tier split.
- A per-family `coverage.md` with all six required sections (per
  `ARCHITECTURE.md` §"Coverage Discipline").
- An updated library-root `coverage.md` claiming the new domain.
- An updated `SNAPSHOT.lock` and `CHANGELOG.md`.

The output is a family that passes `validate-metadata.py --all` cleanly
and is invokable as soon as the plugin reloads.

## When to Use

- The operator names a new domain to bring under the library (e.g., "we
  need a `git` family", "let's add `postgres`").
- The operator points at authority docs (URL + named author + work title)
  and wants a family scaffolded against them.
- A domain claimed in the library-root `coverage.md` needs to move from
  "Deferred" to "In Scope".

## When NOT to Use

- For a *single* skill that doesn't form a family — use `skill-author`
  directly. A family without a router and at least three atoms is just
  a skill.
- For adding *one more atom* to a family that already exists — use
  `skill-author` directly with the family's `coverage.md` updated.
- For refactoring an existing family — use `skill-refactor` per skill,
  or hand-author the family's restructure against `coverage.md`.
- For library-root coverage updates that span multiple families — those
  are hand-authored.

## The Stages

Six heavyweight stages. Each stage produces a named intermediate artifact
the next consumes. Templates live in the references.

### Stage 1 — Domain intake

**Consumes:** the operator's prompt and the named authority documents
(URL + author + work title).

**Produces:** `domain-intake.yaml` containing
- `domain` (bare-domain mental-model name; will become the router's name)
- `authority` (URL, author, title — citable)
- `scope` (one-paragraph statement of what the family will and will not
  cover)
- `expected_size` (anticipated Tier 1 count; sanity-checks against Stage 3)

**Gate:** authority cites a URL AND a named author (no "general consensus"
sources). The domain name passes the naming regex (and is *not* already
taken in the library).

See `references/domain-intake-checklist.md`.

### Stage 2 — Capability indexing

**Consumes:** the authority corpus from Stage 1.

**Produces:** `capabilities.json`: a flat list of domain capabilities
lifted from the authority. Each entry has:
- `name` (provisional, lifted from the authority's vocabulary)
- `description` (one sentence, paraphrased from the authority)
- `citation` (section / page / heading in the authority)

**Gate:** ≥10 capabilities indexed. Every entry cites a specific
location in the authority — no synthesized capabilities.

### Stage 3 — Taxonomy design (tiered)

**Consumes:** `capabilities.json`.

**Produces:** `taxonomy.md` with three tiered groups (per
`ARCHITECTURE.md` §"The Tier Model"):
- **Tier 1 (essential)** — 6-9 atoms. Every user touches these regularly.
- **Tier 2 (encompassing)** — 4-7 atoms. Specialist needs. Specced but
  not built; folded into Tier 1 with the split flagged in `coverage.md`.
- **Tier 3 (advanced)** — 2-5 atoms. Long tail. Documented as deferred
  with **observable build triggers** (not "build when needed").

See `references/tier-model.md` for the full discipline.

**Gate:** every capability from `capabilities.json` lands in exactly one
tier. Every Tier 3 entry has an observable build trigger. **All three
tier sizes are within their declared caps**:
- Tier 1: 6–9 atoms (smaller → author a single skill via `skill-author`
  instead; larger → either narrow scope or split into two families).
- Tier 2: 4–7 atoms (smaller is fine if there's genuinely little
  encompassing complexity; larger means the family's scope is too broad
  and Tier 1 is hiding capabilities that belong on the surface).
- Tier 3: 2–5 atoms (smaller is fine for self-contained domains;
  larger means the long-tail is bloated and the operator should
  collapse triggers or move some to Out of Scope).

The Tier 2/3 caps were declared in `references/tier-model.md` from
v0.1.0 but only enforced at the gate from v0.2.1 onward (per audit
findings A6/A7 from the v0.4.0 family-bootstrap dogfood). A taxonomy
that authored under the old gate-rules and exceeds the Tier 2/3 caps
should narrow scope before re-entering the gate.

### Stage 4 — Per-skill authoring

**Consumes:** the Tier 1 rows from `taxonomy.md`.

**Produces:** one SKILL.md per Tier 1 atom, plus the family's router
SKILL.md.

For each Tier 1 atom: invoke `skill-author` with a pre-filled
`intake.yaml` derived from the taxonomy row:

```yaml
archetype: atom
name: <domain>-<scope>            # the row's name from taxonomy.md Tier 1
purpose: <one-line from row>      # the row's "Capabilities (one-line)"
family: <domain>                  # from domain-intake.yaml
siblings:                         # every OTHER Tier 1 atom in the family
  - <domain>-<scope-2>
  - <domain>-<scope-3>
  - …
```

`skill-author` walks its own 4 stages; this orchestrator's Stage 4
doesn't pass until each delegated `skill-author` call passes its own
Stage 4 gate. **Note**: the per-atom `skill-author` Stage 2 (ecosystem
audit) defers to this orchestrator's Stage 5 (family-wide audit ritual)
during family-bootstrap delegation — the operator does not run two
separate audits per atom. See `skill-author` SKILL.md Stage 2 for the
"When invoked from family-bootstrap" note.

The router is hand-authored as a separate `skill-author` call with
archetype=`router`. **The Routing Table lists only Tier 1 atoms that
are actually built** — never deferred Tier 2/3 atoms or specced-but-
not-yet-authored entries. The `## Atoms in This Family` section is
the place specced atoms appear (organized by tier with explicit
"Tier 2 (Specced, Not Yet Built)" / "Tier 3 (Deferred)" headers per
the family's `taxonomy.md`).

This split was added in v0.2.5 per audit finding A64. The
context-site-build v0.1.0 router shipped with 10 of 16 Routing Table
rows pointing at unbuilt Tier 2/3 atoms — pollutes routing-eval
signal because the LLM router treats every row as a real target
and routes prompts to dead ends. v0.1.2 dropped the deferred rows
from the table; the convention is now codified here.

When Tier 2/3 atoms get authored later (via `skill-author` directly,
not another `family-bootstrap` run), the router's Routing Table is
extended at PATCH bump time to include them. The "Atoms in This
Family" section gets the matching tier-header line removed.

**Gate:** every delegated `skill-author` invocation passed. Router has
all required sections (Routing Table, Disambiguation Protocol, Atoms in
This Family). Routing Table lists only built atoms (per A64).

### Stage 5 — Weaving

**Consumes:** the atoms and router produced in Stage 4.

**Produces:**
- Cross-handoffs: every atom names ≥1 sibling in its `Handoffs to Other
  Skills` section.
- Anti-triggers: cross-referenced between siblings via the audit ritual
  (per `skill-author` references/audit-ritual.md), now run across the
  whole family at once. Concretely: invoke the per-skill ritual once
  per Tier 1 atom *and* once for the router, with the "top three
  siblings" pool spanning every other atom in the family plus the
  router. Anti-trigger updates queued during these N invocations are
  applied in a single batch at the end of the stage so that no atom
  ships with a stale anti-trigger pointing at a not-yet-existing
  sibling.
- Per-skill dependency declarations *(rare for atoms; common for
  orchestrators and tools)*: any atom that calls another skill
  programmatically — typically only in mechanism-tool-policy
  three-way refactor results, not in plain bootstrapped atoms — is
  recorded in `SNAPSHOT.lock` under that atom's `depends_on:` entry
  (e.g., `<sibling>@<version>`). For most freshly-bootstrapped
  families, this set is empty: atoms hand off via prose
  (`## Handoffs to Other Skills`), not via lockfile pins. The Stage 6
  snapshot write applies whatever pins this stage produced. (See
  `GOVERNANCE.md` §"Dependency Model" for why `SNAPSHOT.lock`
  `depends_on:` is the canonical mechanism rather than a separate
  per-atom lockfile.) Audit finding A15.

**Gate:** four checks, all must pass:

1. **Routing table coverage**: every entry in the router's
   `## Routing Table` resolves to a real atom in the family
   (`skills/<domain>-<atom>/SKILL.md` exists). The new
   `validate-metadata.py` router-atom-resolves check (v0.4.0+,
   audit finding A21) catches this for the `## Atoms in This Family`
   section but currently does NOT cross-check the routing table
   itself; the operator verifies manually. Cross-check that every
   Tier 1 atom from `coverage.md` "In Scope" appears in the
   router's Routing Table — this is the inverse direction
   (audit finding A14).
2. **Cross-handoff coverage**: every atom names ≥1 sibling in
   `## Handoffs to Other Skills`. *Strong recommendation* (not a
   blocking gate): the family hand-off graph is connected — every
   pair of atoms is reachable from every other via Handoffs. A
   single isolated atom is a refactor signal even if the gate
   technically passes (audit finding A17).
3. **Audit ritual completed**: the per-atom + router audit-ritual
   runs produced no orphan contentions. The ritual artifacts
   (`audit-report.md` per atom + router) are **ephemeral**, not
   committed — the persistent outputs are the anti-trigger updates
   applied to descriptions in batch (per
   `skill-author/references/audit-ritual.md`'s "Note on the
   audit-report.md artifact"; audit finding A18).
4. **Snapshot dependency declarations**: any `depends_on:` entries
   produced are well-formed (`<skill>@<version>` per
   `GOVERNANCE.md`). Empty set is normal for atom families.

### Stage 6 — Coverage & registration

**Consumes:** the woven family from Stage 5.

**Where does the new family land?** The meta-pipeline (this plugin)
produces families *into a consuming library*, not into itself. Per
the meta-pipeline's own `coverage.md`, "domain skills themselves are
out of scope for this plugin". The consuming library is wherever the
operator runs the orchestrator from — typically a sibling plugin
(e.g., `context-git/`, `context-postgres/`) with its own
`SNAPSHOT.lock`, `coverage.md`, and `CHANGELOG.md`. References to
"the snapshot" / "coverage.md" / "CHANGELOG.md" below are the
*consuming library's*, not the meta-pipeline's. Audit finding A20.

**Produces:**
- Per-family `coverage.md` at `skills/<domain>/coverage.md` *in the
  consuming library* with all six sections from
  `references/coverage-template.md`. The "Out of Scope" section
  must have at least one entry — silent gaps are the failure mode
  this enforces.
- A new row in the *consuming library's* root-level `coverage.md`
  under "Domains Claimed" pointing at the family's `coverage.md`.
- A new entry per atom in the *consuming library's* `SNAPSHOT.lock`
  with archetype/path/health.
- A new entry in the *consuming library's* `CHANGELOG.md` under
  "Added" listing the router and every Tier 1 atom.

**Gate:** Three checks run together, in this order:

1. **Structural validation.** `validate-metadata.py --all` passes
   against every new SKILL.md in the family.
2. **Coverage discipline.** `coverage.md` has all six sections;
   "Out of Scope" non-empty; the library-root `coverage.md` row
   resolves to the new family's coverage.md.
3. **Health audit (advisory).** `audit-skill.py --all --root <family-root>`
   produces a rollup. Recency gate is expected to pass (everything was
   just authored). Drift gate failures are common on fresh families
   where descriptions were authored quickly — the operator iterates
   on flagged descriptions until drift falls below 10% before
   declaring the bootstrap complete. This check is advisory only
   (does not hard-block bootstrap), but a family that ships with
   drift-flagged skills will surface as "Health" entries on the next
   skill-audit run, which is the lock-step coordination point with
   `MAINTENANCE.md`.

**Why audit-skill at Stage 6:** the dogfood run that authored this
v0.2.0 of family-bootstrap discovered that 8 of 9 freshly-bootstrapped
skills failed the drift gate immediately (descriptions over-promised
relative to body content). Without the audit at Stage 6, the operator
finds out only on the next periodic skill-audit cycle — by which
point the family has shipped to consumers.

## Skills Coordinated

- **`skill-author`** — invoked once per Tier 1 atom in Stage 4, plus
  once for the router.
- **`scripts/validate-metadata.py`** — invoked at the Stage 6 first
  gate-check (structural validation) against every produced SKILL.md.
- **`scripts/audit-skill.py`** — invoked at the Stage 6 third
  gate-check (advisory health audit). v0.2.0+: mechanizes Gates 1
  (recency) and 4 (description drift) per `skill-audit/references/health-gates.md`.

## Failure Modes

- **Authority is unreliable** (Stage 1 gate fails). Halt; the operator
  finds a citable authority or escalates the domain to "Out of scope" in
  library-root `coverage.md`.
- **Capability count below 10** (Stage 2 gate fails). The domain is too
  narrow for a family — author a single atom via `skill-author` instead.
- **Taxonomy can't fit Tier 1 into 6-9 atoms** (Stage 3 gate fails).
  Reconsider the scope. Either narrow it (move some capabilities to
  out-of-scope) or split the family in two.
- **A delegated `skill-author` fails** (Stage 4). The whole orchestrator
  halts; the operator fixes that atom and re-invokes from Stage 4 for
  the failed atom only.
- **Audit ritual finds a sibling-router contention** (Stage 5). Add
  anti-triggers; if contention persists across two iterations, escalate
  to `skill-refactor` to redraw the family boundary.
- **`validate-metadata.py` fails on any atom** (Stage 6). Halt; fix the
  failing atom (typically a missing required section); re-run Stage 6.

## Handoffs

- **To `skill-author`** at Stage 4 — heavily, once per atom.
- **To `skill-audit`** — the produced family is in scope for the next
  audit run.
- **To routers in adjacent domains** — if the new family's anti-triggers
  affect routing in adjacent domains, those routers are updated lock-step.
- **From the operator** — the operator manually updates
  `~/.claude/settings.json` if the new family's router needs to be
  enabled separately.

## Edge Cases

- **The domain has its own router-style entry point** (e.g., `git` —
  the binary is itself a router over subcommands). The family's router
  SKILL.md mirrors that structure: routing table maps subcommands /
  failure modes to atoms.
- **The authority disagrees with itself** (multiple sources, conflicting
  vocabulary). Pick one canonical authority; cite the others in the
  family's `coverage.md` "Out of Scope" with a pointer.
- **Two atoms cover overlapping capabilities.** Stage 5 weaving catches
  this — collapse the atoms or sharpen the boundary in Stage 3.
- **A Tier 1 atom turns out to be too large** during Stage 4 (skill-author
  Stage 3 produces a body >500 lines that won't push detail to references
  cleanly). Halt; split the atom in two by going back to Stage 3 of this
  orchestrator and re-tiering.

## Self-Audit

Before invoking this orchestrator on a new domain, confirm:
- `SNAPSHOT.lock` is current (run `skill-audit` if uncertain).
- The library-root `coverage.md` has the target domain in "Deferred"
  (otherwise add it before starting).
- No existing family already claims overlapping capabilities (run the
  audit ritual against the proposed router's description first).
