"""Mapping from font-specific code points to Unicode Tengwar characters.

The charset files use font-specific encoding (e.g., code 60 for TELCO)
but we need to map these to actual Unicode Tengwar code points
in the Private Use Area (U+E000+).

This mapping uses the FTF/Everson Unicode standard, which is what
modern Tengwar fonts (Eldamar, Parmaite, Telcontar) actually support.
This ensures transcriptions are renderable with real fonts.
"""

# Mapping from font hex codes to Unicode Tengwar characters
# Using FTF/Everson standard (compatible with Eldamar, Parmaite, Telcontar fonts)
FONT_TO_UNICODE = {
    # Basic consonants (DS font codes -> FTF/Everson Unicode)
    0x31: '\ue000',  # TINCO (hex 31) -> U+E000
    0x32: '\ue004',  # ANDO (hex 32) -> U+E004  
    0x33: '\ue008',  # SULE/THULE (hex 33) -> U+E008
    0x34: '\ue00c',  # ANTO (hex 34) -> U+E00C
    0x35: '\ue010',  # NUMEN (hex 35) -> U+E010
    0x36: '\ue014',  # NOLDO (hex 36) -> U+E014
    0x37: '\ue018',  # ANNA (hex 37) -> U+E018
    0x38: '\ue01c',  # VILYA (hex 38) -> U+E01C
    0x60: '\ue02e',  # TELCO (hex 60) -> U+E02E
    0x3a: '\ue024',  # VALA (hex 3a) -> U+E024
    0x3b: '\ue028',  # YANTA (hex 3b) -> U+E028
    0x3c: '\ue02c',  # URE (hex 3c) -> U+E02C
    0x3d: '\ue030',  # ORE (hex 3d) -> U+E030
    
    # Row 2 consonants  
    0x41: '\ue001',  # PARMA (hex 41) -> U+E001
    0x42: '\ue005',  # UMBAR (hex 42) -> U+E005
    0x43: '\ue009',  # FORMEN (hex 43) -> U+E009
    0x44: '\ue00d',  # AMPA (hex 44) -> U+E00D
    0x45: '\ue011',  # ANGA (hex 45) -> U+E011
    0x46: '\ue015',  # UNQUE (hex 46) -> U+E015
    0x47: '\ue019',  # THINGOL (hex 47) -> U+E019
    0x48: '\ue01d',  # HARMA (hex 48) -> U+E01D
    0x49: '\ue021',  # HWESTA (hex 49) -> U+E021
    0x4a: '\ue025',  # QUESSE (hex 4a) -> U+E025
    0x4b: '\ue029',  # KERMA (hex 4b) -> U+E029
    0x4c: '\ue02d',  # ARA (hex 4c) -> U+E02D
    0x4d: '\ue031',  # SILME (hex 4d) -> U+E031
    0x4f: '\ue039',  # AIRE (hex 4f) -> U+E039
    
    # Row 3 consonants
    0x51: '\ue002',  # CALMA (hex 51) -> U+E002
    0x52: '\ue006',  # MALTA (hex 52) -> U+E006
    0x53: '\ue00a',  # NOLDOWA (hex 53) -> U+E00A
    0x54: '\ue00e',  # NWA (hex 54) -> U+E00E
    0x55: '\ue012',  # UNGWE (hex 55) -> U+E012
    0x56: '\ue016',  # GULMA (hex 56) -> U+E016
    0x57: '\ue01a',  # GWANN (hex 57) -> U+E01A
    0x58: '\ue01e',  # AHA (hex 58) -> U+E01E
    0x59: '\ue022',  # HWESTA (hex 59) -> U+E022
    0x5a: '\ue026',  # RUMA (hex 5a) -> U+E026
    0x5b: '\ue02a',  # VANTA (hex 5b) -> U+E02A
    0x5c: '\ue02e',  # ANNA_SINDARINWA (hex 5c) -> U+E02E
    0x5d: '\ue032',  # ESSE (hex 5d) -> U+E032
    0x5e: '\ue036',  # ESSE_NUQUERNA (hex 5e) -> U+E036
    0x5f: '\ue03a',  # OSTA (hex 5f) -> U+E03A
    
    # Row 4 consonants  
    0x61: '\ue003',  # QUENYA CALMA (hex 61) -> U+E003
    0x62: '\ue007',  # QUENYA MALTA (hex 62) -> U+E007
    0x63: '\ue00b',  # QUENYA NOLDOWA (hex 63) -> U+E00B
    0x64: '\ue00f',  # QUENYA NWA (hex 64) -> U+E00F
    0x65: '\ue013',  # QUENYA UNGWE (hex 65) -> U+E013
    0x66: '\ue017',  # QUENYA GULMA (hex 66) -> U+E017
    0x67: '\ue01b',  # QUENYA GWANN (hex 67) -> U+E01B
    0x68: '\ue01f',  # QUENYA AHA (hex 68) -> U+E01F
    0x69: '\ue023',  # QUENYA HWESTA (hex 69) -> U+E023
    0x6a: '\ue027',  # QUENYA RUMA (hex 6a) -> U+E027
    0x6b: '\ue02b',  # QUENYA VANTA (hex 6b) -> U+E02B
    0x6c: '\ue02f',  # QUENYA ANNA_SINDARINWA (hex 6c) -> U+E02F
    0x6d: '\ue033',  # QUENYA ESSE (hex 6d) -> U+E033
    0x6e: '\ue037',  # QUENYA ESSE_NUQUERNA (hex 6e) -> U+E037
    0x6f: '\ue03b',  # QUENYA OSTA (hex 6f) -> U+E03B
    
    # Special characters and punctuation
    0x20: '\u0020',  # SPACE -> space
    0xa0: '\u00a0',  # NBSP -> non-breaking space
    0x2c: '\ue053',  # COMMA -> comma mark
    0x2d: '\u2e31',  # PUNCT_DDOT -> double dot (U+2E31)
    0x2e: '\ue054',  # PERIOD -> period mark
    0x3d: '\u2e31',  # PUNCT_DOT -> dot (U+2E31)
    
    # Tehtar (vowels) - FTF/Everson standard mappings
    0x23: '\ue04a',  # O_TEHTA (hex 23) -> U+E04A
    0x24: '\ue046',  # E_TEHTA (hex 24) -> U+E046
    0x25: '\ue044',  # I_TEHTA (hex 25) -> U+E044
    0x26: '\ue04c',  # U_TEHTA (hex 26) -> U+E04C
    
    # Extended tehtar (different sizes) - Fixed mappings
    0x42: '\ue045',  # I_TEHTA_XS (hex 42) -> U+E045
    0x43: '\ue040',  # A_TEHTA_XS (hex 43) -> U+E040
    0x44: '\ue040',  # A_TEHTA_S (hex 44) -> U+E040
    0x45: '\ue040',  # A_TEHTA_L (hex 45) -> U+E040
    0x46: '\ue046',  # E_TEHTA_S (hex 46) -> U+E046
    
    # Additional tehtar size variants - Fixed mappings
    0x52: '\ue046',  # E_TEHTA_L -> U+E046
    0x56: '\ue046',  # E_TEHTA_XS -> U+E046
    0x54: '\ue044',  # I_TEHTA_L -> U+E044
    0x48: '\ue04a',  # O_TEHTA_S -> U+E04A
    0x4e: '\ue04a',  # O_TEHTA_XS -> U+E04A
    0x59: '\ue04a',  # O_TEHTA_L -> U+E04A
    0x5e: '\ue04a',  # O_TEHTA_XL -> U+E04A
    0x10c: '\ue04a', # O_TEHTA_DOUBLE_XL -> U+E04A
    0x4a: '\ue04c',  # U_TEHTA_S -> U+E04C
    0x4d: '\ue04c',  # U_TEHTA_XS -> U+E04C
    0x55: '\ue04c',  # U_TEHTA_L -> U+E04C
    0x1a4: '\ue04c', # U_TEHTA_DOUBLE_XL -> U+E04C
    0x1a5: '\ue04c', # U_TEHTA_DOUBLE_L -> U+E04C
    0x1a6: '\ue04c', # U_TEHTA_DOUBLE_S -> U+E04C
    0x1a7: '\ue04c', # U_TEHTA_DOUBLE_XS -> U+E04C
    
    # Critical fix: THSUP_TICK_INV mappings (A_TEHTA_CIRCUM variants)
    0xdc: '\ue040',  # THSUP_TICK_INV_XL (A_TEHTA_CIRCUM_XL) -> U+E040
    0xdd: '\ue040',  # THSUP_TICK_INV_L (A_TEHTA_CIRCUM_L) -> U+E040
    0xde: '\ue040',  # THSUP_TICK_INV_S (A_TEHTA_CIRCUM_S) -> U+E040
    0xdf: '\ue040',  # THSUP_TICK_INV_XS (A_TEHTA_CIRCUM_XS) -> U+E040
    
    # Map other common characters to reasonable Unicode values
    # These will need to be expanded based on actual usage
    0x22: '\ue066',  # DQUOTE_OPEN
    0x27: '\ue067',  # SQUOTE_OPEN
    0x2e: '\ue054',  # PUNCT_DOT
    
    # Fallback for unmapped characters - use Private Use Area
    # This ensures we get Unicode characters rather than ASCII
}

def map_font_code_to_unicode(code_point: int) -> str:
    """Map a font-specific code point to Unicode Tengwar character.
    
    Args:
        code_point: Font-specific code point from charset file
        
    Returns:
        Unicode Tengwar character, or fallback Unicode character
    """
    if code_point in FONT_TO_UNICODE:
        return FONT_TO_UNICODE[code_point]
    else:
        # Fallback: map to Private Use Area for unmapped font characters
        # This ensures we get Unicode characters rather than ASCII
        # Use a simple offset from E1000 for unmapped characters
        if 0x20 <= code_point <= 0x7F:  # Printable ASCII range
            return chr(0xE1000 + code_point)
        else:
            return chr(code_point)
