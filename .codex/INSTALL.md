# Installing Nothing Fancy Skills for Codex

This repository primarily targets Claude Code plugin discovery, but it also exposes a Codex-native skill tree under `.codex/skills/`. The entries there are symlinks back into the plugin-native skill directories, so both harnesses consume the same source of truth.

## Install

1. Clone the repository:
   ```sh
   git clone https://github.com/NothingFancyAI/skills.git ~/.codex/nothingfancy-skills
   ```

2. Run the installer to link the skills into your Codex skills directory:
   ```sh
   ~/.codex/nothingfancy-skills/.codex/scripts/install-for-codex.sh
   ```

3. Restart Codex so it discovers the new skills.

## Verify

```sh
ls -la ~/.codex/skills | grep nothingfancy-
```

You should see one symlink per skill, named `nothingfancy-<skill-name>`.

## Notes

- Claude Code discovery is unchanged — it uses `plugins/<name>/` and `.claude-plugin/marketplace.json`.
- Codex uses the `.codex/skills/` view, which symlinks back into the same source files.
- If you pull new skills, re-run the installer to pick them up.
- The `.codex/skills/` entries are validated in CI: every plugin skill must have a matching symlink. See [`.github/scripts/validate_codex_skills.py`](../.github/scripts/validate_codex_skills.py).
