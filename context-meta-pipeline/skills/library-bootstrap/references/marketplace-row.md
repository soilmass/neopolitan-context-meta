# marketplace.json row reference

`library-bootstrap` Stage 5 adds a row to the parent
`marketplace.json` for the new library. This reference documents
the row shape.

## Row shape

```json
{
  "name": "<library-name>",
  "source": "./<library-dirname>",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "description": "<one-line summary>",
  "keywords": ["<tag1>", "<tag2>", "<tag3>"]
}
```

| Field | Source | Notes |
|---|---|---|
| `name` | library's plugin.json `name` | Must match exactly |
| `source` | path to the library dir relative to the marketplace.json | Always starts with `./` |
| `version` | library's plugin.json `version` | Must match exactly |
| `license` | library's plugin.json `license` | Must match exactly |
| `description` | one-line distillation of plugin.json `description` | Marketplace listings often truncate to ~120 chars |
| `keywords` | library's plugin.json `keywords` | Same array |

## Where the parent marketplace.json lives

Conventional layout: a parent dir that hosts multiple plugins:

```
<workspace>/
├── .claude-plugin/marketplace.json     ← contains the row for each plugin
├── context-meta-pipeline/              ← the meta-pipeline plugin
│   └── .claude-plugin/plugin.json
└── <NEW-LIBRARY>/                       ← what library-bootstrap produced
    └── .claude-plugin/plugin.json
```

Stage 1's `library-intake.yaml` `parent_marketplace:` field names
the path to this marketplace.json.

## Stage 5 gate

The gate: parent marketplace.json parses; the new row's `version`
matches the new library's plugin.json `version`. If the row already
exists for this library name (e.g., re-running bootstrap), Stage 5
halts — the operator must `skill-retire` the existing entry first,
or pick a different name.

## Example

After bootstrap, the parent marketplace.json gains:

```json
{
  "plugins": [
    { "name": "context-meta-pipeline", "source": "./context-meta-pipeline", ... },
    {
      "name": "context-postgres",
      "source": "./context-postgres",
      "version": "0.1.0",
      "license": "Apache-2.0",
      "description": "Postgres-domain skills for the meta-pipeline ecosystem.",
      "keywords": ["postgres", "sql", "database", "migrations"]
    }
  ]
}
```
