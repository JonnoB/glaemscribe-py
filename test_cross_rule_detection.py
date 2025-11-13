#!/usr/bin/env python3
"""Test cross rule detection in RuleGroup."""

from src.glaemscribe.core.rule_group import RuleGroup, RegexPatterns
from src.glaemscribe.core.mode_enhanced import Mode

def test_cross_rule_patterns():
    """Test that the regex patterns match cross rule syntax correctly."""
    
    print("=== Testing Cross Rule Regex Patterns ===")
    
    # Test the patterns directly
    cross_rule_pattern = RegexPatterns.CROSS_RULE_REGEXP
    normal_rule_pattern = RegexPatterns.RULE_REGEXP
    
    test_cases = [
        # Cross rule cases
        ("{V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}", True, "cross"),
        ("{V_D_WN}[{ARG_SL}] --> {__LWSX__} --> [{_ARG_SL_}]{_V_D_WN_}{_LWS_}", True, "cross"),
        ("{A}{B} --> identity --> target", True, "cross"),
        ("a --> 1,2 --> b", True, "cross"),
        
        # Normal rule cases
        ("a --> b", True, "normal"),
        ("{VAR} --> target", True, "normal"),
        ("source --> replacement", True, "normal"),
        
        # Non-rule cases
        ("{VAR} === value", False, "variable"),
        ("** comment", False, "comment"),
        ("", False, "empty"),
    ]
    
    for test_line, should_match, expected_type in test_cases:
        print(f"\nTesting: '{test_line}'")
        
        # Test cross rule pattern
        cross_match = cross_rule_pattern.match(test_line)
        normal_match = normal_rule_pattern.match(test_line)
        
        if expected_type == "cross":
            if cross_match:
                print(f"  ✅ Cross rule detected: source='{cross_match.group(1)}', schema='{cross_match.group(2)}', target='{cross_match.group(3)}'")
            else:
                print(f"  ❌ Expected cross rule but not detected")
        
        elif expected_type == "normal":
            if normal_match and not cross_match:
                print(f"  ✅ Normal rule detected: source='{normal_match.group(1)}', target='{normal_match.group(2)}'")
            else:
                print(f"  ❌ Expected normal rule but not detected correctly")
        
        else:
            if not cross_match and not normal_match:
                print(f"  ✅ Correctly ignored as {expected_type}")
            else:
                print(f"  ❌ Should have been ignored as {expected_type}")

def test_rule_group_detection():
    """Test that RuleGroup correctly detects and processes cross rules."""
    
    print("\n" + "="*60)
    print("=== Testing RuleGroup Cross Rule Detection ===")
    
    # Create a mock mode and rule group
    mode = Mode("test_mode")
    mode.errors = []
    rule_group = RuleGroup(mode, "test_group")
    
    # Test processing different rule types
    test_lines = [
        "{V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}",
        "a --> b", 
        "{VAR} === value",
        "{A}{B} --> identity --> target"
    ]
    
    for line in test_lines:
        print(f"\nProcessing: '{line}'")
        initial_rule_count = len(rule_group.rules)
        
        # Process the line
        rule_group._process_code_line(line, 1)
        
        final_rule_count = len(rule_group.rules)
        if final_rule_count > initial_rule_count:
            print(f"  ✅ Rule added (total: {final_rule_count})")
            # Check the last rule
            last_rule = rule_group.rules[-1]
            if hasattr(last_rule, 'cross_schema'):
                print(f"  ✅ Cross schema: {last_rule.cross_schema}")
            else:
                print(f"  ✅ Normal rule")
        else:
            print(f"  ⚪ No rule added (likely variable/comment)")

if __name__ == "__main__":
    test_cross_rule_patterns()
    test_rule_group_detection()
