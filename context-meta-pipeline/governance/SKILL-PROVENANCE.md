# Skill Provenance

**Build trigger:** skills are distributed beyond the original author's
environment and authenticity verification becomes a real concern. Per
`governance/INDEX.md`, self-contained internal libraries don't need
this; published marketplaces do.

**Pre-trigger applicability:** *None.* The meta-pipeline is internal
to the operator's environment as of v0.5.0. Provenance is not a
concern until skills travel to a third party.

---

## What provenance covers

Once skills cross trust boundaries (published to a marketplace,
shared between organizations, vendored into a downstream consumer),
authenticity verification becomes load-bearing:

- **Was this SKILL.md authored by who I think it was?** (Author
  authentication.)
- **Has this SKILL.md been modified since the author signed it?**
  (Tamper detection.)
- **Is the SNAPSHOT.lock I'm looking at the one the publisher
  signed?** (Ledger integrity.)

The mechanism is GPG signing of release artifacts plus per-file
hashes embedded in `SNAPSHOT.lock`.

## Mechanism

### Per-skill hash in SNAPSHOT.lock

Each skill entry gains a `sha256:` field:

```yaml
skill-author:
  version: "0.1.4"
  archetype: tool
  path: "skills/skill-author/SKILL.md"
  health: "fresh"
  sha256: "abc123..."  # SHA-256 of the SKILL.md bytes
```

The hash is recomputed at every `SNAPSHOT.lock` update. A consumer
verifies by recomputing the hash from the SKILL.md and comparing.

### Signed release tags

Every release tag (`v0.5.0`, etc.) is GPG-signed by the publisher:

```bash
git tag -as v0.5.0 -m "..."
```

The tag's signature attests to the entire `SNAPSHOT.lock` at that
commit, which transitively attests every skill's hash.

### Marketplace-level signature

The parent `marketplace.json` gains a signature row pointing at the
publisher's GPG key fingerprint. Consumers verify the marketplace
itself before trusting any plugin row.

## Verification flow

A consumer of a published library verifies:

1. The marketplace.json signature matches the publisher's known
   GPG key.
2. The plugin's `version` in marketplace.json matches the git tag
   in the plugin's repository.
3. The git tag's GPG signature is valid.
4. Every skill's `sha256:` in `SNAPSHOT.lock` matches the actual
   `SKILL.md` bytes.

If any step fails, the install is refused.

## Implementation

When the trigger fires:

1. `scripts/snapshot-hash.py` is authored — computes / updates
   `sha256:` per skill.
2. `verify.sh` step 8 (added) — verifies hashes match snapshot
   record.
3. `release-tag.sh` is updated to require `git tag -as` (signed).
4. `governance/INDEX.md` documents the publisher's GPG key
   fingerprint policy.
5. This document is cross-referenced from `governance/SECURITY-AUDIT.md`
   (which depends on provenance for forensic accountability).

## Cross-references

- `governance/SECURITY-AUDIT.md` — uses provenance for forensics.
- `GOVERNANCE.md` §"Self-Contained Library" — currently makes this
  unnecessary; that decision reverses if cross-library distribution
  emerges.
- `coverage.md` Domains Out of Scope §"Skill marketplace mechanics"
  — currently out of scope; provenance is the prerequisite.

## Out of scope

- End-to-end encryption of skills in transit (handled by the
  distribution channel — git, HTTPS, etc.).
- Per-operator authentication (handled by Claude Code core).
- Compliance with specific regulatory frameworks (those would
  layer on top of provenance, not replace it).
