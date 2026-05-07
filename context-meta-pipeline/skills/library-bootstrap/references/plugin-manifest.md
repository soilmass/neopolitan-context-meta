# plugin.json schema reference

`library-bootstrap` Stage 2 produces `<root>/.claude-plugin/plugin.json`.
The schema is owned by Claude Code (per `coverage.md` Domains Out of
Scope: "Plugin packaging mechanics"); this reference documents the
fields library-bootstrap fills in.

## Required fields

```json
{
  "name": "<library-name>",
  "version": "0.1.0",
  "description": "<one-paragraph from Stage 1's library-intake.yaml>",
  "license": "Apache-2.0"
}
```

| Field | Source | Notes |
|---|---|---|
| `name` | library-intake.yaml `name:` | Must match `^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$` |
| `version` | hardcoded `"0.1.0"` for fresh libraries | Subsequent bumps via VERSIONING-POLICY.md rules |
| `description` | library-intake.yaml `description:` | One paragraph; matches plugin's stated purpose |
| `license` | hardcoded `"Apache-2.0"` | Default; can be changed per-library if needed |

## Optional fields

| Field | When to include |
|---|---|
| `keywords` | Always — array of 3–6 strings categorizing the library |
| `homepage` | If the library has a docs URL |
| `repository` | If the source repo URL differs from the marketplace's `source` field |

## Schema validation

Currently no schema validator runs against `plugin.json` (Claude Code
itself validates at plugin-load time). If a future library-bootstrap
build trigger fires for "first publish failure due to manifest
shape", this reference adds the failing field-validity rules.

Until then: trust Claude Code's plugin-load validation to surface
malformed manifests at install time.

## Stage 2 gate (library-bootstrap)

The gate is "JSON parses; required keys present". The 4 required
keys above (name, version, description, license) must all be set.
Optional keys are left out unless the operator supplies them.

## Example

```json
{
  "name": "context-postgres",
  "version": "0.1.0",
  "description": "Postgres-domain skills for the meta-pipeline ecosystem.",
  "license": "Apache-2.0",
  "keywords": ["postgres", "sql", "database", "migrations"]
}
```
