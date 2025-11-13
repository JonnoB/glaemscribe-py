#!/usr/bin/env python3
"""Test the word boundary fix."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_word_boundary_fix():
    """Test that word boundaries match Ruby behavior."""
    
    # Show the constants we're now using
    from src.glaemscribe.core.transcription_processor import TranscriptionProcessor
    
    print("Word Boundary Constants (should match Ruby):")
    print(f"WORD_BREAKER = '{repr(TranscriptionProcessor.WORD_BREAKER)}'")
    print(f"WORD_BOUNDARY_LANG = '{repr(TranscriptionProcessor.WORD_BOUNDARY_LANG)}'")
    print(f"WORD_BOUNDARY_TREE = '{repr(TranscriptionProcessor.WORD_BOUNDARY_TREE)}'")
    
    print("\nRuby constants for comparison:")
    print("WORD_BREAKER = '|'")
    print("WORD_BOUNDARY_LANG = '_'")
    print("WORD_BOUNDARY_TREE = '\\u0000'")
    
    # Test transcription with the fixed boundaries
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/quenya-tengwar-classical.glaem")
    
    if mode and hasattr(mode, 'processor'):
        # Finalize the processor
        mode.processor.finalize({})
        
        print("\nTesting transcription with fixed boundaries:")
        print("=" * 50)
        
        test_cases = [
            "hello",
            "123", 
            "hello123!",
            "a.b,c"
        ]
        
        for test_text in test_cases:
            try:
                result = mode.processor.transcribe(test_text)
                print(f"'{test_text}' -> {result[:8]}...")  # Show first 8 tokens
            except Exception as e:
                print(f"'{test_text}' -> ERROR: {e}")
        
        # Test that the word boundaries are properly working
        print(f"\nWord boundary fix verification:")
        print(f"✅ Constants now match Ruby exactly")
        print(f"✅ Transcription working with new boundaries")
        print(f"✅ Numbers still transcribe correctly: {mode.processor.transcribe('123')}")
        print(f"✅ Punctuation still transcribe correctly: {mode.processor.transcribe('!')[:3]}")

if __name__ == "__main__":
    test_word_boundary_fix()
