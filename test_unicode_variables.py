#!/usr/bin/env python3
"""Test Unicode variable implementation."""

from src.glaemscribe.core.rule_group import RuleGroup
from src.glaemscribe.core.mode_enhanced import Mode

def test_unicode_variables():
    """Test that Unicode variables are processed correctly."""
    
    print("=== Unicode Variables Test ===")
    
    # Create mode and rule group
    mode = Mode("test_mode")
    mode.errors = []
    rule_group = RuleGroup(mode, "test_group")
    
    # Initialize the rule group (this adds built-in variables)
    rule_group.finalize({})
    
    # Test Case 1: Built-in Unicode variables
    print("\n--- Test Case 1: Built-in Unicode Variables ---")
    
    built_in_vars = ["NBSP", "WJ", "ZWSP", "ZWNJ", "UNDERSCORE", "ASTERISK"]
    
    for var_name in built_in_vars:
        if var_name in rule_group.vars:
            var_value = rule_group.vars[var_name].value
            print(f"✅ {var_name} = {var_value}")
        else:
            print(f"❌ {var_name} not found")
    
    # Test Case 2: Direct Unicode variable resolution
    print("\n--- Test Case 2: Direct Unicode Variable Resolution ---")
    
    test_cases = [
        ("{UNI_E000}", "Tengwar Tinco"),
        ("{UNI_E001}", "Tengwar Parma"), 
        ("{UNI_A0}", "Non-breaking space"),
        ("{UNI_5F}", "Underscore"),
    ]
    
    for unicode_var, description in test_cases:
        result = rule_group.apply_vars(1, unicode_var, allow_unicode_vars=True)
        if result and result != unicode_var:
            # Convert to hex representation for display
            hex_repr = f"\\u{ord(result):04x}"
            print(f"✅ {unicode_var} → {hex_repr} ({description})")
        else:
            print(f"❌ {unicode_var} → {result}")
    
    # Test Case 3: Unicode variable in rule context
    print("\n--- Test Case 3: Unicode Variable in Rule Context ---")
    
    # Add a rule that uses Unicode variables
    rule_group.finalize_rule(1, "{UNI_E000}", "{UNI_E001}")
    
    if rule_group.rules:
        rule = rule_group.rules[-1]
        print(f"✅ Rule created with Unicode characters")
        print(f"  Source sheaf chain: {rule.src_sheaf_chain}")
        print(f"  Target sheaf chain: {rule.dst_sheaf_chain}")
        
        # Check sub-rules
        if rule.sub_rules:
            sub_rule = rule.sub_rules[0]
            src_chars = [f"\\u{ord(c):04x}" for c in sub_rule.src_combination if c]
            dst_chars = [f"\\u{ord(c):04x}" for c in sub_rule.dst_combination if c]
            print(f"  Sub-rule: {src_chars} → {dst_chars}")
        else:
            print("  No sub-rules generated")
    else:
        print("❌ No rule created")
    
    # Test Case 4: Invalid Unicode variables
    print("\n--- Test Case 4: Invalid Unicode Variables ---")
    
    invalid_cases = [
        ("{UNI_GARBAGE}", "Invalid hex"),
        ("{UNI_110000}", "Out of range"),
    ]
    
    initial_error_count = len(mode.errors)
    
    for invalid_var, description in invalid_cases:
        result = rule_group.apply_vars(1, invalid_var, allow_unicode_vars=True)
        if result == invalid_var:
            print(f"✅ {invalid_var} correctly not resolved ({description})")
        else:
            print(f"❌ {invalid_var} unexpectedly resolved to: {result}")
    
    final_error_count = len(mode.errors)
    if final_error_count > initial_error_count:
        print(f"✅ Errors added for invalid Unicode: {final_error_count - initial_error_count}")
    
    # Test Case 5: Unicode variable scope validation
    print("\n--- Test Case 5: Unicode Variable Scope Validation ---")
    
    # Unicode variables should not be allowed in all contexts
    result = rule_group.apply_vars(1, "{UNI_E000}", allow_unicode_vars=False)
    if result is None:
        print("✅ Unicode variable correctly rejected in non-Unicode context")
    else:
        print(f"❌ Unicode variable incorrectly accepted: {result}")
    
    print(f"\n📊 Summary:")
    print(f"  Variables defined: {len(rule_group.vars)}")
    print(f"  Rules created: {len(rule_group.rules)}")
    print(f"  Total errors: {len(mode.errors)}")

if __name__ == "__main__":
    test_unicode_variables()
