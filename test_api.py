#!/usr/bin/env python3
"""Test the Glaemscribe API."""

from src.glaemscribe import Glaemscribe, Charset, Mode

def test_api():
    """Test the Glaemscribe API."""
    
    # Create the Glaemscribe instance
    glaem = Glaemscribe()
    
    # Create and add a charset
    charset = Charset(
        name="tengwar-annatar",
        version="1.0.0",
        characters={
            "a": "˚",
            "b": "·",
            "c": "¸",
            "vowel": "˚¸·"
        }
    )
    glaem.add_charset(charset)
    
    # Create and add a mode
    mode = Mode(
        name="quenya-tengwar",
        language="quenya",
        writing="tengwar",
        human_name="Quenya to Tengwar",
        authors="Test",
        version="1.0.0",
        supported_charsets={"tengwar-annatar": charset},
        default_charset="tengwar-annatar"
    )
    
    # Add transcription rules
    mode.add_rule(r"abc", "vowel", priority=2)
    mode.add_rule(r"\s+", " ", priority=1)
    
    glaem.add_mode(mode)
    
    # Test the API
    print("Available modes:", glaem.list_modes())
    print("Available charsets:", glaem.list_charsets())
    
    # Test transcription
    test_cases = [
        ("a", "˚"),
        ("b", "·"),
        ("c", "¸"),
        ("abc", "˚¸·"),
        ("hello world", "hello world"),  # No rules for this
    ]
    
    print("\nTesting API transcription:")
    all_passed = True
    
    for input_text, expected in test_cases:
        try:
            result = glaem.transcribe(input_text, "quenya-tengwar")
            status = "✓" if result == expected else "✗"
            print(f"  {status} '{input_text}' -> '{result}' (expected: '{expected}')")
            if result != expected:
                all_passed = False
        except Exception as e:
            print(f"  ✗ '{input_text}' -> ERROR: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✓ All API tests passed!")
    else:
        print("\n✗ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    test_api()
