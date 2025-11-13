#!/usr/bin/env python3
"""Test English Tengwar mode with macro system to unlock cross rules."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_english_tengwar_with_macros():
    """Test that English Tengwar cross rules now work through macros."""
    
    print("=== English Tengwar Macro Test ===")
    
    # Load the English Tengwar mode
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/english-tengwar-espeak.glaem")
    
    if not mode:
        print("❌ Failed to load English Tengwar mode")
        return
    
    print(f"✅ Loaded mode: {mode.name}")
    
    # Finalize the processor
    if hasattr(mode, 'processor') and mode.processor:
        print("🔧 Finalizing processor...")
        mode.processor.finalize({})
        
        print(f"✅ Processor finalized")
        print(f"✅ Rule groups: {list(mode.processor.rule_groups.keys())}")
        
        # Check for macros and cross rules
        total_macros = 0
        total_rules = 0
        cross_rules = 0
        
        for rg_name, rg in mode.processor.rule_groups.items():
            rules_count = len(rg.rules) if hasattr(rg, 'rules') else 0
            macros_count = len(rg.macros) if hasattr(rg, 'macros') else 0
            total_rules += rules_count
            total_macros += macros_count
            
            print(f"\n📋 Rule group: {rg_name}")
            print(f"  Macros: {macros_count}")
            print(f"  Rules: {rules_count}")
            
            # Check for cross schemas in rules
            if hasattr(rg, 'rules'):
                for rule in rg.rules:
                    if hasattr(rule, 'cross_schema') and rule.cross_schema is not None:
                        cross_rules += 1
                        print(f"  🎯 Cross rule found: schema='{rule.cross_schema}'")
                        
                        # Show some sub-rules from this cross rule
                        print(f"    Sub-rules (first 3):")
                        for i, sub_rule in enumerate(rule.sub_rules[:3]):
                            print(f"      {i+1}. {sub_rule.src_combination} -> {sub_rule.dst_combination}")
            
            # Show macro names if any
            if macros_count > 0:
                macro_names = list(rg.macros.keys())
                print(f"  Macro names: {macro_names[:5]}...")  # Show first 5
        
        print(f"\n📊 Cross Rule Unlock Summary:")
        print(f"  Total macros: {total_macros}")
        print(f"  Total rules: {total_rules}")
        print(f"  Cross rules: {cross_rules}")
        
        if cross_rules > 0:
            print("🎉 SUCCESS: Cross rules are now unlocked through macros!")
            
            # Test transcription if we have cross rules
            print(f"\n🧪 Testing Transcription:")
            test_cases = [
                "test",
                "hello", 
                "english"
            ]
            
            for test_text in test_cases:
                try:
                    result = mode.processor.transcribe(test_text)
                    print(f"  '{test_text}' -> {result[:20]}...")  # Show first 20 chars
                except Exception as e:
                    print(f"  '{test_text}' -> ERROR: {e}")
        else:
            print("⚠️ No cross rules found yet - may need further investigation")
    
    print(f"\n🐛 Mode errors: {len(mode.errors)}")
    for error in mode.errors[:5]:  # Show first 5 errors
        print(f"  {error}")
    
    print(f"\n📝 Parser errors: {len(parser.errors)}")
    for error in parser.errors[:5]:  # Show first 5 errors
        print(f"  {error}")

if __name__ == "__main__":
    test_english_tengwar_with_macros()
