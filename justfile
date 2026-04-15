# Nothing Fancy skills — repo automation.
# Dogfoods the conventions taught by plugins/justfile.

set positional-arguments

# Default: list available recipes
default:
    @just --list

# Run all three metadata validators with fail-fast semantics: plugin metadata, skill frontmatter, Codex sidecar
validate:
    #!/usr/bin/env bash
    set -euo pipefail
    uv run .github/scripts/validate_plugin_metadata.py
    uv run .github/scripts/validate_skill_frontmatter.py
    uv run .github/scripts/validate_codex_skills.py

# Lint Python scripts without modifying anything: ruff check + format check
lint:
    #!/usr/bin/env bash
    set -euo pipefail
    uvx ruff check .
    uvx ruff format --check .

# Auto-fix lint issues and reformat Python scripts
fmt:
    #!/usr/bin/env bash
    set -euo pipefail
    uvx ruff check --fix .
    uvx ruff format .

# Full quality gate: validate metadata, lint, and dry-run the eval suite (fail-fast)
check:
    #!/usr/bin/env bash
    set -euo pipefail
    just validate
    just lint
    uv run evals/framework/run.py --dry-run

# Run the eval framework; pass --list-skills, --dry-run, --skill NAME, or --provider ID
@eval *args='':
    uv run evals/framework/run.py "$@"

# Report plugin, skill, and eval-case counts; flag skills missing eval coverage
stats:
    uv run .github/scripts/stats.py

# Install the Codex sidecar symlinks into ~/.codex/skills/
install-codex:
    ./.codex/scripts/install-for-codex.sh
