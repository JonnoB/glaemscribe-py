#!/usr/bin/env python3
"""Generate canonical Sindarin transcription outputs for regression tests.

This script is analogous in spirit to generate_reference_transcriptions.py
used for Quenya. It computes the current (known-good) Python transcription
outputs for selected Sindarin phrases, and writes them to a JSON fixture
file consumed by pytest.

Run from the project root with:

    uv run python scripts/generate_sindarin_reference_transcriptions.py

This will create or overwrite:

    tests/fixtures/sindarin_transcription_canonical.json

"""

from __future__ import annotations

import json
import os
from pathlib import Path

from glaemscribe.parsers.mode_parser import ModeParser
from glaemscribe.resources import get_mode_path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "sindarin_transcription_canonical.json"


PHRASE_LINES = [
    "Ai na vedui Dúnadan !",
    "Mae govannen !",
    "Ennyn Durin aran Moria: pedo mellon a minno!",
    "Im Narvi hain echant. Celebrimbor o Eregion teithant i thiw hin.",
]

MODES = [
    ("sindarin-tengwar-general_use", "Sindarin Tengwar - General Use"),
    ("sindarin-tengwar-beleriand", "Sindarin Tengwar - Beleriand"),
]


def transcribe_mode(mode_name: str, text: str) -> str:
    """Helper to transcribe text using a specific mode.

    This mirrors the pattern used in test_poem_transcription.
    """
    parser = ModeParser()
    mode_file = get_mode_path(mode_name)
    mode = parser.parse(str(mode_file))
    mode.processor.finalize({})
    success, result, _ = mode.transcribe(text)
    if not success:
        raise RuntimeError(f"Transcription failed for mode={mode_name!r}, text={text!r}: {result}")
    return result


def main() -> None:
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases = []
    for mode_name, mode_desc in MODES:
        for idx, line in enumerate(PHRASE_LINES, start=1):
            desc = f"Sindarin phrase line {idx} ({mode_desc})"
            output = transcribe_mode(mode_name, line)
            cases.append(
                {
                    "mode": mode_name,
                    "description": desc,
                    "line": line,
                    "output": output,
                }
            )

    with FIXTURE_PATH.open("w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    print(f"Wrote {FIXTURE_PATH} with {len(cases)} cases")


if __name__ == "__main__":
    main()
