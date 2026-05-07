# Deprecation Communication

**Build trigger:** library has external consumers (other teams,
third-party users) for whom CHANGELOG-only communication is
insufficient.

**Pre-trigger applicability:** *None.* The meta-pipeline has no
external consumers as of v0.5.0. CHANGELOG entries + the
`skill-retire` redirect-note mechanism + audit-skill banners cover
the in-house case.

---

## What deprecation communication covers

When a skill is retired or substantially changed, four channels
should communicate the change:

1. **`CHANGELOG.md`** — already canonical; entry under the
   release date.
2. **In-description warning banner** — applied by `skill-retire`
   Stage 3 to the retired skill's body; visible at skill load
   time.
3. **Direct notification to dependent skill maintainers** — for
   routers and orchestrators that pin the retired skill.
4. **Sunset timeline** — for non-immediate retirements, a date by
   which consumers should have migrated.

The first two ship today (in-house). The third + fourth become
load-bearing only when external consumers exist.

## Channel 3: dependent notification

When `skill-retire` Stage 4 identifies dependents (per
`SNAPSHOT.lock` `depends_on:`):

- Each dependent's maintainer receives a notification (email,
  channel post, GitHub PR comment — whatever the consuming team's
  communication channel is).
- The notification names: the retired skill, the replacement (if
  any), the migration guide (if any), the timeline.
- The notification includes the GitHub PR or commit link for the
  retirement, so the maintainer can subscribe / track.

The implicit-ownership model (`MAINTENANCE.md`) identifies the
maintainer as the last contributor to the dependent skill.

## Channel 4: sunset timeline

For retirements that should be propagated by a date (rather than
immediately):

- The retirement entry in `CHANGELOG.md` includes a "Sunset:
  YYYY-MM-DD" line.
- Until the sunset date, consumers can still pin to the retired
  version.
- After the sunset date, the retired version is no longer
  recommended (it's still in git history and still pinnable, but
  the warning banner becomes louder).

## Notification mechanism (when implemented)

A `scripts/notify-dependents.py` (deferred) takes a retirement
event + the four channels' configurations and:

1. Pulls the dependent list from `SNAPSHOT.lock`.
2. Resolves each dependent's maintainer via the implicit-ownership
   query.
3. Drafts a notification message per channel.
4. Calls the channel's API (SMTP for email, Slack/Discord webhook
   for chat, gh API for PR comments).

The configuration lives at `governance/notification-channels.yaml`
(deferred), with the schema:

```yaml
channels:
  - type: email
    smtp: smtp.example.com
    from: meta-pipeline@example.com
  - type: slack
    webhook_url: ${SLACK_WEBHOOK_URL}
  - type: github
    repo: org/consumer-library
```

## Pre-trigger behavior

Until external consumers exist, these channels are unused:

- Channel 1 (CHANGELOG) and Channel 2 (in-description banner) work
  today.
- Channel 3 (dependent notification) is implicitly handled by the
  in-house team (everyone reads the CHANGELOG).
- Channel 4 (sunset timeline) is implicitly "next release" for
  the in-house case.

## Cross-references

- `skills/skill-retire/SKILL.md` — the procedure that triggers
  notifications.
- `skills/skill-retire/references/redirect-note-template.md` —
  Channel 2's mechanism.
- `GOVERNANCE.md` §"CHANGELOG and Audit Trail" — Channel 1.
- `MAINTENANCE.md` §"Implicit Ownership" — identifies the
  maintainer for Channel 3.
- `coverage.md` Domains Out of Scope §"Skill marketplace mechanics"
  — currently out of scope; deprecation communication scales when
  the marketplace question reverses.

## Out of scope

- Public PR / press / announcements (consumer-side comms,
  case-by-case).
- Customer support workflows (out of meta-pipeline scope).
- Long-term archival of retired skills (already covered by
  `skill-retire` — git history is the archive).
