---
name: creating-plugins
description: Walks through creating a new plugin for the Nothing Fancy skills marketplace — naming, description drafting, directory setup, SKILL.md content, starter eval cases, metadata sync, and verification. Use when asked to add, create, scaffold, or write a new plugin in this repository, or when starting work on a new skill for the NF marketplace.
---

# creating-plugins

Creates a new plugin for the Nothing Fancy skills marketplace. Every step is a judgment call, not a template fill. Read [CLAUDE.md](../../../CLAUDE.md) before starting — it's the quality bar this skill enforces.

## When to Use

- The user asks to add, create, scaffold, or write a new plugin for this repository.
- The user has identified a gap in the marketplace and wants to start a new skill.
- An existing `plugin.json` needs to be created (e.g., a skill was drafted locally and now needs to be promoted to a public plugin).

## When NOT to Use

- The user wants to **edit** an existing plugin. Edit the files directly.
- The user wants a **private, repo-local skill** (lives in their project's `.claude/skills/`, not this marketplace). Point them at Claude Code docs.
- The user wants to update plugin metadata (version, description) without other changes. That's a direct edit to `plugin.json` + `marketplace.json`, no scaffolding needed.
- The user hasn't decided what the plugin does. Ask clarifying questions first — use [ask-questions-if-underspecified](https://github.com/trailofbits/skills/tree/main/plugins/ask-questions-if-underspecified) as a model if they're vague.

## Workflow

Follow in order. Every step is a judgment call. Don't skip the thinking steps to rush to the mechanical ones.

### 1. Confirm scope and name

Before touching files, answer these:

- **What does this plugin do in one sentence?** If you can't, it's two plugins. Split it.
- **What's the kebab-case name?** Prefer gerund form (`authoring-X`, `analyzing-Y`) or a recognizable tool noun (`justfile`, `ripgrep`). Avoid vague names (`helper`, `utils`). Avoid reserved words (`anthropic`, `claude`, `openai`).
- **Does the name collide?** Check `ls plugins/` and `cat .claude-plugin/marketplace.json`. Also check the pi default command list — pi doesn't namespace, so `/hello`, `/test`, `/run` etc. could collide with built-ins.

See [references/naming.md](references/naming.md) for the decision tree and anti-patterns.

### 2. Draft the description

The `description:` field is the trigger. A vague description will never fire; an overfit one will fire for the wrong thing.

Write it as if a user asked a random question and a matching-algorithm had to decide whether to surface your skill. Include:

- **Third-person verb**: "Authors justfiles..." not "I help you author justfiles."
- **Concrete triggers**: name the kinds of prompts that should fire it. "Use when writing, editing, or reviewing a justfile..." not "Command-runner helper."
- **Scope limits when relevant**: "Supports Python, Go, and TypeScript" tells the matcher not to fire for Rust.

Run the **"will this fire?"** test before moving on: invent three plausible user prompts, and for each, ask whether your description would trigger the skill. If any of them feels ambiguous, rewrite.

See [references/naming.md](references/naming.md) for worked examples.

### 3. Decide harness support

This marketplace targets Claude Code, Codex, and pi. Your plugin might not support all three.

- **Skill-only plugins** (SKILL.md + references, no commands/hooks/agents/MCP) → portable to all three. Default case.
- **Plugins with Claude-specific components** (hooks, subagents, MCP servers) → Claude-only for those features. Document the gap in the plugin README under a **Harness support** table.
- **Plugins with pi-specific components** (TypeScript extensions, tool registration) → pi-only for those features. Same — document the gap.

Consult the [pi docs](https://github.com/badlogic/pi-mono) before adding non-skill components — they document the extensions, prompt templates, and tool-registration surfaces that don't exist in Claude. Any harness gap should be called out in the plugin's README.

### 4. Scaffold the directory

Copy the templates to `plugins/<name>/` and fill in the `{{placeholders}}`. The templates live in [`templates/`](templates/) next to this SKILL.md.

Required:

```
plugins/<name>/
  .claude-plugin/plugin.json    ← from templates/plugin.json
  package.json                  ← from templates/package.json (pi manifest)
  README.md                     ← from templates/README.md.tmpl
  skills/<name>/
    SKILL.md                    ← from templates/SKILL.md.tmpl
```

Optional (add only if you need them):

```
  commands/                     ← slash commands (Claude + pi prompt templates)
  agents/                       ← Claude subagents (no pi equivalent)
  hooks/                        ← Claude hooks (no pi file-format equivalent)
  extensions/                   ← pi TypeScript extensions
  skills/<name>/references/     ← long-form docs, one level deep
  skills/<name>/workflows/      ← step-by-step guides
  skills/<name>/scripts/        ← utility scripts (PEP 723 if Python)
```

### 5. Write the SKILL.md body

The templates give you the skeleton. The hard work is the content. Read [CLAUDE.md](../../../CLAUDE.md) under **Quality Standards** before you start, and keep the SKILL.md under **500 lines**.

Mandatory structure:

1. Frontmatter (`name`, `description`).
2. H1 title.
3. One-paragraph explanation of what the skill does and its guiding principle.
4. `## When to Use` — concrete scenarios.
5. `## When NOT to Use` — scenarios where another tool is better. Prevents misfire.
6. Body — the actual guidance, organized as the user needs it.
7. Anti-patterns table if applicable — document the wrong approaches with reasoning.

**Behavioral guidance over reference dumps.** Don't paste entire specs. Teach judgment: when to reach for which tool, what failure looks like, when to stop. Explain WHY, not just WHAT.

If the skill is long, split into `references/` files (one level deep, not chained). Link them from the main SKILL.md.

### 6. Write starter eval cases

Every plugin MUST ship at least three eval cases in `evals/cases/<name>/cases.yaml`. This is non-negotiable.

- **Positive case** — a realistic prompt that SHOULD fire the skill, with assertions that the skill's guidance is followed.
- **Negative case** — a prompt that *looks* related but should NOT fire the skill.
- **Edge case** — an adversarial or historically-broken input that locks in a regression.

Use `llm-rubric` assertions for behavior, not just string matching. String matching on specific tokens is brittle; rubric assertions on "does the response follow the skill's guidance?" is robust.

See [references/eval-cases.md](references/eval-cases.md) for worked examples of all three types.

Start from [`templates/cases.yaml.tmpl`](templates/cases.yaml.tmpl).

### 7. Create the Codex sidecar symlink

Every plugin skill must have a Codex sidecar entry. The validator checks this.

```sh
cd .codex/skills
ln -sfn ../../plugins/<name>/skills/<name> <name>
```

One symlink per skill (not per plugin) — if a plugin has multiple skills, each gets its own sidecar.

### 8. Sync metadata

Four files need matching entries. The `validate_plugin_metadata.py` validator enforces this, but get it right first pass:

1. **`.claude-plugin/marketplace.json`** — add a `plugins[]` entry with `name`, `version`, `description`, `author`, `source: ./plugins/<name>`. Must match `plugin.json` exactly for name/version/description.
2. **Root `README.md`** — add a row to the appropriate category table. Create a new category heading if no existing one fits.
3. **`CODEOWNERS`** — add `/plugins/<name>/ @<gh-handle>`.
4. **Plugin `README.md`** — one section per file: What it does, Usage (Claude / Codex / pi), Harness support table, Evals link, License.

### 9. Verify

Run the full gate. Iterate on any failure.

```sh
just check
```

This runs:
- `validate_plugin_metadata.py` — catches marketplace/README/CODEOWNERS drift.
- `validate_skill_frontmatter.py` — catches missing frontmatter, wrong name, missing When-to-Use sections.
- `validate_codex_skills.py` — catches missing Codex symlink.
- `ruff` — lints any Python scripts you added.
- Eval dry-run — confirms `cases.yaml` parses and case count is sane.

If you added Python, `just fmt` auto-fixes lint issues before re-running `just check`.

### 10. Commit

Only after `just check` passes. Keep the commit message descriptive: "Add <name> plugin" is fine as a subject, but mention the skill's scope in the body — it helps PR review.

## Anti-patterns

| Anti-pattern | Signal | Fix |
|---|---|---|
| Template-driven content | SKILL.md reads like "this skill does X. Use it when you need X." | Rewrite from scratch. Templates are skeletons, not defaults. |
| Vague description | "Helps with Python" | Add concrete triggers. Name the situations where it should fire. |
| Missing negative case | Only positive cases in cases.yaml | Always add at least one negative. Untriggered is as important as triggered. |
| String-match-only assertions | Every assertion is `type: contains` | Add at least one `llm-rubric` — matches behavior, not tokens. |
| Bloated SKILL.md | >500 lines, everything in one file | Split into `references/`. One level deep, no chains. |
| Reference dump | SKILL.md pastes a full library's API | Teach judgment. Link to the library's docs, don't reproduce them. |
| Claude-specific with no gap note | Uses Claude hooks, no harness table in README | Document the harness gap. Users running pi or Codex deserve to know. |
| Skipping verification | Commits without `just check` | Always run the gate. Broken metadata is visible in CI anyway. |

## Quick reference

```sh
# After answering steps 1-3 (name, description, harness support):
cp -r .claude/skills/creating-plugins/templates/skeleton plugins/<name>   # (see templates/)
# Edit files, fill in placeholders, write content.

cd .codex/skills && ln -sfn ../../plugins/<name>/skills/<name> <name> && cd -

# Add entries to .claude-plugin/marketplace.json, README.md, CODEOWNERS.

just check
git add -A && git commit -m "Add <name> plugin"
```
