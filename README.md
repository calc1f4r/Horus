<div align="center">

# Horus

**A vulnerability knowledge base and agentic audit system for smart contract security.**

Look up what is already known to be broken. Scan your codebase against every recorded attack pattern. Run a full contest-grade audit with proof and judging built in.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DB Entries](https://img.shields.io/badge/entries-337-brightgreen)](DB)
[![Patterns](https://img.shields.io/badge/patterns-2%2C002-brightgreen)](DB/manifests)
[![Hunt Cards](https://img.shields.io/badge/hunt%20cards-1%2C560-red)](DB/manifests/huntcards)
[![Exploits](https://img.shields.io/badge/exploits-875-orange)](DeFiHackLabs)
[![Raw Reports](https://img.shields.io/badge/raw%20reports-22%2C287-yellow)](https://github.com/calc1f4r/Horus/branches/all?query=reports%2F)
[![Agents](https://img.shields.io/badge/audit%20agents-49-blueviolet)](docs/agents-reference.md)

</div>

---

## What you can do with Horus

**Look up a vulnerability topic.** 337 curated entries covering 15 categories: oracle manipulation, lending and liquidation, bridges, AMMs, MEV, access control, zk-rollups, Solana, Sui Move, Cosmos, Substrate, BNB Chain, Ethereum L1 clients, account abstraction, and more. Each entry gives you the root cause, detection patterns, false-positive guards, exploit scenarios, and references to the incidents and audits behind it. A lookup takes minutes and reads about forty lines, not whole files. Start in [docs/workflows/db-lookup.md](docs/workflows/db-lookup.md).

**Scan a codebase against every known pattern.** 1,560 hunt cards each carry a grep pattern plus a verify checklist. Point the scanner at a repo and it keeps only the cards whose pattern actually hits, then shards the survivors for parallel review. Scope it to your diff when you only changed a few files. See [docs/workflows/bulk-scan.md](docs/workflows/bulk-scan.md).

**Run a full audit.** One command starts an 11-phase pipeline: scope, context, invariants, four discovery lanes plus an economic lane, falsified triage, executable PoCs, profitability checks on economic attacks, three-platform judging, and a report containing only findings that survived all of it. See [docs/workflows/full-audit.md](docs/workflows/full-audit.md).

**Audit any language, not just Solidity.** The pipeline detects the target's language and ecosystem (EVM contracts, Solana programs, Move, Cosmos SDK chains, Rust/Go/C++ services and L1 nodes) and works in its idioms, translating patterns documented in other languages instead of assuming EVM. Formal-verification suites run where a toolchain exists (EVM, Sui) and skip with a logged reason elsewhere.

**Verify fixes.** After a sponsor ships patches, run a mitigation review: every original finding gets FIXED, PARTIALLY FIXED, NOT FIXED, or FIXED BUT INTRODUCED NEW ISSUE, with the fix diff itself audited for regressions. See [docs/workflows/mitigation-review.md](docs/workflows/mitigation-review.md).

## The knowledge base

| | |
|---|---|
| Curated entries | 337 across 18 manifests and 15 categories |
| Indexed patterns | 2,002, each with severity and exact line ranges |
| Hunt cards | 1,560 compressed detection rules |
| Keyword index | 13,498 term → manifest mappings |
| Real exploits | 875 incidents with executable PoCs (DeFiHackLabs, 2017-07 to 2026-09) |
| Raw audit reports | 22,287 findings fetched from Solodit, split across 49 `reports/*` branches |
| Protocol contexts | 17: lending, DEX, vault, bridge, perps, L2 rollup, smart accounts, Solana, Sui Move, Cosmos, Substrate, BNB Chain, Ethereum L1 clients, and more |
| Related-variant graph | 7,150 nodes and 63,963 edges connecting patterns that share root causes |
| Audit agents | 49, mirrored across Claude Code, Codex, and GitHub runtimes |

Retrieval is tiered so you read as little as possible: the index routes you to a manifest, the manifest gives you exact line ranges, and you read those lines. The graph expands a hit to its cousins. Nothing requires loading the whole database.

## Getting started

Install the CLI and bootstrap:

```bash
./scripts/install.sh && horus bootstrap
```

Then, from whatever runtime you use:

- **Claude Code** — start with [`CLAUDE.md`](CLAUDE.md)
- **Codex CLI** — start with [`AGENTS.md`](AGENTS.md)
- **Gemini CLI** — start with [`GEMINI.md`](GEMINI.md)
- **Cursor / VS Code** — the files above work as workspace instructions

Run a full audit:

```
/agent audit-orchestrator <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
```

Hunt one topic on one codebase:

```
/agent invariant-catcher <codebase-path> --topic "oracle staleness"
```

Rebuild the knowledge graph on demand:

```bash
horus db graph
```

## Documentation

| Doc | For |
|---|---|
| [docs/workflows/](docs/workflows) | Every workflow start to finish: which skills do what |
| [docs/agents-reference.md](docs/agents-reference.md) | All 49 agents: what each does and when to use it |
| [docs/db-guide.md](docs/db-guide.md) | The knowledge base in depth |
| [DB/SEARCH_GUIDE.md](DB/SEARCH_GUIDE.md) | Worked retrieval examples |
| [docs/agentic-workflow.md](docs/agentic-workflow.md) | System overview |

## Authors

- **Yash Srivastava (calc1f4r)** — [github.com/calc1f4r](https://github.com/calc1f4r)
- **Tushar Bhatia (tushar1698)** — [github.com/tushar1698](https://github.com/tushar1698)

## License

MIT. See [`LICENSE`](LICENSE).
