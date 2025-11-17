#!/usr/bin/env python3
"""Dump the transcription processor tree to JSON for cross-implementation diffing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from glaemscribe.parsers.mode_parser import ModeParser


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


def main():
    mode_path = ROOT / "resources" / "glaemresources" / "modes" / "quenya-tengwar-classical.glaem"
    out_path = ROOT / "debug_tree_python.json"

    parser = ModeParser()
    mode = parser.parse(str(mode_path))
    mode.processor.finalize({})

    tree_root = mode.processor.transcription_tree
    tree_dict = build_node_dict(tree_root)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(tree_dict, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
