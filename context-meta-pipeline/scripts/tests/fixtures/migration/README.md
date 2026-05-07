# Migration-guide-gen fixture pairs

Each subdirectory is a *pair fixture* — `MODIFIED.md` (the changed
SKILL.md) plus `meta.yaml` (baseline reference) plus
`expected-fragments.txt` (markdown headings the generated guide
must contain).

verify.sh step 7 invokes
`migration-guide-gen.py --old <baseline> --new MODIFIED.md` for
each pair and greps the output for every line in
`expected-fragments.txt`. Avoids golden-file brittleness.

## Pairs

- `pair-frontmatter-rename/` — `name:` field changed (`bl-atom` → `bl-atom-renamed`)
- `pair-section-restructure/` — section removed; another added
- `pair-capability-moved/` — capability removed (atom)
- `pair-routing-changed/` — routing-table target changed (router)
- `fail-malformed-yaml.md` — invalid YAML; expected exit 2
