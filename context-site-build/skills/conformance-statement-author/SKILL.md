---
name: conformance-statement-author
description: >
  Authors the WCAG 2.2 Accessibility Conformance Statement at
  Phase 5 hardening — conformance level claimed (AA), standards
  met, pages tested, methods used (automated + manual + assistive
  tech), known issues with timeline to fix, contact for
  accessibility feedback. Output at
  docs/05-hardening/a11y-conformance-statement.md (SOP §8.2.7).
  Use during Phase 5 hardening, before Gate 5. Do NOT use for:
  per-component a11y annotations on hi-fi designs (use
  a11y-annotations-author in site-design family — that is
  design-time intent; this is post-implementation conformance);
  the threat model (use threat-model-author in site-build);
  Phase 7 ongoing a11y monitoring (folds into this atom's
  re-issue at quarterly + annual cadence per SOP §10.3.6); the
  Phase 5 audit results themselves (those are operator-driven
  test outputs that this atom consumes and synthesizes).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable draft-conformance-statement skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# conformance-statement-author

Phase 5 — produce the WCAG 2.2 Accessibility Conformance Statement.

## When to Use

- Phase 5 hardening is closing; the a11y audit (automated +
  manual + assistive tech) has been run; the conformance
  statement is a Gate 5 deliverable.
- Quarterly a11y re-audit per SOP §10.3.6 — re-issue the
  conformance statement with updated test dates + any
  delta in known issues.
- Annual full a11y audit per §10.3.6 — major re-issue.
- A regulatory request (EAA, public-sector procurement)
  demands a current conformance statement; re-issue with
  the latest evidence.

## When NOT to Use

- **Per-component a11y annotations on hi-fi designs** —
  `a11y-annotations-author` (site-design family). Annotations
  are *design intent*; conformance is *post-implementation
  verification*. Annotations are upstream; conformance
  consumes them + actual audit results.
- The threat model — `threat-model-author` (site-build).
  Threat model is security; conformance is accessibility.
- Phase 7 ongoing a11y monitoring — folds into this atom's
  re-issue at quarterly + annual cadence per §10.3.6.
- The Phase 5 audit results themselves — operator-driven
  test outputs (axe DevTools / Lighthouse / Pa11y / NVDA /
  JAWS / VoiceOver / TalkBack passes). This atom *consumes*
  + synthesizes audit results into the conformance
  statement.
- Authoring fix work for known issues — that's sprint
  planning territory. The statement *documents* known
  issues + timelines; it doesn't fix them.
- VPAT (Voluntary Product Accessibility Template) — VPAT is
  a US-procurement-specific document derived from the
  conformance statement. If a VPAT is needed, author it
  separately (out of scope here unless added later).

## Capabilities Owned

- Document the **conformance level claimed** per SOP §8.2.7:
  - WCAG 2.2 AA (the project's floor per §1.4).
  - WCAG 2.2 AAA where reasonable (call out specific
    AAA criteria met).
  - **EN 301 549** for EU markets; **ATAG 2.0** for content-
    authoring tools; **Section 508** for US public sector
    (per §5.1.2).
- List **pages tested** — the key templates the audit covered
  + sample of long-tail.
- Document **methods used**:
  - **Automated** — axe DevTools, Lighthouse Accessibility,
    Pa11y CI (per §8.2.1).
  - **Manual screen reader** — NVDA + Firefox, JAWS + Chrome
    (where licensed), VoiceOver (macOS + iOS), TalkBack
    (Android) — top 5 user flows each (per §8.2.2).
  - **Keyboard-only navigation review** (per §8.2.3).
  - **Color contrast verification** at zoom + dark mode
    (per §8.2.4).
  - **Reduced motion** check (per §8.2.5).
- Document **known issues with timeline to fix** — every
  unresolved violation gets:
  - Stable issue ID.
  - WCAG criterion violated.
  - Severity (blocker / serious / moderate / minor).
  - Workaround (if any).
  - Target fix date + sprint.
- Document **contact for accessibility feedback** —
  named role + email + escalation path; SLA for response
  (typically 5 business days).
- Document **assistive technology coverage** — list
  successfully tested AT + browser combinations (per
  §8.2.2).
- Cite the **a11y annotations** + **wireframes** + **design
  tokens** by stable name (the Phase 3 design intent
  conformance verifies).
- Write to `docs/05-hardening/a11y-conformance-statement.md`.

## Handoffs to Other Skills

- **From `a11y-annotations-author`** (site-design family) —
  per-component a11y annotations are the design intent
  conformance verifies.
- **From `wireframe-author`** + **`component-states-matrix-
  author`** (site-design) — interactive states the audit
  tested.
- **From the audit operator** — axe / Lighthouse / Pa11y
  reports; manual SR + keyboard test notes; contrast
  spreadsheet.
- **To Phase 5 Gate 5** — the statement is a Gate 5
  deliverable.
- **To `optimization-backlog-author`** — known issues with
  Phase 7 fix targets land in the optimization backlog.
- **To `awards-submission-author`** (Tier 3) — the
  conformance statement is one input to the awards
  submission's a11y posture rationale.
- **From the user-invocable `draft-conformance-statement`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Audit reveals AA-blocker violations.** The statement
  cannot claim AA conformance until they're fixed.
  Surface honestly; downgrade the claim or block the gate.
- **Manual SR testing wasn't done** (only automated).
  Refuse AA claim — automated catches only ~30-40% of
  real barriers (per E3 §4.1). Either add manual testing
  or document the limited claim ("partial AA — automated
  only").
- **Site uses motion / scroll-jacking** that violates
  2.3.3, 2.5.7, 2.5.8 (new in WCAG 2.2). Surface as
  known issues with prefers-reduced-motion-respecting
  alternative paths documented.
- **Contact email isn't real** (placeholder). Refuse to
  ship; the statement is a contract with users. The
  email must be monitored.
- **Quarterly re-audit shows regression** (new violations
  not present at launch). Document explicitly + assign
  owner + target fix date; don't paper over.
- **EAA / Section 508 claim** without testing for those
  specific requirements. Refuse the claim unless the
  audit covered the additional standards explicitly.

## References

No external `references/*.md` files yet — first real
authoring run will produce a template worth promoting. The
canonical authorities are `internal://site-build-procedure.md`
§8.2.7 (conformance statement section) + §8.2 (full a11y
audit). WCAG 2.2 AA, EN 301 549, ATAG 2.0, Section 508 are
the named industry standards. The user-invocable
`draft-conformance-statement` is a peer skill producing the
same artifact via a different procedure.

## Self-Audit

Before declaring a conformance statement complete, confirm:
- Conformance level claimed is justifiable (audit covered
  the criteria for the claimed level).
- Pages tested listed (key templates + sample of long-tail).
- Methods documented (automated + manual + assistive tech +
  keyboard + contrast + reduced motion).
- Known issues each have: ID + WCAG criterion + severity +
  workaround + target fix.
- Contact for a11y feedback is real + monitored.
- Assistive technology coverage matrix listed.
- Cross-references to a11y annotations + wireframes by
  stable name.
- Statement date is current + re-issue cadence stated
  (typically quarterly + annual).
