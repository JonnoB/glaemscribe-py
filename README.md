# Glaemscribe-py

A Python implementation of Glaemscribe for transcribing Tolkien's Elvish languages to Tengwar script using Unicode.

## Overview

Glaemscribe-py is a Python port focused on transcribing J.R.R. Tolkien's Elvish languages (Quenya and Sindarin) to Tengwar script. Unlike the original JavaScript Glaemscribe which uses font-specific encodings, this implementation outputs **Unicode characters** (Private Use Area) for greater font independence and modern compatibility.

### Key Features

- ✅ **Quenya transcription** - Full support for Classical Quenya to Tengwar
- ✅ **Sindarin transcription** - Full support for General Sindarin to Tengwar  
- ✅ **Unicode output** - Uses Unicode PUA characters (U+E000+) compatible with FreeMonoTengwar font
- ✅ **PNG rendering** - Built-in support for rendering transcriptions to images
- ✅ **Preprocessing** - Handles diacritics, substitutions, and special characters
- ✅ **Extensible architecture** - Mode system supports adding new transcription modes

### What's Different from Original Glaemscribe

- **Unicode-first**: Outputs Unicode characters instead of font-specific encodings
- **Font independence**: Works with any Unicode Tengwar font (tested with FreeMonoTengwar)
- **Python native**: Pure Python implementation with modern tooling (uv, pytest)
- **Focused scope**: Currently supports Elvish languages; architecture ready for expansion

## Supported Languages & Modes

### ✅ Fully Supported
- **Quenya** - `quenya-tengwar-classical.glaem`
- **Sindarin** - `sindarin-general.glaem`

### 🚧 Architecture Ready, Implementation Needed
The core architecture supports all transcription modes from the original Glaemscribe. The following can be added by adapting their mode files to use Unicode charsets:

- **English Tengwar** - Requires eSpeak NG integration for phonemic transcription
- **Other Tengwar modes** - Mode files exist, need Unicode charset adaptation
- **Cirth (Runes)** - Mode files exist, need Unicode charset adaptation  
- **Sarati** - Mode files exist, need Unicode charset adaptation
- **Other scripts** - Any mode from original Glaemscribe can be ported

The main work for adding new modes is:
1. Converting charset files from font-specific encoding to Unicode
2. For phonemic modes (like English), integrating required preprocessing tools

## About Glaemscribe

Glaemscribe is the definitive transcription engine for Tolkien's languages and writing systems. Originally created by Benjamin Babut (Talagan), it enables accurate transcription between languages and writing systems.

**Original Project**: [BenTalagan/glaemscribe](https://github.com/BenTalagan/glaemscribe)  
**Official Site**: [Glaemscrafu](https://glaemscrafu.jrrvf.com/english/glaemscribe.html)

## Installation

```bash
# Clone the repository
git clone https://github.com/JonnoB/glaemscribe-py.git
cd glaemscribe-py

# Install dependencies
pip install -e .[dev]
# or with uv
uv sync
```

## Quick Start

### Basic Transcription

```python
from src.glaemscribe.parsers.mode_parser import ModeParser

# Load a Quenya mode
parser = ModeParser()
mode = parser.parse('resources/glaemresources/modes/quenya-tengwar-classical.glaem')
mode.finalize({})

# Transcribe Quenya text
success, result, debug = mode.transcribe("Elen síla lúmenn' omentielvo")
if success:
    print(result)  # Outputs Unicode Tengwar characters (U+E000+ range)
```

### Rendering to PNG

```python
from PIL import Image, ImageDraw, ImageFont

# After transcribing (see above)
font = ImageFont.truetype("src/glaemscribe/fonts/FreeMonoTengwar.ttf", 48)
img = Image.new('RGB', (800, 100), color='white')
draw = ImageDraw.Draw(img)
draw.text((20, 20), result, font=font, fill='black')
img.save('output.png')
```

### Example: Namárië Poem

```python
poem = """Ai ! laurië lantar lassi súrinen ,
yéni únótimë ve rámar aldaron !
Yéni ve lintë yuldar avánier"""

success, result, debug = mode.transcribe(poem)
# Result contains full Tengwar transcription with proper diacritics
```

## Advanced Usage

### Using Different Charsets

```python
# Load with specific charset
from src.glaemscribe.parsers.charset_parser import CharsetParser

charset_parser = CharsetParser()
charset = charset_parser.parse("resources/glaemresources/charsets/tengwar_ds_sindarin.cst")

# Transcribe with charset
result = mode.transcribe("text", charset)
```

### Debug Mode

```python
from src.glaemscribe.core.mode_debug_context import ModeDebugContext

debug = ModeDebugContext()
success, result, debug = mode.transcribe("text")

# Access debug information
print(f"Processor output: {debug.processor_output}")
print(f"Post-processor output: {debug.postprocessor_output}")
```

## Testing

```bash
# Run all tests
uv run pytest
```

## Developer utilities

Helper scripts live under `scripts/` and are intended to be run as modules from the project root (so imports like `from src.glaemscribe...` work correctly).

### Render Namárië poem

Render the canonical Namárië transcription to PNGs in the `data/` directory:

```bash
uv run python -m scripts.render_poem
```

Outputs:

- `data/namarie_poem_transcription.png` – original lines + Tengwar
- `data/namarie_poem_tengwar_only.png` – Tengwar-only version

### English Ring Verse experiment (phonemic mode)

Experimental English Tengwar transcription of the Ring Verse (requires the phonemic `english-tengwar-espeak` mode; accuracy depends on future eSpeak NG integration):

```bash
uv run python -m scripts.test_english_ring_verse
```

Output:

- `data/ring_verse_english_tengwar.png`

### Debug transcription tree for "Ai ! laurië ..."

Build the Python transcription decision tree for debugging:

```bash
uv run python -m scripts.test_ai_lauri
```

This writes:

- `data/debug_tree_ai_lauri_python.json`

If you also place the JavaScript reference tree as:

- `data/debug_tree_ai_lauri_js.json`

you can compare them with:

```bash
uv run python -m scripts.compare_ai_lauri_trees
```

which produces:

- `data/debug_tree_ai_lauri_diff.txt`

### Unicode / Tengwar validation CLI

Validate a piece of text or a transcription result:

```bash
uv run python -m scripts.validate_unicode "some text"
uv run python -m scripts.validate_unicode --mode quenya-tengwar-classical "Elen síla lúmenn' omentielvo"
```

You can also list available modes:

```bash
uv run python -m scripts.validate_unicode --list-modes "dummy"
```

## Contributing

Contributions are welcome! When contributing:

1. **Maintain compatibility** with original Glaemscribe behavior
2. **Add tests** for new features
3. **Follow existing** code style and patterns
4. **Update documentation** as needed

### Adding New Modes

To add a new transcription mode:
1. Convert the charset file from font-specific encoding to Unicode (FreeMonoTengwar)
2. Update the mode file to reference the Unicode charset
3. Add tests to verify transcription accuracy
4. For phonemic modes, integrate required preprocessing tools (e.g., eSpeak NG)

## License

This port follows the same license as the original Glaemscribe project (GNU Affero General Public License v3.0).

## Acknowledgments

- **Benjamin Babut (Talagan)** - Original creator of Glaemscribe
- **The Tengwar and Quenya community** - For supporting the creation of the original Glaemscribe  

---

**Original Implementation**: [Ruby/JavaScript](https://github.com/BenTalagan/glaemscribe)  
