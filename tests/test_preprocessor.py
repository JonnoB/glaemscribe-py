"""Tests for glaemscribe.core.preprocessor."""

import pytest

from glaemscribe.core.preprocessor import (
    SubstituteOperator,
    RxSubstituteOperator,
    Preprocessor,
)


def test_substitute_operator_simple_replacement():
    op = SubstituteOperator("ë", "e")

    result = op.apply("Eärendil and Eëar")

    assert "ë" not in result
    assert result == "Eärendil and Eear"


def test_rxsubstitute_operator_regex_replacement():
    op = RxSubstituteOperator(r"[āâ]", "á")

    result = op.apply("tēl ā, têl â")

    assert "ā" not in result and "â" not in result
    assert "á" in result


def test_rxsubstitute_invalid_pattern_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        RxSubstituteOperator("(", "x", line=42)

    msg = str(excinfo.value)
    assert "Invalid regex pattern" in msg
    assert "42" in msg


def test_preprocessor_apply_and_clear():
    pre = Preprocessor()
    pre.add_substitute("ë", "e")
    pre.add_rxsubstitute(r"[āâ]", "á")

    text = "Eärendil ë, têl ā, têl â"
    processed = pre.apply(text)

    assert "ë" not in processed
    assert "ā" not in processed and "â" not in processed
    assert "á" in processed

    pre.clear()
    assert "0 operators" in str(pre)
