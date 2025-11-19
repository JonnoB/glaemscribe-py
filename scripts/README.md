
## Scripts


### Render Namárië poem

Render the canonical Namárië transcription to PNGs in the `data/` directory:

```bash
uv run python -m scripts.render_poem
```

Outputs:

- `data/namarie_poem_transcription.png` – original lines + Tengwar
- `data/namarie_poem_tengwar_only.png` – Tengwar-only version


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