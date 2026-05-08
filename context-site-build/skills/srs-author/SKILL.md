---
name: srs-author
description: >
  Authors a Software Requirements Specification scaffold with
  Functional Requirements (FR) and Non-Functional Requirements (NFR).
  Each FR has ID / description / acceptance criteria / priority; each
  NFR has category / measurable target / test method. Cross-references
  vision, personas, ADRs, threat model, privacy plan when present.
  Writes docs/02-requirements/srs.md per site-build-procedure.md §5.1.
  Used at Phase 2 start, after vision and personas exist. Do NOT use
  for: writing a single architectural decision (use adr-author);
  threat modeling (use threat-model-author once built; draft-threat-
  model covers it now); privacy planning (use privacy-plan-author
  once built; draft-privacy-plan covers it now); persona work (use
  persona-author); operational runbooks (use runbook-author).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-triggers fall back to user-invocable peers
            for unbuilt skills (B6/A62); precondition "vision/personas
            don't exist yet" moved from When NOT to Use to Edge Cases;
            "Authority surface" reframed; deferred references/
            template.md row dropped.
    v0.1.0 — initial. Authored via skill-author during the v0.7.0
            first-real-consumer dogfood. Modeled on the user-invocable
            draft-srs skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# srs-author

Phase 2 — produce the project's Software Requirements Specification.

## When to Use

- Phase 2 begins; vision and ≥1 persona exist; SRS has not been
  written.
- A major scope expansion has occurred and the existing SRS no longer
  encompasses what's being built — re-author or extend rather than
  patch piecemeal.
- A team is taking over a project mid-flight and needs a consolidated
  view of what's specified.

## When NOT to Use

- Recording one architectural decision — that's `adr-author`. ADRs
  may be referenced from the SRS but they are their own artifacts.
- Doing the threat model — that's `threat-model-author` (Tier 2;
  `draft-threat-model` is the user-invocable peer).
  The SRS *references* the threat model; it doesn't replace it.
- Doing the privacy / GDPR plan — that's `privacy-plan-author`
  (Tier 2; `draft-privacy-plan` is the user-invocable peer).
- Operational runbook authoring — that's `runbook-author`. Runbooks
  follow Phase 5 / 6, not Phase 2.
- Patching one FR or NFR — edit the doc directly. This atom is for
  full scaffolding.

## Capabilities Owned

- Scaffold an SRS with two top-level sections: **Functional
  Requirements** and **Non-Functional Requirements**.
- For each **FR**: assign a stable ID (`FR-001`+), a one-paragraph
  description, **acceptance criteria** as a bulleted Given/When/Then
  list, and a priority (`MUST` / `SHOULD` / `COULD` / `WON'T`).
- For each **NFR**: name the category (perf, a11y, security, privacy,
  SEO, reliability, observability, …), a **measurable target** (e.g.,
  "LCP ≤ 2.5 s on 4G median device"), and the **test method** that
  verifies it (lab tool, RUM threshold, audit checklist, etc.).
- Cross-reference adjacent artifacts by stable ID: vision (one cite),
  personas (≥1 per FR), ADRs (when relevant), threat-model rows (per
  NFR if security), privacy plan (per NFR if privacy).
- Maintain **traceability**: every FR points to ≥1 persona; every NFR
  points to ≥1 measurable threshold or audit reference.
- Write the artifact to `docs/02-requirements/srs.md`.

## Handoffs to Other Skills

- **From `vision-author` + `persona-author`** — these are the
  upstream inputs. SRS authoring halts if either is missing.
- **To `adr-author`** — when an FR or NFR carries an architectural
  implication that warrants a standalone decision record (e.g., "FR-007
  implies adopting Auth.js"), defer to `adr-author` for the ADR.
- **To `threat-model-author`** — security NFRs hand off here for
  STRIDE coverage. The SRS row points at the threat-model row.
- **To `privacy-plan-author`** — privacy NFRs hand off here.
- **To `runbook-author`** — operational NFRs (e.g., recovery time
  objectives, alerting thresholds) hand off into the runbooks at
  Phase 5/6.

## Edge Cases

- **Vision or personas don't exist yet.** Halt; defer to
  `vision-author` and `persona-author` first. SRS authoring requires
  both as upstream inputs (precondition, not a sibling fence).
- **Acceptance criteria are unwritable for an FR** (the operator can
  describe the FR but cannot describe how it would be tested). This
  signals the FR is too vague — refine the FR before authoring its
  acceptance criteria.
- **Persona reference is impossible for an FR** (e.g., admin-only
  features that no end-user persona covers). Author or extend a
  persona for the operator role rather than skipping the persona link.
- **NFR has no measurable target** (e.g., "must be fast"). Refuse;
  the NFR is policy, not requirement. Either find a threshold or
  move it to a separate design-philosophy or communications artifact.
- **Conflicting FRs** (e.g., FR-007 and FR-012 imply different
  architectures). Halt; the resolution is an ADR via `adr-author`.

## References

No external `references/*.md` files yet. The canonical authority is
`internal://site-build-procedure.md` §5.1. The user-invocable
`draft-srs` skill is a peer producing the same artifact via a
different procedure.

## Self-Audit

Before declaring an SRS document complete, confirm:
- Every FR has acceptance criteria in Given/When/Then form.
- Every FR cites ≥1 persona by stable name.
- Every NFR has a measurable target AND a test method.
- No FR uses the word "fast", "simple", or "intuitive" without a
  measurable companion NFR.
- The SRS body fits in one document; massive SRSs split into
  per-feature appendices but the index lives at `srs.md`.
