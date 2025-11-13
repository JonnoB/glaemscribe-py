#!/usr/bin/env python3
"""Test Unicode Tengwar charset support."""

from src.glaemscribe.parsers.mode_parser import ModeParser

def test_unicode_tengwar_charset():
    """Test that Unicode Tengwar charsets work correctly."""
    
    print("=== Unicode Tengwar Charset Test ===")
    
    # Load a mode that uses Unicode Tengwar charset
    parser = ModeParser()
    mode = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/modes/raw-tengwar.glaem")
    
    if not mode:
        print("❌ Failed to load raw-tengwar mode")
        return
    
    print(f"✅ Loaded mode: {mode.name}")
    
    # Finalize the processor
    if hasattr(mode, 'processor') and mode.processor:
        mode.processor.finalize({})
        print(f"✅ Processor finalized")
        
        # Check if Unicode charset is working
        print(f"\n📋 Mode information:")
        print(f"  Language: {getattr(mode, 'language', 'Unknown')}")
        print(f"  Writing: {getattr(mode, 'writing', 'Unknown')}")
        
        # Test transcription with Unicode characters
        print(f"\n🧪 Testing Unicode transcription:")
        test_cases = [
            "tinco",  # Should map to Unicode Tengwar tinco
            "parma",  # Should map to Unicode Tengwar parma
        ]
        
        for test_text in test_cases:
            try:
                result = mode.processor.transcribe(test_text)
                print(f"  '{test_text}' → {result}")
                
                # Show Unicode characters in result
                if result:
                    unicode_chars = []
                    for char in result:
                        if ord(char) >= 0xE000:  # Private Use Area
                            unicode_chars.append(f"\\u{ord(char):04x}")
                        else:
                            unicode_chars.append(char)
                    print(f"    Unicode: {''.join(unicode_chars)}")
                    
            except Exception as e:
                print(f"  '{test_text}' → ERROR: {e}")
    
    print(f"\n🐛 Mode errors: {len(mode.errors)}")
    for error in mode.errors[:3]:  # Show first 3 errors
        print(f"  {error}")

if __name__ == "__main__":
    test_unicode_tengwar_charset()
