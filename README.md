# Glaemscribe Python

A Python implementation of the Glaemscribe transcription engine for converting text between writing systems (e.g., Quenya to Tengwar).

## Current Status

This is a minimal working implementation that demonstrates the core transcription functionality. It includes:

- **Core transcription engine** with regex-based rule processing
- **Character set management** for mapping between character names and actual characters
- **Mode system** for defining different transcription rules
- **Simple API** for easy use

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd glaemscribe-py

# Install dependencies (optional, for development)
pip install -e .[dev]
```

## Quick Start

```python
from glaemscribe import Glaemscribe, Charset, Mode

# Create a Glaemscribe instance
glaem = Glaemscribe()

# Create a character set
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

# Create a transcription mode
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
glaem.add_mode(mode)

# Transcribe text
result = glaem.transcribe("abc", "quenya-tengwar")
print(result)  # Output: ˚¸·
```

## Architecture

```
src/glaemscribe/
├── __init__.py      # Main package exports
├── api.py           # Public API (Glaemscribe class)
└── core/
    ├── __init__.py
    ├── charset.py   # Charset class for character mappings
    └── mode.py      # Mode and TranscriptionRule classes
```

## Testing

Run the test suite:

```bash
python3 test_core.py   # Test core components
python3 test_api.py    # Test the API
```

## Next Steps

To make this a complete implementation:

1. **Add parsers** for `.glaem` and `.cst` files from the original Glaemscribe
2. **Implement resource manager** for loading modes and charsets from files
3. **Add more sophisticated rule processing** (context-aware rules, etc.)
4. **Include real Tengwar fonts and character sets**
5. **Add comprehensive tests** with pytest
6. **Create CLI interface** for command-line use

## Compatibility

This implementation aims to be compatible with the existing Glaemscribe resource files (`.glaem` modes and `.cst` charsets) from the original project.
