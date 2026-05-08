# Governance Index — context-site-build

This library inherits the meta-pipeline's three load-bearing
governance docs by reference. Authoring local versions is
unnecessary; the meta-pipeline is the canonical source.

## Currently Documented

(inherited from `../context-meta-pipeline/`)

| Doc | Path | Authority |
|---|---|---|
| Metadata validation rules | `../context-meta-pipeline/governance/METADATA-VALIDATION.md` | load-bearing |
| Breaking-change detection | `../context-meta-pipeline/governance/BREAKING-CHANGE-DETECTION.md` | load-bearing |
| Rollback procedure | `../context-meta-pipeline/governance/ROLLBACK-PROCEDURE.md` | load-bearing |
| Extension points | `../context-meta-pipeline/governance/EXTENSION-POINTS.md` | reference |

The seven optional governance docs (integration testing,
discoverability, provenance, security audit, emergency hotfix,
deprecation communication, usage analytics) are inherited from the
meta-pipeline as-is. v0.7.0 of the meta-pipeline ships pre-trigger
mechanizers for four of them; this library benefits transitively.

## Deferred

(inherited; first build trigger to fire on this library will be
the trigger for the relevant deferred doc)

## Local-only governance

None at v0.1.0. If this library accumulates conventions that
diverge from the meta-pipeline (e.g., site-build–specific banner
templates, phase-aware audit cadences), they will live under
`governance/local/` to avoid namespace collision with the
meta-pipeline's docs.
