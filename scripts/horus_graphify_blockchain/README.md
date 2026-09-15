# horus-graphify-blockchain

Tree-sitter-backed blockchain DSL extractor for Horus graph workflows.

The CLI emits graphify-compatible JSON with `nodes`, `edges`, and `hyperedges`
arrays. It is intentionally additive: when a grammar package is unavailable,
the extractor falls back to conservative regex extraction so Phase 0 can still
produce useful codebase graph context.

## Install

```bash
pip install -e scripts/horus_graphify_blockchain/
```

Optional grammar packages can be installed per language:

```bash
pip install tree-sitter-solidity tree-sitter-cairo tree-sitter-move
```

See `GRAMMARS.md` for current grammar verification status.

## Usage

```bash
horus-graphify-blockchain languages
horus-graphify-blockchain extract <path> --out audit-output/graph/blockchain-ast.json
```

Supported v1 languages:

- Solidity (`.sol`)
- Move / Sui Move (`.move`)
- Cairo (`.cairo`)

Graphify already handles Rust, Go, Python, TypeScript, JavaScript, and other
general-purpose languages directly, so this package skips those files.

## Known Limitations

- No inter-procedural data flow.
- Solidity inheritance is declared but not flattened.
- Cross-file call resolution is not implemented in v1.
- External calls are detected as unresolved graph edges.
- Reentrancy is not detected by this extractor; downstream Horus agents reason
  over the emitted graph and invariant suite.
