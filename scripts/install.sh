#!/usr/bin/env bash
# install.sh — symlink scripts/horus into a PATH directory and seed minimal state.json.
#
# Idempotent. Does not run bootstrap. After this completes, run `horus bootstrap`
# to install the venv + graphify + blockchain extractor.
#
# Override target dir via HORUS_BIN_DIR (default: $HOME/.local/bin).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HORUS_BIN="$SCRIPT_DIR/horus"
TARGET_DIR="${HORUS_BIN_DIR:-$HOME/.local/bin}"
TARGET="$TARGET_DIR/horus"
STATE_DIR="$HOME/.horus"
STATE_FILE="$STATE_DIR/state.json"

# --- preconditions ------------------------------------------------------------

if [ ! -f "$HORUS_BIN" ]; then
    echo "[error] $HORUS_BIN not found" >&2
    exit 1
fi
if [ ! -x "$HORUS_BIN" ]; then
    chmod +x "$HORUS_BIN"
fi

# --- symlink ------------------------------------------------------------------

mkdir -p "$TARGET_DIR"

if [ -L "$TARGET" ]; then
    EXISTING=$(readlink "$TARGET")
    if [ "$EXISTING" = "$HORUS_BIN" ]; then
        echo "[info] $TARGET already points at $HORUS_BIN"
    else
        ln -sf "$HORUS_BIN" "$TARGET"
        echo "[info] updated $TARGET (was: $EXISTING)"
    fi
elif [ -e "$TARGET" ]; then
    echo "[error] $TARGET exists and is not a symlink — refusing to overwrite" >&2
    echo "[error] move it aside or set HORUS_BIN_DIR to a different directory" >&2
    exit 1
else
    ln -s "$HORUS_BIN" "$TARGET"
    echo "[info] linked $TARGET -> $HORUS_BIN"
fi

# --- seed state.json ----------------------------------------------------------

mkdir -p "$STATE_DIR"

if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" <<EOF
{
  "repo_path": "$REPO_ROOT",
  "schema_version": 1
}
EOF
    echo "[info] wrote $STATE_FILE"
elif command -v python3 >/dev/null 2>&1; then
    python3 - "$STATE_FILE" "$REPO_ROOT" <<'PY'
import json, sys
state_path, repo = sys.argv[1], sys.argv[2]
try:
    with open(state_path) as f:
        state = json.load(f)
    if not isinstance(state, dict):
        state = {}
except (OSError, json.JSONDecodeError):
    state = {}
changed = False
if state.get("repo_path") != repo:
    state["repo_path"] = repo
    changed = True
if state.get("schema_version") != 1:
    state["schema_version"] = 1
    changed = True
if changed:
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    print(f"[info] updated repo_path in {state_path}")
PY
fi

# --- PATH check ---------------------------------------------------------------

case ":${PATH}:" in
    *":$TARGET_DIR:"*)
        ;;
    *)
        echo "[warn] $TARGET_DIR is not on PATH" >&2
        echo "       add this to your shell rc (~/.bashrc / ~/.zshrc):" >&2
        echo "         export PATH=\"$TARGET_DIR:\$PATH\"" >&2
        ;;
esac

echo "[info] install.sh done. next: 'horus bootstrap' to install venv + dependencies."
