"""horus update / horus uninstall — stub.

Invoked via the dispatcher as `horus update` or `horus uninstall`. The
dispatcher passes the verb as argv[0] so this module sees its own action.
"""

from __future__ import annotations

import sys

from . import _stub

USAGE = "Usage: horus <update|uninstall>"

_VERBS = {"update", "uninstall"}


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    verb = argv[0]
    if verb not in _VERBS:
        print(f"horus lifecycle: unknown verb: {verb}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    return _stub.stub("S10", verb)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
