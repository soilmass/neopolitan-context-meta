---
name: adr-author
description: >
  Authors a single Architecture Decision Record. Captures status,
  context, decision, and consequences plus the alternatives considered
  and the reason each was rejected. Assigns a sequential ADR number.
  Writes the artifact to docs/02-requirements/adrs/NNNN-<slug>.md
  (cross-phase work; site-build-procedure.md §5.3.6). Use after
  settling a significant architectural choice. Do NOT use for:
  authoring the full SRS (use srs-author); authoring a runbook (use
  runbook-author); authoring a vision or persona (use vision-author
  or persona-author); threat modeling (use threat-model-author once
  built; draft-threat-model covers it now); recording a scope change
  rather than an architectural choice (use the user-invocable
  draft-change-request, or change-request-author once built).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-trigger threat-model fallback aligned with
            the user-invocable peer pattern (B6/A62); "Authority
            surface" reframed as Handoff to peer; deferred
            references/template.md row dropped.
    v0.1.0 — initial. Authored via skill-author during the v0.7.0
            first-real-consumer dogfood. Modeled on the user-invocable
            draft-adr skill.
---

# adr-author

Cross-phase — record one architectural decision.

## When to Use

- A significant architectural choice has been settled (auth provider,
  database engine, framework, hosting model, observability stack,
  build-vs-buy, etc.) and needs a durable record.
- A previous ADR is being **superseded** — author a new ADR that
  links back, rather than editing the old one.
- A choice was made informally (in a meeting, in chat) and it's now
  consequential enough that the team needs the rationale captured.

## When NOT to Use

- The decision was a non-architectural product choice (which feature
  to ship next, which copy to use). ADRs are for architecture.
- The decision changes scope rather than architecture — a
  `change-request` (the user-invocable skill, or `change-request-
  author` when built) records scope changes; ADRs record the
  architecture *implementing* the new scope.
- Documenting an FR or NFR — that goes in the SRS via `srs-author`.
  ADRs *implement* SRS rows; they don't replace them.
- A trivial decision that wouldn't reverse if questioned later
  (e.g., "we use the standard library's date utilities"). Save ADRs
  for decisions that are non-trivial to reverse.
- Operational runbooks — `runbook-author`.
- Threat-model entries — `threat-model-author` (Tier 2).

## Capabilities Owned

- Assign the next sequential **ADR number** (`NNNN`) by reading the
  existing `docs/02-requirements/adrs/` directory; refuses to write
  with a colliding number.
- Capture **status** (`proposed` / `accepted` / `superseded by ADR-NNNN`
  / `deprecated`).
- Write a **context** section: the forces, constraints, and signals
  that pushed for a decision now.
- Write the **decision** itself in one paragraph plus a clear
  one-line summary that fits in the doc title.
- Enumerate **alternatives considered** — at least 2 — with the
  reason each was rejected. ADRs without alternatives are red flags;
  this atom refuses.
- Capture **consequences**: positive (what becomes possible / easier),
  negative (debt incurred, doors closed), and neutral (just true now).
- Link to PR / commit / experiment if applicable.
- Write to `docs/02-requirements/adrs/NNNN-<slug>.md` where `<slug>`
  is a kebab-case three-to-six-word summary.

## Handoffs to Other Skills

- **From `srs-author`** — when an FR/NFR implies a non-trivial
  architectural choice, srs-author hands off here.
- **To `srs-author`** — a newly-accepted ADR may add or modify NFRs;
  the SRS update happens upstream.
- **To `threat-model-author`** — when an ADR has security
  implications (e.g., "we adopt OAuth via Auth.js"), threat-model-
  author runs against the implications.
- **To sibling `adr-author` runs** — superseding ADRs link to the
  superseded number.
- **From the user-invocable `draft-adr` skill** — this atom is the
  meta-pipeline-conformant version of the same artifact.

## Edge Cases

- **Two ADRs were authored simultaneously** (concurrent PRs picking
  the same NNNN). The second to merge bumps to NNNN+1; cross-link
  the two if their topics are related.
- **The decision was made years ago** but is being recorded now for
  the first time. Author it with `status: accepted` and a context
  block that flags the historical recovery; the decision date is
  the original decision, the doc date is today.
- **The decision is provisional** (we'll revisit in 6 months). Use
  `status: proposed` with a re-evaluation date in the consequences.
- **An ADR's decision is reversed** without a successor. Use
  `status: deprecated` with a context note. Do not delete the file.

## References

No external `references/*.md` files yet (the well-known Michael
Nygard ADR format is the starting baseline; promote to a reference
on the first real authoring run). The canonical authority is
`internal://site-build-procedure.md` §5.3.6.

## Self-Audit

Before declaring an ADR complete, confirm:
- Sequential number assigned correctly (no collision).
- ≥2 alternatives with rejection rationale.
- Consequences include ≥1 negative consequence (no purely-positive
  ADRs — those signal hidden trade-offs).
- Title is a one-line decision summary that fits in a tab title.
- ADR is ≤1 page rendered.
