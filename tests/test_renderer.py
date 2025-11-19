"""Tests for glaemscribe.render.renderer."""

import base64

from glaemscribe.render.renderer import (
    TengwarRenderer,
    render_tengwar,
    tengwar_to_image,
    tengwar_to_base64,
)


def test_render_text_respects_explicit_size():
    renderer = TengwarRenderer(font_size=16)

    image = renderer.render_text("aiya", size=(80, 32), padding=0)

    assert image.size == (80, 32)


def test_render_to_bytes_and_base64_are_consistent():
    renderer = TengwarRenderer(font_size=18)
    text = "elen sila"

    image_bytes = renderer.render_to_bytes(text, format="PNG", padding=5)
    assert len(image_bytes) > 0

    b64_string = renderer.render_to_base64(text, format="PNG", padding=5)
    decoded = base64.b64decode(b64_string)

    assert decoded == image_bytes


def test_render_to_file_creates_image(tmp_path):
    renderer = TengwarRenderer(font_size=20)
    output = tmp_path / "rendered.png"

    renderer.render_to_file("nai", str(output), padding=4)

    assert output.exists()
    assert output.stat().st_size > 0


def test_convenience_wrappers(tmp_path):
    output_path = tmp_path / "tengwar.png"

    render_tengwar("aear", str(output_path))
    assert output_path.exists()

    image = tengwar_to_image("quenya")
    assert image.size[0] > 0 and image.size[1] > 0

    b64_string = tengwar_to_base64("vala")
    assert isinstance(b64_string, str)
    assert len(b64_string) > 0
