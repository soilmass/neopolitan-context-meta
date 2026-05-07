#!/usr/bin/env python3
# pre-trigger build (v0.7.0); reassess when trigger fires per
# governance/SKILL-DISCOVERABILITY.md (50+ skills).
"""
search-skills.py — token-overlap search over skill descriptions, capabilities,
and tags. Per governance/SKILL-DISCOVERABILITY.md.

This is a v0.7.0 ahead-of-trigger build. The discoverability doc names the
build trigger as "50+ skills in one library." The library has 14. The script
ships now to give consumer libraries a canonical search implementation when
they reach the threshold; reassess at trigger time.

Ranking:
- exact tag match: 3.0× weight (matches `metadata.tags` directly)
- description token match: 1.0× weight
- Capabilities-Owned section token match: 0.5× weight (lower because the
  capability list often duplicates the description)

Exit codes:
  0  search ran (≥0 results)
  2  invocation problem (no skills, malformed query)

Usage:
  search-skills.py "audit drift"
  search-skills.py "router" --top 5
  search-skills.py "discoverability" --format json

Dependencies: PyYAML (via _skill_io) + stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from _skill_io import iter_live_skills, parse_skill, split_h2_bodies, tokens


@dataclass
class SearchHit:
    skill: str
    archetype: str
    score: float
    description_match: int
    capability_match: int
    tag_match: int
    tags: list[str]
    description_one_liner: str


def search(query: str, plugin_root: Path, top: int = 10) -> list[SearchHit]:
    q_tokens = tokens(query)
    if not q_tokens:
        return []
    hits: list[SearchHit] = []
    for skill_md in iter_live_skills(plugin_root):
        try:
            doc = parse_skill(skill_md)
        except ValueError:
            continue
        meta = doc.frontmatter.get("metadata") or {}
        archetype = str(meta.get("archetype", ""))
        tags = meta.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        tag_strs = [str(t) for t in tags if isinstance(t, str)]

        desc = str(doc.frontmatter.get("description") or "")
        desc_tokens = tokens(desc)
        sections = split_h2_bodies(doc.body)
        cap_text = sections.get("Capabilities Owned", "") or sections.get("Routing Table", "")
        cap_tokens = tokens(cap_text)

        # Tags match: count how many query tokens appear as tags (exact or
        # token-of-tag).
        tag_token_set: set[str] = set()
        for t in tag_strs:
            tag_token_set |= tokens(t)
        tag_hits = len(q_tokens & tag_token_set)
        desc_hits = len(q_tokens & desc_tokens)
        cap_hits = len(q_tokens & cap_tokens)
        score = 3.0 * tag_hits + 1.0 * desc_hits + 0.5 * cap_hits

        if score == 0:
            continue
        # Truncate description to a one-liner.
        one_liner = " ".join(desc.split())[:160]
        hits.append(
            SearchHit(
                skill=str(doc.frontmatter.get("name") or skill_md.parent.name),
                archetype=archetype,
                score=score,
                description_match=desc_hits,
                capability_match=cap_hits,
                tag_match=tag_hits,
                tags=tag_strs,
                description_one_liner=one_liner,
            )
        )
    hits.sort(key=lambda h: (-h.score, h.skill))
    return hits[:top]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("query", help="search query (free text)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not (args.root / "skills").is_dir():
        sys.stderr.write(f"error: no skills/ directory under {args.root}\n")
        return 2

    hits = search(args.query, args.root, top=args.top)

    if args.format == "json":
        print(json.dumps(
            [
                {
                    "skill": h.skill,
                    "archetype": h.archetype,
                    "score": h.score,
                    "tag_match": h.tag_match,
                    "description_match": h.description_match,
                    "capability_match": h.capability_match,
                    "tags": h.tags,
                    "description": h.description_one_liner,
                }
                for h in hits
            ],
            indent=2,
        ))
    else:
        if not hits:
            print(f"No skills matched query: {args.query!r}")
            return 0
        print(f"Top {len(hits)} match(es) for: {args.query!r}\n")
        for h in hits:
            tags_str = ",".join(h.tags) if h.tags else "<no tags>"
            print(f"  {h.skill} ({h.archetype})  score={h.score:.1f}  "
                  f"[tag={h.tag_match} desc={h.description_match} cap={h.capability_match}]  "
                  f"tags={tags_str}")
            print(f"    {h.description_one_liner}")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
