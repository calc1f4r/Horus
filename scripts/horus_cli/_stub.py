"""Shared stub for slices not yet implemented.

Each subcommand module under horus_cli/ that has no real implementation yet
calls `stub(slice_id, name)` and exits 0. The dispatcher and tests can verify
routing without depending on concrete behavior.
"""

from __future__ import annotations

from . import common


def stub(slice_id: str, name: str) -> int:
    common.log_warn(
        f"`horus {name}` not yet implemented — see issues/{slice_id}-*.md"
    )
    return 0
