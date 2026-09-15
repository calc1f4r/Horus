"""horus_cli — implementation modules for the `horus` CLI dispatcher.

Module map (one slice per module):
    bootstrap         S02
    doctor            S03
    graph             S05 (init), S06 (verify), S05 (update)
    db                S04
    install_runtime   S07 (claude), S12 (codex)
    lifecycle         S10 (update + uninstall)

Shared helpers live in `common`. Stubs for not-yet-implemented slices live in `_stub`.
"""
