---
name: persona-author
description: >
  Authors an evidence-backed persona document for one audience
  segment. Synthesizes interview, survey, and analytics evidence into
  a persona with jobs-to-be-done, pain points, and distinguishing
  characteristics from sibling personas. Writes the artifact to
  docs/01-discovery/personas/<name>.md (site-build-procedure.md
  §4.2.3). Use after the project vision has been authored. Do NOT
  use for: authoring the project vision (use vision-author);
  authoring measurable success metrics (use kpi-author once built;
  draft-kpi-doc covers it now); mapping opportunities downstream of
  personas (use ost-author once built; draft-ost covers it now);
  authoring stakeholder RACI (use stakeholder-map-author once built;
  draft-stakeholder-map covers it now); authoring the SRS (use
  srs-author).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-triggers fall back to user-invocable peers
            for unbuilt skills (B6/A62); "Authority surface" reframed
            as "Sibling skill in operator environment"; deferred
            references/template.md row dropped.
    v0.1.0 — initial. Authored via skill-author during the v0.7.0
            first-real-consumer dogfood. Modeled on the user-invocable
            draft-persona skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# persona-author

Phase 1 — produce one evidence-backed persona document.

## When to Use

- New project in Phase 1; user research has produced raw evidence
  (interview notes, survey responses, analytics segments) and a
  persona needs synthesizing.
- Adding a new persona to an existing persona set when the project
  expands to a new audience segment.
- A claimed persona has gone stale (re-research has produced new
  evidence) and the persona document needs re-authoring against the
  fresh evidence.

## When NOT to Use

- The project's vision is undefined — `vision-author` first.
- Defining measurable success metrics for the persona — that's
  `kpi-author` (Tier 2).
- Mapping persona pains to product opportunities — that's
  `ost-author` (Tier 3) and downstream of this atom.
- Authoring a stakeholder map (project sponsors, decision-makers) —
  that's `stakeholder-map-author` (Tier 3); stakeholders are not
  personas.
- A persona built only on demographics with no jobs-to-be-done — this
  atom refuses; demographic-only personas are vibe-personas.
- Patching an existing persona after a small wording change — edit
  the doc directly.

## Capabilities Owned

- Synthesize one persona from **named evidence sources** (interview
  IDs, survey IDs, analytics segment IDs). Refuses to author without
  cited evidence.
- Capture the persona's **jobs-to-be-done** (situation × motivation
  × desired outcome) with one or more JTBD per persona.
- Capture **pain points** with the current alternative (status-quo
  product, manual workflow, competitor).
- Note the persona's **distinguishing characteristic** vs sibling
  personas already authored — what specifically differs (not just
  job title or demographic).
- Identify the persona's **proxy KPI hint** — one observable signal
  that would tell us the persona is being served (handed off to
  `kpi-author` for formalization).
- Write the artifact to `docs/01-discovery/personas/<name>.md`,
  where `<name>` is the persona's stable handle (e.g., `clara-cmo`).

## Handoffs to Other Skills

- **From `vision-author`** — vision authoring may halt with "personas
  needed"; this atom resolves that.
- **To `kpi-author`** — proxy-KPI hints handed off here become
  measurable thresholds.
- **To `ost-author`** (when authored) — persona pains feed
  opportunities in the OST.
- **To `srs-author`** — every functional requirement should reference
  ≥1 persona by name; this atom's output is one such named persona.
- **To sibling `persona-author` runs** — distinguishing-characteristic
  bullets cross-reference siblings, so the second run reads the first.

## Edge Cases

- **Insufficient evidence** (one interview, no analytics). Halt;
  this atom refuses to fabricate. The operator either gathers more
  evidence or uses a `provisional persona` template — but provisional
  personas are out of scope for this atom.
- **Persona overlaps with an existing one** (e.g., two CMOs with
  similar jobs). Halt; either merge into one persona with two named
  variants, or sharpen distinguishing characteristics until they're
  meaningfully different.
- **Anti-persona** (a non-target user the project explicitly does not
  serve). This atom can author them; mark with `## Status: Anti-Persona`
  and ensure they appear in the vision's out-of-scope statement.
- **Persona is a B2B buyer + end-user simultaneously** (common in
  SMB tools). Author as one persona with named role-modes — do not
  split into two.

## References

No external `references/*.md` files yet. The canonical authority is
`internal://site-build-procedure.md` §4.2.3. The user-invocable
`draft-persona` skill is a peer producing the same artifact via a
different procedure.

## Self-Audit

Before declaring a persona document complete, confirm:
- ≥1 cited evidence source per persona claim (no uncited assertions).
- ≥1 named job-to-be-done with situation × motivation × outcome.
- Distinguishing characteristic vs sibling personas (when ≥1 exists).
- Proxy-KPI hint present, ready for `kpi-author` to formalize.
- Doc is ≤2 pages rendered (~1000 words proxy).
