"""Focused tests for glaemscribe.core.rule_group.

These tests avoid full mode parsing and transcription, and instead
validate small, self-contained pieces of RuleGroup behavior.
"""

import types

from glaemscribe.core.rule_group import RuleGroup
from glaemscribe.core.transcription_processor import TranscriptionProcessor


class _FakeMode:
    """Minimal stand-in for a Mode object, capturing errors."""

    def __init__(self):
        self.errors = []


def test_apply_vars_basic_and_nested():
    mode = _FakeMode()
    rg = RuleGroup(mode, name="test")

    # Simple var
    rg.add_var("FOO", "bar")

    # Nested: {OUTER} -> {INNER}, {INNER} -> baz
    rg.add_var("OUTER", "{INNER}")
    rg.add_var("INNER", "baz")

    # Simple replacement
    result = rg.apply_vars(line=1, string="{FOO} qux")
    assert result == "bar qux"

    # Nested should resolve in multiple passes
    nested = rg.apply_vars(line=2, string="{OUTER}")
    assert nested == "baz"

    # No new errors expected
    assert mode.errors == []


def test_apply_vars_unknown_and_unicode_vars():
    mode = _FakeMode()
    rg = RuleGroup(mode, name="test")

    # Unknown variable should record an error; implementation may
    # return the original string or None, we only assert error recording.
    result = rg.apply_vars(line=10, string="{NOPE}")
    assert any("failed to evaluate variable" in str(e) for e in mode.errors)

    # Clear errors and test unicode vars
    mode.errors.clear()

    # When unicode vars are allowed, they should not raise errors
    mode.errors.clear()
    s = rg.apply_vars(line=11, string="{UNI_00A0}", allow_unicode_vars=True)
    assert mode.errors == []

    # When not allowed, using a unicode var should record an error
    s2 = rg.apply_vars(line=12, string="{UNI_00A0}", allow_unicode_vars=False)
    assert any("making wrong use of unicode variable" in str(e) for e in mode.errors)


def _make_fake_rule_with_src_combination(src_combination):
    """Create a minimal fake rule object with the required shape."""
    sub_rule = types.SimpleNamespace(src_combination=src_combination)
    rule = types.SimpleNamespace(sub_rules=[sub_rule])
    return rule


def test_build_input_charset_basic_and_ignores_special_chars():
    mode = _FakeMode()
    rg = RuleGroup(mode, name="default")
    rg.in_charset = {}

    # Rule with combination containing regular chars and special markers
    src_combination = [
        "AB",  # normal characters
        TranscriptionProcessor.WORD_BREAKER,
        "C",
        TranscriptionProcessor.WORD_BOUNDARY_TREE,
    ]
    rg.rules = [_make_fake_rule_with_src_combination(src_combination)]

    rg._build_input_charset()

    # Normal characters should be present
    assert rg.in_charset["A"] is rg
    assert rg.in_charset["B"] is rg
    assert rg.in_charset["C"] is rg

    # Special markers should not appear
    assert TranscriptionProcessor.WORD_BREAKER not in rg.in_charset
    assert TranscriptionProcessor.WORD_BOUNDARY_TREE not in rg.in_charset


def test_build_input_charset_numbers_group_guard():
    mode = _FakeMode()
    rg = RuleGroup(mode, name="numbers")
    rg.in_charset = {}

    src_combination = ["AB"]  # would normally add 'A' and 'B'
    rg.rules = [_make_fake_rule_with_src_combination(src_combination)]

    rg._build_input_charset()

    # Guard: numbers group should not capture A/B
    assert "A" not in rg.in_charset
    assert "B" not in rg.in_charset
