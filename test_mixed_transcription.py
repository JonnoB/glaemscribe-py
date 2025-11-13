#!/usr/bin/env python3
"""Test mixed character transcription using charset building."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_mixed_transcription():
    """Test transcription with mixed character types."""
    
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    if mode and hasattr(mode, 'processor'):
        # Finalize the processor
        mode.processor.finalize({})
        
        # Test mixed character strings
        test_cases = [
            "hello",        # Letters only
            "123",          # Numbers only
            "hello123",     # Letters + numbers
            "hello!",       # Letters + punctuation
            "hello123!",    # Letters + numbers + punctuation
            "a.b,c",        # Letters with punctuation
        ]
        
        print("Testing mixed character transcription:")
        print("=" * 50)
        
        for test_text in test_cases:
            try:
                result = mode.processor.transcribe(test_text)
                print(f"'{test_text}' -> {result[:10]}...")  # Show first 10 tokens
            except Exception as e:
                print(f"'{test_text}' -> ERROR: {e}")
        
        print("\nCharacter grouping verification:")
        print("=" * 50)
        
        # Show which rule group handles each character type
        test_chars = ['a', '1', '.', '!']
        for char in test_chars:
            group = mode.processor.in_charset.get(char)
            if group:
                print(f"'{char}' is handled by '{group.name}' rule group")
            else:
                print(f"'{char}' is not handled by any rule group")

if __name__ == "__main__":
    test_mixed_transcription()
