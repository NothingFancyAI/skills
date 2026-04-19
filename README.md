# Nothing Fancy Skills [WIP]

A public marketplace of narrowly-scoped agent skills from [Nothing Fancy](https://nothingfancy.ai) — practical tools for teams adopting AI with confidence. Each skill is installable in isolation so you can run a tight, purpose-built session without importing a world you didn't ask for.

The goals is for this to run in **Claude Code**, **Codex**, and **pi** ([`@mariozechner/pi-coding-agent`](https://github.com/badlogic/pi-mono)). Skills are the common currency across all three — the portability spec is the [Agent Skills standard](https://agentskills.io/specification).  Full portability of the plugin toolset is uneven.

> **Evals are a first class citizen.** See [`evals/`](evals/) for the framework and the philosophy behind it.  This is still an **alpha-quality** concept, and has not actually be used; consider it a scaffolded proposal rather than an implementation.  It is really hard to test skills!  But this is the work now, understanding how to test this stuff, introduce incremental improvements, and understand skill weaknesses is essential improving output quality, and thereby increase agent independence.

## Installation

While marketplace support works, I currently only recommend this method.

### Claude Code — single plugin only

```
git clone https://github.com/NothingFancyAI/skills.git /path/to/skills
claude --plugin-dir /path/to/skills/plugins/<plugin-name>
```

This is the preferred mode when you want a narrow, focused session.

## Available Plugins

### Development

| Plugin | Description |
|--------|-------------|
| [spec-anchored-development](plugins/spec-anchored-development/) | Treats specifications as living system maps with a bidirectional graph to code. Supports Python, Go, and TypeScript. |
| [justfile](plugins/justfile/) | Authors and maintains global and project justfiles using opinionated conventions — positional arguments, working-directory attributes, no thin alias chains. |

### Generative AI

| Plugin | Description |
|--------|-------------|
| [nano-banana-prompting](plugins/nano-banana-prompting/) | Crafts and reviews prompts for Google's Nano Banana 2 (Gemini 3.1 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image) image generation and editing models — frameworks, camera/lighting direction, and text rendering. |

## Philosophy

Read [`AGENTS.md`](AGENTS.md) before authoring. The short version:

- **Narrow scope per plugin.** If you can't describe it in one line, it should be two plugins.
- **Behavioral guidance over reference dumps.** Teach judgment; don't paste specs.
- **Evals are the quality bar.** Every skill ships with a regression suite in `evals/cases/`. Untested skills don't merit public distribution.
- **Harness-neutral where possible.** Favor the Agent Skills spec; isolate Claude-specific or pi-specific components.
- **Plain writing.** Third-person, concrete, specific. If it doesn't ship on Monday, it doesn't count.

## Contributing

See [`AGENTS.md`](AGENTS.md) for authoring guidelines, the quality bar, and the PR checklist.

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). Made by [Nothing Fancy](https://nothingfancy.ai).
