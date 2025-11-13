#!/usr/bin/env python3
"""Test the Charset parser."""

from src.glaemscribe.parsers.charset_parser import CharsetParser

def test_simple_charset():
    """Test parsing a simple charset definition."""
    
    # Create a simple test charset file
    test_content = r"""
\version 1.0.0

\char 0x61 TINCO
\char 0x62 ANDO
\char 0x63 SULE

\beg virtual VOWEL_MARK
  \beg class VOWEL_XS
    TINCO
    ANDO
  \end
  \beg class VOWEL_S
    SULE
  \end
\end
"""
    
    # Write test file
    test_file = "/tmp/test_charset.cst"
    with open(test_file, "w") as f:
        f.write(test_content)
    
    # Parse it
    parser = CharsetParser()
    charset = parser.parse(test_file)
    
    print("Simple charset test:")
    print(f"Charset name: {charset.name}")
    print(f"Characters found: {len(charset.characters)}")
    print("Character mappings:")
    for name, value in charset.characters.items():
        print(f"  {name} -> '{value}'")
    
    print(f"Virtual characters: {len(charset.virtual_chars)}")
    for name, value in charset.virtual_chars.items():
        print(f"  {name} -> {value}")
    
    print(f"Errors: {len(parser.errors)}")
    for error in parser.errors[:10]:  # Show first 10 errors
        print(f"  {error}")
    
    # Clean up
    import os
    os.remove(test_file)
    
    return len(parser.errors) == 0

def test_real_charset():
    """Test parsing a real charset file."""
    
    parser = CharsetParser()
    
    try:
        charset = parser.parse("/home/jonno/glaemscribe-py/resources/glaemresources/charsets/tengwar_ds_annatar.cst")
        
        print(f"\nReal charset test:")
        print(f"Charset name: {charset.name}")
        print(f"Characters found: {len(charset.characters)}")
        print(f"Virtual characters: {len(charset.virtual_chars)}")
        print(f"Errors: {len(parser.errors)}")
        
        if parser.errors:
            print("First few errors:")
            for error in parser.errors[:5]:
                print(f"  {error}")
        
        # Show some character mappings
        print("\nSample character mappings:")
        for i, (name, value) in enumerate(list(charset.characters.items())[:10]):
            print(f"  {name} -> '{value}' (0x{ord(value):02x})")
        
        # Show some virtual characters
        if charset.virtual_chars:
            print("\nSample virtual characters:")
            for i, (name, value) in enumerate(list(charset.virtual_chars.items())[:5]):
                print(f"  {name} -> {value}")
        
        return len(parser.errors) == 0
        
    except Exception as e:
        print(f"Error parsing real charset: {e}")
        return False

if __name__ == "__main__":
    success1 = test_simple_charset()
    success2 = test_real_charset()
    
    if success1 and success2:
        print("\n✓ All charset parser tests passed!")
    else:
        print("\n✗ Some tests failed!")
