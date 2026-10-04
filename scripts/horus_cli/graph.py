"""horus graph <init|verify|update>.

init   — stub
verify — stub
update — stub (incremental rebuild)
"""

from __future__ import annotations

import sys

from . import _stub

USAGE = "Usage: horus graph <init|verify|update> [args...]"

_SLICE_MAP = {
    "init":   ("S05", "graph init"),
    "verify": ("S06", "graph verify"),
    "update": ("S05", "graph update"),
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    sub = argv[0]
    if sub not in _SLICE_MAP:
        print(f"horus graph: unknown subcommand: {sub}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    slice_id, name = _SLICE_MAP[sub]
    return _stub.stub(slice_id, name)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
