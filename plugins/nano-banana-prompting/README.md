# nano-banana-prompting

Crafts and reviews prompts for Google's Nano Banana 2 (Gemini 3.1 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image) image generation and editing models.

## What it does

Teaches a small set of decisions, not a wall of specs:

- **Pick the right framework** for the task — text-to-image, multimodal-with-references, editing, web-search-grounded, or text rendering.
- **Write narratively, not in keywords.** Subject + Action + Location + Composition + Style.
- **Use positive framing.** "Empty street" beats "no cars" — negation leaks the forbidden concept into the model's attention.
- **Direct like a creative director.** Specify lighting, camera/lens/film stock, and material textures rather than vague style words.
- **Render legible text correctly.** Quote the literal words, name the font, and use the text-first hack for complex typography.

Includes a brief tech-specs comparison table for choosing between Flash and Pro, and an anti-patterns table covering keyword soup, unquoted text, and unlabelled reference images.

## Usage

### Claude Code

```sh
claude --plugin-dir ./plugins/nano-banana-prompting
```

Or via the marketplace, once installed.

### pi

```sh
pi -e ./plugins/nano-banana-prompting    # ephemeral
pi install ./plugins/nano-banana-prompting
```

### Codex

See the root [`.codex/INSTALL.md`](../../.codex/INSTALL.md).

## Harness support

| Feature | Claude Code | Codex | pi |
|---|---|---|---|
| Skill (SKILL.md) | ✅ | ✅ | ✅ |

Pure skill content — runs identically in all three harnesses.

## Evals

Regression cases live in [`../../evals/cases/nano-banana-prompting/cases.yaml`](../../evals/cases/nano-banana-prompting/cases.yaml).

```sh
uv run evals/framework/run.py --skill nano-banana-prompting
```

## License

[CC BY-SA 4.0](../../LICENSE) — made by [Nothing Fancy](https://nothingfancy.ai).
