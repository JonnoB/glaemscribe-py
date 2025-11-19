"""Tests for glaemscribe.parsers.charset_parser (focused, no real .cst files)."""

import types

from glaemscribe.core.charset import Charset as CoreCharset
from glaemscribe.parsers.charset_parser import (
    Char,
    VirtualChar,
    VirtualClass,
    CharsetParser,
)


def _make_fake_parser(charset_name: str):
    """Create a minimal object that looks like a CharsetParser for tests."""
    fake = types.SimpleNamespace()
    fake.charset = types.SimpleNamespace(name=charset_name)
    fake._chars_by_name = {}

    def _get_character_by_name(name: str):
        return fake._chars_by_name.get(name)

    fake._get_character_by_name = _get_character_by_name
    return fake


def test_char_uses_direct_unicode_mapping_for_freemono_charset(monkeypatch):
    fake_parser = _make_fake_parser("tengwar_freemono")

    # PUA codepoint: should map directly to chr(code)
    c_pua = Char(line=1, code=0xE000, names=["TINCO"], str_value="", charset=fake_parser)
    assert c_pua.str_value == "\ue000"

    # Non-PUA codepoint but freemono charset: still direct mapping, no font map
    called_with = {}

    def fake_map_font_code_to_unicode(code):  # pragma: no cover - guard that it's NOT called
        called_with["code"] = code
        return "X"

    # Ensure legacy mapping function is not used for freemono
    monkeypatch.setattr(
        "glaemscribe.parsers.charset_parser.map_font_code_to_unicode",
        fake_map_font_code_to_unicode,
    )

    c_ascii = Char(line=2, code=0x41, names=["A"], str_value="", charset=fake_parser)
    assert c_ascii.str_value == "A"
    assert called_with == {}


def test_char_uses_font_mapping_for_legacy_charset(monkeypatch):
    fake_parser = _make_fake_parser("ds_legacy")

    seen = {}

    def fake_map_font_code_to_unicode(code):
        seen["code"] = code
        return "\ue123"

    monkeypatch.setattr(
        "glaemscribe.parsers.charset_parser.map_font_code_to_unicode",
        fake_map_font_code_to_unicode,
    )

    c_legacy = Char(line=3, code=0x41, names=["A"], str_value="", charset=fake_parser)

    assert c_legacy.str_value == "\ue123"
    assert seen["code"] == 0x41


def test_virtual_char_finalize_builds_lookup_table():
    fake_parser = _make_fake_parser("tengwar_freemono")

    # Real characters that virtual char will refer to
    base_char = Char(line=1, code=0xE000, names=["TINCO", "T"], str_value="", charset=fake_parser)
    ext_char = Char(line=2, code=0xE001, names=["TINCO_EXT"], str_value="", charset=fake_parser)

    # Register chars in fake parser lookup
    fake_parser._chars_by_name["TINCO"] = base_char
    fake_parser._chars_by_name["T"] = base_char
    fake_parser._chars_by_name["TINCO_EXT"] = ext_char

    vclass = VirtualClass(target="TINCO_EXT", triggers=["TINCO"])
    vchar = VirtualChar(line=10, names=["A_TEHTA"], classes=[vclass], charset=fake_parser)

    vchar.finalize()

    # All names of the trigger char should map to the same result char
    assert vchar["TINCO"] is ext_char
    assert vchar["T"] is ext_char


def test_virtual_char_get_str_default_and_fallback():
    fake_parser = _make_fake_parser("tengwar_freemono")

    default_char = Char(line=1, code=0xE010, names=["DEFAULT_CHAR"], str_value="", charset=fake_parser)
    fake_parser._chars_by_name["DEFAULT_CHAR"] = default_char

    # With default pointing to an existing char
    v_with_default = VirtualChar(
        line=5,
        names=["VC"],
        classes=[],
        charset=fake_parser,
        default="DEFAULT_CHAR",
    )
    assert v_with_default.get_str() == default_char.str_value

    # Without default (or missing), falls back to '?'
    v_no_default = VirtualChar(line=6, names=["VC2"], classes=[], charset=fake_parser)
    assert v_no_default.get_str() == "?"


class _FakeNode:
    """Minimal stand-in for glaeml.Node used in internal parser helpers."""

    def __init__(self, name: str, args=None, children=None, line: int = 1, is_text: bool = False):
        self.name = name
        self.args = args or []
        self.children = children or []
        self.line = line
        self._is_text = is_text

    def is_text(self) -> bool:
        return self._is_text

    def is_element(self) -> bool:
        return not self._is_text

    def gpath(self, name: str):
        return [c for c in self.children if c.name == name]


def test_process_virtual_builds_virtualchar_and_registers_in_charset():
    parser = CharsetParser()
    parser.charset = CoreCharset(name="test_charset", version="1.0.0")

    # Build a virtual element with:
    #   - names: VOWEL_VC
    #   - one class: target=VOWEL_EXT, triggers from args + text body
    #   - reversed flag present
    #   - default target name
    class_text_child = _FakeNode("text", args=["TINCO ?"], children=[], is_text=True)
    class_node = _FakeNode("class", args=["VOWEL_EXT", "A"], children=[class_text_child])
    reversed_node = _FakeNode("reversed", args=[], children=[])
    default_node = _FakeNode("default", args=["DEFAULT_CHAR"], children=[])
    virtual_node = _FakeNode(
        "virtual",
        args=["VOWEL_VC", "?"],  # '?' should be ignored
        children=[class_node, reversed_node, default_node],
        line=42,
    )

    parser._process_virtual(virtual_node)

    # A VirtualChar should have been added
    assert isinstance(parser.chars[-1], VirtualChar)
    vchar = parser.chars[-1]
    assert vchar.names == ["VOWEL_VC"]
    # Triggers: 'A' from args and 'TINCO' from text, '?' filtered out
    vc_class = vchar.classes[0]
    assert vc_class.target == "VOWEL_EXT"
    assert set(vc_class.triggers) == {"A", "TINCO"}
    assert vchar.reversed is True
    assert vchar.default == "DEFAULT_CHAR"

    # It should also be registered in the core charset's virtual_chars
    assert parser.charset.virtual_chars["VOWEL_VC"] is vchar


def test_process_swap_registers_targets_on_charset():
    parser = CharsetParser()
    parser.charset = CoreCharset(name="test_charset", version="1.0.0")

    # Swap with targets from both args and text children, filtering '?'
    text_child = _FakeNode("text", args=["C D ?"], children=[], is_text=True)
    swap_node = _FakeNode(
        "swap",
        args=["A", "B", "?"],
        children=[text_child],
    )

    parser._process_swap(swap_node)

    # Charset.add_swap should have populated swaps
    assert parser.charset.has_swap_target("A", "B")
    assert parser.charset.has_swap_target("A", "C")
    assert parser.charset.has_swap_target("A", "D")
    # '?' should not be present
    assert not parser.charset.has_swap_target("A", "?")


def test_process_sequence_registers_sequence_tokens():
    parser = CharsetParser()
    parser.charset = CoreCharset(name="test_charset", version="1.0.0")

    text_child = _FakeNode("text", args=["C D ?"], children=[], is_text=True)
    seq_node = _FakeNode(
        "sequence",
        args=["SEQ_NAME", "A", "B", "?"],
        children=[text_child],
    )

    parser._process_sequence(seq_node)

    tokens = parser.charset.sequences["SEQ_NAME"]
    # Tokens from args and text, '?' filtered
    assert tokens == ["A", "B", "C", "D"]
