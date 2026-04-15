# justfile

Authors and maintains global and project justfiles using opinionated conventions.

## What it does

Encodes a specific, opinionated style:

- **One global justfile** at `$HOME/justfile` for personal automations.
- **Positional arguments** via `set positional-arguments` so generic commands accept passthrough args.
- **Working-directory attributes** (`[working-directory: 'subdir']`) instead of `cd x && y`.
- **Shebang recipes** for anything beyond a single shell invocation.
- **No thin alias chains** — one wrapper recipe with passthrough args beats five near-identical aliases.

Every recipe gets a crisp comment. The default recipe lists available commands.

## Usage

### Claude Code

```sh
claude --plugin-dir ./plugins/justfile
```

### pi

```sh
pi -e ./plugins/justfile
```

### Codex

See the root [`.codex/INSTALL.md`](../../.codex/INSTALL.md).

## Harness support

| Feature | Claude Code | Codex | pi |
|---|---|---|---|
| Skill (SKILL.md) | ✅ | ✅ | ✅ |

Pure skill content — runs identically in all three harnesses.

## Evals

Regression cases live in [`../../evals/cases/justfile/cases.yaml`](../../evals/cases/justfile/cases.yaml).

```sh
uv run evals/framework/run.py --skill justfile
```

## License

[CC BY-SA 4.0](../../LICENSE) — made by [Nothing Fancy](https://nothingfancy.ai).
