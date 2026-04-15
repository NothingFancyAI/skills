---
name: justfile
description: Authors and maintains global and project justfiles using opinionated conventions — positional arguments, working-directory attributes, shebang recipes for anything nontrivial, and avoiding thin alias chains. Use when writing, editing, refactoring, or reviewing a justfile, setting up `$HOME/justfile` for the first time, migrating from Makefile to just, or when the user mentions just or command runners.
---

# justfile

Opinionated conventions for authoring justfiles. The global personal justfile lives at `$HOME/justfile`; project-specific recipes live at `./justfile` in the project root.

## When to Use

- The user asks to create, edit, refactor, or review a justfile.
- The user is migrating from a Makefile, shell aliases, or npm scripts to `just`.
- The user wants to set up a global `$HOME/justfile` for personal automations.
- The user mentions "just", "justfile", or asks about command runners and task orchestration.

## When NOT to Use

- The user wants a CI-only task runner — use a CI-native tool (GitHub Actions, etc.), not a justfile.
- The user needs a build system with dependency tracking (incremental builds, file-level dependencies). Use `make`, `ninja`, or a real build tool; `just` is a command runner, not a build system.
- The user's task is a single shell invocation that doesn't need naming or documenting. Don't create a justfile for one command.
- The user's team already has a strong convention that contradicts these opinions. Flag the conflict rather than silently overriding.

## Conventions

### Default recipe lists commands

Every justfile starts with this so `just` alone is informative:

```justfile
default:
    @just --list
```

### Positional arguments by default

Almost always, you want passthrough args so a generic recipe can forward them to its underlying command:

```justfile
set positional-arguments

@mycommand *args='':
    mycommand "$@"
```

### Comment every recipe

Every recipe gets a short, precise comment on the line above it. "What it does" in one clause; "why" if the why isn't obvious:

```justfile
# Build the release artifact into ./dist
build:
    ./bin/build

# Run the full test suite; set PYTEST_ARGS for filtering
test:
    ./bin/test
```

Vague comments like `# build stuff` are worse than none — they look informative but aren't.

### Working-directory attribute, not cd chains

```justfile
[working-directory: 'services/api']
api-logs:
    tail -f logs/app.log
```

Prefer this over `cd services/api && tail -f logs/app.log`. The attribute is declarative and doesn't corrupt the shell process state if the recipe has multiple lines.

### Environment variables

Justfile string interpolation uses `{{...}}` for just variables and `${...}` for shell variables. Inside recipe bodies, shell substitution works normally:

```justfile
print_home_folder:
    echo "HOME is: '${HOME}'"
```

### Shebang recipes for anything nontrivial

Once a recipe is more than a single command, switch to a shebang recipe so you get real shell semantics (pipes, loops, `set -euo pipefail`):

```justfile
foo:
    #!/usr/bin/env bash
    set -euo pipefail
    hello='Yo'
    echo "$hello from Bash!"
```

The shebang runs the entire recipe body in one shell process, which is the only way to keep variables and `cd` state between lines.

### Avoid thin alias chains

There are sharply declining marginal returns on each additional recipe that just aliases another command. If you have five recipes that all `cd terraform && terraform <verb>`, collapse them into one wrapper with passthrough args.

**Bad** — noise, and every new subcommand needs a new recipe:

```justfile
tf-init:
    cd terraform && terraform init

tf-plan:
    cd terraform && terraform plan

tf-apply:
    cd terraform && terraform apply
```

**Good** — one recipe, every terraform subcommand works:

```justfile
# Terraform wrapper: init, plan, apply, state list, output
[working-directory: 'terraform']
terraform *args:
    terraform "$@"
```

Call as `just terraform init`, `just terraform plan -out=plan.out`, etc.

The exception: if a recipe materially simplifies the invocation (bundles several commands, sets environment variables, handles errors), it earns its keep. A thin wrapper that only adds a `cd` does not.

## Anti-patterns

| Anti-pattern | Signal | Fix |
|---|---|---|
| Alias proliferation | Five recipes that differ only by the subcommand they pass to the underlying tool | One wrapper recipe with `*args` |
| Silent failures in multi-line recipes | Using plain `recipe:` with multi-line bodies and no `set -e` | Switch to shebang recipe with `set -euo pipefail` |
| `cd` chains | `cd subdir && command` repeated across recipes | Use `[working-directory: 'subdir']` |
| Vague or missing comments | `# stuff`, `# build`, or no comment at all | One-line precise description; why if non-obvious |
| Hidden positional args | Recipe takes arguments but doesn't `set positional-arguments` | Add the directive at the top of the file |
| Justfile-as-build-system | Recipes with file-level dependencies, timestamps, or incremental logic | Use `make` or a real build tool |

## Quick reference

- `just` → run default recipe (which should be `@just --list`)
- `just --list` → list all recipes
- `just --show <recipe>` → print a recipe's body without running it
- `just --choose` → interactive picker
- `just --evaluate` → print the values of all variables
