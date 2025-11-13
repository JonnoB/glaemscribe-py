#!/usr/bin/env python3
"""Debug what rule group names are being used."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def debug_rule_names():
    """Debug the rule group names."""
    
    parser = ModeParser()
    
    # Monkey patch to add debug
    original_extract_rule_groups = parser._extract_processor_rules
    
    def debug_extract_rule_groups(doc):
        print("DEBUG: Finding all processor.rules elements...")
        
        # Find all processor.rules elements
        processor_nodes = doc.root_node.gpath("processor")
        if processor_nodes:
            processor_node = processor_nodes[0]
            rules_nodes = processor_node.gpath("rules")
            
            print(f"DEBUG: Found {len(rules_nodes)} rules elements:")
            
            for i, rules_element in enumerate(rules_nodes):
                print(f"  Rules element {i}:")
                print(f"    Name: {rules_element.name}")
                print(f"    Args: {rules_element.args}")
                if rules_element.args:
                    print(f"    First arg (rule group name): '{rules_element.args[0]}'")
        
        return original_extract_rule_groups(doc)
    
    parser._extract_processor_rules = debug_extract_rule_groups
    
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    print(f"\nFinal rule groups: {list(mode.rule_groups.keys())}")

if __name__ == "__main__":
    debug_rule_names()
