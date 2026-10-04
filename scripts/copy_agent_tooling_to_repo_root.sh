#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/copy_agent_tooling_to_repo_root.sh [--dry-run] [--include-agents-md] [target_root]

Copies the repo-local agent tooling into another project root.

This script is Codex-runtime-first:
- `.agents/` and `.codex/` are the active Codex surfaces
- legacy repo-root `codex/` mirrors are removed from the target if present
- generated runtime directories are replaced, not merged, so stale files do not survive

Default target_root:
  The parent directory of this repository. This matches the workflow where
  this repo is cloned inside the codebase you want to audit.

Copied paths:
  .github/agents   -> <target_root>/.github/agents
  .claude          -> <target_root>/.claude
  .claude-plugins  -> <target_root>/.claude-plugins (if present here)
  .agents          -> <target_root>/.agents
  .codex           -> <target_root>/.codex
                      This is the generated Codex runtime surface, including
                      repo-local skills, custom agents, shared references,
                      shared rules, and repo config.

Options:
  --dry-run            Print planned copy operations without writing files.
  --include-agents-md  Also copy AGENTS.md to <target_root>/AGENTS.md.
  -h, --help           Show this help text.

Examples:
  ./scripts/copy_agent_tooling_to_repo_root.sh
  ./scripts/copy_agent_tooling_to_repo_root.sh /path/to/target-repo
  ./scripts/copy_agent_tooling_to_repo_root.sh --dry-run /path/to/target-repo
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_TARGET_ROOT="$(cd "${SOURCE_ROOT}/.." && pwd)"

DRY_RUN=0
INCLUDE_AGENTS_MD=0
TARGET_ROOT=""

while (($# > 0)); do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --include-agents-md)
      INCLUDE_AGENTS_MD=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -n "${TARGET_ROOT}" ]]; then
        echo "Only one target_root argument is supported." >&2
        usage >&2
        exit 1
      fi
      TARGET_ROOT="$1"
      shift
      ;;
  esac
done

if [[ -z "${TARGET_ROOT}" ]]; then
  TARGET_ROOT="${DEFAULT_TARGET_ROOT}"
fi

TARGET_ROOT="$(cd "${TARGET_ROOT}" 2>/dev/null && pwd)" || {
  echo "Target root does not exist or is not accessible: ${TARGET_ROOT}" >&2
  exit 1
}

if [[ "${TARGET_ROOT}" == "${SOURCE_ROOT}" ]]; then
  echo "Refusing to copy into the source repository itself: ${SOURCE_ROOT}" >&2
  exit 1
fi

remove_path() {
  local dest_rel="$1"
  local dest="${TARGET_ROOT}/${dest_rel}"

  if [[ ! -e "${dest}" ]]; then
    return 0
  fi

  echo "Removing stale ${dest_rel}"
  if [[ "${DRY_RUN}" == "1" ]]; then
    return 0
  fi

  rm -rf "${dest}"
}

copy_dir() {
  local src_rel="$1"
  local dest_rel="$2"
  local optional="${3:-0}"

  local src="${SOURCE_ROOT}/${src_rel}"
  local dest="${TARGET_ROOT}/${dest_rel}"

  if [[ ! -d "${src}" ]]; then
    if [[ "${optional}" == "1" ]]; then
      echo "Skipping missing optional directory: ${src_rel}"
      return 0
    fi
    echo "Missing required source directory: ${src}" >&2
    return 1
  fi

  echo "Syncing ${src_rel} -> ${dest_rel}"
  if [[ "${DRY_RUN}" == "1" ]]; then
    return 0
  fi

  mkdir -p "${dest}"
  cp -a "${src}/." "${dest}/"
}

replace_dir() {
  local src_rel="$1"
  local dest_rel="$2"

  local src="${SOURCE_ROOT}/${src_rel}"
  local dest="${TARGET_ROOT}/${dest_rel}"

  if [[ ! -d "${src}" ]]; then
    echo "Missing required source directory: ${src}" >&2
    return 1
  fi

  echo "Replacing ${dest_rel} from ${src_rel}"
  if [[ "${DRY_RUN}" == "1" ]]; then
    return 0
  fi

  rm -rf "${dest}"
  mkdir -p "${dest}"
  cp -a "${src}/." "${dest}/"
}

copy_file() {
  local src_rel="$1"
  local dest_rel="$2"
  local optional="${3:-0}"

  local src="${SOURCE_ROOT}/${src_rel}"
  local dest="${TARGET_ROOT}/${dest_rel}"

  if [[ ! -f "${src}" ]]; then
    if [[ "${optional}" == "1" ]]; then
      echo "Skipping missing optional file: ${src_rel}"
      return 0
    fi
    echo "Missing required source file: ${src}" >&2
    return 1
  fi

  echo "Copying ${src_rel} -> ${dest_rel}"
  if [[ "${DRY_RUN}" == "1" ]]; then
    return 0
  fi

  mkdir -p "$(dirname "${dest}")"
  cp -a "${src}" "${dest}"
}

echo "Source root: ${SOURCE_ROOT}"
echo "Target root: ${TARGET_ROOT}"
if [[ "${DRY_RUN}" == "1" ]]; then
  echo "Mode: dry-run"
fi

remove_path "codex"
copy_dir ".github/agents" ".github/agents"
copy_dir ".claude" ".claude"
copy_dir ".claude-plugins" ".claude-plugins" 1
replace_dir ".agents" ".agents"
replace_dir ".codex" ".codex"

if [[ "${INCLUDE_AGENTS_MD}" == "1" ]]; then
  copy_file "AGENTS.md" "AGENTS.md"
fi

echo "Copy complete."
