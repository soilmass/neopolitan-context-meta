#!/usr/bin/env python3
"""
routing-eval-runner.py — execute the routing-eval suite at
`scripts/tests/routing-eval.yaml` and report triggering accuracy
per skill.

Per skill-audit/references/routing-eval-protocol.md, the suite is a
list of (prompt, expected_skill, source) tuples. The runner needs a
"routing layer" — something that takes a prompt and returns the skill
that fires. Three modes:

  --mode operator    Operator-scored: print each prompt, ask the operator
                     to enter the skill that fired (or 'none'). Useful for
                     a small suite or a calibration run.

  --mode static      Match prompts against skill descriptions using a
                     simple keyword-overlap heuristic. Approximation only;
                     the real routing layer (LLM-based) is what production
                     uses. Use this to detect *gross* mis-routing during
                     development.

  --mode external    Read JSON from stdin: a list of {"prompt": "...",
                     "actual": "skill-name"} entries. The caller is
                     responsible for invoking the real routing layer.
                     This is the production-quality mode.

Per coverage.md `skill-evaluate` deferred row, the production runner
(real routing layer) is deferred. This script is the scaffolding around
it. The static mode is rough but trigger-agnostic.

Exit codes:
  0  eval ran; accuracy report produced
  1  eval ran; one or more skills below 85% triggering accuracy
  2  invocation problem (no suite, malformed, mode-input missing)

Usage:
  routing-eval-runner.py --suite scripts/tests/routing-eval.yaml --mode static
  routing-eval-runner.py --mode static --skill skill-author
  routing-eval-runner.py --mode external < responses.json
  routing-eval-runner.py --mode operator   # interactive
  routing-eval-runner.py --threshold 0.80  # override Gate 3 threshold

Dependencies: PyYAML + stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# v0.7.0: tokens / TOKEN_STOPWORDS relocated to _skill_io for reuse by
# search-skills.py. Local alias preserves call shape.
from _skill_io import tokens as _tokens

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("error: PyYAML not installed. `pip install pyyaml`\n")
    sys.exit(2)


DEFAULT_THRESHOLD = 0.85  # Gate 3 from MAINTENANCE.md


@dataclass
class EvalEntry:
    prompt: str
    expected: str  # skill name, or "none" for true negatives
    source: str
    rationale: str = ""


@dataclass
class EvalResult:
    entry: EvalEntry
    actual: str  # skill name produced by the routing layer (or "none")
    correct: bool


@dataclass
class SkillAccuracy:
    skill: str
    total: int = 0
    correct: int = 0
    failures: list[EvalResult] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


def load_suite(path: Path) -> list[EvalEntry]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or "prompts" not in data:
        raise ValueError(f"{path}: expected a YAML mapping with a 'prompts' key")
    entries: list[EvalEntry] = []
    for item in data["prompts"]:
        if not isinstance(item, dict):
            continue
        entries.append(EvalEntry(
            prompt=str(item.get("prompt", "")),
            expected=str(item.get("expected", "")),
            source=str(item.get("source", "")),
            rationale=str(item.get("rationale", "")),
        ))
    return entries


# ---------------------------------------------------------------------------
# Routing modes
# ---------------------------------------------------------------------------


def static_routing(prompt: str, plugin_root: Path) -> str:
    """Simple keyword-overlap heuristic. Produces an approximation of which
    skill the routing layer would pick. Not a substitute for the real
    LLM-based routing layer; useful for catching gross mis-routing during
    development."""
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return "none"
    prompt_words = set(_tokens(prompt))
    if not prompt_words:
        return "none"
    best_skill = "none"
    best_score = 0.0
    for skill_dir in skills_dir.iterdir():
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8")
        # Pull the description from frontmatter
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[4:end]) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(fm, dict):
            continue
        desc = str(fm.get("description", ""))
        # Drop the anti-trigger block — we don't want anti-trigger words to score
        for marker in ("Do NOT use for", "Do not use for", "do NOT use for"):
            idx = desc.find(marker)
            if idx != -1:
                desc = desc[:idx]
                break
        desc_words = set(_tokens(desc))
        if not desc_words:
            continue
        score = len(prompt_words & desc_words) / len(prompt_words | desc_words)
        # A23 fix (v0.5.2): de-rank routers in the static heuristic. A router's
        # description necessarily lists every atom name it dispatches to via
        # the routing table — so a prompt like "I want to write a new SKILL.md"
        # matches the router as strongly as it matches `skill-author`. The
        # static mode is a coarse pre-screen, not the production routing layer;
        # router atoms should fire only when no atom matches well. Apply a 0.7×
        # de-rank so a tied router loses to a tied atom.
        archetype = ""
        meta = fm.get("metadata")
        if isinstance(meta, dict):
            archetype = str(meta.get("archetype", ""))
        if archetype == "router":
            score *= 0.7
        if score > best_score:
            best_score = score
            best_skill = str(fm.get("name", skill_dir.name))
    return best_skill if best_score > 0.05 else "none"


def operator_routing(prompt: str, choices: list[str]) -> str:
    sys.stderr.write(f"\nPROMPT: {prompt}\n")
    sys.stderr.write(f"Choices: {', '.join(choices)} (or 'none')\n")
    sys.stderr.write("Which skill fires? > ")
    sys.stderr.flush()
    answer = input().strip()
    return answer or "none"


def external_routing(responses: list[dict[str, Any]], prompt: str) -> str:
    for r in responses:
        if r.get("prompt") == prompt:
            return str(r.get("actual", "none"))
    return "none"


# v0.7.0: _tokens originally lived here; tokenizer relocated to _skill_io.tokens
# for reuse by search-skills.py. Import at top of file.


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run(
    entries: list[EvalEntry],
    mode: str,
    plugin_root: Path,
    external_responses: list[dict[str, Any]] | None = None,
    only_skill: str | None = None,
    operator_transcript: list[str] | None = None,
) -> list[EvalResult]:
    results: list[EvalResult] = []
    skill_choices = sorted({e.expected for e in entries if e.expected != "none"})
    transcript_idx = 0
    for entry in entries:
        if only_skill and entry.expected != only_skill:
            continue
        if mode == "static":
            actual = static_routing(entry.prompt, plugin_root)
        elif mode == "operator":
            if operator_transcript is not None:
                # v0.6.2: replay pre-canned answers from --operator-transcript.
                if transcript_idx < len(operator_transcript):
                    actual = operator_transcript[transcript_idx].strip() or "none"
                    transcript_idx += 1
                else:
                    actual = "none"  # transcript exhausted
            else:
                actual = operator_routing(entry.prompt, skill_choices)
        elif mode == "external":
            actual = external_routing(external_responses or [], entry.prompt)
        else:
            actual = "none"
        results.append(EvalResult(entry=entry, actual=actual, correct=actual == entry.expected))
    return results


def aggregate(results: list[EvalResult]) -> dict[str, SkillAccuracy]:
    by_skill: dict[str, SkillAccuracy] = {}
    for r in results:
        target = r.entry.expected
        if target not in by_skill:
            by_skill[target] = SkillAccuracy(skill=target)
        by_skill[target].total += 1
        if r.correct:
            by_skill[target].correct += 1
        else:
            by_skill[target].failures.append(r)
    return by_skill


def render_text(
    by_skill: dict[str, SkillAccuracy], threshold: float, mode: str, *, verbose: bool = False
) -> str:
    out = [f"# Routing-eval report (mode={mode}, threshold={int(threshold*100)}%)\n"]
    for skill in sorted(by_skill):
        acc = by_skill[skill]
        passed = acc.accuracy >= threshold
        mark = "✓" if passed else "✗"
        out.append(f"\n{mark} {skill}: {acc.correct}/{acc.total} = {acc.accuracy*100:.1f}%")
        if acc.failures:
            for f in acc.failures[:3]:
                out.append(f"    miss: {f.entry.prompt!r} → got {f.actual!r} (expected {f.entry.expected!r})")
                if verbose and f.entry.rationale:
                    # v0.6.1: surface the prompt's rationale on misses, so the
                    # operator can see WHY the prompt was authored to fire that
                    # skill. Useful when a miss is "static heuristic limitation"
                    # vs "real description-drift signal."
                    out.append(f"        rationale: {f.entry.rationale}")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--suite", type=Path, default=Path("scripts/tests/routing-eval.yaml"))
    parser.add_argument("--mode", choices=("static", "operator", "external"), default="static")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--skill", help="evaluate only the entries for this skill")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--verbose", action="store_true",
                        help="render EvalEntry.rationale on misses (text mode only)")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="for --mode external: read responses JSON from this file instead "
        "of stdin. Lets verify.sh exercise the mode without redirect tricks.",
    )
    parser.add_argument(
        "--operator-transcript",
        type=Path,
        default=None,
        help="for --mode operator: read pre-canned operator answers from this "
        "file (one answer per line, in prompt order). Lets verify.sh and "
        "fixtures replay an operator session deterministically.",
    )
    args = parser.parse_args(argv)

    if not args.suite.is_file():
        sys.stderr.write(f"error: suite not found: {args.suite}\n")
        return 2

    try:
        entries = load_suite(args.suite)
    except (ValueError, yaml.YAMLError) as e:
        sys.stderr.write(f"error parsing suite: {e}\n")
        return 2

    external_responses: list[dict[str, Any]] | None = None
    if args.mode == "external":
        # v0.6.2: --input overrides stdin so verify.sh + fixtures can drive
        # external mode without shell redirect tricks. Stdin remains the
        # default (production CI flow: real routing layer → JSON → stdin).
        try:
            if args.input is not None:
                if not args.input.is_file():
                    sys.stderr.write(f"error: --input file not found: {args.input}\n")
                    return 2
                external_responses = json.loads(args.input.read_text(encoding="utf-8"))
            else:
                external_responses = json.load(sys.stdin)
            if not isinstance(external_responses, list):
                raise ValueError("external responses must be a JSON list")
        except (json.JSONDecodeError, ValueError, OSError) as e:
            sys.stderr.write(f"error reading --mode external responses: {e}\n")
            return 2

    # v0.6.2: --operator-transcript replaces stdin for operator mode.
    # The transcript is a plain-text file with one answer per line, in
    # the order prompts are processed.
    operator_transcript: list[str] | None = None
    if args.mode == "operator" and args.operator_transcript is not None:
        if not args.operator_transcript.is_file():
            sys.stderr.write(f"error: --operator-transcript file not found: {args.operator_transcript}\n")
            return 2
        operator_transcript = args.operator_transcript.read_text(encoding="utf-8").splitlines()

    results = run(
        entries,
        args.mode,
        args.root,
        external_responses,
        args.skill,
        operator_transcript=operator_transcript,
    )
    by_skill = aggregate(results)

    if args.format == "json":
        print(json.dumps({
            "mode": args.mode,
            "threshold": args.threshold,
            "by_skill": {
                k: {"total": v.total, "correct": v.correct, "accuracy": v.accuracy}
                for k, v in by_skill.items()
            },
            "failures": [
                {"prompt": r.entry.prompt, "expected": r.entry.expected, "actual": r.actual}
                for r in results if not r.correct
            ],
        }, indent=2))
    else:
        print(render_text(by_skill, args.threshold, args.mode, verbose=args.verbose))

    any_below = any(acc.accuracy < args.threshold for acc in by_skill.values())
    return 1 if any_below else 0


if __name__ == "__main__":
    sys.exit(main())
