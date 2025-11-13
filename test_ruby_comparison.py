#!/usr/bin/env python3
"""Test that our implementation matches Ruby behavior exactly."""

from src.glaemscribe.core.rule_group import RuleGroup
from src.glaemscribe.core.mode_enhanced import Mode

def test_ruby_comparison():
    """Test cross rule processing matches Ruby exactly."""
    
    print("=== Ruby vs Python Comparison Test ===")
    
    # Create mode and rule group
    mode = Mode("test_mode")
    mode.errors = []
    rule_group = RuleGroup(mode, "test_group")
    
    # Test Case 1: Identity should become None
    print("\n--- Test Case 1: Identity Handling ---")
    print("Ruby: identity → cross = nil")
    print("Python: identity → cross_schema = None")
    
    # Add a variable for testing
    rule_group.add_var("TEST_VAR", "2,1")
    
    # Test identity rule through _process_code_line (matches Ruby flow)
    rule_group._process_code_line("[a][b] --> identity --> [a][b]", 1)
    
    if rule_group.rules:
        rule = rule_group.rules[-1]
        print(f"✅ Identity cross schema: {rule.cross_schema}")
        if rule.cross_schema is None:
            print("✅ Correctly converted to None (matches Ruby)")
        else:
            print(f"❌ Should be None, got: {rule.cross_schema}")
    
    # Test Case 2: Variable resolution
    print("\n--- Test Case 2: Variable Resolution ---")
    print("Ruby: {VAR} → resolved value → cross = resolved")
    print("Python: {VAR} → resolved value → cross_schema = resolved")
    
    rule_group._process_code_line("[a][b] --> {TEST_VAR} --> [b][a]", 2)
    
    if rule_group.rules:
        rule = rule_group.rules[-1]
        print(f"✅ Variable cross schema: {rule.cross_schema}")
        if rule.cross_schema == "2,1":
            print("✅ Correctly resolved variable (matches Ruby)")
        else:
            print(f"❌ Should be '2,1', got: {rule.cross_schema}")
    
    # Test Case 3: Numeric schema (should pass through)
    print("\n--- Test Case 3: Numeric Schema ---")
    print("Ruby: '2,1' → cross = '2,1'")
    print("Python: '2,1' → cross_schema = '2,1'")
    
    rule_group._process_code_line("[a][b] --> 2,1 --> [b][a]", 3)
    
    if rule_group.rules:
        rule = rule_group.rules[-1]
        print(f"✅ Numeric cross schema: {rule.cross_schema}")
        if rule.cross_schema == "2,1":
            print("✅ Correctly passed through (matches Ruby)")
        else:
            print(f"❌ Should be '2,1', got: {rule.cross_schema}")
    
    # Test Case 4: Invalid variable
    print("\n--- Test Case 4: Invalid Variable ---")
    print("Ruby: {NONEXISTENT} → error")
    print("Python: {NONEXISTENT} → error")
    
    initial_error_count = len(mode.errors)
    rule_group._process_code_line("[a][b] --> {NONEXISTENT} --> [b][a]", 4)
    
    final_error_count = len(mode.errors)
    if final_error_count > initial_error_count:
        print("✅ Correctly added error for invalid variable")
        print(f"Error: {mode.errors[-1]}")
    else:
        print("❌ Should have added error for invalid variable")
    
    print(f"\n📊 Summary:")
    print(f"Total rules created: {len(rule_group.rules)}")
    print(f"Total errors: {len(mode.errors)}")

if __name__ == "__main__":
    test_ruby_comparison()
