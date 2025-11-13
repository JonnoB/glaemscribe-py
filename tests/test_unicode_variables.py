"""Test Unicode variable implementation."""

import pytest
from src.glaemscribe.core.rule_group import RuleGroup
from src.glaemscribe.core.mode_enhanced import Mode


class TestUnicodeVariables:
    """Test Unicode variable functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mode = Mode("test_mode")
        self.mode.errors = []
        self.rule_group = RuleGroup(self.mode, "test_group")
        self.rule_group.finalize({})
    
    def test_builtin_unicode_variables_defined(self):
        """Test that built-in Unicode variables are defined."""
        builtin_vars = ["NBSP", "WJ", "ZWSP", "ZWNJ", "UNDERSCORE", "ASTERISK"]
        
        for var_name in builtin_vars:
            assert var_name in self.rule_group.vars
            assert self.rule_group.vars[var_name].value.startswith("{UNI_")
    
    def test_unicode_variable_resolution(self):
        """Test direct Unicode variable resolution."""
        test_cases = [
            ("{UNI_E000}", "\ue000"),  # Tengwar Tinco
            ("{UNI_E001}", "\ue001"),  # Tengwar Parma
            ("{UNI_A0}", "\u00a0"),    # Non-breaking space
            ("{UNI_5F}", "\u005f"),    # Underscore
        ]
        
        for unicode_var, expected_char in test_cases:
            result = self.rule_group.apply_vars(1, unicode_var, allow_unicode_vars=True)
            assert result == expected_char, f"Expected {expected_char}, got {result}"
    
    def test_unicode_variable_in_rule_context(self):
        """Test Unicode variables work in transcription rules."""
        # Add a rule that uses Unicode variables
        self.rule_group.finalize_rule(1, "{UNI_E000}", "{UNI_E001}")
        
        assert len(self.rule_group.rules) == 1
        rule = self.rule_group.rules[0]
        
        # Check that Unicode characters are in the source
        assert "\ue000" in str(rule.src_sheaf_chain)
    
    def test_invalid_unicode_hex_format(self):
        """Test invalid Unicode hex codes are rejected."""
        initial_error_count = len(self.mode.errors)
        
        result = self.rule_group.apply_vars(1, "{UNI_GARBAGE}", allow_unicode_vars=True)
        
        # Should return original string and add error
        assert result == "{UNI_GARBAGE}"
        assert len(self.mode.errors) > initial_error_count
    
    def test_unicode_out_of_range(self):
        """Test Unicode code points beyond limit are rejected."""
        initial_error_count = len(self.mode.errors)
        
        result = self.rule_group.apply_vars(1, "{UNI_110000}", allow_unicode_vars=True)
        
        # Should return original string and add error
        assert result == "{UNI_110000}"
        assert len(self.mode.errors) > initial_error_count
    
    def test_unicode_variable_scope_validation(self):
        """Test Unicode variables rejected in non-Unicode context."""
        result = self.rule_group.apply_vars(1, "{UNI_E000}", allow_unicode_vars=False)
        
        # Should return None when Unicode not allowed
        assert result is None
    
    def test_nested_unicode_variable_resolution(self):
        """Test Unicode variables in nested variable definitions."""
        # Define a variable that contains Unicode
        self.rule_group.add_var("TEST_VAR", "{UNI_E000}", False)
        
        # Use the variable in a rule
        result = self.rule_group.apply_vars(1, "{TEST_VAR}", allow_unicode_vars=True)
        
        assert result == "\ue000"
    
    @pytest.mark.regression
    def test_regression_empty_target_sheaf_chain(self):
        """REGRESSION: Unicode rules should not create empty target chains."""
        # This was a bug where Unicode variables created empty targets
        self.rule_group.finalize_rule(1, "{UNI_E000}", "normal_text")
        
        assert len(self.rule_group.rules) == 1
        rule = self.rule_group.rules[0]
        
        # Target should not be empty
        assert rule.dst_sheaf_chain.sheaves[0].fragments[0].value == "normal_text"
