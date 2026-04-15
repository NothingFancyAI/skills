# Eval case authoring reference

Every plugin ships three required eval cases: **positive**, **negative**, **edge**. This file gives worked examples and the reasoning behind the patterns.

Read [`evals/README.md`](../../../../evals/README.md) for the framework and cross-harness grid philosophy first.

## The three required types

### Positive case

A realistic user prompt that SHOULD fire the skill, with assertions that the response follows the skill's guidance.

**What to include:**
- A prompt phrased the way a real user would phrase it (not artificially perfect).
- Assertions that check for the *behavior* the skill teaches, not just keywords.
- At least one `llm-rubric` assertion — the model is the judge of whether guidance is followed.

**Worked example** (from `justfile/cases.yaml`):

```yaml
- description: "Positive — set up global justfile from scratch"
  vars:
    prompt: |
      I want to set up a global justfile at ~/justfile for my personal
      automations. Can you scaffold the basics and add a recipe that wraps
      terraform calls for my infra/ directory?
  assert:
    - type: contains
      value: "default:"
    - type: contains
      value: "just --list"
    - type: contains-any
      value:
        - "set positional-arguments"
        - "*args"
    - type: contains-any
      value:
        - "working-directory"
        - "[working-directory:"
    - type: llm-rubric
      value: |
        The scaffold should: (1) include a default recipe calling
        `@just --list`, (2) use `set positional-arguments`, (3) include
        commented recipes, (4) wrap terraform via a single passthrough
        recipe with `[working-directory: 'infra']`, NOT separate
        tf-init/tf-plan/tf-apply aliases.
```

Why this works:
- The prompt is specific enough to trigger the skill reliably.
- String assertions catch the mechanical requirements (`default:`, `just --list`).
- `contains-any` allows alternate phrasing the skill might use.
- The `llm-rubric` captures the *hard* part — that the wrapped terraform recipe avoids the alias-chain anti-pattern, which no string match could verify.

### Negative case

A prompt that looks related but should NOT fire the skill. If the skill fires anyway, it's over-triggering.

**What to include:**
- A prompt in the adjacent space but with a different real intent.
- Assertions that the skill's signature output is *absent*.
- An `llm-rubric` checking that the response addresses the actual intent instead of the wrong one.

**Worked example** (from `justfile/cases.yaml`):

```yaml
- description: "Negative — user wants make, not just"
  vars:
    prompt: |
      I'm building a C project and need a build system with proper file
      dependencies and incremental compilation. What should I use?
  assert:
    - type: not-contains
      value: "justfile"
    - type: llm-rubric
      value: |
        The response should recommend `make` or a real build tool, NOT
        a justfile. The skill should explicitly recognize that `just` is
        a command runner, not a build system with dependency tracking.
```

Why this works:
- The prompt sounds task-runner-adjacent ("build system," "what should I use?") but really needs `make`.
- `not-contains: justfile` catches the most obvious over-trigger.
- The rubric enforces the skill's documented scope limit: just is a command runner, not a build system.

### Edge case

An adversarial or historically-broken input, locked in as a regression. This is the case you add *after* fixing a bug.

**What to include:**
- The exact input that broke the skill (even if lightly paraphrased to avoid leaking user data).
- Assertions that specifically catch the broken behavior.
- A comment in the cases.yaml or the description linking to the incident / commit that motivated the case.

**Worked example** (from `justfile/cases.yaml`):

```yaml
- description: "Edge — multi-line recipe that needs shebang"
  vars:
    prompt: |
      Write a just recipe called `deploy` that: activates a venv, sets
      DEPLOY_ENV=staging, runs ./bin/migrate, and then ./bin/deploy. It
      should exit if any step fails.
  assert:
    - type: contains
      value: "#!/usr/bin/env bash"
    - type: contains
      value: "set -euo pipefail"
    - type: llm-rubric
      value: |
        Because the recipe has multiple dependent steps and needs
        fail-fast semantics, the answer MUST use a shebang recipe with
        `set -euo pipefail`. A plain multi-line recipe would silently
        continue on failure.
```

Why this works:
- The prompt is the kind of request that *naively* produces a broken recipe (plain multi-line with no fail-fast).
- The assertions lock in the correct fix (shebang + `set -euo pipefail`).
- The rubric explains WHY the correct answer is required — so if the test fails later, the reviewer immediately understands the regression.

## Assertion types — when to use each

| Type | Use for | Example |
|---|---|---|
| `contains` | Mechanical output that MUST be present | `default:` in a justfile response |
| `not-contains` | Mechanical output that MUST be absent | `justfile` in a make-recommendation |
| `contains-any` | Alternate phrasings are all acceptable | `set positional-arguments` OR `*args` |
| `contains-all` | Multiple things must all be present | Rarely the right call; prefer multiple `contains` |
| `llm-rubric` | Behavior, judgment, or anti-patterns | Does the response avoid the alias-chain? |
| `javascript` / `python` | Structural checks, parsing output | JSON shape validation |

**The default should be mixing string assertions (mechanical) with one or more `llm-rubric` (behavioral).** String-only is brittle; rubric-only is slow and expensive. The mix gives fast feedback on the mechanical bits and deep feedback on the judgment bits.

## Cross-harness grid

Recall from `evals/README.md`: cases run across the (harness × model) grid. Don't write assertions that only work for one model's phrasing. If a string match depends on "Claude will say X," rewrite as `contains-any` with alternatives or convert to a rubric.

The point of the grid is to find (harness × model) cells where guidance *isn't* followed. Brittle assertions hide that signal.

## How many cases?

**Minimum: three** (positive, negative, edge).

**Good: five to seven.** Multiple positive cases for different triggers the skill should handle, one or two negative cases for different misfire risks, one or two edge cases for known failure modes.

**Too many: >15.** Diminishing returns, slow suite, contributors stop running it. Prefer quality over quantity. Each case should teach the reviewer something about what the skill does.
