#!/bin/bash
# Install Nothing Fancy skills into ~/.codex/skills/ as symlinks.
#
# This script links every entry under .codex/skills/ into the user's
# Codex skills directory, prefixed with "nothingfancy-" so they don't
# collide with other providers.
#
# Re-run after pulling new skills to pick them up.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SOURCE_DIR="${REPO_ROOT}/.codex/skills"
TARGET_DIR="${HOME}/.codex/skills"

mkdir -p "${TARGET_DIR}"

if [ ! -d "${SOURCE_DIR}" ]; then
  echo "ERROR: Source directory does not exist: ${SOURCE_DIR}" >&2
  exit 1
fi

count=0
for skill_dir in "${SOURCE_DIR}"/*; do
  [ -e "${skill_dir}" ] || continue
  skill_name="$(basename "${skill_dir}")"
  target_link="${TARGET_DIR}/nothingfancy-${skill_name}"
  ln -sfn "${skill_dir}" "${target_link}"
  count=$((count + 1))
done

if [ "${count}" -eq 0 ]; then
  echo "WARNING: No skills found in ${SOURCE_DIR}" >&2
  exit 1
fi

echo "Installed ${count} Nothing Fancy Codex skills into ${TARGET_DIR}"
echo "Restart Codex for the new skills to be discovered."
