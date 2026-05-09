---
name: awards-submission-author
description: >
  Authors the Awwwards / SOTD / Honors / SOTM / SOTY submission
  package — case-study writeup, screenshots, video walkthrough,
  jury narrative, scoring rationale per criterion (Design 40 /
  Usability 30 / Creativity 20 / Content 10 plus the six
  developer-award sub-scores). Writes to docs/06-launch/awards/<id>.md
  plus linked media. Use after launch when polish has shipped
  and the project is ready to compete. Do NOT use for: launch
  communications (use launch-comms-author Tier 1 — that is the
  customer-facing announcement; awards is jury-facing); polish
  discipline (use polish-discipline-author Tier 1 — polish is
  upstream); the diagnostic sweep (use diagnostic-sweep-author
  Tier 2); marketing case studies for sales (different audience;
  out of scope here unless the operator chooses to derive); on-
  going entry to other awards bodies (Webby, FWA, CSSDA — same
  pattern but not Awwwards-specific; can be adapted).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. No user-invocable peer
            exists for this Awwwards-tier addition; this atom
            establishes the pattern.
---

# awards-submission-author

Phase 6 / 7 — produce one Awwwards submission package.

## When to Use

- Post-launch; the polish phase has closed; the project is
  ready to compete (per Ueno's Phase 6 "Awards (optional)"
  per docs/research/E2 §C.6).
- An Awwwards Site of the Day / Honors submission is being
  prepared; the package needs the structured case-study
  writeup + media.
- A Site of the Month / Site of the Year nomination has
  triggered (project won SOTD; the SOTM nomination needs
  package augmentation).
- Adjacent awards bodies (Webby, FWA, CSSDA, Communication
  Arts Webpicks) — the pattern adapts; document the
  per-body criteria differences.

## When NOT to Use

- Launch communications — `launch-comms-author` (Tier 1).
  Launch comms is customer-facing; awards is jury-facing.
- Polish discipline — `polish-discipline-author` (Tier 1).
  Polish is upstream; without it Awwwards-tier scoring is
  unreachable.
- Diagnostic sweep — `diagnostic-sweep-author` (Tier 2).
- Marketing case studies for sales — different audience;
  the awards submission can be the seed but the marketing
  version typically softens technical depth and adds
  business-outcome storytelling.
- A submission for a project that doesn't meet
  Awwwards-tier polish criteria — refuse politely; the
  jury will score it as a reputation hit. Per E1 mean
  Animations score is 8.7/10 on winners; below that
  threshold, submission is theatre.
- Compulsive entry to every awards body — strategic
  selection per project / per audience matters.

## Capabilities Owned

- Author the **case-study writeup** per Awwwards
  submission requirements + research/E1 § (5 stack
  patterns) emblematic-winners observations:
  - **Project context** — client, timeline, team, scope.
  - **Creative thesis** — what the concept was (cite
    `concept-author`'s output).
  - **Art direction posture** — visual language summary
    (cite `art-direction-author`).
  - **Motion language** + signature interactions (cite
    `motion-language-author`).
  - **Technical highlights** — stack, asset pipeline,
    performance posture, accessibility posture.
  - **Polish phase narrative** — what 30-80% of project
    time was spent perfecting (cite
    `polish-discipline-author`).
- Curate **screenshots + media**:
  - Hero screenshot at 1440px and 375px (mobile).
  - 5-10 supporting screenshots showing key moments,
    states, scroll depth.
  - Short video walkthrough (30-90 sec) showing motion
    language in action.
  - Optional: case-study microsite link.
- Author **jury narrative** — the operator-facing prose
  about why this project deserves the award:
  - Awwwards-jury-aware framing — references emblematic
    winners + how this project differs.
  - Honest acknowledgment of trade-offs (a11y posture,
    performance vs creativity tension).
  - Per-criterion scoring rationale:
    - **Design (40%)** — visual + typography + palette
      + composition.
    - **Usability (30%)** — IA + interaction clarity +
      mobile.
    - **Creativity (20%)** — distinctive concept,
      narrative, motion, surprise.
    - **Content (10%)** — copy quality, content depth.
  - Per developer-award sub-score:
    - Animations / Transitions (the highest-leverage
      sub-score per E1 mean 8.7/10).
    - Responsive Design.
    - WPO (Web Performance Optimization) — honest about
      the WebGL-vs-CWV trade-off.
    - Semantics / SEO.
    - Accessibility — honest posture (winners cluster
      ~7.0/10; aspirational but realistic).
    - Markup / Meta-data.
- Document **submission metadata** — credits (designer /
  developer / agency), tags, category.
- Cite **launch comms** + **polish notes** + **art
  direction** + **concept** + **motion language** by
  stable name.
- Write to `docs/06-launch/awards/<id>.md` plus linked
  media in `docs/06-launch/awards/media/<id>/`.

## Handoffs to Other Skills

- **From `polish-discipline-author`** (Tier 1) — polish
  notes inform the polish-phase narrative.
- **From `art-direction-author`** + **`concept-author`**
  + **`motion-language-author`** (site-design) — the
  creative posture the case study captures.
- **From `engineering-handoff-spec-author`** (site-design)
  — technical highlights.
- **From `conformance-statement-author`** (Tier 1 here) —
  honest a11y posture.
- **From `launch-comms-author`** (Tier 1 here) — launch
  comms artefacts (announcement post, blog) inform
  framing.
- **To Awwwards submission portal** — operator submits.
- **To `quarterly-business-review-author`** + **`annual-
  retrospective-author`** — won awards become QBR /
  annual-retro highlights.
- No user-invocable peer.

## Edge Cases

- **Submission refused** (fails Honors threshold ≥6.5).
  Document the result; capture jury feedback if available;
  retro on what would change before resubmission.
- **A11y score will tank below 7.0** (failing Developer
  Award threshold). Acknowledge in the jury narrative
  rather than pretending; transparency is rewarded over
  spin.
- **Project doesn't have polish-phase notes** (ad-hoc
  polish without `polish-discipline-author`). Surface as
  a quality risk; the case-study narrative will be weaker
  without the documented polish discipline.
- **Submission requires features the project doesn't
  have** (e.g., custom cursor required for a category but
  the project deliberately didn't ship one for a11y
  reasons). Acknowledge in the jury narrative; choose the
  category honestly.
- **Operator wants to submit a project that hasn't
  polished.** Refuse the submission; per E1 the Animations
  threshold mean is 8.7/10 — un-polished projects fail
  visibly + harm the operator's submission credibility for
  future work.
- **Multiple entries for the same project** (different
  awards bodies). Author one canonical case-study; derive
  per-body submissions with body-specific criteria.

## References

No external `references/*.md` files yet — first real
authoring run will produce a template worth promoting. The
canonical authority is `internal://docs/research/
E1-awwwards-judging-and-winners.md` (Awwwards judging
weights, jury composition, recurring patterns) plus
`internal://docs/research/E2-agency-methodologies.md` §C.6
(Ueno's Phase 6 "Awards (optional)" naming the awards
phase). No user-invocable peer exists for this Awwwards-
tier addition.

## Self-Audit

Before declaring an awards submission package shipped,
confirm:
- Case-study writeup covers all 6 sections (context /
  thesis / art direction / motion / technical / polish).
- Hero screenshots at 1440px + 375px present.
- 5-10 supporting screenshots present.
- Video walkthrough 30-90 sec present.
- Jury narrative addresses all 4 Awwwards criteria + 6
  dev-award sub-scores.
- A11y posture honestly stated (not over-claimed).
- Performance posture honestly stated (CWV trade-offs
  documented).
- Cross-references to polish notes + art direction +
  concept + motion language + conformance statement.
- Submission metadata complete (credits, tags, category).
