#!/usr/bin/env python3
"""Debug what's being passed to traverse_if_tree."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def debug_traverse_call():
    """Debug the traverse_if_tree call."""
    
    parser = ModeParser()
    
    # Monkey patch to add debug
    original_traverse_if_tree = parser._process_rule_group_content
    
    def debug_process_rule_group_content(element, rule_group):
        print(f"DEBUG: _process_rule_group_content called with element: {element.name}")
        print(f"DEBUG: Element has {len(element.children)} children")
        
        # Show first few children
        for i, child in enumerate(element.children[:5]):
            print(f"  Child {i}: {child.name} (type: {child.type})")
        
        return original_traverse_if_tree(element, rule_group)
    
    parser._process_rule_group_content = debug_process_rule_group_content
    
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    print(f"\nFinal result: {mode.rule_groups['rules'].root_code_block.terms}")

if __name__ == "__main__":
    debug_traverse_call()
