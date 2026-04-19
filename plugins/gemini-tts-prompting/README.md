# gemini-tts-prompting

Crafts and reviews prompts for Google's Gemini 3.1 Flash TTS (text-to-speech) model — voice selection, style instructions, and the inline audio-tag system.

## What it does

Teaches a small set of decisions, not a wall of specs:

- **Pick a baseline voice and language**, then steer with natural-language style instructions for tone, accent, and persona.
- **Compose audio tags** using the `[pacing] + text + [expressive] + text + [pause] + text` formula — never two tags adjacent.
- **Direct expression** with the right tag family — emotional ([determination], [whispers], [laughs]), pacing ([slow], [fast], [short pause], [long pause]), or non-verbal vocalizations.
- **Stack tags for drama** in long-form content (audiobooks, scene narration) without over-tagging short utterances.
- **Handle accents the right way** — through the style prompt, not the language setting.
- **Cover the common shapes**: accessibility narration, audiobook scene-setting, IVR/notification, multilingual content with English tags.

Includes an anti-patterns table covering adjacent tags, SSML carryover, and accent-via-language-setting.

## Usage

### Claude Code

```sh
claude --plugin-dir ./plugins/gemini-tts-prompting
```

Or via the marketplace, once installed.

### pi

```sh
pi -e ./plugins/gemini-tts-prompting    # ephemeral
pi install ./plugins/gemini-tts-prompting
```

### Codex

See the root [`.codex/INSTALL.md`](../../.codex/INSTALL.md).

## Harness support

| Feature | Claude Code | Codex | pi |
|---|---|---|---|
| Skill (SKILL.md) | ✅ | ✅ | ✅ |

Pure skill content — runs identically in all three harnesses.

## Evals

Regression cases live in [`../../evals/cases/gemini-tts-prompting/cases.yaml`](../../evals/cases/gemini-tts-prompting/cases.yaml).

```sh
uv run evals/framework/run.py --skill gemini-tts-prompting
```

## License

[CC BY-SA 4.0](../../LICENSE) — made by [Nothing Fancy](https://nothingfancy.ai).
