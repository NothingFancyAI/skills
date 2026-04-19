---
name: gemini-tts-prompting
description: Crafts and reviews prompts for Google's Gemini 3.1 Flash TTS (text-to-speech) model using audio tags, voice style instructions, and pacing controls. Use when asked to write, refine, or debug a TTS prompt for Gemini, Vertex AI speech generation, or Google AI Studio speech; when adding expressive audio tags like [whispers] or [excitement], controlling pacing with [slow]/[fast]/[short pause]/[long pause], or directing voice style and accent for narration, audiobooks, IVR, accessibility, or game audio.
---

# Gemini TTS Prompting

Helps a user craft prompts for Google's Gemini 3.1 Flash TTS. The guiding principle: this model exposes three layered controls — **voice selection, natural-language style instructions, and inline audio tags** — and getting expressive output means using all three together. Tags are not decoration; they are punctuation for performance.

## When to Use

- Writing a Gemini TTS prompt for narration, audiobooks, scene reads, or character dialogue.
- Adding expressive direction (emotion, pacing, pauses, non-verbal vocalizations) to text that will be spoken.
- Producing IVR, automated notifications, fraud alerts, or other enterprise voice flows where tone shifts matter.
- Generating accessibility audio — game menus, audio descriptions for film/TV, screen-reader replacements.
- Multilingual audio: spoken text in French, Korean, Japanese, etc., with English-language audio tags.
- Debugging a Gemini TTS prompt that produced flat, monotone, robotic, or mispaced output.

## When NOT to Use

- The target model is ElevenLabs, OpenAI TTS, Amazon Polly, Azure Neural TTS, or any non-Gemini TTS. Their controls (SSML, voice settings, custom phonemes, stability sliders) are different — applying these audio-tag formulas verbatim will produce no effect or break their parsers.
- The task is integrating the Gemini TTS API from code (auth, streaming, audio format selection). That's an SDK/Vertex AI integration job — reach for the Vertex AI docs.
- The user wants speech-to-text (STT/transcription), not TTS. Different model family, different prompting model — most controls here don't apply.
- The task is music (Lyria), generic audio effects, or sound design from text. Different model family.
- The user wants live voice cloning or custom voice training. Gemini TTS uses 30 prebuilt voices and does not train custom voices from samples.

## The three layers of control

Every Gemini TTS prompt steers the model through three layers, applied in this order:

1. **Voice and language selection** — pick one of the [30 prebuilt voices](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts#voice_options) and a target language from [70+ supported options](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts#available_languages). This is configuration, not part of the text prompt.
2. **Natural-language style instruction** — a sentence describing the persona, tone, accent, and delivery style. Sits alongside the spoken text in the request, not inline.
3. **Inline audio tags** — square-bracketed control codes embedded directly in the spoken text. Steer pacing, expression, and non-verbal sounds at specific moments.

A common failure mode is reaching for tags first and skipping layers 1 and 2. A flat read with twelve tags sprinkled in still sounds flat — the baseline voice and persona instruction set the texture that the tags then modulate.

## The audio-tag formula

```
[pacing tag] + spoken text + [expressive tag] + spoken text + [pause tag] + spoken text
```

Hard rules — break these and the model either errors or strips your tags:

- **Square brackets only.** `[whispers]`, `[excitement]`, `[short pause]`. Not `<whispers>`, not `(whispers)`, not curly braces.
- **English-only tag names.** Even when the spoken text is French, Japanese, or Korean — the tag itself stays English. `[whispers] Le document secret...` is correct.
- **Never two tags adjacent.** `[whispers][slow]` will error. Always separate tags with at least one word or one piece of punctuation between them.
- **Tags mark transitions.** Place a tag at the exact moment delivery should change, not at the start of the prompt as a global setting (that's the style instruction's job).
- **Accents come from the style instruction, not the language setting.** Set the language to the *language being spoken*; describe the accent ("with a soft Scottish lilt") in the style prompt.

## Direct the performance with the right tag family

The model supports 200+ tags. They fall into three families. Pick from the family that matches the kind of change you want.

### Emotional and expressive tags

For shifts in emotional register. Common picks: `[determination]`, `[enthusiasm]`, `[awe]`, `[admiration]`, `[nervousness]`, `[frustration]`, `[excitement]`, `[curiosity]`, `[hope]`, `[annoyance]`, `[amusement]`, `[aggression]`, `[tension]`, `[agitation]`, `[confusion]`, `[anger]`, `[adoration]`, `[interest]`, `[positive]`, `[neutral]`, `[negative]`, `[whispers]`, `[laughs]`.

Use `[positive]`, `[neutral]`, `[negative]` as low-commitment dial-shifts when you want a tone change without naming a specific emotion — common in enterprise IVR flows that need to transition between informational and reassuring without sounding theatrical.

### Pacing and stylistic tags

For tempo and breath. `[slow]` and `[fast]` change rate of delivery. `[short pause]` and `[long pause]` insert dramatic silence — the only reliable way to get a beat between sentences without trusting the model to infer it from punctuation.

Use pauses to let critical information land — account numbers, times, gate numbers, the name of the bank — and to build suspense in narrative content.

### Non-verbal vocalizations

`[laughs]` and `[whispers]` are the most useful. They produce realistic non-verbal audio rather than rendering the literal word. `[whispers]` is a special case: it acts as both an emotion (lowered intensity) and a vocalization style that persists until the next expressive tag overrides it.

## Worked examples

### Audiobook scene — stack tags for drama

Stack pacing and expression to build narrative arc. Each tag marks a beat the listener should feel.

```
[cautious] Step carefully around the glowing runes on the floor.
[anxiety] One wrong move and the entire temple collapses.
[relief] We finally found the crystal. [awe] It is more brilliant
than the stories described. [alarm] Wait, the light inside is
turning red. [panic] Run for the exit!
```

Why this works: each emotional tag corresponds to a clear narrative beat; the tags are separated by full sentences (never adjacent); pacing is implied by the emotional arc rather than fighting `[slow]`/`[fast]` on top.

### Enterprise IVR — transitions, not theatrics

Banking and notification flows need to shift from neutral information to reassuring resolution without sounding like an audiobook narrator.

```
[neutral] Hello. This is an automated fraud prevention alert from
Horizon Bank. [seriousness] We detected unusual activity on your
card ending in [slow] 4 3 2 1. [positive] If you recognize a charge
of eighty-five dollars at City Electronics, please press one.
```

Two tricks worth copying: `[slow]` around digit strings forces digit-by-digit clarity (essential for confirmations); the `[neutral] → [seriousness] → [positive]` arc handles attention-getter, problem statement, and call-to-action without ever reaching for a high-emotion tag.

### Accessibility — clear and inviting, not flat

Game menus and audio descriptions need to be expressive enough to feel inviting, restrained enough not to compete with primary content.

```
[enthusiasm] You have selected the Twilight Forest level.
[interest] This area features hidden artifacts and new challenges.
It includes an expansive map, challenging puzzles, and a
specialized survival kit.
```

For TV or film audio descriptions specifically, `[whispers]` is the right choice for tense scene-setting — it ducks under the primary audio rather than competing with it.

### Multilingual — English tags, native text

Set the language to the spoken language. Tag in English. Describe the accent in the style instruction (not by switching language codes).

```
[cautious] L'ombre avança lentement dans la pièce silencieuse.
[whispers] Le document secret devait être caché ici. [short pause]
Mais où? [gasp] Soudain, un bruit sourd résonna dans le couloir.
[panic] Il fallait sortir d'ici immédiatement.
```

## Long-form content: don't hand-tag everything

For chapter-length narration, manually inserting tags is tedious and error-prone. The recommended pattern: use Gemini 3.1 Flash-Lite as a preprocessor to annotate the text with audio tags, then pass the annotated text to Gemini 3.1 Flash TTS. Two model calls, two responsibilities — the preprocessor reads the text and decides where the beats are, the TTS model performs them.

The Google team published a [demo of this pipeline](https://take3bounce.app/) that's worth referencing when scoping any audiobook-length project.

## Watermarking

All Gemini 3.1 Flash TTS output carries a SynthID watermark woven into the audio. This is non-removable through normal editing and is detectable by Google's verification tools. Mention this when the output will be used in contexts that require AI-content disclosure (broadcast, regulated industries, journalism).

## Anti-patterns

| Anti-pattern | Signal | Fix |
|---|---|---|
| Adjacent tags | `[whispers][slow] text` or `[fast][excitement]` — back-to-back square brackets | Separate every pair of tags with at least one word or one piece of punctuation. |
| SSML or other-vendor syntax | `<break time="500ms"/>`, `<prosody rate="slow">`, `<emphasis>` | Gemini TTS does not parse SSML. Use `[short pause]` / `[long pause]` and `[slow]` / `[fast]`. |
| Localized tag names | `[susurros]` for Spanish, `[chuchote]` for French | Tag names are English-only regardless of spoken language. The Spanish text gets `[whispers]`. |
| Accent via language setting | Picking `en-IN` to get an Indian-English accent | Pick the language you want spoken; describe the accent in the natural-language style instruction. |
| Tag-only direction with no style instruction | All steering is inline tags; voice/persona is left blank | Set persona and tone in the style instruction first; let tags modulate from that baseline. |
| Over-tagging short utterances | A 10-word IVR confirmation with five expressive tags | One or two tags is plenty for short content. Tags should mark genuine transitions, not decorate every clause. |
| Under-tagging long-form | A two-page audiobook scene with no tags | Stack tags to mark beats. Plain text reads flat. For chapter-length, preprocess with Flash-Lite. |
| Reaching for expressive tags when pacing is the real fix | Adding `[excitement]` when the actual problem is rushed delivery | Try `[slow]` or `[short pause]` before reaching for emotion tags. Pacing changes often solve "it sounds wrong." |
| Trying to render character names as different voices mid-prompt | Inline tags like `[character: Alice]` to switch voices per line | The model uses one voice per request. For multi-character dialogue, generate each character's lines as a separate request and stitch the audio. |
| Treating digit strings as words | `[slow] 4321` (one token) for an account number | Insert spaces — `[slow] 4 3 2 1` — so the model speaks each digit individually. Same trick for flight numbers, gate numbers, codes. |
