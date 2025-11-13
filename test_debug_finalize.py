#!/usr/bin/env python3
"""Debug the finalize process."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def debug_finalize():
    """Debug the finalize process."""
    
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    # Test the litteral rule group specifically
    litteral_rg = mode.rule_groups['litteral']
    
    print(f"Litteral rule group before finalize:")
    print(f"  Terms: {len(litteral_rg.root_code_block.terms)}")
    print(f"  Vars: {len(litteral_rg.vars)}")
    
    # Debug the first CodeLinesTerm
    first_term = litteral_rg.root_code_block.terms[0]
    print(f"  First term type: {type(first_term).__name__}")
    if hasattr(first_term, 'code_lines'):
        print(f"  First term code lines: {len(first_term.code_lines)}")
        for i, code_line in enumerate(first_term.code_lines[:5]):
            print(f"    Line {i}: '{code_line.expression}'")
            
            # Test the regex
            from src.glaemscribe.core.rule_group import RegexPatterns
            match = RegexPatterns.VAR_DECL_REGEXP.match(code_line.expression.strip())
            if match:
                print(f"      ✓ MATCH: var='{match.group(1)}' value='{match.group(2)}'")
            else:
                print(f"      ✗ NO MATCH")
    
    # Call finalize and check result
    print(f"\nCalling finalize...")
    litteral_rg.finalize({})
    
    print(f"Litteral rule group after finalize:")
    print(f"  Vars: {len(litteral_rg.vars)}")
    print(f"  Rules: {len(litteral_rg.rules)}")
    
    if litteral_rg.vars:
        print(f"  Variable names: {list(litteral_rg.vars.keys())}")

if __name__ == "__main__":
    debug_finalize()
