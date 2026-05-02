# launching-google-ai

Opens Google Gemini or Google Stitch in the browser with a pre-filled prompt and optional Gemini tool selection (image, video, music, deep research, canvas, guided learning).

## What it does

- Builds the right URL for Gemini (`https://gemini.google.com/?prompt=...&tool=...`) or Stitch (`https://stitch.withgoogle.com/?prompt=...`).
- Picks the correct Gemini tool alias from natural-language cues — "research this" → `tool=research`, "make a video of" → `tool=video`, "generate an image of" → `tool=image`.
- URL-encodes the prompt safely, including newlines (`%0A`) and special characters.
- Honors `$BROWSER` (so users can route to a specific Chrome profile or browser binary), falling back to `xdg-open`.
- Stops at pre-fill — never auto-submits, so the user keeps a final-edit step.

## Usage

### Claude Code

```sh
claude --plugin-dir ./plugins/launching-google-ai
```

Or via the marketplace, once installed.

### pi

```sh
pi -e ./plugins/launching-google-ai    # ephemeral
pi install ./plugins/launching-google-ai
```

### Codex

See the root [`.codex/INSTALL.md`](../../.codex/INSTALL.md).

## Harness support

| Feature | Claude Code | Codex | pi |
|---|---|---|---|
| Skill (SKILL.md) | ✅ | ✅ | ✅ |

Pure skill content — runs identically in all three harnesses. The only host requirement is a shell with `$BROWSER` or `xdg-open` available (Linux/macOS); on macOS, `open` works as a drop-in replacement for `xdg-open` and the skill will use it via `$BROWSER` if set.

## Evals

Regression cases live in [`../../evals/cases/launching-google-ai/cases.yaml`](../../evals/cases/launching-google-ai/cases.yaml).

```sh
uv run evals/framework/run.py --skill launching-google-ai
```

## License

[CC BY-SA 4.0](../../LICENSE) — made by [Nothing Fancy](https://nothingfancy.ai).
