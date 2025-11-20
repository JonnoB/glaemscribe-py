#!/usr/bin/env python3
"""Dump a Glaemscribe mode's transcription tree to JSON.

Generalized version of dump_debug_tree.py that works for any mode and
writes to a user-specified output path. Intended for cross-implementation
comparison and debugging (e.g., Python vs JS trees).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glaemscribe.parsers.mode_parser import ModeParser
from glaemscribe.resources import get_mode_path


def build_node_dict(node, path: str = ""):
    children = []
    for char in sorted(node.siblings.keys()):
        child = node.siblings[char]
        children.append(build_node_dict(child, path + (char or "")))

    return {
        "character": node.character if node.character is not None else "ROOT",
        "path": path,
        "replacement": node.replacement,
        "effective": node.is_effective(),
        "child_count": len(children),
        "children": children,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump a mode's transcription tree to JSON")
    parser.add_argument("mode", help="Mode name, e.g. 'quenya-tengwar-classical' or 'sindarin-tengwar-general_use'")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output JSON path (default: data/debug_tree_<mode>_python.json)",
    )

    args = parser.parse_args()

    mode_name = args.mode

    if args.output is not None:
        out_path = args.output
    else:
        safe_mode = mode_name.replace("/", "_").replace(" ", "_")
        out_path = ROOT / "data" / f"debug_tree_{safe_mode}_python.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    mode_path = get_mode_path(mode_name)

    parser_obj = ModeParser()
    mode = parser_obj.parse(str(mode_path))
    mode.processor.finalize({})

    tree_root = mode.processor.transcription_tree
    tree_dict = build_node_dict(tree_root)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(tree_dict, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
