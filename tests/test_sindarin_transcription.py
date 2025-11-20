"""Canonical Sindarin transcription regression tests.

These tests are analogous to test_poem_transcription, but for Sindarin
phrases in both the General Use and Beleriand Tengwar modes. They compare
Python transcription output against a canonical Unicode PUA fixture
captured from the (now parity-checked) implementation.
"""

from __future__ import annotations

import json
import os

import pytest
from glaemscribe.parsers.mode_parser import ModeParser


def load_canonical_outputs():
    """Load canonical Sindarin outputs from the fixture JSON."""
    fixture_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "sindarin_transcription_canonical.json"
    )
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


CANONICAL_OUTPUTS = load_canonical_outputs()


def transcribe_mode(mode_name: str, text: str) -> str:
    """Helper function to transcribe text using a specific mode.

    Mirrors the helper in test_poem_transcription, but works for any mode.
    """
    from glaemscribe.resources import get_mode_path

    parser = ModeParser()
    mode_file = get_mode_path(mode_name)
    mode = parser.parse(str(mode_file))
    mode.processor.finalize({})
    success, result, _ = mode.transcribe(text)
    return result if success else result


@pytest.mark.parametrize("test_case", CANONICAL_OUTPUTS)
def test_sindarin_phrase_transcription(test_case):
    """Test each Sindarin phrase line against canonical output.

    This ensures that Sindarin General Use and Beleriand modes continue to
    produce the same Tengwar output as the canonical fixture, guarding
    against regressions in the core engine or mode parsing.
    """
    mode_name = test_case["mode"]
    line = test_case["line"]

    result = transcribe_mode(mode_name, line)

    assert result == test_case["output"], (
        f"Transcription mismatch for '{line}' (mode={mode_name})\n"
        f"Description: {test_case['description']}\n"
        f"Expected: {test_case['output']}\n"
        f"Got:      {result}\n"
        f"Expected chars: {[f'U+{ord(c):04X}' for c in test_case['output']]}\n"
        f"Got chars:      {[f'U+{ord(c):04X}' for c in result]}"
    )
