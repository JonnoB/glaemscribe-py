#!/usr/bin/env python3
"""Test the charset building functionality."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_charset_building():
    """Test that charset building works correctly."""
    
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    if mode and hasattr(mode, 'rule_groups'):
        print(f"Rule groups: {len(mode.rule_groups)}")
        
        # Test charset building for each rule group
        for name, rg in mode.rule_groups.items():
            print(f"\nRule group: {name}")
            
            # Finalize the rule group (this should build the charset)
            rg.finalize({})
            
            print(f"  Variables: {len(rg.vars)}")
            print(f"  Rules: {len(rg.rules)}")
            print(f"  Input charset size: {len(rg.in_charset)}")
            
            # Show some sample characters from the charset
            charset_chars = list(rg.in_charset.keys())[:10]
            print(f"  Sample charset characters: {charset_chars}")
            
            # Verify that characters map to the correct rule group
            for char in charset_chars[:3]:
                mapped_group = rg.in_charset[char]
                print(f"    '{char}' -> {mapped_group.name}")
        
        # Test processor charset building
        print(f"\nTesting processor charset building...")
        try:
            mode.processor.finalize({})
            
            print(f"  Processor input charset size: {len(mode.processor.in_charset)}")
            
            # Show some sample characters from processor charset
            proc_chars = list(mode.processor.in_charset.keys())[:10]
            print(f"  Sample processor charset characters: {proc_chars}")
            
            # Verify character grouping
            for char in proc_chars[:3]:
                mapped_group = mode.processor.in_charset[char]
                print(f"    '{char}' -> {mapped_group.name}")
            
            # Test for character conflicts (should be none if working correctly)
            if mode.errors:
                print(f"  ⚠️  Errors found: {len(mode.errors)}")
                for error in mode.errors[:3]:
                    print(f"    {error}")
            else:
                print(f"  ✅ No character conflicts detected!")
            
        except Exception as e:
            print(f"  ✗ Processor error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_charset_building()
