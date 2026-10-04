"""horus install-runtime <claude|codex>.

claude — stub
codex  — stub
"""

from __future__ import annotations

import sys

from . import _stub

USAGE = "Usage: horus install-runtime <claude|codex>"

_SLICE_MAP = {
    "claude": ("S07", "install-runtime claude"),
    "codex":  ("S12", "install-runtime codex"),
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    runtime = argv[0]
    if runtime not in _SLICE_MAP:
        print(f"horus install-runtime: unknown runtime: {runtime}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    slice_id, name = _SLICE_MAP[runtime]
    return _stub.stub(slice_id, name)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
