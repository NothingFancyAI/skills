---
name: nano-banana-prompting
description: Crafts and reviews prompts for Google's Nano Banana 2 (Gemini 3.1 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image) image generation and editing models. Use when asked to write, refine, or debug a prompt for Nano Banana, Gemini image generation, or Vertex AI image generation; when generating with reference images, editing or inpainting an existing image, or rendering legible text and typography.
---

# Nano Banana Prompting

Helps a user craft prompts for Google's Nano Banana 2 (Gemini 3.1 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image). The guiding principle: these models reason about the prompt before generating, so narrative descriptions beat keyword lists, positive framing beats negation, and explicit camera/lighting/material direction beats vague style words.

## When to Use

- Writing a Nano Banana or Gemini Image prompt to generate from a blank canvas.
- Generating with one or more reference images (character or product consistency, sketch-to-render, style transfer setup).
- Editing an existing image — inpainting, removing or adding elements, recoloring, or style transfer.
- Rendering legible text or typography inside an image (posters, mockups, ads).
- Localizing image text into another language.
- Debugging a prompt that produced a wrong, blurry, or visually-incoherent result.

## When NOT to Use

- The task is calling the Gemini Image API from code. That is an SDK / Vertex AI integration job, not a prompt-engineering one — reach for the Vertex AI docs or the Anthropic/OpenAI SDK skill instead.
- The target model is Midjourney, DALL-E, Stable Diffusion, Imagen 3, or any non-Gemini image model. Their prompting conventions (parameter flags, weight syntax, style references) are different — applying these formulas verbatim will produce worse output, not better.
- The task is video (Veo) or music (Lyria). Different model families, different prompting patterns.
- The user wants pricing, quota, or model availability info. Read the live [Vertex AI documentation](https://cloud.google.com/vertex-ai/generative-ai/docs) — that data goes stale.

## Pick the framework that matches the task

| You want to... | Use framework |
|---|---|
| Generate from a blank canvas | **1. Text-to-image** |
| Combine references (sketch + texture, product + scene, character consistency) | **2. Multimodal with references** |
| Modify an image you already have | **3. Editing** |
| Pull live data into the image (weather, prices, current events) | **4. Web-search-grounded** |
| Put readable words on the image | **5. Text rendering** |

These compose. A poster with legible text combines #1 and #5. Refining an editorial photo conversationally is #1 followed by several rounds of #3.

## Core principles

1. **Be specific.** Concrete details about subject, lighting, and composition. "Cherry red seamless studio backdrop with a soft three-point softbox setup" beats "nice background."
2. **Use positive framing.** Describe what should be in the frame, not what to avoid. "Empty street at dawn" beats "street with no cars and no people." Negation tends to leak the forbidden concept into the model's attention — the model has to imagine the cars to remove them.
3. **Control the camera.** Use the photographic vocabulary: low-angle, aerial, macro, f/1.8, GoPro, Fujifilm color science, 1980s color film. The model knows what these look like and they collapse a paragraph of vague style words into one word.
4. **Iterate conversationally.** Refine in follow-ups rather than packing every constraint into the first prompt. Each turn can change one variable, which makes the failure mode obvious.
5. **Start with a strong verb.** *Generate*, *Edit*, *Combine*, *Render*, *Translate*. A verb-first prompt disambiguates the operation; a noun-first prompt forces the model to guess.

## Elicit style when it's underspecified

If the user's request names no concrete style — no camera, no film stock, no lighting cue, no art-historical reference, no genre — pause and offer them a small menu **before** generating. A vague style produces a generic image; a chosen style produces a directed one. Picking silently almost always lands on a bland default that's easy to dismiss as "AI-looking."

**How to ask.** Use the harness's interactive question mechanism. In Claude Code that's the `AskUserQuestion` tool (cap of 4 explicit options; the harness auto-adds an "Other" escape). In pi or Codex, ask in plain text and list the choices inline. Either way, present:

- **3 common styles** that obviously fit the subject — defaults the user is likely already considering.
- **2 adventurous styles** — deliberate left turns the user probably hasn't pictured but might love.

When constrained to 4 options (Claude Code), drop one common style rather than an adventurous one — the "Other" auto-option already covers the conservative escape, so the adventurous picks earn their slot by being unexpected.

Each option must be concrete enough that someone could write a prompt from it: name the camera, lens, lighting, film stock, palette, or art-historical reference. "Editorial" is too vague; "Editorial fashion shot on medium-format Portra 400, soft window light, slight grain" is enough.

**Skip the menu when:** the user has already named a style ("make it Wes-Anderson-symmetrical", "shot on a GoPro", "Studio Ghibli watercolor"), is iterating on an earlier image where the style is already settled, or explicitly says "surprise me / your call". In the surprise-me case, make a confident choice, *tell them* which one you picked, and proceed — so they can redirect on the next turn.

**Worked example.** Asked for a portrait of a chef in their kitchen with no style cue, propose:

- *Documentary food photography* — 35mm Fujifilm color science, available window light, shallow depth of field f/2.0. *(common)*
- *Glossy magazine cover* — three-point softbox lighting, medium-format digital, crisp detail, cool highlights. *(common)*
- *Moody chiaroscuro oil painting* — Caravaggio-style single-source lighting, painterly texture, deep shadow. *(common)*
- *1980s Polaroid candid* — on-camera flash, slight motion blur, washed colors, dated white border. *(adventurous)*
- *Wes-Anderson symmetrical diorama* — pastel palette, dead-center composition, flat lighting, miniaturized props. *(adventurous)*

Then assemble the chosen style into the Subject + Action + Location + Composition + Style formula.

## Framework 1 — Text-to-image (no references)

Formula:

```
[Subject] + [Action] + [Location/context] + [Composition] + [Style]
```

A keyword list won't cut it. Describe the scene narratively. Worked example:

> A striking fashion model wearing a tailored brown dress, sleek boots, and holding a structured handbag *[Subject]*, posing with a confident, statuesque stance, slightly turned *[Action]*, against a seamless deep cherry red studio backdrop *[Location]*, medium-full shot, center-framed *[Composition]*, fashion magazine editorial shot on medium-format analog film, pronounced grain, high saturation, cinematic lighting *[Style]*.

Each slot can be one phrase or a paragraph. The Style slot is where camera-direction vocabulary lives.

## Framework 2 — Multimodal generation (with references)

Formula:

```
[Reference images] + [Relationship instruction] + [New scenario]
```

The relationship instruction is the critical part — tell the model *how* each reference contributes (structure, texture, identity, pose, palette, background). Without it, the model blends the references in unintended ways.

Worked example:

> Using the attached napkin sketch as the *structure* and the attached fabric sample as the *texture*, transform this into a high-fidelity 3D armchair render. Place it in a sun-drenched, minimalist living room.

Both models accept up to 14 reference images per prompt. Naming each reference's role keeps the model from averaging them.

## Framework 3 — Editing

You already have a base image; the prompt focuses on what changes and what stays.

**Semantic masking (text-driven inpainting).** Define the "mask" through text. Be explicit about what to preserve:

> Remove the man on the left from the photo. Keep the lighting, background buildings, and reflection on the wet pavement exactly the same.

The "keep the rest exactly the same" clause is what separates an *edit* from a *regeneration*. Without it the model often re-renders the whole frame.

**Adding elements.** Upload base + object, name how they should combine. "Place the attached watch on the model's left wrist; preserve the original lighting and skin tones."

**Style transfer.** Upload a photo, ask the model to recreate the *same content* in a new style. "Transform this photo of a modern city street into a Van Gogh-style oil painting; preserve the layout of buildings and street."

## Framework 4 — Web-search-grounded prompts

Both models are powered by real-time information from web search. Instead of describing a fictional scene, instruct the model to retrieve real-world data and visualize it.

Formula:

```
[Source/search request] + [Analytical task on the data] + [Visual translation]
```

Worked example:

> Search for the current weather and date in San Francisco. If it's raining, render the scene grey and wet; if sunny, render it bright and golden. Visualize this as a miniature city-in-a-cup concept embedded inside a realistic, modern smartphone UI.

This is the unlock for localized marketing, travel apps, and dashboards that need real numbers rather than placeholder copy.

## Framework 5 — Text rendering and localization

Both models render sharp, legible text and support 10+ languages. Rules:

- **Quote the literal words.** Wrap rendered text in quotes: `"GLOW"`, `"Happy Birthday"`. Quotes signal to the model that these are literals to render, not concepts to depict.
- **Name a font.** "Bold white sans-serif", "Century Gothic 12px", "elegant brush script", "heavy blocky Impact". Concrete typography vocabulary beats "nice font" by a wide margin.
- **Style each text block separately.** If the poster has three lines with three styles, write three styled clauses, each tied to one line.
- **Localize explicitly.** Write the prompt in English, then specify the target language for the rendered text ("translate the headline into Korean and Arabic").
- **Text-first hack.** For complex typographic posters, *first* converse with the model to settle the wording, *then* ask for the image with the finalized text. Generating concept, copy, and layout in one prompt usually produces awkward word choices.

Worked example:

> A high-end glossy commercial beauty shot of a sleek minimalist nude-coloured face moisturizer jar on a warm studio background. Soft radiant lighting. Render three lines of text: top line `"GLOW"` in a flowing elegant Brush Script font; middle line `"10% OFF"` in a heavy blocky Impact font; bottom line `"Your First Order"` in a thin minimalist Century Gothic font.

## Direct like a creative director

For results that look intentional rather than generic, stop typing keywords and start directing.

**Lighting.** Name the setup: "three-point softbox setup" for product evenness, "Chiaroscuro lighting with harsh, high contrast" for drama, "golden hour backlighting creating long shadows" for warmth. Lighting words do more work than almost any other vocabulary.

**Camera and lens.** Specifying hardware changes the visual DNA. Ask for a GoPro for distorted action immersion, a Fujifilm body for that specific color science, a disposable camera for a raw nostalgic flash aesthetic. Lens choice forces perspective: "low-angle shot, shallow depth of field f/1.8" for portraiture, "wide-angle lens" for vast scale, "macro lens" for intricate texture.

**Color grading and film stock.** "1980s color film, slightly grainy" for nostalgia. "Cinematic color grading with muted teal tones" for modern moody. The texture and color set the emotional tone before the subject does — choose them consciously.

**Materiality and texture.** Don't ask for "a suit jacket" — ask for "navy blue tweed". Don't ask for "armor" — ask for "ornate elven plate armor etched with silver leaf patterns". For product mockups, name the surface: "minimalist matte ceramic coffee mug".

## Tech specs at a glance

| | Nano Banana 2 (Gemini 3.1 Flash Image) | Nano Banana Pro (Gemini 3 Pro Image) |
|---|---|---|
| Input tokens (max) | 131,072 | 65,536 |
| Output tokens (max) | 32,768 | 32,768 |
| Resolutions | 0.5K, 1K, 2K, 4K | 1K, 2K, 4K |
| Aspect ratios | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 + extreme 1:4, 4:1, 1:8, 8:1 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| Reference images per prompt | up to 14 | up to 14 |
| Knowledge cutoff | January 2025 | January 2025 |
| Live web search grounding | Yes | Yes |
| Watermark / provenance | C2PA + SynthID | C2PA + SynthID |

When choosing between them: Pro produces higher-fidelity results and is the default for hero assets; Flash is faster and cheaper, supports the smaller 0.5K resolution and the extreme 8:1/1:8 panoramic ratios, and accepts a much larger input context (useful when supplying many reference images plus long instructions).

Always confirm current limits against the live [Gemini 3 Pro Image](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image) and [Gemini 3.1 Flash Image](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-flash-image) documentation — these numbers move.

## Anti-patterns

| Anti-pattern | Signal | Fix |
|---|---|---|
| Keyword soup | "photo, woman, red dress, studio, professional, 4k" | Rewrite as a narrative sentence using the Subject + Action + Location + Composition + Style slots. |
| Negative framing | "no cars, no people, not blurry" | State the positive: "empty street at dawn, sharp focus". Negation leaks the forbidden concept into the model's attention. |
| Vague style ("make it cinematic") | No camera, lens, lighting, or film stock named | Specify hardware: "shot on a Fujifilm GFX 100 with a 50mm lens, golden hour backlighting, slight halation". |
| Picking a style silently when the user gave none | Final prompt invents a style the user never asked for | Pause and offer a menu of ~5 concrete styles (3 common + 2 adventurous) before assembling the prompt. |
| Unquoted text to render | "add the words happy birthday" | Quote it: render `"HAPPY BIRTHDAY"` in a [named font]. |
| Editing without a preservation clause | "remove the man" | "Remove the man on the left; keep the lighting, background, and pavement reflection exactly the same." |
| Mixing references without role labels | Pasting 5 images and saying "combine these" | Name each reference's contribution: "use #1 for character, #2 for pose, #3 for palette, #4 for background lighting". |
| Skipping the text-first hack for typographic posters | Trying to nail copy + layout + style in one shot | First chat to settle the words, then ask for the image with the finalized text and per-line type specs. |
| Reusing Midjourney-style syntax | `::` weights, `--ar 16:9`, `--stylize 750` | These don't apply. Set aspect ratio via the API parameter and write narrative prompts in plain English. |
| Asking the wrong model | Demanding 8:1 panoramic or 0.5K from Pro | Switch to Nano Banana 2 (Flash), which is the only model that supports those. |
