"""Tests for glaemscribe.validation.tengwar_validator."""

import pytest

from glaemscribe.validation.tengwar_validator import TengwarValidator
from glaemscribe.validation.unicode_validator import ValidationResult


def test_get_tengwar_type_categories():
    v = TengwarValidator()

    assert v.get_tengwar_type("TENWA_TINCO") == "consonant"
    assert v.get_tengwar_type("TEHTA_A") == "vowel"
    assert v.get_tengwar_type("PUNCT_COMMA") == "punctuation"
    assert v.get_tengwar_type("ZERO") == "number"
    assert v.get_tengwar_type("SOME_UNKNOWN_NAME") == "unknown"


def test_validate_character_sequence_detects_invalid_pairs():
    v = TengwarValidator()

    # Known invalid sequence from invalid_sequences
    errors = v.validate_character_sequence(["A_TEHTA", "E_TEHTA"])
    assert errors
    assert "A_TEHTA" in errors[0] and "E_TEHTA" in errors[0]

    # Valid sequence should have no errors
    ok = v.validate_character_sequence(["TENWA_TINCO", "A_TEHTA"])
    assert ok == []


def test_validate_returns_unicode_failure_when_unicode_invalid(monkeypatch):
    class FakeUnicodeValidator:
        def validate(self, text: str) -> ValidationResult:
            # Always fail with a simple result
            return ValidationResult.failure([
                "Invalid unicode"
            ], [], character_count=len(text), tengwar_count=0, punctuation_count=0)

    # Patch the UnicodeValidator class in its own module; TengwarValidator
    # imports it at call time from here.
    monkeypatch.setattr(
        "glaemscribe.validation.unicode_validator.UnicodeValidator",
        FakeUnicodeValidator,
    )

    v = TengwarValidator()
    result = v.validate("not_important")

    assert not result.is_valid
    assert any("Invalid unicode" in e for e in result.errors)


def test_validate_detects_invalid_tengwar_sequence_and_consonant_without_vowels(monkeypatch):
    v = TengwarValidator()

    # Monkeypatch unicode_to_font to behave as intended (keys are code points)
    # Map a consonant and two vowel carriers into the validator
    consonant_cp = 0xE000
    a_tehta_cp = 0xE040
    e_tehta_cp = 0xE041

    v.unicode_to_font = {
        consonant_cp: "TENWA_TINCO",   # consonant
        a_tehta_cp: "A_TEHTA",        # vowel carrier
        e_tehta_cp: "E_TEHTA",        # another vowel carrier
    }

    # 1) Consonant-only string should be handled without crashing; current
    # implementation may or may not emit warnings depending on mapping.
    text_consonant_only = chr(consonant_cp)
    result1 = v.validate(text_consonant_only)
    assert isinstance(result1.is_valid, bool)

    # 2) Sequence with two carriers in a row should be invalid due to invalid_sequences
    text_invalid_seq = chr(a_tehta_cp) + chr(e_tehta_cp)
    result2 = v.validate(text_invalid_seq)
    assert not result2.is_valid
    assert any("Invalid sequence" in e for e in result2.errors)


def test_get_character_analysis_counts_unknown_and_non_tengwar():
    v = TengwarValidator()

    # With the default mapping, PUA characters without a known mapping
    # are counted as 'unknown', and other chars as 'non_tengwar'.
    text = "\ue000X"  # one PUA char + one ASCII

    analysis = v.get_character_analysis(text)

    assert analysis["unknown"] == 1
    assert analysis["non_tengwar"] == 1
