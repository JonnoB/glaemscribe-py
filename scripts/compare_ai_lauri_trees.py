#!/usr/bin/env python3
"""Compare Python and JS debug trees for 'Ai ! laurië lantar lassi súrinen ,' phrase."""

import json
import os

def flatten_tree(tree, path="", result=None):
    """Flatten tree to a list of paths with their properties."""
    if result is None:
        result = []
    
    # Add current node
    result.append({
        'path': path,
        'character': tree['character'],
        'replacement': tree['replacement'],
        'effective': tree['effective']
    })
    
    # Recursively add children
    for child in tree['children']:
        flatten_tree(child, child['path'], result)
    
    return result

def compare_trees():
    # Load the trees
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    py_path = os.path.join(data_dir, 'debug_tree_ai_lauri_python.json')
    js_path = os.path.join(data_dir, 'debug_tree_ai_lauri_js.json')

    with open(py_path, 'r') as f:
        python_tree = json.load(f)
    
    with open(js_path, 'r') as f:
        js_tree = json.load(f)
    
    # Flatten both trees
    python_nodes = {node['path']: node for node in flatten_tree(python_tree)}
    js_nodes = {node['path']: node for node in flatten_tree(js_tree)}
    
    # Find all paths
    all_paths = set(python_nodes.keys()) | set(js_nodes.keys())
    
    print(f"Python nodes: {len(python_nodes)}")
    print(f"JS nodes: {len(js_nodes)}")
    print(f"Total unique paths: {len(all_paths)}")
    print()
    
    # Find differences
    differences = []
    for path in sorted(all_paths):
        py_node = python_nodes.get(path)
        js_node = js_nodes.get(path)
        
        if py_node and js_node:
            # Both exist, check for differences
            if (py_node['character'] != js_node['character'] or
                py_node['replacement'] != js_node['replacement'] or
                py_node['effective'] != js_node['effective']):
                differences.append({
                    'path': path,
                    'type': 'different',
                    'python': py_node,
                    'js': js_node
                })
        elif py_node:
            differences.append({
                'path': path,
                'type': 'python_only',
                'python': py_node,
                'js': None
            })
        else:
            differences.append({
                'path': path,
                'type': 'js_only',
                'python': None,
                'js': js_node
            })
    
    print(f"Found {len(differences)} differences")
    print()
    
    # Show first 20 differences
    for i, diff in enumerate(differences[:20]):
        print(f"{i+1}. Path: {repr(diff['path'])}")
        print(f"   Type: {diff['type']}")
        
        if diff['type'] == 'different':
            print(f"   Python: char={repr(diff['python']['character'])}, repl={repr(diff['python']['replacement'])}, eff={diff['python']['effective']}")
            print(f"   JS:     char={repr(diff['js']['character'])}, repl={repr(diff['js']['replacement'])}, eff={diff['js']['effective']}")
        elif diff['type'] == 'python_only':
            print(f"   Python only: char={repr(diff['python']['character'])}, repl={repr(diff['python']['replacement'])}, eff={diff['python']['effective']}")
        else:
            print(f"   JS only: char={repr(diff['js']['character'])}, repl={repr(diff['js']['replacement'])}, eff={diff['js']['effective']}")
        print()
    
    # Save differences to file
    os.makedirs(data_dir, exist_ok=True)
    diff_path = os.path.join(data_dir, 'debug_tree_ai_lauri_diff.txt')
    with open(diff_path, 'w') as f:
        for diff in differences:
            f.write(f"Path: {repr(diff['path'])}\n")
            f.write(f"Type: {diff['type']}\n")
            if diff['python']:
                f.write(f"Python: {diff['python']}\n")
            if diff['js']:
                f.write(f"JS: {diff['js']}\n")
            f.write("\n")
    
    print(f"All differences saved to {diff_path}")

if __name__ == "__main__":
    compare_trees()
