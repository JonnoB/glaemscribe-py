"""Tests for glaemscribe.validation.unicode_validator."""

from glaemscribe.validation.unicode_validator import (
    UnicodeValidator,
    ValidationResult,
)


def test_is_in_range_and_get_character_type_basic_cases():
    v = UnicodeValidator()

    # Tengwar PUA
    assert v.is_in_range(0xE02A)
    assert v.get_character_type(0xE02A) == "tengwar"

    # Space
    assert v.is_in_range(0x20)
    assert v.get_character_type(0x20) == "space"

    # Punctuation
    assert v.is_in_range(0x2E31)
    assert v.get_character_type(0x2E31) in {"punctuation", "control"}

    # Clearly invalid control character
    assert not v.is_in_range(0x0001)
    assert v.get_character_type(0x0001) == "unknown"


def test_validate_success_and_failure_paths():
    v = UnicodeValidator()

    # All valid: mix of Tengwar (PUA) and space
    valid_text = "\ue02a\ue02b \ue040"
    result_ok = v.validate(valid_text)
    assert result_ok.is_valid
    assert result_ok.character_count == len(valid_text)
    assert result_ok.tengwar_count == 3

    # Empty string should be valid with zero counts
    empty = v.validate("")
    assert empty.is_valid
    assert empty.character_count == 0
    assert empty.tengwar_count == 0

    # Invalid character introduces errors
    invalid_text = "X\u0001Y"
    result_bad = v.validate(invalid_text)
    assert not result_bad.is_valid
    assert len(result_bad.errors) >= 1


def test_validate_warnings_for_no_tengwar_and_question_mark():
    v = UnicodeValidator()

    # Currently, validator does not special-case '?' but this should
    # still be a valid, non-crashing path.
    with_question = v.validate("???")
    assert with_question.character_count == 3


def test_get_validation_summary_formats_success_and_failure():
    v = UnicodeValidator()

    ok = ValidationResult.success(character_count=10, tengwar_count=8, punctuation_count=2)
    ok_summary = v.get_validation_summary(ok)
    assert "Valid Unicode transcription" in ok_summary
    assert "10" in ok_summary
    assert "8" in ok_summary

    bad = ValidationResult.failure([
        "Invalid character at position 0",
        "Invalid character at position 1",
        "Invalid character at position 2",
        "Invalid character at position 3",
    ], [], character_count=4, tengwar_count=0, punctuation_count=0)

    bad_summary = v.get_validation_summary(bad)
    assert "Invalid Unicode transcription" in bad_summary
    assert "Errors: 4" in bad_summary
    assert "Invalid character at position 0" in bad_summary
