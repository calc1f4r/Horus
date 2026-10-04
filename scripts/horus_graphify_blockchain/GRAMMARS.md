# Grammar Sources — horus-graphify-blockchain

This file documents the tree-sitter grammar source, version, and status for each supported blockchain language.
**Executing agents: verify these before implementing. If a grammar is broken or missing, document here and skip.**

## Phase 2a (Implemented)

| Language | Extension | Grammar Package | PyPI | Source Repo | Status |
|----------|-----------|-----------------|------|-------------|--------|
| Solidity | `.sol` | `tree-sitter-solidity==1.2.13` | Yes | `JoranHonig/tree-sitter-solidity` | Verified on Python 3.12; tree-sitter extraction active |
| Move (Sui) | `.move` | `tree-sitter-move==0.0.2` | Yes, broken wheel | Various forks — canonical Sui source still needs confirmation | Import fails with `invalid ELF header`; regex fallback active |
| Cairo 1.x | `.cairo` | `tree-sitter-cairo==0.0.2` | Yes, broken deps | `starkware-libs/tree-sitter-cairo` | Import fails because package requires missing `typed_parser`; regex fallback active |

## Phase 2b (Not Yet Implemented)

| Language | Extension | Grammar Package | Source Repo | Notes |
|----------|-----------|-----------------|-------------|-------|
| Vyper | `.vy`, `.vyi` | `tree-sitter-vyper` | Search GitHub | EVM alternative to Solidity |
| Sway | `.sw` | `tree-sitter-sway` | `FuelLabs/sway` tree-sitter subdir | Fuel Network |
| Tact | `.tact` | `tree-sitter-tact` | `tact-lang/tree-sitter-tact` | TON |
| FunC | `.fc` | `tree-sitter-func` | Search GitHub | TON legacy |

## Languages Handled by graphify Natively (NO extraction needed here)

- **Rust** (`.rs`) — Solana, NEAR, Polkadot ink!, CosmWasm, Stellar Soroban
- **Go** (`.go`) — Cosmos SDK, IBC
- **Python** (`.py`) — test harnesses, scripts
- **TypeScript / JavaScript** (`.ts`, `.js`) — Hardhat/Foundry scripts, frontend

## Node Type Mapping Conventions

When implementing a new language module, use these mappings as a reference:

| Concept | Solidity | Move | Cairo | graphify node_kind |
|---------|----------|------|-------|--------------------|
| Top-level declaration | `contract_declaration` | `module_definition` | `mod_item` | `Module` |
| Callable unit | `function_definition` | `function_definition` | `function_declaration` | `Function` |
| Storage slot | `state_variable_declaration` | (struct fields via `#[storage]`) | `Storage` struct field | `StateVar` |
| User type | `struct_definition` | `struct_definition` | `struct_item` | `Struct` |
| Access gate | `modifier_definition` | attribute / `#[...` | attribute | `Modifier` |
| Side effect signal | `event_definition` | (Move events via emit) | `#[event]` enum | `Event` |

## Installation Instructions (for the implementing agent)

```bash
# Try modern API first (tree-sitter >= 0.21):
pip install tree-sitter tree-sitter-solidity

# Test:
python3 -c "
import tree_sitter_solidity
from tree_sitter import Language, Parser
lang = Language(tree_sitter_solidity.language())
parser = Parser(lang)
tree = parser.parse(b'contract Foo {}')
print(tree.root_node.type)  # should print 'source_file'
"

# If tree-sitter-solidity not on PyPI, try tree-sitter-languages bundle:
pip install tree-sitter-languages
python3 -c "import tree_sitter_languages; lang = tree_sitter_languages.get_language('solidity'); print(lang)"
```

If neither works for a language: the regex fallback in each language module activates automatically. Document the failure here and move on.

## Verification Log

Verified on 2026-04-28 in `/tmp/horus-test-venv`:

```bash
pip install tree-sitter-solidity tree-sitter-cairo tree-sitter-move
horus-graphify-blockchain languages
pytest scripts/horus_graphify_blockchain/tests/ -v
```

Results:

- Solidity: grammar import succeeds; test suite passes with tree-sitter active.
- Move: PyPI package installs, but importing `tree_sitter_move` fails with an invalid ELF header.
- Cairo: PyPI package installs, but importing `tree_sitter_cairo` fails due missing `typed_parser`.
- Fallback extraction remains enabled for Move and Cairo, and the v1 test suite passes through those fallbacks.
