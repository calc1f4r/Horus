"""
File-extension to language detection for blockchain DSLs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

EXTENSION_MAP: dict[str, str] = {
    ".sol":  "solidity",
    ".vy":   "vyper",
    ".vyi":  "vyper",
    ".move": "move",      # Disambiguated below via Move.toml
    ".cairo":"cairo",
    ".sw":   "sway",
    ".tact": "tact",
    ".fc":   "func",      # TON FunC
}

# graphify already handles these natively — skip to avoid double-extraction
GRAPHIFY_NATIVE = {".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp", ".rb", ".cs", ".kt", ".scala", ".php"}

_SUI_MARKERS   = ["[dependencies.Sui]", '"sui"', "sui-framework", "0x2::"]
_APTOS_MARKERS = ["[dependencies.AptosFramework]", "aptos-framework", "@aptos-labs", "0x1::aptos"]


def detect_language(file_path: str | Path, project_root: str | Path | None = None) -> Optional[str]:
    """Return the blockchain language name for a file, or None if unsupported."""
    path = Path(file_path)
    if path.suffix.lower() in GRAPHIFY_NATIVE:
        return None                    # let graphify handle these
    lang = EXTENSION_MAP.get(path.suffix.lower())
    if lang == "move" and project_root:
        lang = _detect_move_dialect(Path(project_root))
    return lang


def _detect_move_dialect(project_root: Path) -> str:
    """Read Move.toml to pick between move_sui and move_aptos."""
    for candidate in [project_root / "Move.toml", project_root.parent / "Move.toml"]:
        if candidate.exists():
            text = candidate.read_text(errors="ignore").lower()
            if any(m.lower() in text for m in _SUI_MARKERS):
                return "move_sui"
            if any(m.lower() in text for m in _APTOS_MARKERS):
                return "move_aptos"
    return "move_sui"   # safe default (Sui is more common in Horus DB)


def iter_blockchain_files(directory: str | Path) -> Iterator[tuple[str, str]]:
    """
    Yield (absolute_file_path, language) for all supported blockchain files
    under the given directory, skipping hidden dirs, node_modules, and build artifacts.
    """
    root = Path(directory)
    skip_dirs = {"node_modules", ".git", "target", "build", "out", "artifacts", "__pycache__", ".venv"}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        lang = detect_language(path, root)
        if lang:
            yield str(path), lang
