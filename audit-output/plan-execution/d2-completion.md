# D2 Completion — horus-graphify-blockchain v1

Status: complete for v1 languages: Solidity, Move/Sui fallback, Cairo fallback.

## Changes

- Fixed package build backend to `setuptools.build_meta`.
- Added missing `README.md`.
- Fixed Solidity tree-sitter traversal through `contract_body` and `function_body`.
- Strengthened Solidity regex fallback to emit state vars, modifiers, functions,
  events, and `declares` edges.
- Updated `GRAMMARS.md` with verified package versions and failure notes.

## Validation

Install:

```bash
/tmp/horus-test-venv/bin/pip install -e scripts/horus_graphify_blockchain/
```

Tests:

```bash
/tmp/horus-test-venv/bin/python -m pytest scripts/horus_graphify_blockchain/tests/ -v
```

Result: 20 passed, 1 deprecation warning from `tree_sitter.Language(...)`.

CLI smoke test:

```bash
/tmp/horus-test-venv/bin/horus-graphify-blockchain extract scripts/horus_graphify_blockchain/tests/fixtures/solidity/ERC20.sol --out /tmp/erc20-ast.json
```

Result: 17 nodes, 36 edges, 0 hyperedges.

## Grammar Status

- Solidity: `tree-sitter-solidity==1.2.13` works.
- Move: `tree-sitter-move==0.0.2` installs but import fails with invalid ELF header.
- Cairo: `tree-sitter-cairo==0.0.2` installs but import fails due missing `typed_parser`.

