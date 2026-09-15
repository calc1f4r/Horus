#!/usr/bin/env bash
# Test S01: scripts/horus dispatcher + scripts/install.sh.
#
# Behavior verified:
#   - install.sh creates ~/.local/bin/horus symlink (in tmp HOME).
#   - install.sh seeds ~/.horus/state.json with repo_path + schema_version.
#   - install.sh is idempotent (rerun produces no error).
#   - `horus --help`, `-h`, `help`, and bare `horus` all exit 0.
#   - Unknown top-level subcommand exits 2.
#   - Each implemented dispatcher route (bootstrap, doctor, graph, graph init,
#     db, db graph, install-runtime claude, update, uninstall) reaches its
#     stub module and exits 0.
#   - Unknown sub-subcommand under `graph` / `db` / `install-runtime` exits 2.
#   - HORUS_HOME env var overrides state.json resolution.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_HOME="$(mktemp -d)"
trap 'rm -rf "$TMP_HOME"' EXIT

export HOME="$TMP_HOME"
export HORUS_BIN_DIR="$TMP_HOME/.local/bin"
export PATH="$HORUS_BIN_DIR:$PATH"
unset HORUS_HOME || true

fail() {
    echo "FAIL: $1" >&2
    exit 1
}

# --- 1. install.sh creates symlink + state.json ------------------------------

bash "$REPO_ROOT/scripts/install.sh" >/dev/null 2>&1 || fail "install.sh exit nonzero"
[ -L "$HORUS_BIN_DIR/horus" ] || fail "symlink not created"
[ "$(readlink "$HORUS_BIN_DIR/horus")" = "$REPO_ROOT/scripts/horus" ] \
    || fail "symlink target wrong"
[ -f "$TMP_HOME/.horus/state.json" ] || fail "state.json not seeded"

REPO_FROM_STATE=$(python3 -c "import json; print(json.load(open('$TMP_HOME/.horus/state.json'))['repo_path'])")
[ "$REPO_FROM_STATE" = "$REPO_ROOT" ] || fail "state.json repo_path wrong: $REPO_FROM_STATE"

SCHEMA=$(python3 -c "import json; print(json.load(open('$TMP_HOME/.horus/state.json'))['schema_version'])")
[ "$SCHEMA" = "1" ] || fail "state.json schema_version wrong: $SCHEMA"

# --- 2. install.sh idempotent ------------------------------------------------

bash "$REPO_ROOT/scripts/install.sh" >/dev/null 2>&1 || fail "install.sh second run failed"

# --- 3. help variants exit 0 -------------------------------------------------

horus --help >/dev/null || fail "horus --help nonzero"
horus -h >/dev/null     || fail "horus -h nonzero"
horus help >/dev/null   || fail "horus help nonzero"
horus >/dev/null        || fail "bare horus nonzero"

# --- 4. unknown subcommand exits 2 -------------------------------------------

set +e
horus completely-bogus-subcmd >/dev/null 2>&1
RC=$?
set -e
[ "$RC" = "2" ] || fail "unknown subcommand exit code: expected 2 got $RC"

# --- 5. dispatcher routes reach stubs (exit 0) -------------------------------

for cmd in "bootstrap" "doctor" "graph" "graph init" "graph verify" "graph update" \
           "db" "db graph" "install-runtime" "install-runtime claude" \
           "install-runtime codex" "update" "uninstall"; do
    # shellcheck disable=SC2086
    horus $cmd >/dev/null 2>&1 || fail "horus $cmd nonzero"
done

# --- 6. unknown sub-subcommands exit 2 ---------------------------------------

set +e
horus graph bogus >/dev/null 2>&1; [ $? -eq 2 ] || { set -e; fail "graph bogus should exit 2"; }
horus db bogus >/dev/null 2>&1; [ $? -eq 2 ] || { set -e; fail "db bogus should exit 2"; }
horus install-runtime bogus >/dev/null 2>&1; [ $? -eq 2 ] || { set -e; fail "install-runtime bogus should exit 2"; }
set -e

# --- 7. HORUS_HOME env override ----------------------------------------------

OVERRIDE_DIR="$TMP_HOME/alt-horus"
mkdir -p "$OVERRIDE_DIR/scripts"
HORUS_HOME="$OVERRIDE_DIR" horus --help >/dev/null || fail "HORUS_HOME override failed"

echo "PASS: S01 dispatcher tests"
