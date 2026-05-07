---
name: dummy-connector
description: >
  Extension-seam fixture exercising the `archetype:` enumeration. Uses
  `archetype: connector` — a hypothetical 6th archetype that does not
  exist at v0.6.0. validate-metadata.py is *expected to fail*. If a
  future PR adds the connector archetype, this fixture flips to pass —
  making the seam test self-documenting. Do NOT use for: real skills
  (use one of the five canonical archetypes).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: connector
  changelog: |
    v0.1.0 — extension-seam fixture only. Per governance/EXTENSION-POINTS.md
            §4, adding a 6th archetype is OUT OF SCOPE at v0.6.0 — it would
            be a MAJOR refactor. This fixture exists to prove the seam
            holds (validator rejects the unknown archetype).
---

# dummy-connector

Fixture-only. The body content is intentionally minimal — the test is
the frontmatter `archetype:` enumeration check.

## Purpose

Prove the extension seam at `governance/EXTENSION-POINTS.md` §4 holds:
the validator rejects unknown archetypes today, and that rejection is
the gate that prevents accidental 6th-archetype introduction.

## When to Use

- Never in production. This is fixture-only.

## When NOT to Use

- Anywhere outside `scripts/tests/fixtures/extension-seams/`.

## Capabilities Owned

- Demonstrating-seam-rejection — the only "capability" exercised.

## Dependencies

- None.

## Evaluation

The fixture passes when `validate-metadata.py` exits non-zero on this
file. If validate-metadata.py exits 0, the seam has been silently
broken — either:
- A 6th archetype has been added without restructuring (bad: indicates
  the validator's archetype enumeration was extended without a MAJOR
  refactor), or
- The validator's archetype check has been removed (bad: indicates a
  regression).

## Handoffs

- N/A.

## Edge Cases

- N/A.

## Self-Audit

- N/A.
