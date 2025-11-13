#!/usr/bin/env python3
"""Test simple cross rule implementation."""

from src.glaemscribe.parsers.mode_parser import ModeParser
import tempfile
import os

def test_simple_cross_rules():
    """Test simple cross rules with a minimal mode."""
    
    print("=== Simple Cross Rules Test ===")
    
    # Create a simple test mode content
    test_mode_content = """
mode test_cross
  language test
  writing test
  version 1.0

group test_group
  # Variable for cross schema
  {SWAP} === 2,1
  
  # Cross rule with variable
  [a][b] --> {SWAP} --> [b][a]
  
  # Cross rule with numeric schema
  [x][y] --> 2,1 --> [y][x]
  
  # Normal rule
  c --> c
"""
    
    # Write test mode to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.glaem', delete=False) as f:
        f.write(test_mode_content)
        temp_file = f.name
    
    try:
        # Parse the test mode
        parser = ModeParser()
        mode = parser.parse(temp_file)
        
        if mode:
            print(f"✅ Loaded test mode: {mode.name}")
            
            # Finalize processor
            if hasattr(mode, 'processor') and mode.processor:
                print("🔧 Finalizing processor...")
                mode.processor.finalize({})
                
                print("✅ Processor finalized")
                
                # Check for cross rules
                cross_rules_found = 0
                for rg_name, rg in mode.processor.rule_groups.items():
                    print(f"\n📋 Rule group: {rg_name}")
                    print(f"  Variables: {list(rg.vars.keys())}")
                    print(f"  Rules: {len(rg.rules)}")
                    
                    for rule in rg.rules:
                        if hasattr(rule, 'cross_schema'):
                            if rule.cross_schema is not None:
                                cross_rules_found += 1
                                print(f"  🎯 Cross rule: schema='{rule.cross_schema}'")
                                
                                # Show sub-rules
                                print(f"    Sub-rules:")
                                for i, sub_rule in enumerate(rule.sub_rules[:3]):
                                    print(f"      {i+1}. {sub_rule.src_combination} -> {sub_rule.dst_combination}")
                            else:
                                print(f"  ⚪ Normal rule (identity processed)")
                        else:
                            print(f"  ⚪ Normal rule (no cross schema)")
                
                print(f"\n📊 Summary:")
                print(f"  Cross rules found: {cross_rules_found}")
                print(f"  Mode errors: {len(mode.errors)}")
                
                if cross_rules_found > 0:
                    print("🎉 Cross rules are working!")
                    
                    # Test transcription
                    print(f"\n🧪 Testing transcription:")
                    test_cases = ["ab", "xy", "c"]
                    for test_text in test_cases:
                        try:
                            result = mode.processor.transcribe(test_text)
                            print(f"  '{test_text}' -> {result}")
                        except Exception as e:
                            print(f"  '{test_text}' -> ERROR: {e}")
                else:
                    print("❌ No cross rules found")
        else:
            print("❌ Failed to load test mode")
    
    finally:
        # Clean up temporary file
        os.unlink(temp_file)

if __name__ == "__main__":
    test_simple_cross_rules()
