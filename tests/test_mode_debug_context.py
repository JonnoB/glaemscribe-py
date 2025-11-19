"""Tests for glaemscribe.core.mode_debug_context."""

from glaemscribe.core.mode_debug_context import ModeDebugContext


def test_mode_debug_context_adds_paths_and_includes_in_summary():
    ctx = ModeDebugContext()

    ctx.preprocessor_output = "pre-out"
    ctx.processor_output = ["tok1", "tok2"]
    ctx.postprocessor_output = "post-out"
    ctx.tts_output = "tts"

    ctx.add_processor_path("a", ["t1"], ["f1"])
    ctx.add_processor_path("bc", ["t2", "t3"], ["f2"])

    summary = ctx.get_summary()

    assert "Transcription Debug Summary" in summary
    assert "Preprocessor output: 7 chars" in summary
    assert "Processor steps: 2" in summary
    assert "Processor output: 2 tokens" in summary
    assert "Postprocessor output: 8 chars" in summary
    assert "TTS output: 3 chars" in summary

    # First few processor steps section should list the paths
    assert "First few processor steps" in summary
    assert "1. 'a' -> ['t1']" in summary
    assert "2. 'bc' -> ['t2', 't3']" in summary


def test_mode_debug_context_clear_resets_all_fields():
    ctx = ModeDebugContext()

    ctx.preprocessor_output = "x"
    ctx.processor_pathes.append(["eaten", ["tok"], ["ftok"]])
    ctx.processor_output = ["tok"]
    ctx.postprocessor_output = "y"
    ctx.tts_output = "z"

    ctx.clear()

    assert ctx.preprocessor_output == ""
    assert ctx.processor_pathes == []
    assert ctx.processor_output == []
    assert ctx.postprocessor_output == ""
    assert ctx.tts_output == ""


def test_mode_debug_context_str_uses_summary():
    ctx = ModeDebugContext()
    ctx.preprocessor_output = "abc"

    s = str(ctx)
    assert "Transcription Debug Summary" in s
    assert "Preprocessor output: 3 chars" in s
