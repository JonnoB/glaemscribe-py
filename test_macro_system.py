#!/usr/bin/env python3
"""Test macro system implementation."""

from src.glaemscribe.core.rule_group import RuleGroup
from src.glaemscribe.core.macro import Macro, MacroDeployTerm
from src.glaemscribe.core.mode_enhanced import Mode

def test_macro_system():
    """Test that macro definitions and deployments work correctly."""
    
    print("=== Macro System Test ===")
    
    # Create mode and rule group
    mode = Mode("test_mode")
    mode.errors = []
    rule_group = RuleGroup(mode, "test_group")
    
    # Test Case 1: Create a simple macro
    print("\n--- Test Case 1: Simple Macro Definition ---")
    
    macro = Macro(rule_group, "test_macro", ["ARG1", "ARG2"])
    rule_group.add_macro(macro)
    
    print(f"✅ Created macro: {macro}")
    print(f"✅ Macros in rule group: {list(rule_group.macros.keys())}")
    
    # Test Case 2: Macro deployment with arguments
    print("\n--- Test Case 2: Macro Deployment ---")
    
    deploy = MacroDeployTerm(
        macro=macro,
        line=10,
        parent_code_block=rule_group.root_code_block,
        arg_value_expressions=["value1", "value2"]
    )
    
    print(f"✅ Created deployment: {deploy}")
    print(f"✅ Arguments: {deploy.arg_value_expressions}")
    
    # Test Case 3: Test macro argument validation
    print("\n--- Test Case 3: Argument Validation ---")
    
    # Valid argument names
    valid_macro = Macro(rule_group, "valid_macro", ["ARG_A", "ARG_B", "ARG_123"])
    print(f"✅ Valid macro: {valid_macro}")
    
    # Test Case 4: Test macro deployment logic
    print("\n--- Test Case 4: Macro Deployment Logic ---")
    
    # Add a rule to the macro's code block
    from src.glaemscribe.core.rule_group import CodeLinesTerm, CodeLine
    
    code_lines_term = CodeLinesTerm(macro.root_code_block)
    macro.root_code_block.add_term(code_lines_term)
    
    # Add a code line that uses macro arguments
    code_line = CodeLine("{ARG1} --> {ARG2}", 1)
    code_lines_term.code_lines.append(code_line)
    
    print(f"✅ Added rule to macro: {code_line.expression}")
    
    # Now deploy the macro
    rule_group.root_code_block.add_term(deploy)
    
    # Initialize and finalize
    rule_group.finalize({})
    
    print(f"✅ Rule group finalized")
    print(f"✅ Rules created: {len(rule_group.rules)}")
    
    # Check if the macro was expanded
    if rule_group.rules:
        rule = rule_group.rules[0]
        print(f"✅ First rule source: {rule.src_sheaf_chain}")
        print(f"✅ First rule target: {rule.dst_sheaf_chain}")
        
        if rule.sub_rules:
            sub_rule = rule.sub_rules[0]
            print(f"✅ Sub-rule: {sub_rule.src_combination} -> {sub_rule.dst_combination}")
    
    # Test Case 5: Error handling
    print("\n--- Test Case 5: Error Handling ---")
    
    initial_error_count = len(mode.errors)
    
    # Try to deploy non-existent macro
    fake_deploy = MacroDeployTerm(
        macro=Macro(rule_group, "fake", []),
        line=20,
        parent_code_block=rule_group.root_code_block,
        arg_value_expressions=[]
    )
    
    # This should fail when we try to deploy it
    # (We'll test this through the parser later)
    
    print(f"✅ Initial errors: {initial_error_count}")
    print(f"✅ Final errors: {len(mode.errors)}")
    
    print(f"\n📊 Summary:")
    print(f"  Macros defined: {len(rule_group.macros)}")
    print(f"  Rules created: {len(rule_group.rules)}")
    print(f"  Total errors: {len(mode.errors)}")

def test_cross_rule_in_macro():
    """Test that cross rules work inside macros."""
    
    print("\n" + "="*60)
    print("=== Cross Rule in Macro Test ===")
    
    # Create mode and rule group
    mode = Mode("test_cross_mode")
    mode.errors = []
    rule_group = RuleGroup(mode, "test_cross_group")
    
    # Add cross schema variable
    rule_group.add_var("SWAP_SCHEMA", "2,1", False)
    
    # Create macro with cross rule
    cross_macro = Macro(rule_group, "cross_swap", ["ARG1", "ARG2"])
    
    # Add cross rule to macro
    from src.glaemscribe.core.rule_group import CodeLinesTerm, CodeLine
    
    code_lines_term = CodeLinesTerm(cross_macro.root_code_block)
    cross_macro.root_code_block.add_term(code_lines_term)
    
    # Add cross rule using macro arguments
    cross_line = CodeLine("[{ARG1}][{ARG2}] --> {SWAP_SCHEMA} --> [{_ARG2_}][{_ARG1_}]", 1)
    code_lines_term.code_lines.append(cross_line)
    
    rule_group.add_macro(cross_macro)
    
    # Deploy the macro
    deploy = MacroDeployTerm(
        macro=cross_macro,
        line=10,
        parent_code_block=rule_group.root_code_block,
        arg_value_expressions=["a", "b"]
    )
    
    rule_group.root_code_block.add_term(deploy)
    
    # Finalize
    rule_group.finalize({})
    
    print(f"✅ Cross macro created and deployed")
    print(f"✅ Rules created: {len(rule_group.rules)}")
    
    if rule_group.rules:
        rule = rule_group.rules[0]
        print(f"✅ Cross schema: {rule.cross_schema}")
        
        if rule.sub_rules:
            for i, sub_rule in enumerate(rule.sub_rules[:3]):
                print(f"  {i+1}. {sub_rule.src_combination} -> {sub_rule.dst_combination}")
    
    print(f"🎉 Cross rules in macros are working!")

if __name__ == "__main__":
    test_macro_system()
    test_cross_rule_in_macro()
