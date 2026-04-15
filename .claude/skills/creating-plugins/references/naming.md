# Naming and description reference

The name and description together determine whether a skill fires for the right prompts. Bad choices here waste every downstream improvement — a great SKILL.md body that never fires helps nobody.

## Name decision tree

1. **Is there an obvious tool or concept name?** Use it directly. `justfile`, `ripgrep`, `mermaid`. Recognizable nouns beat invented gerunds for tool-specific skills.

2. **Is it a generic activity?** Use gerund form. `authoring-justfiles`, `analyzing-logs`, `reviewing-prs`. The gerund makes it clear this is a verb-shaped skill.

3. **Is it a domain?** Kebab-case noun phrase. `spec-anchored-development`, `constant-time-analysis`, `supply-chain-audit`. Avoid single-word domains (`security`, `testing`) — too broad to trigger usefully.

## Anti-patterns

| Name | Why it's bad | Fix |
|---|---|---|
| `helper` | Vague. Every skill is a helper. | Name the activity or domain. |
| `utils` | Same. Describes *nothing*. | Ditto. |
| `tools` | Same. | Ditto. |
| `misc` | If you can't name it, it's two skills. | Split. |
| `python` | Too broad — what *about* Python? | `modernizing-python-projects`, `profiling-python` |
| `ai-helper` | Vague AND reserved-word-adjacent. | Specific activity. |
| `claude-thing` | Reserved word (`claude`). | Drop the vendor name. |
| `helpTest` | camelCase. | `help-test`, then rethink because this is still vague. |

## Description decision tree

1. **Write a third-person verb phrase** that names the activity. "Authors X," "Audits Y," "Analyzes Z." Not "I help you..." Not "A tool for..."

2. **Add concrete triggers**. Prompt-shaped phrases. "Use when writing, editing, or reviewing a justfile..." The matcher literally uses these to decide whether to surface the skill.

3. **State scope or limits** when they'd prevent misfire. "Supports Python, Go, and TypeScript." "Smart contracts only — Solidity and Move." "Does not cover release management."

4. **Mention the key tool or concept** by name once. Users search for the tool name; so will the matcher.

## "Will this fire?" test

Before committing a description, do this:

1. Invent three realistic user prompts that *should* trigger the skill.
2. Invent three realistic user prompts that *should NOT* trigger it but sound related.
3. Read your description. For each prompt, decide: would this description fire?
4. If any expected-fire prompt feels ambiguous, the description is too vague. Add triggers.
5. If any expected-miss prompt feels like it *would* fire, the description is too broad. Add scope limits.

This is the single most effective authoring exercise. Skipping it is the #1 reason skills misfire.

## Worked examples

### Good: `justfile`

```yaml
name: justfile
description: Authors and maintains global and project justfiles using opinionated conventions — positional arguments, working-directory attributes, shebang recipes for anything nontrivial, and avoiding thin alias chains. Use when writing, editing, refactoring, or reviewing a justfile, setting up `$HOME/justfile` for the first time, migrating from Makefile to just, or when the user mentions just or command runners.
```

Why it works:
- Third-person verb: "Authors and maintains"
- Concrete triggers: "writing, editing, refactoring, or reviewing a justfile"
- Scope implied by the tool name
- Migration trigger ("migrating from Makefile") catches a common adjacent intent
- Mentions `$HOME/justfile` — specific enough that the matcher will surface it for "global task runner" questions

### Good: `spec-anchored-development`

```yaml
name: spec-anchored-development
description: Treats specifications as living system maps with a bidirectional graph to implementing code. Use when asked to create a spec, write a specification, generate a spec from code, maintain specs, sync specs with code, establish a spec-to-code graph, work in greenfield or brownfield spec mode, reverse-engineer a spec, or document system architecture. Supports Python, Go, and TypeScript projects.
```

Why it works:
- Unique philosophy stated up front ("living system maps")
- Eight concrete triggers, each a different user intent
- Explicit language scope limits misfire on Rust/Java/Ruby
- "Reverse-engineer" and "sync" both appear — catches the maintenance-mode intent

### Bad: `python-helper`

```yaml
name: python-helper
description: Helps with Python code.
```

Why it fails:
- Name is too broad and uses `helper`
- Description has no triggers — the matcher can't decide when to fire
- "Helps with" is filler — says nothing
- No scope, so the matcher will surface it for *every* Python prompt, guaranteeing false positives

### Bad: `advanced-reviewer`

```yaml
name: advanced-reviewer
description: An advanced code review tool with expert insights.
```

Why it fails:
- "Advanced" is marketing, not descriptive
- "Expert insights" is meaningless — the matcher can't act on it
- No mention of WHAT is being reviewed, for WHICH language, in response to WHICH user prompts
- Will either fire for everything or nothing, depending on matcher luck
