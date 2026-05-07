#!/usr/bin/env python3
"""
dependency-graph.py — produce a textual or DOT-format dependency graph
of the SNAPSHOT.lock `depends_on` edges.

Per GOVERNANCE.md §"Dependency Model", the canonical dependency mechanism
is `SNAPSHOT.lock` `depends_on:` per-skill entries. This script visualizes
that graph for impact analysis and review.

Output formats:
  - text:    indented tree (default), human-readable
  - dot:     Graphviz DOT format (pipe to `dot -Tpng -o graph.png`)
  - json:    structured edges + nodes for further processing

Exit codes:
  0  graph produced
  2  invocation problem (file missing, malformed YAML, cycle detected)

Usage:
  dependency-graph.py
  dependency-graph.py --snapshot SNAPSHOT.lock --format dot
  dependency-graph.py --skill family-bootstrap --format text   # subgraph

Dependencies: PyYAML + stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("error: PyYAML not installed. `pip install pyyaml`\n")
    sys.exit(2)


@dataclass
class Edge:
    src: str
    dst: str
    pinned_version: str  # the @<version> from `dst@<version>` form


@dataclass
class Graph:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)  # name → entry
    edges: list[Edge] = field(default_factory=list)


def load_graph(snapshot_path: Path) -> Graph:
    data = yaml.safe_load(snapshot_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{snapshot_path}: snapshot must be a YAML mapping")
    skills = data.get("skills") or {}
    g = Graph()
    for name, entry in skills.items():
        if not isinstance(entry, dict):
            continue
        g.nodes[name] = entry
        for dep in entry.get("depends_on") or []:
            if not isinstance(dep, str) or "@" not in dep:
                continue
            dst, version = dep.split("@", 1)
            g.edges.append(Edge(src=name, dst=dst, pinned_version=version))
    return g


def detect_cycles(g: Graph) -> list[list[str]]:
    """Find any cycles in the dependency graph (DFS with three-color)."""
    cycles: list[list[str]] = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in g.nodes}
    parent: dict[str, str | None] = {n: None for n in g.nodes}

    def dfs(node: str) -> None:
        color[node] = GRAY
        for e in g.edges:
            if e.src != node:
                continue
            if e.dst not in color:
                continue
            if color[e.dst] == GRAY:
                cycle: list[str] = [e.dst]
                cur: str | None = node
                while cur is not None and cur != e.dst:
                    cycle.append(cur)
                    cur = parent.get(cur)
                cycle.append(e.dst)
                cycles.append(list(reversed(cycle)))
            elif color[e.dst] == WHITE:
                parent[e.dst] = node
                dfs(e.dst)
        color[node] = BLACK

    for n in g.nodes:
        if color[n] == WHITE:
            dfs(n)
    return cycles


def render_text(g: Graph, focus: str | None = None) -> str:
    out: list[str] = []
    out.append(f"# Dependency graph ({len(g.nodes)} skills, {len(g.edges)} edges)")
    out.append("")

    deps_by_src: dict[str, list[Edge]] = {n: [] for n in g.nodes}
    for e in g.edges:
        deps_by_src.setdefault(e.src, []).append(e)

    deps_by_dst: dict[str, list[Edge]] = {n: [] for n in g.nodes}
    for e in g.edges:
        deps_by_dst.setdefault(e.dst, []).append(e)

    nodes_to_show = [focus] if focus else sorted(g.nodes)
    for name in nodes_to_show:
        if name not in g.nodes:
            out.append(f"  (skill {name!r} not in snapshot)")
            continue
        entry = g.nodes[name]
        out.append(f"## {name} v{entry.get('version', '?')} ({entry.get('archetype', '?')})")
        deps = deps_by_src.get(name, [])
        if deps:
            out.append("  Depends on:")
            for e in sorted(deps, key=lambda x: x.dst):
                out.append(f"    → {e.dst} @ {e.pinned_version}")
        rev = deps_by_dst.get(name, [])
        if rev:
            out.append("  Depended on by:")
            for e in sorted(rev, key=lambda x: x.src):
                out.append(f"    ← {e.src}")
        if not deps and not rev:
            out.append("  (no dependencies)")
        out.append("")

    cycles = detect_cycles(g)
    if cycles:
        out.append("## ⚠️ Cycles detected")
        for c in cycles:
            out.append(f"  {' → '.join(c)}")
    return "\n".join(out)


def render_dot(g: Graph) -> str:
    lines = [
        'digraph "snapshot_depends_on" {',
        '  rankdir=LR;',
        '  node [shape=box, fontname="Helvetica"];',
    ]
    for name, entry in g.nodes.items():
        archetype = entry.get("archetype", "?")
        version = entry.get("version", "?")
        color = {
            "atom": "lightblue",
            "tool": "lightgreen",
            "router": "lightyellow",
            "orchestrator": "lightpink",
            "policy": "lavender",
        }.get(archetype, "white")
        lines.append(f'  "{name}" [label="{name}\\nv{version}\\n({archetype})", style=filled, fillcolor={color}];')
    for e in g.edges:
        lines.append(f'  "{e.src}" -> "{e.dst}" [label="@{e.pinned_version}"];')
    lines.append("}")
    return "\n".join(lines)


def render_json(g: Graph) -> str:
    return json.dumps({
        "nodes": [
            {"name": n, "version": e.get("version"), "archetype": e.get("archetype"), "health": e.get("health")}
            for n, e in g.nodes.items()
        ],
        "edges": [{"src": e.src, "dst": e.dst, "pinned_version": e.pinned_version} for e in g.edges],
        "cycles": detect_cycles(g),
    }, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--snapshot", type=Path, default=Path("SNAPSHOT.lock"))
    parser.add_argument("--skill", help="focus on a single skill's neighborhood")
    parser.add_argument("--format", choices=("text", "dot", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.snapshot.is_file():
        sys.stderr.write(f"error: snapshot not found: {args.snapshot}\n")
        return 2

    try:
        g = load_graph(args.snapshot)
    except (ValueError, yaml.YAMLError) as e:
        sys.stderr.write(f"error parsing snapshot: {e}\n")
        return 2

    if args.format == "dot":
        print(render_dot(g))
    elif args.format == "json":
        print(render_json(g))
    else:
        print(render_text(g, focus=args.skill))
    return 0


if __name__ == "__main__":
    sys.exit(main())
