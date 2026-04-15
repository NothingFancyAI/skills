# spec-anchored-development

Treats specifications as living system maps with a bidirectional graph to implementing code. Specs define *what* and *why*; plans define *how* and *when*. Supports Python, Go, and TypeScript.

## What it does

- Three operating modes: **greenfield**, **existing codebase**, **maintenance**.
- Enforces a bidirectional graph: `Spec:` back-link comments in code, code map tables in specs.
- Language-specific guidance for Python, Go, and TypeScript.
- Mermaid diagram conventions for sequence, flowchart, state, and topology diagrams.
- Quality checklist and explicit anti-pattern catalog (god specs, micro specs, directory-driven breakdown).

## Usage

### Claude Code

```
claude --plugin-dir ./plugins/spec-anchored-development
```

Or via the marketplace, once installed.

### pi

```sh
pi -e ./plugins/spec-anchored-development    # ephemeral
pi install ./plugins/spec-anchored-development
```

### Codex

Install the full repository's Codex sidecar — see the root [`.codex/INSTALL.md`](../../.codex/INSTALL.md).

## Harness support

| Feature | Claude Code | Codex | pi |
|---|---|---|---|
| Skill (SKILL.md + references) | ✅ | ✅ | ✅ |
| Slash commands | — | — | — |
| Subagents | — | — | — |
| Hooks | — | — | — |
| MCP servers | — | — | — |

No harness-specific components — this plugin is pure skill content and runs identically in all three harnesses.

## Future directions

- **Agent-dispatched exploration.** The existing-codebase mode currently inspects the repository in the primary context. Dispatching sub-agents for exploration (one per subsystem, results harvested back) would keep the writing context clean while producing a more thorough system map. Not yet implemented — tracked as a known enhancement.
- **Spec drift detection via evals.** When the bidirectional graph exists, changes to code should be detectable via broken `Spec:` back-links. A lint pass could run in CI.

## Evals

Regression cases live in [`../../evals/cases/spec-anchored-development/cases.yaml`](../../evals/cases/spec-anchored-development/cases.yaml). Run locally:

```sh
uv run evals/framework/run.py --skill spec-anchored-development
```

## License

[CC BY-SA 4.0](../../LICENSE) — made by [Nothing Fancy](https://nothingfancy.ai).
