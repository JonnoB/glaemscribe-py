#!/usr/bin/env python3
"""Debug the litteral rule group charset."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_litteral_charset():
    """Debug what characters the litteral rule group actually handles."""
    
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    if mode and 'litteral' in mode.rule_groups:
        rg = mode.rule_groups['litteral']
        rg.finalize({})
        
        print(f"Litteral rule group charset ({len(rg.in_charset)} characters):")
        print("=" * 50)
        
        # Sort and display all characters
        chars = sorted(rg.in_charset.keys())
        for i, char in enumerate(chars):
            print(f"  '{char}'", end='')
            if (i + 1) % 10 == 0:
                print()  # New line every 10 characters
        
        print("\n\nFirst few rules in litteral group:")
        print("=" * 50)
        
        for i, rule in enumerate(rg.rules[:5]):
            print(f"Rule {i}: {len(rule.sub_rules)} sub-rules")
            for j, sub_rule in enumerate(rule.sub_rules[:3]):
                src = "".join(sub_rule.src_combination)
                dst = " ".join(sub_rule.dst_combination)
                print(f"  '{src}' -> {dst}")

if __name__ == "__main__":
    test_litteral_charset()
