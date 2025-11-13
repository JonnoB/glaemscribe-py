#!/usr/bin/env python3
"""Test the core components."""

from src.glaemscribe.core.charset import Charset
from src.glaemscribe.core.mode import Mode

def test_basic_transcription():
    """Test basic transcription functionality."""
    
    # Create a simple charset using ASCII representations
    charset = Charset(
        name="test",
        version="1.0.0",
        characters={
            "a": "[A]",
            "b": "[B]",
            "c": "[C]",
            "vowel": "[VOWEL]"
        }
    )
    
    # Create a mode
    mode = Mode(
        name="test-mode",
        language="test",
        writing="test-script",
        human_name="Test Mode",
        authors="Test Author",
        version="1.0.0",
        supported_charsets={"test": charset},
        default_charset="test"
    )
    
    # Add some rules
    mode.add_rule(r"abc", "vowel", priority=2)
    mode.add_rule(r"\s+", " ", priority=1)  # Normalize spaces
    
    # Test cases
    tests = [
        ("a", "[A]"),
        ("b", "[B]"),
        ("c", "[C]"),
        ("abc", "[VOWEL]"),
        ("a b c", "[A] [B] [C]"),
    ]
    
    print("Testing core transcription:")
    all_passed = True
    
    for input_text, expected in tests:
        try:
            result = mode.transcribe(input_text)
            status = "✓" if result == expected else "✗"
            print(f"  {status} '{input_text}' -> '{result}' (expected: '{expected}')")
            if result != expected:
                all_passed = False
        except Exception as e:
            print(f"  ✗ '{input_text}' -> ERROR: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✓ All core tests passed!")
    else:
        print("\n✗ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    test_basic_transcription()
