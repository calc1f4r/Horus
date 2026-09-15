---
description: Conventions for the cross-audit lesson memory at ~/.horus/lessons.db (lessons_db.py)
globs: ["scripts/lessons_db.py"]
---

# Lessons DB Conventions

## Location

`~/.horus/lessons.db` — SQLite database, user-local, never committed to the repo.

## Schema

FTS5 virtual table `lessons` with columns:
- `ecosystem` — evm, solana, cosmos, sui, starknet, ton, fuel, multi
- `protocol_type` — lending_protocol, dex_amm, vault_yield, governance_dao, cross_chain_bridge, etc.
- `phase` — which audit phase generated the lesson (e.g., `4-protocol-reasoning`)
- `category` — vulnerability class: `oracle`, `access_control`, `reentrancy`, `arithmetic`, `logic`, `bridge`, `dos`, `governance`, `flash_loan`, `liquidation`, `other`
- `severity` — CRITICAL, HIGH, MEDIUM, LOW
- `lesson` — the FTS-indexed lesson text (scrubbed of PII)
- `related_hunt_cards` — space-separated hunt card IDs
- Stored unindexed: `audit_id`, `date`, `client_tag`, `finding_id`

## Privacy

**Default: no memory.** Lessons are only stored when the user explicitly opts in:
- CLI: `python3 scripts/lessons_db.py ingest <dir> --memory`
- Env: `HORUS_MEMORY=1`

Privacy scrub removes before storage: Ethereum addresses (`0x[0-9a-fA-F]{40}`), IPv4/IPv6, email addresses, API keys/secrets.

## Subcommands

```bash
python3 scripts/lessons_db.py init                        # create DB (idempotent)
python3 scripts/lessons_db.py ingest <audit-dir> [opts]   # parse CONFIRMED-REPORT.md
python3 scripts/lessons_db.py query [--ecosystem] [--protocol-type] [--topic] [--limit N]
python3 scripts/lessons_db.py purge --client-tag <tag>    # GDPR delete
python3 scripts/lessons_db.py stats                       # row counts by ecosystem/category
```

## Integration Points

- `report-aggregator` agent: after writing `CONFIRMED-REPORT.md`, if `HORUS_MEMORY=1`, run `python3 scripts/lessons_db.py ingest <audit-output-dir> --memory`
- `audit-orchestrator` Phase 0: query lessons for warm-start context via `lessons_db.py query`
- Do NOT auto-ingest without the opt-in flag — that violates the privacy contract

## Lesson Categories (classify_category heuristics)

| Keywords | Category |
|----------|----------|
| oracle, price, twap, chainlink, stale | oracle |
| owner, admin, role, access, onlyOwner | access_control |
| reentr, callback, fallback, hook | reentrancy |
| overflow, underflow, precision, rounding | arithmetic |
| flash, loan, atomic | flash_loan |
| bridge, relay, message, cross-chain | bridge |
| governance, proposal, vote, timelock | governance |
| liquidat, collateral, health | liquidation |
| dos, grief, lock, brick | dos |
| (else) | other |
