# router-disambiguation.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

How the `meta` router resolves ambiguous prompts. The router's body has a
short Disambiguation Protocol; this reference fleshes out the discipline
for consumer libraries authoring their own routers.

## When the router fires

Per `meta/SKILL.md`:
- when a prompt could plausibly route to ≥2 of the cluster's atoms, AND
- when no atom's anti-trigger explicitly excludes the prompt

If the prompt clearly matches one atom (description-overlap is dominant),
the routing layer dispatches directly — `meta` doesn't fire. If the prompt
matches *no* atoms, the routing layer surfaces "no skill matches" — also
not `meta`'s job.

## The disambiguation protocol

Three steps:

1. **List the candidate atoms.** From the routing-table entries that
   plausibly match the prompt.
2. **Surface the discriminating axis.** What information would the
   operator need to provide to choose between candidates? (e.g., "are
   you authoring a new skill, or modifying one that exists?")
3. **Ask one question.** Single-question disambiguation is the
   discipline. Multi-step interviews fall back to operator-driven
   decision-making rather than routing.

## Author conventions for routers

When authoring a per-cluster router (consumer libraries do this when their
cluster reaches 5+ atoms):

- The router's `## Disambiguation Protocol` section is required.
- The protocol must terminate in ≤3 questions for any reasonable prompt.
- The protocol must NOT delegate further routing to a sub-router (no
  recursive routing without explicit cross-cluster meta-router approval —
  the cross-cluster pattern is deferred per `ARCHITECTURE.md`).

## Anti-patterns

- **Router decides without asking** — defeats the purpose. If the router
  could decide, the routing layer's description-overlap should have
  decided.
- **Router delegates to operator without surfacing the axis** — "what do
  you want to do?" is not a disambiguation question.
- **Router handles >7 atoms** — the cluster is too big; split into
  sub-clusters and add a cross-cluster meta-router (deferred at v0.7.0).

## Static routing de-rank (v0.5.2 fix)

`routing-eval-runner.py:static_routing()` de-ranks `archetype: router`
skills by 0.7×. The reason: a router's description necessarily lists every
atom name in its routing table, so a prompt that matches one atom strongly
also matches the router strongly. The de-rank ensures the static heuristic
prefers a tied atom over a tied router.

This is a *static-mode-only* convention. The real LLM-routing layer
(deferred per `governance/SKILL-DISCOVERABILITY.md`) doesn't need it; the
LLM understands semantic intent.

## Cross-cluster meta-router (deferred)

When ≥5 clusters exist (i.e., ≥5 family routers), a cross-cluster
meta-router becomes useful. v0.7.0 doesn't have any cross-cluster routers
because the meta-pipeline is a single cluster. Consumer libraries with
multi-cluster surfaces will need to author one when the trigger fires.
