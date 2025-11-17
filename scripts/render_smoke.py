#!/usr/bin/env python3
"""Render Glaemscribe output with the shared Tengwar CSUR font.

Matches the smoke test used in the `tengwar` (Rust) bindings so results can be
compared side-by-side.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from glaemscribe.parsers.mode_parser import ModeParser

try:
    from tengwar.font import extract_bundled_fonts
except ImportError:  # pragma: no cover - optional dependency
    extract_bundled_fonts = None

DEFAULT_TEXT = "Elen síla lúmenn’ omentielvo"
DEFAULT_MODE_FILE = Path(
    "resources/glaemresources/modes/quenya-tengwar-classical.glaem"
)
DEFAULT_SIZE = 72
DEFAULT_OUTPUT = Path("glaemscribe_sample.png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", default=DEFAULT_TEXT, help="Plain text to transliterate")
    parser.add_argument(
        "--mode-path",
        type=Path,
        default=DEFAULT_MODE_FILE,
        help="Path to a .glaem mode file (default: Quenya Tengwar Classical)",
    )
    parser.add_argument("--font-path", type=Path, help="Path to a .ttf font. Defaults to the bundled CSUR font from the `tengwar` package if available.")
    parser.add_argument("--font-size", type=int, default=DEFAULT_SIZE, help="Font size in points")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output PNG path")
    return parser.parse_args()


def load_font(font_path: Path | None) -> Path:
    if font_path:
        return font_path
    if extract_bundled_fonts is None:
        raise SystemExit("Install the `tengwar` package or pass --font-path to point at a CSUR font.")
    fonts = extract_bundled_fonts()
    if not fonts:
        raise SystemExit("No fonts found via the `tengwar` package; pass --font-path explicitly.")
    return fonts[0]


def load_mode(mode_path: Path):
    if not mode_path.exists():
        raise SystemExit(f"Mode file not found: {mode_path}")
    parser = ModeParser()
    mode = parser.parse(str(mode_path))
    mode.processor.finalize({})
    return mode


def transcribe(text: str, mode_path: Path, charset_name: str = None) -> str:
    mode = load_mode(mode_path)
    success, result, _debug = mode.transcribe(text, charset=charset_name)
    if not success:
        raise SystemExit("Glaemscribe transcription failed")
    return result


def render(text: str, mode_path: Path, font_file: Path, font_size: int, output: Path) -> None:
    # Determine charset based on font name
    if "freemono" in font_file.name.lower():
        charset_name = "tengwar_freemono"
    else:
        charset_name = None  # Use default charset
    
    glyphs = transcribe(text, mode_path, charset_name)
    font = ImageFont.truetype(str(font_file), font_size)

    # Estimate canvas size
    tmp_img = Image.new("RGBA", (10, 10), (255, 255, 255, 0))
    tmp_draw = ImageDraw.Draw(tmp_img)
    left, top, right, bottom = tmp_draw.textbbox((0, 0), glyphs, font=font)
    padding = 20
    width = max(1, right - left) + padding * 2
    height = max(1, bottom - top) + padding * 2

    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), glyphs, font=font, fill=(0, 0, 0, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    print(
        f"Rendered '{text}' with mode '{mode_path.name}' to {output} using font {font_file.name}"
    )


def main() -> None:
    args = parse_args()
    font_file = load_font(args.font_path)
    render(args.text, args.mode_path, font_file, args.font_size, args.output)


if __name__ == "__main__":
    main()
