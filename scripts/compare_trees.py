#!/usr/bin/env python3
"""Compare two Glaemscribe debug transcription trees.

This is a generalized version of compare_ai_lauri_trees.py that can
compare any two JSON trees produced by dump_debug_tree_mode.py (or
compatible scripts).

It reports differences per path in terms of:
- character
- replacement
- effective status

Optionally, you can filter to nodes whose replacement looks like it
contains Tengwar tehtar (heuristic substring match) to focus on
vowel/tehta placement issues.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List


def flatten_tree(tree: Dict[str, Any], path: str = "", result: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    """Flatten tree to a list of paths with their properties."""
    if result is None:
        result = []

    result.append(
        {
            "path": path,
            "character": tree["character"],
            "replacement": tree["replacement"],
            "effective": tree["effective"],
        }
    )

    for child in tree["children"]:
        flatten_tree(child, child["path"], result)

    return result


TEHTAR_HINTS = [
    "TEHTA",
    "A_TEHTA",
    "E_TEHTA",
    "I_TEHTA",
    "O_TEHTA",
    "U_TEHTA",
    "Y_TEHTA",
    "O_LOOP",
    "U_LOOP",
]


def looks_like_tehta_node(node: Dict[str, Any]) -> bool:
    """Heuristically decide if a node's replacement involves tehtar.

    This assumes the replacement string for debug trees contains
    symbolic names such as A_TEHTA, O_LOOP, etc., or that these names
    appear in some serialized form.
    """

    repl = node.get("replacement")
    if repl is None:
        return False

    if not isinstance(repl, str):
        repl = str(repl)

    return any(hint in repl for hint in TEHTAR_HINTS)


def compare_trees(py_path: Path, js_path: Path, only_tehtar: bool, show_limit: int) -> Path:
    with py_path.open("r", encoding="utf-8") as f:
        python_tree = json.load(f)

    with js_path.open("r", encoding="utf-8") as f:
        js_tree = json.load(f)

    python_nodes = {node["path"]: node for node in flatten_tree(python_tree)}
    js_nodes = {node["path"]: node for node in flatten_tree(js_tree)}

    all_paths = set(python_nodes.keys()) | set(js_nodes.keys())

    print(f"Python nodes: {len(python_nodes)}")
    print(f"JS nodes: {len(js_nodes)}")
    print(f"Total unique paths: {len(all_paths)}")
    print()

    differences = []
    for path in sorted(all_paths):
        py_node = python_nodes.get(path)
        js_node = js_nodes.get(path)

        if only_tehtar:
            # Skip if neither side looks like a tehta node
            if not ((py_node and looks_like_tehta_node(py_node)) or (js_node and looks_like_tehta_node(js_node))):
                continue

        if py_node and js_node:
            if (
                py_node["character"] != js_node["character"]
                or py_node["replacement"] != js_node["replacement"]
                or py_node["effective"] != js_node["effective"]
            ):
                differences.append({
                    "path": path,
                    "type": "different",
                    "python": py_node,
                    "js": js_node,
                })
        elif py_node:
            differences.append({
                "path": path,
                "type": "python_only",
                "python": py_node,
                "js": None,
            })
        else:
            differences.append({
                "path": path,
                "type": "js_only",
                "python": None,
                "js": js_node,
            })

    print(f"Found {len(differences)} differences")
    print()

    for i, diff in enumerate(differences[:show_limit]):
        print(f"{i + 1}. Path: {repr(diff['path'])}")
        print(f"   Type: {diff['type']}")

        if diff["type"] == "different":
            print(
                f"   Python: char={repr(diff['python']['character'])}, "
                f"repl={repr(diff['python']['replacement'])}, eff={diff['python']['effective']}"
            )
            print(
                f"   JS:     char={repr(diff['js']['character'])}, "
                f"repl={repr(diff['js']['replacement'])}, eff={diff['js']['effective']}"
            )
        elif diff["type"] == "python_only":
            print(
                f"   Python only: char={repr(diff['python']['character'])}, "
                f"repl={repr(diff['python']['replacement'])}, eff={diff['python']['effective']}"
            )
        else:
            print(
                f"   JS only: char={repr(diff['js']['character'])}, "
                f"repl={repr(diff['js']['replacement'])}, eff={diff['js']['effective']}"
            )
        print()

    # Save full diff alongside the input trees
    out_dir = py_path.parent
    base_name = f"debug_tree_diff_{py_path.stem}_vs_{js_path.stem}.txt"
    diff_path = out_dir / base_name

    with diff_path.open("w", encoding="utf-8") as f:
        for diff in differences:
            f.write(f"Path: {repr(diff['path'])}\n")
            f.write(f"Type: {diff['type']}\n")
            if diff["python"]:
                f.write(f"Python: {diff['python']}\n")
            if diff["js"]:
                f.write(f"JS: {diff['js']}\n")
            f.write("\n")

    print(f"All differences saved to {diff_path}")
    return diff_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two Glaemscribe debug transcription trees")
    parser.add_argument("py_tree", type=Path, help="Path to Python tree JSON")
    parser.add_argument("js_tree", type=Path, help="Path to JS/reference tree JSON")
    parser.add_argument(
        "--only-tehtar",
        action="store_true",
        help="Only consider nodes whose replacements look like they involve tehtar",
    )
    parser.add_argument(
        "--show-limit",
        type=int,
        default=40,
        help="Number of differences to print to stdout (default: 40)",
    )

    args = parser.parse_args()

    compare_trees(args.py_tree, args.js_tree, args.only_tehtar, args.show_limit)


if __name__ == "__main__":
    main()
