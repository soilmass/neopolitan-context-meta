#!/usr/bin/env python3
"""
audit-skill.py — mechanizes the implementable health gates from
skill-audit's references/health-gates.md.

Runs Gate 1 (recency via `git log`) and Gate 4 (description drift via the
Jaccard formula pinned in health-gates.md). Gates 2 (test pass rate) and
3 (triggering accuracy) are explicit N/A in v0.1.x — both depend on
infrastructure deferred per governance/INDEX.md and library-root
coverage.md.

Output is a per-skill rollup. For any skill that fails Gate 1 or Gate 4,
emits a banner block matching MAINTENANCE.md §"Auto-Warn Mechanism" that
the operator prepends to the skill's description on the next release.

Exit codes:
  0  every audited skill passes (or has explicit N/A)
  1  one or more skills failed an implementable gate
  2  invocation problem (no skills found, malformed YAML, etc.)

Usage:
  audit-skill.py --all                       # audit every skill under ./skills/
  audit-skill.py --skill skill-author        # one skill
  audit-skill.py --skill skill-author --skill skill-audit
  audit-skill.py --all --format json
  audit-skill.py --all --recency-months 6    # override the recency threshold

Dependencies: PyYAML + stdlib + subprocess (git for Gate 1; ok if absent).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# v0.6.1: shared parser + archetype detection + section splitter live in
# _skill_io. Keeps parsing rules in one place (was 7-way duplicated at v0.6.0).
# _skill_io re-exports raise its own ImportError if PyYAML is missing.
from _skill_io import (
    ARCHETYPES as _SKILL_IO_ARCHETYPES,
    detect_archetype as _detect_archetype_shared,
    parse_skill_text,
    split_h2_bodies,
)


# ---------------------------------------------------------------------------
# Constants from skill-audit/references/health-gates.md
# ---------------------------------------------------------------------------

RECENCY_MONTHS_DEFAULT = 6  # Gate 1
DRIFT_THRESHOLD = 0.10  # Gate 4 — drift must be < 10%

# Stopwords stripped from tokenization. Includes structural words common in
# this library's prose ("stage", "gate", "produce", "consume") that don't
# carry capability semantics on their own.
STOPWORDS = frozenset({
    # Articles, conjunctions, prepositions, common verbs:
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or",
    "but", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "do", "does", "did", "with", "by", "as", "this", "that",
    "these", "those", "it", "its", "from", "into", "than", "then", "if",
    "when", "while", "where", "use", "uses", "used", "using", "not", "no",
    "any", "all", "more", "most", "some", "each", "every", "such",
    # Library-pipeline noise:
    "skill", "skills", "via", "stage", "stages", "gate", "gated", "gates",
    "step", "steps", "produce", "produces", "produced", "consume",
    "consumes", "consumed", "section", "sections", "block", "blocks",
    "entry", "entries", "field", "fields", "file", "files", "name", "names",
    "list", "lists", "level", "levels", "single", "multiple", "new",
    "existing", "one", "two", "three", "four", "five", "six",
    "through", "across", "between", "above", "below", "after", "before",
})


@dataclass
class GateResult:
    name: str  # "recency" | "test_pass_rate" | "triggering_accuracy" | "drift"
    status: str  # "pass" | "fail" | "n/a"
    value: str  # human-readable value (e.g., "3 months ago", "8.4%")
    threshold: str  # human-readable threshold (e.g., "<6 months", "<10%")
    reason: str = ""  # populated for n/a or fail


@dataclass
class SkillRollup:
    skill: str
    gates: list[GateResult] = field(default_factory=list)

    @property
    def has_failure(self) -> bool:
        return any(g.status == "fail" for g in self.gates)


# v0.6.1: parse_skill / split_sections / detect_archetype now live in _skill_io.
# Local thin wrappers preserve the existing call sites' shape without duplicating
# logic. Removing has_any_data which had no consumers anywhere in the codebase.

def parse_skill(path: Path) -> tuple[dict[str, Any], str]:
    """Wrapper around _skill_io.parse_skill_text. Preserves the existing
    audit-skill API shape (tuple of frontmatter+body)."""
    return parse_skill_text(path.read_text(encoding="utf-8"), source=str(path))


# Section splitter — re-export under the original name `split_sections` so the
# rest of audit-skill.py doesn't need touching. Functionally identical.
split_sections = split_h2_bodies

# Archetype valid-set + detection — re-export so existing references stay valid.
VALID_ARCHETYPES = _SKILL_IO_ARCHETYPES


def detect_archetype(fm: dict[str, Any]) -> str:
    return _detect_archetype_shared(fm)


# ---------------------------------------------------------------------------
# Gate 1: Recency
# ---------------------------------------------------------------------------


def gate_recency(skill_dir: Path, fm: dict[str, Any], threshold_months: int) -> GateResult:
    """Gate 1 — recency: skill last touched within `threshold_months`.
    Bypassed by `metadata.recency_pin: stable`. Per MAINTENANCE.md."""
    # `metadata.recency_pin: stable` bypasses the gate per health-gates.md.
    meta = fm.get("metadata") or {}
    pin = meta.get("recency_pin") if isinstance(meta, dict) else None
    if pin == "stable":
        return GateResult(
            name="recency",
            status="pass",
            value="pinned stable",
            threshold=f"<{threshold_months} months",
            reason="metadata.recency_pin: stable",
        )

    # `git log --format=%cI -n 1 -- <skill-dir-rel>` returns the most recent
    # ISO-8601 commit date affecting the skill's directory.
    try:
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=skill_dir,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # No git repo. Per skill-audit Stage 2 edge case: treat as freshly-
        # authored using working-tree mtime.
        mtime = skill_dir.stat().st_mtime
        last = _dt.datetime.fromtimestamp(mtime, tz=_dt.timezone.utc)
        return _recency_finalize(last, threshold_months, source="working-tree mtime (no git)")

    rel = str(skill_dir.resolve().relative_to(repo_root))
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=%cI", "-n", "1", "--", rel],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        out = ""

    if not out:
        # No commits yet — freshly authored (skill-audit Stage 2 edge case).
        return GateResult(
            name="recency",
            status="pass",
            value="no commits yet",
            threshold=f"<{threshold_months} months",
            reason="freshly_authored: true",
        )

    try:
        last = _dt.datetime.fromisoformat(out)
    except ValueError:
        return GateResult(
            name="recency",
            status="n/a",
            value=out,
            threshold=f"<{threshold_months} months",
            reason="git returned an unparseable date",
        )

    return _recency_finalize(last, threshold_months, source="git log")


def _recency_finalize(
    last: _dt.datetime, threshold_months: int, source: str
) -> GateResult:
    now = _dt.datetime.now(tz=_dt.timezone.utc) if last.tzinfo else _dt.datetime.now()
    delta = now - last
    months = delta.days / 30.4375
    if months < threshold_months:
        return GateResult(
            name="recency",
            status="pass",
            value=f"{months:.1f} months ago",
            threshold=f"<{threshold_months} months",
            reason=source,
        )
    return GateResult(
        name="recency",
        status="fail",
        value=f"{months:.1f} months ago",
        threshold=f"<{threshold_months} months",
        reason=source,
    )


# ---------------------------------------------------------------------------
# Gate 4: Description drift (Jaccard distance, formula from health-gates.md)
# ---------------------------------------------------------------------------


def gate_drift(fm: dict[str, Any], body: str, archetype: str | None = None) -> GateResult:
    # archetype is accepted for forward-compat but not used in the asymmetric
    # containment formula (which scans the entire body, not an archetype-
    # specific section). Earlier formula used it; preserved for callers.
    """Asymmetric containment per health-gates.md Gate 4 (v0.2.0 formula).

    drift = |A − B_full| / |A|

    where A is description tokens (sans anti-trigger block) and B_full is
    *all* body tokens. The asymmetric measure captures "description
    over-promises" without penalizing bodies that go deeper than the
    description summarizes.
    """
    desc = fm.get("description") or ""
    desc_set = _tokenize(_strip_anti_triggers(desc))
    body_set = _tokenize(body)

    if not desc_set:
        return GateResult(
            name="drift",
            status="n/a",
            value="—",
            threshold=f"<{int(DRIFT_THRESHOLD*100)}%",
            reason="description has no capability tokens",
        )

    # Containment is prefix-based: a description token "matches" the body
    # if any body token shares at least the first 5 characters (or is
    # contained in / contains the description token). This forgives
    # imperfect lemmatization — `orchestrat` (from "orchestrates") matches
    # `orchestrator` in the body; `archival` matches `archive`.
    missing: set[str] = set()
    for token in desc_set:
        if token in body_set:
            continue
        if any(_token_match(token, b) for b in body_set):
            continue
        missing.add(token)

    drift = len(missing) / len(desc_set)
    pct = f"{drift*100:.1f}%"

    if drift < DRIFT_THRESHOLD:
        return GateResult(
            name="drift",
            status="pass",
            value=pct,
            threshold=f"<{int(DRIFT_THRESHOLD*100)}%",
        )
    return GateResult(
        name="drift",
        status="fail",
        value=pct,
        threshold=f"<{int(DRIFT_THRESHOLD*100)}%",
        reason=f"description claims {sorted(missing)[:8]} (truncated); not found in body",
    )


def _token_match(a: str, b: str, min_prefix: int = 5) -> bool:
    """Two tokens "match" if either contains the other as a prefix of length
    >= min_prefix. Forgives noun/verb form differences ("archive" / "archival",
    "orchestrate" / "orchestrator")."""
    if len(a) < min_prefix or len(b) < min_prefix:
        return a == b
    short, long = (a, b) if len(a) <= len(b) else (b, a)
    return long.startswith(short[:min_prefix])


def _strip_anti_triggers(desc: str) -> str:
    """Drop the 'Do NOT use for' anti-trigger block from a description."""
    for phrase in ("Do NOT use for", "Do not use for", "do NOT use for"):
        idx = desc.find(phrase)
        if idx != -1:
            return desc[:idx]
    return desc


def _tokenize(text: str) -> set[str]:
    """Lowercase, drop stopwords, lemmatize crudely. Used for both A and B."""
    tokens: set[str] = set()
    for word in re.findall(r"[A-Za-z][A-Za-z-]*", text):
        w = word.lower().strip("-")
        if not w or w in STOPWORDS or len(w) < 3:
            continue
        # Crude lemmatization: drop trailing 'ing' / 'ies' / 'es' / 'ed' / 's'.
        for suffix in ("ing", "ies", "es", "ed", "s"):
            if w.endswith(suffix) and len(w) > len(suffix) + 2:
                w = w[: -len(suffix)]
                break
        tokens.add(w)
    return tokens


# ---------------------------------------------------------------------------
# Gates 2 + 3 — explicit N/A in v0.1.x
# ---------------------------------------------------------------------------


def gate_test_pass_rate() -> GateResult:
    """Gate 2 — test pass rate (deferred): per-skill integration test pass-rate
    >90%. Mechanizer is INTEGRATION-TESTING.md (build trigger 10+ cross-dep
    skills + 2 regressions; not yet fired). Reports explicit N/A today."""
    return GateResult(
        name="test_pass_rate",
        status="n/a",
        value="—",
        threshold=">90%",
        reason="INTEGRATION-TESTING.md deferred per governance/INDEX.md",
    )


def gate_eval_coverage(skill_name: str, eval_path: Path | None, threshold: int = 3) -> GateResult:
    """Gate 5 (v0.6.1) — eval-suite coverage: a skill must have at least
    `threshold` positive prompts in scripts/tests/routing-eval.yaml. Catches
    the case where a skill ships without held-out coverage; that's the input
    Gate 3 (triggering accuracy) needs once the routing-layer runner exists.

    Mechanizable today (no deferred infra). Reports N/A only when the suite
    file is missing entirely.
    """
    if eval_path is None or not eval_path.is_file():
        return GateResult(
            name="eval_coverage",
            status="n/a",
            value="—",
            threshold=f">={threshold} prompts",
            reason="no routing-eval suite — file missing",
        )
    try:
        import yaml  # type: ignore[import-untyped]
        data = yaml.safe_load(eval_path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError) as e:
        return GateResult(
            name="eval_coverage",
            status="n/a",
            value="—",
            threshold=f">={threshold} prompts",
            reason=f"eval suite unreadable: {e}",
        )
    prompts = data.get("prompts") or []
    if not isinstance(prompts, list):
        return GateResult(
            name="eval_coverage",
            status="n/a",
            value="—",
            threshold=f">={threshold} prompts",
            reason="eval suite has no prompts: list",
        )
    n = sum(
        1 for p in prompts
        if isinstance(p, dict) and p.get("expected") == skill_name
    )
    if n >= threshold:
        return GateResult(
            name="eval_coverage",
            status="pass",
            value=f"{n} positive prompts",
            threshold=f">={threshold} prompts",
        )
    return GateResult(
        name="eval_coverage",
        status="fail",
        value=f"{n} positive prompts",
        threshold=f">={threshold} prompts",
        reason=f"add {threshold - n} more `expected: {skill_name}` prompts",
    )


def gate_triggering_accuracy(skill_name: str, eval_path: Path | None) -> GateResult:
    """Gate 3 — triggering accuracy (deferred runner): held-out routing-eval
    accuracy >85%. Suite exists at scripts/tests/routing-eval.yaml from v0.2.0;
    real routing-layer runner is deferred per coverage.md `skill-evaluate`
    row. Reports N/A with reason today."""
    if eval_path is None or not eval_path.is_file():
        return GateResult(
            name="triggering_accuracy",
            status="n/a",
            value="—",
            threshold=">85%",
            reason="no routing-eval suite — see coverage.md Deferred section for skill-evaluate",
        )
    # Suite exists. v0.1.x doesn't ship a routing layer to actually run the
    # prompts against, so we report that the input is present but the runner
    # is deferred. Honest N/A rather than a fake number.
    return GateResult(
        name="triggering_accuracy",
        status="n/a",
        value="—",
        threshold=">85%",
        reason=f"eval suite present at {eval_path} but routing-layer runner is "
        f"deferred per coverage.md (build trigger: 25 skills OR first regression)",
    )


# ---------------------------------------------------------------------------
# Banner emission per MAINTENANCE.md §"Auto-Warn Mechanism"
# ---------------------------------------------------------------------------


def render_banner(rollup: SkillRollup) -> str:
    if not rollup.has_failure:
        return ""
    out = ["⚠️ Health Check Failing"]
    for g in rollup.gates:
        check = "✓" if g.status == "pass" else ""
        if g.status == "n/a":
            out.append(f"{_label(g.name)}: N/A ({g.threshold}) — {g.reason}")
        else:
            out.append(f"{_label(g.name)}: {g.value} (threshold: {g.threshold}) {check}".rstrip())
    return "\n".join(out)


def _label(name: str) -> str:
    return {
        "recency": "Last update",
        "test_pass_rate": "Test pass rate",
        "triggering_accuracy": "Triggering accuracy",
        "drift": "Description drift",
        "eval_coverage": "Eval coverage",
    }.get(name, name)


# ---------------------------------------------------------------------------
# Banner application (v0.6.2: --apply-banners)
# ---------------------------------------------------------------------------


# A banner is a multiline block starting with this exact marker. v0.6.2's
# --apply-banners detects existing banners by this prefix to ensure idempotency.
BANNER_MARKER = "⚠️ Health Check Failing"


def apply_banner_to_skill_md(
    skill_md_path: Path, banner: str, *, dry_run: bool = True
) -> tuple[bool, str]:
    """Prepend a banner block to a SKILL.md's frontmatter `description:` value.

    Uses string-replace surgery on the frontmatter region — does NOT round-trip
    through yaml.safe_dump (PyYAML drops quoting style + key order). The
    description must use the `description: >\\n  ...` folded-block style; that's
    the convention every skill in this library follows (validate-metadata.py
    enforces ≤1024 chars but doesn't enforce style; current 14/14 skills use
    the folded style).

    Idempotent: if the description already contains BANNER_MARKER, returns
    (False, "already-applied").

    Returns (mutated, reason). When dry_run=True, no file write occurs but the
    same logic runs for accurate reporting.
    """
    text = skill_md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return (False, "no-frontmatter")
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        return (False, "unterminated-frontmatter")

    frontmatter = text[4:end_idx]
    if BANNER_MARKER in frontmatter:
        return (False, "already-applied")

    # Find the description: line. Must be folded-block style (`description: >`).
    desc_match = re.search(r"(?m)^description:\s*>\s*\n", frontmatter)
    if not desc_match:
        return (False, "no-folded-description")

    # The folded-block continues until the next un-indented top-level key. Find
    # it by walking lines after the `description: >` marker.
    insert_pos_in_fm = desc_match.end()  # right after "description: >\n"
    # The first body line of the folded block. Banner lines are 2-space-indented
    # to match the YAML folded-block convention.
    banner_block = "\n".join(f"  {ln}" if ln else "" for ln in banner.splitlines())
    # Insert: banner_block + blank line (folded YAML treats consecutive blank
    # lines as a paragraph break, preserving structure).
    insertion = banner_block + "\n  \n"

    new_frontmatter = frontmatter[:insert_pos_in_fm] + insertion + frontmatter[insert_pos_in_fm:]
    new_text = "---\n" + new_frontmatter + "\n---\n" + text[end_idx + 5 :]

    if not dry_run:
        skill_md_path.write_text(new_text, encoding="utf-8")
    return (True, "would-apply" if dry_run else "applied")


# ---------------------------------------------------------------------------
# SNAPSHOT.lock health-state writeback (v0.6.2)
# ---------------------------------------------------------------------------


# 6-state health enum per SNAPSHOT.lock comments. v0.6.2 starts using them.
HEALTH_STATES = ("fresh", "healthy", "flagged", "unhealthy", "rolled-back", "retired")
# States that --write-health preserves (operator-managed, audit doesn't touch).
PRESERVED_HEALTH_STATES = frozenset({"rolled-back", "retired"})


def _read_prior_health(snapshot_path: Path) -> dict[str, str]:
    """Read each skill's previous health from `git show HEAD~1:SNAPSHOT.lock`.
    Returns {} if git history is unavailable (shallow clone, fresh repo)."""
    try:
        repo_root = Path(
            subprocess.check_output(
                ["git", "-C", str(snapshot_path.parent), "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        )
        rel = snapshot_path.resolve().relative_to(repo_root)
        text = subprocess.check_output(
            ["git", "-C", str(repo_root), "show", f"HEAD~1:{rel}"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        import yaml
        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict):
            return {}
        skills = data.get("skills") or {}
        if not isinstance(skills, dict):
            return {}
        prior: dict[str, str] = {}
        for name, spec in skills.items():
            if isinstance(spec, dict) and isinstance(spec.get("health"), str):
                prior[name] = spec["health"]
        return prior
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return {}


def _classify_health(rollup: SkillRollup, prior: str | None) -> str:
    """Determine new health state from gates + prior state.

    - any-fail: `flagged` (or `unhealthy` if prior was `flagged`)
    - all-pass-implementable: `healthy`
    - never observed (no rollup gates): preserve prior or default `fresh`
    """
    if not rollup.gates:
        return prior or "fresh"
    if rollup.has_failure:
        if prior == "flagged":
            return "unhealthy"
        return "flagged"
    # All implementable gates pass (n/a doesn't count as fail).
    return "healthy"


def write_health_to_snapshot(snapshot_path: Path, rollups: list[SkillRollup]) -> int:
    """Write per-skill health states back to SNAPSHOT.lock via string-replace
    surgery (does NOT round-trip through yaml.safe_dump — preserves quoting and
    key order). Idempotent: re-running with no state change produces no diff.

    Returns the number of skills whose `health:` value was actually mutated.
    """
    text = snapshot_path.read_text(encoding="utf-8")
    prior = _read_prior_health(snapshot_path)
    n_changed = 0
    for rollup in rollups:
        # Preserve operator-managed states.
        existing = _extract_skill_health(text, rollup.skill)
        if existing in PRESERVED_HEALTH_STATES:
            continue
        new_state = _classify_health(rollup, prior.get(rollup.skill))
        if existing == new_state:
            continue
        text = _replace_skill_health(text, rollup.skill, new_state)
        n_changed += 1
    if n_changed > 0:
        snapshot_path.write_text(text, encoding="utf-8")
    return n_changed


def _find_skill_block(snapshot_text: str, skill_name: str) -> tuple[int, int] | None:
    """Locate the byte range of a skill's block in SNAPSHOT.lock.

    Skill blocks live under `skills:` at 2-space indent. The block's body lines
    are at 4-space (or deeper) indent until the next 2-space-or-shallower line.
    Returns (start_byte, end_byte) of the block including its body, or None.
    """
    # Find the skill heading line.
    head_pattern = re.compile(
        rf'^(  {re.escape(skill_name)}:\s*)$\n', re.MULTILINE
    )
    m = head_pattern.search(snapshot_text)
    if not m:
        return None
    block_start = m.start()
    # Walk forward line-by-line until we hit a line that's not 4-space-indented
    # (or empty/comment) — that's the next block's start.
    pos = m.end()
    while pos < len(snapshot_text):
        eol = snapshot_text.find("\n", pos)
        if eol == -1:
            pos = len(snapshot_text)
            break
        line = snapshot_text[pos:eol]
        # A line is "still in this block" if it's 4-space-indented OR empty.
        if line.startswith("    ") or line.strip() == "":
            pos = eol + 1
            continue
        # A 2-space-indented line is the next sibling skill (or `retired:` etc).
        # A 0-space-indented line is the next top-level key.
        # Either way, current block ends here.
        break
    return (block_start, pos)


def _extract_skill_health(snapshot_text: str, skill_name: str) -> str | None:
    """Find the `health:` value for a given skill in SNAPSHOT.lock text."""
    span = _find_skill_block(snapshot_text, skill_name)
    if span is None:
        return None
    block = snapshot_text[span[0]:span[1]]
    health_match = re.search(r'^\s+health:\s*["\']?([^"\'\n]+)["\']?\s*$', block, re.MULTILINE)
    if not health_match:
        return None
    return health_match.group(1).strip()


def _replace_skill_health(snapshot_text: str, skill_name: str, new_state: str) -> str:
    """Replace the `health:` value for a given skill, preserving quoting style."""
    span = _find_skill_block(snapshot_text, skill_name)
    if span is None:
        return snapshot_text  # No block to update; leave alone.
    block = snapshot_text[span[0]:span[1]]
    # Replace health: line within block. Preserve double-quoted style (matches
    # the canonical SNAPSHOT.lock convention).
    new_block = re.sub(
        r'(^\s+health:\s*)["\']?[^"\'\n]+["\']?(\s*)$',
        rf'\1"{new_state}"\2',
        block,
        count=1,
        flags=re.MULTILINE,
    )
    if new_block == block:
        return snapshot_text  # No health: line in this block; nothing to do.
    return snapshot_text[: span[0]] + new_block + snapshot_text[span[1]:]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def render_text(rollups: list[SkillRollup]) -> str:
    out: list[str] = []
    for r in rollups:
        out.append(f"\n=== {r.skill} ===")
        for g in r.gates:
            mark = {"pass": "✓", "fail": "✗", "n/a": "—"}[g.status]
            line = f"  [{mark}] {_label(g.name):<20} {g.value:<22} (threshold: {g.threshold})"
            if g.status != "pass" and g.reason:
                line += f"  | {g.reason[:120]}"
            out.append(line)
        if r.has_failure:
            out.append("\n  Suggested banner:")
            for line in render_banner(r).splitlines():
                out.append(f"    {line}")
    out.append("")
    flagged = [r.skill for r in rollups if r.has_failure]
    if flagged:
        out.append(f"FLAGGED ({len(flagged)}): {', '.join(flagged)}")
    else:
        out.append(f"All {len(rollups)} skills passed implementable gates.")
    return "\n".join(out)


def render_json(rollups: list[SkillRollup]) -> str:
    return json.dumps(
        [
            {
                "skill": r.skill,
                "gates": [
                    {
                        "name": g.name,
                        "status": g.status,
                        "value": g.value,
                        "threshold": g.threshold,
                        "reason": g.reason,
                    }
                    for g in r.gates
                ],
                "banner": render_banner(r) or None,
            }
            for r in rollups
        ],
        indent=2,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--skill", action="append", help="skill name (repeatable)")
    g.add_argument("--all", action="store_true", help="audit every skill under ./skills/")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--recency-months",
        type=int,
        default=RECENCY_MONTHS_DEFAULT,
        help=f"recency threshold in months (default {RECENCY_MONTHS_DEFAULT})",
    )
    parser.add_argument(
        "--eval-suite",
        type=Path,
        default=None,
        help="path to scripts/tests/routing-eval.yaml; default: probe ./scripts/tests/routing-eval.yaml",
    )
    parser.add_argument(
        "--eval-coverage-threshold",
        type=int,
        default=3,
        help="minimum positive prompts per skill in routing-eval.yaml (default 3)",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--apply-banners",
        action="store_true",
        help="prepend health banners to descriptions of failing skills "
        "(idempotent; refuses if banner already present). Use with --dry-run "
        "first to preview changes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="when used with --apply-banners, report what would change without "
        "writing to SKILL.md files.",
    )
    parser.add_argument(
        "--write-health",
        action="store_true",
        help="write back per-skill health states to SNAPSHOT.lock per the "
        "6-state enum (fresh/healthy/flagged/unhealthy/rolled-back/retired). "
        "Idempotent on repeat invocation.",
    )
    args = parser.parse_args(argv)

    skills_root = args.root / "skills"
    if not skills_root.is_dir():
        sys.stderr.write(f"error: no skills/ directory under {args.root}\n")
        return 2

    if args.all:
        skill_dirs = sorted(p for p in skills_root.iterdir() if (p / "SKILL.md").is_file())
    else:
        skill_dirs = []
        for name in args.skill or []:
            d = skills_root / name
            if not (d / "SKILL.md").is_file():
                sys.stderr.write(f"error: skill {name!r} not found at {d}/SKILL.md\n")
                return 2
            skill_dirs.append(d)

    if not skill_dirs:
        sys.stderr.write("error: no skills selected\n")
        return 2

    eval_path = args.eval_suite
    if eval_path is None:
        candidate = args.root / "scripts" / "tests" / "routing-eval.yaml"
        eval_path = candidate if candidate.is_file() else None

    rollups: list[SkillRollup] = []
    for skill_dir in skill_dirs:
        try:
            fm, body = parse_skill(skill_dir / "SKILL.md")
        except ValueError as e:
            sys.stderr.write(f"error parsing {skill_dir.name}: {e}\n")
            return 2
        archetype = detect_archetype(fm)
        rollup = SkillRollup(skill=skill_dir.name)
        rollup.gates.append(gate_recency(skill_dir, fm, args.recency_months))
        rollup.gates.append(gate_test_pass_rate())
        rollup.gates.append(gate_triggering_accuracy(skill_dir.name, eval_path))
        rollup.gates.append(gate_eval_coverage(skill_dir.name, eval_path, args.eval_coverage_threshold))
        rollup.gates.append(gate_drift(fm, body, archetype))
        rollups.append(rollup)

    if args.format == "json":
        print(render_json(rollups))
    else:
        print(render_text(rollups))

    # v0.6.2: --apply-banners — prepend health banners to descriptions of
    # failing skills. Idempotent. Use --dry-run to preview without writing.
    if args.apply_banners:
        applied = 0
        skipped = 0
        for r, skill_dir in zip(rollups, skill_dirs):
            if not r.has_failure:
                continue
            banner = render_banner(r)
            mutated, reason = apply_banner_to_skill_md(
                skill_dir / "SKILL.md", banner, dry_run=args.dry_run
            )
            verb = "DRY-RUN would apply" if args.dry_run else ("APPLIED" if mutated else "SKIPPED")
            sys.stderr.write(f"{verb} banner to {skill_dir.name}: {reason}\n")
            if mutated:
                applied += 1
            else:
                skipped += 1
        sys.stderr.write(f"--apply-banners summary: {applied} would-apply, {skipped} skipped\n")

    # v0.6.2: --write-health — write per-skill health states back to
    # SNAPSHOT.lock. Reads previous state from `git show HEAD~1:SNAPSHOT.lock`
    # to compute "two-consecutive-flagged → unhealthy". Idempotent.
    if args.write_health:
        snap_path = args.root / "SNAPSHOT.lock"
        if not snap_path.is_file():
            sys.stderr.write(f"--write-health: {snap_path} not found; skipping.\n")
        else:
            n_changed = write_health_to_snapshot(snap_path, rollups)
            sys.stderr.write(f"--write-health: {n_changed} skill(s) updated in SNAPSHOT.lock\n")

    return 1 if any(r.has_failure for r in rollups) else 0


if __name__ == "__main__":
    sys.exit(main())
