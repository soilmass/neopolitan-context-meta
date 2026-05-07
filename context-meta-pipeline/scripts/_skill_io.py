"""
_skill_io.py — internal utility module for parsing SKILL.md files,
splitting their H2 bodies, detecting archetypes, walking the library,
and loading SNAPSHOT.lock.

This module exists because v0.6.0 had 7 scripts each independently
re-implementing parse_skill / split_h2_bodies / split_sections /
detect_archetype. Phase 1 of the v0.7.0 build-out consolidates them
here so the parsing rules live in one place.

This module is INTERNAL — it has no CLI surface and is therefore not
subject to the validator interface contract documented in
governance/EXTENSION-POINTS.md §2 (which applies to scripts/<name>.py
files with argparse + exit codes 0/1/2). It is a private helper.

The Finding and Report dataclasses live here as their canonical home;
validate-metadata.py re-exports them via PEP 484 `from _skill_io
import Finding as Finding` to preserve the dummy-validator-shape
extension-seam fixture (verify.sh §9b ast-walks validate-metadata.py
for ClassDef nodes named "Finding" and "Report").

Dependencies: PyYAML + stdlib only — same constraint that's been
load-bearing across the library since v0.1.0.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError as e:
    raise ImportError("PyYAML required: pip install pyyaml") from e


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ARCHETYPES: tuple[str, ...] = ("atom", "tool", "router", "orchestrator", "policy")


# ---------------------------------------------------------------------------
# Findings + Reports (canonical home; re-exported from validate-metadata.py)
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single validation finding. Severity is "error" or "warning"."""
    severity: str  # "error" | "warning"
    message: str

    def render_text(self) -> str:
        prefix = "[X]" if self.severity == "error" else "[!]"
        return f"{prefix} {self.message}"


@dataclass
class Report:
    """A per-skill validation rollup. Used by validate-metadata.py."""
    skill: str
    archetype: str
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def add(self, f: Finding) -> None:
        (self.errors if f.severity == "error" else self.warnings).append(f)

    def render_text(self) -> str:
        if self.passed and not self.warnings:
            return f"METADATA VALIDATION PASSED for skill: {self.skill}\nArchetype detected: {self.archetype}\n"

        header = (
            f"METADATA VALIDATION {'PASSED (with warnings)' if self.passed else 'FAILED'} for skill: {self.skill}\n"
            f"Archetype detected: {self.archetype}\n\n"
        )
        out = [header]
        if self.errors:
            out.append("Errors (block merge):\n")
            out.extend(f.render_text() + "\n" for f in self.errors)
            out.append("\n")
        if self.warnings:
            out.append("Warnings (do not block):\n")
            out.extend(f.render_text() + "\n" for f in self.warnings)
            out.append("\n")
        if self.errors:
            out.append("Fix the errors and re-run validation.\n")
        return "".join(out)

    def render_json(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "archetype": self.archetype,
            "errors": [f.message for f in self.errors],
            "warnings": [f.message for f in self.warnings],
            "passed": self.passed,
        }


# ---------------------------------------------------------------------------
# SkillDoc — rich parsing dataclass
# ---------------------------------------------------------------------------


@dataclass
class SkillDoc:
    """Rich parsed representation of a SKILL.md file. Used by
    validate-metadata.py and any script that wants section_titles or
    body_lines counts."""
    path: Path
    frontmatter: dict[str, Any]
    body: str
    body_lines: int

    @property
    def section_titles(self) -> list[str]:
        # H2 sections only — `## Section Name`
        return [
            line[3:].strip()
            for line in self.body.splitlines()
            if line.startswith("## ") and not line.startswith("### ")
        ]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_skill_text(text: str, *, source: str = "<text>") -> tuple[dict[str, Any], str]:
    """Parse a SKILL.md from a text string. Returns (frontmatter, body).

    Used by scripts that read content from git history (e.g.,
    detect-breaking-changes against a baseline-ref) or from any source
    other than a filesystem path.

    Raises ValueError on malformed input. The `source` kwarg is purely
    cosmetic — included in the error message to identify which file or
    git ref was being parsed when the error occurred.
    """
    if not text.startswith("---\n"):
        raise ValueError(f"{source}: missing YAML frontmatter (no leading ---)")
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        raise ValueError(f"{source}: unterminated YAML frontmatter")
    frontmatter_text = text[4:end_idx]
    body = text[end_idx + 5 :]
    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"{source}: malformed YAML frontmatter: {e}") from e
    if not isinstance(frontmatter, dict):
        raise ValueError(
            f"{source}: frontmatter must be a mapping, got {type(frontmatter).__name__}"
        )
    return frontmatter, body


def parse_skill(path: Path) -> SkillDoc:
    """Parse a SKILL.md from a filesystem path. Returns a rich SkillDoc.

    For scripts that only need (frontmatter, body), use parse_skill_text
    against the file contents instead — that pattern is what most
    scripts (audit-skill, rollback-skill, etc.) prefer.
    """
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_skill_text(text, source=str(path))
    body_lines = body.count("\n")
    return SkillDoc(path=path, frontmatter=frontmatter, body=body, body_lines=body_lines)


# ---------------------------------------------------------------------------
# Section splitting (the most-duplicated function in v0.6.0)
# ---------------------------------------------------------------------------


def split_h2_bodies(body: str) -> dict[str, str]:
    """Split a markdown body into a {h2-title: content} dict.

    Identical implementation to what 6 scripts each independently
    shipped in v0.6.0. H2 only — `### Subsection` lines are NOT
    treated as section starts; they stay inside whatever H2 they
    fall under.
    """
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            current = line[3:].strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {title: "\n".join(lines).strip() for title, lines in sections.items()}


# ---------------------------------------------------------------------------
# Archetype detection
# ---------------------------------------------------------------------------


def detect_archetype(frontmatter: dict[str, Any], override: str | None = None) -> str:
    """Detect a skill's archetype from frontmatter, with optional override.

    Returns the canonical archetype name (one of ARCHETYPES) or "atom"
    as the silent fallback. Note: silent-fallback is preserved here for
    backward compatibility with the existing detect_archetype calls;
    validate-metadata.py:check_archetype_known() (added v0.6.0) emits
    an explicit error finding when the frontmatter `archetype:` value
    is unknown, surfacing the seam-discipline issue at validation time.
    """
    if override:
        if override not in ARCHETYPES:
            raise ValueError(
                f"unknown archetype override: {override!r}; expected one of {ARCHETYPES}"
            )
        return override
    meta = frontmatter.get("metadata", {})
    if isinstance(meta, dict):
        archetype_value = meta.get("archetype")
        if isinstance(archetype_value, str):
            a: str = archetype_value.lower()
            if a in ARCHETYPES:
                return a
    return "atom"


# ---------------------------------------------------------------------------
# Library traversal
# ---------------------------------------------------------------------------


def iter_live_skills(plugin_root: Path) -> Iterator[Path]:
    """Yield every live SKILL.md under <plugin_root>/skills/*/SKILL.md.

    Walks the directory directly rather than reading SNAPSHOT.lock —
    this is intentional: the directory is the source of truth for
    "what files exist." SNAPSHOT.lock is the canonical *register* of
    which skills are blessed; coverage-check.py and library-audit.py
    cross-validate the two.
    """
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_file():
            yield skill_md


# ---------------------------------------------------------------------------
# Snapshot loading
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Tokenization (v0.7.0: relocated from routing-eval-runner.py for reuse by
# search-skills.py and any future consumer.)
# ---------------------------------------------------------------------------


TOKEN_STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or", "but",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "with", "by", "as", "this", "that", "these", "those",
    "it", "its", "from", "into", "than", "then", "if", "when", "while",
    "where", "use", "uses", "used", "using", "not", "no", "any", "all", "more",
    "most", "some", "each", "every", "such", "skill", "skills", "via", "stage",
    "stages", "i", "you", "we", "my", "your", "our", "show", "me",
})


def tokens(text: str) -> set[str]:
    """Tokenize text for routing-eval / search-skills overlap matching.

    Lowercases, strips kebab segments, drops stopwords and 1-2 char tokens,
    and applies basic suffix-stemming (ing/ies/es/ed/s). Returns the set of
    tokens (set, not list — search uses set intersection).
    """
    out: set[str] = set()
    for w in re.findall(r"[A-Za-z][A-Za-z-]*", text):
        w = w.lower().strip("-")
        if not w or w in TOKEN_STOPWORDS or len(w) < 3:
            continue
        for suffix in ("ing", "ies", "es", "ed", "s"):
            if w.endswith(suffix) and len(w) > len(suffix) + 2:
                w = w[: -len(suffix)]
                break
        out.add(w)
    return out


def load_snapshot(path: Path) -> dict[str, Any]:
    """Load and validate SNAPSHOT.lock as a YAML mapping.

    Returns the parsed dict. Raises ValueError if the file is missing
    or doesn't parse as a top-level mapping. Does NOT validate schema
    beyond the top-level shape — coverage-check.py and library-audit
    own schema-level invariants.
    """
    if not path.is_file():
        raise ValueError(f"{path}: SNAPSHOT.lock not found")
    text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"{path}: malformed SNAPSHOT.lock YAML: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"{path}: SNAPSHOT.lock must be a mapping at top level")
    return data
