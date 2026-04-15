# Contributing Skills

This is the authoring guide for the Nothing Fancy skills marketplace. Read it before opening a PR.

## Philosophy

### Narrow scope wins

A skill should do one thing well enough that you'd install it on its own. If you have to list two capabilities with an "and," you probably have two skills.

The reason: users should be able to run `claude --plugin-dir ./plugins/<name>` or `pi -e ./plugins/<name>` for a single session and get exactly the context they need, no more. Narrow scope is what makes that possible. A plugin that bundles five loosely-related capabilities forces every session to import all five.

### Behavioral guidance over reference dumps

A skill is a **judgment-bearing tool**, not a wiki page. Don't paste the full spec of a library into `SKILL.md` — teach when to reach for which tool, what the failure modes look like, and when to stop.

The `spec-anchored-development` skill doesn't include the full Mermaid grammar; it teaches which diagram type to pick for which situation. The `justfile` skill doesn't enumerate every `just` feature; it teaches an opinionated subset and explicitly flags the anti-pattern (alias chains).

Explain WHY, not just WHAT. Anti-patterns belong in the skill, with the reasoning.

### Evals are the quality bar

Every skill in this marketplace ships with cases in [`evals/cases/<skill-name>/cases.yaml`](evals/). A skill without evals is an untested skill, and untested skills don't graduate to public distribution.

Evals in this repo are not only regression tests. They are **cross-harness comparison suites**: the same task evaluated across Claude Code, Codex, and pi — sometimes across multiple models in each. Model jaggedness is real, and the honest answer to "which is better at X" is to run it.

See [`evals/README.md`](evals/README.md) for the framework and the scoring philosophy.

### Harness neutrality where possible

Skills are the common currency across Claude Code, Codex, and pi — the [Agent Skills spec](https://agentskills.io/specification) is shared. Author to the common denominator:

- Use `$ARGUMENTS` in slash commands, not pi-specific `$1`/`$2`, unless you're intentionally pi-only.
- Don't hardcode tool names like `Bash` or `Edit` in the skill body; say "run the shell command" or "edit the file."
- Put Claude-only components (hooks, agents, MCP servers) in `hooks/`, `agents/`, `.mcp.json` at the plugin root — they're auto-discovered by Claude and ignored by pi.
- Put pi-only extensions in `extensions/` with a `package.json` referencing them.
- Document harness gaps in the plugin's `README.md` under a **Harness support** section.

### Plain writing

- Third-person, concrete descriptions. "Authors justfiles using opinionated conventions" — not "An elegant tool to empower your workflow."
- Real triggers in `description:`. A skill that says "Use when working with Python" will never fire; one that says "Use when asked to set up a new Python project, migrate from setup.py, or configure pytest" will.
- If the skill has a sharp edge or a known failure mode, document it. Pretending the skill is flawless loses user trust on the first bad run.

## Resources

- [Agent Skills specification](https://agentskills.io/specification) — the shared contract
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins) — Claude-specific manifest and discovery rules
- [Claude Code Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — progressive disclosure, degrees of freedom
- [pi docs](https://github.com/badlogic/pi-mono) — extensions, prompt templates, package structure

## Technical Reference

### Plugin Structure

```
plugins/<plugin-name>/
  .claude-plugin/
    plugin.json           # Claude Code manifest (name, version, description, author)
  package.json            # pi manifest (npm metadata + "pi" key)
  README.md               # plugin overview, harness support, future directions
  skills/
    <skill-name>/
      SKILL.md            # entry point with frontmatter
      references/         # optional: detailed docs, one level deep
      workflows/          # optional: step-by-step guides
      scripts/            # optional: utility scripts (PEP 723 if Python)
  commands/               # optional: slash commands (Claude + pi prompt templates)
  agents/                 # optional: Claude subagents (no pi equivalent)
  hooks/                  # optional: Claude hooks (no pi file-format equivalent)
  extensions/             # optional: pi TypeScript extensions
```

**Important:** component directories live at the plugin root, NOT inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

### Frontmatter

```yaml
---
name: skill-name              # kebab-case, matches parent directory, ≤64 chars
description: "Third-person description of what it does and when to use it, with concrete triggers"
allowed-tools:                # optional: Claude-only, restricts tool access
  - Read
  - Grep
---
```

### Required sections

Every `SKILL.md` must include:

```markdown
## When to Use
[Specific, concrete scenarios where this skill applies]

## When NOT to Use
[Scenarios where another approach is better — prevents misfire]
```

### Naming conventions

- **kebab-case**: `spec-anchored-development`, not `SpecAnchoredDevelopment`.
- **Gerund form or recognizable noun**: prefer `authoring-justfiles` or `analyzing-logs`; recognizable tool names like `justfile` are acceptable when they match the primary concept exactly.
- **Avoid vague names**: `helper`, `utils`, `tools`, `misc`.
- **Avoid reserved words**: `anthropic`, `claude`, `openai`.

### Path handling

- Use relative paths from the skill directory.
- Never hardcode `/home/...`, `/Users/...`, or `C:\...`.
- Use forward slashes (`/`) even on Windows.

### Python scripts

When skills include Python scripts with dependencies:

1. **PEP 723 inline metadata:**
   ```python
   # /// script
   # requires-python = ">=3.11"
   # dependencies = ["requests>=2.28"]
   # ///
   ```

2. **`uv run`** for execution:
   ```bash
   uv run scripts/process.py input.txt
   ```

3. **`pyproject.toml`** in `scripts/` if you need dev tooling (ruff, mypy).

### Content organization

- Keep `SKILL.md` **under 500 lines**. Split into `references/` or `workflows/` for detail.
- **Progressive disclosure**: quick start in `SKILL.md`, details in linked files.
- **One level deep**: `SKILL.md` links to files, files don't chain to more files. (Directory depth like `references/languages/python.md` is fine — reference *chains* are not.)

## Quality Standards

### Description quality

Your skill's description is its trigger. A vague description will never fire; an overfit one will fire for the wrong thing.

- **Third-person voice:** "Audits GitHub workflows for AI agent risks" not "I help you audit workflows."
- **Concrete triggers:** "Use when asked to scaffold a justfile, migrate from Makefile, or add a new just recipe" beats "Command-runner helper."
- **Name the domain:** "Python, Go, and TypeScript" beats "multiple languages."

### Required evals

Every skill must have starter cases in [`evals/cases/<skill-name>/cases.yaml`](evals/). Minimum:

- One **positive case**: a realistic trigger prompt, with assertions that the skill's guidance is followed.
- One **negative case**: a prompt that looks related but should NOT fire the skill, asserting it isn't invoked.
- One **edge case**: an ambiguous or adversarial input that historically broke the skill, locked in as a regression test.

Run the suite locally before submitting: `uv run evals/framework/run.py --skill <name>`.

### Security / audit skills

Audit or security-adjacent skills must also include:

```markdown
## Rationalizations to Reject
[Common shortcuts or rationalizations that lead to missed findings — with the reasoning]
```

## PR Checklist

Before submitting:

**Technical (CI validates these):**
- [ ] Valid YAML frontmatter with `name` and `description`
- [ ] Name is kebab-case, ≤64 characters, matches directory
- [ ] All referenced files exist
- [ ] No hardcoded absolute paths
- [ ] `python3 .github/scripts/validate_plugin_metadata.py` passes
- [ ] `python3 .github/scripts/validate_skill_frontmatter.py` passes
- [ ] `python3 .github/scripts/validate_codex_skills.py` passes

**Quality (reviewers check these):**
- [ ] Description has concrete triggers (third-person, specific)
- [ ] "When to Use" and "When NOT to Use" sections present
- [ ] Explains WHY, not just WHAT
- [ ] Anti-patterns documented with reasoning
- [ ] At least positive + negative + edge eval cases
- [ ] Harness support documented in plugin README

**Documentation:**
- [ ] Plugin has `README.md` with description, usage, harness support
- [ ] Added to root `README.md` catalog table
- [ ] Registered in root `.claude-plugin/marketplace.json`
- [ ] Codex sidecar symlink exists (`.codex/skills/<name>` → plugin skill dir)
- [ ] Added to `CODEOWNERS`

**Version updates (existing plugins):**
- [ ] Version bumped in `plugins/<name>/.claude-plugin/plugin.json`
- [ ] Matching version bump in root `.claude-plugin/marketplace.json`
- [ ] Clients only update on version increase — ship a real bump
