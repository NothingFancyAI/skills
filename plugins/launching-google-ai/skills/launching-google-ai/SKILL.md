---
name: launching-google-ai
description: Opens Google Gemini or Google Stitch in the browser with a pre-filled prompt and optional Gemini tool (image, video, music, deep research, canvas, guided learning). Use when asked to "ask Gemini", "open Gemini with", "stitch this", "use deep research on", "generate a video in Gemini", or otherwise launch a prefilled Gemini or Stitch session via URL parameters from the shell. Does not auto-submit — only pre-fills the prompt box.
---

# Launching Google AI

Opens a Google Gemini or Google Stitch session in the user's browser with a prompt already typed in the box and (for Gemini) a tool already selected. The skill exists because the user wants to hand off to a hosted UI for the next step — usually a multi-modal session, a deep-research run, or a Stitch design loop — without retyping context.

The guiding principle: **build the URL, open it, stop.** Don't auto-submit. The user owns the final edit and the send button, every time.

## When to Use

- The user says "ask Gemini …", "open Gemini with …", "in Gemini, …", "fire up Gemini for …".
- The user says "stitch …", "stitch this …", "open Stitch with …", or names a UI mockup task they want Stitch to handle.
- The user wants a specific Gemini tool: "deep research X", "use canvas to …", "generate a video of …", "generate an image of …", "make some music about …", "guided learning for …".
- The user wants to take prompt text already in the conversation and continue it in a hosted Google AI UI.

## When NOT to Use

- The user wants to **call the Gemini API or Vertex AI** programmatically — that's an SDK task, not a URL launcher.
- The user wants to **write or refine** a prompt for Gemini image generation — use `nano-banana-prompting`.
- The user wants to **write or refine** a prompt for Gemini TTS — use `gemini-tts-prompting`.
- The user wants the model's actual answer in this conversation — answer it here; don't bounce them to the web UI.
- The user wants Google AI Studio, NotebookLM, or another Google surface — those are not covered (Gemini and Stitch only).
- The user wants the browser to **submit** automatically — that's outside this skill's contract and the underlying URL parameters do not support it.

## URL Patterns

### Gemini (default)

```
https://gemini.google.com/?prompt=<encoded_text>
https://gemini.google.com/?prompt=<encoded_text>&tool=<tool_alias>
```

### Stitch

```
https://stitch.withgoogle.com/?prompt=<encoded_text>
```

Stitch does not accept a `tool` parameter. Adding one is a silent no-op at best; treat it as a hard error and omit it.

## Gemini Tool Aliases

Pick the alias from natural-language cues. The aliases on the right are what go in `&tool=<alias>` — use the short form, not the human label.

| User cue | Tool | Alias |
|---|---|---|
| "generate an image", "draw", "make a picture" | Create image | `image` |
| "make a video", "generate a video", "animate" | Create video | `video` |
| "write a song", "compose music", "make music" | Create music | `music` |
| "deep research", "research this thoroughly", "comprehensive report on" | Deep research | `research` |
| "open canvas", "iterate in canvas", "use canvas for …" | Canvas | `canvas` |
| "teach me", "guided learning", "walk me through learning …" | Guided learning | `learn` |

If the user's intent doesn't clearly match one of these, omit the `tool` parameter — Gemini will pick a sensible default.

## Building the URL

1. **Pick the surface.** Default to Gemini. Switch to Stitch only when the user explicitly says Stitch or describes a UI/mockup design task that fits Stitch's scope.
2. **Pick the tool** (Gemini only) using the alias table above. If unsure, omit it.
3. **URL-encode the prompt** using standard percent-encoding. Newlines become `%0A`. Spaces can be `%20` or `+` (prefer `%20` for readability). Pass raw text — the receiving page handles HTML escaping.
4. **Assemble**: `?prompt=<encoded>` first, then `&tool=<alias>` if present.

## Opening the URL

```sh
${BROWSER:-xdg-open} "<url>"
```

Honor `$BROWSER` so the user can route to a specific browser or profile. Common pattern:

```sh
export BROWSER="google-chrome --profile-directory='Profile 1'"
```

On macOS, users typically set `$BROWSER` to `open` or to a specific app bundle path. Don't hardcode `xdg-open` without the `${BROWSER:-…}` fallback — it breaks Mac users.

## Worked Example

User: *"ask gemini to research the history of LISP"*

1. Surface: Gemini (default).
2. Tool: "research" → `research`.
3. Encode prompt `the history of LISP` → `the%20history%20of%20LISP`.
4. URL: `https://gemini.google.com/?prompt=the%20history%20of%20LISP&tool=research`.
5. Open: `${BROWSER:-xdg-open} "https://gemini.google.com/?prompt=the%20history%20of%20LISP&tool=research"`.

User: *"stitch a clean SaaS pricing page with three tiers"*

1. Surface: Stitch (explicit).
2. Tool: omit (Stitch does not support `tool`).
3. Encode prompt `a clean SaaS pricing page with three tiers` → `a%20clean%20SaaS%20pricing%20page%20with%20three%20tiers`.
4. URL: `https://stitch.withgoogle.com/?prompt=a%20clean%20SaaS%20pricing%20page%20with%20three%20tiers`.
5. Open with `${BROWSER:-xdg-open}`.

## Anti-patterns

| Anti-pattern | Signal | Fix |
|---|---|---|
| Auto-submitting the prompt | The skill tries to script a click or send-key after opening the URL | Pre-fill is the contract. Stop at the URL — the user submits. |
| Using `?q=` instead of `?prompt=` | URL has `?q=…` | The Gemini/Stitch URL contract is `prompt=`. `q=` does not pre-fill. |
| Adding `tool=` to a Stitch URL | URL is `stitch.withgoogle.com/?prompt=…&tool=…` | Drop the `tool=` — Stitch ignores it (and "ignore" is a generous read). |
| Hardcoding the browser | `xdg-open` or `chromium` literal in the command | Use `${BROWSER:-xdg-open}` — Mac and per-profile users depend on it. |
| Translating tool names | `&tool=Create%20image` | Use the short alias (`image`, `video`, `research`, etc.), not the human label. |
| Re-typing prompt content into the URL | Prompt in URL diverges from what the user said | Encode the user's prompt verbatim; only normalize whitespace. |
| Fabricating an unsupported tool | `&tool=summarize`, `&tool=translate`, etc. | Only the six aliases in the table are real. If the user wants something else, omit `tool=` entirely. |
