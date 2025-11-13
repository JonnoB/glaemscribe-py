#!/usr/bin/env python3
"""End-to-end test of cross rule implementation with real modes."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_english_tengwar_cross_rules():
    """Test cross rules in English Tengwar mode."""
    
    print("=== End-to-End Cross Rules Test ===")
    
    # Load the English Tengwar mode
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/english-tengwar-espeak.glaem")
    
    if not mode:
        print("❌ Failed to load English Tengwar mode")
        return
    
    print(f"✅ Loaded mode: {mode.name}")
    
    # Check for variables that should be used in cross rules
    print(f"\n📋 Mode Variables:")
    for rg_name, rg in mode.rule_groups.items():
        if hasattr(rg, 'vars') and rg.vars:
            print(f"  Rule group '{rg_name}': {list(rg.vars.keys())}")
            for var_name, var in rg.vars.items():
                print(f"    {var_name} = '{var.value}'")
    
    # Finalize the processor
    if hasattr(mode, 'processor') and mode.processor:
        print(f"\n🔧 Finalizing processor...")
        mode.processor.finalize({})
        
        print(f"✅ Processor finalized")
        print(f"✅ Rule groups: {list(mode.processor.rule_groups.keys())}")
        
        # Check for cross rules in all rule groups
        total_rules = 0
        cross_rules = 0
        
        for rg_name, rg in mode.processor.rule_groups.items():
            rules_count = len(rg.rules) if hasattr(rg, 'rules') else 0
            total_rules += rules_count
            
            # Check for cross schemas in rules
            if hasattr(rg, 'rules'):
                for rule in rg.rules:
                    if hasattr(rule, 'cross_schema') and rule.cross_schema is not None:
                        cross_rules += 1
                        print(f"  🎯 Cross rule in '{rg_name}': schema='{rule.cross_schema}'")
                        
                        # Show some sub-rules from this cross rule
                        print(f"    Sub-rules (first 3):")
                        for i, sub_rule in enumerate(rule.sub_rules[:3]):
                            print(f"      {i+1}. {sub_rule.src_combination} -> {sub_rule.dst_combination}")
        
        print(f"\n📊 Cross Rule Summary:")
        print(f"  Total rules: {total_rules}")
        print(f"  Cross rules: {cross_rules}")
        
        # Test transcription if we have cross rules
        if cross_rules > 0:
            print(f"\n🧪 Testing Transcription:")
            test_cases = [
                "test",
                "hello",
                "english"
            ]
            
            for test_text in test_cases:
                try:
                    result = mode.processor.transcribe(test_text)
                    print(f"  '{test_text}' -> {result[:10]}...")  # Show first 10 tokens
                except Exception as e:
                    print(f"  '{test_text}' -> ERROR: {e}")
        else:
            print("⚠️ No cross rules found - may be in macros/not implemented sections")
    
    print(f"\n🐛 Mode errors: {len(mode.errors)}")
    for error in mode.errors[:5]:  # Show first 5 errors
        print(f"  {error}")

def test_simple_cross_rule_mode():
    """Test with a simple mode that has cross rules."""
    
    print("\n" + "="*60)
    print("=== Simple Cross Rule Mode Test ===")
    
    # Create a simple test mode content
    test_mode_content = """
# Simple mode with cross rules
mode test_cross_rules
  language test
  writing test
  version 1.0

# Define variables for cross schemas
{CROSS_SWAP} === 2,1
{CROSS_IDENTITY} === identity

# Rule group with cross rules
group test_group
  # Normal rule
  a --> a
  
  # Cross rule with variable
  [a][b] --> {CROSS_SWAP} --> [b][a]
  
  # Cross rule with numeric schema
  [x][y][z] --> 3,1,2 --> [y][z][x]
  
  # Cross rule with identity (should become None)
  [p][q] --> {CROSS_IDENTITY} --> [p][q]
"""
    
    # Write test mode to temporary file
    import tempfile
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
                mode.processor.finalize({})
                
                print(f"✅ Processor finalized")
                
                # Check cross rules
                cross_rules_found = 0
                for rg_name, rg in mode.processor.rule_groups.items():
                    if hasattr(rg, 'rules'):
                        for rule in rg.rules:
                            if hasattr(rule, 'cross_schema') and rule.cross_schema is not None:
                                cross_rules_found += 1
                                print(f"  🎯 Cross rule: schema='{rule.cross_schema}'")
                                
                                # Show sub-rules
                                print(f"    Sub-rules:")
                                for i, sub_rule in enumerate(rule.sub_rules[:5]):
                                    print(f"      {i+1}. {sub_rule.src_combination} -> {sub_rule.dst_combination}")
                
                print(f"\n📊 Found {cross_rules_found} cross rules in test mode")
                
                if cross_rules_found > 0:
                    print("🎉 Cross rules are working end-to-end!")
                else:
                    print("❌ No cross rules found in test mode")
        else:
            print("❌ Failed to load test mode")
    
    finally:
        # Clean up temporary file
        import os
        os.unlink(temp_file)

if __name__ == "__main__":
    test_english_tengwar_cross_rules()
    test_simple_cross_rule_mode()
