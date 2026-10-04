"""Shared paths, state, and logging for horus CLI subcommands.

State file: ~/.horus/state.json
    {
      "repo_path": "...",          # written by install.sh
      "venv_path": "...",          # written by horus bootstrap (S02)
      "graphify_version": "...",   # written by horus bootstrap (S02)
      "installed_at": "...",       # ISO 8601 UTC
      "schema_version": 1
    }
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

STATE_SCHEMA_VERSION = 1
GRAPH_SCHEMA_VERSION = 1


# --- paths -------------------------------------------------------------------


def state_path() -> Path:
    return Path.home() / ".horus" / "state.json"


def horus_home() -> Path:
    """Resolve Horus repo path.

    Priority: $HORUS_HOME env > state.json["repo_path"] > error.
    install.sh seeds state.json["repo_path"] so the second branch is the
    common case after install.
    """
    env = os.environ.get("HORUS_HOME")
    if env:
        return Path(env).resolve()
    state = read_state()
    repo = state.get("repo_path")
    if repo:
        return Path(repo).resolve()
    raise RuntimeError(
        "cannot resolve Horus repo path; set HORUS_HOME or run scripts/install.sh"
    )


def venv_python() -> Path | None:
    """Return path to the bootstrapped venv python, or None if not yet installed."""
    state = read_state()
    venv = state.get("venv_path")
    if not venv:
        return None
    py = Path(venv) / "bin" / "python3"
    return py if py.exists() else None


# --- state file -------------------------------------------------------------


def read_state() -> dict[str, Any]:
    """Read state.json. Returns {} if missing or unreadable."""
    p = state_path()
    if not p.exists():
        return {}
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def write_state(data: dict[str, Any]) -> None:
    """Write state.json atomically (temp file + rename)."""
    p = state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    tmp.replace(p)


# --- logging ----------------------------------------------------------------

_USE_COLOR = sys.stderr.isatty() and os.environ.get("NO_COLOR", "") == ""
_RED = "\033[31m" if _USE_COLOR else ""
_YELLOW = "\033[33m" if _USE_COLOR else ""
_GREEN = "\033[32m" if _USE_COLOR else ""
_BLUE = "\033[34m" if _USE_COLOR else ""
_RESET = "\033[0m" if _USE_COLOR else ""


def log_info(msg: str) -> None:
    print(f"{_BLUE}[info]{_RESET} {msg}", file=sys.stderr)


def log_warn(msg: str) -> None:
    print(f"{_YELLOW}[warn]{_RESET} {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"{_RED}[error]{_RESET} {msg}", file=sys.stderr)


def log_pass(msg: str) -> None:
    print(f"{_GREEN}[pass]{_RESET} {msg}", file=sys.stderr)
